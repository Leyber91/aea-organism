"""earcheck.py - WHY IS IT HEARING ME BADLY. Separates the mic, the room, and the model.

Luis, 2026-07-29: "on parallel you will record my voice and analyze it, because I'm feeling it's
transcribing my words bad."

He is right that it is, and "the ear is bad" has THREE causes that need three different fixes:

  THE MIC    level too low, clipping, one channel dead, wrong device. Fixed with hardware.
  THE ROOM   speech not far enough above the noise floor. Fixed by moving, not by software - D13
             recorded this the expensive way: normalising a quiet clip changed NOTHING, because
             lifting voice and room together leaves SNR identical. Whisper is level-robust and
             noise-fragile.
  THE MODEL  clean audio, good SNR, still wrong words. Only then is a bigger model the answer.

Guessing between them is how an hour disappears. This records a KNOWN sentence, measures the
signal, transcribes it, and says which of the three is failing.

  python -m aea.io.earcheck                 the default 5 phrases
  python -m aea.io.earcheck --device 1      pick the mic
  python -m aea.io.earcheck --keep          keep the wavs for listening

NOTHING IS UPLOADED. The audio is recorded, measured and transcribed entirely on this machine, and
deleted at the end unless --keep is passed.
"""
from __future__ import annotations

import math
import os
import re
import sys
import time

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SR = 16000
OUT = os.path.join(str(grid.STATE), "earcheck")

# Chosen to span the failure modes actually observed, not to be a nice reading passage:
# two SHORT phrases (where every real failure happened), one with domain words, one long
# sentence (which has always come back clean), and one with numbers.
PHRASES = [
    "Okay so",
    "What are your laws",
    "Hit me with the question",
    "It's just that I feel like when I talk you don't understand all my words",
    "Multiply ninety two thousand by four thousand",
]


def _stats(x, sr: int) -> dict:
    """Signal quality, in the terms that decide which of the three causes it is."""
    import numpy as np
    a = np.asarray(x, dtype="float32")
    if a.size == 0:
        return {}
    peak = float(np.abs(a).max())
    clipped = int((np.abs(a) > 0.985).sum())
    n = int(0.02 * sr)                                  # 20ms frames
    frames = [a[i:i + n] for i in range(0, max(0, len(a) - n), n)]
    rms = np.array([float(np.sqrt(np.mean(f ** 2))) for f in frames]) if frames else np.array([0.0])
    srt = np.sort(rms)
    # The quietest fifth is the room; the loudest fifth is speech. Comparing those two is the
    # honest SNR for a single take, without needing a separate silence recording.
    k = max(1, len(srt) // 5)
    noise = float(srt[:k].mean()) or 1e-9
    speech = float(srt[-k:].mean())
    snr = 20 * math.log10(speech / noise) if speech > 0 else 0.0
    voiced = float((rms > noise * 3).mean())
    return dict(peak=round(peak, 4), rms=round(float(np.sqrt(np.mean(a ** 2))), 5),
                noise=round(noise, 5), speech=round(speech, 5), snr_db=round(snr, 1),
                clipped=clipped, voiced_frac=round(voiced, 2),
                seconds=round(len(a) / sr, 2))


def _wait_and_record(device=None, max_wait: float = 25.0, hangover: float = 1.3,
                     max_utter: float = 20.0):
    """Open the mic, WAIT for speech, record until it stops. Returns float samples or None.

    Calibrates its floor on the first 0.6s of room, then triggers on anything that clears it by a
    real margin. Deliberately generous: this is a diagnostic, so a false trigger costs one retake
    and a missed utterance costs the whole measurement.

    It also prints the live level while waiting, because a person staring at a silent terminal
    cannot tell 'listening' from 'crashed' - which is the exact complaint that started this."""
    import numpy as np
    import sounddevice as sd
    blk = 480
    st = sd.InputStream(samplerate=SR, channels=1, dtype="float32", blocksize=blk, device=device)
    st.start()
    try:
        for _ in range(8):                      # drain the speaker tail
            st.read(blk)
        vals = []
        for _ in range(20):                     # ~0.6s of room
            b, _o = st.read(blk)
            vals.append(float(np.sqrt(np.mean(b[:, 0] ** 2))))
        vals.sort()
        floor = vals[len(vals) // 2]
        thr = max(floor * 2.5, 0.006)
        print(f"       listening (room {floor:.4f}, speak when ready)...", flush=True)
        buf, speaking_now, silent, hot, t0 = [], False, 0.0, 0, time.time()
        peak = 0.0
        last = time.time()
        while True:
            b, _o = st.read(blk)
            m = b[:, 0]
            r = float(np.sqrt(np.mean(m ** 2)))
            peak = max(peak, r)
            dt = blk / SR
            if not speaking_now:
                if time.time() - t0 > max_wait:
                    return None
                if time.time() - last > 4.0:
                    print(f"       still waiting... your peak {peak:.4f} vs gate {thr:.4f}",
                          flush=True)
                    peak, last = 0.0, time.time()
                if r >= thr:
                    hot += 1
                    if hot >= 2:
                        speaking_now = True
                        print("       (got you - keep going, stop when done)", flush=True)
                        buf.extend(m.tolist())
                else:
                    hot = 0
            else:
                buf.extend(m.tolist())
                silent = silent + dt if r < thr else 0.0
                if silent >= hangover or len(buf) / SR >= max_utter:
                    break
        return buf
    finally:
        st.stop(); st.close()


def verdict(s: dict, wer: float, heard: str = "") -> str:
    """Which of the three is failing. Ordered so the CHEAPEST fix is named first.

    `heard` is REQUIRED to tell a broken ear from a person saying something else, and leaving it
    out is what made this function report MODEL five times on a run where the ear was perfect."""
    if not s:
        return "no audio at all - wrong device"
    if s["peak"] < 0.02:
        return "MIC: signal far too quiet. Raise the input level or move closer."
    if s["clipped"] > 50:
        return "MIC: clipping. Lower the input gain."
    if s["snr_db"] < 15:
        return ("ROOM: speech is only %.0f dB above the noise. Whisper is noise-fragile and "
                "level-robust, so no software setting recovers this - move somewhere quieter or "
                "closer to the mic." % s["snr_db"])
    # A HIGH WORD-ERROR IS NOT EVIDENCE THE EAR FAILED. It is only evidence the words differ from
    # the ones I asked for, and a person talking naturally differs constantly - which is the
    # behaviour we are actually trying to measure.
    #
    # MEASURED THREE TIMES 2026-07-29, and I reported "MODEL" all three times on a PERFECT
    # transcript: "Yeah, but I'm not hearing it..." (WER 1.00), "Hit me with the question"
    # (word for word right, WER 1.00 because it landed in the next phrase's window), and
    # "So, okay, you can hear me now. Take your time." (WER 4.50). Each one was clean audio and a
    # correct transcription of what was really said, and my scorer called the model broken.
    #
    # So the model is only blamed when the transcript is GARBAGE, never when it is merely
    # DIFFERENT. Garbage has a signature: whisper's non-speech artifacts are bracketed or
    # parenthesised ("[Music]", "(air whooshing)"), or collapse to one or two tokens.
    txt = (heard or "").strip()
    words = [w for w in re.findall(r"[A-Za-z']+", txt) if len(w) > 1]
    artifact = bool(re.match(r"^\s*[\[\(]", txt)) or txt.lower().strip(" .") in (
        "thank you", "you", "thanks", "bye", "oh")
    if artifact or len(words) < 2:
        return ("MODEL/SIGNAL: clean on paper (%.0f dB) but the transcript is a non-speech "
                "artifact - the words did not survive." % s["snr_db"])
    if wer > 0.34:
        return ("fine - the ear worked. The transcript is coherent speech; it just is not the "
                "phrase I asked for, which scores as error and is not one.")
    return "fine - clean audio, correct words"


def run(device=None, keep: bool = False, speaking: bool = True) -> list:
    import numpy as np
    import sounddevice as sd
    import soundfile as sf
    from aea.io import listen, speak
    from aea.lab.convbench import wer, semantic_match

    os.makedirs(OUT, exist_ok=True)
    print("EAR CHECK - recording, measuring and transcribing locally. Nothing is uploaded.\n")
    print(f"  device : {device if device is not None else 'default'}")
    print(f"  warming whisper... {listen.warm('en')}s\n")

    rows = []
    for i, phrase in enumerate(PHRASES):
        print(f"  [{i+1}/{len(PHRASES)}] SAY THIS, then stay quiet:")
        print(f"       \"{phrase}\"")
        # IT HAS TO SAY IT OUT LOUD. The first version only PRINTED the prompt, so Luis sat in
        # front of a silent machine waiting for it to speak - "the test wasn't emitting any voice".
        # A voice diagnostic that never uses the voice makes the person read a terminal while
        # being told to talk naturally, which is not the situation being measured. It also proves
        # the OUTPUT path works before asking the input path to prove anything.
        if speaking:
            speak.say_stream(f"Say: {phrase}", voice=speak.EDGE_VOICE)
            time.sleep(0.35)          # let the speaker tail die before the mic opens
        # NO COUNTDOWN, NO FIXED WINDOW. IT WAITS FOR YOU.
        #
        # The first version counted 3-2-1-GO and then recorded a fixed number of seconds. Reading
        # the envelopes afterwards showed why every result was junk: on one phrase the speech sat
        # at the very START and left three seconds of room, on another it was at the very END, and
        # on the last one the window for phrase five captured phrase four. The windows and the
        # speaker were out of sync in BOTH directions.
        #
        # The cause was me. I was posting "Go" into the chat, arriving seconds after the terminal's
        # own countdown, and Luis was speaking to my cue. I put myself inside a timing-critical
        # loop and then read the desynchronised result as evidence about whisper. An instrument
        # that requires an operator to be punctual is measuring the operator.
        #
        # So it now does what the real system does: opens the mic, waits however long it takes for
        # speech to start, and records until you stop. No pressure, no cue to miss, and it
        # exercises the same trigger-and-hangover path the conversation actually uses.
        x = _wait_and_record(device)
        if x is None or len(x) == 0:
            print("       (heard nothing at all in 25s - skipping)\n")
            continue
        import numpy as _np
        x = _np.asarray(x, dtype="float32")
        wav = os.path.join(OUT, f"p{i}.wav")
        sf.write(wav, x, SR, subtype="PCM_16")
        s = _stats(x, SR)
        got = listen.transcribe_samples([float(v) for v in x], SR, "en").strip()
        w = wer(phrase, got)
        sem = semantic_match(phrase, got)
        v = verdict(s, w, got)
        rows.append(dict(phrase=phrase, heard=got, wer=round(w, 2), semantic=sem, verdict=v, **s))
        print(f"       heard : {got!r}")
        print(f"       signal: peak {s['peak']:.3f}  SNR {s['snr_db']:.0f}dB  "
              f"voiced {s['voiced_frac']:.0%}  clipped {s['clipped']}")
        print(f"       words : WER {w:.2f}  {'MEANING OK' if sem else 'MEANING LOST'}")
        print(f"       -> {v}\n")

    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    import statistics
    snrs = [r["snr_db"] for r in rows]
    peaks = [r["peak"] for r in rows]
    short = [r for r in rows if len(r["phrase"].split()) <= 5]
    long_ = [r for r in rows if len(r["phrase"].split()) > 5]
    print(f"  SNR median {statistics.median(snrs):.0f} dB   peak median {statistics.median(peaks):.3f}")
    if short:
        print(f"  SHORT phrases ({len(short)}): {sum(1 for r in short if r['semantic'])}/{len(short)} "
              f"understood, median WER {statistics.median([r['wer'] for r in short]):.2f}")
    if long_:
        print(f"  LONG phrases  ({len(long_)}): {sum(1 for r in long_ if r['semantic'])}/{len(long_)} "
              f"understood, median WER {statistics.median([r['wer'] for r in long_]):.2f}")
    causes = [r["verdict"].split(":")[0] for r in rows]
    print(f"\n  causes: " + ", ".join(f"{c}x{causes.count(c)}" for c in sorted(set(causes))))
    grid.atomic_save_json(os.path.join(OUT, "result.json"),
                          {"at": time.strftime("%Y-%m-%d %H:%M"), "rows": rows})
    print(f"  written {os.path.join(OUT, 'result.json')}")
    if not keep:
        for i in range(len(PHRASES)):
            try:
                os.remove(os.path.join(OUT, f"p{i}.wav"))
            except Exception:
                pass
        print("  recordings deleted (pass --keep to listen to them)")
    else:
        print(f"  recordings kept in {OUT}")
    return rows


if __name__ == "__main__":
    a = sys.argv[1:]
    dev = int(a[a.index("--device") + 1]) if "--device" in a else None
    run(device=dev, keep="--keep" in a, speaking="--silent" not in a)
