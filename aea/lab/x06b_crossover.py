"""x06b - THE CROSSOVER, done properly. Calibrate the UNIT OF WORK first, then find where L0 breaks.

WHY THERE IS A SECOND VERSION. x06 put the stepped arm on llama-3.2-3b and it scored 0/8 at every length.
That was not a finding about carried state; it was a finding about the 3b, which cannot do a single one of
these operations reliably. I had calibrated the TASKS and never the UNIT OF WORK - I built a fifty-step
chain out of an operation whose per-step accuracy I had never measured. It was the third time in this
project that a treatment went onto a rod that could not carry it, which is law I violated at the arm level.

So this runs in three phases, cheap before expensive, and each phase decides the next:

  A  PER-STEP CALIBRATION. Single operations, seven of them, covering every op and both signs. This gives
     p, the per-step accuracy, per rod, per temperature. A stepped arm of length L can at best reach p^L,
     so p is what says whether an arm is even possible: at p=0.99, fifty steps is 61%; at p=0.90 it is 0.5%.
  B  FIND WHERE L0 BREAKS. One-breath only, cheap (8 calls per length), sweeping length upward on the rods
     phase A says are accurate. gpt-oss-20b held 8/8 at length 50 in x06, so the break is further out.
  C  THE CONFRONTATION, at the break length only. Stepped versus one-breath on the same rod, where one
     breath demonstrably fails. This is the single expensive run, and it is aimed rather than sprayed.

AND THE TEMPERATURE DEBT IS PAID HERE. Every measurement in this project was taken at 0.2 and never
varied; fuel.py has flagged it KNOWN/UNSET since it was written, which means variance attributed to noise
was partly unmeasured sampling. Phase A sweeps 0.0, 0.2 and 0.7 - and because a chain multiplies per-step
accuracy, temperature should matter MORE the longer the chain, which is itself a prediction to check.

Run: python -m aea.lab.x06b_crossover
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import re
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.lab.x06_long_chain import START, apply_op, chain, truth
from aea.mind import checkpoint as CP
from aea.mind import fuel

TEMPS = (0.0, 0.2, 0.7)
STEP_N = 4                      # trials per (rod, temp, pair)
LENGTHS = (50, 100, 200)        # phase B sweep; x06 already showed 20b holds 50
CONF_N = 8

RODS = [
    ("nvidia", "meta/llama-3.2-3b-instruct"),
    ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2"),
    ("nvidia", "openai/gpt-oss-20b"),
    ("groq",   "llama-3.3-70b-versatile"),
    ("nvidia", "nvidia/nemotron-3-super-120b-a12b"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),
]

# every op, both signs, both parities - the unit of work, isolated
PAIRS = [(7, "double"), (14, "halve if even, otherwise add 1"),
         (7, "halve if even, otherwise add 1"), (5, "add 3"), (3, "subtract 5"),
         (-10, "halve if even, otherwise add 1"), (-3, "double")]

# a stepped arm is only worth running if it could plausibly finish the chain
P_FLOOR = 0.98


def _nums(t):
    return re.findall(r"-?\d+", (t or "").replace(",", ""))


def _one_step(rod, v, op, temp):
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content":
                     "The current value is %s. Apply exactly this one operation: %s. "
                     "Reply with ONLY the resulting number." % (v, op)}],
                     max_tokens=400, temperature=temp)
    if not r.get("ok"):
        return None, r
    n = _nums(r.get("text") or "")
    return (n[-1] if n else None), r


def phase_a() -> list:
    out = []
    for rod in RODS:
        for temp in TEMPS:
            pool = _futures.ThreadPoolExecutor(max_workers=8)
            try:
                jobs = [(v, op) for v, op in PAIRS for _ in range(STEP_N)]
                futs = [pool.submit(_one_step, rod, v, op, temp) for v, op in jobs]
                res = [f.result() for f in futs]
            finally:
                pool.shutdown(wait=True)
            ok = 0
            fails = 0
            tin = tout = 0
            for (v, op), (got, r) in zip(jobs, res):
                if got is None:
                    fails += 1
                    continue
                tin += r.get("prompt_tokens") or 0
                tout += r.get("tokens") or 0
                if got == str(apply_op(v, op)):
                    ok += 1
            scored = len(jobs) - fails
            p = round(ok / scored, 4) if scored else None
            row = {"phase": "A", "rod": "%s/%s" % rod, "temperature": temp, "correct": ok,
                   "scored": scored, "failures": fails, "p_step": p, "tok_in": tin, "tok_out": tout,
                   "p50": round(p ** 50, 4) if p else None,
                   "p200": round(p ** 200, 6) if p else None,
                   "fuel": fuel.stamp(rod[0], rod[1], n=STEP_N, temperature=temp,
                                      attempts=len(jobs), failures=fails)}
            out.append(row)
            print("  A  %-42s t=%.1f  p=%-7s %d/%-3d  p^50=%-8s p^200=%s"
                  % (rod[1][:41], temp, p, ok, scored, row["p50"], row["p200"]))
    return out


def _breath(rod, n, temp):
    ops = chain(n)
    listing = "\n".join("%d. %s" % (i + 1, o) for i, o in enumerate(ops))
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content":
                     "Start with the value %d. Apply the following %d operations IN ORDER, one after "
                     "another, each to the result of the previous one.\n\n%s\n\n"
                     "Reply with ONLY the final number." % (START, n, listing)}],
                     max_tokens=2600, temperature=temp)
    nn = _nums(r.get("text") or "")
    return {"ok": bool(r.get("ok")), "answer": nn[-1] if nn else None,
            "tok_in": r.get("prompt_tokens") or 0, "tok_out": r.get("tokens") or 0,
            "error": r.get("error")}


def phase_b(rods, temp) -> list:
    out = []
    for n in LENGTHS:
        exp = str(truth(n))
        for rod in rods:
            pool = _futures.ThreadPoolExecutor(max_workers=8)
            t0 = time.time()
            try:
                res = [f.result() for f in
                       [pool.submit(_breath, rod, n, temp) for _ in range(CONF_N)]]
            finally:
                pool.shutdown(wait=True)
            ok = [r for r in res if r["ok"]]
            passes = sum(1 for r in ok if r["answer"] == exp)
            row = {"phase": "B", "arm": "one_breath", "rod": "%s/%s" % rod, "length": n,
                   "temperature": temp, "expected": exp, "passes": passes, "scored": len(ok),
                   "failures": len(res) - len(ok), "calls": len(res),
                   "tok_in": sum(r["tok_in"] for r in res),
                   "wall_s": round(time.time() - t0, 1),
                   "answers": [r["answer"] for r in res]}
            out.append(row)
            print("  B  len=%-4d %-42s %d/%-2d  %5.1fs" %
                  (n, rod[1][:41], passes, len(ok), row["wall_s"]))
    return out


def _stepped(rod, n, temp, trial):
    name = "x06b_%d_%d" % (n, trial)
    CP.wipe(name)
    ck = CP.Checkpoint(name, {"value": START, "step": 0})
    rodname = "%s/%s" % rod
    calls = tin = tout = 0
    broke = None
    for i, op in enumerate(chain(n)):
        got, r = _one_step(rod, ck.read()["value"], op, temp)
        calls += 1
        tin += r.get("prompt_tokens") or 0
        tout += r.get("tokens") or 0
        if got is None:
            broke = "step %d: %s" % (i + 1, r.get("error") or "no number")
            break
        ck.write(rod=rodname, note=op, value=int(got), step=i + 1)
    return {"ok": broke is None, "answer": str(ck.read().get("value")), "calls": calls,
            "tok_in": tin, "tok_out": tout, "error": broke, "revisions": ck.revision}


def phase_c(rod, n, temp) -> dict:
    exp = str(truth(n))
    pool = _futures.ThreadPoolExecutor(max_workers=CONF_N)
    t0 = time.time()
    try:
        res = [f.result() for f in
               [pool.submit(_stepped, rod, n, temp, i) for i in range(CONF_N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [r for r in res if r["ok"]]
    passes = sum(1 for r in ok if r["answer"] == exp)
    row = {"phase": "C", "arm": "stepped", "rod": "%s/%s" % rod, "length": n, "temperature": temp,
           "expected": exp, "passes": passes, "scored": len(ok), "failures": len(res) - len(ok),
           "calls": sum(r["calls"] for r in res), "tok_in": sum(r["tok_in"] for r in res),
           "wall_s": round(time.time() - t0, 1), "answers": [r["answer"] for r in res],
           "errors": [r["error"] for r in res if r.get("error")][:3]}
    print("  C  len=%-4d %-42s %d/%-2d  %d calls  %5.1fs" %
          (n, rod[1][:41], passes, len(ok), row["calls"], row["wall_s"]))
    return row


def run() -> dict:
    print("PHASE A - per-step accuracy, %d rods x %d temps x %d pairs x n=%d"
          % (len(RODS), len(TEMPS), len(PAIRS), STEP_N))
    a = phase_a()

    # best temperature per rod, then the rods accurate enough for a stepped arm to be possible
    best = {}
    for r in a:
        if r["p_step"] is None:
            continue
        if r["scored"] < 20:
            continue
        if r["rod"] not in best or r["p_step"] > best[r["rod"]]["p_step"]:
            best[r["rod"]] = r
    # A THIN CELL CANNOT PICK A ROD. In the first run, 120b at t=0.7 scored 0 of 28 and 70b at t=0.7
    # scored 3 of 28 - all 429s - yet both read as p=1.0 and cleared the floor. p is meaningless without
    # the count behind it, which is the underpowered rule applied at selection instead of at verdict.
    MIN_CELL = 20
    strong = [r for r in best.values() if r["p_step"] >= P_FLOOR and r["scored"] >= MIN_CELL]
    strong.sort(key=lambda r: -r["p_step"])
    print()
    print("  rods with per-step p >= %.2f (a stepped arm is possible at all): %s"
          % (P_FLOOR, ", ".join("%s p=%.3f t=%.1f" % (r["rod"].split("/")[-1], r["p_step"],
                                                      r["temperature"]) for r in strong) or "NONE"))
    if not strong:
        return {"id": "x06b_crossover", "phase_a": a, "phase_b": [], "phase_c": None,
                "conclusion": "no rod reached the per-step floor - a stepped arm of any useful length "
                              "is impossible on this fuel, and claim 1 cannot be tested this way",
                "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}

    pick = strong[0]
    temp = pick["temperature"]
    rods_b = [tuple(r["rod"].split("/", 1)) for r in strong[:3]]
    print()
    print("PHASE B - where does one breath break? temp=%.1f" % temp)
    b = phase_b(rods_b, temp)

    # the break: the shortest length where the strongest rod drops below 7/8
    rodname = pick["rod"]
    mine = [r for r in b if r["rod"] == rodname]
    broke = next((r for r in sorted(mine, key=lambda r: r["length"]) if r["passes"] < 7), None)
    print()
    c = None
    if broke:
        print("PHASE C - one breath breaks at length %d (%d/%d). Now the stepped arm, same rod."
              % (broke["length"], broke["passes"], broke["scored"]))
        c = phase_c(tuple(rodname.split("/", 1)), broke["length"], temp)
        concl = ("one breath breaks at %d (%d/%d); stepped scored %d/%d at %dx the calls"
                 % (broke["length"], broke["passes"], broke["scored"], c["passes"], c["scored"],
                    broke["length"]))
    else:
        concl = ("one breath did NOT break by length %d on %s - claim 1 is not supported at these "
                 "lengths and the honest reading is that a long deterministic chain is not the task "
                 "class that needs the architecture" % (max(LENGTHS), rodname))
        print("  " + concl)

    rep = {"id": "x06b_crossover", "question": "at what chain length does carried state overtake one "
                                               "breath, on a rod that can carry either?",
           "measures": ["C-80", "C-16"], "p_floor": P_FLOOR, "temps": list(TEMPS),
           "lengths": list(LENGTHS), "n": CONF_N, "phase_a": a, "phase_b": b, "phase_c": c,
           "chosen": {"rod": rodname, "temperature": temp, "p_step": pick["p_step"]},
           "conclusion": concl, "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}

    d = os.path.join(grid.STATE, "lab", "runs", "x06b_crossover")
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
                                      "check_id": "exact-final-value", "n": CONF_N,
                                      "rods": [r["rod"] for r in a[:0]] or [x[1] for x in RODS],
                                      "measures": rep["measures"], "verdicts": [],
                                      "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


if __name__ == "__main__":
    r = run()
    print()
    print("CONCLUSION:", r["conclusion"])
    print("EVIDENCE  state/lab/runs/x06b_crossover/%s.json" % r.get("run_id", "(not saved)"))
