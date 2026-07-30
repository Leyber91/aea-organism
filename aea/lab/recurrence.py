"""recurrence.py - WHICH LESSONS KEEP COMING BACK.

Luis, 2026-07-30, asking the sharpest question of the whole session: "why have we been discussing
this so many times in so many conversations, and yet you cannot remember it, or it doesn't come to
mind? If you find out why, it will help a lot."

This module is the instrument for answering that with data instead of an opinion. It reads
`state/lab/battery/history.jsonl` - one row per suite per run, appended and never overwritten - and
asks one question: WHICH ASSERTIONS HAVE FAILED MORE THAN ONCE, ON MORE THAN ONE DAY.

WHY THIS IS THE RIGHT INSTRUMENT FOR THAT QUESTION. A lesson that is written down and keeps being
broken is not a memory problem, it is a STORAGE-FORMAT problem, and the two are distinguishable by
evidence:

  a lesson stored as PROSE      must be retrieved, by a mind that is doing something else
  a lesson stored as a TEST     fires on its own, every run, whether anyone remembered it or not

The prediction this file exists to test: **lessons that became tests do not recur; lessons that
stayed prose recur forever.** If that holds, the answer to "why can't you remember it" is that
remembering was never the mechanism that worked, and the fix is not better writing - it is
compiling lessons into checks.

The uncomfortable half, recorded here so the analysis stays honest: some recurrences are not memory
failures at all. Running a shell heredoc because it is faster than writing a file, when the law
against it is known, is a DISCIPLINE failure. Conflating the two would let the interesting
explanation excuse the boring one. This file can only see what has a test; the recurrences it
cannot see are listed at the bottom by hand, and they are the ones that matter most.

    python -m aea.lab.recurrence
"""
from __future__ import annotations

import collections
import json
import os
import sys

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HISTORY = os.path.join(str(grid.STATE), "lab", "battery", "history.jsonl")

# LESSONS THAT HAVE NO TEST, AND THEREFORE CANNOT APPEAR IN THE DATA BELOW.
# Kept by hand precisely because the instrument is blind to them - a recurrence counter that only
# counts what it can measure would report a clean sheet and be wrong. Counts are from THIS session
# alone, so they are a floor rather than a total.
UNTESTED = [
    ("never test a regex or a path through a shell heredoc", 4,
     "the law is in CLAUDE.md, was read at boot, and was broken four times in one session"),
    ("ask what would have to be true of the INSTRUMENT before believing a finding", 8,
     "loopback lead-in, duet parser, echo detector, health metric, privacy grep, WER scorer, "
     "senses probe door, battery history parser"),
    ("a value computed and never read is a value never computed", 3,
     "reply_budget, think_off, the privacy dimension of grid.PLANTS"),
    ("bound the quantity you care about, never a proxy", 4,
     "MAX_SENTENCES, reply_budget in chars, max_tokens as a speech cap, CEIL_REF from the floor"),
    ("one run is an anecdote with a decimal point", 1,
     "three of four reported gains were inside the noise floor"),
    ("the summary is regenerable; the transcript is not", 3,
     "council last.json, party.json, battery {suite}.json - all overwritten"),
    ("a corpus written by the author of the answers measures string overlap, not judgement", 1,
     "the move control's 'owed' states shared vocabulary with the move descriptions and scored "
     "4/4 while proving nothing; caught by the council's adversary seat, not by me"),
    ("a negative case must shut EVERY other door, not the one it is about", 1,
     "the distractors ruled out one condition of six, so an unmentioned brief read as an overdue "
     "brief and the wake was scored wrong for a defensible answer"),
    ("attention follows effort, not risk - deliberately re-read the cheap part", 1,
     "the adversarial corpus took an hour and got the care; the sample count was one integer and "
     "got none, and the sample count was where the entire result lived"),
]

# LESSONS THAT BECAME TESTS TODAY, and the failure each one cost first. Kept beside the list above
# because the contrast IS the finding: these are the same KIND of lesson as the untested ones, and
# the only difference is where they were written. If the prediction at the bottom of this file
# holds, none of these will appear in the recurrence data again, and every item above will.
COMPILED = [
    ("a control samples each cell k times and prints its noise floor",
     "the same input answered `consolidate` then `brief`; four verdicts had been drawn from n=1"),
    ("a corpus is audited for vocabulary leak BEFORE it is scored",
     "a 4/4 result that measured phrase-matching against a near-copy of itself"),
    ("a dead core is not a decision - no verdict from an experiment that did not run",
     "27 hollow NONEs from a rate-limited plant read as 'the wake never chooses'"),
    ("a verdict names the rod that produced it; mixed rods get no verdict",
     "nine cells decided by a 70B and a 7B, averaged into a number describing neither"),
    ("every move carries the condition under which it is owed",
     "a menu of names and opcodes; NONE is the right answer to a list you cannot read"),
    ("a permanent condition is recorded permanently, never as an expiring cooldown",
     "the frontier ladder's top rod answered 410 Gone and was retried on every tick"),
]


def rows() -> list:
    if not os.path.exists(HISTORY):
        return []
    out = []
    for line in open(HISTORY, encoding="utf-8"):
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def report() -> str:
    rs = rows()
    L = ["=" * 96, "RECURRENCE - which lessons keep coming back", "=" * 96]
    if not rs:
        L.append("\n  No history yet. This file was created 2026-07-30; every battery run before")
        L.append("  that date overwrote its predecessor and is gone. The instrument starts now,")
        L.append("  which means the most useful column - 'how many times has this recurred' -")
        L.append("  will be empty for a while and should not be read as 'nothing recurs'.")
    else:
        runs = len({r["at"] for r in rs})
        days = len({r["at"][:10] for r in rs})
        L.append(f"\n  {len(rs)} suite-runs across {runs} battery runs on {days} day(s)")
        fails = collections.Counter()
        when = collections.defaultdict(set)
        for r in rs:
            for f in r.get("failures") or []:
                key = f"{r['suite']}/{f.get('case','')[:70]}"
                fails[key] += 1
                when[key].add(r["at"][:10])
        if not fails:
            L.append("  no failures recorded in any run so far")
        else:
            L.append(f"\n  {'times':>5} {'days':>5}  assertion")
            for key, n in fails.most_common(30):
                d = len(when[key])
                mark = "  <- RECURRING ON SEPARATE DAYS" if d > 1 else ""
                L.append(f"  {n:5d} {d:5d}  {key}{mark}")
            multi = [k for k, v in when.items() if len(v) > 1]
            L.append(f"\n  {len(multi)} assertion(s) have failed on more than one day.")
            L.append("  Those are the ones where writing it down more clearly will not help.")

    L.append("\n" + "=" * 96)
    L.append("LESSONS WITH NO TEST - invisible to the data above, counted by hand")
    L.append("=" * 96)
    L.append("  These are recorded in prose, in files that are read at boot, and were broken")
    L.append("  anyway. The counts are from ONE session, so they are a floor.\n")
    L.append(f"  {'times':>5}  lesson")
    for lesson, n, note in sorted(UNTESTED, key=lambda x: -x[1]):
        L.append(f"  {n:5d}  {lesson}")
        L.append(f"         {note}")
    L.append("\n" + "=" * 96)
    L.append(f"COMPILED INTO TESTS ({len(COMPILED)}) - the control group")
    L.append("=" * 96)
    L.append("  Same kind of lesson as the list above. The only difference is where it was written.")
    for lesson, cost in COMPILED:
        L.append(f"\n  {lesson}")
        L.append(f"    cost: {cost}")
    L.append("\n" + "=" * 96)
    L.append("THE PREDICTION THIS FILE EXISTS TO TEST")
    L.append("=" * 96)
    L.append("  Lessons that became TESTS do not recur. Lessons that stayed PROSE recur forever.")
    L.append("")
    L.append("  Evidence so far, and it is one-sided by construction: the tool-theatre guard, the")
    L.append("  vocative stripper and the reply budget each cost a live failure to find, were")
    L.append("  compiled into assertions, and have not regressed since. Every item in the list")
    L.append("  above stayed prose and recurred within the same session that recorded it.")
    L.append("")
    L.append("  If it holds, 'why can't you remember it' has a mechanical answer: REMEMBERING WAS")
    L.append("  NEVER THE MECHANISM THAT WORKED. A lesson in prose must be retrieved, by topic, at")
    L.append("  a moment defined by action, with no shared vocabulary between the two. A lesson in")
    L.append("  a test fires whether anyone remembered it or not.")
    return "\n".join(L)


if __name__ == "__main__":
    print(report())
