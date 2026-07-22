"""aea.gameapi.read - the /game/* GET handlers: pure reads, re-homed to the REAL organ functions.

Never reimplements an organ - it calls the same functions the control room already exposes, behind
the honesty firewall. Imports are lazy (inside the handlers) so the seam can be mounted from
controlroom without an import cycle (controlroom imports gameapi; gameapi reads controlroom.state).
"""
from __future__ import annotations

from .honesty import receipt


def state() -> dict:
    """/game/state - the folded live snapshot (identity / life / energy / trust / brief).

    Wraps controlroom.state(): every value is read from the same files the entity writes; an absent
    field stays None and the client renders a dash, never a guess.
    """
    from aea.server import controlroom  # lazy: avoid the controlroom <-> gameapi import cycle
    return receipt(controlroom.state)


def run(run_id: str) -> dict:
    """/game/run?id= - the persisted run trace (links / axes / receipt / pass) for one ignition.

    Wraps bench_core.run_status(): reads bench_runs.json fresh every call (the file is the truth).
    status 'halted' is the visible blue fail; 'lost' is a carrier-lost receipt. Missing id -> a
    receipt naming the requirement, never a crash.
    """
    from aea.bench import bench_core
    from aea.kernel import grid

    def _run():
        out = bench_core.run_status(run_id)
        if isinstance(out, dict) and out.get("links"):
            # cost_u = REAL metered requests this run spent. A keyless-unlimited plant (the local
            # hearth) is genuinely free -> 0; a rate-capped plant costs 1 against a real budget.
            # Never a fabricated stake on a free draw (the honesty law over the game's want).
            cost = 0
            for link in out["links"]:
                rc = link.get("receipt")
                plant = rc.get("plant") if isinstance(rc, dict) else None
                p = grid.PLANTS.get(plant or "", {})
                if plant and (p.get("rpm") is not None or p.get("rpd") is not None):
                    cost += 1
            out["cost_u"] = cost
        return out
    return receipt(_run)


def events(since: float = 0.0) -> dict:
    """/game/events?since= - the live nervous signal (pulse), one real row per emitted event.

    Wraps pulse.tail(): the real event stream the entity writes as it acts. One conduit particle
    per real row - never a decorative one. Returns {ok, events:[...]}.
    """
    from aea.kernel import pulse

    def _tail():
        return {"ok": True, "events": pulse.tail(since)}
    return receipt(_tail)
