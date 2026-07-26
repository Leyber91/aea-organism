"""x07 - CAN A ROD PREDICT ITS OWN FAILURE? The experiment that decides two rung placements.

WHY THIS RUNS BEFORE ANYTHING ELSE. The linear hierarchy places `C-26 ceiling-detect` at L4 (a different
fuel) and `C-17 self-model` at L5 (state that outlives the call). Both placements were judgment calls, and
both reduce to one measurable question. A placement claim is falsifiable in a specific way: item X sits at
rung N because rung N-1 cannot do it. So:

  IF A ROD CAN ACCURATELY SAY "I WILL FAIL THIS", then ceiling-detect costs one cheap call and needs
  neither a second rod nor persistent state. It belongs at L1, the routing layer above it becomes an
  optimisation rather than a requirement, and C-26, C-70 and C-71 all move down.

  IF IT CANNOT, then knowing a rod's ceiling requires measuring it from outside. The calibration table
  becomes load-bearing rather than convenient, and L4 is correct.

TWO PROBES, because they test different rungs:

  PROSPECTIVE   "will you get this right?" asked BEFORE the attempt. This is C-26/C-17 - self-knowledge.
  RETROSPECTIVE "did you get that right?" asked AFTER, with its own answer in front of it. This tests
                whether THE MEASURE (L1, currently local deterministic work costing 0ms) could be a model
                call instead. If a rod reliably knows it was wrong, a cheap self-check substitutes for an
                external scorer, and L1's content changes.

GROUND TRUTH IS MEASURED IN THE SAME RUN rather than read from x05, so a rod's prediction and its
performance come from the same minutes on the same fuel. The comparison that matters is not overall
accuracy - a rod that always says YES scores well on tasks it passes. The discriminating cells are the
ones it FAILS: does it say NO there? That is measured separately as `honest_on_failure`.

Run: python -m aea.lab.x07_self_assessment
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.lab.calibrate import TASKS
from aea.mind import fuel

N = 8
TEMP = 0.0
RODS = [
    ("nvidia", "meta/llama-3.2-3b-instruct"),
    ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2"),
    ("nvidia", "openai/gpt-oss-20b"),
    ("groq",   "llama-3.3-70b-versatile"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),
]


def _yesno(text: str):
    """Read a YES/NO verdict without letting a reasoning preamble decide it."""
    t = (text or "").strip().upper()
    for line in reversed([x.strip() for x in t.splitlines() if x.strip()]):
        y = line.startswith("YES") or line.endswith("YES")
        n = line.startswith("NO") or line.endswith("NO")
        if y and n:
            return None          # ambiguous - never guess, and never guess toward YES
        if y:
            return True
        if n:
            return False
    if "YES" in t and "NO" not in t:
        return True
    if "NO" in t and "YES" not in t:
        return False
    return None


def _trial(rod, task_id, i):
    t = TASKS[task_id]
    out = {"trial": i, "task": task_id}

    # 1 PROSPECTIVE - self-knowledge before the attempt
    r1 = H.call_gated(rod[0], rod[1], [{"role": "user", "content":
                      "You will be asked the question below. Before answering it, judge whether YOU will "
                      "get it right. Reply with ONLY the single word YES or NO.\n\nQUESTION:\n"
                      + t["prompt"]}], max_tokens=400, temperature=TEMP)
    out["prospective_raw"] = (r1.get("text") or "") if r1.get("ok") else None
    out["prospective"] = _yesno(out["prospective_raw"])

    # 2 THE ATTEMPT - ground truth, same rod, same minutes
    r2 = H.call_gated(rod[0], rod[1], [{"role": "user", "content": t["prompt"]}],
                      max_tokens=700, temperature=TEMP)
    if not r2.get("ok"):
        out["actual"] = None
        return out
    answer = r2.get("text") or ""
    out["actual"] = bool(t["check"](answer))

    # 3 RETROSPECTIVE - can it mark its own work?
    r3 = H.call_gated(rod[0], rod[1], [{"role": "user", "content":
                      "QUESTION:\n" + t["prompt"] + "\n\nAN ANSWER WAS GIVEN:\n" + answer[-1500:] +
                      "\n\nIs that answer correct? Reply with ONLY the single word YES or NO."}],
                      max_tokens=400, temperature=TEMP)
    out["retrospective_raw"] = (r3.get("text") or "") if r3.get("ok") else None
    out["retrospective"] = _yesno(out["retrospective_raw"])
    out["answer_raw"] = answer
    out["tok_in"] = sum((r.get("prompt_tokens") or 0) for r in (r1, r2, r3))
    out["tok_out"] = sum((r.get("tokens") or 0) for r in (r1, r2, r3))
    return out


def cell(rod, task_id):
    pool = _futures.ThreadPoolExecutor(max_workers=8)
    try:
        trials = [f.result() for f in [pool.submit(_trial, rod, task_id, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    scored = [t for t in trials if t.get("actual") is not None]
    passed = [t for t in scored if t["actual"]]
    failed = [t for t in scored if not t["actual"]]

    def agree(key, subset):
        u = [t for t in subset if t.get(key) is not None]
        return (sum(1 for t in u if t[key] == t["actual"]), len(u))

    pro_all, pro_n = agree("prospective", scored)
    ret_all, ret_n = agree("retrospective", scored)
    pro_fail, pro_fn = agree("prospective", failed)
    ret_fail, ret_fn = agree("retrospective", failed)
    return {"rod": "%s/%s" % rod, "task": task_id,
            "actual_pass": len(passed), "scored": len(scored),
            "prospective_agree": pro_all, "prospective_n": pro_n,
            "retrospective_agree": ret_all, "retrospective_n": ret_n,
            "honest_on_failure_pro": pro_fail, "failures": len(failed), "pro_fail_n": pro_fn,
            "honest_on_failure_ret": ret_fail, "ret_fail_n": ret_fn,
            "said_yes": sum(1 for t in scored if t.get("prospective") is True),
            "tok_in": sum(t.get("tok_in", 0) for t in trials),
            "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                               attempts=len(trials), failures=len(trials) - len(scored)),
            "trials": trials}


def run():
    cells = []
    print("x07 - %d rods x %d tasks x n=%d x 3 probes" % (len(RODS), len(TASKS), N))
    for rod in RODS:
        for task_id in TASKS:
            c = cell(rod, task_id)
            cells.append(c)
            print("  %-42s %-11s actual %d/%-2d  said-YES %d/%-2d  pro-agree %d/%-2d  "
                  "honest-on-fail %d/%-2d" %
                  (rod[1][:41], task_id, c["actual_pass"], c["scored"], c["said_yes"], c["scored"],
                   c["prospective_agree"], c["prospective_n"],
                   c["honest_on_failure_pro"], c["pro_fail_n"]), flush=True)
    rep = {"id": "x07_self_assessment",
           "question": "can a rod predict its own failure, and can it mark its own work?",
           "measures": ["C-26", "C-17", "C-15"], "n": N, "temperature": TEMP,
           "decides": "the rung placement of C-26 (L4) and C-17 (L5), and whether L1's MEASURE could be "
                      "a model call instead of local deterministic work",
           "cells": cells, "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}

    # THE VERDICT, computed rather than eyeballed
    tot_f = sum(c["pro_fail_n"] for c in cells)
    hit_f = sum(c["honest_on_failure_pro"] for c in cells)
    tot_r = sum(c["ret_fail_n"] for c in cells)
    hit_r = sum(c["honest_on_failure_ret"] for c in cells)
    rep["summary"] = {
        "prospective_honest_on_failure": [hit_f, tot_f],
        "retrospective_honest_on_failure": [hit_r, tot_r],
        "verdict": None}
    if tot_f >= 20:
        rate = hit_f / tot_f
        if rate >= 0.7:
            v = ("rods DO predict their own failure (%d of %d) - C-26 ceiling-detect costs one cheap "
                 "call and belongs at L1, not L4; the routing layer becomes an optimisation"
                 % (hit_f, tot_f))
        elif rate <= 0.3:
            v = ("rods do NOT predict their own failure (%d of %d) - a ceiling can only be known by "
                 "measuring from outside, so C-26/C-70/C-71 stay at L4 and the calibration table is "
                 "load-bearing" % (hit_f, tot_f))
        else:
            v = ("mixed (%d of %d) - self-assessment is real but unreliable; it cannot replace external "
                 "measurement and the L4 placement stands with a note" % (hit_f, tot_f))
        rep["summary"]["verdict"] = v
    else:
        rep["summary"]["verdict"] = ("too few failure cells (%d) to decide - the rods passed too much"
                                     % tot_f)

    d = os.path.join(grid.STATE, "lab", "runs", "x07_self_assessment")
    os.makedirs(d, exist_ok=True)
    rid = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    p = os.path.join(d, "%s.json" % rid)
    if os.path.exists(p):
        raise ValueError("refusing to overwrite evidence at %s" % p)
    rep["run_id"] = rid
    grid.atomic_save_json(p, rep)
    ip = os.path.join(grid.STATE, "lab", "INDEX.json")
    idx = grid.load_json(ip, {"runs": []})
    idx.setdefault("runs", []).append({"experiment": rep["id"], "run_id": rid, "at": rep["at"],
                                      "check_id": "per-task", "n": N,
                                      "rods": ["%s/%s" % r for r in RODS],
                                      "measures": rep["measures"], "verdicts": [],
                                      "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


if __name__ == "__main__":
    r = run()
    s = r["summary"]
    print()
    print("PROSPECTIVE  honest on the cells it failed: %d of %d" % tuple(s["prospective_honest_on_failure"]))
    print("RETROSPECTIVE honest on the cells it failed: %d of %d" % tuple(s["retrospective_honest_on_failure"]))
    print()
    print("VERDICT:", s["verdict"])
    print("EVIDENCE  state/lab/runs/x07_self_assessment/%s.json" % r["run_id"])
