"""calibrate.py - THE FAILURE WINDOW. Measure which rods fail which task, BEFORE designing anything.

THE MISTAKE THIS EXISTS TO PREVENT. Three of chapter I's four laws did not survive re-measurement, and
all three failed the same way: the capability was tested on rods that did not need it. The judge matrix
read "the critic did not help" off models that had already answered correctly - where there is no wrong
answer to repair, the only thing being measured is the critic's price. Two more experiments (x03, x04)
lost most of their rods to the identical error even after the guards were added, because the guards can
only VOID the arm after the tokens are spent.

The fix is ordering, not vigilance. A capability's BENEFIT can only be measured inside the failure
window of the fuel, so the window has to be measured first and the experiment designed against the
table. Bare-only, no treatment, no claims - just: on this task, which rods fail?

THE THREE CLASSES, and each is a different kind of useless or useful:
  SATURATED  >= 7/8 passes  the rod already does it. A benefit experiment here measures COST ONLY.
  WINDOW      1..6/8        partial. The measurable zone: there is room to improve and proof it can.
  FLOOR       0/8           total failure. Good for a benefit test IF the rod can be helped at all -
                            llama-3.2-1b sits at FLOOR on everything and is helped by nothing, which
                            is a different fact from 3b sitting at FLOOR and going to 8/8 with a frame.

A valid benefit experiment needs >= 3 rods NOT saturated on its task. That is now checkable before a
single treatment token is spent.

Run: python -m aea.lab.calibrate
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import statistics
import sys
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.mind import fuel

# THE TASK BANK. Every task is cheap, unambiguously checkable, and probes a different failure mode.
TASKS = {
    "wordcount":  dict(prompt="Count the words in the sentence below and reply with ONLY the number.\n"
                              "the mouth draws power through the ladder and the measure closes the wire",
                       check=H.last_number_is("13"),
                       probes="positional bookkeeping - counting requires tracking, not recall"),
    "batball":    dict(prompt="A bat and a ball cost 1.10 in total. The bat costs 1.00 more than the "
                              "ball. How much does the ball cost? Answer in cents.",
                       check=H.last_number_is("5"),
                       probes="a cognitive trap - the intuitive answer (10) is wrong"),
    "lilypad":    dict(prompt="In a lake there is a patch of lily pads. Every day the patch doubles in "
                              "size. It takes 48 days for the patch to cover the entire lake. How many "
                              "days does it take to cover half the lake? Answer with only the number.",
                       check=H.last_number_is("47"),
                       probes="a trap where halving the result feels like halving the input"),
    "machines":   dict(prompt="If it takes 5 machines 5 minutes to make 5 widgets, how many minutes "
                              "would 100 machines take to make 100 widgets? Answer with only the number.",
                       check=H.last_number_is("5"),
                       probes="a rate trap - the attractive wrong answer is 100"),
    "strictjson": dict(prompt='Reply with only this JSON object and nothing else: '
                              '{"ok": true, "organ": "DRAW"}',
                       check=H.all_of(H.contains('"organ"'), H.starts_with("{")),
                       probes="format obedience - can it emit a bare form with no preamble"),
}

# EIGHT RODS: 1b to 550b, four families, two providers. The three big ones were probed reachable the
# same day; three others were reachable but too slow for an n=8 sweep and are recorded in fuel.TOO_SLOW
# rather than silently omitted.
RODS = [
    ("nvidia", "meta/llama-3.2-1b-instruct"),
    ("nvidia", "meta/llama-3.2-3b-instruct"),
    ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2"),
    ("nvidia", "openai/gpt-oss-20b"),
    ("groq",   "llama-3.3-70b-versatile"),
    ("nvidia", "mistralai/mistral-small-4-119b-2603"),
    ("nvidia", "nvidia/nemotron-3-super-120b-a12b"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),
]

N = 8
# generous, because the two big nemotrons emit their reasoning as visible text - a small budget would
# truncate mid-thought and score a capable rod as a failure
MAX_TOKENS = 700


def classify(passes: int, scored: int) -> str:
    if not scored:
        return "NOT MEASURED"
    if passes >= 7:
        return "SATURATED"
    if passes == 0:
        return "FLOOR"
    return "WINDOW"


def _cell(task_id: str, rod: tuple, n: int) -> dict:
    t = TASKS[task_id]
    exp = {"task": {"prompt": t["prompt"], "recall_q": None}, "check": t["check"],
           "max_tokens": MAX_TOKENS, "judge_rod": None, "n": n}
    a = {"name": "bare", "modules": ["tap", "scorer"], "frame": None, "ctx": {},
         "baseline": True, "expect_precondition": "met"}
    pool = _futures.ThreadPoolExecutor(max_workers=8)
    try:
        futs = [pool.submit(H._trial_retried, exp, a, rod, 0.2, i) for i in range(n)]
        trials = [f.result() for f in futs]
    finally:
        pool.shutdown(wait=True)
    ok = [x for x in trials if x["passed"] is not None]
    att = sum(x.get("attempts", 1) for x in trials)
    passes = sum(1 for x in ok if x["passed"])
    return {"task": task_id, "rod": "%s/%s" % rod, "passes": passes, "scored": len(ok),
            "class": classify(passes, len(ok)),
            "tok_in": sum(x["tok_in"] for x in trials),
            "tok_out": sum(x["tok_out"] for x in trials),
            "ms_median": round(statistics.median([x["ms"] for x in trials])) if trials else None,
            "fuel": fuel.stamp(rod[0], rod[1], n=n, temperature=0.2, max_tokens=MAX_TOKENS,
                               attempts=att, failures=att - len(ok)),
            "check_id": H.check_id(t["check"]), "trials": trials}


def sweep(n: int = N) -> dict:
    cells = []
    for task_id in TASKS:
        for rod in RODS:
            c = _cell(task_id, rod, n)
            cells.append(c)
            print("  %-11s %-42s %d/%-2d %s" % (task_id, "%s/%s" % rod, c["passes"], c["scored"],
                                                c["class"]))
    rep = {"id": "x05_calibrate", "question": "which rods fail which task, measured before any "
                                              "capability is tested",
           "measures": ["C-16"], "n": n, "check": "per-task, see cells", "check_id": "per-cell",
           "rods": ["%s/%s" % r for r in RODS], "refused": [], "cells": cells,
           "effect_min_delta": H.EFFECT_MIN_DELTA, "verdicts": [],
           "usable": {}, "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
    for task_id in TASKS:
        rows = [c for c in cells if c["task"] == task_id]
        rep["usable"][task_id] = {
            "not_saturated": [c["rod"] for c in rows if c["class"] in ("WINDOW", "FLOOR")],
            "window": [c["rod"] for c in rows if c["class"] == "WINDOW"],
            "floor": [c["rod"] for c in rows if c["class"] == "FLOOR"],
            "saturated": [c["rod"] for c in rows if c["class"] == "SATURATED"],
        }
        rep["usable"][task_id]["valid_for_benefit_test"] = \
            len(rep["usable"][task_id]["not_saturated"]) >= H.MIN_RODS
    _save(rep)
    return rep


def _save(rep: dict) -> str:
    d = os.path.join(grid.STATE, "lab", "runs", "x05_calibrate")
    os.makedirs(d, exist_ok=True)
    rid = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    p = os.path.join(d, "%s.json" % rid)
    if os.path.exists(p):
        raise ValueError("refusing to overwrite existing evidence at %s" % p)
    rep["run_id"] = rid
    grid.atomic_save_json(p, rep)
    grid.atomic_save_json(os.path.join(grid.STATE, "lab", "x05_calibrate_latest.json"), rep)
    ip = os.path.join(grid.STATE, "lab", "INDEX.json")
    idx = grid.load_json(ip, {"runs": []})
    idx.setdefault("runs", []).append({
        "experiment": rep["id"], "run_id": rid, "at": rep["at"], "check_id": "per-cell",
        "n": rep["n"], "rods": rep["rods"], "measures": rep["measures"], "verdicts": [],
        "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return p


def render(rep: dict) -> str:
    L = ["THE FAILURE WINDOW - bare only, n=%d, %d rods x %d tasks" %
         (rep["n"], len(RODS), len(TASKS)), ""]
    L.append(H.explain(rep["measures"]))
    L.append("")
    head = "%-42s" % "ROD" + "".join("%-12s" % t[:11] for t in TASKS)
    L.append(head)
    L.append("-" * len(head))
    for rod in rep["rods"]:
        row = "%-42s" % rod.split("/", 1)[-1][:41]
        for t in TASKS:
            c = next((x for x in rep["cells"] if x["task"] == t and x["rod"] == rod), None)
            row += "%-12s" % ("%d/%d %s" % (c["passes"], c["scored"], c["class"][0]) if c else "-")
        L.append(row)
    L.append("")
    L.append("S = SATURATED (>=7/8, measures cost only)   W = WINDOW (1-6/8)   F = FLOOR (0/8)")
    L.append("")
    L.append("USABLE FOR A BENEFIT EXPERIMENT (needs >= %d rods not saturated)" % H.MIN_RODS)
    for t, u in rep["usable"].items():
        L.append("  %-11s %-5s  not-saturated %d  (window %d, floor %d, saturated %d)"
                 % (t, "YES" if u["valid_for_benefit_test"] else "NO",
                    len(u["not_saturated"]), len(u["window"]), len(u["floor"]),
                    len(u["saturated"])))
    return "\n".join(L)


if __name__ == "__main__":
    print("calibrating %d tasks x %d rods x n=%d = %d calls (bare only)"
          % (len(TASKS), len(RODS), N, len(TASKS) * len(RODS) * N))
    r = sweep()
    print()
    print(render(r))
    print()
    print("EVIDENCE  state/lab/runs/x05_calibrate/%s.json" % r["run_id"])
    sys.exit(0)
