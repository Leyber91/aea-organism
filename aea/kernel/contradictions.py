"""contradictions.py - TWO THINGS THE RECORD BELIEVES THAT CANNOT BOTH BE TRUE.

    python -m aea.kernel.contradictions           what disagrees right now
    python -m aea.kernel.contradictions --test    the selftest, with controls

WHY THIS EXISTS, and it is the answer to a question three failed attempts sharpened.

R5 needs a hypothesis the entity GENERATES, not one it selects. `check_a_belief` was added to the
move surface on 2026-08-04 and chosen zero times in 72 sandbox ticks - and choosing it would not
have been generation anyway, because the claim it tests is handed to it. A menu item is a lever
somebody else loaded. **A hypothesis is not a move; it is a noticing.**

Two things have already been tried and neither produced one:

    THE NUDGE       "your record holds NOTHING from outside, N of M budget unspent"
                    named a deficiency AND its remedy. That is an instruction, and it produced
                    compliance - two look_outward choices while the line was present
    THE SURFACE     "right now I can: ..." named CAPABILITIES and stopped.
                    Measured: the treatment arm chose NONE 16 times against the control's 7 and
                    used 5 distinct moves against 7. Naming what it could do made it do LESS

A capability is not a reason. A deficiency-with-a-remedy is an order. **A contradiction is neither:
it is a fact, with a hole in it, and no instruction attached.** It cannot be complied with. The only
way to resolve it is to find out which side is false - which is a hypothesis, arrived at rather than
picked. That is the claim this module exists to test, and it is falsifiable: if the entity reads a
contradiction and proposes nothing, the theory is wrong and the bound is something else again.

NO MODEL RUNS HERE. Every rule below is two files compared by arithmetic. A detector that asked a
model what looks inconsistent would be handing the entity a model's opinion dressed as its own
record, and the honesty law does not survive that. `selftest` includes a control that a consistent
record yields nothing, because a detector that always finds something is a horoscope.

AND IT NAMES NO REMEDY, ENFORCED BY A CONTROL. `render()` output is checked against an imperative
word-list, because the whole distinction from the nudge is that this text tells the entity nothing
to do. The moment someone appends "you could check this with check_a_belief", this stops being an
experiment about noticing and becomes the nudge again, wearing different clothes.
"""
from __future__ import annotations

import json
import os
import sys

from aea.kernel import grid

# The words that would turn a fact into an instruction. Checked in the selftest, not merely avoided.
IMPERATIVES = ("you should", "you could", "try ", "consider ", "check ", "run ", "use ",
               "recommend", "suggest", "next step", "in order to", "so that you")


def _load(name: str) -> dict:
    return grid.load_json(os.path.join(grid.STATE, name), {}) or {}


def find(state: dict = None, limit: int = 6) -> list:
    """Every pair of rows the entity wrote that cannot both be true. Most decisive first.

    `state` lets the selftest pass a synthetic record; production passes nothing and it reads disk."""
    s = state or {}
    usage = s.get("energy_usage.json", _load("energy_usage.json"))
    paths = s.get("paths.json", _load("paths.json"))
    fitness = s.get("model_fitness.json", _load("model_fitness.json"))
    rods = s.get("rods.json", _load("rods.json"))
    out = []

    def add(rank, kind, subject, a, b):
        out.append(dict(rank=rank, kind=kind, subject=subject, a=a, b=b))

    # 1. A FILE AGAINST ITSELF. The sharpest kind: no staleness argument is available, because both
    #    numbers were written by the same writer about the same rod. Something that answered 120
    #    times is not a rod that "cannot answer" - one of the two readings must be wrong.
    for key, u in (usage or {}).items():
        if not isinstance(u, dict) or not u.get("cooled_at"):
            continue
        if (u.get("ok") or 0) > 0:
            add(0, "one file against itself", key,
                "energy_usage.json: cooled after %s consecutive failures - it cannot answer"
                % u.get("consec_fail"),
                "energy_usage.json: ok=%s of %s calls - it HAS answered"
                % (u.get("ok"), u.get("calls")))

    # 2. A ROUTE THAT WAS CRYSTALLISED POINTS AT A ROD THE USAGE RECORD REFUSES.
    for route, spec in (paths or {}).items():
        if not isinstance(spec, dict):
            continue
        key = "%s/%s" % (spec.get("plant"), spec.get("model"))
        u = usage.get(key)
        if isinstance(u, dict) and (u.get("cooled_at") or (u.get("consec_fail") or 0) >= 3):
            add(1, "a route against the usage record", key,
                "paths.json[%s]: crystallised winner, wins=%s" % (route, spec.get("wins")),
                "energy_usage.json: consec_fail=%s, cooled=%s"
                % (u.get("consec_fail"), bool(u.get("cooled_at"))))

    # 3. A ROD PROMOTED BY FITNESS THAT USAGE HAS COOLED.
    for n in (fitness.get("nodes") or []):
        key = "%s/%s" % (n.get("plant"), n.get("model"))
        u = usage.get(key)
        if isinstance(u, dict) and u.get("cooled_at"):
            add(2, "fitness against usage", key,
                "model_fitness.json (%s): promoted, tier=%s"
                % (fitness.get("generated"), n.get("tier")),
                "energy_usage.json: cooled, consec_fail=%s" % u.get("consec_fail"))

    # 4. THE CATALOGUE SAYS SERVED, USAGE SAYS UNUSABLE.
    for m, v in (rods.get("rods") or {}).items():
        if not isinstance(v, dict) or v.get("nvidia_catalog_state") != "served":
            continue
        key = "nvidia/%s" % m
        u = usage.get(key)
        if isinstance(u, dict) and u.get("cooled_at"):
            add(3, "the catalogue against usage", key,
                "rods.json (%s): served" % rods.get("generated"),
                "energy_usage.json: cooled, consec_fail=%s" % u.get("consec_fail"))

    out.sort(key=lambda r: (r["rank"], r["subject"]))
    return out[:limit]


def render(items: list = None, limit: int = 3) -> str:
    """The lines the wake sees. A FACT AND A HOLE - never an instruction.

    It stops after stating both sides. No move is named, no remedy is offered, and the selftest
    enforces that against a word-list, because the difference between this and the nudge is exactly
    the absence of the sentence a reader most wants to add."""
    items = find() if items is None else items
    if not items:
        return ""
    lines = ["things your record says that cannot both be true:"]
    for c in items[:limit]:
        lines.append("  - about %s" % c["subject"])
        lines.append("      %s" % c["a"])
        lines.append("      %s" % c["b"])
    return "\n".join(lines)


def selftest() -> list:
    checks = []

    def chk(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    # CONTROL: a consistent record must yield NOTHING. A detector that always fires is a horoscope.
    clean = {"energy_usage.json": {"a/b": dict(calls=5, ok=5, consec_fail=0)},
             "paths.json": {}, "model_fitness.json": {}, "rods.json": {}}
    chk("CONTROL a consistent record yields no contradiction", find(clean) == [])

    # a planted self-contradiction is found
    planted = dict(clean)
    planted["energy_usage.json"] = {"p/q": dict(calls=100, ok=90, consec_fail=4, cooled_at=1.0)}
    got = find(planted)
    chk("a rod that is cooled AND has succeeded is caught", len(got) == 1, str(len(got)))
    chk("...and it is ranked first (a file against itself)",
        bool(got) and got[0]["kind"] == "one file against itself")
    chk("...and it names BOTH sides", bool(got) and got[0]["a"] and got[0]["b"])

    # CONTROL: cooled with zero successes is NOT a contradiction - it is just a dead rod
    consistent_dead = dict(clean)
    consistent_dead["energy_usage.json"] = {"p/q": dict(calls=100, ok=0, consec_fail=100,
                                                        cooled_at=1.0)}
    chk("CONTROL a rod cooled with ZERO successes is not a contradiction",
        find(consistent_dead) == [])

    # a route pointing at a refused rod is caught
    route = dict(clean)
    route["energy_usage.json"] = {"groq/x": dict(calls=10, ok=0, consec_fail=9, cooled_at=1.0)}
    route["paths.json"] = {"math": dict(plant="groq", model="x", wins=2)}
    g2 = find(route)
    chk("a crystallised route pointing at a refused rod is caught", len(g2) == 1, str(g2[:1])[:60])

    # THE TEXT NAMES NO REMEDY - the control that keeps this from becoming the nudge
    txt = render(got).lower()
    bad = [w for w in IMPERATIVES if w in txt]
    chk("CONTROL the rendered text contains NO instruction", not bad, str(bad))
    chk("...and it does name a move", "check_a_belief" not in txt)
    chk("the rendered text states both sides", txt.count("about ") >= 1 and "\n" in txt)

    # NOTHING HERE MAY RUN A MODEL, and the needles are BUILT rather than written, because the
    # first version searched its own source for the literal string and found it - in the search.
    # A guard that reads the file it lives in must not name what it is hunting, or it reports
    # itself. Small, and the same shape as a grep that matches its own pattern file.
    src = open(__file__, encoding="utf-8", errors="replace").read()
    needles = ["call_" + "openai", "energy." + "draw", "grid." + "complete"]
    hits = [n for n in needles if n in src]
    chk("CONTROL no model is consulted by this module", not hits, str(hits))
    return checks


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if "--test" in sys.argv:
        res = selftest()
        for n, ok, d in res:
            print("  %-58s %s%s" % (n, "ok" if ok else "FAIL", ("   " + d) if d else ""))
        bad = [r for r in res if not r[1]]
        print("\n  %d of %d checks pass" % (len(res) - len(bad), len(res)))
        sys.exit(1 if bad else 0)
    items = find()
    print("%d contradiction(s) in the record\n" % len(items))
    print(render(items, limit=10) or "  (none)")
