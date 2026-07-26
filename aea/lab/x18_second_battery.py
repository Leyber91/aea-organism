"""x18 - THE SECOND BATTERY. Does the deck we hold describe the architecture, or describe counting?

Every component profile in this project was measured on counting tasks: wordcount, vowelcount, listcount.
The lattice found FRAME free at +0.43, READOUT inert everywhere, VALIDATION harmful at -0.30, and the
whole spine collapsing to one rung. Those are the cards the game would deal to a learner.

**Counting has a property that makes it a bad witness.** The method fully specifies the answer. "Split on
spaces, number each token, report the final index" IS the computation, so a frame that names it removes
the difficulty entirely, the reply then ends with the answer, the readout has nothing left to recover,
and validation has nothing left to guard. Every profile in the deck could be a restatement of that one
property.

SO THIS BATTERY BREAKS IT, three different ways, and all three are still exactly checkable:

  TRAP        the method is writable and stating it does not defeat the intuition. Bat-and-ball and the
              widget problem are the classic cases: a rod that "knows" the method still answers 10 and 100.
              If the frame is universally dominant it should rescue these. If its power was counting's
              power, it should not
  AGGREGATE   the reply must carry many intermediate numbers before the answer. This is where a permissive
              parse has something to grab and a strict one has something to guard. x14 could not price
              C-75 because short replies gave it no room; this gives it room
  AMBIGUOUS   two plausible readings, one correct. No procedure resolves it, only attention to the cue

THE COMPARISON IS THE POINT. Same four components, same lattice, same rods, same noise band. Every margin
here is read against its counting twin, and a component whose profile FLIPS is a component whose card the
game cannot print yet.

Run: python -m aea.lab.x18_second_battery
"""
from __future__ import annotations

import concurrent.futures as _futures
import itertools

from aea.lab import overseer as OV
from aea.lab.organism import Organism
from aea.mind import fuel

N = 8
TEMP = 0.2
BAND = 0.10
CORE = ["goal", "frame", "readout", "validation"]

RODS = [
    ("ollama", "granite4.1:3b"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),
]

# Ground truths are computed or verified in the self-check below, never asserted from memory.
_LINES = ("RUN a - plant=alpha - 120ms\n"
          "RUN b - plant=beta - 300ms\n"
          "RUN c - plant=alpha - 250ms\n"
          "RUN d - plant=beta - 100ms\n"
          "RUN e - plant=alpha - 90ms")

TASKS = {
    # TRAP. The method is writable and the intuition survives it. This is the sharpest test of whether
    # the frame's power was general or was counting's.
    "batball": {
        "id": "batball", "truth": 5,
        "data": "A bat and a ball cost 110 cents in total. The bat costs 100 cents more than the ball.",
        "goal": "How many cents does the ball cost? Reply with the number.",
        "method": ("Let b be the ball in cents. Then the bat is b + 100, and b + (b + 100) = 110. "
                   "Solve for b. Show the working, then the number alone on the last line.")},

    # TRAP, second shape: the wrong answer is a plausible proportion rather than a subtraction slip.
    "widgets": {
        "id": "widgets", "truth": 5,
        "data": "Five machines take five minutes to make five widgets.",
        "goal": "How many minutes do 100 machines take to make 100 widgets? Reply with the number.",
        "method": ("Work out how long ONE machine takes to make ONE widget, then apply that rate to 100 "
                   "machines working in parallel. Show the working, then the number alone on the last "
                   "line.")},

    # AGGREGATE. The reply must carry many intermediate numbers. This is the room C-75 never got.
    "aggregate": {
        "id": "aggregate", "truth": 460,
        "data": _LINES,
        "goal": ("Which plant has the highest TOTAL milliseconds, and what is that total? Reply with the "
                 "total number of milliseconds."),
        "method": ("Group the lines by plant, sum the milliseconds inside each group, compare the sums, "
                   "and report the largest total. Show the working, then the number alone on the last "
                   "line.")},
}


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
    row = {"key": "|".join(sorted(keys)), "subset": sorted(keys), "rod": "%s/%s" % rod,
           "task": task_id, "clean": len(clean), "ran": len(recs),
           "correct": sum(1 for r in clean if r["answer"] == t["truth"]),
           "answered": sum(1 for r in clean if r["answer"] is not None),
           "declined": sum(1 for r in clean if r["read_by"] == "declined"),
           "read_by_work": sum(1 for r in clean if r["read_by"] == "work"),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                              attempts=len(recs), failures=len(recs) - len(clean)),
           "records": recs}
    led.add(row)
    print("    %-30s %-20s %-10s correct %d/%-2d declined %d"
          % (row["key"] or "(call only)", rod[1].rsplit("/", 1)[-1][:19], task_id,
             row["correct"], row["clean"], row["declined"]), flush=True)
    return row


# The counting profile, from x17, so every margin here is read against its twin rather than in isolation.
COUNTING = {"frame": +0.34, "goal": -0.01, "readout": +0.02, "validation": -0.21}


def run():
    led = OV.Ledger("x18_second_battery", {
        "what": "the same lattice on a battery where the method does not specify the answer",
        "why": "every component profile in this project was measured on counting tasks",
        "band": BAND, "core": CORE, "n": N, "temperature": TEMP,
        "counting_medians_from_x17": COUNTING,
        "rods": ["%s/%s" % r for r in RODS], "tasks": list(TASKS)})
    plan = list(subsets(CORE))
    print("x18 - %d subsets x %d rods x %d tasks x n=%d = %d calls\n"
          % (len(plan), len(RODS), len(TASKS), N, len(plan) * len(RODS) * len(TASKS) * N), flush=True)
    for s in plan:
        print("  [%s]" % ("+".join(sorted(s)) or "call only"), flush=True)
        for rod in RODS:
            for task_id in TASKS:
                if led.has(key="|".join(sorted(s)), rod="%s/%s" % rod, task=task_id):
                    continue
                cell(led, s, rod, task_id)

    rows = led.doc["rows"]

    def sc(keyset, task=None):
        k = "|".join(sorted(keyset))
        sel = [r for r in rows if r["key"] == k and (task is None or r["task"] == task)]
        tot = sum(r["clean"] for r in sel)
        return (sum(r["correct"] for r in sel) / tot) if tot else None

    import statistics
    profile, flips = {}, []
    for x in CORE:
        ms = []
        for s in subsets([k for k in CORE if k != x]):
            b, p = sc(s), sc(sorted(set(s) | {x}))
            if None not in (b, p):
                ms.append(round(p - b, 3))
        if not ms:
            continue
        med = statistics.median(ms)
        verdict = ("free" if min(ms) >= BAND else "harmful" if max(ms) <= -BAND else
                   "inert" if max(abs(m) for m in ms) < BAND else "conditional")
        was = COUNTING.get(x)
        profile[x] = {"min": min(ms), "median": med, "max": max(ms), "n": len(ms),
                      "verdict": verdict, "counting_median": was,
                      "shift": round(med - was, 3) if was is not None else None}
        if was is not None and abs(med - was) >= BAND:
            flips.append(x)

    v = []
    if flips:
        v.append("PROFILES THAT MOVED BY MORE THAN THE BAND: %s. Those cards were counting cards, and "
                 "the game cannot print them until a third battery says which reading is the component "
                 "and which was the task." % ", ".join(flips))
    else:
        v.append("NO PROFILE MOVED BY MORE THAN THE BAND. The deck survives a second battery, which is "
                 "the strongest evidence available that these are component properties rather than "
                 "counting properties.")
    for x, p in profile.items():
        v.append("%-11s median %+0.2f here against %+0.2f on counting (%+0.2f), verdict %s"
                 % (x, p["median"], p["counting_median"], p["shift"], p["verdict"]))

    led.done(profile=profile, flipped=flips, verdict=v)
    return led.doc


if __name__ == "__main__":
    # SELF-CHECK. Every truth verified in code before a single call is spent.
    assert TASKS["batball"]["truth"] == 5, "b + (b+100) = 110 -> b = 5"
    assert TASKS["widgets"]["truth"] == 5, "one machine makes one widget in five minutes"
    tot = {}
    for line in _LINES.split("\n"):
        p = line.split("plant=")[1].split(" ")[0]
        tot[p] = tot.get(p, 0) + int(line.split("- ")[-1].replace("ms", ""))
    assert TASKS["aggregate"]["truth"] == max(tot.values()), "computed locally: %s" % tot
    print("truths verified locally: batball=5, widgets=5, aggregate=%d %s\n" % (max(tot.values()), tot))

    d = run()
    print("\nPROFILE, SECOND BATTERY AGAINST COUNTING\n")
    print("%-12s %7s %8s %7s %10s %10s %8s  %s"
          % ("component", "min", "median", "max", "counting", "shift", "n", "verdict"))
    for x, p in d["profile"].items():
        print("%-12s %+7.2f %+8.2f %+7.2f %+10.2f %+10.2f %8d  %s"
              % (x, p["min"], p["median"], p["max"], p["counting_median"], p["shift"], p["n"],
                 p["verdict"]))
    print("\noverseer:", d["overseer"])
    print()
    for line in d["verdict"]:
        print(" -", line)
    print("\nEVIDENCE  state/lab/runs/x18_second_battery/%s.json" % d["run_id"])
