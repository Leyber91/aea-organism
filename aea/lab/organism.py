"""organism.py - AN ASSEMBLED AEA. Version N is the first N components seated, and it is a creature.

THE UNIT OF MEASUREMENT CHANGES HERE, and this is the correction that makes the walk testable.

Until now this lab measured RODS: what fuel can do, on a bench, with instruments applied in analysis.
That is the ground the architecture stands on rather than the architecture. A creature is not a rod. **A
creature is an assembled entity**: a version of the AEA with a specific set of components seated, running
end to end, on stated fuel.

  ORGANISM      an ordered set of components, assembled and runnable
  VERSION N     the first N components of an order. v1 can do one thing; v86 is the whole architecture
  FUEL          a pinned rod. Law IV: the same organism on different fuel is a different creature, so
                the fuel is never chosen by a ladder at run time and never left unstated

THREE KINDS OF CREATURE, and the last two are the reason this file exists rather than a loop over levels:

  ASCENDING       v1, v2, v3... each is everything before it plus one component, in necessity order.
                  ~86 of them on the full path. The spine of the bestiary
  TOXIC           an assembly whose component's PRECONDITION is absent. It runs, it returns something,
                  and the something is empty or worse. `Arbiter vacui` is one: a scorer above no goal
                  returns a clean verdict about nothing
  OBLIQUE         an assembly that SKIPS a rung below it and works anyway. Every one of these is a
                  counterexample to C-63, the ordering claim, and two are already suspected: latency
                  needs nothing beneath it, and a procedure succeeds with no goal above it

WHAT A COMPONENT IS. A small object with a name, a census id, the preconditions it needs, and one
function that transforms a stage of the pipeline. The pipeline is deliberately tiny, because the whole
point is that a version of the AEA is assembled rather than written:

  SHAPE   the prompt is built             (GOAL, FRAME shape it)
  FIRE    one call on the pinned rod      (CALL: without it there is no organism)
  READ    the reply becomes an answer     (READOUT, VALIDATION read it)
  JUDGE   the answer becomes a verdict    (MEASURE judges it; LATENCY annotates it)

Preconditions are DECLARED and CHECKED, which is the capability the census does not contain and the
bench cannot do: a part whose precondition is unmet is recorded as `precondition_unmet` rather than
silently producing a clean-looking result.

Run: python -m aea.lab.organism            (self-test: assemble v1..vN and show what each can do)
"""
from __future__ import annotations

import re
import time

from aea.lab import harness as H
from aea.lab import overseer as OV


# --- COMPONENTS ------------------------------------------------------------------------------------

class Component:
    """One seatable part of an AEA. `stage` says where it acts; `requires` is checked, never assumed."""

    def __init__(self, key, name, census, stage, requires=(), note=""):
        self.key, self.name, self.census = key, name, census
        self.stage, self.requires, self.note = stage, tuple(requires), note

    def __repr__(self):
        return "<%s %s>" % (self.key, self.census or "candidate")


# The order is the NECESSITY order the walk has measured, not the census's filing order. Where a
# measurement moved something, the measurement wins and the note says which run.
CATALOGUE = [
    Component("call", "THE CALL", "C-62", "fire", (),
              "without it there is no organism; every version contains it"),
    Component("goal", "THE GOAL", "C-12", "shape", ("call",),
              "x12: 0 of 304 succeed with neither goal nor procedure"),
    Component("measure", "THE MEASURE", "C-15", "judge", ("call",),
              "x13: changes no answer, changes what can be known. 0 of 153 fooled"),
    Component("frame", "THE FRAME", "C-04", "shape", ("call", "goal"),
              "x15: working 0.41 -> 1.00. A METHOD frame only; a manner frame harms"),
    Component("readout", "THE READOUT", "C-87?", "read", ("call",),
              "x13/x15: recovers on UNFRAMED replies; redundant once framed"),
    Component("validation", "THE VALIDATION", "C-75", "read", ("call",),
              "x14: identical accuracy, converts silent commitment into visible abstention"),
    Component("latency", "THE CLOCK", "C-74", "judge", (),
              "x13: requires NOTHING below it. The first oblique component"),
]
BY_KEY = {c.key: c for c in CATALOGUE}


# --- THE ORGANISM ----------------------------------------------------------------------------------

_ENUM = re.compile(r"(?m)^\s*(\d{1,3})[.)]\s+\S")


class Organism:
    """An assembled AEA on pinned fuel. Assemble it, run a task through it, get a receipt."""

    def __init__(self, keys, rod, *, version=None, label=None):
        self.keys = list(keys)
        self.parts = [BY_KEY[k] for k in self.keys]
        self.rod = tuple(rod)
        self.version = version
        self.label = label or ("v%s" % version if version else "+".join(self.keys))
        self.unmet = self._check_preconditions()

    def _check_preconditions(self):
        """THE CHECK THE CENSUS DOES NOT CONTAIN. A part whose precondition is absent is recorded, not
        silently trusted. This is what makes a TOXIC assembly visible instead of merely wrong."""
        have = set(self.keys)
        return [(c.key, r) for c in self.parts for r in c.requires if r not in have]

    def has(self, key):
        return key in self.keys

    def run(self, task, *, temperature=0.2, max_tokens=1200):
        """SHAPE, FIRE, READ, JUDGE. Every stage records what it did, so the receipt shows the assembly
        working rather than a number with no provenance."""
        rec = {"organism": self.label, "version": self.version, "parts": list(self.keys),
               "rod": "%s/%s" % self.rod, "task": task["id"],
               "precondition_unmet": self.unmet, "temperature": temperature}

        # SHAPE
        prompt = task["data"]
        if self.has("frame"):
            prompt = task["method"] + "\n\n" + prompt
        if self.has("goal"):
            prompt = (task["goal"] + "\n" + prompt) if not self.has("frame") else \
                     (task["method"] + "\n\n" + task["goal"] + "\n" + task["data"])
        rec["prompt_chars"] = len(prompt)

        # FIRE
        t0 = time.time()
        r = H.call_gated(self.rod[0], self.rod[1], [{"role": "user", "content": prompt}],
                         max_tokens=max_tokens, temperature=temperature)
        seen = OV.inspect(r, max_tokens=max_tokens, prompt=prompt)
        rec["flags"], rec["ok"] = seen["flags"], bool(r.get("ok"))
        text = seen["text"]
        rec["elapsed_s"] = round(time.time() - t0, 3)
        rec["tok_out"] = r.get("tokens")
        rec["raw"] = text[-320:]

        # READ
        answer, how = self._read(text)
        rec["answer"], rec["read_by"] = answer, how

        # JUDGE
        if self.has("measure"):
            rec["verdict"] = ("pass" if answer == task["truth"] else
                              ("abstain" if answer is None else "fail"))
            # A VERDICT WITH NO GOAL IS `Arbiter vacui`: it judges an answer to a question nobody asked.
            rec["verdict_is_empty"] = not (self.has("goal") or self.has("frame"))
        else:
            rec["verdict"] = None          # the organism cannot know whether it worked
            rec["verdict_is_empty"] = False
        if self.has("latency"):
            rec["clock"] = rec["elapsed_s"]
        return rec

    def _read(self, text):
        nums = re.findall(r"(?<![\d.])(-?\d{1,5})(?![\d.])", (text or "").replace(",", ""))
        stated = int(nums[-1]) if nums else None
        if self.has("validation"):
            # STRICT: commit only where the reply commits. Abstain rather than guess.
            t = (text or "").strip()
            bare = re.fullmatch(r"[^\d]{0,24}?(-?\d{1,5})[^\d]{0,24}", t)
            if bare:
                stated = int(bare.group(1))
            elif len(set(nums)) != 1:
                m = re.search(r"(?:answer|result|total|is)\D{0,12}(-?\d{1,5})\s*$", t, re.I)
                stated = int(m.group(1)) if m else None
        if stated is not None:
            return stated, "stated"
        if self.has("readout"):
            idx = [int(m.group(1)) for m in _ENUM.finditer(text or "")]
            if idx:
                return max(idx), "work"
        return None, "none"


# --- THE THREE FAMILIES ----------------------------------------------------------------------------

def ascending(order=None):
    """v1..vN. Each is everything before it plus one component. The spine."""
    keys = list(order or [c.key for c in CATALOGUE])
    return [(i + 1, keys[:i + 1]) for i in range(len(keys))]


def toxic(order=None):
    """Assemblies with a component whose precondition is absent. They run and return something."""
    keys = list(order or [c.key for c in CATALOGUE])
    out = []
    for c in CATALOGUE:
        if not c.requires:
            continue
        for r in c.requires:
            if r == "call":
                continue                    # nothing runs without a call; that is not toxic, it is void
            asm = [k for k in keys if k in ("call", c.key)]
            out.append(("%s without %s" % (c.key, r), asm))
    return out


def oblique(order=None):
    """Assemblies that SKIP a rung and may work anyway. Each is a candidate counterexample to C-63."""
    return [
        ("frame without measure", ["call", "goal", "frame"]),
        ("frame+readout without measure", ["call", "goal", "frame", "readout"]),
        ("clock alone", ["call", "latency"]),
        ("procedure without goal", ["call", "frame"]),
    ]


if __name__ == "__main__":
    print("THE ASCENDING SERIES, from the catalogue this walk has measured\n")
    print("%-5s %-46s %s" % ("ver", "components", "what it can newly do"))
    for v, keys in ascending():
        c = BY_KEY[keys[-1]]
        print("%-5s %-46s %s" % ("v%d" % v, "+".join(keys), c.name))
    print("\nTOXIC assemblies (a precondition is absent, and it still runs)\n")
    for name, keys in toxic():
        o = Organism(keys, ("nvidia", "x"), label=name)
        print("  %-30s %-26s unmet: %s" % (name, "+".join(keys), o.unmet))
    print("\nOBLIQUE assemblies (skip a rung, may work anyway: candidate C-63 counterexamples)\n")
    for name, keys in oblique():
        o = Organism(keys, ("nvidia", "x"), label=name)
        print("  %-32s %-34s unmet: %s" % (name, "+".join(keys), o.unmet or "none"))
