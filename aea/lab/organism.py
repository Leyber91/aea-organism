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

    def run(self, task, *, temperature=None, max_tokens=1200, keep_full=False, carried=""):
        ctx = P.Ctx(task, self.rod, temperature=temperature or self.temperature,
                    max_tokens=max_tokens, seat=self.keys, config=self.config)
        ctx.ok = False
        if carried:
            ctx.note(carried=carried)
        for part in self.parts:
            part.run(ctx)
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
