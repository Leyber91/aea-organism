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
    return receipt(bench_core.run_status, run_id)
