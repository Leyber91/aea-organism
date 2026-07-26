"""listen.py - the entity's EARS. Offline speech-to-text: Whisper-base (multilingual - English
and Spanish both work) through the same sherpa-onnx wheel the voice uses. LOCAL only: what you
say to your entity never leaves this machine.

  python listen.py --selftest          # PROOF with no microphone: Kokoro speaks a sentence to a
                                       # wav, Whisper transcribes it back, texts must match
  python listen.py --mic 6             # record 6s from the default mic, print what it heard
  python listen.py file.wav            # transcribe a wav file
  python listen.py --mic 6 --lang es   # Spanish

Mic capture: sounddevice (pip wheel, PortAudio rides inside - passes AppLocker like the rest).
"""
from __future__ import annotations
import os, sys, glob, time, wave, struct

from aea.kernel import grid

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

HERE = grid.HERE
WHISPER = os.path.join(grid.ROOT, "voice", "sherpa-onnx-whisper-base")
_recs: dict = {}                # lazy singletons, ONE PER LANGUAGE (a whisper recognizer is
                                # language-bound at construction; a single global _rec silently
                                # served English to Spanish callers - fixed 2026-07-24)
THREADS = 4                     # MEASURED optimum on this 20-core i7-13850HX, do NOT raise:
                                # threads=4 -> 0.19s on a 2.5s clip; threads=16 -> 42s (the ONNX
                                # graph thrashes on oversubscription). More cores is slower here.


def available() -> bool:
    return bool(glob.glob(os.path.join(WHISPER, "*encoder*.onnx")))


def _engine(lang: str = "en"):
    """Lazy per-language recognizer. Whisper pads every input to a fixed 30s window, so decode
    cost is CONSTANT per turn regardless of how short the utterance is."""
    rec = _recs.get(lang)
    if rec is None:
        import sherpa_onnx
        enc = sorted(glob.glob(os.path.join(WHISPER, "*encoder*.onnx")))[0]
        dec = sorted(glob.glob(os.path.join(WHISPER, "*decoder*.onnx")))[0]
        tok = glob.glob(os.path.join(WHISPER, "*tokens*.txt"))[0]
        rec = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=enc, decoder=dec, tokens=tok, language=lang, task="transcribe",
            num_threads=THREADS)
        _recs[lang] = rec
    return rec


def warm(lang: str = "en", rounds: int = 2) -> float:
    """Pay the load + settle cost UP FRONT. Measured: decode 1 ~20s, decode 2 ~6.7s, decode 3+
    ~0.19s. Without this the first thing anyone says costs 20 seconds. Returns seconds spent."""
    t0 = time.time()
    silence = [0.0] * 8000                       # 0.5s at 16k - enough to run the graph
    for _ in range(max(1, rounds)):
        transcribe_samples(silence, 16000, lang)
    return round(time.time() - t0, 1)


def read_wav(path: str):
    """-> (samples float[-1..1], sample_rate). Mono-izes if needed."""
    with wave.open(path, "rb") as w:
        sr, n, ch, sw = w.getframerate(), w.getnframes(), w.getnchannels(), w.getsampwidth()
        raw = w.readframes(n)
    if sw != 2:
        raise ValueError(f"expected 16-bit wav, got {sw*8}-bit")
    ints = struct.unpack(f"<{n*ch}h", raw)
    if ch > 1:
        ints = ints[::ch]
    return [s / 32768.0 for s in ints], sr


def transcribe_wav(path: str, lang: str = "en") -> str:
    samples, sr = read_wav(path)
    return transcribe_samples(samples, sr, lang)


def transcribe_samples(samples, sr: int, lang: str = "en") -> str:
    rec = _engine(lang)
    s = rec.create_stream()
    s.accept_waveform(sr, samples)          # sherpa resamples to 16k internally
    rec.decode_stream(s)
    return (s.result.text or "").strip()


def record(seconds: float = 6.0, sr: int = 16000):
    """Push-to-talk capture from the default microphone. Returns (samples, sr)."""
    import sounddevice as sd
    print(f"listening ({seconds:.0f}s)...")
    buf = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="float32")
    sd.wait()
    samples = [float(x) for x in buf[:, 0]]
    rms = (sum(x * x for x in samples) / max(1, len(samples))) ** 0.5
    return samples, sr, rms


def hear(seconds: float = 6.0, lang: str = "en") -> str:
    """Record + transcribe in one move - the husk's ear."""
    samples, sr, rms = record(seconds)
    if rms < 0.0015:
        return ""                            # silence - nothing said
    return transcribe_samples(samples, sr, lang)


def selftest() -> bool:
    """No-microphone proof: the mouth speaks, the ears must understand it."""
    import re
    from aea.io import speak
    sentence = "The vault code is seven three nine one, and the entity keeps it private."
    wav = os.path.join(grid.ROOT, "voice", "_selftest.wav")
    print("MOUTH->EARS ROUND TRIP")
    r = speak.kokoro_render(sentence, wav, sid=6)
    if not r["ok"]:
        print(f"  render failed: {r.get('error')}"); return False
    print(f"  spoke   : {sentence}")
    t0 = time.time()
    heard = transcribe_wav(wav)
    print(f"  heard   : {heard}   ({round(time.time()-t0,1)}s incl model load)")
    norm = lambda t: set(re.findall(r"[a-z']+", t.lower()))
    a, b = norm(sentence), norm(heard)
    overlap = len(a & b) / max(1, len(a))
    print(f"  overlap : {round(100*overlap)}%  -> {'PASS' if overlap >= 0.75 else 'FAIL'}")
    return overlap >= 0.75


if __name__ == "__main__":
    a = sys.argv[1:]
    lang = a[a.index("--lang") + 1] if "--lang" in a else "en"
    if "--selftest" in a:
        sys.exit(0 if selftest() else 1)
    if "--mic" in a:
        secs = float(a[a.index("--mic") + 1]) if a.index("--mic") + 1 < len(a) else 6
        text = hear(secs, lang)
        print(f"heard: {text!r}" if text else "heard: (silence)")
    elif a and a[0].endswith(".wav"):
        print(transcribe_wav(a[0], lang))
    else:
        print(__doc__)
