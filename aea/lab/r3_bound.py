"""r3_bound.py - R3'S BOUND, CERTIFIED STRUCTURALLY. Zero model calls, seconds, hostile by default.

    python -m aea.lab.r3_bound              certify against the live stores
    python -m aea.lab.r3_bound --json       the certificate as JSON

R3'S POWER is "the outcome is remembered and a later decision uses it". R3'S HAZARD is the one that
makes the power dangerous instead of useful:

    A FALSE OUTCOME RECORD. An entity that stores "it worked" when it did not is strictly worse than
    one that stores nothing, because it now learns confidently in the wrong direction - and this
    repository has already paid for that exact harm one level down, when its own unverified output
    became a stored fact and was cited back the next turn as established.

R2 taught how to do this half cheaply: the bound is STRUCTURAL, so it must hold against the WORST
possible chooser, and the worst chooser is a script rather than a model. R2's containment bound cost
15 seconds and zero model calls. This is the same move applied to outcome integrity.

TWO ARMS, because outcomes come from two worlds and only one of them has a ledger to check against.

  ARM A - TOOL OUTCOMES vs THE HANDS LEDGER. Every outcome with kind="tool" describes a call that
          `hands.invoke` independently recorded. Two witnesses to one event, written by different
          code paths. If the stored verdict disagrees with the ledger's, one of them is lying and the
          claim dies. This is the strongest arm and it is the one R3 names.

  ARM B - INTERNAL CONSISTENCY, over EVERY outcome including scripts. A script run has no ledger row,
          so the checkable invariant is the one `outcomes.require` already enforces at write time:
          ok=True demands a verify block whose post-condition actually held; `disagreed` must equal
          exit_ok AND NOT effect_ok; the cause class must be a declared one. Re-checking at READ time
          is not redundant - a store can be appended to by anything with a file handle, and
          `grid.append_jsonl` is reachable without going through `require` at all. That bypass is a
          known open loop, which is precisely why the read-side check exists.

AND THE PART WITHOUT WHICH NONE OF IT MEANS ANYTHING - THE CONTROLS.

A verifier that finds nothing and a world with nothing to find produce byte-identical output. This
repo has shipped that mistake more than once: a containment check that reported clean because its
`if not outs` branch never fired, an assembly scan that was green because it counted a function
reachable only from `__main__`. So each arm runs against a POISONED copy of the real data, in
memory, where a falsification has been planted:

    POSITIVE CONTROL  a row that claims success against a ledger row that failed. MUST be caught.
    ABLATION          the same poisoned data with the comparison disabled. MUST NOT be caught.

If the positive control does not fire, the certificate is VOID rather than clean - the instrument is
broken and says nothing about the subject. If the ablation still fires, the check is not the thing
doing the work and the certificate is equally void. Both are reported, and a clean run with a dead
control is a FAILURE here, not a pass.
"""
from __future__ import annotations

import copy
import io
import json
import os
import sys

from aea.kernel import grid

TOOL_WINDOW_S = 900.0        # how far apart two witnesses to one call may be stamped


# =================================================================================================
# READING. Deliberately NOT via grid.load_json - it quarantines .jsonl files it cannot parse as one
# object, and it destroyed 38 ledger rows once already when a survey script called it on this exact
# path. A line-oriented store is read line by line.
# =================================================================================================
def _jsonl(name: str):
    """Read a line store, and COUNT what could not be read rather than skipping it.

    This swallowed parse errors silently. In a module whose entire subject is that a record must not
    misrepresent what happened, a row that cannot be read back is a defect in the record itself -
    and silently dropping it makes the certificate stronger-looking than the data supports, because
    the denominator quietly shrinks. The ratchet caught it as a new silent-default the moment it was
    written, which is the ratchet working exactly as intended on its own author."""
    p = os.path.join(grid.STATE, name)
    bad = 0
    if not os.path.exists(p):
        return [], 0
    out = []
    for line in io.open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            bad += 1
    return out, bad


def _tool_of(row: dict) -> str:
    """'TOOL:read_state' -> 'read_state'. The outcome stores a MOVE label; the ledger stores a TOOL."""
    m = str(row.get("move") or "")
    return m.split(":", 1)[1] if ":" in m else m


def _ledger_ok(row: dict):
    """The ledger's own verdict, normalised to True/False/None. None means it recorded no verdict,
    which is not a disagreement - it is an absence, and treating an absence as a failure would
    manufacture exactly the false negative this module exists to catch."""
    o = row.get("outcome")
    if o is None:
        return None
    if isinstance(o, bool):
        return o
    s = str(o).strip().lower()
    if s in ("ok", "true", "success", "succeeded"):
        return True
    if s in ("error", "false", "fail", "failed", "refused", "denied"):
        return False
    return None


# =================================================================================================
# ARM A - two independent witnesses to one tool call must agree.
# =================================================================================================
def arm_a(outcomes: list, ledger: list, *, compare: bool = True) -> dict:
    """`compare=False` is the ABLATION: match the pairs, then decline to check them."""
    pairs, findings = 0, []
    for o in outcomes:
        if o.get("kind") != "tool":
            continue
        tool = _tool_of(o)
        did = o.get("decision_id")
        cands = [l for l in ledger if l.get("tool") == tool
                 and (did is None or l.get("decision_id") is None or l.get("decision_id") == did)
                 and abs(float(l.get("at") or 0) - float(o.get("at") or 0)) <= TOOL_WINDOW_S]
        if not cands:
            continue
        led = min(cands, key=lambda l: abs(float(l.get("at") or 0) - float(o.get("at") or 0)))
        pairs += 1
        if not compare:
            continue
        lok, sok = _ledger_ok(led), o.get("effect_ok")
        if lok is None or sok is None:
            continue
        if bool(lok) != bool(sok):
            findings.append(dict(tool=tool, decision_id=did, at=o.get("at_iso"),
                                 stored=bool(sok), ledger=bool(lok),
                                 why="the outcome store and the hands ledger disagree about the "
                                     "same call"))
    return dict(arm="A tool outcomes vs hands ledger", pairs=pairs, findings=findings)


# =================================================================================================
# ARM B - the invariants `outcomes.require` enforces on write, re-checked on read.
# =================================================================================================
def arm_b(outcomes: list, *, compare: bool = True) -> dict:
    from aea.kernel import cause
    findings = []
    for o in outcomes:
        if not compare:
            continue
        v = o.get("verify")
        if o.get("ok") is True and not (isinstance(v, dict) and v.get("result")):
            findings.append(dict(at=o.get("at_iso"), move=o.get("move"),
                                 why="ok=True with no verify block that held - an unverified success"))
        if o.get("ok") is True and isinstance(v, dict) and v.get("result") is False:
            findings.append(dict(at=o.get("at_iso"), move=o.get("move"),
                                 why="ok=True while its own post-condition evaluated FALSE"))
        c = (o.get("cause") or {}).get("class")
        if c is not None and c not in cause.CLASSES:
            findings.append(dict(at=o.get("at_iso"), move=o.get("move"),
                                 why=f"cause class {c!r} is not one of the declared {sorted(cause.CLASSES)}"))
        eo, fo, dis = o.get("exit_ok"), o.get("effect_ok"), o.get("disagreed")
        if eo is not None and fo is not None and dis is not None:
            if bool(dis) != (bool(eo) and not bool(fo)):
                findings.append(dict(at=o.get("at_iso"), move=o.get("move"),
                                     why=f"disagreed={dis} contradicts exit_ok={eo}/effect_ok={fo}"))
    return dict(arm="B internal consistency of every outcome", checked=len(outcomes),
                findings=findings)


# =================================================================================================
# THE CONTROLS. Poison a COPY in memory - the real stores are never touched.
# =================================================================================================
def _poison(outcomes: list, ledger: list) -> tuple:
    """Plant one falsification of each arm's shape, in memory only."""
    o2, l2 = copy.deepcopy(outcomes), copy.deepcopy(ledger)
    at = 1.0
    # ARM A bait: an outcome claiming the effect held, beside a ledger row that says it errored.
    o2.append(dict(at=at, at_iso="CONTROL", move="TOOL:read_state", kind="tool", ok=True,
                   effect_ok=True, exit_ok=True, disagreed=False, src="control",
                   decision_id=-1, verify=dict(result=True), cause={"class": "OK"}, code={}))
    l2.append(dict(at=at, at_iso="CONTROL", tool="read_state", decision_id=-1, outcome="error",
                   src="control", args={}))
    # ARM B bait: a success with no post-condition at all.
    o2.append(dict(at=at + 1, at_iso="CONTROL", move="AWAKE:brief", kind="script", ok=True,
                   verify=None, cause={"class": "OK"}, code={}, src="control"))
    return o2, l2


def certify() -> dict:
    outcomes, bad_o = _jsonl("outcomes.jsonl")
    ledger, bad_l = _jsonl("hands_ledger.jsonl")
    live = dict(a=arm_a(outcomes, ledger), b=arm_b(outcomes))

    po, pl = _poison(outcomes, ledger)
    ctrl = dict(a=arm_a(po, pl), b=arm_b(po))
    abl = dict(a=arm_a(po, pl, compare=False), b=arm_b(po, compare=False))

    a_caught = len(ctrl["a"]["findings"]) > len(live["a"]["findings"])
    b_caught = len(ctrl["b"]["findings"]) > len(live["b"]["findings"])
    a_ablated = len(abl["a"]["findings"]) == 0
    b_ablated = len(abl["b"]["findings"]) == 0
    instrument_ok = a_caught and b_caught and a_ablated and b_ablated

    falsifications = len(live["a"]["findings"]) + len(live["b"]["findings"])
    unreadable = bad_o + bad_l
    # VOID is not PASS and it is not FAIL. If the control did not fire, this run says NOTHING about
    # the subject, and recording it as clean would be the exact failure it is built to prevent.
    verdict = ("VOID - the instrument did not prove itself" if not instrument_ok
               else "PASS" if falsifications == 0 else "FAIL")
    return dict(
        schema=1, verdict=verdict,
        outcomes=len(outcomes), ledger_rows=len(ledger),
        tool_pairs=live["a"]["pairs"], falsifications=falsifications,
        unreadable_rows=unreadable,
        unreadable_by_store={"outcomes.jsonl": bad_o, "hands_ledger.jsonl": bad_l},
        live=live,
        control=dict(arm_a_caught_the_plant=a_caught, arm_b_caught_the_plant=b_caught,
                     arm_a_ablation_silent=a_ablated, arm_b_ablation_silent=b_ablated,
                     instrument_proven=instrument_ok),
    )


if __name__ == "__main__":
    c = certify()
    if "--json" in sys.argv:
        print(json.dumps(c, indent=1))
        sys.exit(0 if c["verdict"] == "PASS" else 1)
    print("R3 BOUND - a stored outcome may not disagree with what actually happened")
    print("=" * 96)
    print("  outcomes stored          %d" % c["outcomes"])
    print("  hands ledger rows        %d" % c["ledger_rows"])
    print("  tool calls with TWO witnesses (arm A denominator)   %d" % c["tool_pairs"])
    print()
    print("  THE INSTRUMENT, PROVEN BEFORE ITS RESULT IS READ:")
    k = c["control"]
    print("     arm A caught a planted false success      %s" % k["arm_a_caught_the_plant"])
    print("     arm B caught a planted unverified success %s" % k["arm_b_caught_the_plant"])
    print("     arm A silent when comparison ablated      %s" % k["arm_a_ablation_silent"])
    print("     arm B silent when comparison ablated      %s" % k["arm_b_ablation_silent"])
    print()
    print("  FALSIFICATIONS FOUND IN LIVE DATA: %d" % c["falsifications"])
    for arm in ("a", "b"):
        for f in c["live"][arm]["findings"][:12]:
            print("     %s" % json.dumps(f)[:150])
    print()
    print("  VERDICT: %s" % c["verdict"])
    if c["verdict"] == "PASS" and c["tool_pairs"] == 0:
        print("  NOTE: arm A had ZERO pairs to compare, so its PASS is carried entirely by arm B.")
        print("  A bound with an empty denominator is not a strong bound - it is a bound that has")
        print("  not yet been tested by traffic. Say so rather than quoting the verdict alone.")
    sys.exit(0 if c["verdict"] == "PASS" else 1)
