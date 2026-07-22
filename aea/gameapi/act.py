"""aea.gameapi.act - the /game/* POST handlers: allowlisted acts, each a receipt.

compose -> IGNITE -> run-or-fail. Wraps bench_core.start_run (THE BENCH - the ONE execution
engine; never duplicated). A malformed body is refused BEFORE any metered draw (the crash-rider
guard); a live run refuses a second ignite loudly, it never queues. First light guards the
awe-beat on the UNLIMITED local hearth: the opening construct's task pins tier 'local' (ollama).
"""
from __future__ import annotations

from typing import Optional

from .honesty import receipt


def ignite(req: dict, bad_body: Optional[str] = None) -> dict:
    """/game/ignite {spec, task} -> {ok: True, run_id, ...} | {ok: False, refused: '<clause>'}.

    req: {spec?: construct spec v0.1.0, task?: task id}. Defaults (empty req) to the opening
    construct (TAP + SCORER) on the one curated task t-01, which fires on the local hearth. The
    run executes in its own thread and returns a run_id instantly; poll /game/run?id= for the trace.
    """
    if bad_body:  # a malformed packet must never spend a metered draw (crash rider 2026-07-20)
        return {"ok": False, "refused": f"{bad_body} - a malformed packet never fires; "
                                        "the bench refuses loudly and spends nothing"}
    from aea.bench import bench_core
    return receipt(bench_core.start_run, req)
