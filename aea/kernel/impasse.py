"""impasse.py - THE ENTITY NOTICING IT IS STUCK, AND SAYING WHY.

THE FAILURE THIS EXISTS FOR. `produce_brief` failed thirty consecutive wakes across eighteen days.
Every failure was byte-identical: `hades=unverified sections_ok=False`. The entity woke on schedule,
did the work, failed the same way, recorded it, and woke again. It never noticed that thirty
failures were ONE failure repeated thirty times. A human read the ledger and found the cause in
about a minute.

BEING STUCK IS NOT THE SAME AS FAILING OFTEN, and the difference is the whole file. A capability
that fails for a different reason each time is UNRELIABLE - it is trying things and they are not
working. A capability that fails for the SAME reason every time is STUCK - repeating the attempt
cannot help, and only changing something can. Those two states need opposite responses and the
ledger could not tell them apart.

WHY THIS IS THE RUNG UNDER CRYSTALLIZATION. SOAR named the trigger in 1986 and the 2026 skill-
induction literature has converged back on it: do not crystallize on success, crystallize on a
RESOLVED IMPASSE. A thing worth keeping forever is a thing that got you unstuck. So the system must
be able to see an impasse before it can ever learn from leaving one. This is step 2 of five:

    1 NOTICE       trust.record counts consecutive failures and alarms      built
    2 DIAGNOSE     same failure repeated, or many different ones            this file
    3 VARY         when stuck, change something instead of repeating
    4 RECORD       keep what was varied and whether it worked
    5 CRYSTALLIZE  the resolution becomes a reusable part

THE SIGNATURE IS THE MECHANISM. A history line carries a timestamp, an outcome and a note. The
timestamp is what makes every line unique, so it is stripped; what remains is the SHAPE of the
failure. Numbers inside the note are stripped too, because `x3` and `x17` are the same failure
counted twice. What survives is the reason.

  python -m aea.kernel.impasse          read the live ledger and report
"""
from __future__ import annotations

import re
from collections import Counter

from aea.kernel import grid, trust

STUCK_AT = 3          # identical consecutive failures before it counts as an impasse
_TS = re.compile(r"^\s*\d{4}-\d{2}-\d{2} \d{2}:\d{2}\s*")
_NUM = re.compile(r"\b[xX]?\d+\b")
_LVL = re.compile(r"->\s*(FORBIDDEN|DRAFT|WATCHED|TRUSTED)\s*")


def signature(line: str) -> str:
    """What a failure IS, with everything that makes one instance unique removed.

    Strips the timestamp (unique per line by construction), the failure counter (`x3` is not a
    different failure from `x17`) and the resulting level (a demotion changes the level while the
    cause stays the same). What is left is the reason, and two lines with the same reason are the
    same failure however far apart they happened.
    """
    s = _TS.sub("", line or "")
    s = _LVL.sub("-> ", s)
    s = _NUM.sub("N", s)
    return " ".join(s.split()).lower()


def read(cap: str, state: dict | None = None) -> dict:
    """Is this capability stuck, unreliable, or working? Answered from its own record."""
    st = state or grid.load_json(trust.LEDGER, {})
    e = st.get(cap) or {}
    hist = list(e.get("history") or [])
    fails = [h for h in hist if "FAIL" in str(h)]

    # THE TAIL IS WHAT MATTERS. A capability that failed ten times last week and has been clean
    # since is not stuck; it recovered. Only the unbroken run of failures at the END counts.
    tail = []
    for h in reversed(hist):
        if "FAIL" not in str(h):
            break
        tail.append(str(h))
    tail.reverse()

    sigs = [signature(h) for h in tail]
    counts = Counter(sigs)
    top, n_top = (counts.most_common(1)[0] if counts else ("", 0))
    distinct = len(counts)

    if not tail:
        verdict, why = "working", "no unbroken run of failures at the end of the record"
    elif n_top >= STUCK_AT and distinct == 1:
        verdict, why = "stuck", ("the last %d failures are ONE failure repeated; repeating the "
                                 "attempt cannot help" % n_top)
    elif n_top >= STUCK_AT:
        verdict, why = "stuck", ("%d of the last %d failures share one cause; the rest are noise "
                                 "around it" % (n_top, len(tail)))
    elif len(tail) >= STUCK_AT:
        verdict, why = "unreliable", ("%d consecutive failures with %d different causes - it is "
                                      "trying things and they are not working" % (len(tail), distinct))
    else:
        verdict, why = "failing", "%d consecutive failures, below the impasse floor" % len(tail)

    return {"capability": cap, "verdict": verdict, "why": why,
            "consecutive_failures": len(tail), "distinct_causes": distinct,
            "dominant_signature": top, "dominant_count": n_top,
            "level": trust.LEVEL_NAMES.get(e.get("level"), "?"),
            "total_runs": e.get("runs"), "total_fails": e.get("fails"),
            "stuck": verdict == "stuck",
            "evidence": tail[-3:]}


def scan(state: dict | None = None) -> list:
    st = state or grid.load_json(trust.LEDGER, {})
    return [read(cap, st) for cap in trust.CHARTER if cap in st]


def render(rows=None) -> str:
    rows = rows if rows is not None else scan()
    L = ["IMPASSE SCAN - stuck is not the same as failing often", "=" * 78,
         "%-22s %-11s %-6s %-8s %s" % ("capability", "verdict", "fails", "causes", "level")]
    for r in rows:
        L.append("%-22s %-11s %-6s %-8s %s"
                 % (r["capability"], r["verdict"], r["consecutive_failures"],
                    r["distinct_causes"] or "-", r["level"]))
    stuck = [r for r in rows if r["stuck"]]
    L.append("")
    if stuck:
        for r in stuck:
            L.append("STUCK: %s" % r["capability"])
            L.append("  %s" % r["why"])
            L.append("  the repeated cause: %s" % (r["dominant_signature"] or "-")[:150])
            L.append("  changing something is the only move that can help.")
    else:
        L.append("Nothing is stuck. No capability is repeating one failure.")
    return "\n".join(L)


if __name__ == "__main__":
    print(render())
