"""aea.gameapi.honesty - THE FIREWALL. The single boundary where the honesty law is enforced.

One rule, one place: a /game/* reply is ALWAYS a receipt - a dict the server sends as HTTP 200 +
JSON - never an exception across the wire, never a fabricated value. Absent stays absent (an organ
returning None flows through untouched; the client renders a dash, never a guess). A refusal keeps
its clause verbatim. The claim ceiling holds: this layer asserts nothing about the entity's inner
life; it only relays what the organs measured.
"""
from __future__ import annotations

from typing import Callable


def receipt(fn: Callable[..., object], *args, **kwargs) -> dict:
    """Run an organ call and guarantee a dict receipt.

    The organ's own contract passes through untouched - {ok: True, ...}, {ok: False, refused: ...},
    {ok: False, error: ...}. Only an UNEXPECTED raise is converted here, so the socket never 500s
    and the plate never hangs on a torn response (the /autonomy + bench never-500 idiom, made a law).
    """
    try:
        out = fn(*args, **kwargs)
    except Exception as e:  # never-500: the refusal contract holds even if an organ raises
        return {"ok": False, "error": str(e)[:160]}
    if isinstance(out, dict):
        return out
    return {"ok": True, "data": out}
