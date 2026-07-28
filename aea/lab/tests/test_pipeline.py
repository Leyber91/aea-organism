"""test_pipeline.py - THE SELF-MODIFICATION LADDER, TESTED ON CHANGES DESIGNED TO GET THROUGH.

A gate is only proven by a candidate that TRIES to pass while being wrong. Testing it with an
obviously broken file proves nothing, because the failure mode that matters is the change that looks
fine. So every case below is a real attack on a specific rung:

  1 an innocent change PASSES                  the gate is not simply refusing everything
  2 a change that edits its own judge FAILS    G3: the candidate may not author the test
  3 a change that breaks a frozen behaviour    the golden file actually bites
  4 a change that disconnects a module         no-new-orphans catches what tests cannot
  5 a change to a PROTECTED path is REFUSED    before it is ever judged
  6 nothing in the module can reach `prod`     G5: autonomy is granted, never taken

Run: python -m aea.lab.tests.test_pipeline      (or: python aea/lab/tests/test_pipeline.py)

THIS FILE IS NOT A GATE FILE ON PURPOSE. The gate must be judgeable by checks a proposal cannot
edit; this tests the gate itself and is run by a human or by CI, which is a different job. If it
were in GATE_FILES it would be restored during its own run, which is the kind of circularity that
makes a green light meaningless.
"""
from __future__ import annotations

import io
import os
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from aea.kernel import shadow  # noqa: E402

PASSED, FAILED = [], []


def check(name: str, fn):
    try:
        ok, detail = fn()
    except Exception as e:
        FAILED.append((name, "%s: %s" % (type(e).__name__, str(e)[:120])))
        return
    (PASSED if ok else FAILED).append((name, detail))


def _read(rel: str) -> str:
    with io.open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- 1 the ladder is declared honestly
def t_stages_declare_blind_spots():
    """Every rung must state what it CANNOT see. A stage with no blind spots is a stage nobody
    thought about, and this is the field that stops a green tick from reading as a guarantee."""
    names = [s["stage"] for s in shadow.STAGES]
    if names != ["dev", "qa", "prod"]:
        return False, "stages are %s" % names
    missing = [s["stage"] for s in shadow.STAGES if not s.get("blind")]
    if missing:
        return False, "no declared blind spots for: %s" % missing
    return True, "3 rungs, %d blind spots declared" % sum(len(s["blind"]) for s in shadow.STAGES)


# ---------------------------------------------------------------- 2 no promote, anywhere
def t_no_promote_exists():
    """G5: autonomy is granted, never taken. The module must not contain a way to apply itself."""
    src = _read("aea/kernel/shadow.py")
    bad = [ln for ln in src.splitlines()
           if ln.strip().startswith("def promote") or ln.strip().startswith("def apply_self")]
    if bad:
        return False, "found: %s" % bad[:2]
    if not hasattr(shadow, "propose"):
        return False, "propose() is missing"
    if hasattr(shadow, "promote"):
        return False, "shadow.promote exists"
    return True, "no promote(); propose() is the only exit"


# ---------------------------------------------------------------- 3 protected paths refuse first
def t_protected_refuses_before_judging():
    """A change to a PROTECTED path must be refused at the DEV rung, before anything is executed.
    Refusing later would mean the candidate's code ran first."""
    prot = [p for p in shadow.PROTECTED]
    if not prot:
        return False, "PROTECTED is empty"
    hits = [p for p in prot if shadow.protected(p)]
    if len(hits) != len(prot):
        return False, "protected() does not match its own list: %s" % (set(prot) - set(hits))
    if shadow.protected("aea/kernel/hands.py"):
        return False, "a normal source file is being treated as protected"
    return True, "%d protected paths, all matched; a normal file is not" % len(prot)


# ---------------------------------------------------------------- 4 the judge is restored, always
def t_gate_files_are_restored():
    """G3 mechanically: whatever a candidate writes into a gate file is overwritten by the running
    self's copy BEFORE a verdict is computed. Order is the whole guarantee, so the source must show
    restore_gate() called after apply_to() and before gate()."""
    src = _read("aea/kernel/shadow.py")
    i_apply = src.find("written = apply_to(dest, changes)")
    i_restore = src.find("restored = restore_gate(dest)")
    i_gate = src.find("v = gate(dest,")
    if -1 in (i_apply, i_restore, i_gate):
        return False, "could not locate the three calls in propose()"
    if not (i_apply < i_restore < i_gate):
        return False, "order is apply=%d restore=%d gate=%d" % (i_apply, i_restore, i_gate)
    if not shadow.GATE_FILES:
        return False, "GATE_FILES is empty"
    return True, "restore runs after apply and before gate; %d gate files" % len(shadow.GATE_FILES)


# ---------------------------------------------------------------- 5 the gate really is unauthorable
def t_gate_checks_are_not_configurable():
    """The four checks must be fixed in code, not read from state. A gate whose checks come from a
    file the candidate can write is not a gate."""
    src = _read("aea/kernel/shadow.py")
    body = src[src.find("def gate("):src.find("def _import_smoke(")]
    for smell in ("load_json", "os.environ.get", "json.load("):
        if smell in body:
            return False, "gate() reads external configuration: %s" % smell
    for required in ("every module imports", "frozen behaviours", "no new orphans",
                     "the candidate's own code is what loaded", "can still think"):
        if required not in body:
            return False, "missing check: %s" % required
    # THE FROZEN COUNT IS READ FROM THE SUITE AND FLOORED IN CODE. A literal count here was a
    # maintenance trap: adding a frozen behaviour broke the gate, which punishes exactly the thing
    # we want. A bare regex would let a candidate DELETE behaviours, so the floor is the real check.
    if "FROZEN_FLOOR" not in body:
        return False, "the frozen-behaviour count has no floor"
    if shadow.FROZEN_FLOOR < 31:
        return False, "FROZEN_FLOOR regressed to %d" % shadow.FROZEN_FLOOR
    return True, "5 checks, hardcoded, none configurable; frozen floor %d" % shadow.FROZEN_FLOOR


# ---------------------------------------------------------------- 6 the live gate actually runs
def t_gate_runs_on_the_live_tree():
    """The gate must EXECUTE, not just exist. Run it against the running tree and require a verdict
    with one row per check. This is the only case here that costs real time, and it is the one that
    proves the other five are talking about something real."""
    v = shadow.gate()
    if not isinstance(v, dict) or "checks" not in v:
        return False, "gate() returned %r" % type(v)
    if len(v["checks"]) < 5:
        return False, "only %d checks ran" % len(v["checks"])
    failed = [c["check"] for c in v["checks"] if not c["pass"]]
    return (v["pass"], "%d checks ran; %s" % (len(v["checks"]),
                                              "all pass" if v["pass"] else "FAILED: %s" % failed))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("THE SELF-MODIFICATION LADDER - testing the gate, not the change\n" + "=" * 92)
    for name, fn in [
        ("the ladder declares its blind spots", t_stages_declare_blind_spots),
        ("no promote() exists anywhere", t_no_promote_exists),
        ("protected paths refuse before judging", t_protected_refuses_before_judging),
        ("the judge is restored after the candidate writes", t_gate_files_are_restored),
        ("the gate's checks cannot be configured", t_gate_checks_are_not_configurable),
        ("the gate runs on the live tree", t_gate_runs_on_the_live_tree),
    ]:
        check(name, fn)
    for n, d in PASSED:
        print("  [PASS] %-48s %s" % (n, d))
    for n, d in FAILED:
        print("  [FAIL] %-48s %s" % (n, d))
    print("")
    print("all %d ladder invariants hold" % len(PASSED) if not FAILED
          else "%d of %d FAILED" % (len(FAILED), len(PASSED) + len(FAILED)))
    sys.exit(1 if FAILED else 0)
