"""Read a run's capacities off its trace, against the definitions sealed in catalogue.json.

Lived in x22 until 2026-07-27, which made it unfalsifiable: a capacity chosen after seeing what a
module did is a capacity every module delivers. The definitions are data; this is only the reader.
"""
from __future__ import annotations

from aea.lab.parts.base import load_catalogue

_FIELD = {
    "answered": lambda s: s.get("value") is not None,
    "on_task": lambda s: bool(s.get("on_task")),
    "shows_working": lambda s: bool(s.get("showed_work")),
    "recoverable": lambda s: bool(s.get("from_work")),
    "can_abstain": lambda s: bool(s.get("declined")),
    "revised": lambda s: bool(s.get("repaired")),
    "held": lambda s: bool(s.get("hit")),
}


def names(doc=None):
    return list((doc or load_catalogue()).get("capacities", {}))


def of(rec, doc=None):
    """Rates over the completed steps of one sequence. Only capacities the trace can witness."""
    t = [s for s in rec.get("trace", []) if s.get("ok")]
    if not t:
        return {}
    return {k: sum(1 for s in t if f(s)) / len(t)
            for k, f in _FIELD.items() if k in names(doc)}


def gained(before, after, band=0.10):
    return {k: round(v - before.get(k, 0.0), 3) for k, v in after.items()
            if v - before.get(k, 0.0) >= band}


def lost(before, after, band=0.10):
    """THE ADDITION LAW: any capacity that drops by more than the band when a part is added."""
    return {k: round(v - before.get(k, 0.0), 3) for k, v in after.items()
            if v - before.get(k, 0.0) <= -band}
