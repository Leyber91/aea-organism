"""blackbox.py - KEEP BOTH SIDES OF EVERY TURN: the audio, and what the machine made of it.

Luis, 2026-07-29: "you will record both my sound and what actually is transcribed, so you can
measure how inefficient is the model versus what you do. It's like in Interstellar when they were
going into the black hole of Gargantua - because outside of the black hole you couldn't get the
data. Only once you are inside."

He is right, and the whole session proves it. Every conclusion about the ear tonight was drawn from
ONE side of the boundary - the transcript - and every one of them was wrong:

  "Creysau", "Where you lost", "and not meet with the question"  ->  read as a weak MODEL
  the actual cause                                               ->  input level swinging 25x
  the fix I was one command from buying                          ->  a 636MB model, twice

The transcript alone cannot distinguish a bad model from a starved microphone from a person saying
something different. Those three need three different fixes and look identical from outside. The
only way to tell is to keep the AUDIO beside the TEXT and measure them together.

WHAT IT KEEPS, per turn:
  the raw samples (wav, 16k mono)
  the transcript
  the signal stats that decide the cause - peak, SNR, voiced fraction, clipping
  the prosody measurements
  the endpoint decision, and whether it was early or waited
  what the machine SAID back, and what it cost

WHAT IT IS NOT. Not a recording of a conversation for its own sake. It is an INSTRUMENT, off by
default, and everything it writes lives under state/blackbox/ which is gitignored. Luis's own voice
is the most personal thing this repo has ever touched.

  python -m aea.io.blackbox --report      read the last session back
  python -m aea.io.blackbox --purge       delete every stored turn
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DIR = os.path.join(str(grid.STATE), "blackbox")
INDEX = os.path.join(DIR, "index.jsonl")


def enabled() -> bool:
    """Off unless explicitly switched on. Recording a person by default is not a default."""
    return bool(grid.load_json(os.path.join(str(grid.STATE), "blackbox.json"),
                               {"enabled": False}).get("enabled"))


def signal_stats(samples, sr: int) -> dict:
    """The signal numbers that decide MIC vs ROOM vs MODEL. Shared with earcheck deliberately -
    two different measures of 'was the audio good' would eventually disagree."""
    try:
        from aea.io.earcheck import _stats
        return _stats(samples, sr)
    except Exception:
        return {}


def keep(samples, sr: int, heard: str, stats: dict, prosody_m: dict, endpoint: dict,
         reply: str = "", receipt: dict = None) -> str:
    """Store one turn, both sides. Returns the wav path, or "" if disabled or it failed.

    Never raises: a failure to record must not cost the person a turn. That is the same rule as
    the prosody read, and it is why this returns a string instead of throwing."""
    if not enabled():
        return ""
    try:
        import numpy as np
        import soundfile as sf
        os.makedirs(DIR, exist_ok=True)
        stamp = time.strftime("%Y%m%dT%H%M%S")
        wav = os.path.join(DIR, f"{stamp}.wav")
        sf.write(wav, np.asarray(samples, dtype="float32"), sr, subtype="PCM_16")
        row = dict(at=time.strftime("%Y-%m-%d %H:%M:%S"), wav=os.path.basename(wav),
                   heard=heard, seconds=round(len(samples) / sr, 2),
                   signal=stats or {}, prosody=prosody_m or {}, endpoint=endpoint or {},
                   reply=reply, receipt={k: v for k, v in (receipt or {}).items()
                                         if k in ("model", "ttfb", "tier", "noticed",
                                                  "acted", "budget")})
        with open(INDEX, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        return wav
    except Exception:
        return ""


def rows() -> list:
    if not os.path.exists(INDEX):
        return []
    out = []
    for line in open(INDEX, encoding="utf-8"):
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def report() -> str:
    """What the stored turns say about the ear, from BOTH sides of the boundary."""
    rs = rows()
    if not rs:
        return "no turns recorded (enable with state/blackbox.json {\"enabled\": true})"
    L = [f"BLACK BOX - {len(rs)} turns recorded", "=" * 92,
         f"  {'when':>8} {'sec':>5} {'peak':>7} {'SNR':>6} {'vox':>5}  transcript"]
    import statistics
    good, thin, artifact = [], [], []
    for r in rs:
        s = r.get("signal") or {}
        h = (r.get("heard") or "").strip()
        pk, snr, vox = s.get("peak", 0), s.get("snr_db", 0), s.get("voiced_frac", 0)
        words = len([w for w in h.split() if len(w) > 1])
        art = h.startswith(("[", "(")) or h.lower().strip(" .") in ("thank you", "you", "")
        (artifact if art else (thin if words < 3 else good)).append(r)
        L.append(f"  {r['at'][-8:]:>8} {r.get('seconds',0):5.1f} {pk:7.3f} {snr:6.1f} "
                 f"{vox:5.2f}  {h[:52]!r}{'  <- ARTIFACT' if art else ''}")
    L.append("")
    L.append("THE THING THE TRANSCRIPT ALONE CANNOT TELL YOU:")
    for name, group in (("clean transcripts", good), ("very short", thin),
                        ("non-speech artifacts", artifact)):
        if not group:
            continue
        pk = [(g.get('signal') or {}).get('peak', 0) for g in group]
        sn = [(g.get('signal') or {}).get('snr_db', 0) for g in group]
        L.append(f"  {name:22s} n={len(group):3d}  median peak {statistics.median(pk):.3f}  "
                 f"median SNR {statistics.median(sn):.1f} dB")
    if good and artifact:
        gp = statistics.median([(g.get('signal') or {}).get('peak', 0) for g in good])
        ap = statistics.median([(g.get('signal') or {}).get('peak', 0) for g in artifact])
        L.append("")
        L.append(f"  artifacts arrive at {ap:.3f} peak and clean transcripts at {gp:.3f} "
                 f"({gp/max(ap,1e-6):.1f}x).")
        L.append("  If that ratio is large the ear is STARVED, not weak - and a bigger model buys")
        L.append("  nothing. If it is near 1.0, the model genuinely is the limit.")
    return "\n".join(L)


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--purge" in a:
        import shutil
        if os.path.isdir(DIR):
            shutil.rmtree(DIR)
        print("black box purged - every recording deleted")
    elif "--on" in a:
        grid.atomic_save_json(os.path.join(str(grid.STATE), "blackbox.json"), {"enabled": True})
        print("black box ON. Every turn stores audio + transcript under state/blackbox/ (gitignored).")
    elif "--off" in a:
        grid.atomic_save_json(os.path.join(str(grid.STATE), "blackbox.json"), {"enabled": False})
        print("black box OFF")
    else:
        print(report())
