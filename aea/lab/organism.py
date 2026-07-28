"""An assembled AEA. A creature is a seat of parts on pinned fuel, and both live in files.

  ORGANISM   an ordered set of parts, assembled and runnable
  SEAT       which parts. `aea/lab/organisms/creatures/*.json`
  FUEL       a pinned rod. Law IV: the same seat on different fuel is a different creature
  WIRING     derived, never written. Each part declares its stage and its order within that stage,
             and the runner sorts by both. Adding a module is all it takes to seat a new part.

The parts live in `aea/lab/parts/`, one module each. `parts.check_against_catalogue()` refuses to let
the code and `organisms/catalogue.json` disagree.

Run: python -m aea.lab.organism
"""
from __future__ import annotations

import json
import os

from aea.lab import parts as P
from aea.lab.parts.carry import FORMS as CARRY_FORMS  # noqa: F401
from aea.lab.parts.read import read_work  # noqa: F401

_HERE = os.path.dirname(os.path.abspath(__file__))
ORGANISMS_DIR = os.path.join(_HERE, "organisms")

CATALOGUE_DOC = P.load_catalogue()
CATALOGUE = [P.Part.registry[c["key"]] for c in CATALOGUE_DOC["components"]
             if c["key"] in P.Part.registry]
BY_KEY = P.Part.registry


class Organism:
    """A seat on fuel. `run` sends one task through every seated part, in wired order."""

    def __init__(self, keys, rod, *, version=None, label=None, config=None):
        self.keys = list(keys)
        self.rod = tuple(rod)
        self.version = version
        self.config = dict(config or {})
        self.label = label or ("v%s" % version if version else "+".join(self.keys))
        self.parts = P.wire(self.keys)
        self.unmet = P.unmet(self.keys)
        self.spec = None
        self.temperature = 0.2
        self.fuel = None

    def run(self, task, *, temperature=None, max_tokens=1200, keep_full=False, carried="",
            fuel=None, history=None):
        ctx = P.Ctx(task, self.rod, temperature=temperature or self.temperature,
                    max_tokens=max_tokens, seat=self.keys, config=self.config,
                    fuel=fuel or self.fuel, history=history)
        ctx.ok = False
        if carried:
            ctx.note(carried=carried)
        for part in self.parts:
            # THE MANIPULATION CHECK, AS AN ASSERTION RATHER THAN A CONVENTION. Experimental
            # psychology calls the failure this catches CONSTRUCT CONFOUNDING: manipulating more
            # than the intended construct. Seating a component must change that component's fields
            # and nothing else, or the arm is not a manipulation of that component - it is a
            # manipulation of whatever else it touched. The lab's flagship result was exactly this
            # failure and it survived for weeks because nothing ever checked.
            before = set(ctx.reads)
            part.run(ctx)
            stray = (set(ctx.reads) - before) - {part.key}
            if stray:
                raise RuntimeError(
                    "%s wrote reads it does not own: %s. Seating a part must change only its own "
                    "fields, or the arm measures more than the part." % (part.key, sorted(stray)))
            if part.stage == "fire" and not ctx.ok:
                break
        rec = {"organism": self.label, "version": self.version, "parts": list(self.keys),
               "rod": "%s/%s" % self.rod, "task": task["id"],
               "precondition_unmet": self.unmet, "temperature": ctx.temperature,
               "ok": ctx.ok, "flags": sorted(set(ctx.flags)),
               "answer": ctx.answer, "read_by": ctx.read_by or "none",
               "verdict": ctx.verdict, "tok_in": ctx.tok_in, "tok_out": ctx.tok_out}
        rec.update(ctx.rec)
        if keep_full:
            rec["text"] = ctx.text
        return rec

    def has(self, key):
        return key in self.keys

    def wiring(self):
        return [(p.stage, p.order, p.key) for p in self.parts]


def load_creature(name_or_path):
    """An organism from its file: seat, pinned fuel, receipt, measured state."""
    p = name_or_path
    if not os.path.isabs(p) and not p.endswith(".json"):
        p = os.path.join(ORGANISMS_DIR, "creatures", "%s.json" % p)
    with open(p, encoding="utf-8") as fh:
        spec = json.load(fh)
    f = spec["fuel"]
    org = Organism(spec["seat"], (f["plant"], f["model"]), label=spec["name"],
                   config=spec.get("seat_config"))
    org.spec = spec
    org.temperature = f.get("temperature", 0.2)
    return org


def creatures():
    d = os.path.join(ORGANISMS_DIR, "creatures")
    return sorted(f[:-5] for f in os.listdir(d) if f.endswith(".json")) if os.path.isdir(d) else []


# THE THREE ASSEMBLY FAMILIES x16 MEASURES. Removed in the modularity audit (bc0b27c) because
# nothing in the runtime called them - but x16 did, and x17/x19/x20 import x16, so FOUR experiment
# modules stopped importing at all. Found 2026-07-28 by importing all 86 runtime modules rather than
# reading them. It matters beyond tidiness: x19's findings are cited as evidence in METHOD.md and in
# the annex, and a result whose experiment cannot be re-run is a result nobody can check. Restored
# verbatim from the commit that dropped them.

def ascending(order=None):
    """v1..vN, each everything before it plus one part. The spine."""
    keys = list(order or [c["key"] for c in CATALOGUE_DOC["components"]])
    return [(i + 1, keys[:i + 1]) for i in range(len(keys))]


def deprived(order=None):
    """Seats missing a DECLARED precondition. Nothing is called toxic before it runs: x16 ran
    call+frame, whose declared precondition is absent, and it scored 0.65 against 0.66 for the seat
    that satisfies it. A precondition in a catalogue is a hypothesis until an assembly convicts it."""
    keys = list(order or [c["key"] for c in CATALOGUE_DOC["components"]])
    out = []
    for c in CATALOGUE_DOC["components"]:
        for r in c.get("requires", ()):
            if r != "call":
                out.append(("%s without %s" % (c["key"], r),
                            [k for k in keys if k in ("call", c["key"])]))
    if not out:
        # AN EMPTY FAMILY IS A CLAIM AND IT HAS TO BE MADE OUT LOUD.
        #
        # Every component in the catalogue today declares `requires: [call]` and nothing else, and
        # this function filters `call` out by design - so it returns [] for the whole catalogue.
        # Re-running x16 would report an empty "toxic" family, no error, no warning, and a reader
        # would take it as "nothing was toxic" rather than "nothing was tested". That is defect 20's
        # exact shape: a container that silently never ran. Raising costs one line and makes the
        # difference between a measured zero and an unmeasured one impossible to confuse.
        raise ValueError(
            "no deprived seat exists: every component in the catalogue declares only `call` as a "
            "precondition, so there is no non-trivial precondition to withhold. This family cannot "
            "be measured against the current catalogue - that is a finding about the catalogue, not "
            "an empty result to report.")
    return out


def oblique(order=None):
    """Seats that SKIP a rung beneath them. Whether they WORK is measured, never assumed.

    REQUIRES and DEPENDS are two edges and the census encodes one. Latency requires nothing and
    depends on everything, so it is not a counterexample to the ordering claim; the frame seats are.
    """
    return [("frame without measure", ["call", "goal", "frame"]),
            ("frame+readout without measure", ["call", "goal", "frame", "readout"]),
            ("clock alone", ["call", "latency"]),
            ("procedure without goal", ["call", "frame"])]


def __getattr__(name):
    """Chain moved to aea.lab.chain. Re-exported so existing experiments keep importing it."""
    if name == "Chain":
        from aea.lab.chain import Chain
        return Chain
    raise AttributeError(name)


def classify(label, correct, baseline, *, band=0.10):
    """Assigned FROM measurement, against the band x16 established by accident when the same
    assembly ran twice under two names and scored 0.70 and 0.60."""
    if correct is None:
        return "unmeasured"
    if correct <= 0.01:
        return "void"
    if baseline is None:
        return "working" if correct > band else "weak"
    d = correct - baseline
    return "toxic" if d <= -band else ("working" if d >= band else "inert")


if __name__ == "__main__":
    problems = P.check_against_catalogue(CATALOGUE_DOC)
    print("code vs catalogue.json:", problems or "agree on every field", "\n")
    print("%-7s %-6s %-11s %-9s %s" % ("stage", "order", "part", "kind", "metric"))
    for p in P.wire(list(P.Part.registry)):
        print("%-7s %-6d %-11s %-9s %s" % (p.stage, p.order, p.key, p.kind, p.metric))
    print("\ncreatures on disk:")
    for cid in creatures():
        o = load_creature(cid)
        print("  %-22s %-34s %s/%s" % (o.label, "+".join(o.keys), o.rod[0], o.rod[1]))
