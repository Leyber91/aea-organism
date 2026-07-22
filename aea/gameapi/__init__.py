"""aea.gameapi - THE HONEST SEAM (first light).

The ONE curated /game/* facade over the REAL organs. The honesty law lives here, structurally:
absent -> null -> a dash (rendered client-side); a refusal -> {ok: false, refused: '<clause>'};
every reply is a RECEIPT (HTTP 200 + JSON body), never an exception across the wire, never a
fabricated value. It IMPORTS the preserved organs (bench_core, controlroom.state); it never
reimplements them.

Mounted by aea.server.controlroom: `route_get` / `route_post` return a JSON-able dict for a
recognised /game/* endpoint, or None to fall through (so /game/<static-asset> still serves files).
The seam adds NO new HTTP server at first light - it rides the control room's 127.0.0.1:7799.
"""
from __future__ import annotations

from typing import Optional

from . import read, act

__all__ = ["route_get", "route_post"]


def route_get(path: str) -> Optional[dict]:
    """A /game/* GET -> a receipt dict, or None if this is not a game-API path (fall through to
    the scoped static server so /game/js/... still loads)."""
    p = path.split("?", 1)[0]
    if p == "/game/state":
        return read.state()
    if p == "/game/run":
        qid = ""
        if "id=" in path:
            qid = path.split("id=", 1)[1].split("&", 1)[0]
        return read.run(qid)
    return None


def route_post(path: str, req: dict, bad_body: Optional[str] = None) -> Optional[dict]:
    """A /game/* POST -> a receipt dict, or None if this is not a game act path."""
    if path == "/game/ignite":
        return act.ignite(req, bad_body)
    return None
