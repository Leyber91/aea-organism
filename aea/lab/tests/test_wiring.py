"""test_wiring.py - EVERY RUNG FROM R0 UP IS REACHABLE, and a new disconnection fails loudly.

    python -m aea.lab.tests.test_wiring

WHAT THIS CATCHES THAT NOTHING ELSE DOES. `ladder.verify_funcs()` has computed this answer for
weeks and nothing asserted it, so its output was a thing a human read when a human happened to
look. On 2026-08-04 R5 declared its functions for the first time and EIGHT came back UNWIRED - the
hypothesis store, the probe and the settlement were reachable from a terminal and from nothing the
organism runs. That is the R1 defect, verbatim, in a rung built the same day by an author who had
read R1's postmortem hours earlier. A check nobody runs is a check that does not exist.

THE RATCHET SHAPE, and why it is not "assert unwired == 0". One name is legitimately unreachable
right now and it is named below with its reason. A test that demanded zero would have to either
fail forever - and a permanently red test is read as broken, then ignored, then deleted - or be
satisfied by widening what "wired" means, which is the one move that destroys the check. So the
allow-list is explicit, each entry carries WHY, and anything not on it fails. Shrinking the list is
the only edit that needs no argument; growing it needs one in writing.

FOUR ASSERTIONS:
  missing == 0           a rung naming code that does not exist is a claim about absent work
  unwired subset of KNOWN a NEW disconnection fails; a known one is on the record with its reason
  measured rungs declare  a rung that is PROVEN or PARTIAL and declares nothing is invisible to
                          this whole file - which is precisely how R5 stayed unmeasured
  R0..R5 contiguous       no measured rung sits above an unmeasured one
"""
from __future__ import annotations

import sys

from aea.tooling import ladder

# EVERY ENTRY NEEDS A REASON. "It is fine" is not one.
KNOWN_UNWIRED = {
    "kernel.hypotheses:state":
        "R5's claims are readable by the console but by nothing the ORGANISM runs, so the entity "
        "cannot see what it claimed or what died. The fix is the wake's standing block, deferred "
        "2026-08-04 only because editing the wake prompt mid-run would contaminate the outward "
        "experiment that is still counting. A real gap, held open deliberately, not an exemption.",
}

# The rungs that must be wired for the ladder to mean anything below R6.
SPINE = ("R0", "R1", "R1.5", "R2", "R3", "R4a", "R4b", "R5")


def run() -> list:
    checks = []

    def chk(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    v = ladder.verify_funcs()
    chk("every declared name EXISTS", not v["missing"], str(v["missing"])[:110])

    unwired = {u.split(" [")[0] for u in v["unwired"]}
    new = sorted(unwired - set(KNOWN_UNWIRED))
    chk("no NEW capability is unreachable", not new, ("new: %s" % new) if new else "")
    healed = sorted(set(KNOWN_UNWIRED) - unwired)
    chk("the known-unwired list has not gone stale", not healed,
        ("now wired, delete from KNOWN_UNWIRED: %s" % healed) if healed else "")

    # A MEASURED RUNG MUST DECLARE. This is the assertion that would have caught R5.
    rows = ladder.measure_all() if hasattr(ladder, "measure_all") else None
    statuses = {}
    if rows is None:
        for rid, fn in ladder.MEASURE.items():
            try:
                statuses[rid] = bool((fn() or {}).get("met"))
            except Exception:
                statuses[rid] = False
    else:
        for r in rows:
            statuses[r.get("id")] = bool(r.get("met"))

    silent = [rid for rid in ladder.MEASURE
              if not (ladder.RUNG_FUNCS.get(rid) or []) and rid != "R4b"]
    chk("every rung with a measurement function also declares its code", not silent,
        ("declares nothing: %s" % silent) if silent else "R4b exempt by its own recorded note")

    for rid in SPINE:
        chk("%-5s is present in the ladder" % rid, rid in ladder.RUNG_FUNCS,
            "" if rid in ladder.RUNG_FUNCS else "absent from RUNG_FUNCS")

    # NO MEASURED RUNG ABOVE AN UNMEASURED ONE. A ladder with a hole in it is not a ladder.
    measured = [rid for rid in SPINE if rid in ladder.MEASURE]
    hole = [SPINE[i] for i in range(len(SPINE))
            if SPINE[i] not in ladder.MEASURE and any(s in ladder.MEASURE for s in SPINE[i + 1:])]
    chk("no unmeasured rung sits below a measured one", not hole, str(hole))
    chk("the spine is measured end to end", len(measured) == len(SPINE),
        "%d of %d" % (len(measured), len(SPINE)))

    chk("names checked against REACHABILITY, not existence", "reach" in str(v.get("claim", "")))
    return checks


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    res = run()
    for name, ok, detail in res:
        print("  %-56s %s%s" % (name, "ok" if ok else "FAIL", ("   " + detail) if detail else ""))
    bad = [r for r in res if not r[1]]
    print("\n  %d of %d wiring checks pass" % (len(res) - len(bad), len(res)))
    if KNOWN_UNWIRED:
        print("\n  KNOWN UNWIRED, on the record with a reason:")
        for k, why in KNOWN_UNWIRED.items():
            print("    %s\n      %s" % (k, why[:150]))
    sys.exit(1 if bad else 0)
