"""test_knobs - THE DECLARATION MAY NOT GROW INTO A PROGRAMMING LANGUAGE.

Law S5 (design/THE_LAWS.md:169): *a declaration names a registered operation with parameters. Never
code.* Its NAMED failure path is the one Ansible walked and its author disavows - the declaration
grows `when:`, then `loop:`, then `rescue:`, each one reasonable on the day it is added, until the
thing is a language nobody designed and nothing can validate.

A comment cannot stop that. A test asserting a LITERAL key-set can, because adding a key has to
break a test on purpose, in a file the entity may never edit (`aea/lab/tests/` is inside
`shadow.PROTECTED`). That is the whole point of this file.

It also asserts the two properties that make a knob safe rather than merely declared: every knob is
BOUNDED, and no knob may name a permission.

    python -m aea.lab.tests.test_knobs
"""
from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None

# THIS TEST DOES NOT TOUCH THE PRODUCTION STORE. It exercises the clamp by setting hi*100, and the
# first version persisted 32000 into the live knobs file - so the brief ran under a real ceiling
# this test had installed, the "restore" restored the already-polluted value, and it passed alone
# while failing in a sweep. Redirected BEFORE knobs is imported so the module never sees the real
# path. D48, in a file written the same day as the fix for D48.
import os as _os, tempfile as _tf
_os.environ["AEA_KNOBS"] = _os.path.join(_tf.mkdtemp(prefix="knobtest_"), "knobs.json")

from aea.kernel import knobs, unstick

ROWS: list = []


def check(name, ok, got="", want=""):
    ROWS.append(dict(case=name, ok=bool(ok), got=str(got)[:44], want=str(want)[:34]))


def run() -> dict:
    # THE FROZEN SCHEMA. Change this literal only with a reason written beside it.
    check("knob schema is exactly these keys",
          knobs.KNOB_KEYS == ("default", "lo", "hi", "unit", "desc"),
          knobs.KNOB_KEYS, '("default","lo","hi","unit","desc")')

    for (cap, knob), spec in knobs.KNOBS.items():
        k = f"{cap}.{knob}"
        check(f"{k} declares exactly the frozen keys",
              tuple(sorted(spec)) == tuple(sorted(knobs.KNOB_KEYS)), tuple(sorted(spec)))
        # BOUNDED, NOT MERELY DECLARED. A knob without a range is an unbounded write with a
        # friendly name; max_tokens=10_000_000 is the same operation as 900, aimed off a cliff.
        check(f"{k} is bounded and the range is sane",
              isinstance(spec["lo"], (int, float)) and isinstance(spec["hi"], (int, float))
              and spec["lo"] < spec["hi"], f"{spec['lo']}..{spec['hi']}")
        # A DECLARED None IS "NO CEILING" AND IS THE HONEST RESTING STATE FOR A BUDGET. The first
        # version of this assertion required a numeric default, which quietly forced every knob to
        # name a number - and a number nobody chose is the defect this whole table exists to remove.
        check(f"{k} default is None (no ceiling) or inside its bounds",
              spec["default"] is None or spec["lo"] <= spec["default"] <= spec["hi"],
              spec["default"])
        check(f"{k} says WHY it exists", len(str(spec["desc"])) > 30, len(str(spec["desc"])))
        # NO KNOB MAY NAME A PERMISSION. `unstick.INVARIANTS` enforces this on the move; the table
        # simply contains no such entry, so the two guards agree by construction.
        low = k.lower()
        check(f"{k} names no permission",
              not any(w in low for w in unstick.INVARIANTS), k)

    # REFUSALS, exercised rather than assumed.
    r = knobs.set("produce_brief", "not_a_real_knob", 1, by="test")
    check("an undeclared knob is REFUSED", r["ok"] is False, r.get("refused", "")[:40])

    spec = knobs.KNOBS[("produce_brief", "max_tokens")]
    was = knobs.get("produce_brief", "max_tokens")
    r = knobs.set("produce_brief", "max_tokens", spec["hi"] * 100, by="test")
    check("an over-range value CLAMPS and says so", r.get("clamped") is True and r["to"] == spec["hi"],
          f"{r.get('to')} clamped={r.get('clamped')}")
    r = knobs.set("produce_brief", "max_tokens", "not a number", by="test")
    check("a non-numeric value is REFUSED", r["ok"] is False, r.get("refused", "")[:40])
    knobs.set("produce_brief", "max_tokens", was, why="restore after test", by="test")
    check("restored to the pre-test value", knobs.get("produce_brief", "max_tokens") == was, was)

    # THE READER EXISTS. A knob nothing reads is a write with no meaning - the exact reason
    # `_apply_knob` returned False until this was true.
    import inspect
    from aea.organs import brief
    src = inspect.getsource(brief.grid_private)
    check("brief.grid_private READS its budget knob", "knobs.get" in src,
          "knobs.get" in src)

    bad = [r for r in ROWS if not r["ok"]]
    print("=" * 92)
    print(f"TEST_KNOBS - {len(ROWS) - len(bad)}/{len(ROWS)}")
    print("=" * 92)
    for r in ROWS:
        if not r["ok"]:
            print(f"  FAIL {r['case']:54s} {r['got']}   want {r['want']}")
    print("  VERDICT:", "THE DECLARATION HOLDS" if not bad else f"{len(bad)} FAILED")
    return dict(ok=not bad, total=len(ROWS), failed=len(bad))


if __name__ == "__main__":
    sys.exit(0 if run()["ok"] else 1)
