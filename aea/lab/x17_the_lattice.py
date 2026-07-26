"""x17 - THE ORDERING LATTICE. Deriving the dependency graph instead of reasoning it.

Every order this walk has used was REASONED. The census placed 86 items by asking what forces what, the
book inherited that, and every anomaly since has been the same shape: an edge the ladder could not carry.

  the readout arrived BEFORE its material          (inert at L1, live at L2)
  the scorer added knowing rather than accuracy    (0.38 -> 0.35, can-know 0.00 -> 1.00)
  latency required nothing and was worth nothing   (two different edges, one word)
  validation cost 18 points when added IN ORDER    (a conflict, not a dependency)
  the frame worked without the two rungs below it  (0.65 with neither)

A line has ONE relation available. The structure has at least four. So this experiment stops asking
"what is the right order" and measures the graph directly.

THE METHOD. For each component X and each subset S of the others, compare S against S+X on the same
task and the same pinned fuel. That single comparison, repeated across the lattice, yields every edge:

  MARGIN(X | S) = correct(S + X) - correct(S)

  X REQUIRES Y      X is void without Y and works with it
  X DEPENDS ON Y    margin(X | S) is worth having only when Y is in S
  X ALTERNATIVE Y   each is worth having alone, and having both adds nothing over either
  X CONFLICTS Y     margin(X | S) is NEGATIVE when Y is in S
  X INERT           margin is inside the noise band everywhere
  X FREE            margin is positive and does not vary with S

THE NOISE BAND IS 0.10, and it was not chosen. x16 ran the identical assembly `call+frame` twice under
two labels and scored 0.70 and 0.60, so anything smaller than that spread is not a finding.

SCOPE. `call` is in every assembly because nothing runs without it. That leaves six components and 64
subsets; at n=8 on 2 tasks and 2 rods this is 2048 calls with the full lattice, so the run measures the
LOWER LATTICE exhaustively (all subsets of the four components that actually move the number) and probes
the rest at the margins. Every cell is written as it completes and the run resumes.

Run: python -m aea.lab.x17_the_lattice
"""
from __future__ import annotations

import concurrent.futures as _futures
import itertools

from aea.lab import overseer as OV
from aea.lab.organism import Organism, classify
from aea.lab.x16_the_organisms import TASKS
from aea.mind import fuel

N = 8
TEMP = 0.2
BAND = 0.10          # measured, not chosen: x16 scored the same assembly 0.70 and 0.60

# The four that moved the number in x16, plus the two that did not. The lattice is exhaustive over the
# first four and probes the last two, because a component that is inert everywhere needs fewer cells to
# establish than one that interacts.
CORE = ["goal", "frame", "readout", "validation"]
PROBE = ["measure", "latency"]

RODS = [
    ("ollama", "granite4.1:3b"),                        # needs the frame: 0.00 bare
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),    # does not: 0.93 bare
]


def subsets(items):
    for r in range(len(items) + 1):
        for c in itertools.combinations(items, r):
            yield list(c)


def cell(led, keys, rod, task_id):
    org = Organism(["call"] + keys, rod, label="+".join(keys) or "call only")
    t = TASKS[task_id]
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        recs = [f.result() for f in [pool.submit(org.run, t, temperature=TEMP) for _ in range(N)]]
    finally:
        pool.shutdown(wait=True)
    clean = [r for r in recs if r["ok"] and not r["flags"]]
    for r in recs:
        led.note_flags(r["flags"])
    row = {"subset": sorted(keys), "key": "|".join(sorted(keys)), "rod": "%s/%s" % rod,
           "task": task_id, "clean": len(clean), "ran": len(recs),
           "correct": sum(1 for r in clean if r["answer"] == t["truth"]),
           "answered": sum(1 for r in clean if r["answer"] is not None),
           "declined": sum(1 for r in clean if r["read_by"] == "declined"),
           "read_by_work": sum(1 for r in clean if r["read_by"] == "work"),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                              attempts=len(recs), failures=len(recs) - len(clean)),
           "records": recs}
    led.add(row)
    print("    %-34s %-22s %-11s correct %d/%-2d  declined %d"
          % (row["key"] or "(call only)", rod[1].rsplit("/", 1)[-1][:21], task_id,
             row["correct"], row["clean"], row["declined"]), flush=True)
    return row


def run():
    led = OV.Ledger("x17_the_lattice", {
        "what": "marginal contribution of each component against every subset",
        "band": BAND, "band_source": "x16 ran the identical assembly twice: 0.70 and 0.60",
        "core": CORE, "probe": PROBE, "n": N, "temperature": TEMP,
        "rods": ["%s/%s" % r for r in RODS], "tasks": list(TASKS)})
    plan = [s for s in subsets(CORE)]
    for p in PROBE:                       # probe: the empty set and the full core, with and without
        plan += [[p], CORE + [p]]
    seen, uniq = set(), []
    for s in plan:
        k = "|".join(sorted(s))
        if k not in seen:
            seen.add(k)
            uniq.append(s)
    print("x17 - %d subsets x %d rods x %d tasks x n=%d = %d calls\n"
          % (len(uniq), len(RODS), len(TASKS), N, len(uniq) * len(RODS) * len(TASKS) * N), flush=True)
    for s in uniq:
        print("  [%s]" % ("+".join(sorted(s)) or "call only"), flush=True)
        for rod in RODS:
            for task_id in TASKS:
                if led.has(key="|".join(sorted(s)), rod="%s/%s" % rod, task=task_id):
                    continue
                cell(led, s, rod, task_id)

    rows = led.doc["rows"]

    def score(keyset, rod=None):
        k = "|".join(sorted(keyset))
        sel = [r for r in rows if r["key"] == k and (rod is None or r["rod"] == rod)]
        tot = sum(r["clean"] for r in sel)
        return (sum(r["correct"] for r in sel) / tot) if tot else None

    # THE MARGINS. margin(X | S) for every component and every subset that lacks it.
    margins = {}
    for x in CORE + PROBE:
        for s in subsets(CORE):
            if x in s:
                continue
            base, plus = score(s), score(sorted(set(s) | {x}))
            if None in (base, plus):
                continue
            margins.setdefault(x, []).append({"given": sorted(s), "base": round(base, 3),
                                              "with": round(plus, 3), "margin": round(plus - base, 3)})

    # THE EDGES, read off the margins rather than declared
    edges = {}
    for x, ms in margins.items():
        pos = [m for m in ms if m["margin"] >= BAND]
        neg = [m for m in ms if m["margin"] <= -BAND]
        edges[x] = {
            "n": len(ms),
            "helps_in": len(pos), "harms_in": len(neg),
            "alone": next((m["margin"] for m in ms if not m["given"]), None),
            "conflicts_with": sorted({y for m in neg for y in m["given"]}),
            "depends_on": sorted({y for m in pos for y in m["given"]}) if pos and not any(
                not m["given"] for m in pos) else [],
            "verdict": ("inert" if not pos and not neg else
                        ("free" if len(pos) == len(ms) else
                         ("conditional" if pos and neg else
                          ("harmful" if neg and not pos else "conditional")))),
            "margins": ms}

    led.done(margins=margins, edges=edges)
    return led.doc


if __name__ == "__main__":
    d = run()
    print("\nTHE EDGES, derived from %d subset comparisons\n" % sum(e["n"] for e in d["edges"].values()))
    print("%-12s %-9s %6s %6s %8s %-22s %s" % ("component", "verdict", "helps", "harms", "alone",
                                               "conflicts with", "depends on"))
    for x, e in d["edges"].items():
        print("%-12s %-9s %5d/%-2d %5d %8s %-22s %s"
              % (x, e["verdict"], e["helps_in"], e["n"], e["harms_in"],
                 ("%+.2f" % e["alone"]) if e["alone"] is not None else "  -  ",
                 ",".join(e["conflicts_with"]) or "-", ",".join(e["depends_on"]) or "-"))
    print("\nnoise band %.2f, measured (x16 ran one assembly twice: 0.70 and 0.60)" % d["band"])
    print("overseer:", d["overseer"])
    print("\nEVIDENCE  state/lab/runs/x17_the_lattice/%s.json" % d["run_id"])
