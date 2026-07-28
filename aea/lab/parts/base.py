"""The wire and the socket. Everything a part needs, and the contract it implements."""
from __future__ import annotations

import json
import os

STAGES = ("shape", "fire", "read", "repair", "carry", "judge")

# WHICH READ WINS, DECLARED RATHER THAN EMERGENT. This ordering reproduces exactly what the old
# last-writer-wins code did, verified against the frozen trace - it is written down, not changed.
# Whether it is the RIGHT ordering is now a separate question that can be asked with an experiment,
# because it is a config key (`{"read": {"precedence": [...]}}`) instead of an accident of stage
# order. That separation is the fix: making the seam explicit and re-litigating it are two changes,
# and doing both at once would have conflated them.
READ_PRECEDENCE = ("critic", "validation", "readout", "call")

_HERE = os.path.dirname(os.path.abspath(__file__))
CATALOGUE_PATH = os.path.join(os.path.dirname(_HERE), "organisms", "catalogue.json")


class Ctx:
    """The wire. Parts read and write here; nothing is passed between them directly."""

    def __init__(self, task, rod, *, temperature=0.2, max_tokens=1200, seat=(), config=None,
                 fuel=None, history=None):
        from aea.lab.parts.fuel import DEFAULT
        self.task, self.rod = task, rod
        # FUEL IS SEATED, NOT IMPORTED. Law IV in the code rather than only in the JSON.
        self.fuel = fuel or DEFAULT
        self.temperature, self.max_tokens = temperature, max_tokens
        self.seat, self.config = set(seat), dict(config or {})
        # PRIOR TURNS, AS REAL MESSAGES. Defect 13: chain.py built a history for the `conversation`
        # container and passed it nowhere, because there was no field here to pass it to and Call
        # always sent a single user message. The container that was supposed to carry the most
        # carried nothing at all, and its published finding is void. A container is not implemented
        # until the thing it claims to carry arrives in the request.
        self.history = list(history or [])
        self.prompt = task.get("data", "")
        self.text = ""              # what the call returned
        # ONE WRITER PER FIELD. Four parts used to assign ctx.answer directly - Call, Readout,
        # Validation and Critic - and the last one to run won. So "adding validation subtracts the
        # recoverable capacity", this lab's flagship result, was a statement about a shared mutable
        # slot rather than about guarding: on a mute reply, call+readout recovers 4 and
        # call+readout+validation returns None, because the guard re-reads the raw text from scratch
        # and clobbers the lever. In experimental terms the treatment was never independently
        # manipulated, which is construct confounding rather than a finding.
        #
        # Now each part claims its OWN key and the winner is decided by a DECLARED precedence. The
        # seam stops being an accident of ordering and becomes a variable that can be varied - which
        # is what it always should have been, because the precondition thesis lives in exactly that
        # interaction.
        self.reads = {}             # part key -> {value, dialect, declined}
        self.precedence = tuple((config or {}).get("read", {}).get("precedence") or READ_PRECEDENCE)
        self.verdict = None
        self.flags, self.rec = [], {}
        self.tok_in = self.tok_out = 0

    def has(self, key):
        return key in self.seat

    def cfg(self, key, field, default=None):
        return self.config.get(key, {}).get(field, default)

    def note(self, **kw):
        self.rec.update(kw)

    # --- THE READ CHANNEL. One writer per key, one resolver, precedence declared as data. --------

    def claim(self, key, value, dialect, declined=False):
        """The only way a part may record a read. A second claim on the same key is a bug, not a
        later opinion, so it raises rather than overwriting - which is the whole point."""
        if key in self.reads:
            raise RuntimeError("%s claimed the read twice; one writer per field" % key)
        self.reads[key] = {"value": value, "dialect": dialect, "declined": declined}

    def _winner(self):
        for key in self.precedence:
            r = self.reads.get(key)
            if r is not None:
                return r
        return None

    @property
    def answer(self):
        w = self._winner()
        return w["value"] if w else None

    @property
    def read_by(self):
        w = self._winner()
        return w["dialect"] if w else None

    @property
    def declined(self):
        w = self._winner()
        return bool(w and w["declined"])


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


_CAT = None


def variant_of(key, config=None):
    """The chosen variant, or the one marked default."""
    v = (config or {}).get(key, {}).get("variant")
    if v:
        return v
    vs = _entry(key).get("variants", {})
    return next((n for n, d in vs.items() if d.get("default")), None)


def template(key, variant=None, field="template"):
    """Prompt text is DATA. A variant is a data change, never a code change."""
    vs = _entry(key).get("variants", {})
    v = variant or next((n for n, d in vs.items() if d.get("default")), None)
    return (vs.get(v) or {}).get(field, "")


def _entry(key):
    global _CAT
    if _CAT is None:
        _CAT = load_catalogue()
    return next((c for c in _CAT["components"] if c["key"] == key), {})


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


def load_tasks(path=None):
    """The task bank as data. Experiments stop carrying their own copies."""
    path = path or os.path.join(os.path.dirname(_HERE), "organisms", "tasks.json")
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    for tid, t in doc["tasks"].items():
        t["id"] = tid
    return doc["tasks"], doc
