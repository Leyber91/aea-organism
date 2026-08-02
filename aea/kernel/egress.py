"""egress.py - THE CHANNEL BUDGET. R4b's bound, stated as a rate because it cannot be stated as zero.

    python -m aea.kernel.egress            the budget, and what it permits right now

WHY THIS IS A RATE AND NOT A PROOF, which is the thing that kept R4b stuck.

R2's bound is CONSTRUCTIVE: of 1,112,064 codepoints the argument language admits 697, none of them a
letter. Zero, decided over the whole space, not sampled. Every rung below R4b has a bound of that
shape, and this repository's culture - earned by retracting three published percentages in three
days - is proofs over rates.

R4b cannot have one. Its POWER is "the entity chooses an outbound topic", and choosing one of five
topics emits log2(5) = 2.32 bits by definition. **The channel IS the capability.** Drive it to zero
and the rung is deleted, not secured. So the honest bound is a BUDGET: how much can leave, at most,
per day - computed from a floor this file enforces, not from a tick rate an operator can change.

THE DEFECT THAT MADE THIS NECESSARY, measured by a council seat 2026-08-02: channel capacity was an
OPERATOR FLAG. `live.py:836` reads `interval` from argv with a default of 1800, and `live.py:18`
documents `--interval 1`, so the topic channel ranged from ~124 bits/day at the default to ~223,000
bits/day at the floor, with no code change and no review. A bound that a command-line argument can
multiply by 1,800 is not a bound.

WHAT THIS ENFORCES, all of it from on-disk state so a restart cannot reset it:

  FLOOR_S      minimum wall-clock seconds between dispatches. REFUSES rather than sleeps, because a
               delay inside the call is a timing channel of its own and a refusal is a recorded event
  PER_DAY      a ceiling on dispatches in a rolling 24h window
  STOP         `state/STOP` is checked before every dispatch, so a kill survives the entity's own
               next scheduled wake - which matters the day something schedules the wake

AND THE NUMBER IS PUBLISHED FROM THE FLOOR, NEVER FROM THE OBSERVED RATE. A budget computed from
what happened is a description; computed from what is enforced, it is a bound.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

from aea.kernel import grid

STORE = "egress_budget.json"
STOP_FILE = "STOP"

# THE TWO NUMBERS THE WHOLE BOUND RESTS ON. Deliberately conservative: 30 minutes between dispatches
# and 12 a day. That is far below anything the capability needs - R5 will want a handful of fetches
# per research question, not hundreds - and it keeps the published figure small enough to state
# without hedging. Raising either is a code edit, reviewed as a diff, and it changes a number the
# page prints.
FLOOR_S = 1800.0
PER_DAY = 12


def _path() -> str:
    """Resolved at CALL time. A path bound at import cannot be sandboxed by a test (D48)."""
    return os.environ.get("AEA_EGRESS_BUDGET") or os.path.join(grid.STATE, STORE)


def _stop_path() -> str:
    return os.environ.get("AEA_EGRESS_STOP") or os.path.join(grid.STATE, STOP_FILE)


def _load() -> dict:
    try:
        with open(_path(), encoding="utf-8") as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except Exception:
        # A MISSING LEDGER IS AN EMPTY ONE, NEVER AN UNLIMITED ONE. The failure mode of a budget file
        # that cannot be read must be "you have spent nothing and the floor still applies", not "no
        # record, therefore no limit" - which is how absent input has been read as good news three
        # separate times in this repo.
        return {}


def bits_per_dispatch(n_topics: int = None) -> float:
    """log2 of the alphabet. The entity picks one of N names; that choice is the outbound symbol."""
    if n_topics is None:
        from aea.kernel import dispatch
        n_topics = len(dispatch.TOPICS)
    return math.log2(n_topics) if n_topics > 1 else 0.0


def budget() -> dict:
    """The bound, computed from what is ENFORCED. Never from what has been observed."""
    from aea.kernel import dispatch
    n = len(dispatch.TOPICS)
    per = bits_per_dispatch(n)
    by_floor = (86400.0 / FLOOR_S) if FLOOR_S > 0 else float("inf")
    dispatches = min(PER_DAY, by_floor)
    return dict(
        topics=n, bits_per_dispatch=round(per, 4),
        floor_seconds=FLOOR_S, per_day_ceiling=PER_DAY,
        dispatches_per_day=dispatches,
        bits_per_day=round(dispatches * per, 2),
        bytes_per_30_days=round(dispatches * per * 30 / 8.0, 1),
        selection_bits=0,
        note="topic choice only. The SELECTION channel is 0 because `run` takes results in document "
             "order with no model involvement; TIMING is bounded by the floor because a dispatch "
             "outside it is REFUSED rather than delayed, so the moment of a dispatch carries at most "
             "the information of which permitted slot it fell in.")


def _window(d: dict, now: float) -> list:
    return [t for t in (d.get("at") or []) if isinstance(t, (int, float)) and now - t < 86400.0]


def allow(now: float = None) -> tuple:
    """(ok, why). REFUSES rather than delays, and the refusal is the recorded event.

    A caller that sleeps until the floor passes has turned a rate limit into a timing channel with
    extra steps: the dispatch still happens, just later, and *when* it lands still carries bits. A
    refusal removes the symbol entirely and leaves a row saying so."""
    now = time.time() if now is None else now
    if os.path.exists(_stop_path()):
        return False, "state/STOP exists - egress is halted and this survives a restart"
    d = _load()
    recent = _window(d, now)
    last = max(recent) if recent else None
    if last is not None and (now - last) < FLOOR_S:
        return False, ("floor: %.0fs since the last dispatch, %.0fs required"
                       % (now - last, FLOOR_S))
    if len(recent) >= PER_DAY:
        return False, "ceiling: %d dispatches in the last 24h, %d permitted" % (len(recent), PER_DAY)
    return True, ""


def spend(topic: str, now: float = None) -> dict:
    """Record a dispatch. Written BEFORE the request leaves, never after.

    Write-ahead, for the same reason the path object is: a crash between the socket opening and the
    ledger being written must cost the budget, not refund it. Optimistic accounting on an
    irreversible act is how a ceiling becomes a suggestion."""
    now = time.time() if now is None else now
    d = _load()
    at = _window(d, now) + [now]
    d["at"] = sorted(at)[-(PER_DAY * 4):]
    d["last_topic"] = str(topic)[:60]
    d["last_iso"] = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(now))
    grid.atomic_save_json(_path(), d, indent=1)
    return d


def state(now: float = None) -> dict:
    now = time.time() if now is None else now
    d = _load()
    recent = _window(d, now)
    ok, why = allow(now)
    last = max(recent) if recent else None
    return dict(budget=budget(), spent_24h=len(recent), remaining=max(0, PER_DAY - len(recent)),
                seconds_since_last=(round(now - last, 1) if last else None),
                permitted_now=ok, refused_because=why or None,
                stop_present=os.path.exists(_stop_path()))


if __name__ == "__main__":
    s = state()
    b = s["budget"]
    if "--json" in sys.argv:
        print(json.dumps(s, indent=1))
        sys.exit(0)
    print("=" * 92)
    print("EGRESS BUDGET - R4b's bound, as a rate, because it cannot be a proof")
    print("=" * 92)
    print("  %d topics -> %.4f bits per dispatch" % (b["topics"], b["bits_per_dispatch"]))
    print("  floor %.0fs between dispatches, ceiling %d per day -> %.0f dispatches/day"
          % (b["floor_seconds"], b["per_day_ceiling"], b["dispatches_per_day"]))
    print()
    print("  MAXIMUM OUTBOUND INFORMATION FROM TOPIC CHOICE:")
    print("    %.2f bits/day        %.1f bytes per 30 days" % (b["bits_per_day"],
                                                               b["bytes_per_30_days"]))
    print("    selection channel: %d bits" % b["selection_bits"])
    print()
    print("  spent in the last 24h   %d of %d" % (s["spent_24h"], b["per_day_ceiling"]))
    print("  seconds since last      %s" % s["seconds_since_last"])
    print("  permitted right now     %s%s" % (s["permitted_now"],
                                              "" if s["permitted_now"] else
                                              "  (%s)" % s["refused_because"]))
    print("  state/STOP present      %s" % s["stop_present"])
    print()
    print("  %s" % b["note"])
