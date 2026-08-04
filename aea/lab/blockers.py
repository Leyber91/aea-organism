"""blockers.py - WHAT CAN THE ENTITY NOT CHOOSE, AND WHY? The defect class, hunted on purpose.

    python -m aea.lab.blockers

FIVE INSTANCES OF ONE DEFECT WERE FOUND ON 2026-08-04, EVERY ONE BY ACCIDENT while doing something
else. That is luck, not a search, and the fifth cost a whole night of testing the wrong hypotheses:

    R1's original gate      asked for an action the wake's own surface could not express
    look_outward            built, wired, budgeted, certified - and no MOVE named it, so R4b's
                            condition 3 was unsatisfiable by construction
    check_a_belief          same defect again, same day, by an author who had just read that note
    the contradiction line  appended to a standing block already exactly at its 620-char cap and
                            silently truncated away - built, declared, never delivered
    check_a_belief's menu   rendered as "(no description - do not pick this)" for five hours,
                            because `decide.WHEN` had no entry and `_moves` fails closed

THE SHAPE IS ALWAYS THE SAME: the capability EXISTS, the code is CORRECT, the wiring is REACHABLE -
and something upstream stops it from ever being selected. Unit tests pass. `verify_funcs` reports
wired. The organ is present and dead, and nothing that reads the code can see it, because the code
is not what is wrong.

SO THIS ASKS THE ONE QUESTION THE OTHER INSTRUMENTS DO NOT: not "does it exist", not "can it be
reached", but **CAN IT BE CHOSEN, AND HAS IT EVER BEEN?** A move nothing has picked in 799 ticks is
either useless or blocked, and those two look identical from the inside.

SEVEN CHECKS, each one a way a capability can be present and unpickable:

    1  a TOOL no move can name              the look_outward defect
    2  a MOVE with no description           the check_a_belief defect - rendered "do not pick this"
    3  a MOVE with an empty enum            a closed set the reader cannot see is one they cannot use
    4  a PROMPT ELEMENT that does not fit   the truncation defect: rendered length vs the hard cap
    5  a MOVE NEVER CHOSEN                  the outcome measure. Present, describable, and dead
    6  a ROUTING LINE that omits a move     the map from need to move, checked against the registry
    7  a TOOL the charter refuses everywhere  present in the list, refused in every zone

WHAT THIS CANNOT SEE, said plainly: whether a move that IS chosen is chosen for a good reason, and
whether a move nobody needs SHOULD be removed rather than fixed. It finds the unpickable; deciding
what to do about each one is a judgement it does not make.
"""
from __future__ import annotations

import json
import os
import re
import sys

from aea.kernel import grid

W = "=" * 100


def _hands_ledger_moves() -> dict:
    """How many times each move was actually CHOSEN, across BOTH ledgers.

    TWO LEDGERS, BECAUSE THERE ARE TWO KINDS OF MOVE, and reading one of them made this report
    `brief`, `consolidate` and `reflect` as never chosen in 801 ticks. They had been chosen 32, 26
    and 96 times. Tool moves land in `hands_ledger.jsonl` keyed by TOOL; organ moves are
    subprocesses and land in `outcomes.jsonl` keyed by their ACTION string - `AWAKE:brief`,
    `ASLEEP:consolidate`, `REFLECT:self`. A search for the unpickable that looks in the wrong ledger
    manufactures the exact finding it exists to detect, which is worse than not running at all: it
    spends the reader's attention on a fiction and teaches them to distrust the real rows beside it.

    A count here is a LOWER BOUND. Both files are append-only but neither is guaranteed complete
    back to tick 1, so `0` means "no record of it being chosen", never "it was never chosen"."""
    counts = {}

    def bump(k):
        if k:
            counts[k] = counts.get(k, 0) + 1

    p = os.path.join(grid.STATE, "hands_ledger.jsonl")
    if os.path.exists(p):
        with open(p, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("src") == "wake":
                    bump(r.get("tool"))

    # organ moves: the ACTION string carries the move name after the colon, e.g. ASLEEP:consolidate
    p2 = os.path.join(grid.STATE, "outcomes.jsonl")
    if os.path.exists(p2):
        with open(p2, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                mv = str(r.get("move") or "")
                if ":" in mv:
                    tail = mv.split(":", 1)[1].split("(")[0].strip()
                    bump(tail)
                    bump(mv.split()[0])
    return counts


def find() -> list:
    """Every way a capability is present and cannot be chosen. Each row names the FIX."""
    from aea.kernel import decide, hands
    out = []

    def add(kind, subject, why, fix):
        out.append(dict(kind=kind, subject=subject, why=why, fix=fix))

    # THREE REGISTRIES, NOT ONE, and the first version of this check knew about one of them.
    # `_moves` builds the menu from TOOL_KNOWN + KNOWN + FREE_ARG, so reading only TOOL_KNOWN
    # reported `calc` as unreachable while it sits in the menu with a description. A detector for
    # "the code is right and something upstream is wrong" that reads the wrong upstream is the
    # defect it hunts, wearing a lab coat. Derived from `_moves` itself so it cannot drift again.
    all_moves = {}
    for reg in ("TOOL_KNOWN", "KNOWN", "FREE_ARG"):
        d = getattr(decide, reg, None) or {}
        for k in d:
            all_moves[k] = (decide.TOOL_KNOWN or {}).get(k) or {}
    reach = {(s or {}).get("tool") for s in (decide.TOOL_KNOWN or {}).values()}
    reach |= set(all_moves)          # a move named in KNOWN/FREE_ARG reaches its tool by name

    # 1. a TOOL no move can name
    for t in sorted(set(hands.TOOLS) - reach):
        spec = hands.TOOLS[t] or {}
        add("tool with no move", t,
            "in hands.TOOLS and no entry in decide.TOOL_KNOWN names it, so the wake has no word "
            "for it (capability=%s)" % spec.get("capability"),
            "add it to decide.TOOL_KNOWN, or delete the tool - a hand nothing can call is dead weight")

    # 2. a MOVE with no description -> rendered "do not pick this"
    for m in sorted(all_moves):
        if not (decide.WHEN or {}).get(m):
            add("move with no description", m,
                "decide.WHEN has no entry, so `_moves` renders it as '(no description - do not "
                "pick this)' - the menu instructs the wake to avoid it",
                "add a WHEN entry stating the condition under which it is the RIGHT move")

    # 3. a MOVE that takes an argument but offers no values
    for m, spec in (decide.TOOL_KNOWN or {}).items():
        if (spec or {}).get("arg") and not tuple((spec or {}).get("enum") or ()):
            add("move with an empty enum", m,
                "it takes argument %r and the menu shows no accepted values, so every call "
                "collapses to the default" % spec.get("arg"),
                "derive the enum from its source of truth (law S1: derive the map, never draw it)")

    # 4. a PROMPT ELEMENT that does not survive the cap
    try:
        from aea.loop import aea as loop
        st = grid.load_json(os.path.join(grid.STATE, "aea_state.json"), {})
        rendered = loop.standing(st)
        cap_c, cap_l = loop.STANDING_CHARS, loop.STANDING_LINES
        if len(rendered) >= cap_c:
            add("prompt element truncated", "standing block",
                "renders to exactly the %d-char cap, so anything appended is silently cut - the "
                "line looks delivered in the code and never reaches the wake" % cap_c,
                "raise the cap or insert high; then RENDER IT AND READ IT BACK, never trust the append")
        if len(rendered.splitlines()) >= cap_l:
            add("prompt element truncated", "standing block (lines)",
                "renders %d lines against a %d-line cap" % (len(rendered.splitlines()), cap_l),
                "same - verify by rendering, not by reading the code")
    except Exception as e:
        add("prompt element truncated", "standing block",
            "could not render: %s: %s" % (type(e).__name__, str(e)[:60]), "fix the renderer first")

    # 5. a MOVE NEVER CHOSEN - the outcome measure, and the one nothing else asks
    counts = _hands_ledger_moves()
    st = grid.load_json(os.path.join(grid.STATE, "aea_state.json"), {})
    ticks = st.get("tick") or 0
    for m, spec in sorted(all_moves.items()):
        tool = (spec or {}).get("tool") or m
        n = counts.get(tool, 0)
        if n == 0:
            add("move never chosen", m,
                "the wake has chosen it 0 times in %d ticks - present, reachable, and dead. "
                "Useless and blocked look identical from inside" % ticks,
                "check 2, 3 and 6 for this move first; if all clean, the condition may simply "
                "never fire and that is a design answer, not a defect")

    # 6. a ROUTING LINE that omits a move it should offer
    try:
        from aea.loop import aea as loop
        src = open(os.path.join(grid.ROOT, "aea", "loop", "aea.py"),
                   encoding="utf-8", errors="replace").read()
        m = re.search(r"match the question to the move:(.{0,600}?)\"\)", src, re.S)
        routing = m.group(1) if m else ""
        named = {n for n in all_moves if "`%s`" % n in routing}
        missing = sorted(set(all_moves) - named)
        if routing and missing:
            add("routing line omits moves", ", ".join(missing[:6]),
                "the question-kind -> move map names %d of %d moves; a need that matches an "
                "omitted move is routed to the closest one that IS named"
                % (len(named), len(decide.TOOL_KNOWN)),
                "this map is a DESIGN STATEMENT and may legitimately omit moves - but every "
                "omission should be deliberate. Check that none of these is the right answer to a "
                "question the line does route somewhere else")
    except Exception:
        pass

    # 7. a TOOL the charter refuses in every zone
    for t, spec in sorted((hands.TOOLS or {}).items()):
        zones = tuple((spec or {}).get("zones") or ())
        if not zones:
            add("tool refused everywhere", t,
                "declares no zone, so no seat may call it",
                "give it a zone or remove it")
    return out


def render(items: list) -> str:
    L = [W, "SELECTION BLOCKERS - capabilities that exist and cannot be chosen", W]
    if not items:
        L.append("\n  none found. Every move is nameable, described, enumerated, fits the prompt,")
        L.append("  and has been chosen at least once.")
        return "\n".join(L + ["", W])
    by = {}
    for it in items:
        by.setdefault(it["kind"], []).append(it)
    for kind, rows in by.items():
        L.append("\n  %s  (%d)" % (kind.upper(), len(rows)))
        for r in rows:
            L.append("    %-26s %s" % (r["subject"][:26], r["why"][:96]))
            L.append("    %-26s FIX: %s" % ("", r["fix"][:92]))
    L.append("\n  %d finding(s). A finding is not automatically a defect - some are design" % len(items))
    L.append("  answers. What is NOT acceptable is not knowing which.")
    L.append(W)
    return "\n".join(L)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    items = find()
    print(render(items))
    sys.exit(0)
