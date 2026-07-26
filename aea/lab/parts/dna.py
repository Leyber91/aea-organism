"""Read a creature's class off its wiring graph. The class is derived, never labelled.

  toxic   a CONFLICT edge fires        two modules, or a module and its fuel, fight
  inert   a REQUIRES edge is unmet     technically dead; seat the partner and it wakes
  feral   correct with an almost empty seat: the architecture is not necessary here
  healthy every requirement met, no conflict

These are the same edges x17 derived from the margins, read from the other side.
"""
from __future__ import annotations

from aea.lab.parts.base import Part, load_catalogue

FUEL_TRAITS = ("passes_bare",)


def _entry(doc, key):
    return next((c for c in doc["components"] if c["key"] == key), {})


def edges(seat, *, fuel_traits=(), config=None, doc=None):
    """Every edge the seat produces. `fuel_traits` are facts about the rod, e.g. passes_bare."""
    doc, config = doc or load_catalogue(), dict(config or {})
    have, out = set(seat), []
    for key in seat:
        e = _entry(doc, key)
        for r in e.get("requires", ()):
            out.append({"kind": "requires", "from": key, "to": r, "met": r in have})
        for c in e.get("conflicts", ()):
            w = c["with"]
            fires = (w in have) if not w.startswith("fuel:") else (w.split(":", 1)[1] in fuel_traits)
            out.append({"kind": "conflicts", "from": key, "to": w,
                        "fires": fires, "receipt": c.get("receipt")})
        v = config.get(key, {}).get("variant")
        if v and _entry(doc, key).get("variants", {}).get(v, {}).get("class") == "toxic":
            out.append({"kind": "conflicts", "from": "%s:%s" % (key, v), "to": "the task",
                        "fires": True,
                        "receipt": doc["components"][0] and e["variants"][v].get("receipt")})
    return out


def classify_seat(seat, *, fuel_traits=(), config=None, doc=None, correct=None, band=0.10):
    """The class, plus the edges that produced it. Never a bare label."""
    doc = doc or load_catalogue()
    es = edges(seat, fuel_traits=fuel_traits, config=config, doc=doc)
    firing = [e for e in es if e["kind"] == "conflicts" and e["fires"]]
    unmet = [e for e in es if e["kind"] == "requires" and not e["met"]]
    seated = [k for k in seat if k != "call"]
    if firing:
        cls, why = "toxic", firing
    elif unmet:
        cls, why = "inert", unmet
    elif len(seated) <= 1 and correct is not None and correct >= 1.0 - band:
        cls, why = "feral", [{"kind": "feral", "seat": list(seat), "correct": correct}]
    else:
        cls, why = "healthy", []
    return {"class": cls, "gloss": doc["classes"][cls], "because": why, "edges": es}
