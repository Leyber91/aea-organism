"""The wire and the socket. Everything a part needs, and the contract it implements."""
from __future__ import annotations

import json
import os

STAGES = ("shape", "fire", "read", "repair", "carry", "judge")

_HERE = os.path.dirname(os.path.abspath(__file__))
CATALOGUE_PATH = os.path.join(os.path.dirname(_HERE), "organisms", "catalogue.json")


class Ctx:
    """The wire. Parts read and write here; nothing is passed between them directly."""

    def __init__(self, task, rod, *, temperature=0.2, max_tokens=1200, seat=(), config=None):
        self.task, self.rod = task, rod
        self.temperature, self.max_tokens = temperature, max_tokens
        self.seat, self.config = set(seat), dict(config or {})
        self.prompt = task.get("data", "")
        self.text = ""              # what the call returned
        self.answer = None          # what a read part extracted
        self.read_by = None
        self.declined = False       # a guard refused; ends the read
        self.verdict = None
        self.flags, self.rec = [], {}
        self.tok_in = self.tok_out = 0

    def has(self, key):
        return key in self.seat

    def cfg(self, key, field, default=None):
        return self.config.get(key, {}).get(field, default)

    def note(self, **kw):
        self.rec.update(kw)


class Part:
    """One seatable component. Subclass it, declare where it sits, implement `run`.

    Registration is automatic: importing the module is all it takes for the runner to wire it.
    """

    key = None
    stage = None
    order = 1
    kind = "lever"
    metric = "accuracy"
    requires = ()

    registry = {}

    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        if cls.key:
            if cls.stage not in STAGES:
                raise ValueError("%s declares unknown stage %r" % (cls.key, cls.stage))
            Part.registry[cls.key] = cls

    def run(self, ctx):
        raise NotImplementedError

    def __repr__(self):
        return "<%s %s.%d>" % (self.key, self.stage, self.order)


def load_catalogue(path=None):
    with open(path or CATALOGUE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def check_against_catalogue(doc=None):
    """Code and data must agree. A part in one and not the other is a silent divergence."""
    doc = doc or load_catalogue()
    declared = {c["key"]: c for c in doc["components"]}
    problems = []
    for key in set(declared) | set(Part.registry):
        if key not in Part.registry:
            problems.append("%s is in catalogue.json with no module" % key)
        elif key not in declared:
            problems.append("%s has a module with no catalogue entry" % key)
        else:
            cls, d = Part.registry[key], declared[key]
            for field in ("stage", "order", "kind", "metric"):
                if getattr(cls, field) != d.get(field):
                    problems.append("%s.%s: code %r, catalogue %r"
                                    % (key, field, getattr(cls, field), d.get(field)))
            if tuple(cls.requires) != tuple(d.get("requires", ())):
                problems.append("%s.requires: code %r, catalogue %r"
                                % (key, cls.requires, d.get("requires")))
    return problems


def wire(seat):
    """Seat keys in, ordered part instances out. Stage order then within-stage order."""
    unknown = [k for k in seat if k not in Part.registry]
    if unknown:
        raise KeyError("no module for %s" % ", ".join(unknown))
    parts = [Part.registry[k]() for k in seat]
    parts.sort(key=lambda p: (STAGES.index(p.stage), p.order))
    return parts


def unmet(seat):
    """Declared preconditions that are absent. Recorded, never assumed satisfied."""
    have = set(seat)
    return [(k, r) for k in seat for r in Part.registry[k].requires if r not in have]
