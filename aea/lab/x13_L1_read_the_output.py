"""x13 - CHAPTER II / LEVEL 1. What can be learned from a reply without spending another call?

L0 closed with a wall it produced itself: **52% of failed trials already contained the correct answer**,
sitting in the rod's own text, unreachable because L0 has one prompt and one reply and no instrument that
can look past the reply into the work. L1 is the room where that instrument exists. Everything here is
LOCAL, EXACT and FREE, and nothing here sends a second call. A second call is L3.

L1 holds four census items and two have never been tested:

  C-15  #4 coherence, the per-tick score      M, missing. THE MEASURE: is this reply right?
  C-60  PR-2 restorable coherence             E, embodied
  C-74  v0.16 LatencyTracker                  C, compressed. NEVER TESTED
  C-75  v0.17 parser validation               C, compressed. NEVER TESTED

STRICTLY L1. The goal may be stated, because L0 proved a call without one cannot succeed. Nothing may
name a METHOD, because that is THE FRAME at L2. So whatever working the rod shows, it volunteered, and
this chapter reads only what it was already given.

FOUR MEASUREMENTS, and they are chosen so all three kinds of creature can appear rather than only the
flattering one.

  1  THE READOUT'S YIELD.  Cases where the work is right and the stated answer is wrong. L0 measured 52%
     of failures this way; here it is measured as a recovery rate at zero tokens.

  2  THE INVERSE, AND NOBODY HAS LOOKED FOR IT.  Cases where the stated answer is RIGHT and the working
     is WRONG. A rod that enumerates to twelve and then says thirteen is correct by accident. The scorer
     records a pass and the construct above it inherits a coin flip. This is measurable with exactly the
     same data and it has never been counted.

  3  PARSER VALIDATION, C-75, and it is a TOXIC instrument when it guesses. Our own loose parser read
     "b5 moved 2 shelves ahead from shelf 4 to shelf 6" and returned 2, converting correct working into a
     confident wrong answer. So strict and loose parses run side by side, and the count that matters is
     how often LOOSE MANUFACTURES A WRONG ANSWER WHERE STRICT WOULD HAVE ABSTAINED. A readout that
     guesses is worse than no readout, and that is a hazard rather than a bug.

  4  LATENCY AS A FREE PREDICTOR, C-74.  Every call already carries a latency and a first-byte time.
     Nobody has asked whether they predict correctness. If a rod's slow replies are reliably its wrong
     ones, then a construct can route on a number it already has, at zero tokens. If they do not predict,
     C-74 is bookkeeping and the chapter says so.

Run: python -m aea.lab.x13_L1_read_the_output
"""
from __future__ import annotations

import concurrent.futures as _futures
import re
import statistics
import time

from aea.lab import harness as H
from aea.lab import overseer as OV
from aea.mind import fuel

N = 8
MAXTOK = 1200
TEMPS = (0.2, 0.7)

# ENUMERABLE TASKS ONLY. The readout reads WORK, so the work has to have a countable shape. Three tasks
# rather than one, because every finding in this lab so far rests on wordcount and that is a named gap.
TASKS = {
    "wordcount": {
        "prompt": ("Count the words in the sentence below and reply with the number.\n"
                   "the mouth draws power through the ladder and the measure closes the wire"),
        "truth": 13},
    "listcount": {
        "prompt": ("How many items are in this list? Reply with the number.\n"
                   "iron, copper, tin, zinc, lead, nickel, silver, gold, cobalt, chromium, tungsten"),
        "truth": 11},
    "vowelcount": {
        "prompt": ("How many vowels are in the word below? Reply with the number.\n"
                   "unconventionality"),
        "truth": 8},
}

RODS = [
    ("ollama", "qwen3:0.6b",              "nano"),
    ("ollama", "granite4.1:3b",           "micro"),
    ("ollama", "granite4.1:8b",           "normal"),
    ("groq",   "llama-3.1-8b-instant",    "normal"),
    ("groq",   "llama-3.3-70b-versatile", "large"),
    ("cerebras", "gpt-oss-120b",          "large"),
]

_ENUM = re.compile(r"(?m)^\s*(\d{1,3})[.)]\s+\S")          # "1. the" / "2) copper"
_INLINE = re.compile(r"\b(\d{1,3})\s*[.)]\s*[A-Za-z]")      # inline "1. the 2. mouth"


def stated(text: str):
    """STRICT. The last standalone number, which is where an answer lives when one is given."""
    nums = re.findall(r"(?<![\d.])(-?\d{1,4})(?![\d.])", (text or "").replace(",", ""))
    return int(nums[-1]) if nums else None


def from_work(text: str):
    """THE READOUT. The highest enumeration index the rod itself wrote. Zero tokens, zero milliseconds."""
    idx = [int(m.group(1)) for m in _ENUM.finditer(text or "")]
    if not idx:
        idx = [int(m.group(1)) for m in _INLINE.finditer(text or "")]
    return max(idx) if idx else None


def loose(text: str):
    """A DELIBERATELY PERMISSIVE parse, kept so its damage can be counted rather than assumed.

    This is the shape our own parser had when it converted correct working into a wrong answer: take any
    number near the end and commit to it. It is included as an instrument under test, never as a fallback.
    """
    nums = re.findall(r"-?\d{1,4}", (text or "").replace(",", ""))
    return int(nums[-1]) if nums else None


def _trial(rod, task_id, temp, i):
    t = TASKS[task_id]
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": t["prompt"]}],
                     max_tokens=MAXTOK, temperature=temp)
    seen = OV.inspect(r, max_tokens=MAXTOK, prompt=t["prompt"])
    text = seen["text"]
    s, w, l = stated(text), from_work(text), loose(text)
    truth = t["truth"]
    return {"trial": i, "ok": bool(r.get("ok")), "flags": seen["flags"],
            "stated": s, "work": w, "loose": l, "truth": truth,
            "stated_ok": s == truth, "work_ok": w == truth,
            "showed_work": w is not None,
            # the four cells of the confusion table this chapter exists to fill
            "both_right": s == truth and w == truth,
            "mute": w == truth and s != truth,              # work right, mouth wrong: THE READOUT pays
            "lucky": s == truth and w is not None and w != truth,   # mouth right, work wrong
            "both_wrong": s != truth and (w is None or w != truth),
            # C-75: does the permissive parse manufacture a wrong answer where strict abstains?
            "loose_manufactures": (s is None and l is not None and l != truth),
            "loose_corrupts": (s == truth and l is not None and l != truth),
            "latency": r.get("latency"), "first_byte": r.get("first_byte_s"),
            "tok_out": r.get("tokens") or 0, "raw": text[-320:]}


def cell(led, rod, task_id, temp):
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        tr = [f.result() for f in [pool.submit(_trial, rod, task_id, temp, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [t for t in tr if t["ok"] and not t["flags"]]
    for t in tr:
        led.note_flags(t["flags"])
    row = {"rod": "%s/%s" % rod[:2], "size": rod[2], "task": task_id, "temperature": temp,
           "clean": len(ok), "ran": len(tr),
           "stated_ok": sum(1 for t in ok if t["stated_ok"]),
           "readout_ok": sum(1 for t in ok if t["stated_ok"] or t["work_ok"]),
           "showed_work": sum(1 for t in ok if t["showed_work"]),
           "mute": sum(1 for t in ok if t["mute"]),
           "lucky": sum(1 for t in ok if t["lucky"]),
           "loose_manufactures": sum(1 for t in ok if t["loose_manufactures"]),
           "loose_corrupts": sum(1 for t in ok if t["loose_corrupts"]),
           "lat_right": [t["latency"] for t in ok if t["stated_ok"] and t["latency"]],
           "lat_wrong": [t["latency"] for t in ok if not t["stated_ok"] and t["latency"]],
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=temp,
                              attempts=len(tr), failures=len(tr) - len(ok)),
           "trials": tr}
    led.add(row)
    print("    %-24s %-11s t=%.1f  stated %d/%-2d  +readout %d/%-2d  work %d  mute %d  lucky %d  loose-bad %d"
          % (row["rod"].split("/")[-1][:23], task_id, temp, row["stated_ok"], row["clean"],
             row["readout_ok"], row["clean"], row["showed_work"], row["mute"], row["lucky"],
             row["loose_manufactures"] + row["loose_corrupts"]), flush=True)
    return row


def run():
    led = OV.Ledger("x13_L1_read_the_output", {
        "level": "L1", "chapter": "II", "closes": ["C-74", "C-75"], "receipts": ["C-15", "C-60"],
        "question": "what can be learned from a reply without spending another call?",
        "n": N, "temperatures": list(TEMPS), "tasks": list(TASKS), "max_tokens": MAXTOK})
    print("x13 - LEVEL 1, chapter II. %d rods x %d tasks x %d temps x n=%d"
          % (len(RODS), len(TASKS), len(TEMPS), N), flush=True)
    for rod in RODS:
        print("\n  %s (%s)" % (rod[1], rod[2]), flush=True)
        for temp in TEMPS:
            for task_id in TASKS:
                if led.has(rod="%s/%s" % rod[:2], task=task_id, temperature=temp):
                    continue
                cell(led, rod, task_id, temp)

    rows = led.doc["rows"]
    tot = lambda k: sum(r[k] for r in rows)
    clean = tot("clean") or 1
    stated_rate, readout_rate = tot("stated_ok") / clean, tot("readout_ok") / clean

    # C-74. Latency as a free predictor: does a wrong reply take longer than a right one?
    right = [x for r in rows for x in r["lat_right"]]
    wrong = [x for r in rows for x in r["lat_wrong"]]
    lat = None
    if len(right) >= 8 and len(wrong) >= 8:
        mr, mw = statistics.median(right), statistics.median(wrong)
        lat = {"median_right_s": round(mr, 2), "median_wrong_s": round(mw, 2),
               "ratio": round(mw / mr, 2) if mr else None, "n_right": len(right), "n_wrong": len(wrong)}

    v = []
    v.append("THE READOUT RECOVERS %d of %d clean trials at ZERO tokens: stated %.0f%% to %.0f%%. "
             "%d trials were MUTE (work right, mouth wrong)."
             % (tot("readout_ok") - tot("stated_ok"), clean, 100 * stated_rate, 100 * readout_rate,
                tot("mute")))
    if tot("lucky"):
        v.append("THE LUCKY ONES: %d trials stated the RIGHT answer over WRONG working. A scorer records "
                 "these as passes and the construct above inherits a coin flip. Nobody had counted them."
                 % tot("lucky"))
    else:
        v.append("NO LUCKY TRIALS: every correct statement rested on correct working, so a pass at L1 can "
                 "be trusted on these tasks.")
    bad = tot("loose_manufactures") + tot("loose_corrupts")
    if bad:
        v.append("C-75 IS LOAD-BEARING AND THE PERMISSIVE PARSE IS TOXIC: it produced a confident WRONG "
                 "answer %d times (%d where strict abstained, %d where it overwrote a correct one). A "
                 "readout that guesses is worse than no readout."
                 % (bad, tot("loose_manufactures"), tot("loose_corrupts")))
    else:
        v.append("C-75: the permissive parse never manufactured a wrong answer on these tasks. Validation "
                 "is still cheap insurance, but this run does not price it.")
    if lat:
        if lat["ratio"] and (lat["ratio"] >= 1.5 or lat["ratio"] <= 0.67):
            v.append("C-74 IS A REAL SIGNAL: wrong replies take %.2fx the median latency of right ones "
                     "(%.2fs against %.2fs). A construct can route on a number it already holds, for free."
                     % (lat["ratio"], lat["median_wrong_s"], lat["median_right_s"]))
        else:
            v.append("C-74 IS BOOKKEEPING, NOT A SIGNAL: wrong replies take %.2fx the latency of right "
                     "ones, which is inside noise. Latency is worth recording and does not predict "
                     "correctness here." % lat["ratio"])
    else:
        v.append("C-74 UNDECIDED: too few clean trials on one side to compare latencies.")

    led.done(stated_rate=round(stated_rate, 3), readout_rate=round(readout_rate, 3),
             mute=tot("mute"), lucky=tot("lucky"), showed_work=tot("showed_work"),
             loose_manufactures=tot("loose_manufactures"), loose_corrupts=tot("loose_corrupts"),
             latency=lat, verdict=v)
    return led.doc


if __name__ == "__main__":
    d = run()
    print()
    print("stated %.3f  ->  with readout %.3f   (work shown in %d trials, mute %d, lucky %d)"
          % (d["stated_rate"], d["readout_rate"], d["showed_work"], d["mute"], d["lucky"]))
    print("loose parse: manufactured %d, corrupted %d" % (d["loose_manufactures"], d["loose_corrupts"]))
    print("latency:", d["latency"])
    print("overseer:", d["overseer"])
    print()
    for line in d["verdict"]:
        print(" -", line)
    print("\nEVIDENCE  state/lab/runs/x13_L1_read_the_output/%s.json" % d["run_id"])
