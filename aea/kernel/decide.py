"""decide.py - THE WIRE FROM THE LOOP THAT THINKS TO THE LOOP THAT ACTS.

THE DEFECT THIS CLOSES, measured 2026-07-30 by reading both loops line by line:

    aea/loop/aea.py    deliberates every tick and writes {matters_now, changed, ACTION,
                       note_to_self} to state/aea_state.json. NOTHING READS IT. Verified: the file
                       and the key `surfaced` appear nowhere else in the tree except a comment and
                       a privacy exclusion.
    aea/loop/live.py   executes, survives, has a heartbeat - and chooses what to do with a
                       hardcoded if/elif over three scripts. No model is consulted.

One loop thinks and cannot act. The other acts and cannot think. This module is the pathway, and
it is deliberately the SMALLEST possible one: at this rung the wake may only REORDER actions
`live` already performs. It cannot add a power. That makes the whole wire reversible and testable
without touching a single capability ceiling.

------------------------------------------------------------------------------------------------
THE FIRST LAW HERE: A REFUSAL IS A RESULT, AND IT MUST SAY WHY.

Every function below returns `(value, why)`. Never a bare None, never a bare False.

This is not style. A deviation-triggered loop spends most of its life NOT acting, so "chose not to
act" is the normal case - and it is byte-identical, from outside, to "broke and returned nothing".
The council's adversary found the sharp end of this in forty seconds:

    "If brief_age returns None the vector math produces NaN; NaN > threshold is False in Python,
     so the entity silently does nothing for that cycle."

That is true, and it is the worst failure mode this architecture can have, because the null result
is indistinguishable from the healthy result. The same hole is ALREADY in `live.tick`: the IDLE
branch logs and returns without emitting a pulse, so a resting tick is invisible on the bus while
an acting tick is visible. An observer watching events cannot tell a resting entity from a dead one.

So: every decline carries a reason, every reason reaches the bus, and `test_wiring` asserts that no
path can return empty-handed and silent.
"""
from __future__ import annotations

import json
import math
import os
import re
import time

from aea.kernel import grid

STATE = os.path.join(str(grid.STATE), "aea_state.json")

# HOW OLD A DECISION MAY BE AND STILL BE ACTED ON. The wake reasons about "what matters right now";
# a decision from yesterday is about a world that has moved. 90 minutes is three of live's default
# 1800s ticks - long enough that one slow wake does not waste a decision, short enough that nothing
# stale ever executes.
MAX_AGE_S = 5400

# HOW FAR INTO THE ACTION A HINT MAY MATCH. Six words is about one clause - long enough for
# "consolidate the memory backlog now" and short enough that a subordinate "...review its content"
# nine words in cannot fire. Refusing is cheap here: the ladder catches it and the entity tries
# again next tick. See the note in `parse` for the live decision that set this number.
HINT_WINDOW = 6

# WHAT THE WAKE IS ALLOWED TO CHOOSE AT THIS RUNG: exactly the actions `live` already runs, and
# nothing else. The wake gets to say WHICH and WHEN, not WHAT. Adding a name here is adding a
# capability, so this table is the review surface - it should be short and it should be read.
KNOWN = {
    "brief":       ("AWAKE:brief",           ["-m", "aea.organs.brief"], 240),
    "consolidate": ("ASLEEP:consolidate",    ["-m", "aea.memory.consolidate", "--limit", "6"], 600),
    "reflect":     ("REFLECT:self",          ["-m", "aea.organs.reflect", "--once"], 240),
}

# The wake writes prose. These are the shapes it actually produces, mapped to the table above.
# Deliberately a closed vocabulary over a corpus rather than a model call (law W2): the mapping has
# to be deterministic, or the same decision could execute differently on two runs and nothing in
# the log would explain it.
_HINTS = (
    (re.compile(r"\b(brief|daily|report|summar(y|ise|ize)|digest)\b", re.I), "brief"),
    (re.compile(r"\b(consolidat|memor|corpus|distil|index|archive)\w*\b", re.I), "consolidate"),
    (re.compile(r"\b(reflect|review|introspect|self[- ]?check|audit)\w*\b", re.I), "reflect"),
)


def _finite(x) -> bool:
    """NaN and inf are the silent killers here. `NaN > threshold` is False, `NaN < threshold` is
    ALSO False, so a NaN slipped into any comparison makes every branch fall through to 'do
    nothing' with no error raised anywhere. Anything numeric crossing this boundary is checked."""
    try:
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(float(x))
    except Exception:
        return False


def latest(path: str = None, now: float = None) -> tuple:
    """The wake's most recent decision, or a REASON there isn't one.

    Returns (decision_dict | None, why). Every failure mode is named rather than collapsed into
    None, because 'the wake has never run' and 'the file is corrupt' need different responses and
    look identical from a falsy return."""
    # THE PATH IS RESOLVED AT CALL TIME, NOT AT DEFINITION. `def latest(path=STATE)` binds STATE
    # ONCE, when the module is imported - so reassigning `decide.STATE` afterwards changes the
    # constant and nothing else, and every call keeps reading the original file. Found by the
    # integration test on its first run: it redirected STATE to a temp file, `choose()` read the
    # real one anyway, and every case came back "decision is stale (1665306s old)" - a 19-day-old
    # file the test never touched.
    #
    # It is not only a testing problem. It means the module cannot be pointed anywhere else, ever,
    # by anything - and it fails in the most expensive way, by SILENTLY reading a different file
    # than the caller asked for and giving a plausible answer about it.
    path = path or STATE
    now = time.time() if now is None else now
    if not os.path.exists(path):
        return None, "no wake state on disk (the wake has never run)"
    try:
        raw = open(path, encoding="utf-8").read()
    except Exception as e:
        return None, f"wake state unreadable: {str(e)[:60]}"
    if not raw.strip():
        return None, "wake state is empty"
    try:
        d = json.loads(raw)
    except Exception as e:
        return None, f"wake state is not valid json: {str(e)[:60]}"
    if not isinstance(d, dict):
        return None, "wake state is not an object"
    surfaced = d.get("surfaced") or []
    if not isinstance(surfaced, list) or not surfaced:
        return None, "the wake has produced no decisions yet"
    last = surfaced[-1]
    if not isinstance(last, dict):
        return None, "the last decision is not an object"

    # AGE. The wake does not stamp its decisions, so the file's mtime is the only clock available.
    # Using it is honest but weak - it dates the WRITE, not the THOUGHT - and if two decisions are
    # written in one run they share a timestamp. Recorded as a known limit rather than hidden: the
    # right fix is for the wake to stamp each decision, and that belongs in the wake.
    try:
        age = now - os.path.getmtime(path)
    except Exception:
        age = 0.0
    if not _finite(age):
        return None, "decision age is not a finite number"
    if age > MAX_AGE_S:
        return None, f"decision is stale ({int(age)}s old, limit {MAX_AGE_S}s)"
    return dict(last, _age_s=round(age, 1)), ""


def parse(decision: dict, known: dict = None) -> tuple:
    """A decision -> (name, action, argv, timeout), or a REASON it cannot be used.

    Returns (candidate | None, why). Refusing is the common case and it is not an error - the wake
    writes prose about what matters, and most of what matters is not one of three scripts."""
    known = KNOWN if known is None else known
    if not isinstance(decision, dict):
        return None, "decision is not an object"
    # ONLY THE `action` FIELD, AND ONLY ITS OPENING - and this is the correction that matters most
    # in this module.
    #
    # MEASURED on the first live end-to-end run, 2026-07-30. The wake decided:
    #     "Finalize and publish the Operational AI Diagnostic offer - REVIEW its content, pricing,
    #      and supporting materials so it's ready for clients."
    # and this function matched the word "review" and scheduled a self-reflection. The wake wanted
    # to ship a sales offer. The correct answer was "this maps to nothing" - and refusing would
    # have been RIGHT, because publishing an offer is not one of three scripts.
    #
    # Two separate errors made it:
    #   the fields   matters_now and changed are CONTEXT, not instruction. Concatenating them means
    #                any word anywhere in a paragraph about the world can trigger an action.
    #   the window   a verb governs a sentence from the front. "Review" as the ninth word is a
    #                subordinate clause; as the first it is the instruction. Matching anywhere
    #                turns a keyword into a tripwire.
    #
    # This is law B2 - test the property, never a proxy for it - violated inside a module written
    # an hour after quoting it. The property is "what is the wake telling me to do"; the proxy was
    # "does this word appear".
    action_text = str(decision.get("action") or "").strip()
    if not action_text:
        return None, "decision names no action"
    if len(action_text) > 4000:
        return None, "decision text is implausibly long - refusing to parse"
    words = re.findall(r"[\w'-]+", action_text)
    if not words:
        return None, "decision action has no words"
    text = " ".join(words[:HINT_WINDOW])

    hits = [name for pat, name in _HINTS if pat.search(text) and name in known]
    if not hits:
        return None, f"nothing in the decision maps to a known action ({sorted(known)})"
    # MORE THAN ONE MATCH IS A REFUSAL, NOT A COIN FLIP. A decision that reads as both "write the
    # brief" and "consolidate memory" has not chosen; picking the first would invent a preference
    # the wake never expressed and would be untraceable in the log.
    if len(set(hits)) > 1:
        return None, f"decision is ambiguous - matches {sorted(set(hits))}"

    name = hits[0]
    action, argv, tmo = known[name]
    if not argv or not isinstance(argv, list) or not all(isinstance(x, str) for x in argv):
        return None, f"known action {name!r} has a malformed argv"
    if not _finite(tmo) or tmo <= 0:
        return None, f"known action {name!r} has a non-finite timeout"
    return dict(name=name, action=action, argv=list(argv), timeout=int(tmo),
                age_s=decision.get("_age_s")), ""


def choose(path: str = None, known: dict = None, now: float = None) -> tuple:
    """The whole wire in one call: (candidate | None, why). `why` is never empty when candidate is
    None, and the caller is expected to log it whichever way it goes.

    `path=None` resolves at call time - see `latest` for the defaulted-argument trap this avoids."""
    d, why = latest(path, now=now)
    if d is None:
        return None, why
    cand, why2 = parse(d, known)
    if cand is None:
        return None, why2
    return cand, f"the wake chose {cand['name']} ({int(cand.get('age_s') or 0)}s ago)"


def explain(cand, why: str) -> str:
    """One line for the log, in both directions, so a rest and an act read the same way."""
    return (f"WAKE -> {cand['action']} ({why})" if cand else f"WAKE -> nothing: {why}")
