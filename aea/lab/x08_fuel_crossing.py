"""x08 - IF THE FUEL CHANGES, WHAT STAYS? The other half of C-80, and chapter II's title question.

x06b established that carried state repairs a rod that drifts: nemotron-9b on a 50-step chain went from
9/16 in one breath to 11/11 stepped. That proves the checkpoint works FOR ONE ROD. It says nothing about
the question the chapter is named for.

THE CLAIM UNDER TEST (chapter II, claim 2). State written on one fuel can be read and continued on
another, and the construct that results is recognisably the same construct.

WHY IT MATTERS MORE THAN IT SOUNDS. Law IV says the same composition on different fuel is a different
organism - one composition gave four verdicts across five rods. If that holds, then nothing about the
construct itself makes it one entity across a fuel change, and the only candidate is the state it shares.
The census records C-80 as EMBODIED; the code contains none of it; thirty-five separate files stand in its
place, each written alone and read alone. So this asks whether those files are one self or thirty-five
strangers, and roughly forty items downstream wait on the answer.

FOUR ARMS, all on the same 50-step chain, all with ground truth computed locally:

  A  9b ALONE            all 50 steps on nemotron-9b            - the x06b baseline, re-measured here
  B  20b ALONE           all 50 steps on gpt-oss-20b            - the accurate rod, stepped
  C  HANDOFF 9b -> 20b   steps 1-25 on the 9b, then the SAME checkpoint handed to the 20b
  D  HANDOFF 20b -> 9b   the reverse, because a handoff may only work downhill

C and D are the experiment. If a handoff finishes as well as the stronger arm, the checkpoint carries
identity across fuel and C-80 earns its EMBODIED mark in substance rather than in the document. If the
handoff breaks - drifts, stalls, or silently continues a different computation - then the thirty-five
files are strangers, C-80 is genuinely missing, and the route ahead changes.

The checkpoint records a `fuel_trail` of every rod that wrote it, so the crossing is readable from the
artefact itself rather than inferred from the score.

Run: python -m aea.lab.x08_fuel_crossing
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import re
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.lab.x06_long_chain import START, chain, truth
from aea.mind import checkpoint as CP
from aea.mind import fuel

LENGTH = 50
HANDOFF_AT = 25
N = 8
TEMP = 0.0

NINE = ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2")
TWENTY = ("nvidia", "openai/gpt-oss-20b")


def _step(rod, v, op):
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content":
                     "The current value is %s. Apply exactly this one operation: %s. "
                     "Reply with ONLY the resulting number." % (v, op)}],
                     max_tokens=400, temperature=TEMP)
    if not r.get("ok"):
        return None, r
    n = re.findall(r"-?\d+", (r.get("text") or "").replace(",", ""))
    return (int(n[-1]) if n else None), r


def _walk(name, plan, trial):
    """Run the chain with a per-step rod schedule. `plan` maps step index -> rod.

    ONE checkpoint object for the whole walk, whichever rod is writing. That is the point: the construct
    is not the rod, it is the state plus whatever is currently burning.
    """
    ck_name = "x08_%s_%d" % (name, trial)
    CP.wipe(ck_name)
    ck = CP.Checkpoint(ck_name, {"value": START, "step": 0})
    calls = tin = tout = 0
    broke = None
    for i, op in enumerate(chain(LENGTH)):
        rod = plan(i)
        got, r = _step(rod, ck.read()["value"], op)
        calls += 1
        tin += r.get("prompt_tokens") or 0
        tout += r.get("tokens") or 0
        if got is None:
            broke = "step %d on %s: %s" % (i + 1, rod[1], r.get("error") or "no number")
            break
        ck.write(rod="%s/%s" % rod, note=op, value=got, step=i + 1)
    return {"ok": broke is None, "answer": ck.read().get("value"), "calls": calls,
            "tok_in": tin, "tok_out": tout, "error": broke, "revisions": ck.revision,
            "fuel_trail": ck.fuel_trail(), "crossed_fuel": ck.crossed_fuel(),
            "checkpoint": ck_name}


ARMS = {
    "A_9b_alone":       lambda i: NINE,
    "B_20b_alone":      lambda i: TWENTY,
    "C_handoff_9_to_20": lambda i: NINE if i < HANDOFF_AT else TWENTY,
    "D_handoff_20_to_9": lambda i: TWENTY if i < HANDOFF_AT else NINE,
}


def arm(name, plan):
    exp = truth(LENGTH)
    pool = _futures.ThreadPoolExecutor(max_workers=N)
    t0 = time.time()
    try:
        res = [f.result() for f in [pool.submit(_walk, name, plan, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [r for r in res if r["ok"]]
    passes = sum(1 for r in ok if r["answer"] == exp)
    trails = sorted({" -> ".join(r["fuel_trail"]) for r in res})
    row = {"arm": name, "length": LENGTH, "handoff_at": HANDOFF_AT, "expected": exp,
           "passes": passes, "scored": len(ok), "failures": len(res) - len(ok),
           "calls": sum(r["calls"] for r in res), "tok_in": sum(r["tok_in"] for r in res),
           "wall_s": round(time.time() - t0, 1),
           "answers": [r["answer"] for r in res],
           "crossed_fuel": all(r["crossed_fuel"] for r in res) if "handoff" in name else False,
           "fuel_trails": trails,
           "errors": [r["error"] for r in res if r.get("error")][:3],
           "trials": res}
    print("  %-20s %d/%-2d  calls=%-4d %6.1fs  trail: %s" %
          (name, passes, len(ok), row["calls"], row["wall_s"], trails[0][:60]), flush=True)
    return row


def run():
    print("x08 - chain %d, handoff at %d, n=%d, ground truth %d"
          % (LENGTH, HANDOFF_AT, N, truth(LENGTH)))
    rows = [arm(k, v) for k, v in ARMS.items()]
    by = {r["arm"]: r for r in rows}

    def rate(k):
        r = by[k]
        return (r["passes"] / r["scored"]) if r["scored"] else None

    verdict = None
    a, b = rate("A_9b_alone"), rate("B_20b_alone")
    c, d = rate("C_handoff_9_to_20"), rate("D_handoff_20_to_9")
    if None not in (a, b, c, d):
        weaker, stronger = min(a, b), max(a, b)
        # SATURATION GUARD. Added 2026-07-25 immediately after the first run, which returned 100% on all
        # four arms. A comparison where every arm is perfect has NO HEADROOM: it cannot distinguish "the
        # handoff costs nothing" from "the task was too easy to reveal a cost". The same ceiling effect
        # shaped chapter II's opening and voided most of x03 and x04, and this is its third appearance.
        # Passing a saturated comparison off as a confirmation would be the exact error the harness exists
        # to prevent, so it is reported as NO RESOLUTION instead.
        if min(a, b, c, d) >= 1.0:
            verdict = ("NO RESOLUTION - all four arms scored 100%%, so the comparison has no headroom. "
                       "What IS established: a handoff introduced no measurable degradation in either "
                       "direction (%d and %d of %d trials, fuel_trail confirms two rods wrote each "
                       "checkpoint). What is NOT established: that a handoff is free under stress, "
                       "because nothing here was under stress."
                       % (by["C_handoff_9_to_20"]["passes"], by["D_handoff_20_to_9"]["passes"], N))
        elif c >= stronger - 0.15 and d >= weaker - 0.15:
            verdict = ("THE CHECKPOINT CARRIES ACROSS FUEL. Handoffs finished at %.0f%% (9b->20b) and "
                       "%.0f%% (20b->9b) against %.0f%% and %.0f%% for the single-rod arms. State "
                       "written on one fuel was continued on another without breaking, so C-80 earns "
                       "its EMBODIED mark in substance." % (100 * c, 100 * d, 100 * a, 100 * b))
        elif c < weaker or d < weaker:
            verdict = ("A HANDOFF COSTS SOMETHING THE SINGLE-ROD ARMS DO NOT. Handoffs %.0f%% and %.0f%% "
                       "against %.0f%% and %.0f%% alone - the crossing itself degrades the work, so the "
                       "thirty-five files behave more like strangers than one self."
                       % (100 * c, 100 * d, 100 * a, 100 * b))
        else:
            verdict = ("MIXED - handoffs %.0f%% and %.0f%%, alone %.0f%% and %.0f%%. Direction may "
                       "matter: a handoff uphill is not the same as downhill."
                       % (100 * c, 100 * d, 100 * a, 100 * b))

    rep = {"id": "x08_fuel_crossing",
           "question": "can state written on one fuel be read and continued on another?",
           "measures": ["C-80", "C-16", "C-84"], "n": N, "temperature": TEMP,
           "length": LENGTH, "handoff_at": HANDOFF_AT, "rows": rows, "verdict": verdict,
           "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}

    d_ = os.path.join(grid.STATE, "lab", "runs", "x08_fuel_crossing")
    os.makedirs(d_, exist_ok=True)
    rid = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    p = os.path.join(d_, "%s.json" % rid)
    if os.path.exists(p):
        raise ValueError("refusing to overwrite evidence at %s" % p)
    rep["run_id"] = rid
    grid.atomic_save_json(p, rep)
    ip = os.path.join(grid.STATE, "lab", "INDEX.json")
    idx = grid.load_json(ip, {"runs": []})
    idx.setdefault("runs", []).append({"experiment": rep["id"], "run_id": rid, "at": rep["at"],
                                      "check_id": "exact-final-value", "n": N,
                                      "rods": ["%s/%s" % NINE, "%s/%s" % TWENTY],
                                      "measures": rep["measures"], "verdicts": [],
                                      "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


if __name__ == "__main__":
    r = run()
    print()
    print("VERDICT:", r["verdict"])
    print("EVIDENCE  state/lab/runs/x08_fuel_crossing/%s.json" % r["run_id"])
