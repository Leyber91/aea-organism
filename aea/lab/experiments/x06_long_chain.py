"""x06 - THE LONG CHAIN. L0 against L5: one breath, or carried state?

THE CLAIM UNDER TEST (chapter II, claim 1). There exists a task on which the 550b, unaided, fails, and on
which a construct built from small fuel plus the right organs succeeds. If no such task exists, the AEA is
a small-fuel efficiency technique rather than a capability architecture, and the book must say so.

WHY THIS TASK IS NOT RIGGED. The obvious cheat is to hide information and then observe that the arm with
memory wins - which proves only that storage stores. Here **every arm receives the complete problem.** The
big rod is told the starting value and all N operations in order; nothing is withheld. If it fails it fails
for the one reason L0 cannot fix: a single call is a single breath, and a long chain drifts inside it.

The operations are generated deterministically (no RNG, so the chain is reproducible) and deliberately
resist shortcutting: DOUBLE and HALVE make the sequence order-dependent and parity-dependent, so it cannot
be collapsed into one sum. Ground truth is computed locally in Python, for free.

THE HONEST FRAMING, AND IT IS NOT "L5 WINS". The stepped arm uses the model for every single step, so its
accuracy is a product of per-step accuracies: at 99% per step, 50 steps is 61%. Stepping is not obviously
better - it trades one hard call for many easy ones, and error compounds either way. So the measurement is
not a winner, it is a **CROSSOVER LENGTH**: the chain length at which carried state overtakes one breath.
If there is no crossover, claim 1 dies and that is a real result.

The cost is reported beside it, always: the stepped arm buys its accuracy with N times the calls, and a
construct that needs fifty calls to beat one is only worth it where the one call cannot win at all.

Run: python -m aea.lab.x06_long_chain
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import re
import statistics
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.mind import checkpoint as CP
from aea.mind import fuel

START = 7
LENGTHS = (10, 25, 50)
N = 8

# ONE_BREATH runs on rods that saturate the one-call bank - the point is whether saturation survives length
BIG = [("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),
       ("nvidia", "openai/gpt-oss-20b"),
       ("nvidia", "meta/llama-3.2-3b-instruct")]
# STEPPED runs on the SMALL rod only: the confrontation is a small construct against a large single call
SMALL = ("nvidia", "meta/llama-3.2-3b-instruct")

OPS = ("double", "halve if even, otherwise add 1", "add 3", "subtract 5")


def chain(n: int) -> list:
    """Deterministic op sequence - no RNG, so any run reproduces any other.

    THE CYCLE IS DELIBERATELY BOUNDED. The first version stepped (double, add 3, halve, subtract 5),
    which roughly doubles every four steps: truth(50) came out at 49157. That would have confounded the
    variable under test - a failure at 50 steps could have been five-digit arithmetic rather than drift
    over a long chain, and the experiment would have measured the wrong thing while looking correct.
    In this order the cycle contracts by 2 per 4 steps, so every individual step stays trivial at every
    length and CHAIN LENGTH is the only thing that varies.
    """
    return [OPS[i % len(OPS)] for i in range(n)]


def apply_op(v: int, op: str) -> int:
    if op == "add 3":
        return v + 3
    if op == "double":
        return v * 2
    if op == "subtract 5":
        return v - 5
    return v // 2 if v % 2 == 0 else v + 1


def truth(n: int) -> int:
    v = START
    for op in chain(n):
        v = apply_op(v, op)
    return v


def _numbers(t: str) -> list:
    return re.findall(r"-?\d+", (t or "").replace(",", ""))


def one_breath(rod: tuple, n: int) -> dict:
    """L0. The whole chain in a single call, with the whole problem in the prompt."""
    ops = chain(n)
    listing = "\n".join("%d. %s" % (i + 1, op) for i, op in enumerate(ops))
    prompt = ("Start with the value %d. Apply the following %d operations IN ORDER, one after another, "
              "each to the result of the previous one.\n\n%s\n\n"
              "Reply with ONLY the final number." % (START, n, listing))
    r = grid.call_openai(rod[0], rod[1], [{"role": "user", "content": prompt}],
                         max_tokens=1400, temperature=0.2, timeout=None)
    nums = _numbers(r.get("text") or "")
    return {"ok": bool(r.get("ok")), "answer": nums[-1] if nums else None,
            "calls": 1, "tok_in": r.get("prompt_tokens") or 0, "tok_out": r.get("tokens") or 0,
            "text": r.get("text") or "", "error": r.get("error")}


def stepped(rod: tuple, n: int, trial: int) -> dict:
    """L5. One call per step; C-80 carries the running value. No local arithmetic anywhere - the model
    does every step, the checkpoint only remembers."""
    name = "x06_%d_%d" % (n, trial)
    CP.wipe(name)
    ck = CP.Checkpoint(name, {"value": START, "step": 0}, persist=True)
    rodname = "%s/%s" % rod
    calls = tin = tout = 0
    broke = None
    for i, op in enumerate(chain(n)):
        v = ck.read()["value"]
        if v is None:
            broke = "step %d: the checkpoint held no value" % (i + 1)
            break
        r = grid.call_openai(rod[0], rod[1], [{"role": "user", "content":
                             "The current value is %s. Apply exactly this one operation: %s. "
                             "Reply with ONLY the resulting number." % (v, op)}],
                             max_tokens=60, temperature=0.2, timeout=None)
        calls += 1
        tin += r.get("prompt_tokens") or 0
        tout += r.get("tokens") or 0
        if not r.get("ok"):
            broke = "step %d: %s" % (i + 1, r.get("error"))
            break
        nums = _numbers(r.get("text") or "")
        if not nums:
            broke = "step %d: no number in reply" % (i + 1)
            break
        ck.write(rod=rodname, note=op, value=int(nums[-1]), step=i + 1)
    final = ck.read().get("value")
    return {"ok": broke is None, "answer": str(final) if final is not None else None,
            "calls": calls, "tok_in": tin, "tok_out": tout, "error": broke,
            "revisions": ck.revision, "fuel_trail": ck.fuel_trail(), "checkpoint": name}


def _arm(label: str, fn, rod: tuple, n: int) -> dict:
    pool = _futures.ThreadPoolExecutor(max_workers=8)
    t0 = time.time()
    try:
        if label == "stepped":
            futs = [pool.submit(fn, rod, n, i) for i in range(N)]
        else:
            futs = [pool.submit(fn, rod, n) for _ in range(N)]
        res = [f.result() for f in futs]
    finally:
        pool.shutdown(wait=True)
    exp = str(truth(n))
    ok = [r for r in res if r["ok"]]
    passes = sum(1 for r in ok if r["answer"] == exp)
    return {"arm": label, "rod": "%s/%s" % rod, "length": n, "expected": exp,
            "passes": passes, "scored": len(ok), "failures": len(res) - len(ok),
            "calls": sum(r["calls"] for r in res), "tok_in": sum(r["tok_in"] for r in res),
            "tok_out": sum(r["tok_out"] for r in res), "wall_s": round(time.time() - t0, 1),
            "answers": [r["answer"] for r in res],
            "errors": [r["error"] for r in res if r.get("error")][:3],
            "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=0.2,
                               attempts=len(res), failures=len(res) - len(ok)),
            "trials": res}


def run() -> dict:
    rows = []
    for n in LENGTHS:
        print("  chain length %d - ground truth %d" % (n, truth(n)))
        for rod in BIG:
            r = _arm("one_breath", one_breath, rod, n)
            rows.append(r)
            print("    %-12s %-42s %d/%-2d  %d calls  %5.1fs" %
                  (r["arm"], r["rod"], r["passes"], r["scored"], r["calls"], r["wall_s"]))
        r = _arm("stepped", stepped, SMALL, n)
        rows.append(r)
        print("    %-12s %-42s %d/%-2d  %d calls  %5.1fs" %
              (r["arm"], r["rod"], r["passes"], r["scored"], r["calls"], r["wall_s"]))
    rep = {"id": "x06_long_chain", "question": "at what chain length does carried state overtake one "
                                               "breath?",
           "measures": ["C-80", "C-16"], "n": N, "lengths": list(LENGTHS), "start": START,
           "ops": list(OPS), "rows": rows, "refused": [],
           "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
    d = os.path.join(grid.STATE, "lab", "runs", "x06_long_chain")
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
                                       "check_id": "exact-final-value", "n": N,
                                       "rods": sorted({r["rod"] for r in rows}),
                                       "measures": rep["measures"], "verdicts": [],
                                       "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


def render(rep: dict) -> str:
    L = ["THE LONG CHAIN - L0 (one breath) against L5 (carried state), n=%d" % rep["n"], ""]
    L.append("%-12s %-34s %-6s %-7s %-8s %-9s %s" %
             ("LENGTH", "ARM / ROD", "PASS", "CALLS", "TOK IN", "WALL", "ANSWERS"))
    L.append("-" * 108)
    for n in rep["lengths"]:
        for r in [x for x in rep["rows"] if x["length"] == n]:
            L.append("%-12s %-34s %-6s %-7d %-8d %-9s %s" %
                     ("%d (=%s)" % (n, r["expected"]),
                      "%s %s" % (r["arm"][:9], r["rod"].split("/")[-1][:22]),
                      "%d/%d" % (r["passes"], r["scored"]), r["calls"], r["tok_in"],
                      "%.1fs" % r["wall_s"],
                      ",".join(str(a) for a in r["answers"][:5])))
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    print("x06 THE LONG CHAIN - lengths %s, n=%d" % (list(LENGTHS), N))
    print("ground truth computed locally:", {n: truth(n) for n in LENGTHS})
    rep = run()
    print()
    print(render(rep))
    print("EVIDENCE  state/lab/runs/x06_long_chain/%s.json" % rep["run_id"])
