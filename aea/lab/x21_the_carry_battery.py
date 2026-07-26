"""x21 - THE CARRY BATTERY. World 3's three components are three SHAPES of one job, plus a control.

SEALED OPENING: design/refs/bundle/W3_THE_REMEMBERER/W3_SEALED_OPENING.md, sha256 86d0cd4bd36f2c31,
written before the CARRY stage existed. Five predictions. This run scores 1, 2, 3 and 5.

WHAT WORLD 3 ACTUALLY HAS. `CHECKPOINT` (C-80) is the only p-value in the project: 11/11 against 9/16,
p=0.0216, at 50x calls - on ONE task at ONE chain length. `RECALL` (C-81) is n=3. `CONVERSATION` has
never been measured anywhere in this repo. Five of L5's fifteen census items have no implementation.

THE UNIT CHANGES HERE, and that is why the lattice cannot be reused. Every component in Worlds 1 and 2
acts INSIDE one exchange, so a subset lattice over independent trials could see it. `carry` acts
BETWEEN exchanges: run the same assembly twice independently and a component that persists state has
nowhere to put anything. The unit is a SEQUENCE.

FOUR CONTAINERS, and the container is the experiment:

  none          the running value and nothing else. The control, and what Worlds 1 and 2 did all along
  checkpoint    a DECLARED state line, emitted by the rod and fed forward verbatim. Bounded
  conversation  the FULL prior exchange, both sides, as real message history. Unbounded
  free          the rod writes its own note in any form. Prior sighting: 4,801 characters of doubt

TWO LENGTHS, because a rod that holds at four steps and drifts at sixteen is TWO CREATURES, and this
axis does not exist in the first two worlds. Length is the multiplier that makes World 3's bestiary
larger than eight without inventing anything.

COST IS MEASURED IN BOTH DIRECTIONS. `conversation` spends nothing extra on output and everything on
input, because its cost is a context that grows every step. A smoke test that summed only output priced
the most expensive container at zero, which is why `tok_in` is recorded per step.

WHAT IS BEING LOOKED FOR - the six bestiary slots, not "did it help":
  correct        a container converts a rod that drifts without it
  toxic          a container scores BELOW the control. Predicted: free form
  non-functional a rod no container reaches. Predicted to exist (prediction 5)
  attributes     a rod legible in DRIFT POINT rather than in the final answer
  evolution      rod + container -> a different creature
  the door       what none of them fixes

Run: python -m aea.lab.x21_the_carry_battery
"""
from __future__ import annotations

import concurrent.futures as _futures
import statistics

from aea.lab import overseer as OV
from aea.lab.organism import Chain, CARRY_FORMS
from aea.mind import fuel

N = 4
TEMP = 0.2
BAND = 0.10
LENGTHS = (4, 16)

# The chain is generated locally and its truth is computed locally, never asserted from memory. Each
# operation is small so a single arithmetic slip is a drift rather than a catastrophe, which is what
# makes the DRIFT POINT readable.
_OPS = ["add 7", "multiply by 3", "subtract 5", "add 12", "subtract 8", "multiply by 2",
        "add 19", "subtract 3", "add 6", "multiply by 2", "subtract 14", "add 25",
        "subtract 9", "multiply by 3", "add 4", "subtract 17"]


def ops(n):
    return _OPS[:n]


def truth_at(n):
    """Value after n steps, computed here. Never quoted from a prior run."""
    v = 0
    for op in _OPS[:n]:
        k = int(op.split()[-1])
        v = v + k if op.startswith("add") else v - k if op.startswith("subtract") else v * k
    return v


RODS = [
    ("ollama", "granite4.1:3b"),
    ("groq", "llama-3.1-8b-instant"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),
]


def cell(led, form, steps, rod):
    o = ops(steps)
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        recs = [f.result() for f in
                [pool.submit(Chain(rod, form=form, temperature=TEMP).run, o, truth_at)
                 for _ in range(N)]]
    finally:
        pool.shutdown(wait=True)
    done = [r for r in recs if r["completed"] == steps]
    for r in recs:
        led.note_flags(r["flags"])
    misses = [r["first_miss"] for r in done if r["first_miss"]]
    row = {"form": form, "steps": steps, "rod": "%s/%s" % rod,
           "ran": len(recs), "completed": len(done),
           "correct": sum(1 for r in done if r["correct"]),
           "hits": sum(r["hits"] for r in done), "hits_of": sum(r["completed"] for r in done),
           "median_first_miss": statistics.median(misses) if misses else None,
           "never_missed": sum(1 for r in done if r["first_miss"] is None),
           "tok_in": sum(r["tok_in"] for r in done), "tok_out": sum(r["tok_out"] for r in done),
           "tok_total": sum(r["tok_total"] for r in done),
           "carried_max": max([r["carried_max"] for r in done] or [0]),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                              attempts=len(recs), failures=len(recs) - len(done)),
           "records": recs}
    led.add(row)
    print("    %-13s len=%-3d %-24s correct %d/%-2d  steps-hit %3d/%-3d  drift@%s  tok %d"
          % (form, steps, rod[1].rsplit("/", 1)[-1][:23], row["correct"], row["completed"],
             row["hits"], row["hits_of"], row["median_first_miss"], row["tok_total"]), flush=True)
    return row


def run():
    led = OV.Ledger("x21_the_carry_battery", {
        "what": "four containers for state across a sequence, at two lengths",
        "why": "CONVERSATION has never been measured; CHECKPOINT has one task at one chain length",
        "sealed_opening": "W3_SEALED_OPENING.md sha256 86d0cd4bd36f2c31",
        "scores_predictions": ["1_checkpoint_is_a_lever", "2_conversation_disappoints_short",
                               "3_free_form_is_harmful", "5_a_creature_nothing_carries"],
        "unit": "a SEQUENCE, not a trial - the lattice cannot see a component that acts between calls",
        "forms": list(CARRY_FORMS), "lengths": list(LENGTHS), "n": N, "temperature": TEMP,
        "band": BAND, "rods": ["%s/%s" % r for r in RODS],
        "truth_source": "computed locally in truth_at(), never quoted from a prior run",
        "echo_note": "echoes_prompt is dropped for every container: a carrier quotes what it carries"})
    total = len(CARRY_FORMS) * sum(LENGTHS) * len(RODS) * N
    print("x21 - %d forms x lengths %s x %d rods x n=%d = %d calls\n"
          % (len(CARRY_FORMS), LENGTHS, len(RODS), N, total), flush=True)
    for steps in LENGTHS:
        for form in CARRY_FORMS:
            print("  [%s, %d steps]" % (form, steps), flush=True)
            for rod in RODS:
                if led.has(form=form, steps=steps, rod="%s/%s" % rod):
                    continue
                cell(led, form, steps, rod)

    rows = led.doc["rows"]

    def rate(form, steps, rod=None):
        s = [r for r in rows if r["form"] == form and r["steps"] == steps
             and (rod is None or r["rod"] == rod)]
        tot = sum(r["completed"] for r in s)
        return (sum(r["correct"] for r in s) / tot) if tot else None

    def cost(form, steps):
        s = [r for r in rows if r["form"] == form and r["steps"] == steps]
        tot = sum(r["completed"] for r in s)
        return (sum(r["tok_total"] for r in s) / tot) if tot else None

    margins, costs = {}, {}
    for steps in LENGTHS:
        base = rate("none", steps)
        base_c = cost("none", steps)
        for form in CARRY_FORMS:
            if form == "none":
                continue
            r = rate(form, steps)
            margins[(form, steps)] = None if None in (base, r) else round(r - base, 3)
            c = cost(form, steps)
            costs[(form, steps)] = None if not base_c or c is None else round(c / base_c, 2)

    SHORT, LONG = LENGTHS
    v, res = [], {}
    m_cp_long = margins.get(("checkpoint", LONG))
    res["1_checkpoint_is_a_lever"] = (m_cp_long is not None and m_cp_long >= 0.20)
    m_cv_short = margins.get(("conversation", SHORT))
    res["2_conversation_disappoints_short"] = (m_cv_short is not None and abs(m_cv_short) < BAND)
    m_free = [margins.get((("free"), L)) for L in LENGTHS]
    res["3_free_form_is_harmful"] = any(m is not None and m <= -BAND for m in m_free)
    unreached = []
    for rod in RODS:
        k = "%s/%s" % rod
        b = rate("none", LONG, k)
        if b is None or b > 0.5:
            continue
        if all((rate(f, LONG, k) or 0) - b < BAND for f in CARRY_FORMS if f != "none"):
            unreached.append(k)
    res["5_a_creature_nothing_carries"] = bool(unreached)

    v.append("SEALED PREDICTIONS SCORED: %d of %d held." % (sum(res.values()), len(res)))
    for k, okk in res.items():
        v.append("  %-34s %s" % (k, "HELD" if okk else "LOST"))
    for steps in LENGTHS:
        v.append("LENGTH %d - none %.2f | %s" % (
            steps, rate("none", steps) or 0,
            " | ".join("%s %s%s (%.1fx)" % (f, "+" if (margins.get((f, steps)) or 0) >= 0 else "",
                                            margins.get((f, steps)), costs.get((f, steps)) or 0)
                       for f in CARRY_FORMS if f != "none")))
    if unreached:
        v.append("NOTHING CARRIES: %s fails without a container and no container reaches it."
                 % ", ".join(u.rsplit("/", 1)[-1] for u in unreached))
    led.done(margins={"%s@%d" % k: v2 for k, v2 in margins.items()},
             cost_ratio={"%s@%d" % k: v2 for k, v2 in costs.items()},
             prediction_results=res, nothing_carries=unreached, verdict=v)
    return led.doc


if __name__ == "__main__":
    # SELF-CHECK before a single call. Truth is computed twice by different routes and must agree.
    assert truth_at(1) == 7 and truth_at(2) == 21 and truth_at(3) == 16, truth_at(3)
    v = 0
    for op in _OPS:
        k = int(op.split()[-1])
        v = v + k if op.startswith("add") else v - k if op.startswith("subtract") else v * k
    assert truth_at(len(_OPS)) == v
    print("truths verified locally: 4 steps -> %d, 16 steps -> %d\n" % (truth_at(4), truth_at(16)))

    d = run()
    print("\nRESULT\n")
    for line in d["verdict"]:
        print(" ", line)
    print("\noverseer:", d["overseer"])
    print("EVIDENCE  state/lab/runs/x21_the_carry_battery/%s.json" % d["run_id"])
