"""x10 - THE COVERAGE SWEEP. Every size class, four temperatures, three framings, one task.

WHY THIS EXISTS. An audit of `state/lab/INDEX.json` against `state/capability_census.json` says the lab has
been measuring a sliver:

  RODS          ~11 distinct of 115 scored in the census (~10%)
  PLANTS        3 of the 6 with live models; 3 of 15 configured
  TEMPERATURES  0.0 in six runs, 0.2 in one. Effectively ONE POINT on an axis nobody varied.
  SIZE CLASSES  large / normal / micro / nano touched; PICO never
  FRAMINGS      bare, posture, fitted, +readout - all on one task family

**THE TEMPERATURE GAP IS THE ONE THAT ALREADY COST SOMETHING**, and it is why this experiment leads with it
rather than with model count. D15: at temperature 0.0 ollama returned BYTE-IDENTICAL replies in 11 of 12
cells, so n=8 was n=1 and the harness could not tell power from repetition - and a claim that the posture
frame "converts" llama3.1:8b got written down before the check caught it (5/8 vs 3/8 bare at the game's real
temperature, within noise by the harness's own EFFECT_MIN_DELTA=3). Worse, `bench_core` sets no temperature
at all, so the product fires at 0.2 while the lab was measuring at 0.0. One axis, unexplored, wrong value,
and it manufactured a false finding.

THE DESIGN - one task held fixed so the axes mean something.

  TASK        wordcount, 13 words, exact local check. The task x01/x02 measured, so the sweep extends a
              known result rather than starting a new one.
  FRAMINGS    bare | posture (the only non-trivial template the bench can seat) | fitted (names the METHOD)
              ...and THE READOUT computed FREE from every reply, since it is local parsing, not a call.
  TEMPS       0.0, 0.2, 0.7, 1.0 - deterministic through creative, with 0.2 marked as the product's own.
  RODS        stratified across FIVE size tiers and FOUR plants, so law IV can be tested rather than
              assumed: the same composition on different fuel is a different organism.

WHAT IT CAN ANSWER THAT NO SINGLE-ROD RUN CAN:
  - is THE FRAME's benefit a small-rod phenomenon, or does it hold up the size ladder? (the precondition
    boundary, mapped instead of asserted)
  - does THE READOUT pay broadly? it is the only rung that costs ZERO, so if it pays across fuel it is the
    highest-value part in the whole architecture and the forge queue is wrong.
  - where does determinism break, per plant? the effective-n curve against temperature, which is the fix
    for D15 rather than a note about it.
  - is there ANY rod where the posture frame genuinely pays? x01 said no on one plant; this asks at breadth.

A REACHABILITY PRE-PASS RUNS FIRST - one call per rod. Burning a 1000-call sweep on unverified model ids is
the D13 lesson (verify the test rig, not just the code); unreachable rods are recorded and skipped, never
silently dropped.

Run: python -m aea.lab.x10_coverage_sweep          (add --dry to print the matrix and exit)
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import re
import sys
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.mind import fuel

N = 8
MAXTOK = 320
TEMPS = (0.0, 0.2, 0.7, 1.0)
GAME_TEMP = 0.2

WORDS = "the mouth draws power through the ladder and the measure closes the wire"      # 13 words
WANT = "13"
BASE = "Count the words in the sentence below and reply with ONLY the number.\n" + WORDS

# Quoted verbatim from aea/lab/experiments/x02_fitted_frame.py and bench_core.SCAFFOLDS, so the sweep
# extends the measured artefacts rather than paraphrases of them.
POSTURE = "You are on the bench. Answer exactly and only what is asked.\n"
FITTED = ("To count words: split the sentence on spaces, number each token 1,2,3..., then report the "
          "FINAL index. Show the numbered list, then the count alone on the last line.")

FRAMINGS = (("bare", BASE),
            ("posture", POSTURE + BASE),
            ("fitted", FITTED + "\n\n" + BASE))

# STRATIFIED BY SIZE AND BY PLANT. Five tiers x four plants, chosen from state/capability_census.json so
# every entry is a rod the census already saw answer. (plant, model, size_tier)
RODS = [
    ("nvidia", "meta/llama-3.2-1b-instruct",              "nano"),
    ("nvidia", "meta/llama-3.2-3b-instruct",              "micro"),
    ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2",       "normal"),
    ("nvidia", "openai/gpt-oss-20b",                      "normal"),
    ("nvidia", "mistralai/mistral-small-4-119b-2603",     "large"),   # census top score, 12
    ("nvidia", "nvidia/nemotron-3-super-120b-a12b",       "large"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b",       "large"),
    ("groq",   "llama-3.1-8b-instant",                    "normal"),
    ("groq",   "llama-3.3-70b-versatile",                 "large"),
    ("ollama", "granite4.1:8b",                           "normal"),  # census 10, and x09's converter
    ("ollama", "llama3.1:8b",                             "normal"),  # x09's FRAME+READOUT case
    ("pollinations", "openai-fast",                       "micro"),   # census 11, keyless - a 4th plant
]


def check(text: str) -> bool:
    nums = re.findall(r"-?\d+", (text or "").replace(",", ""))
    return bool(nums) and nums[-1] == WANT


def readout(text: str):
    """THE READOUT (candidate C-87, L1): the answer read out of the WORK. Zero tokens, zero latency."""
    idx = [int(m.group(1)) for m in re.finditer(r"(?m)^\s*(\d{1,2})\.\s+\S", text or "")]
    return max(idx) if idx else None


def _one(rod, prompt, temp, i):
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": prompt}],
                     max_tokens=MAXTOK, temperature=temp)
    if not r.get("ok"):
        return {"trial": i, "ok": False, "error": (r.get("error") or "")[:120]}
    text = r.get("text") or ""
    w = readout(text)
    return {"trial": i, "ok": True, "pass": check(text), "from_work": w,
            "pass_with_readout": bool(check(text) or (w is not None and str(w) == WANT)),
            "enumerated": w is not None, "raw": text[-320:],
            "tok_in": r.get("prompt_tokens") or 0, "tok_out": r.get("tokens") or 0,
            "cut": (r.get("tokens") or 0) >= MAXTOK - 2}


def reach(rod) -> dict:
    """One call. Records who answers, so the sweep never spends on an id that does not serve."""
    t0 = time.time()
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": "Reply with only: OK"}],
                     max_tokens=16, temperature=0.0, tries=2)
    return {"rod": "%s/%s" % rod[:2], "size": rod[2], "ok": bool(r.get("ok")),
            "latency_s": round(time.time() - t0, 2), "error": (r.get("error") or "")[:140] or None}


def cell(rod, fname, prompt, temp):
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        trials = [f.result() for f in [pool.submit(_one, rod, prompt, temp, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [t for t in trials if t["ok"]]
    # DISTINCT IS THE HONEST n (D15). Identical replies are one measurement repeated, never eight.
    distinct = len({t["raw"] for t in ok})
    row = {"rod": "%s/%s" % rod[:2], "size": rod[2], "framing": fname, "temperature": temp,
           "passes": sum(1 for t in ok if t["pass"]), "scored": len(ok),
           "passes_with_readout": sum(1 for t in ok if t["pass_with_readout"]),
           "enumerated": sum(1 for t in ok if t["enumerated"]),
           "distinct_replies": distinct, "effective_n": distinct,
           "cuts": sum(1 for t in ok if t["cut"]),
           "tok_in": sum(t["tok_in"] for t in ok), "tok_out": sum(t["tok_out"] for t in ok),
           "errors": [t.get("error") for t in trials if not t["ok"]][:2],
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=temp,
                              attempts=len(trials), failures=len(trials) - len(ok)),
           "trials": trials}
    print("    %-46s %-8s t=%.1f  %d/%-2d  +ro %d/%-2d  distinct=%d"
          % (row["rod"][:45], fname, temp, row["passes"], row["scored"],
             row["passes_with_readout"], row["scored"], distinct), flush=True)
    return row


def run(dry: bool = False):
    print("x10 - %d rods x %d framings x %d temps x n=%d  (the game fires at %.1f)"
          % (len(RODS), len(FRAMINGS), len(TEMPS), N, GAME_TEMP))
    print("     max calls if all reachable: %d" % (len(RODS) * len(FRAMINGS) * len(TEMPS) * N))
    if dry:
        for r in RODS:
            print("   %-8s %-46s %s" % (r[0], r[1], r[2]))
        return None

    print("\nREACHABILITY (one call per rod)")
    pool = _futures.ThreadPoolExecutor(max_workers=6)
    try:
        reach_rows = [f.result() for f in [pool.submit(reach, r) for r in RODS]]
    finally:
        pool.shutdown(wait=True)
    for rr in reach_rows:
        print("   %-52s %-6s %5.2fs %s" % (rr["rod"][:51], "OK" if rr["ok"] else "DEAD",
                                           rr["latency_s"], rr["error"] or ""))
    live = [r for r in RODS if next(x for x in reach_rows if x["rod"] == "%s/%s" % r[:2])["ok"]]
    print("   -> %d of %d reachable" % (len(live), len(RODS)))

    rows = []
    for temp in TEMPS:
        print("\n  TEMPERATURE %.1f%s" % (temp, "   (the product's own)" if temp == GAME_TEMP else ""))
        for rod in live:
            for fname, prompt in FRAMINGS:
                rows.append(cell(rod, fname, prompt, temp))

    rep = {"id": "x10_coverage_sweep",
           "question": "does THE FRAME's and THE READOUT's benefit hold across size, plant and "
                       "temperature - and where does determinism break?",
           "measures": ["C-04", "C-19", "C-23", "C-16", "C-87"], "n": N,
           "temperatures": list(TEMPS), "game_temperature": GAME_TEMP,
           "task": "wordcount-13", "framings": [f[0] for f in FRAMINGS],
           "reachability": reach_rows, "rows": rows,
           "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
    rep["analysis"] = analyse(rows)

    d = os.path.join(grid.STATE, "lab", "runs", "x10_coverage_sweep")
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
                                       "check_id": "last-number-is-13", "n": N,
                                       "rods": ["%s/%s" % r[:2] for r in live],
                                       "measures": rep["measures"], "verdicts": [],
                                       "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


def analyse(rows: list) -> dict:
    """Every claim is read at the product's temperature; the other temps answer the determinism question."""
    def get(rod, fname, temp, key="passes"):
        r = next((x for x in rows if x["rod"] == rod and x["framing"] == fname
                  and x["temperature"] == temp), None)
        return (r[key] / r["scored"]) if r and r["scored"] else None

    rods = sorted({r["rod"] for r in rows})
    size = {r["rod"]: r["size"] for r in rows}
    per_rod = {}
    for rod in rods:
        bare = get(rod, "bare", GAME_TEMP)
        post = get(rod, "posture", GAME_TEMP)
        fit = get(rod, "fitted", GAME_TEMP)
        fit_ro = get(rod, "fitted", GAME_TEMP, "passes_with_readout")
        bare_ro = get(rod, "bare", GAME_TEMP, "passes_with_readout")
        enum = get(rod, "fitted", GAME_TEMP, "enumerated")
        d = "-"
        if bare is None:
            d = "unmeasured"
        elif bare >= 0.9:
            d = "needs nothing - passes bare"
        elif fit is not None and fit >= 0.9:
            d = "THE FRAME alone"
        elif None not in (fit, fit_ro) and fit_ro - fit >= 0.25:
            d = "THE FRAME and THE READOUT (jointly necessary)"
        elif None not in (bare, bare_ro) and bare_ro - bare >= 0.25:
            d = "THE READOUT alone"
        elif enum is not None and enum < 0.5:
            d = "the frame does not take - the named method is ignored"
        else:
            d = "no free lever measured here converts it"
        per_rod[rod] = {"size": size[rod], "bare": bare, "posture": post, "fitted": fit,
                        "fitted_plus_readout": fit_ro, "bare_plus_readout": bare_ro,
                        "enumerated": enum, "diagnosis": d}

    # THE PRECONDITION BOUNDARY, mapped by size rather than asserted. x02's claim was that a frame cannot
    # rescue a capability that was never missing; this shows where "missing" stops.
    by_size = {}
    for tier in ("nano", "micro", "normal", "large"):
        v = [p for p in per_rod.values() if p["size"] == tier and p["bare"] is not None]
        if v:
            by_size[tier] = {"rods": len(v),
                             "bare_mean": round(sum(p["bare"] for p in v) / len(v), 3),
                             "fitted_mean": round(sum(p["fitted"] for p in v
                                                      if p["fitted"] is not None) / len(v), 3),
                             "frame_pays_on": sum(1 for p in v if p["fitted"] is not None
                                                  and p["fitted"] - p["bare"] >= 0.25),
                             "readout_pays_on": sum(1 for p in v
                                                    if p["fitted_plus_readout"] is not None
                                                    and p["fitted"] is not None
                                                    and p["fitted_plus_readout"] - p["fitted"] >= 0.25)}

    # DETERMINISM, per plant per temperature - the fix for D15 rather than a note about it.
    det = {}
    for t in sorted({r["temperature"] for r in rows}):
        for plant in sorted({r["rod"].split("/")[0] for r in rows}):
            c = [r for r in rows if r["temperature"] == t and r["rod"].startswith(plant + "/")
                 and r["scored"]]
            if c:
                det["t=%.1f %s" % (t, plant)] = {
                    "cells": len(c),
                    "collapsed": sum(1 for r in c if r["distinct_replies"] <= 1),
                    "median_effective_n": sorted(r["effective_n"] for r in c)[len(c) // 2]}

    posture_pays = [r for r in rods if None not in (per_rod[r]["bare"], per_rod[r]["posture"])
                    and per_rod[r]["posture"] - per_rod[r]["bare"] >= 0.25]
    readout_pays = [r for r in rods if per_rod[r]["diagnosis"].startswith("THE READOUT")
                    or "READOUT" in per_rod[r]["diagnosis"]]
    return {"per_rod": per_rod, "by_size": by_size, "determinism": det,
            "posture_pays_on": posture_pays, "readout_pays_on": readout_pays}


if __name__ == "__main__":
    r = run(dry="--dry" in sys.argv)
    if not r:
        sys.exit(0)
    a = r["analysis"]
    print()
    print("DIAGNOSIS PER ROD (read at the product's temperature %.1f)" % r["game_temperature"])
    for rod, v in a["per_rod"].items():
        print("  %-46s %-7s bare %-5s fitted %-5s +ro %-5s  %s"
              % (rod[:45], v["size"],
                 "-" if v["bare"] is None else "%.2f" % v["bare"],
                 "-" if v["fitted"] is None else "%.2f" % v["fitted"],
                 "-" if v["fitted_plus_readout"] is None else "%.2f" % v["fitted_plus_readout"],
                 v["diagnosis"]))
    print()
    print("THE PRECONDITION BOUNDARY, BY SIZE")
    for tier, v in a["by_size"].items():
        print("  %-7s rods=%d  bare %.2f -> fitted %.2f   frame pays on %d, readout pays on %d"
              % (tier, v["rods"], v["bare_mean"], v["fitted_mean"], v["frame_pays_on"],
                 v["readout_pays_on"]))
    print()
    print("DETERMINISM - where n stops being real")
    for k, v in a["determinism"].items():
        print("  %-18s %d of %d cells collapsed to one reply   median effective n = %s"
              % (k, v["collapsed"], v["cells"], v["median_effective_n"]))
    print()
    print("POSTURE frame pays on: %s" % (", ".join(a["posture_pays_on"]) or "NO ROD"))
    print("READOUT pays on:       %s" % (", ".join(a["readout_pays_on"]) or "NO ROD"))
    print("EVIDENCE  state/lab/runs/x10_coverage_sweep/%s.json" % r["run_id"])
