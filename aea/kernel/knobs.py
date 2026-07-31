"""knobs.py - THE DECLARED SURFACE THE ENTITY MAY TURN. Data naming a declared operation, never code.

    python -m aea.kernel.knobs             # the board: every knob, its bounds, its current value
    python -m aea.kernel.knobs --reset      # back to declared defaults

THE GAP THIS CLOSES, AND IT WAS THE ONE MAKING R3 INERT. `unstick.propose` has correctly returned
`{"move": "raise_budget", "knob": "max_tokens", "to": 900}` for weeks. `crystal` can admit a move
that works. `outcomes` can record whether it worked. And NOTHING COULD APPLY ONE, because every
budget in the tree is a literal at a call site - `brief.py` alone carries `mx=400`, `mx=300`,
`mx=700`, `mx=320`. An organ that cannot READ a knob makes the whole loop unable to close:
`worked` is never true, so `harvest` never admits, so `applicable` is always empty, so the library
stays at 40 bytes while every function reports reachable.

`_apply_knob` returned False on purpose rather than writing a value nobody reads - because
`applied=True` with no reader is a FALSE OUTCOME RECORD, R3's own hazard, produced by R3's own loop.
This module is the reader, so the write can start meaning something.

THE LAW IT OBEYS (S5, design/THE_LAWS.md): *a declaration names a registered operation with
parameters. Never code.* A knob is a NAME from the table below plus a NUMBER inside declared
bounds. There is no expression, no callable, no import, and nothing here is ever `eval`ed. The named
failure path is a declaration that grows `when:`, then `loop:`, then `rescue:` until it is a
programming language nobody designed - so the schema is frozen by a test asserting a literal
key-set, and adding a key has to break that test on purpose.

WHY BOUNDS ARE PART OF THE DECLARATION AND NOT A POLICY. A knob without a range is an unbounded
write with a friendly name: `max_tokens = 10_000_000` is not a different KIND of change from
`max_tokens = 900`, it is the same operation aimed off a cliff. `lo`/`hi` are declared beside the
default, `set()` clamps and says it clamped, and a value outside them is refused rather than
silently truncated.

WHAT A KNOB MAY NEVER BE. Nothing here may name a trust level, a ceiling, a zone, a charter row or
a capability. That is `unstick.INVARIANTS`, enforced there before a move is offered and again after
it is applied; this table simply contains no such entry, so the two guards agree by construction
rather than by coordination.
"""
from __future__ import annotations

import os
import sys
import time

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STORE = "knobs.json"
# BOUNDED. Every set() appends a row INCLUDING refusals, and refusals are the common case - the
# entity proposes five knob moves and only one is declared, so a daemon ticking every 30 minutes
# writes a refusal row roughly every tick, forever. An append-only store with no trim on the path
# that fires most often is unbounded growth wearing an audit trail's clothes. The trust ledger and
# the experience record both trim; this did not.
HISTORY_KEEP = 400


def _path() -> str:
    """RESOLVED AT CALL TIME so a harness can be sandboxed - D48, and it bit again here.

    `test_knobs` exercises the clamp by setting `hi * 100`, which persisted 32000 into the
    PRODUCTION store and left the brief capped there. The test then "restored the pre-test value",
    which on the next run was already the polluted one - so it passed in isolation, failed in a
    sweep, and quietly held a real ceiling on the live organ in between. A store bound to
    `grid.STATE` at import cannot be redirected, which is the same shape that put 4,920 synthetic
    rows in the hands ledger, arriving in code written the same day as the fix for it."""
    return os.environ.get("AEA_KNOBS") or os.path.join(str(grid.STATE), STORE)

# THE FROZEN SCHEMA. Exactly these keys describe a knob, and `test_knobs` asserts this literal so
# that adding `when:` or `unless:` breaks a test deliberately rather than arriving one reasonable
# key at a time. See S5's named failure path.
KNOB_KEYS = ("default", "lo", "hi", "unit", "desc")

# EVERY KNOB THAT EXISTS. A knob absent from this table cannot be read and cannot be set - an
# undeclared knob is not a knob, it is a typo with a value attached.
KNOBS = {
    # DEFAULT None MEANS OMIT THE FIELD - no ceiling, the rod's own published maximum applies.
    #
    # THE FIRST VERSION OF THIS TABLE SAID 300, AND THAT WAS THE DEFECT WEARING THE FIX'S CLOTHES.
    # I lifted the literal out of `brief.py` and wrote it here as the "declared default", which
    # re-invented the exact ceiling the knob existed to remove - now blessed by a registry and
    # therefore harder to see. A number nobody chose does not become chosen by being written down
    # somewhere tidier. The honest default for a budget is NO BUDGET.
    #
    # `lo`/`hi` still bound what may be SET, because a knob the entity can turn needs a range; but
    # the resting state is no ceiling at all.
    ("produce_brief", "max_tokens"): dict(
        default=None, lo=120, hi=32000, unit="tokens",
        desc="budget for the PRIVATE synthesis calls in brief.py. None = omit the field entirely. "
             "The impasse this exists for: a reasoning rod spends its budget thinking and emits "
             "content only afterwards, so at 300 it answers correctly and returns an empty string."),
    ("produce_brief", "public_max_tokens"): dict(
        default=None, lo=120, hi=32000, unit="tokens",
        desc="budget for the PUBLIC gather calls in brief.py. None = omit the field entirely."),
    ("produce_brief", "depth"): dict(
        default=3, lo=1, hi=5, unit="steps",
        desc="how many reasoning steps the private synthesis is given"),
}


class UndeclaredKnob(KeyError):
    """A knob that is not in the table. Refused, and named - never created on demand."""


def _load() -> dict:
    return grid.load_json(_path(), {"schema": "aea.knobs/1", "values": {}, "history": []})


def _save(doc: dict) -> None:
    """Trim, then persist. ONE place, because the first version of this trim was injected at each
    of the five save sites and landed at the wrong indentation in three of them - the module would
    not import. The trim belongs where the write happens, not where the caller happens to be."""
    h = doc.get("history") or []
    if len(h) > HISTORY_KEEP:
        doc["history"] = h[-HISTORY_KEEP:]
    grid.atomic_save_json(_path(), doc, indent=1)


def _key(cap: str, knob: str) -> str:
    return f"{cap}.{knob}"


def declared(cap: str, knob: str) -> dict:
    spec = KNOBS.get((cap, knob))
    if spec is None:
        raise UndeclaredKnob(
            f"{_key(cap, knob)} is not a declared knob. Add it to KNOBS deliberately, with bounds "
            f"and a reason, or the entity is turning something nobody designed to be turned.")
    return spec


def get(cap: str, knob: str, fallback=None):
    """The value an organ should use RIGHT NOW. Falls back to the declared default, then to the
    caller's literal - so an absent or unreadable store can never stop an organ running."""
    try:
        spec = declared(cap, knob)
    except UndeclaredKnob:
        return fallback
    try:
        v = (_load().get("values") or {}).get(_key(cap, knob))
    except Exception:
        v = None
    if v is None:
        # NO STORED VALUE -> the declared default, which may itself be None meaning "no ceiling".
        # `fallback` is only consulted when the knob is undeclared; a declared None is an ANSWER,
        # not an absence, and treating it as one would quietly restore a caller's old literal.
        return spec["default"]
    kind = type(spec["default"]) if spec["default"] is not None else int
    try:
        v = kind(v)
    except Exception:
        return spec["default"]
    return max(spec["lo"], min(spec["hi"], v))


def set(cap: str, knob: str, to, why: str = "", by: str = "unattributed") -> dict:
    """Turn a knob. Returns {ok, key, from, to, clamped, why} and NEVER raises on a bad value.

    A REFUSAL IS A RESULT, NOT AN EXCEPTION, because the caller is a tick that must keep breathing.
    Every attempt is appended to `history` including the refused ones - a knob that was refused and
    a knob that was never tried look identical otherwise, which is the null-looks-like-real shape
    that has cost more than anything else in this repo."""
    doc = _load()
    k = _key(cap, knob)
    row = dict(at=time.time(), at_iso=time.strftime("%Y-%m-%d %H:%M:%S"), key=k, by=by,
               requested=to, why=str(why)[:160])
    try:
        spec = declared(cap, knob)
    except UndeclaredKnob as e:
        row.update(ok=False, refused=str(e)[:200])
        doc.setdefault("history", []).append(row)
        _save(doc)
        return dict(ok=False, key=k, refused=str(e)[:200])
    # None CLEARS THE KNOB, returning it to its declared default - which for a budget is NO CEILING.
    #
    # WITHOUT THIS THE KNOB IS A ONE-WAY RATCHET. `set` coerced through `int`, so `set(..., None)`
    # raised and was refused: the entity could RAISE a budget and never REMOVE one, and every knob
    # drifted permanently toward having a limit. That is the defect this whole module exists to
    # undo, rebuilt as a property of the module itself. Caught by the test's own restore step
    # failing once the default became None.
    if to is None:
        was = (doc.get("values") or {}).get(k, spec["default"])
        doc.setdefault("values", {}).pop(k, None)
        row.update(ok=True, **{"from": was}, to=spec["default"], clamped=False, cleared=True)
        doc.setdefault("history", []).append(row)
        _save(doc)
        return dict(ok=True, key=k, **{"from": was}, to=spec["default"], clamped=False, cleared=True)
    kind = type(spec["default"]) if spec["default"] is not None else int
    try:
        val = kind(to)
    except Exception:
        row.update(ok=False, refused=f"{to!r} is not a {type(spec['default']).__name__}")
        doc.setdefault("history", []).append(row)
        _save(doc)
        return dict(ok=False, key=k, refused=row["refused"])
    clamped = max(spec["lo"], min(spec["hi"], val))
    was = (doc.get("values") or {}).get(k, spec["default"])
    doc.setdefault("values", {})[k] = clamped
    row.update(ok=True, **{"from": was}, to=clamped, clamped=(clamped != val))
    doc.setdefault("history", []).append(row)
    _save(doc)
    return dict(ok=True, key=k, **{"from": was}, to=clamped, clamped=(clamped != val))


def board() -> str:
    doc = _load()
    vals = doc.get("values") or {}
    L = ["KNOBS - the declared surface the entity may turn", "=" * 88,
         "%-34s %8s %8s %14s  %s" % ("knob", "value", "default", "bounds", "unit")]
    for (cap, knob), spec in sorted(KNOBS.items()):
        k = _key(cap, knob)
        cur = vals.get(k, spec["default"])
        mark = " " if cur == spec["default"] else "*"
        L.append("%-34s %8s %8s %14s  %s%s"
                 % (k, cur, spec["default"], f"{spec['lo']}..{spec['hi']}", spec["unit"], mark))
    L.append("")
    L.append("* = turned away from its declared default")
    h = doc.get("history") or []
    L.append(f"{len(h)} recorded change attempt(s), refusals included")
    for r in h[-5:]:
        L.append("  %s %-26s %s -> %s  %s" % (r.get("at_iso", "")[5:16], r.get("key"),
                                              r.get("from", "-"), r.get("to", r.get("requested")),
                                              "" if r.get("ok") else "REFUSED"))
    return "\n".join(L)


if __name__ == "__main__":
    if "--reset" in sys.argv[1:]:
        d = _load()
        d["values"] = {}
        d.setdefault("history", []).append(
            dict(at=time.time(), at_iso=time.strftime("%Y-%m-%d %H:%M:%S"), key="*",
                 ok=True, why="reset to declared defaults", by="cli"))
        grid.atomic_save_json(_path(), d, indent=1)
        print("every knob returned to its declared default")
    print(board())
