"""test_cause - EVERY CLASS IS SHOWN A CASE IT MUST CATCH, AND A CASE IT MUST NOT.

D18's law, paid for by six of ten defects living in code written to CHECK something: *a detector
that has never been shown a positive it must catch has not been tested, it has only been run.* A
classifier is exactly that kind of code, and this one decides whether a capability gets discredited.

THE TWO-SIDED REQUIREMENT, which is the whole reason this file exists. An earlier version of the R3
plan specified only the false-NEGATIVE arm - "catch 25 consolidates that exit 0 and change nothing".
A classifier passing only that test is satisfied by grading EVERYTHING as the move's fault, which is
precisely how the entity would learn to abandon `brief` after a week of rate limits. So every case
below is paired: something the class must catch, and something it must refuse to claim.

    python -m aea.lab.tests.test_cause

This file lives under `aea/lab/tests/`, which is inside `shadow.PROTECTED` - the entity may never
rewrite the thing that grades it. That is not incidental; `cause.py` itself is NOT protected today,
which is a finding recorded alongside this file.
"""
from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None

from aea.kernel import cause

ROWS: list = []


def check(name: str, ok: bool, got="", want="") -> None:
    ROWS.append(dict(case=name, ok=bool(ok), got=str(got)[:46], want=str(want)[:34]))


def _boom():
    """Raise from inside `aea/` so the traceback carries a frame this repo owns."""
    raise ValueError("a defect in our own code")


def run() -> dict:
    # ---------------------------------------------------------------- TRANSIENT_EXTERNAL
    # MUST CATCH: the carried bit is the only thing that may set this class.
    for st in (429, 408, 500, 503):
        c = cause.classify(result=dict(ok=False, transport=True, status=st, error=f"HTTP {st}"))
        check(f"transient/{st} is TRANSIENT_EXTERNAL", c["class"] == cause.TRANSIENT_EXTERNAL, c["class"])
        check(f"transient/{st} never grades the move", c["counts_toward_move"] is False, c["counts_toward_move"])

    # MUST NOT CLAIM: prose that looks exactly like a rate limit, with no bit, is NOT transient.
    # This is the case that would let substring matching back in through the side door.
    c = cause.classify(note="(structuring failed: HTTP Error 429: Too Many Requests)")
    check("429 PROSE alone is not TRANSIENT", c["class"] == cause.UNATTRIBUTABLE, c["class"], "UNATTRIBUTABLE")
    check("429 prose still never grades", c["counts_toward_move"] is False, c["counts_toward_move"])
    check("429 prose keeps a non-binding hint", "rate limit" in c["evidence"], c["evidence"])

    # ---------------------------------------------------------------- CODE_FAULT
    # MUST CATCH: our own frame in the traceback outranks every other reading.
    try:
        _boom()
    except ValueError as e:
        c = cause.classify(exc=e)
    check("our own exception is CODE_FAULT", c["class"] == cause.CODE_FAULT, c["class"])
    check("code fault never grades the move", c["counts_toward_move"] is False, c["counts_toward_move"])
    check("code fault names the frame", "test_cause" in c["evidence"] or "aea" in c["evidence"], c["evidence"])

    # MUST CATCH EVEN WHEN A TRANSPORT BIT IS ALSO PRESENT: a crash in our code that happens to
    # coincide with a 429 is still our crash. Order matters, so it is asserted rather than assumed.
    try:
        _boom()
    except ValueError as e:
        c = cause.classify(result=dict(ok=False, transport=True, status=429), exc=e)
    check("CODE_FAULT outranks a transport bit", c["class"] == cause.CODE_FAULT, c["class"])

    # ---------------------------------------------------------------- VERIFY_FAILED / OK
    # MUST CATCH: the exit-0-but-nothing-happened case. MEASURED, not invented: `consolidate` ran 25
    # times with returncode 0 while state_bytes rose monotonically with zero decreases.
    c = cause.classify(result=dict(ok=True, transport=False),
                       verify=dict(pred="indexed note count strictly increases", result=False,
                                   detail="51 -> 51"))
    check("exit 0 + false post-condition is VERIFY_FAILED", c["class"] == cause.VERIFY_FAILED, c["class"])
    check("VERIFY_FAILED is the one that grades", c["counts_toward_move"] is True, c["counts_toward_move"])

    c = cause.classify(result=dict(ok=True, transport=False),
                       verify=dict(pred="indexed note count strictly increases", result=True,
                                   detail="51 -> 54"))
    check("a held post-condition is OK", c["class"] == cause.OK, c["class"])
    check("OK grades too, so credit is reachable", c["counts_toward_move"] is True, c["counts_toward_move"])

    # THE CASE THE FIRST VERSION OF THIS FILE MISSED, and it cost a real defect. Every wired caller
    # passes a `note` alongside `verify`; the tests did not, so the verify branch was unreachable in
    # production while every control passed. A control less complete than the subject cannot detect
    # the subject's defect - the same shape as an R2 control handed information the wake never had.
    c = cause.classify(result=dict(ok=True, transport=False),
                       verify=dict(pred="count strictly increases", result=False, detail="51 -> 51"),
                       note="ASLEEP:consolidate finished, rc=0, wrote 0 new memories")
    check("verify WITH a note still grades", c["class"] == cause.VERIFY_FAILED, c["class"], "VERIFY_FAILED")
    c = cause.classify(verify=dict(pred="count strictly increases", result=True, detail="51 -> 54"),
                       note="ASLEEP:consolidate finished, rc=0")
    check("passing verify WITH a note is OK", c["class"] == cause.OK, c["class"], "OK")
    check("and it counts toward the move", c["counts_toward_move"] is True, c["counts_toward_move"])

    # A TRANSIENT OUTRANKS A VERIFY BLOCK. If the transport died, whatever the post-condition says
    # about the world is not evidence about the CHOICE.
    c = cause.classify(result=dict(ok=False, transport=True, status=429),
                       verify=dict(pred="count strictly increases", result=False, detail="51 -> 51"),
                       note="HTTP Error 429")
    check("transient outranks a failed verify", c["class"] == cause.TRANSIENT_EXTERNAL, c["class"])
    check("so a 429 never discredits the move", c["counts_toward_move"] is False, c["counts_toward_move"])

    # ---------------------------------------------------------------- UNATTRIBUTABLE
    # MUST CATCH: the two real call sites that return ok=False with NO transport key -
    # grid.py:946 "no key" and grid.py:1169 "no powered plant".
    for err in ("no key GROQ_API_KEY", "no powered plant for chat/private (wait ~60s)"):
        c = cause.classify(result=dict(ok=False, error=err))
        check(f"missing bit -> UNATTRIBUTABLE ({err[:18]})", c["class"] == cause.UNATTRIBUTABLE, c["class"])
        check("unattributable never grades", c["counts_toward_move"] is False, c["counts_toward_move"])

    # MUST NOT CLAIM SUCCESS: no verify block and no bit establishes nothing at all.
    c = cause.classify()
    check("nothing at all is UNATTRIBUTABLE", c["class"] == cause.UNATTRIBUTABLE, c["class"])

    # ---------------------------------------------------------------- THE INVARIANT
    # The whole design in one assertion: exactly two classes may touch a move's score, and both of
    # them require a post-condition to have been EVALUATED.
    grading = {c for c in cause.CLASSES if cause.counts(c)}
    check("exactly OK and VERIFY_FAILED may grade", grading == {cause.OK, cause.VERIFY_FAILED},
          sorted(grading), "OK, VERIFY_FAILED")

    # THE ABLATION. Remove the carried bit from a genuine transient and it MUST stop being
    # TRANSIENT_EXTERNAL - otherwise the bit is decoration and something else is doing the work.
    with_bit = cause.classify(result=dict(ok=False, transport=True, status=429, error="HTTP 429"))
    without = cause.classify(result=dict(ok=False, status=429, error="HTTP 429"))
    check("ABLATION: dropping the bit changes the class",
          with_bit["class"] == cause.TRANSIENT_EXTERNAL and without["class"] != cause.TRANSIENT_EXTERNAL,
          f"{with_bit['class']} -> {without['class']}", "must differ")

    bad = [r for r in ROWS if not r["ok"]]
    print("=" * 96)
    print(f"TEST_CAUSE - {len(ROWS) - len(bad)}/{len(ROWS)}")
    print("=" * 96)
    for r in ROWS:
        mark = "ok  " if r["ok"] else "FAIL"
        print(f"  {mark} {r['case']:52s} {r['got']}" + (f"   want {r['want']}" if not r["ok"] else ""))
    print()
    print("  VERDICT:", "THE CLASSIFIER HOLDS" if not bad else f"{len(bad)} FAILED")
    return dict(ok=not bad, total=len(ROWS), failed=len(bad))


if __name__ == "__main__":
    sys.exit(0 if run()["ok"] else 1)
