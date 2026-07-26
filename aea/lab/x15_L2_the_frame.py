"""x15 - CHAPTER III / LEVEL 2. The last free lever, and the creature it damages.

L1 ended holding a free instrument with nothing to read: `Lector operis` recovers an answer from a rod's
own working at zero tokens and recovered THREE trials of a hundred and fifty-three, because only 29 of 153
replies contained any working at all. L2 is the room where you may finally shape what you send, and after
this room every gain costs a call.

THE PREDICTIONS ARE SEALED. `design/book/04_CHAPTER_III_OPENING_LOCKED.md`, sha256 f1ed053c, locked before
this file existed. This experiment is built to lose them:

  1  replies containing working rise from ~19% to ABOVE 60%          basis: x10 saw 8 bare against 240 framed
  2  the readout's yield rises from +3 of 153 to ABOVE 10%           basis: it is inert only for lack of material
  3  at least one rod is HARMED by more than 10 points when framed   basis: the 550b lost 57
  5  a frame cannot rescue a goal-less call                          basis: 0 of 304 at L0

Prediction 4 concerns `working_objective.append` and belongs to a separate run; the three tools C-53, C-54
and C-55 are a sub-system of their own.

THE LADDER, C-09, WHICH HAS NEVER BEEN TESTED. The census carries a "Prompting ladder" as a missing item.
Here it is three rungs and the difference between the last two is the whole point:

  BARE      the goal, nothing else
  POSTURE   the goal plus a manner, quoted verbatim from bench_core.SCAFFOLDS. Names no method
  FITTED    the goal plus the METHOD, step by step, so that working becomes visible

x01 found a posture frame costs +38 to +107% input tokens and changes nothing, and x10 found it pays on
1 rod of 11. If that reproduces here, the only frame the bench can currently seat is the worthless kind,
and the L2 mission cannot be built on it.

THE TOXIC CELL. `fitted` with the GOAL WITHHELD: a method with no objective, how stated and what missing.
It runs on one task, and it is the cell that decides whether Chapter I needs a second correction.

Run: python -m aea.lab.x15_L2_the_frame
"""
from __future__ import annotations

import concurrent.futures as _futures
import re
import time

from aea.lab import harness as H
from aea.lab import overseer as OV
from aea.mind import fuel

N = 8
MAXTOK = 1200
TEMPS = (0.2, 0.7)

WORDS = "the mouth draws power through the ladder and the measure closes the wire"
WORD = "unconventionality"

TASKS = {
    "wordcount": {
        "data": WORDS, "truth": 13,
        "goal": "Count the words in the sentence below and reply with the number.",
        "method": ("To count words: split the sentence on spaces, number each token 1, 2, 3 and so on, "
                   "then report the FINAL index. Show the numbered list, then the count alone on the "
                   "last line.")},
    "vowelcount": {
        "data": WORD, "truth": 7,
        "goal": "How many of the letters a, e, i, o, u are in the word below? Reply with the number.",
        "method": ("To count these letters: go through the word one letter at a time, number each "
                   "occurrence of a, e, i, o or u as you find it 1, 2, 3 and so on, then report the "
                   "FINAL index. Show the numbered list, then the count alone on the last line.")},
}

# Quoted verbatim from aea/bench/bench_core.py SCAFFOLDS["bench"], so this measures the frame the bench
# can actually seat rather than a paraphrase of it.
POSTURE = "You are on the bench. Answer exactly and only what is asked.\n"

FRAMES = ("bare", "posture", "fitted")

RODS = [
    ("nvidia", "meta/llama-3.2-3b-instruct",          "micro"),
    ("ollama", "granite4.1:3b",                       "micro"),
    ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2",   "normal"),
    ("ollama", "granite4.1:8b",                       "normal"),
    ("groq",   "llama-3.1-8b-instant",                "normal"),
    ("nvidia", "openai/gpt-oss-20b",                  "normal"),
    ("groq",   "llama-3.3-70b-versatile",             "large"),
    # THE ROD PREDICTION 3 IS ABOUT. It scored bare 1.00 and framed 0.25 in x10, and it is the whole
    # reason `Auratus gravis` is in the bestiary. It went silent for hours and came back for this run.
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b",   "large"),
    ("cerebras", "gpt-oss-120b",                      "large"),   # last: rpm 5, the slowest plant we have
]

_ENUM = re.compile(r"(?m)^\s*(\d{1,3})[.)]\s+\S")
_INLINE = re.compile(r"\b(\d{1,3})\s*[.)]\s*[A-Za-z]")


def stated(text: str):
    nums = re.findall(r"(?<![\d.])(-?\d{1,4})(?![\d.])", (text or "").replace(",", ""))
    return int(nums[-1]) if nums else None


def from_work(text: str):
    idx = [int(m.group(1)) for m in _ENUM.finditer(text or "")]
    if not idx:
        idx = [int(m.group(1)) for m in _INLINE.finditer(text or "")]
    return max(idx) if idx else None


# A PROCEDURE THAT NAMES NO OBJECTIVE. Caught before the run and it matters: "To count words: split on
# spaces..." STATES the goal. A method for counting words tells the rod a word count is wanted, so for a
# specific task the method and the goal are not separable, and a cell built that way measures whether a
# method CARRIES its goal rather than whether a frame can work without one. This names a procedure over
# "units", never says what a unit is, and never says why the number is wanted.
GENERIC = ("Go through the input below one unit at a time. Number each unit 1, 2, 3 and so on as you go, "
           "then report the FINAL index. Show the numbered list, then the number alone on the last line.")


def build(task_id: str, frame: str, with_goal: bool = True) -> str:
    t = TASKS[task_id]
    if frame == "generic_nogoal":           # TRULY goal-less: a procedure with no objective at all
        return GENERIC + "\n\n" + t["data"]
    if not with_goal:                       # the task's own method, goal sentence removed (it leaks)
        return t["method"] + "\n" + t["data"]
    if frame == "bare":
        return t["goal"] + "\n" + t["data"]
    if frame == "posture":
        return POSTURE + t["goal"] + "\n" + t["data"]
    return t["method"] + "\n\n" + t["goal"] + "\n" + t["data"]


def _trial(rod, task_id, frame, with_goal, temp, i):
    p = build(task_id, frame, with_goal)
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": p}],
                     max_tokens=MAXTOK, temperature=temp)
    seen = OV.inspect(r, max_tokens=MAXTOK, prompt=p)
    text = seen["text"]
    s, w, truth = stated(text), from_work(text), TASKS[task_id]["truth"]
    return {"trial": i, "ok": bool(r.get("ok")), "flags": seen["flags"],
            "stated": s, "work": w, "truth": truth,
            "stated_ok": s == truth, "work_ok": w == truth, "showed_work": w is not None,
            "readout_ok": (s == truth) or (w == truth),
            "mute": w == truth and s != truth,
            "tok_in": r.get("prompt_tokens"), "tok_out": r.get("tokens"),
            "latency": r.get("latency"), "raw": text[-320:]}


def cell(led, rod, task_id, frame, with_goal, temp):
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        tr = [f.result() for f in
              [pool.submit(_trial, rod, task_id, frame, with_goal, temp, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [t for t in tr if t["ok"] and not t["flags"]]
    for t in tr:
        led.note_flags(t["flags"])
    row = {"rod": "%s/%s" % rod[:2], "size": rod[2], "task": task_id, "frame": frame,
           "goal": bool(with_goal), "temperature": temp, "clean": len(ok), "ran": len(tr),
           "stated_ok": sum(1 for t in ok if t["stated_ok"]),
           "readout_ok": sum(1 for t in ok if t["readout_ok"]),
           "showed_work": sum(1 for t in ok if t["showed_work"]),
           "mute": sum(1 for t in ok if t["mute"]),
           "tok_in": sum(t["tok_in"] or 0 for t in ok),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=temp,
                              attempts=len(tr), failures=len(tr) - len(ok)),
           "trials": tr}
    led.add(row)
    print("    %-24s %-11s %-8s goal=%-5s t=%.1f  stated %d/%-2d  +ro %d/%-2d  work %d/%-2d"
          % (row["rod"].split("/")[-1][:23], task_id, frame, with_goal, temp,
             row["stated_ok"], row["clean"], row["readout_ok"], row["clean"],
             row["showed_work"], row["clean"]), flush=True)
    return row


def run():
    led = OV.Ledger("x15_L2_the_frame", {
        "level": "L2", "chapter": "III", "closes": ["C-09"], "receipts": ["C-04", "C-19", "C-23"],
        "sealed_opening": "design/book/04_CHAPTER_III_OPENING_LOCKED.md sha256 f1ed053c",
        "predictions": {"1_working_above": 0.60, "2_readout_yield_above": 0.10,
                        "3_a_rod_harmed_by": 0.10, "5_frame_rescues_goalless": False},
        "n": N, "temperatures": list(TEMPS), "tasks": list(TASKS), "frames": list(FRAMES)})
    print("x15 - LEVEL 2, chapter III. %d rods x %d tasks x %d frames x %d temps, plus the goal-less cell"
          % (len(RODS), len(TASKS), len(FRAMES), len(TEMPS)), flush=True)
    for rod in RODS:
        print("\n  %s (%s)" % (rod[1], rod[2]), flush=True)
        for temp in TEMPS:
            for task_id in TASKS:
                for frame in FRAMES:
                    if led.has(rod="%s/%s" % rod[:2], task=task_id, frame=frame,
                               goal=True, temperature=temp):
                        continue
                    cell(led, rod, task_id, frame, True, temp)
        # THE TWO GOAL-LESS CELLS, at the product temperature only. They are different questions:
        #   fitted_nogoal   the task's own method with the goal sentence removed. The method leaks the
        #                   objective, so this measures whether a method CARRIES its goal
        #   generic_nogoal  a procedure over "units" that names no objective at all. This is the one
        #                   prediction 5 is actually about
        for fr in ("fitted", "generic_nogoal"):
            if not led.has(rod="%s/%s" % rod[:2], task="wordcount", frame=fr,
                           goal=False, temperature=TEMPS[0]):
                cell(led, rod, "wordcount", fr, False, TEMPS[0])

    rows = [r for r in led.doc["rows"] if r["goal"]]
    nogoal = [r for r in led.doc["rows"] if not r["goal"]]

    def agg(frame, key):
        sel = [r for r in rows if r["frame"] == frame]
        tot = sum(r["clean"] for r in sel)
        return (sum(r[key] for r in sel) / tot) if tot else None

    work = {f: agg(f, "showed_work") for f in FRAMES}
    stated_r = {f: agg(f, "stated_ok") for f in FRAMES}
    readout_r = {f: agg(f, "readout_ok") for f in FRAMES}

    # PREDICTION 3: per rod, bare against fitted, both with the goal present
    harm = {}
    for rod in {r["rod"] for r in rows}:
        def rate(f):
            sel = [r for r in rows if r["rod"] == rod and r["frame"] == f]
            tot = sum(r["clean"] for r in sel)
            return (sum(r["stated_ok"] for r in sel) / tot) if tot else None
        b, fi = rate("bare"), rate("fitted")
        if None not in (b, fi):
            harm[rod] = round(fi - b, 3)

    gen = [r for r in nogoal if r["frame"] == "generic_nogoal"]
    lea = [r for r in nogoal if r["frame"] == "fitted"]
    ng_tot = sum(r["clean"] for r in gen)
    ng_ok = sum(r["stated_ok"] for r in gen)
    leak_tot = sum(r["clean"] for r in lea)
    leak_ok = sum(r["stated_ok"] for r in lea)

    v = []
    p1 = work["fitted"] is not None and work["fitted"] > 0.60
    v.append("PREDICTION 1 %s: working appears in %.0f%% bare, %.0f%% posture, %.0f%% FITTED (predicted "
             "above 60%%)." % ("HOLDS" if p1 else "FAILS",
                               100 * (work["bare"] or 0), 100 * (work["posture"] or 0),
                               100 * (work["fitted"] or 0)))
    gain = (readout_r["fitted"] or 0) - (stated_r["fitted"] or 0)
    p2 = gain > 0.10
    v.append("PREDICTION 2 %s: under a fitted frame the readout adds %.1f points (stated %.0f%% to %.0f%%), "
             "predicted above 10." % ("HOLDS" if p2 else "FAILS", 100 * gain,
                                      100 * (stated_r["fitted"] or 0), 100 * (readout_r["fitted"] or 0)))
    hurt = {k: v_ for k, v_ in harm.items() if v_ <= -0.10}
    v.append("PREDICTION 3 %s: %s" % ("HOLDS" if hurt else "FAILS",
             ("harmed by more than 10 points when framed: " + ", ".join(
                 "%s %+.2f" % (k.rsplit('/', 1)[-1], x) for k, x in sorted(hurt.items(), key=lambda kv: kv[1])))
             if hurt else "NO rod lost more than 10 points to a fitted frame. `Auratus gravis` demotes "
                         "from a law to an observation about one rod on one plant."))
    p5 = ng_ok == 0
    v.append("PREDICTION 5 %s: with the METHOD stated and the GOAL withheld, %d of %d clean trials "
             "succeeded. %s" % ("HOLDS" if p5 else "FAILS", ng_ok, ng_tot,
             "A frame cannot supply a goal." if p5 else
             "A frame PARTLY rescues a goal-less call, and Chapter I's hard floor needs a second correction."))
    v.append("THE POSTURE RUNG: stated %.0f%% bare against %.0f%% posture. %s"
             % (100 * (stated_r["bare"] or 0), 100 * (stated_r["posture"] or 0),
                "The frame the bench can seat today does nothing." if
                abs((stated_r["posture"] or 0) - (stated_r["bare"] or 0)) < 0.05 else
                "The posture frame moves the number."))

    v.append("AND THE CONFLATION FOUND BEFORE THE RUN: the task's own method STATES its objective, so a "
             "'method without a goal' cell measures whether a method carries its goal. It does, %d of %d. "
             "Prediction 5 is tested by the GENERIC cell above, which names a procedure over 'units' and "
             "no objective at all." % (leak_ok, leak_tot))

    led.done(method_carries_goal={"clean": leak_tot, "succeeded": leak_ok},
             working_by_frame={k: (round(x, 3) if x is not None else None) for k, x in work.items()},
             stated_by_frame={k: (round(x, 3) if x is not None else None) for k, x in stated_r.items()},
             readout_by_frame={k: (round(x, 3) if x is not None else None) for k, x in readout_r.items()},
             harm_by_rod=harm, goalless={"clean": ng_tot, "succeeded": ng_ok}, verdict=v)
    return led.doc


if __name__ == "__main__":
    d = run()
    print()
    print("working  by frame:", d["working_by_frame"])
    print("stated   by frame:", d["stated_by_frame"])
    print("readout  by frame:", d["readout_by_frame"])
    print("harm by rod (fitted - bare):")
    for k, x in sorted(d["harm_by_rod"].items(), key=lambda kv: kv[1]):
        print("   %-42s %+.3f" % (k.rsplit("/", 1)[-1][:41], x))
    print("goal-less + method:", d["goalless"])
    print("overseer:", d["overseer"])
    print()
    for line in d["verdict"]:
        print(" -", line)
    print("\nEVIDENCE  state/lab/runs/x15_L2_the_frame/%s.json" % d["run_id"])
