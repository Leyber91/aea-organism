"""x23b - INHERITANCE ACROSS PLANTS, with a calibration gate.

x23 RAN TWO RODS FROM THE LOW END and its `down` arm was void: the receiver scored 0.00 SOLO, so
there was no capability there to lose. You cannot measure a loss on something that has nothing.
Eight rods across four plants are live; x23 used two.

THE GATE IS THE FIX AND IT IS PART OF THE RUN. Solo baselines first, for every rod, on the exact
steps the receiver will be given. Only rods with HEADROOM - solo above 0.5 - can be receivers,
because only they can visibly lose something. Rods below it are givers only.

That is the calibration lesson stated as code rather than as a note: x21's baseline was too high to
show a gain, x23's was too low to show a loss, and both were discovered after the calls were spent.

LAW IV IS THE OTHER HALF. The same seat on different fuel is a different organism, so a handoff
between PLANTS is not the same event as a handoff within one. Arms cross plants deliberately.

  same_plant_down    a stronger rod hands to a weaker one, same plant
  cross_plant_down   the same drop, across plants
  cross_plant_up     weaker to stronger, across plants
  self               the control: the handoff itself, not the fuel

Run: python -m aea.lab.x23b_inheritance_across_plants
"""
from __future__ import annotations

import concurrent.futures as _futures

from aea.lab import overseer as OV
from aea.lab.chain import Chain
from aea.mind import fuel

N = 3
TEMP = 0.2
BAND = 0.10
START = 48371
HANDOFF = 6
HEADROOM = 0.5

OPS = ["add 6", "subtract 13", "add 21", "subtract 8", "add 17", "subtract 24",
       "add 9", "subtract 31", "add 14", "subtract 7", "add 26", "subtract 19"]

SEAT = ["call", "goal", "frame", "readout"]      # v4, the peak assembly from x22

RODS = [
    ("ollama", "granite4.1:3b"),
    ("groq", "llama-3.1-8b-instant"),
    ("groq", "llama-3.3-70b-versatile"),
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),
    ("cerebras", "gpt-oss-120b"),
]


def truth_at(n):
    v = START
    for op in OPS[:n]:
        k = int(op.split()[-1])
        v = v + k if op.startswith("add") else v - k
    return v


def _second_half_truth(base):
    def t(i):
        v = base
        for op in OPS[HANDOFF:HANDOFF + i]:
            k = int(op.split()[-1])
            v = v + k if op.startswith("add") else v - k
        return v
    return t


def _run(rod, ops, start, truth_fn):
    return Chain(rod, form="checkpoint", seat=SEAT, start=start, temperature=TEMP).run(ops, truth_fn)


def solo(rod):
    """The receiver on the second half, from the TRUE value, with no handoff. The gate."""
    return _run(rod, OPS[HANDOFF:], truth_at(HANDOFF), _second_half_truth(truth_at(HANDOFF)))


def handoff(giver, receiver):
    a = _run(giver, OPS[:HANDOFF], START, truth_at)
    ta = [s for s in a["trace"] if s.get("ok")]
    handed = ta[-1]["value"] if ta else None
    if handed is None:
        return {"ok": False}
    b = _run(receiver, OPS[HANDOFF:], handed, _second_half_truth(handed))
    tb = [s for s in b["trace"] if s.get("ok")]
    return {"ok": True, "handed": handed, "giver_clean": handed == truth_at(HANDOFF),
            "inherited": bool(tb) and tb[0]["hit"],
            "hits": sum(1 for s in tb if s["hit"]), "steps": len(tb),
            "first_miss": next((s["step"] for s in tb if not s["hit"]), None)}


def gate(led):
    print("  CALIBRATION GATE - solo baselines on the second half\n", flush=True)
    base = {}
    for rod in RODS:
        k = "%s/%s" % rod
        pool = _futures.ThreadPoolExecutor(max_workers=3)
        try:
            rs = [f.result() for f in [pool.submit(solo, rod) for _ in range(N)]]
        finally:
            pool.shutdown(wait=True)
        hits = sum(r["hits"] for r in rs)
        of = sum(r["completed"] for r in rs)
        rate = round(hits / of, 3) if of else 0.0
        base[k] = rate
        led.add({"kind": "solo", "rod": k, "rate": rate, "hits": hits, "of": of,
                 "headroom": rate >= HEADROOM,
                 "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                                    attempts=len(rs), failures=0),
                 "records": rs})
        print("    %-42s solo %.2f  %s" % (k[:41], rate,
              "RECEIVER (has headroom)" if rate >= HEADROOM else "giver only, nothing to lose"),
              flush=True)
    return base


def run():
    led = OV.Ledger("x23b_inheritance_across_plants", {
        "what": "what crosses between organisms, across plants, with a calibration gate",
        "why": "x23 ran two rods from the low end and its down arm was void - the receiver scored "
               "0.00 solo, so there was no capability to lose",
        "gate": "solo baseline first; only rods above %.2f can be receivers" % HEADROOM,
        "law_iv": "the same seat on different fuel is a different organism, so a cross-plant handoff "
                  "is not the same event as a within-plant one",
        "seat": SEAT, "carry_form": "checkpoint", "handoff_at": HANDOFF,
        "n": N, "temperature": TEMP, "band": BAND,
        "rods": ["%s/%s" % r for r in RODS]})

    base = gate(led)
    receivers = [r for r in RODS if base.get("%s/%s" % r, 0) >= HEADROOM]
    if not receivers:
        led.done(verdict=["NO ROD HAS HEADROOM. Every receiver fails the second half alone, so no "
                          "loss is measurable. The task is too hard for this fleet."])
        return led.doc

    arms = []
    for rec in receivers:
        rk = "%s/%s" % rec
        for giv in RODS:
            gk = "%s/%s" % giv
            if gk == rk:
                arms.append(("self", giv, rec))
            elif base.get(gk, 0) > base[rk] + BAND:
                arms.append(("down_same_plant" if giv[0] == rec[0] else "down_cross_plant", giv, rec))
            elif base.get(gk, 0) < base[rk] - BAND:
                arms.append(("up_same_plant" if giv[0] == rec[0] else "up_cross_plant", giv, rec))

    print("\n  %d receivers with headroom, %d arms\n" % (len(receivers), len(arms)), flush=True)
    for arm, giv, rec in arms:
        gk, rk = "%s/%s" % giv, "%s/%s" % rec
        if led.has(kind="handoff", giver=gk, receiver=rk):
            continue
        pool = _futures.ThreadPoolExecutor(max_workers=3)
        try:
            rs = [f.result() for f in [pool.submit(handoff, giv, rec) for _ in range(N)]]
        finally:
            pool.shutdown(wait=True)
        ok = [r for r in rs if r.get("ok")]
        hits = sum(r["hits"] for r in ok)
        of = sum(r["steps"] for r in ok)
        rate = round(hits / of, 3) if of else None
        cost = round(rate - base[rk], 3) if rate is not None else None
        led.add({"kind": "handoff", "arm": arm, "giver": gk, "receiver": rk,
                 "ok": len(ok), "ran": len(rs),
                 "giver_clean": sum(1 for r in ok if r["giver_clean"]),
                 "inherited": sum(1 for r in ok if r["inherited"]),
                 "rate": rate, "solo": base[rk], "cost": cost,
                 "first_miss": [r["first_miss"] for r in ok], "records": rs})
        print("    %-16s %-30s -> %-30s inh %d/%-2d  %.2f vs solo %.2f  cost %+0.3f"
              % (arm, gk[-29:], rk[-29:], sum(1 for r in ok if r["inherited"]), len(ok),
                 rate or 0, base[rk], cost or 0), flush=True)

    hs = [r for r in led.doc["rows"] if r.get("kind") == "handoff" and r.get("cost") is not None]
    v = []
    for a in ("self", "up_same_plant", "up_cross_plant", "down_same_plant", "down_cross_plant"):
        s = [r for r in hs if r["arm"] == a]
        if s:
            m = sum(r["cost"] for r in s) / len(s)
            v.append("%-17s n=%d  mean cost %+0.3f  (%s)"
                     % (a, len(s), m, "free" if abs(m) < BAND else
                        "LOSES" if m < 0 else "gains"))
    cross = [r["cost"] for r in hs if "cross" in r["arm"]]
    same = [r["cost"] for r in hs if "same_plant" in r["arm"]]
    if cross and same:
        d = sum(cross) / len(cross) - sum(same) / len(same)
        v.append("CROSSING PLANTS costs %+0.3f more than staying within one. %s"
                 % (d, "Law IV shows in the handoff." if abs(d) >= BAND else
                    "Inside the band: fuel identity does not survive as a handoff cost."))
    led.done(baselines=base, verdict=v)
    return led.doc


if __name__ == "__main__":
    def _by_hand(n):
        v = START
        for op in OPS[:n]:
            k = int(op.split()[-1])
            v = v + k if op.startswith("add") else v - k
        return v
    assert all(truth_at(i) == _by_hand(i) for i in range(1, len(OPS) + 1))
    print("truths verified by two routes: handoff %d, final %d\n"
          % (truth_at(HANDOFF), truth_at(len(OPS))))
    d = run()
    print("\nRESULT\n")
    for line in d["verdict"]:
        print(" ", line)
    print("\nEVIDENCE  state/lab/runs/x23b_inheritance_across_plants/%s.json" % d["run_id"])
