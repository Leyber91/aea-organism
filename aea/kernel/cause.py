"""cause.py - WHY DID IT FAIL? Answered mechanically, with no model, so a bad night cannot teach
the entity to abandon a working capability.

    python -m aea.kernel.cause            # the classes, and the corpus they were tested against
    python -m aea.kernel.cause --replay   # classify every failure already on disk

THE FAILURE THIS EXISTS TO PREVENT, and it is not hypothetical - it is what the existing record
would produce on day one.

`state/aea_state.json` holds 226 memory notes. **192 of them are the identical string**
`(structuring failed: HTTP Error 429: Too Many Requests)`. `state/trust_ledger.json` records
`produce_brief` at 85 runs and 68 fails. An outcome store that writes `brief failed` 68 times and a
learner that reads it will conclude **"do not choose brief"** - permanently removing a capability
because a rate limiter was saturated for a week. The move was correct every single time.

So the record cannot store a boolean. It stores a CLASS, and the classes have opposite learning
rules. Exactly one of them is evidence about the entity's judgement:

    TRANSIENT_EXTERNAL   the system failed, not the choice          counts_toward_move = False
    CODE_FAULT           our own code raised                        counts_toward_move = False
    UNATTRIBUTABLE       no provenance survives; we do not know     counts_toward_move = False
    VERIFY_FAILED        it ran, and its declared post-condition    counts_toward_move = TRUE
                         is false                                   <-- the only one that grades

WHY THE BIT IS CARRIED AND NEVER RE-DERIVED. `grid.call_openai` already computes the answer at the
only layer that can see it - `transport=(e.code >= 500 or e.code in (408, 429))` for an HTTPError,
`transport=True` for any socket/DNS/timeout, and `transport=isinstance(payload.get("error"), dict)`
for a 200 carrying a server error object (grid.py:1029/1054/1069/1076/1156/1160). That bit is read
at exactly TWO sites in the whole tree today - `hands.unmeasured` and `brief.py:130` - and brief
uses it for retry policy and then **throws it away** before calling `trust.record` with a bare bool
and a prose note. This module's entire job is to stop that discard.

SUBSTRING MATCHING IS REFUSED AS A CLASSIFIER, and `aea/organs/brief.py:125-129` records why: it is
"whack-a-mole against every provider's error phrasing, forever". A phrase may produce a non-binding
`hint`, which never sets the class and never gates learning. If the bit is absent the honest answer
is UNATTRIBUTABLE - which is a REFUSAL, not a pass, and which yields a work list naming the call
sites that must start carrying provenance rather than a comfortable guess about the past.

WHAT IS DELIBERATELY NOT HERE. CAPABILITY_ABSENT and CONTRACT_VIOLATION are real classes with no
rows on disk to test them against, and a detector that has never been shown a positive it must catch
has not been tested, it has only been run (D18). They arrive the first time one appears.
"""
from __future__ import annotations

import os
import sys
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

TRANSIENT_EXTERNAL = "TRANSIENT_EXTERNAL"
CODE_FAULT = "CODE_FAULT"
VERIFY_FAILED = "VERIFY_FAILED"
UNATTRIBUTABLE = "UNATTRIBUTABLE"
OK = "OK"                    # the post-condition was evaluated and it HELD

CLASSES = (OK, TRANSIENT_EXTERNAL, CODE_FAULT, VERIFY_FAILED, UNATTRIBUTABLE)

# ONLY THESE TWO MAY CREDIT OR DISCREDIT A MOVE. Everything else is evidence about the SYSTEM.
# OK is in the set deliberately: a design that records only failures can discredit a move and never
# credit one, which is a ratchet toward doing nothing - the same shape as a criterion that rewards
# NONE. Crediting and discrediting must be reachable through the same door.
GRADES_THE_MOVE = frozenset({VERIFY_FAILED, OK})

# Confidence is set by WHICH MECHANISM FIRED, never by a model and never by how sure anyone feels.
# `certain` means a bit computed at the layer that could see the truth. `absent` means no provenance
# survived to this point, which is a statement about our instrumentation and not about the world.
CERTAIN, PROBABLE, ABSENT = "certain", "probable", "absent"

# Non-binding. These NEVER set a class. They exist so an UNATTRIBUTABLE row can say what it looks
# like, so the work list is orderable - not so the classifier can quietly guess.
_HINTS = (
    ("429", "looks like a rate limit"),
    ("Too Many Requests", "looks like a rate limit"),
    ("timeout", "looks like a timeout"),
    ("timed out", "looks like a timeout"),
    ("Connection", "looks like a transport failure"),
    ("no powered plant", "looks like every plant was cooling"),
    ("no key", "looks like a missing credential"),
)

_AEA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../aea


# THE SUBSET OF _HINTS THAT MEAN "THE WORLD FAILED, NOT THE CHOICE". Derived from the table above by
# what each hint SAYS, never re-typed, because a second hand-kept copy of these needles is exactly
# the drift this module was written to prevent.
#
# WHY THIS HAD TO BECOME BINDING. `live.py` evaluated a post-condition ONLY when the process exited
# 0, on the correct reasoning that a 429 kills the process and grading the move on that teaches the
# entity to abandon a good action because of network weather. But the consequence was that EVERY
# non-zero exit became UNATTRIBUTABLE, so no failure ever graded a move, so R3's "stop re-choosing
# what fails" could never accumulate a single point of evidence. The rung was unreachable by
# construction - the same shape as R1's gate, found the same day.
#
# The exit code was never the right authority. The post-condition is direct evidence about the
# world; the exit code is a statement about a process. So the post-condition is now evaluated
# either way, and THIS predicate carries the protection that the exit-code guard used to: a tail
# that looks transient produces TRANSIENT_EXTERNAL and grades nothing, exactly as before.
_TRANSIENT_SAYS = ("rate limit", "timeout", "transport failure", "every plant was cooling")
TRANSIENT_NEEDLES = tuple(n for n, say in _HINTS if any(s in say for s in _TRANSIENT_SAYS))


def looks_transient(text: str) -> bool:
    """Does this tail carry a signature of the world failing rather than the choice being wrong?

    Deliberately conservative in ONE direction: a false positive here only costs a move that is not
    graded this tick, while a false negative teaches the entity that a correct action is broken. Of
    the two errors, only the second is permanent."""
    t = str(text or "").lower()
    return any(n.lower() in t for n in TRANSIENT_NEEDLES)


def _hint(text: str) -> str:
    t = str(text or "")
    for needle, say in _HINTS:
        if needle.lower() in t.lower():
            return say
    return ""


def _frame_under_aea(exc) -> str:
    """A traceback frame inside our own package means OUR code raised - free, and certain.

    `hands.py:823-825` catches bare `Exception` and keeps only `str(e)[:160]`, discarding the
    traceback. So a crash inside a tool implementation is currently indistinguishable from the tool
    honestly reporting failure, and would be recorded against the MOVE. The frame is right there and
    costs nothing to look at."""
    if exc is None:
        return ""
    try:
        tb = exc.__traceback__
        frames = traceback.extract_tb(tb) if tb is not None else []
    except Exception:
        return ""
    # ANY frame under `aea/` counts, INCLUDING `aea/lab/`. The first version excluded lab frames on
    # the theory that harness code is not the entity's code. Its own positive control caught that
    # within a minute: the control lives in `aea/lab/tests/`, so the exclusion made CODE_FAULT
    # unreachable by the one case that must prove it fires. The theory was also wrong on the merits
    # - the question this class answers is *did OUR code raise, rather than the move being bad*, and
    # a crash in the harness is still our code raising. D18, arriving inside the detector written to
    # honour D18.
    for fr in reversed(frames):
        fn = os.path.abspath(str(fr.filename))
        if fn.startswith(_AEA_DIR):
            return f"{os.path.relpath(fn, os.path.dirname(_AEA_DIR))}:{fr.lineno}"
    return ""


def classify(result=None, verify=None, exc=None, note: str = "") -> dict:
    """Return {class, confidence, source, evidence, counts_toward_move}. PURE - no I/O, no model.

    `result`  a transport-layer dict, canonically what `grid.call_openai` returns. The `transport`
              key is the one that matters; ABSENT is meaningfully different from False.
    `verify`  the declared post-condition's verdict: {"pred": str, "result": bool, "detail": str}.
              Its ABSENCE is why a row can never claim success - see `outcomes.require`.
    `exc`     the exception object, if one was caught, WITH its traceback still attached.
    `note`    free prose. Used only for a non-binding hint. It can never set the class.
    """
    def out(cls, conf, source, evidence):
        return dict(**{"class": cls}, confidence=conf, source=source, evidence=evidence,
                    counts_toward_move=(cls in GRADES_THE_MOVE))


    # 1. OUR OWN CODE RAISED. Checked FIRST: a crash in the tool implementation is not the entity
    #    choosing badly, and it outranks every other reading of the same failure.
    frame = _frame_under_aea(exc)
    if frame:
        return out(CODE_FAULT, CERTAIN, "traceback-frame-under-aea", frame)

    r = result if isinstance(result, dict) else {}

    # 2. THE CARRIED BIT. Present and true -> the system failed, and the move is untouched.
    if "transport" in r and r.get("transport"):
        ev = f"transport=True status={r.get('status')} {str(r.get('error') or '')[:80]}".strip()
        return out(TRANSIENT_EXTERNAL, CERTAIN, "grid.transport", ev)

    # 3. THE DECLARED POST-CONDITION, AND IT MUST BE CHECKED BEFORE THE NO-PROVENANCE BRANCH.
    #
    # It was not, and the ordering bug made this branch UNREACHABLE for every real caller. The
    # no-provenance test below read `elif r or note:`, and `live._record_outcome` always passes a
    # `note` (the process tail), so every wired row returned UNATTRIBUTABLE - including the
    # exit-0-nothing-happened case this module exists to catch. The unit tests passed because they
    # supplied `verify` with no `note`, exercising a path the caller never takes: **a control less
    # complete than the subject cannot detect the subject's defect.** Same shape as the R2 control
    # that was handed information the wake never had.
    #
    # It also belongs first on the merits. A post-condition that was ACTUALLY EVALUATED is direct
    # evidence about the world; a missing transport bit is only a statement about instrumentation.
    if isinstance(verify, dict) and "result" in verify:
        if verify.get("result"):
            # A PASS IS ALSO EVIDENCE ABOUT THE MOVE, and it must count. A design that records only
            # failures can discredit a move and never credit one, which is a ratchet toward doing
            # nothing - the same shape as a criterion that rewards NONE.
            return out(OK, CERTAIN, "verify", str(verify.get("pred") or ""))
        return out(VERIFY_FAILED, CERTAIN, "verify",
                   f"{verify.get('pred') or 'post-condition'} was false: "
                   f"{str(verify.get('detail') or '')[:120]}")

    if r or note:
        # 3. THE BIT IS ABSENT. This is the honest branch and it is the common one for history.
        #    grid.py:946 ("no key") and grid.py:1169 ("no powered plant") both return ok=False with
        #    NO transport key, and no row written before today carries one at all: measured, 0 of
        #    209 gate_ledger rows and 0 of 226 memory notes. Guessing here is exactly the failure
        #    this module exists to prevent, so it refuses and names what it would have guessed.
        h = _hint(r.get("error") or note)
        return out(UNATTRIBUTABLE, ABSENT, "no-provenance",
                   (h + " | " if h else "") + "no transport bit at this call site")

    # 4. THE ONLY PLACE A MOVE IS GRADED. The action reached its implementation and the declared
    #    post-condition was evaluated. Nothing above this line may reach it.
    if isinstance(verify, dict) and "result" in verify:
        if verify.get("result"):
            # A PASS IS ALSO EVIDENCE ABOUT THE MOVE, and it must count. A design that only records
            # failures can discredit a move and never credit one, which is a ratchet toward doing
            # nothing - the same shape as the NONE-rewarding restraint criterion.
            return out(OK, CERTAIN, "verify", str(verify.get("pred") or ""))
        return out(VERIFY_FAILED, CERTAIN, "verify",
                   f"{verify.get('pred') or 'post-condition'} was false: "
                   f"{str(verify.get('detail') or '')[:120]}")

    # 5. NO VERIFY BLOCK AND NO TRANSPORT BIT. Nothing was established. `outcomes.require` refuses
    #    to persist a success in this state, so reaching here on an ok=True row is a bug upstream.
    return out(UNATTRIBUTABLE, ABSENT, "no-verify",
               (_hint(note) + " | " if _hint(note) else "") + "no post-condition was evaluated")


def counts(cls: str) -> bool:
    """May a row of this class credit or discredit a MOVE? The single place that question is answered."""
    return cls in GRADES_THE_MOVE


if __name__ == "__main__":
    print("=" * 92)
    print("CAUSE - the four classes, and which one may grade a move")
    print("=" * 92)
    for c in (TRANSIENT_EXTERNAL, CODE_FAULT, UNATTRIBUTABLE, VERIFY_FAILED):
        print(f"  {c:20s} counts_toward_move={c in GRADES_THE_MOVE}")
    print()
    if "--replay" in sys.argv[1:]:
        import json
        from aea.kernel import grid
        st = grid.load_json("aea_state.json", {"memory": []})
        notes = [str(m) for m in st.get("memory", [])]
        tally = {}
        for n in notes:
            c = classify(note=n)
            tally[c["class"]] = tally.get(c["class"], 0) + 1
        print(f"  {len(notes)} memory notes on disk:")
        for k, v in sorted(tally.items(), key=lambda kv: -kv[1]):
            print(f"     {k:20s} {v}")
        print()
        print("  UNATTRIBUTABLE IS THE CORRECT ANSWER FOR HISTORY, and it is a refusal rather than")
        print("  a pass. No row written before today carries a transport bit - measured, 0 of 226")
        print("  notes and 0 of 209 gate_ledger rows - so nothing on disk can be attributed. The")
        print("  hints below say what each row LOOKS like; none of them sets a class.")
        seen = {}
        for n in notes:
            h = _hint(n)
            if h:
                seen[h] = seen.get(h, 0) + 1
        for k, v in sorted(seen.items(), key=lambda kv: -kv[1]):
            print(f"     {v:>4d}  {k}")
