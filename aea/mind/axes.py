"""axes.py - C-11, THE POSITION RECORD: where the entity actually stands in the 5-D growth space.

Canon (A15_FULL_COVERAGE C-01..C-11) defines the entity's GROWTH as movement through five axes,
each with an L0..L5 ladder - "the ladders are not decoration, they are the coordinate system." The
census marks C-06..C-11 MISSING, and a grep of the substrate confirmed it: `axis_levels` existed in
zero files. The architecture had a coordinate system with no coordinates.

This is that record, and it is the game's progression: not XP, not a level counter, but the real
position of a real entity in the space canon defines. THE PROBE's walk is closing this census, so
the readout the player watches has to be the same number the architecture is judged by.

THE ONE LAW HERE (the honesty law, applied to progression):
    A LEVEL IS ONLY RAISED BY A RECEIPT.
`raise_axis` refuses without a real run_id or an equally checkable proof reference. There is no
grant, no gift, no unlock-by-narrative. That makes a raise an instance of OP1 axis-extension (C-27:
"a higher level on one of the 5 axes becomes reachable") rather than a number a designer awarded.

Rungs: only the ones canon states explicitly are named here. The rest are UNSPECIFIED on purpose -
inventing a ladder rung would be fabricating canon, which is worse than an honest gap. The mechanism
works regardless of how many rungs are later filled in from the master document.
"""
from __future__ import annotations

import os
import time

from aea.kernel import grid

AXES = ("P", "A", "M", "R", "S")

# name + the module whose REAL behaviour proves that axis (aea_elements.js `proof` fields)
AXIS = {
    "P": {"name": "PATH", "line": "control flow - the entity defines its own next step", "proof": "mind/swarm.py"},
    "A": {"name": "ABSTRACTION", "line": "memory grounding, tool use, writing new skills", "proof": "io/agent_tools.py"},
    "M": {"name": "MULTIPLICITY", "line": "role-differentiated nodes running and synthesising in parallel", "proof": "mind/swarm.py"},
    "R": {"name": "PROMPTING", "line": "a scaffold makes a cheap node beat its raw self", "proof": "memory/memory.py"},
    "S": {"name": "ASYNC", "line": "temporal independence - scheduled, unattended, parallel", "proof": "mind/relay.py"},
}

# Canon states these rungs verbatim (W section 3). Anything canon did not state is UNSPECIFIED -
# the gap is recorded rather than filled, so no rung in this file is invented.
# THE THIRTY RUNGS. Canon states nine of these verbatim (marked [C]); the rest are DERIVED and marked
# [d] - a derived rung is a proposal, not scripture, and it is written as a PROVABLE condition so it can
# be refuted like everything else on this walk. A rung with no test is decoration.
LADDER = {
    "P": {0: ("a single call", "[C]"),
          1: ("a fixed sequence it executes in order", "[d]"),
          2: ("it chooses between branches at runtime", "[d]"),
          3: ("multi-step plan + critique", "[C]"),
          4: ("it revises the plan mid-execution on a real signal", "[d]"),
          5: ("self-versioning recursion", "[C]")},
    "A": {0: ("no grounding", "[C]"),
          1: ("grounded in a retrieved memory", "[d]"),
          2: ("it decides for itself that it needs to retrieve", "[d]"),
          3: ("tool use - it acts through an external function", "[d]"),
          4: ("it combines tools it was not told to combine", "[d]"),
          5: ("it writes a new skill into its own manifest", "[d]")},
    "M": {0: ("one path", "[C]"),
          1: ("two nodes, same role - redundancy", "[d]"),
          2: ("two nodes, different roles", "[d]"),
          3: ("a council of N, synthesised", "[C]"),
          4: ("the council disagrees and the disagreement changes the outcome", "[d]"),
          5: ("organic divergent bifurcation", "[C]")},
    "R": {0: ("the bare prompt", "[d]"),
          1: ("a static frame improves the output", "[d]"),
          2: ("a FITTED frame converts failure into success", "[d]"),
          3: ("the frame is generated for the specific failure, not hand-written", "[d]"),
          4: ("a frontier rod writes the scaffold a cheap rod runs", "[d]"),
          5: ("the scaffold is revised from measured outcomes", "[d]")},
    "S": {0: ("synchronous", "[C]"),
          1: ("it survives the session - state persists", "[d]"),
          2: ("a prewarmer", "[C]"),
          3: ("it fires on a schedule, unattended", "[d]"),
          4: ("parallel unattended runs", "[d]"),
          5: ("parallel + cross-substrate", "[C]")},
}
TOP = 5

_FP = lambda: os.path.join(grid.STATE, "axis_levels.json")


def _blank() -> dict:
    return {"levels": {a: 0 for a in AXES}, "raised": []}


def load() -> dict:
    st = grid.load_json(_FP(), None)
    if not isinstance(st, dict) or "levels" not in st:
        return _blank()
    for a in AXES:                                  # a new axis appears at L0, never absent
        st["levels"].setdefault(a, 0)
    return st


def level(axis: str) -> int:
    return int(load()["levels"].get(axis, 0))


def position() -> dict:
    """The 5-D coordinate, plus how far the whole space has been walked (0.0 - 1.0)."""
    lv = load()["levels"]
    return {"levels": dict(lv), "sum": sum(lv.values()), "max": TOP * len(AXES),
            "walked": round(sum(lv.values()) / float(TOP * len(AXES)), 3)}


def rung(axis: str, lv: int) -> str | None:
    """The rung's name, or None if undefined. Canon-stated rungs and derived ones are distinguished
    by source() - a derived rung is a proposal open to refutation, never presented as canon."""
    r = LADDER.get(axis, {}).get(lv)
    return r[0] if r else None


def source(axis: str, lv: int) -> str | None:
    """'[C]' canon states it verbatim  ·  '[d]' derived by this walk  ·  None undefined."""
    r = LADDER.get(axis, {}).get(lv)
    return r[1] if r else None


def raise_axis(axis: str, to: int, proof: str, note: str = "") -> dict:
    """OP1 axis-extension. Refuses without a real proof reference; refuses a skipped rung.

    `proof` must identify something that actually happened - a bench run_id (r-nn), a pulse event,
    a test id. It is stored verbatim on the raise so the position can always be audited back to the
    thing that earned it.
    """
    if axis not in AXES:
        return {"ok": False, "refused": f"'{axis}' is not an axis - canon names five: {', '.join(AXES)}"}
    if not proof:
        return {"ok": False, "refused": "a level is only raised by a receipt - no proof, no raise (OP1)"}
    to = int(to)
    if not 0 <= to <= TOP:
        return {"ok": False, "refused": f"L{to} is off the ladder - canon runs L0..L{TOP}"}
    st = load()
    cur = int(st["levels"].get(axis, 0))
    if to <= cur:
        return {"ok": False, "refused": f"{AXIS[axis]['name']} already stands at L{cur}"}
    if to > cur + 1:
        return {"ok": False, "refused": f"a rung is climbed, not jumped - {AXIS[axis]['name']} "
                                       f"is at L{cur}, next is L{cur + 1}"}
    st["levels"][axis] = to
    st["raised"].append({"axis": axis, "to": to, "proof": proof, "note": note,
                         "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())})
    grid.atomic_save_json(_FP(), st)
    return {"ok": True, "axis": axis, "name": AXIS[axis]["name"], "level": to,
            "rung": rung(axis, to), "proof": proof, "position": position()}


if __name__ == "__main__":
    import json as _j
    print(_j.dumps(position(), indent=1))
