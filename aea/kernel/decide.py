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

# ================================================================================================
# R2a - THE DECISION MAY NAME A TOOL, AND NO STRING IT WROTE REACHES A TOOL ARGUMENT.
#
# THE THREAT, stated plainly, because it decides the whole shape of this rung. `aea/loop/aea.py`
# `sense()` fetches Hacker News headlines and puts them in the wake's prompt. That is UNTRUSTED
# TEXT sitting in the context of the thing that writes the decision. `hands.py` names the danger on
# its own `web_search` entry: "the model writes a free-text query, so anything in its context can
# leave in the query string (law B3)".
#
# So an unattended wake that can compose tool arguments is a prompt-injection channel with a
# network egress on the end of it. Not hypothetically - that is the documented top failure of every
# shipped agent of this shape, and the reason a university will not allow one on a managed device.
#
# THE RULE AT THIS RUNG: every argument comes from a CLOSED ENUMERATION in this file. The wake
# chooses WHICH tool and WHICH enum member. It cannot write a URL, a query, or an expression.
# Worst case under full injection: the entity reads one of its own state files.
#
# What is deliberately NOT here, and each for its own reason:
#   web_search / web_fetch / json_get   free-text argument, public zone, real egress. R2b, with
#                                       argument provenance designed rather than assumed.
#   calc                                local and pure, but the expression is free text; it is the
#                                       natural first R2b case precisely because it cannot leave.
#   send_email / spend                  impl=None and zones=() in hands.py. Structurally absent,
#                                       not merely unlisted - there is no code to reach.
# IMPORTED, NOT COPIED. `hands.READABLE_STATES` is the enforcement point and therefore the
# authority; a second hand-kept copy of a security boundary drifts, and this repo has paid
# for that shape three times already.
from aea.kernel.hands import READABLE_STATES as STATE_READABLE
BLOCK_KINDS = ("tool_missing", "permission_denied", "bad_response", "no_idea")
SELF_TOPICS = ("structure", "laws", "capabilities", "invariants")

# WHAT EACH MOVE IS FOR, AND WHEN IT IS OWED - the half the wake was missing.
#
# MEASURED 2026-07-30 by a control run. Given a state with forty undistilled memory notes and an
# explicit note saying so, the wake answered NONE. It was not being lazy and the pipeline was not
# broken: the core emitted `MOVE: NONE` and the formatter extracted it faithfully. The wake was
# choosing BLIND. `_moves()` printed `consolidate (runs ASLEEP:consolidate)` - a name and an opcode
# - and nothing anywhere said that consolidate is what you run when notes pile up. NONE is the
# correct answer to a menu you cannot read.
#
# The lesson generalises past this table: DERIVING the list from the source of truth guaranteed the
# names could not drift, and I read that guarantee as "the wake now knows its moves". Names are not
# knowledge. A capability the model cannot tell apart from the others is not reachable, however
# correctly it is wired - which is the same defect as an orphan module, one layer up.
#
# Keyed by move name across BOTH tables, and `test_wiring` asserts total coverage, because a move
# with no `when` silently becomes the one the wake never picks.
# THE THREE INTROSPECTIVE MOVES MUST NAME DIFFERENT ACTS, not three shades of "look at yourself".
# Measured by the control: given "Luis asked what you are able to DO and you had no answer", the
# wake chose `reflect`. Reasonable, and wrong - it was asked for a LIST it does not have, not a
# JUDGEMENT of its past. The three had been described as examining behaviour / knowing structure /
# knowing tools, which are one act at three targets. They are now written as three verbs a reader
# can tell apart: JUDGE what you did, LOOK UP how you are built, LIST what you can call.
WHEN = {
    "brief":           "Luis is owed a digest of what happened - no brief lately, or the world shifted",
    "consolidate":     "raw memory notes have piled up undistilled; this indexes and compresses them",
    "reflect":         "JUDGE your own recent decisions against your laws - about past behaviour, "
                       "never about looking something up",
    "know_yourself":   "LOOK UP how you are built (structure, laws, invariants) because you need a "
                       "fact about yourself you do not have",
    "know_your_hands": "LIST the tools available to call, because someone needs that list and you "
                       "cannot produce it",
    "read_your_state": "read the live contents of one of your own state files right now",
    "what_to_try":     "you are BLOCKED and the obvious move is unavailable - get the ordered ladder "
                       "of what to try next for this kind of block",
    "my_record":       "you want to know how your own recent actions turned out, and which moves "
                       "your record is currently holding back",
    "calc": "you need an exact arithmetic result - write it as `MOVE: calc <expression>`",
}

# =================================================================================================
# R2b - THE FIRST MOVE THAT CARRIES A STRING THE WAKE WROTE.
#
# R2a's guarantee was absolute and deliberately so: every argument comes from a closed enum, so no
# text the wake composed could reach a tool. This breaks that guarantee for exactly one tool, and
# the justification has to be structural rather than a judgement about likelihood - because the
# threat is not hypothetical. `aea/loop/aea.py` `sense()` puts live Hacker News headlines into the
# wake's prompt every tick. That is untrusted text sitting in the context of the thing composing the
# argument, which is the documented top failure of every agent of this shape.
#
# WHY `calc` IS SAFE HERE, AND IT IS NOT "BECAUSE IT IS LOCAL":
#
#   the charset   `_calc` admits `[\d\s+\-*().%]` and nothing else. NO LETTERS. An instruction, a
#                 hostname, a filename, an API key - none of them are REPRESENTABLE in a string
#                 that survives that filter. Injection is not unlikely here, it is impossible to
#                 express, and that is a different and much stronger claim.
#   no egress     outbound=False, no network in the impl. Even a hostile expression has nowhere to
#                 send a result.
#   no capability `capability=None` in the registry - the one tool with no permission cost.
#   the bomb      the only real attack was resource exhaustion (`9**9**9` never returns and raises
#                 nothing, so the tick guard cannot catch it). Measured, then bounded in `_calc`.
#
# All four have to hold for a tool to enter this table. `web_search` fails the first two and is why
# R2c needs an egress budget rather than another entry here.
#
# THE CHARSET CHECK BELOW IS A COURTESY, NOT THE ENFORCEMENT. `hands._calc` re-checks everything and
# is the authority; this one exists so the refusal appears in the decision log with a reason
# attached instead of surfacing as a tool error two modules downstream. It is deliberately looser
# than the real one so the two cannot drift into disagreeing about what is legal.
FREE_ARG = {
    "calc": dict(tool="calc", arg="expression", action="LOOK:calc",
                 ok=re.compile(r"^[\d\s+\-*/().%]{1,120}$")),
}

# WIDENED 2026-08-01, AND WIDENING IS THE POINT. R2-REACH needs 8 distinct (tool, args)
# situations and the surface could reach only 9 in total, of which the wake ever chose ONE. A gate
# with no headroom is a gate that passes by luck. Every entry below is a store the entity writes
# about ITSELF - none is personal, and `hands.PRIVATE_STORES` refuses the personal ones at the tool
# regardless of what this table says.
TOOL_KNOWN = {
    "know_yourself":   dict(tool="self_map",   arg="topic", enum=SELF_TOPICS,   default="structure",
                            action="LOOK:self_map"),
    "know_your_hands": dict(tool="list_tools",  arg=None,    enum=(),            default=None,
                            action="LOOK:list_tools"),
    "read_your_state": dict(tool="read_state", arg="name",  enum=STATE_READABLE, default="heartbeat.json",
                            action="LOOK:read_state"),
    "what_to_try":     dict(tool="what_to_try", arg="kind", enum=BLOCK_KINDS, default="no_idea",
                            action="LOOK:what_to_try"),
    "my_record":       dict(tool="my_record",  arg=None,    enum=(),           default=None,
                            action="LOOK:my_record"),
}

# Which words in the opening of an action select which tool. Same closed-vocabulary discipline as
# _HINTS, and matched in the same six-word window for the same reason.
_TOOL_HINTS = (
    (re.compile(r"\b(inspect|examine|check|inventory)\b.{0,24}\b(self|structure|architecture|"
                r"module|law|invariant|capabilit\w*)\b", re.I), "know_yourself"),
    (re.compile(r"\b(what|which)\b.{0,16}\b(tools?|hands?|can i do)\b", re.I), "know_your_hands"),
    (re.compile(r"\b(read|open|look at)\b.{0,20}\b(state|heartbeat|ledger|trust)\b", re.I),
     "read_your_state"),
)

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

    # AGE, FROM THE DECISION'S OWN STAMP WHEN IT HAS ONE. The wake now records `at` per decision,
    # which dates the THOUGHT; mtime dates the WRITE, and two decisions written in one run shared a
    # timestamp so the older was as "fresh" as the newer. The fallback stays for decisions written
    # before the wake learned to stamp - dropping it would make every historical decision
    # unreadable, and a migration that silently discards the past is worse than a weaker clock.
    stamped = last.get("at")
    if _finite(stamped) and stamped > 0:
        age = now - float(stamped)
        # A stamp from the FUTURE means a clock disagreement, not a fresh decision. Treating it as
        # fresh would let a bad clock bypass the staleness gate entirely.
        if age < -60:
            return None, f"decision is stamped {int(-age)}s in the future - clock disagreement"
        age = max(age, 0.0)
    else:
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

    # ============================================================================================
    # THE EXPLICIT MOVE COMES FIRST, AND WHEN IT IS PRESENT IT IS THE WHOLE ANSWER.
    #
    # Everything below this block is inference: regexes reading prose the wake wrote for a human,
    # guessing at intent. That was the only option while the wake had one action field. It now
    # writes `move` - a name copied from a printed list, or NONE - so the common path stops being a
    # guess and becomes a lookup.
    #
    # WHY THE FIELD EXISTS AT ALL, measured 2026-07-30. Naming the six moves inside the action
    # prompt worked mechanically and corrupted the deliberation: both ticks bent a real priority
    # ("close a sale for the diagnostic offer") into an available chore ("run a brief"), and HADES
    # flagged the second independently - `redo - does not surface Luis's real priorities; it adds a
    # new action`. The council had predicted exactly this. One field cannot hold both a priority and
    # a chore, because the model resolves the conflict toward the thing it can finish.
    #
    # An explicit NONE is therefore a FIRST-CLASS RESULT, not a failure to match, and it is expected
    # to be the majority verdict. A wake that answers NONE ninety times in a hundred is working.
    if "move" in decision:
        raw = str(decision.get("move") or "").strip()
        # Tolerate the shapes a formatter produces around a bare name - `MOVE: brief`, `"brief"`,
        # `know your hands` - then match against the closed table. Tolerant on FORM, exact on NAME.
        key = re.sub(r"^\s*move\s*[:\-]\s*", "", raw, flags=re.I)
        key = re.sub(r"[^a-z0-9]+", "_", key.strip().strip("`\"'").lower()).strip("_")
        if not key or key in ("none", "no", "nothing", "no_move", "n_a", "na", "null"):
            return None, "the wake chose NONE - no mechanical move is needed this tick"
        if key in TOOL_KNOWN:
            spec = TOOL_KNOWN[key]
            # THE DEFAULT ARGUMENT, ALWAYS. The wake picks the tool by name and nothing else; it
            # cannot steer the argument here, so the R2a guarantee (no wake-written string reaches a
            # tool) holds by construction rather than by filtering.
            args = {spec["arg"]: spec["default"]} if spec["arg"] else {}
            return dict(kind="tool", name=key, tool=spec["tool"], args=args,
                        action=spec["action"], age_s=decision.get("_age_s")), ""
        if key in known:
            action, argv, tmo = known[key]
            if not argv or not isinstance(argv, list) or not all(isinstance(x, str) for x in argv):
                return None, f"known action {key!r} has a malformed argv"
            if not _finite(tmo) or tmo <= 0:
                return None, f"known action {key!r} has a non-finite timeout"
            return dict(kind="script", name=key, action=action, argv=list(argv), timeout=int(tmo),
                        age_s=decision.get("_age_s")), ""

        # R2b: A MOVE THAT CARRIES AN ARGUMENT. Tried only AFTER every whole-string match has
        # failed, because the names are matched on the FULL normalised move and splitting first
        # would break every multi-word name - `know your hands` would parse as the move `know` with
        # the argument `your hands`, which is a refusal with a confusing reason attached.
        head, _sep, rest = raw.strip().partition(" ")
        hkey = re.sub(r"[^a-z0-9]+", "_", head.strip().strip("`\"'").lower()).strip("_")
        if hkey in FREE_ARG:
            spec = FREE_ARG[hkey]
            arg = rest.strip().strip("`\"'")
            if not arg:
                return None, f"move {hkey!r} needs an argument and none was given"
            if not spec["ok"].match(arg):
                # The refusal quotes the argument so the log shows WHAT was rejected. Truncated,
                # because the whole point is that this string came from an untrusted context.
                return None, (f"the {hkey!r} argument {arg[:40]!r} is not permitted here - "
                              f"arithmetic characters only, no letters")
            return dict(kind="tool", name=hkey, tool=spec["tool"], args={spec["arg"]: arg},
                        action=spec["action"], age_s=decision.get("_age_s")), ""
        # NAMED SOMETHING THAT DOES NOT EXIST -> REFUSE AND SAY SO. Falling through to the prose
        # regexes would hide the drift: the wake would be proposing a move the table no longer has
        # and the log would show some *other* action running, which is the exact failure `_moves()`
        # was derived from the table to prevent.
        return None, (f"the wake named move {raw[:40]!r}, which is not one of "
                      f"{sorted(list(TOOL_KNOWN) + list(known) + list(FREE_ARG))}")
    # ============================================================================================
    # NO `move` FIELD -> a decision written before the wake learned to choose. Inference below.
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

    # R2a: A TOOL IS TRIED FIRST, because looking is cheaper than running a script and because a
    # tool call is the narrower thing to permit. Arguments are picked from the enum by the same
    # six-word window; anything the wake wrote that is not an exact enum member is discarded and
    # the default stands. NO STRING FROM THE DECISION IS EVER PASSED THROUGH.
    tool_hits = [n for pat, n in _TOOL_HINTS if pat.search(text)]
    if len(set(tool_hits)) == 1:
        spec = TOOL_KNOWN[tool_hits[0]]
        args = {}
        if spec["arg"]:
            low = text.lower()
            picked = [v for v in spec["enum"] if v.split(".")[0].lower() in low]
            # exactly one enum member named, or the default. Two named is not a choice.
            args = {spec["arg"]: picked[0] if len(picked) == 1 else spec["default"]}
            if args[spec["arg"]] not in spec["enum"]:
                return None, f"argument {args[spec['arg']]!r} is not in the closed enum"
        return dict(kind="tool", name=tool_hits[0], tool=spec["tool"], args=args,
                    action=spec["action"], age_s=decision.get("_age_s")), ""
    if len(set(tool_hits)) > 1:
        return None, f"decision is ambiguous between tools - matches {sorted(set(tool_hits))}"

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
    return dict(kind="script", name=name, action=action, argv=list(argv), timeout=int(tmo),
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
