"""x22 - THE CAPACITY LADDER. What does each part ENABLE, as the seat grows?

THE CORRECTION THIS RUN IS BUILT ON. Nine parts of four different kinds were scored against ONE
outcome - accuracy - and every null was read as a verdict. That produced "World 2 has five components
and not one improves an answer", which is rhetorically strong and analytically false: three of those
five were never accuracy instruments.

A part does not add ACCURACY. It adds a CAPACITY. The ladder is not performance, it is what becomes
possible, and the capacities are not commensurable with each other:

  v1  call        an answer exists at all                       answered
  v2  +goal       it addresses what was asked                   on_task
  v3  +frame      the reply SHOWS ITS WORKING                   shows_working
  v4  +readout    an answer is recoverable FROM the working     recoverable
  v5  +validation refusal becomes visible instead of a guess    can_abstain
  v6  +critic     the answer can be re-decided                  revised
  v7  +carry      state survives to the next call               held
  v8  +measure    whether it worked becomes knowable            can_know
  v9  +latency    wrongness is legible with no words            (population-level)

They may not be hierarchical. That is the point of measuring rather than asserting: this run reports
what each rung ENABLES and does not assume the ladder is a ladder.

THE TASK is the calibrated retention chain. Trivial arithmetic on a five-digit value, so holding the
number is the work and the sum is not. Calibration: `none` first-misses at step 2 with 1/14 hits,
`checkpoint` at step 5 with 4/14. Final-answer correctness is 0.00 for every arm at this difficulty
and discriminates nothing, so the accuracy column is DRIFT POINT and steps-hit.

Run: python -m aea.lab.x22_the_capacity_ladder
"""
from __future__ import annotations

import concurrent.futures as _futures
import statistics

from aea.lab import overseer as OV
from aea.lab.organism import Chain
from aea.lab.parts.read import read_work
from aea.mind import fuel

N = 3
TEMP = 0.2
BAND = 0.10
START = 48371
OPS = ["add 6", "subtract 13", "add 21", "subtract 8", "add 17", "subtract 24", "add 9",
       "subtract 31", "add 14", "subtract 7", "add 26", "subtract 19", "add 11", "subtract 5"]

SERIES = [
    ("v1", ["call"], "none", "answered"),
    ("v2", ["call", "goal"], "none", "on_task"),
    ("v3", ["call", "goal", "frame"], "none", "shows_working"),
    ("v4", ["call", "goal", "frame", "readout"], "none", "recoverable"),
    ("v5", ["call", "goal", "frame", "readout", "validation"], "none", "can_abstain"),
    ("v6", ["call", "goal", "frame", "readout", "validation", "critic"], "none", "revised"),
    ("v7", ["call", "goal", "frame", "readout", "validation", "critic"], "checkpoint", "held"),
    ("v8", ["call", "goal", "frame", "readout", "validation", "critic", "measure"], "checkpoint",
     "can_know"),
]

RODS = [
    ("ollama", "granite4.1:3b"),
    ("groq", "llama-3.1-8b-instant"),
]


def truth_at(n):
    v = START
    for op in OPS[:n]:
        k = int(op.split()[-1])
        v = v + k if op.startswith("add") else v - k
    return v


def capacities(rec):
    """What this sequence DEMONSTRATED, read off the per-step trace. Each is a rate, not a score."""
    t = [s for s in rec["trace"] if s.get("ok")]
    if not t:
        return {}
    steps = len(t)
    return {
        # an answer exists at all
        "answered": sum(1 for s in t if s.get("value") is not None) / steps,
        # it APPLIED the operation rather than handing back what it was given
        "on_task": sum(1 for s in t if s.get("on_task")) / steps,
        # visible working, in any of the three dialects the readout speaks
        "shows_working": sum(1 for s in t if s.get("showed_work")) / steps,
        # the answer was taken OUT of the working rather than off the end
        "recoverable": sum(1 for s in t if s.get("from_work")) / steps,
        # a refusal, rather than a guess
        "can_abstain": sum(1 for s in t if s.get("declined")) / steps,
        # a second look moved it
        "revised": sum(1 for s in t if s.get("repaired")) / steps,
        # state survived into the next step
        "held": sum(1 for s in t if s.get("hit")) / steps,
    }


def cell(led, ver, seat, form, adds, rod):
    pool = _futures.ThreadPoolExecutor(max_workers=3)
    try:
        recs = [f.result() for f in
                [pool.submit(Chain(rod, form=form, seat=seat, start=START,
                                   temperature=TEMP).run, OPS, truth_at) for _ in range(N)]]
    finally:
        pool.shutdown(wait=True)
    done = [r for r in recs if r["completed"]]
    for r in recs:
        led.note_flags(r["flags"])
    caps = {}
    for r in done:
        for k, v in capacities(r).items():
            caps.setdefault(k, []).append(v)
    caps = {k: round(statistics.mean(v), 3) for k, v in caps.items()}
    misses = [r["first_miss"] for r in done if r["first_miss"]]
    row = {"version": ver, "seat": seat, "form": form, "adds": adds, "rod": "%s/%s" % rod,
           "ran": len(recs), "completed": len(done),
           "correct": sum(1 for r in done if r["correct"]),
           "hits": sum(r["hits"] for r in done), "of": sum(r["completed"] for r in done),
           "median_first_miss": statistics.median(misses) if misses else None,
           "capacities": caps,
           "tok_total": sum(r["tok_total"] for r in done),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                              attempts=len(recs), failures=len(recs) - len(done)),
           "records": recs}
    led.add(row)
    print("    %-4s %-46s %-22s drift@%-5s hit %2d/%-3d  %s"
          % (ver, "+".join(seat) + ("+carry" if form != "none" else ""),
             rod[1].rsplit("/", 1)[-1][:21], row["median_first_miss"], row["hits"], row["of"],
             " ".join("%s=%.2f" % (k[:4], v) for k, v in sorted(caps.items()) if v)), flush=True)
    return row


def run():
    led = OV.Ledger("x22_the_capacity_ladder", {
        "what": "what each part ENABLES as the seat grows, not what it adds to accuracy",
        "why": "nine parts of four kinds were scored on one metric and every null read as a verdict",
        "task": "the calibrated retention chain: trivial arithmetic on a five-digit value",
        "calibration": "none first-misses at step 2 with 1/14; checkpoint at step 5 with 4/14",
        "note": "final-answer correctness is 0.00 for every arm at this difficulty. The accuracy "
                "column is DRIFT POINT and steps-hit.",
        "hierarchy_note": "the rungs may not be hierarchical. This run reports what each ENABLES and "
                          "does not assume the ladder is a ladder.",
        "series": [(v, s, f, a) for v, s, f, a in SERIES],
        "n": N, "temperature": TEMP, "band": BAND, "start": START, "steps": len(OPS),
        "rods": ["%s/%s" % r for r in RODS]})
    print("x22 - %d versions x %d rods x n=%d x %d steps = %d calls\n"
          % (len(SERIES), len(RODS), N, len(OPS), len(SERIES) * len(RODS) * N * len(OPS)), flush=True)
    for ver, seat, form, adds in SERIES:
        print("  [%s adds %s]" % (ver, adds), flush=True)
        for rod in RODS:
            if led.has(version=ver, rod="%s/%s" % rod):
                continue
            cell(led, ver, seat, form, adds, rod)

    rows = led.doc["rows"]
    ladder, prev = [], {}
    for ver, seat, form, adds in SERIES:
        sel = [r for r in rows if r["version"] == ver]
        if not sel:
            continue
        caps = {}
        for r in sel:
            for k, v in r["capacities"].items():
                caps.setdefault(k, []).append(v)
        caps = {k: round(statistics.mean(v), 3) for k, v in caps.items()}
        gained = {k: round(v - prev.get(k, 0.0), 3) for k, v in caps.items()
                  if v - prev.get(k, 0.0) >= BAND}
        lost = {k: round(v - prev.get(k, 0.0), 3) for k, v in caps.items()
                if v - prev.get(k, 0.0) <= -BAND}
        misses = [r["median_first_miss"] for r in sel if r["median_first_miss"]]
        ladder.append({"version": ver, "adds": adds, "seat": seat, "form": form,
                       "capacities": caps, "gained": gained, "lost": lost,
                       "claimed": adds, "delivered": adds in gained,
                       "drift": statistics.median(misses) if misses else None,
                       "hits": sum(r["hits"] for r in sel), "of": sum(r["of"] for r in sel)})
        prev = caps

    v = []
    # THE ADDITION LAW leads the verdict: a module must not subtract when it is added. A rung that
    # gains its own capacity while destroying another has failed, whatever its own number did.
    breaches = [x for x in ladder if x["lost"]]
    if breaches:
        v.append("THE ADDITION LAW IS BREACHED BY %d OF %d RUNGS. A component must not subtract "
                 "functionality when added." % (len(breaches), len(ladder)))
        for x in breaches:
            v.append("  %-3s +%-12s SUBTRACTED %s"
                     % (x["version"], x["adds"],
                        ", ".join("%s %+0.2f" % (k, val) for k, val in x["lost"].items())))
    else:
        v.append("THE ADDITION LAW HOLDS ON EVERY RUNG: no capacity dropped by more than the band "
                 "anywhere on the ladder.")
    kept = [x for x in ladder if x["delivered"]]
    v.append("PARTS THAT DELIVERED THE CAPACITY THEY CLAIM: %d of %d." % (len(kept), len(ladder)))
    for x in ladder:
        v.append("  %-3s adds %-14s %s%s"
                 % (x["version"], x["adds"],
                    "DELIVERED" if x["delivered"] else "not delivered",
                    ("  also gained %s" % x["gained"]) if x["gained"] else ""))
        if x["lost"]:
            v.append("      AND COST: %s" % x["lost"])
    drifts = [(x["version"], x["drift"]) for x in ladder if x["drift"]]
    v.append("DRIFT POINT along the ladder: " + ", ".join("%s@%s" % d for d in drifts))
    flat = all(abs((x["hits"] / max(x["of"], 1)) - (ladder[0]["hits"] / max(ladder[0]["of"], 1)))
               < BAND for x in ladder)
    if flat:
        v.append("ACCURACY IS FLAT ACROSS THE WHOLE LADDER. Every rung enables something and none of "
                 "it is accuracy on this task, which is the claim this run was built to test.")
    led.done(ladder=ladder, verdict=v)
    return led.doc


if __name__ == "__main__":
    assert truth_at(1) == START + 6 and truth_at(2) == START + 6 - 13
    print("truths verified locally: step 1 -> %d, step %d -> %d\n"
          % (truth_at(1), len(OPS), truth_at(len(OPS))))
    d = run()
    print("\nTHE CAPACITY LADDER\n")
    for x in d["ladder"]:
        print("%-3s +%-11s drift@%-5s hit %2d/%-3d  %s"
              % (x["version"], x["adds"], x["drift"], x["hits"], x["of"],
                 " ".join("%s=%.2f" % (k[:5], val) for k, val in sorted(x["capacities"].items()))))
    print()
    for line in d["verdict"]:
        print(" ", line)
    print("\nEVIDENCE  state/lab/runs/x22_the_capacity_ladder/%s.json" % d["run_id"])
