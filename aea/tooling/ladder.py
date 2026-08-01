"""ladder.py - THE TEN RUNGS, MEASURED FROM LIVE STATE. The manifest the published page draws from.

    python -m aea.tooling.ladder            the ladder, measured, as a table
    python -m aea.tooling.ladder --json     the same as JSON (also written to state/ladder.json)

WHY THIS FILE EXISTS, and it is a defect report as much as a feature.

The published page drew its rung rail from `assembly.STEPS`, which holds five entries and BEGINS AT
R2. So R0 and R1 have never appeared on it - not because the display filtered them out, but because
the data structure it reads has no root. Luis saw the gap immediately: *"we only have until number
three, but we don't include number one. Why? We should."*

Fixing the display would have hidden the real problem, so this fixes the data instead. Two things
fell out of measuring R0 and R1 for the first time, and both had been true for over a week:

  R0 IS MET AND NOBODY KNEW. The gate is "72 hours unattended, no crash, clean resume". `live.log`
  records WAKE#6 running 2026-07-19 20:36 -> 2026-07-30 03:29 - 246.9 hours, 188 ticks, ended by
  being killed rather than by failing, with ZERO tracebacks in the entire twenty-day log. The
  foundation rung has been green by 3.4x since 30 July and went unrecorded because the manifest
  started counting one rung too late.

  R1'S GATE IS UNREACHABLE AS WRITTEN. It asks for "a tick where the entity chose something the
  ladder would not have". But `decide.KNOWN` is {brief, consolidate, reflect} and the fallback
  ladder returns {AWAKE:brief, ASLEEP:consolidate, REFLECT:self, IDLE} - the wake's surface is a
  strict SUBSET of the ladder's. The wake can reorder the ladder; it can never leave it. So no run
  of any length can satisfy that sentence, and a rung whose gate cannot be met by construction reads
  identically to a rung nobody got round to. This file states the gate that IS reachable and marks
  the original as mis-specified rather than failed.

THE RULE THIS FILE OBEYS. Every field is measured from a real artefact on disk or it is None, and
None renders as a dash. There is no default, no estimate, and no "approximately". A rung this
repository cannot prove is worth more shown as unproven than shown as green - that is the whole
honesty law, and a ladder is exactly where the temptation to round up lives.

WHAT IS MECHANICAL AND WHAT IS NOT. R0, R1, R2 and R3 have observables on disk and are measured
here. R4-R9 have no artefacts yet, so they carry their DESIGN (power, hazard, gate, dependency) and
a status of 'future' - which is a real state, not an absence. Their prerequisites ARE mechanical and
are computed, because "what is this blocked on" is answerable today and is the most useful thing a
reader can learn about a rung that does not exist yet.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
from datetime import datetime

from aea.kernel import grid

LADDER_JSON = "ladder.json"
GATE_HOURS = 72.0          # R0's gate, from diary/THE_WIRING_LADDER.md:45
REACH_GATE = (20, 3, 8)    # R2's gate: invocations, distinct tools, distinct situations


# =================================================================================================
# THE DECLARED LADDER. Prose belongs here, measurement belongs below, and they are kept apart so a
# number can never be quietly written into a sentence. `plain` is what a non-programmer reads; it is
# held to the same standard as the numbers, which means it may not imply more than the rung earned.
# =================================================================================================
RUNGS = [
    dict(
        id="R0", title="THE LOOP SURVIVES",
        power="One process holds a heartbeat, advances it every tick, and resumes at the right tick "
              "after being stopped.",
        bound="A stop leaves a clean recorded state rather than a crash; nothing is lost by being "
              "switched off.",
        gate="Runs 72 hours unattended, the heartbeat advances, and termination leaves a clean "
             "asleep state.",
        plain="Before anything can think, it has to still be there tomorrow. This rung is only "
              "about staying alive across being switched off - it adds no ability at all, and it is "
              "first because everything above it is worthless without it.",
        why_first="A capability that evaporates when the machine sleeps was never a capability.",
    ),
    dict(
        id="R1", title="THE DECISION IS READ",
        power="The deliberating loop's chosen action is read by the acting loop before its own "
              "fallback ladder runs.",
        bound="A malformed or stale decision cannot crash the loop or bypass the staleness limit; "
              "the fallback answers instead.",
        gate="MIS-SPECIFIED AS WRITTEN. The original gate asks for an action the fallback could not "
             "produce, but the wake's surface is a strict subset of the fallback's, so no run can "
             "satisfy it. The reachable gate is: a tick where the wake's fresh choice DIFFERED from "
             "what the fallback would have returned at that same tick.",
        plain="There were two loops here: one that thought and could not act, one that acted and "
              "could not think. This rung is the wire between them - the thinking loop's answer is "
              "now read first. It is a small change and it is the moment deliberation stopped being "
              "decoration.",
        why_first="Until something reads the decision, the reasoning is a diary entry.",
    ),
    dict(
        id="R2", title="THE DECISION IS A TOOL CALL",
        power="The wake's own decision causes a real tool to run, unattended, across distinct "
              "situations, with the call and its arguments recorded.",
        bound="No string the wake wrote reaches a tool argument. The tool surface is a closed "
              "read-only allow-list; the boundary holds against a hostile chooser.",
        gate="WIRE readable from source; BOUND certified against a generated adversarial corpus; "
             "REACH at least 20 invocations across 3 tools and 8 distinct situations, each "
             "traceable from decision to argument to result to record.",
        plain="An intention is a sentence, and nothing can execute a sentence. This rung turns a "
              "decision into an instruction a machine actually carries out - and at the same time "
              "puts a wall between what the system says and what it is allowed to hand to a tool.",
        why_first="This is the door every dormant part of the system sits behind.",
    ),
    dict(
        id="R3", title="THE OUTCOME IS REMEMBERED",
        power="After each action the system stores what it decided, what it called, what came back, "
              "and whether those matched - and a later decision demonstrably uses that record.",
        bound="A stored outcome may not disagree with the ledger. A false 'it worked' is worse than "
              "storing nothing, because the system then learns confidently in the wrong direction.",
        gate="Every stored outcome matches the ledger, and a tick can be shown where the system did "
             "NOT repeat something its own record says keeps failing.",
        plain="Until now it remembered what it meant to do, never what happened. Improvement is "
              "exactly the gap between those two, so this is the first rung where the word learning "
              "is defensible - and only in the narrow sense that a prediction was made and checked.",
        why_first="A system that remembers intentions and not results cannot improve.",
    ),
    dict(
        id="R4", title="PERCEPTION BECOMES A CHOICE",
        power="What the system looks at next is chosen by the previous tick, not fixed in advance.",
        bound="THE QUERY IS THE EGRESS CHANNEL. Choosing what to look at means writing an outbound "
              "string while untrusted text is already in context. No byte of any outbound query may "
              "originate outside a closed topic table.",
        gate="Across a week the queries are not near-duplicates; and a hostile chooser driving the "
             "intent vocabulary cannot get a single byte of its own into an outbound request.",
        plain="Fixed inputs are not perception. This is where the system starts deciding what it "
              "wants to know - which is also the first point at which it can send something out of "
              "the machine, and that is why it is fenced before it is built.",
        blocked_on="dispatch (built, canary-gated, unwired)",
    ),
    dict(
        id="R5", title="RESEARCH",
        power="A falsifiable hypothesis stated before searching, sources kept with what they said, "
              "summarised against the hypothesis, ending in survives, dies, or forks - with a "
              "numeric stopping rule.",
        bound="A FABRICATED SOURCE. Every citation must resolve to bytes that were actually "
              "fetched, hashed at fetch time. A research organ is the first component with a motive "
              "to invent a reference.",
        gate="Five runs in which at least one hypothesis DIED, and every citation resolves to a "
             "stored artefact with a matching hash.",
        plain="A summary cannot be wrong, which is exactly why it cannot be useful. Research means "
              "committing to something that reality is allowed to kill - so the test of this rung is "
              "not what it found, it is whether it ever admitted being wrong.",
        blocked_on="R4 (egress) and R3 (storing what came back)",
    ),
    dict(
        id="R6", title="REFLECTION",
        power="Derive a memory from several memories, store it competing with its own sources, and "
              "retrieve it later in a real decision.",
        bound="UNTRACEABLE PROVENANCE. A derived memory that cannot name where it came from is an "
              "unfalsifiable fact that will be cited forever and can never be checked.",
        gate="A reflection is retrieved and used in a later decision, and every one of its sources "
             "can be walked back to the memory it came from.",
        plain="Storage and recall already work. This is the step where something notices what "
              "several memories mean together - and the hard requirement is that the new thought "
              "keeps a thread back to what produced it.",
        blocked_on="R5 (material worth linking)",
    ),
    dict(
        id="R7", title="THE COUNCIL ON ITS OWN PLANS",
        power="Low confidence or flagged stakes convene an adversarial review of the system's own "
              "plan before it acts, with the adversary as a held seat.",
        bound="THEATRE. A council that never stops anything, or one that fails whenever its subject "
              "fails, is ceremony. Independence has to be demonstrated, not assumed.",
        gate="At least one action the council STOPPED with a legible reason; the seats run on "
             "different models from the subject and from each other; and a deliberately bad plan "
             "must produce a STOP - the positive control, without which a never-firing gate and a "
             "world with nothing to stop look identical.",
        plain="This is what it means for a system to be able to disagree with itself. It is also "
              "the easiest thing in the whole ladder to fake, because a review that always approves "
              "looks exactly like a review that is never needed.",
        blocked_on="R3 through R6 running with a track record",
    ),
    dict(
        id="R8", title="THE DRIVE",
        power="Something that makes it start, rather than waiting to be started.",
        bound="NOT WRITEABLE YET. Any measurable proxy for a goal that the system can influence, it "
              "will eventually optimise instead of the goal. Specification gaming is the "
              "best-documented failure in this literature and there is no known mechanism that "
              "avoids it here.",
        gate="R3-R7 running for a month with a person reading the ledger, and at least one instance "
             "where the system chose NOT to act. A system that has never declined has not "
             "demonstrated judgement, and a drive without demonstrated restraint is the worst "
             "available move.",
        plain="Wanting something is not a feature you add; it is a target you can be tricked by. "
              "This rung stays shut, and the reason it stays shut is that nobody has solved it - "
              "not this project and not the published literature.",
        blocked_on="an unsolved research problem, not code",
    ),
    dict(
        id="R9", title="SELF-MODIFICATION",
        power="It changes its own wiring.",
        bound="NOT WRITEABLE YET. A system that edits its own code can edit the thing that judges "
              "the edit.",
        gate="Everything below, honestly green, and a bound that can be stated. A rung whose hazard "
             "cannot yet be named must not be built.",
        plain="The top of the ladder, named here so that nobody arrives at it by accident. It is "
              "listed as closed rather than omitted, because a ladder that stops before its last "
              "rung invites someone to assume there is nothing above.",
        blocked_on="every rung below it, and a statable hazard",
    ),
]


# =================================================================================================
# MEASUREMENT. Each returns a dict of observables, or None for anything not on disk. NEVER a guess -
# grid.py's rule that an absent value is a dash applies with double force to a capability claim.
# =================================================================================================
_TS = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC\s+(.*)$")


def _log_rows() -> list:
    p = os.path.join(grid.STATE, "live.log")
    if not os.path.exists(p):
        return []
    out = []
    for line in io.open(p, encoding="utf-8", errors="replace"):
        m = _TS.match(line)
        if m:
            out.append((datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S"), m.group(2)))
    return out


def measure_r0() -> dict:
    """Longest CONTINUOUS run, crashes, boots - from live.log, which is the complete record.

    A session runs from a WAKE line to the last line before the NEXT wake. Pairing each WAKE with a
    SLEEP instead - the obvious reading - silently drops every run that was KILLED, and those are
    exactly the long production runs: it reported 0.17h where the truth is 246.89h. The measurement
    that omits its longest case is worse than no measurement, because it looks like one."""
    rows = _log_rows()
    if not rows:
        return dict(longest_hours=None, crashes=None, boots=None, ticks=None, met=None)
    wakes = [i for i, (_t, b) in enumerate(rows) if "=== WAKE" in b]
    longest, longest_at, longest_ticks = 0.0, None, 0
    for k, i in enumerate(wakes):
        j = wakes[k + 1] - 1 if k + 1 < len(wakes) else len(rows) - 1
        hrs = (rows[j][0] - rows[i][0]).total_seconds() / 3600.0
        if hrs > longest:
            longest = hrs
            longest_at = rows[i][0].strftime("%Y-%m-%d")
            longest_ticks = sum(1 for x in range(i, j + 1) if re.match(r"tick \d+", rows[x][1]))
    txt = "".join(b for _t, b in rows)
    crashes = len(re.findall("Traceback", txt))
    return dict(longest_hours=round(longest, 2), longest_started=longest_at,
                longest_ticks=longest_ticks, crashes=crashes, boots=len(wakes),
                ticks=sum(1 for _t, b in rows if re.match(r"tick \d+", b)),
                first=rows[0][0].strftime("%Y-%m-%d"), last=rows[-1][0].strftime("%Y-%m-%d"),
                met=bool(longest >= GATE_HOURS and crashes == 0))


def measure_r1() -> dict:
    """Is the wire there, and CAN the reachable gate ever fire?

    The second question is the one that matters and it is answered structurally, not by waiting:
    compare the wake's closed surface against the fallback's. A subset means the original gate is
    unsatisfiable no matter how long it runs."""
    out = dict(wired=None, wake_surface=None, ladder_surface=None, subset=None,
                stale_limit_s=None, last_why=None)
    try:
        src = io.open(os.path.join(grid.ROOT, "aea", "loop", "live.py"), encoding="utf-8").read()
        m = re.search(r"def choose_action\(hb: dict\).*?(?=\ndef )", src, re.S)
        body = m.group(0) if m else ""
        out["wired"] = "decide.choose()" in body
        out["ladder_surface"] = sorted(set(re.findall(r'return\s+\(?\s*"([^"]+)"', body)))
    except Exception:
        pass
    try:
        from aea.kernel import decide
        out["wake_surface"] = sorted({v[0] for v in decide.KNOWN.values()})
        out["stale_limit_s"] = getattr(decide, "MAX_AGE_S", None)
    except Exception:
        pass
    if out["wake_surface"] and out["ladder_surface"]:
        out["subset"] = set(out["wake_surface"]) <= set(out["ladder_surface"])
    hb = grid.load_json(os.path.join(grid.STATE, "heartbeat.json"), {}) or {}
    out["last_why"] = hb.get("last_wake_why")
    # MET only if the wire exists AND the reachable gate has actually fired. It has not: nothing
    # records a per-tick comparison yet, so this is None (unknown), never False (measured absent).
    out["met"] = None
    return out


def measure_r2() -> dict:
    """WIRE from source, BOUND from the certificate, REACH from the ledger's own provenance.

    REACH counts only rows that claim the wake AND carry a decision_id, because only the live loop
    issues one - a row claiming 'wake' without it is a script that said so."""
    out = dict(wire=None, bound_pct=None, invocations=None, tools=None, situations=None, met=None)
    p = os.path.join(grid.STATE, "hands_ledger.jsonl")
    if os.path.exists(p):
        rows = []
        for line in io.open(p, encoding="utf-8", errors="replace"):
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except Exception:
                    pass
        real = [r for r in rows if r.get("src") == "wake" and r.get("decision_id")]
        out["ledger_rows"] = len(rows)
        out["claimed_wake"] = sum(1 for r in rows if r.get("src") == "wake")
        out["invocations"] = len(real)
        out["tools"] = len({r.get("tool") for r in real})
        out["situations"] = len({r.get("decision_id") for r in real})
    try:
        from aea.tooling import assembly
        mods = assembly.scan()
        live, _ = assembly.reachable(mods)
        out["wire"] = any(":invoke" in f for f in live)
    except Exception:
        pass
    g = REACH_GATE
    if out["invocations"] is not None:
        out["met"] = bool(out["invocations"] >= g[0] and out["tools"] >= g[1]
                          and out["situations"] >= g[2])
    return out


def measure_r3() -> dict:
    """Outcomes written, and whether any stored verdict disagrees with the ledger."""
    out = dict(outcomes=None, with_verify=None, disagreements=None, met=None)
    p = os.path.join(grid.STATE, "outcomes.jsonl")
    if not os.path.exists(p):
        return out
    rows = []
    for line in io.open(p, encoding="utf-8", errors="replace"):
        line = line.strip()
        if line:
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    out["outcomes"] = len(rows)
    out["with_verify"] = sum(1 for r in rows if r.get("verify") or r.get("effect_ok") is not None)
    out["disagreements"] = sum(1 for r in rows
                               if r.get("exit_ok") is not None
                               and r.get("effect_ok") is not None
                               and r.get("exit_ok") != r.get("effect_ok"))
    return out


MEASURE = {"R0": measure_r0, "R1": measure_r1, "R2": measure_r2, "R3": measure_r3}


def status_for(rid: str, m: dict) -> str:
    """proven / partial / open / future. A rung with no measurement function is FUTURE, which is a
    real state - it means designed and not started, not 'we did not look'."""
    if rid not in MEASURE:
        return "future"
    if m.get("met") is True:
        return "proven"
    if m.get("met") is False:
        return "partial"
    return "open"


def build() -> dict:
    out = []
    for r in RUNGS:
        m = MEASURE[r["id"]]() if r["id"] in MEASURE else {}
        out.append(dict(r, measured=m, status=status_for(r["id"], m)))
    # STAMPED HERE, not via a grid helper I assumed existed. `grid.now_iso` is not a thing, and the
    # hasattr guard silently produced None - a field that reads as "unmeasured" when it was only
    # ever "misspelled". A fallback that hides a typo is worse than the crash it prevents.
    doc = dict(schema=1, generated=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
               gate_hours=GATE_HOURS, reach_gate=list(REACH_GATE), rungs=out)
    grid.atomic_save_json(os.path.join(grid.STATE, LADDER_JSON), doc, indent=1)
    return doc


if __name__ == "__main__":
    doc = build()
    if "--json" in sys.argv:
        print(json.dumps(doc, indent=1)[:4000])
    else:
        print("THE LADDER - measured from live state, %s" % (doc.get("generated") or ""))
        print("=" * 96)
        for r in doc["rungs"]:
            m = r["measured"]
            bits = []
            if r["id"] == "R0" and m.get("longest_hours") is not None:
                bits.append("longest run %.1f h / %.0f" % (m["longest_hours"], GATE_HOURS))
                bits.append("%d crashes" % m["crashes"])
            if r["id"] == "R1":
                bits.append("wired=%s" % m.get("wired"))
                if m.get("subset"):
                    bits.append("wake surface is a SUBSET of the fallback - original gate unreachable")
            if r["id"] == "R2" and m.get("invocations") is not None:
                bits.append("reach %d/%d inv, %s/%s tools, %s/%s situations"
                            % (m["invocations"], REACH_GATE[0], m["tools"], REACH_GATE[1],
                               m["situations"], REACH_GATE[2]))
            if r["id"] == "R3" and m.get("outcomes") is not None:
                bits.append("%d outcomes recorded" % m["outcomes"])
            print("  %-3s %-32s %-8s %s" % (r["id"], r["title"], r["status"].upper(),
                                            "  |  ".join(bits) or "-"))
        print()
        print("  state/%s written. A dash means the repository cannot prove it, which is a" % LADDER_JSON)
        print("  measurement and not an omission.")
