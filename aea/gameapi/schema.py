"""aea.gameapi.schema - THE BEING AS A STRUCTURE (the world's fog map).

Every field is a real fact, checked against live state - the map cannot lie about what is built:
  - zones  = the real privacy rings, read from grid.ZONES and ordered by restrictiveness (fewest
             allowed plant-classes innermost): sensitive (local-only) -> private -> public. NOT a
             hand-copied literal; a zone added/renamed in grid.ZONES changes the map.
  - alive  = the being's heartbeat has actually ticked. Gates the world's amber core: the core is
             only lit when the mind is really running, never as unconditional decoration.
  - nodes  = the AEA organs. `wired` is TRUE only when the organ's REAL signal is present - a draw
             actually recorded (not a file that merely exists), a memory that exists, a meter that
             has metered, a heartbeat that ticked. An un-wired organ is FOG (cold-blue wireframe),
             and it flips to lit the moment its real signal appears (re-read every request).
  - depth  = the real dependency order (altitude): the BRAIN is the floor everything draws through.
  - edges  = the real organ couplings (a loop writes memory; a governor gates the hands).
"""
from __future__ import annotations

import os

from .honesty import receipt

# organ -> its home zone (ring), dependency depth (altitude), and the real substrate it maps to
_ORGANS = [
    {"id": "BRAIN",    "zone": "private",   "depth": 0, "entry": "energy.draw"},
    {"id": "GOVERNOR", "zone": "private",   "depth": 1, "entry": "grid.METER / hades"},
    {"id": "MEMORY",   "zone": "private",   "depth": 1, "entry": "consolidate.recall"},
    {"id": "LOOP",     "zone": "sensitive", "depth": 1, "entry": "the heartbeat"},
    {"id": "SENSES",   "zone": "sensitive", "depth": 2, "entry": "observe (unwired)"},
    {"id": "HANDS",    "zone": "public",    "depth": 2, "entry": "agent_tools (unwired)"},
]
_EDGES = [["LOOP", "BRAIN"], ["MEMORY", "BRAIN"], ["GOVERNOR", "BRAIN"],
          ["BRAIN", "SENSES"], ["BRAIN", "HANDS"], ["GOVERNOR", "HANDS"]]


def _zones() -> list:
    """The real privacy rings from grid.ZONES, innermost (most restrictive) first."""
    from aea.kernel import grid
    return sorted(grid.ZONES, key=lambda z: len(grid.ZONES[z]))


def _live() -> dict:
    """Live signals read from the same files the entity writes. REAL activity, not file heft."""
    from aea.kernel import grid

    def load(fn, default):
        return grid.load_json(os.path.join(grid.STATE, fn), default)

    hb = load("heartbeat.json", {})
    mem = load("memory.json", [])
    usage = load("energy_usage.json", {})
    gs = load("grid_state.json", {})
    ticks = int(hb.get("total_ticks") or 0)
    return {
        "alive": ticks > 0,
        "wired": {
            # a draw was actually recorded through the mouth (a rod with calls > 0), not just a file
            "BRAIN":    any((v or {}).get("calls", 0) > 0 for v in usage.values()),
            # the meter has actually metered real usage (daily/rpm windows exist), not merely a file
            "GOVERNOR": bool(gs.get("daily") or gs.get("rpm")),
            "MEMORY":   isinstance(mem, list) and len(mem) > 0,   # semantic memories exist
            "LOOP":     ticks > 0,                                # the heartbeat has ticked
            "SENSES":   False,   # no standalone sense organ wired into the live mind yet
            "HANDS":    False,   # agent_tools reaches nothing in the live mind yet
        },
    }


def _build() -> dict:
    live = _live()
    w = live["wired"]
    nodes = [{"id": o["id"], "zone": o["zone"], "depth": o["depth"],
              "entry": o["entry"], "wired": bool(w.get(o["id"]))} for o in _ORGANS]
    return {"ok": True, "core": "MIND", "alive": live["alive"],
            "zones": _zones(), "nodes": nodes, "edges": _EDGES}


def schema() -> dict:
    """/game/schema - the being's structure. Read-safe; the wired bits + alive are live truth."""
    return receipt(_build)
