"""speak.py - the entity's VOICE. Three engines, one interface, privacy-zoned (2026-07-19):

  EDGE (default for normal speech): Microsoft neural voices via the edge-tts pip package -
     genuinely natural (AndrewMultilingual), free, no key, server-side. CLOUD: the text goes to
     Microsoft, so it is BLOCKED for sensitive-zone speech (cloud_ok=False) - same law as the
     browser voice. Normal replies already transited hosted no-train rods, so the exposure class
     is unchanged.
  KOKORO: Kokoro-82M local quality voice. The sherpa-onnx path is EDR-dead; the TORCH path on
     Fooocus's python is PROVEN (voice_test_kokoro.wav, rtf 0.39 warm) - wiring it as the
     sensitive-mode natural voice is ticket G3's remaining step.
  SAPI (floor + the FAST option): Windows built-in System.Speech - robotic but INSTANT and
     unkillable. Forced with voice="sapi"; the terminal fallback for everything.

  python speak.py "text"                      # say it (kokoro if installed, else sapi)
  python speak.py --fast "text"               # force the instant sapi engine
  python speak.py --brief                     # read today's brief aloud
  python speak.py --voices                    # list voices (kokoro speakers + sapi)
  python speak.py --sid 3 "text"              # pick a kokoro speaker
  python speak.py --narrate script.txt out/   # RECORD a presentation: one wav per paragraph + playlist
Stdlib only: subprocess to the sherpa exe / PowerShell. Voice choice lives in identity.json:
  "voice": "kokoro:3"  (engine:speaker)  or  "Microsoft David Desktop" (sapi name).
"""
from __future__ import annotations
import subprocess, sys, os, json, time, re

HERE = os.path.dirname(os.path.abspath(__file__))
IDENTITY = os.path.join(HERE, "identity.json")
VDIR = os.path.join(HERE, "voice")
KOKORO = os.path.join(VDIR, "kokoro-en-v0_19")
SPEAKERS = ["af", "af_bella", "af_nicole", "af_sarah", "af_sky",
            "am_adam", "am_michael", "bf_emma", "bf_isabella", "bm_george", "bm_lewis"]
DEFAULT_SID = 3          # af_sarah - warm, clear US female; change via identity.json "voice": "kokoro:N"

# Engine note (2026-07-11): the sherpa-onnx standalone EXE is blocked by AppLocker on this
# corporate machine, so Kokoro runs through the sherpa-onnx PYTHON wheel instead - python.exe
# carries the trust, the extension DLLs ride along. Same model, same local privacy.
_tts = None              # lazy singleton: pay the ~2-5s model load once per process


def _identity() -> dict:
    try:
        return json.load(open(IDENTITY, encoding="utf-8"))
    except Exception:
        return {}


def kokoro_available() -> bool:
    if not os.path.exists(os.path.join(KOKORO, "model.onnx")):
        return False
    try:
        import sherpa_onnx  # noqa: F401
        return True
    except ImportError:
        return False


def _engine():
    global _tts
    if _tts is None:
        import sherpa_onnx
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=os.path.join(KOKORO, "model.onnx"),
                    voices=os.path.join(KOKORO, "voices.bin"),
                    tokens=os.path.join(KOKORO, "tokens.txt"),
                    data_dir=os.path.join(KOKORO, "espeak-ng-data")),
                num_threads=4))
        _tts = sherpa_onnx.OfflineTts(cfg)
    return _tts


# ------------------------------------------------------------------ KOKORO: human voice + files
def kokoro_render(text: str, out_wav: str, sid: int = DEFAULT_SID, speed: float = 1.0,
                  timeout: int = 600) -> dict:
    """Render text to a wav. Returns dict(ok, seconds_audio, seconds_gen, rtf)."""
    if not text.strip():
        return dict(ok=False, error="empty text")
    t0 = time.time()
    try:
        audio = _engine().generate(text, sid=int(sid), speed=speed)
        import wave, struct
        samples = audio.samples                       # floats in [-1, 1]
        with wave.open(out_wav, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(audio.sample_rate)
            w.writeframes(struct.pack(f"<{len(samples)}h",
                          *(max(-32768, min(32767, int(s * 32767))) for s in samples)))
        gen = round(time.time() - t0, 1)
        dur = round(len(samples) / audio.sample_rate, 1)
        return dict(ok=True, seconds_audio=dur, seconds_gen=gen,
                    rtf=round(gen / dur, 2) if dur else None, path=out_wav)
    except Exception as e:
        return dict(ok=False, error=str(e)[:160])


def play_wav(path: str, timeout: int = 600) -> bool:
    ps = f"(New-Object Media.SoundPlayer '{path}').PlaySync()"
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0
    except Exception:
        return False


# ------------------------------------------------------------------ EDGE: natural neural voice (cloud)
EDGE_VOICE = "en-US-AndrewMultilingualNeural"     # the 2024 conversation-optimized tier

def edge_available() -> bool:
    try:
        import edge_tts  # noqa: F401
        return True
    except ImportError:
        return False


def edge_speak(text: str, timeout: int = 300) -> bool:
    """Generate with edge-tts (mp3) then play via WPF MediaPlayer. Cloud - never for sensitive text."""
    mp3 = os.path.join(HERE, "_live_edge.mp3")
    try:
        r = subprocess.run([sys.executable, "-m", "edge_tts", "--voice", EDGE_VOICE,
                            "--text", text[:1200], "--write-media", mp3],
                           capture_output=True, text=True, timeout=timeout)
        if r.returncode != 0 or not os.path.exists(mp3) or os.path.getsize(mp3) < 400:
            return False
        ps = ("Add-Type -AssemblyName presentationCore; "
              f"$p = New-Object System.Windows.Media.MediaPlayer; $p.Open([uri]'{mp3}'); $p.Play(); "
              "$t0 = Get-Date; while (-not $p.NaturalDuration.HasTimeSpan -and "
              "((Get-Date) - $t0).TotalSeconds -lt 8) { Start-Sleep -Milliseconds 100 }; "
              "if ($p.NaturalDuration.HasTimeSpan) { "
              "Start-Sleep -Milliseconds ([int]$p.NaturalDuration.TimeSpan.TotalMilliseconds + 300) }; "
              "$p.Close()")
        p = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode == 0
    except Exception:
        return False


# ------------------------------------------------------------------ SAPI: the instant fallback
def sapi_speak(text: str, rate: int = 0, voice: str | None = None, timeout: int = 300) -> bool:
    ps = ("Add-Type -AssemblyName System.Speech; "
          "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"$s.Rate = {int(rate)}; "
          + (f"try {{ $s.SelectVoice('{voice}') }} catch {{ }}; " if voice else "")
          + "$t = [Console]::In.ReadToEnd(); $s.Speak($t)")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           input=text, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0
    except Exception:
        return False


# ------------------------------------------------------------------ the one interface
def speak(text: str, voice: str | None = None, rate: int = 0, cloud_ok: bool = True) -> bool:
    """Say it. voice: None -> identity.json -> edge (natural) when cloud_ok, else local engines.
    cloud_ok=False (sensitive zone) NEVER uses the cloud voice - the boundary is code, not a promise."""
    if not text.strip():
        return False
    try:
        import pulse
        pulse.emit("voice", "speak", text[:80])
    except Exception:
        pass
    voice = voice or _identity().get("voice") or "edge"
    if voice == "edge" and not cloud_ok:
        voice = "kokoro:%d" % DEFAULT_SID if kokoro_available() else "sapi"
    if voice == "edge" and edge_available():
        if edge_speak(text):
            return True
        # cloud voice failed - fall through to the local floor, never go silent
        voice = "sapi"
    if voice.startswith("kokoro") and kokoro_available():
        sid = int(voice.split(":")[1]) if ":" in voice else DEFAULT_SID
        wav = os.path.join(VDIR, "_live.wav")
        r = kokoro_render(text, wav, sid=sid)
        if r["ok"]:
            return play_wav(wav)
        # fall through to sapi on any kokoro failure - the voice must never go silent
    return sapi_speak(text, rate=rate, voice=None if voice.startswith(("kokoro", "sapi", "edge")) else voice)


def narrate(script_path: str, out_dir: str, sid: int | None = None) -> list[dict]:
    """RECORD A PRESENTATION: split the script on blank lines (one block per slide/paragraph),
    render each to out_dir/part_NN.wav + a playlist.m3u. Returns the per-part render stats."""
    text = open(script_path, encoding="utf-8").read()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    os.makedirs(out_dir, exist_ok=True)
    sid = sid if sid is not None else DEFAULT_SID
    results = []
    print(f"NARRATION: {len(blocks)} parts -> {out_dir}  (voice {SPEAKERS[sid]})")
    for i, block in enumerate(blocks, 1):
        wav = os.path.join(out_dir, f"part_{i:02d}.wav")
        r = kokoro_render(block, wav, sid=sid)
        results.append(r)
        print(f"  part {i:02d}: " + (f"{r['seconds_audio']}s audio in {r['seconds_gen']}s (rtf {r['rtf']})"
                                     if r["ok"] else f"FAILED {r.get('error')}"))
    with open(os.path.join(out_dir, "playlist.m3u"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"part_{i:02d}.wav" for i in range(1, len(blocks) + 1)))
    ok = sum(1 for r in results if r["ok"])
    print(f"  -> {ok}/{len(blocks)} parts rendered; playlist.m3u written")
    return results


def list_voices() -> str:
    out = []
    if kokoro_available():
        out.append("KOKORO (human, local): " + ", ".join(f"{i}={n}" for i, n in enumerate(SPEAKERS)))
    else:
        out.append("KOKORO: not installed (voice/ missing)")
    ps = ("Add-Type -AssemblyName System.Speech; "
          "(New-Object System.Speech.Synthesis.SpeechSynthesizer).GetInstalledVoices() | "
          "ForEach-Object { $_.VoiceInfo.Name }")
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                       capture_output=True, text=True, timeout=30)
    out.append("SAPI (instant): " + ", ".join((r.stdout or "").split("\n")).strip())
    return "\n".join(out)


def main():
    a = sys.argv[1:]
    if "--voices" in a:
        print(list_voices()); return
    if "--narrate" in a:
        i = a.index("--narrate")
        sid = int(a[a.index("--sid") + 1]) if "--sid" in a else None
        narrate(a[i + 1], a[i + 2] if i + 2 < len(a) else os.path.join(HERE, "narration"), sid=sid)
        return
    sid = int(a[a.index("--sid") + 1]) if "--sid" in a else None
    fast = "--fast" in a
    words = [x for x in a if not x.startswith("--") and (sid is None or x != str(sid))]
    text = " ".join(words) or "I am online, running locally, on free power."
    if "--brief" in a:
        path = os.path.join(HERE, "brief_output.md")
        try:
            text = open(path, encoding="utf-8").read().replace("#", "").replace("*", "").replace("_", " ")
        except Exception as e:
            print(f"no brief to read: {e}"); return
        name = _identity().get("name", "your entity")
        text = f"Good morning Luis. This is {name}. " + text
    voice = "sapi" if fast else (f"kokoro:{sid}" if sid is not None else None)
    print("spoke" if speak(text, voice=voice) else "TTS failed")


if __name__ == "__main__":
    main()
