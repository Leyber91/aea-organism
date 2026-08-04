"""test_r5.py - R5's BEHAVIOUR, FROZEN. Every way a claim could look settled and prove nothing.

    python -m aea.lab.tests.test_r5

WHY A SEPARATE FILE FROM THE STORE'S OWN SELFTEST. `hypotheses.selftest()` proves the mechanism
against fixtures in a sandbox. This proves the LIVE STORE on disk obeys the same rules, and the
distinction is the one `research_cert` already had to make out loud: a mechanism proved against
fixtures and never against the world is a claim about the fixtures. This repo shipped a certificate
that drove `dry` ten times and `run` zero and printed CERTIFIED.

THE FIVE PROPERTIES, and each one is a way a rung could be claimed dishonestly:

    stated first    every citation was READ AFTER its claim was PROPOSED. The only property here
                    that cannot be satisfied by writing more carefully afterwards, and therefore
                    the only one that makes "stated before the evidence" mean anything
    grounded        every DIED or CORROBORATED resolves to stored, verified, citable bytes
    consequential   every DIED names what changes. A refutation that alters nothing is a diary entry
    from the record every claim names where the entity ALREADY asserted it. Without this the rung
                    certifies whatever menu a human wrote (D51: a label is not a measurement)
    honest words    SURVIVES, CONFIRMED and PROVEN are refused. Consistency is not confirmation;
                    reading it as such is affirming the consequent

AND ONE COUNT, reported rather than asserted: the gate is five runs in which something DIED. A test
that failed until the gate was met would be red for days and then deleted, so the count is printed
and the PROPERTIES are what fail. A gate is progress; these are correctness, and they must hold at
run one exactly as they will at run five.
"""
from __future__ import annotations

import sys

from aea.kernel import artefacts, hypotheses
from aea.tooling import ladder


def run() -> list:
    checks = []

    def chk(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    latest = {}
    for r in hypotheses.rows():
        if r.get("hid"):
            latest[r["hid"]] = r
    vals = list(latest.values())
    settled = [r for r in vals if r.get("status") in ("DIED", "CORROBORATED")]
    died = [r for r in settled if r["status"] == "DIED"]
    art = artefacts.rows()
    at_by = {}
    for r in art:
        for k in (r.get("id"), r.get("sha256")):
            if k:
                at_by[str(k).lower()] = float(r.get("at") or 0)

    chk("the live store holds settled claims", bool(settled), "%d settled" % len(settled))

    # ---- stated first ------------------------------------------------------------------------
    posthoc = []
    for r in settled:
        for c in (r.get("citations") or []):
            t = at_by.get(str(c).lower(), 0)
            if t and t < float(r.get("at") or 0):
                posthoc.append(r["hid"])
    chk("STATED FIRST: no citation predates its claim", not posthoc, str(sorted(set(posthoc)))[:80])

    # ---- grounded ----------------------------------------------------------------------------
    ungrounded = []
    for r in settled:
        cites = r.get("citations") or []
        if not cites:
            ungrounded.append(r["hid"])
        for c in cites:
            row = artefacts.resolve(str(c).lower(), among=art)
            if row is None:
                ungrounded.append(r["hid"])
            else:
                ok, _why = artefacts.verify(row)
                if not ok:
                    ungrounded.append(r["hid"])
    chk("GROUNDED: every verdict cites stored, verified, citable bytes",
        not ungrounded, str(sorted(set(ungrounded)))[:80])

    # ---- consequential -----------------------------------------------------------------------
    empty = [r["hid"] for r in died if not str(r.get("consequence") or "").strip()]
    chk("CONSEQUENTIAL: every DIED names what changes", not empty, str(empty)[:80])

    # ---- from the record ---------------------------------------------------------------------
    menu = [r["hid"] for r in vals if not str(r.get("from_record") or "").strip()]
    chk("FROM THE RECORD: no claim came from a menu", not menu, str(menu)[:80])
    chk("...and every claim named its killer BEFORE looking",
        all(str(r.get("killer") or "").strip() for r in vals))

    # ---- honest words ------------------------------------------------------------------------
    for word in ("SURVIVES", "CONFIRMED", "PROVEN"):
        chk("HONEST WORDS: %s is refused" % word, not hypotheses.status_is_legal(word)[0])
    chk("...and CORROBORATED is accepted", hypotheses.status_is_legal("CORROBORATED")[0])
    chk("...and DIED is accepted", hypotheses.status_is_legal("DIED")[0])
    bad_status = [r["hid"] for r in vals if not hypotheses.status_is_legal(r.get("status"))[0]]
    chk("no row on disk carries an illegal status", not bad_status, str(bad_status)[:80])

    # ---- the rung agrees with the store ------------------------------------------------------
    m = ladder.measure_r5()
    chk("the ladder MEASURES R5 at all", "why" not in m, str(m.get("why"))[:80])
    chk("the ladder's bound condition holds", m.get("condition_1"))
    chk("the ladder's honesty condition holds", m.get("condition_2"),
        "violations=%s" % m.get("violations"))
    chk("the ladder's death count agrees with the store", m.get("died") == len(died),
        "%s vs %s" % (m.get("died"), len(died)))

    # ---- the gate, REPORTED not asserted -----------------------------------------------------
    checks.append(("GATE (progress, not correctness): %d of %d runs with a death"
                   % (m.get("runs_with_a_death") or 0, ladder.R5_RUNS_GATE), True,
                   "condition_3 %s" % ("met" if m.get("condition_3") else "not yet")))
    return checks


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    res = run()
    for name, ok, detail in res:
        print("  %-62s %s%s" % (name, "ok" if ok else "FAIL", ("   " + detail) if detail else ""))
    bad = [r for r in res if not r[1]]
    print("\n  %d of %d R5 checks pass" % (len(res) - len(bad), len(res)))
    sys.exit(1 if bad else 0)
