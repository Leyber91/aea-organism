"""x23 - INHERITANCE. The only creature-to-creature interaction in the project.

SEALED OPENING: W3_SEALED_OPENING.md sha256 86d0cd4bd36f2c31, PREDICTION 4:
  "Upward transfer costs nothing. Downward loses a WHOLE UNIT - a step change, not a slope."
  Reasoning as written: a fractional average loss would look like degradation; a whole box looks like
  a capability that either transfers or does not.

WHAT INHERITANCE IS HERE. One organism runs the first half of a chain and hands its carried state to a
DIFFERENT organism, which runs the second half. Everything else in this project measures one creature
alone. This measures what crosses between two.

  same     A hands to A            the control. Any drop is the handoff itself, not the fuel
  up       weak hands to strong    does the strong rod inherit a weak state cleanly?
  down     strong hands to weak    does the weak rod lose a box?

THE MEASURE IS THE SECOND HALF ONLY, and against the right baseline: the receiver running those same
steps ALONE from the true value. Inheritance is not "did the chain survive" - it is "did the receiver
do as well on inherited state as it does on its own".

  inherited = the first post-handoff step is correct given the value it was handed

DISCRETE OR GRADUAL is the actual question. A slope means capability degrades with distance; a step
means it transfers or it does not. That is prediction 4 and it is what the per-step trace can show.

CARRY FORM is `checkpoint`, the declared one. `free` is measured toxic at -0.636 (x21) and would be
measuring the container rather than the handoff.

Run: python -m aea.lab.x23_inheritance
"""
from __future__ import annotations

import concurrent.futures as _futures
import statistics

from aea.lab import overseer as OV
from aea.lab.organism import Chain
from aea.lab.parts.carry import Carry
from aea.mind import fuel

N = 4
TEMP = 0.2
BAND = 0.10
START = 48371
HANDOFF = 6

OPS = ["add 6", "subtract 13", "add 21", "subtract 8", "add 17", "subtract 24",
       "add 9", "subtract 31", "add 14", "subtract 7", "add 26", "subtract 19"]

# The seat is v4, the peak assembly from x22: widest live competence and the best retention on the
# ladder. Measuring a handoff on a degraded organism would confound the two.
SEAT = ["call", "goal", "frame", "readout"]

WEAK = ("ollama", "granite4.1:3b")
STRONG = ("groq", "llama-3.1-8b-instant")

ARMS = [
    ("same_weak", WEAK, WEAK),
    ("same_strong", STRONG, STRONG),
    ("up", WEAK, STRONG),
    ("down", STRONG, WEAK),
]


def truth_at(n):
    v = START
    for op in OPS[:n]:
        k = int(op.split()[-1])
        v = v + k if op.startswith("add") else v - k
    return v


def _half(rod, ops, start, truth_fn):
    return Chain(rod, form="checkpoint", seat=SEAT, start=start, temperature=TEMP).run(ops, truth_fn)


def one_handoff(giver, receiver):
    """First half on the giver, then the receiver continues from whatever it was actually handed."""
    a = _half(giver, OPS[:HANDOFF], START, truth_at)
    ta = [s for s in a["trace"] if s.get("ok")]
    handed = ta[-1]["value"] if ta else None
    if handed is None:
        return {"ok": False, "reason": "giver produced nothing"}

    def truth_from_handed(i):
        v = handed
        for op in OPS[HANDOFF:HANDOFF + i]:
            k = int(op.split()[-1])
            v = v + k if op.startswith("add") else v - k
        return v

    b = _half(receiver, OPS[HANDOFF:], handed, truth_from_handed)
    tb = [s for s in b["trace"] if s.get("ok")]
    return {"ok": True, "handed": handed, "handed_true": truth_at(HANDOFF),
            "giver_clean": handed == truth_at(HANDOFF),
            # INHERITED: the first step after the handoff is right GIVEN what was handed. That
            # separates the receiver's competence from the giver's error.
            "inherited": bool(tb) and tb[0]["hit"],
            "post_hits": sum(1 for s in tb if s["hit"]), "post_steps": len(tb),
            "post_first_miss": next((s["step"] for s in tb if not s["hit"]), None),
            "a": a, "b": b}


def solo_baseline(rod):
    """The receiver on the SAME second-half steps, from the true value, with no handoff."""
    def t(i):
        v = truth_at(HANDOFF)
        for op in OPS[HANDOFF:HANDOFF + i]:
            k = int(op.split()[-1])
            v = v + k if op.startswith("add") else v - k
        return v
    return _half(rod, OPS[HANDOFF:], truth_at(HANDOFF), t)


def cell(led, arm, giver, receiver):
    pool = _futures.ThreadPoolExecutor(max_workers=3)
    try:
        recs = [f.result() for f in [pool.submit(one_handoff, giver, receiver) for _ in range(N)]]
        base = [f.result() for f in [pool.submit(solo_baseline, receiver) for _ in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [r for r in recs if r.get("ok")]
    for r in ok:
        led.note_flags(r["a"]["flags"] + r["b"]["flags"])
    post = sum(r["post_hits"] for r in ok)
    post_of = sum(r["post_steps"] for r in ok)
    solo = sum(b["hits"] for b in base)
    solo_of = sum(b["completed"] for b in base)
    row = {"arm": arm, "giver": "%s/%s" % giver, "receiver": "%s/%s" % receiver,
           "ran": len(recs), "ok": len(ok),
           "giver_clean": sum(1 for r in ok if r["giver_clean"]),
           "inherited": sum(1 for r in ok if r["inherited"]),
           "post_hits": post, "post_of": post_of,
           "post_rate": round(post / post_of, 3) if post_of else None,
           "solo_hits": solo, "solo_of": solo_of,
           "solo_rate": round(solo / solo_of, 3) if solo_of else None,
           "post_first_miss": [r["post_first_miss"] for r in ok],
           "fuel": fuel.stamp(receiver[0], receiver[1], n=N, temperature=TEMP,
                              attempts=len(recs), failures=len(recs) - len(ok)),
           "records": recs}
    row["cost"] = (round(row["post_rate"] - row["solo_rate"], 3)
                   if None not in (row["post_rate"], row["solo_rate"]) else None)
    led.add(row)
    print("    %-12s %-22s -> %-22s inherited %d/%-2d  post %.2f vs solo %.2f  cost %+0.3f"
          % (arm, giver[1][:21], receiver[1][:21], row["inherited"], row["ok"],
             row["post_rate"] or 0, row["solo_rate"] or 0, row["cost"] or 0), flush=True)
    return row


def run():
    led = OV.Ledger("x23_inheritance", {
        "what": "what crosses when one organism hands its carried state to another",
        "why": "the only creature-to-creature interaction in the project, and World 3's evolution slot",
        "sealed_opening": "W3_SEALED_OPENING.md sha256 86d0cd4bd36f2c31, PREDICTION 4",
        "prediction_4": "upward costs nothing; downward loses a WHOLE UNIT - a step, not a slope",
        "seat": SEAT, "seat_note": "v4, the peak assembly from x22",
        "carry_form": "checkpoint - free is measured toxic at -0.636 and would measure the container",
        "measure": "the SECOND HALF only, against the receiver running the same steps alone from the "
                   "true value. Inheritance is not 'did the chain survive'.",
        "handoff_at": HANDOFF, "steps": len(OPS), "n": N, "temperature": TEMP, "band": BAND,
        "arms": [(a, "%s/%s" % g, "%s/%s" % r) for a, g, r in ARMS]})
    print("x23 - %d arms x n=%d x (%d + %d + %d baseline) steps\n"
          % (len(ARMS), N, HANDOFF, len(OPS) - HANDOFF, len(OPS) - HANDOFF), flush=True)
    for arm, g, r in ARMS:
        if led.has(arm=arm):
            continue
        cell(led, arm, g, r)

    rows = {r["arm"]: r for r in led.doc["rows"]}
    v, res = [], {}
    up, down = rows.get("up"), rows.get("down")
    sw, ss = rows.get("same_weak"), rows.get("same_strong")

    if up and up["cost"] is not None:
        res["up_costs_nothing"] = abs(up["cost"]) < BAND
        v.append("UP   weak -> strong: post %.2f vs solo %.2f, cost %+0.3f  (%s)"
                 % (up["post_rate"], up["solo_rate"], up["cost"],
                    "costs nothing" if res["up_costs_nothing"] else "COSTS"))
    if down and down["cost"] is not None:
        res["down_costs"] = down["cost"] <= -BAND
        v.append("DOWN strong -> weak: post %.2f vs solo %.2f, cost %+0.3f  (%s)"
                 % (down["post_rate"], down["solo_rate"], down["cost"],
                    "LOSES" if res["down_costs"] else "no loss"))
    for k, r in (("same_weak", sw), ("same_strong", ss)):
        if r and r["cost"] is not None:
            v.append("CTRL %-11s cost %+0.3f  (the handoff itself, not the fuel)" % (k, r["cost"]))

    # DISCRETE OR GRADUAL: does the receiver miss immediately after the handoff, or drift into it?
    for arm in ("up", "down"):
        r = rows.get(arm)
        if not r:
            continue
        fm = [x for x in r["post_first_miss"] if x]
        if fm:
            med = statistics.median(fm)
            v.append("%-4s first miss after handoff at step %s of %d  -> %s"
                     % (arm.upper(), med, len(OPS) - HANDOFF,
                        "DISCRETE, it fails at the seam" if med <= 1.5 else "GRADUAL, it drifts in"))

    ok4 = res.get("up_costs_nothing") and res.get("down_costs")
    v.append("PREDICTION 4 %s." % ("HELD" if ok4 else "LOST"))
    if not ok4:
        v.append("  claimed: upward costs nothing, downward loses a whole unit. Written before any "
                 "call and not edited.")
    led.done(prediction_4=ok4, results=res, verdict=v)
    return led.doc


if __name__ == "__main__":
    assert truth_at(1) == START + 6 and truth_at(HANDOFF) == 48369, truth_at(HANDOFF)
    print("truths verified locally: handoff value at step %d = %d, final = %d\n"
          % (HANDOFF, truth_at(HANDOFF), truth_at(len(OPS))))
    d = run()
    print("\nRESULT\n")
    for line in d["verdict"]:
        print(" ", line)
    print("\noverseer:", d["overseer"])
    print("EVIDENCE  state/lab/runs/x23_inheritance/%s.json" % d["run_id"])
