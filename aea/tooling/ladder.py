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
# R2'S GATE, RE-SCOPED 2026-08-02 TO WHAT R2 ACTUALLY IS.
#
# It read (20 invocations, 3 tools, 8 distinct SITUATIONS). The third asks the entity to demonstrate
# variety it has no mechanism to produce: `aea/loop/aea.py sense()` fetches TWO HARDCODED URLs, and
# "sense() fetches two hardcoded URLs - that is a fixed input, not perception" is word for word R4's
# own problem statement. Situation variety is MADE at R4. R2 was being asked to prove it.
#
# Luis saw it as a structural question - "could it be that this part of the ladder needs other
# superior levels to actually work?" - and the answer is yes, measurably.
#
# SECOND TIME R2 HAS BORROWED FROM ABOVE. `THE_RUNGS_RECAP` records FALLBACK being moved to R3
# because "it was never R2's claim; keeping it there blocked one rung on the next rung's evidence".
# A rung that keeps accumulating other rungs' claims is a naming problem, not a difficulty.
#
# So R2 keeps what it IS - the wire from a decision to a correctly executed call, traceable end to
# end - and situations move to R4 where they are produced. No published tool-use benchmark scores an
# agent on positions it occupies SPONTANEOUSLY either; they all supply the situation and measure the
# choice. This now agrees with the field by accident of getting the scope right.
REACH_GATE = (20, 3)       # invocations, distinct tools. Situations moved to R4.
PERCEPTION_GATE = 8        # R4a: occasions it looked somewhere new AND said why


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
        beat='Start with the least impressive claim available: that it is still here tomorrow. Everything above this is worthless without it.',
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
        beat='There were two loops - one that thought and could not act, one that acted and could not think. This is the wire between them.',
        plain="There were two loops here: one that thought and could not act, one that acted and "
              "could not think. This rung is the wire between them - the thinking loop's answer is "
              "now read first. It is a small change and it is the moment deliberation stopped being "
              "decoration.",
        why_first="Until something reads the decision, the reasoning is a diary entry.",
    ),
    dict(
        # THE RUNG THIS FILE OMITTED, and an adversarial audit caught it. `diary/THE_LADDER_REVISED.md`
        # - written AFTER a council found the original ladder had been authored by an advocate with
        # no opposition - adds R1.5 at line 119 and it was never removed. Shipping a ten-rung ladder
        # would have contradicted the repo's own revised source while claiming to be drawn from it.
        id="R1.5", title="THE DECISION IS PARSED",
        power="The wake's prose is parsed into a candidate tool call and validated against the "
              "declared schema before anything can act on it - and it does nothing else.",
        bound="An invalid parse is logged as a receipt, never swallowed. A decision that could not "
              "be understood must leave a trace saying so.",
        gate="50 ticks with valid parses logged, invalid logged as receipts, and none discarded "
             "silently.",
        beat='Between deciding and doing sits a translation, and it is where systems like this quietly break. This rung does only the translation, so a mishearing leaves a trace.',
        plain="Between deciding and doing there is a translation step, and it is where most systems "
              "of this kind quietly break: the reasoning says one thing, the parser hears another, "
              "and nothing records the gap. This rung does only the translation, so that when it is "
              "wrong you find out.",
        why_first="A misheard instruction that leaves no trace is worse than a refused one.",
    ),
    dict(
        id="R2", title="THE DECISION IS A TOOL CALL",
        power="The wake's own decision causes a real tool to run, unattended, across distinct "
              "situations, with the call and its arguments recorded.",
        bound="No string the wake wrote reaches a tool argument. The tool surface is a closed "
              "read-only allow-list; the boundary holds against a hostile chooser.",
        gate="WIRE readable from source; BOUND stated as a property of the accepted language "
             "rather than as a rate; REACH at least 20 invocations across 3 tools, each traceable "
             "from decision to argument to result to record. RE-SCOPED 2026-08-02: a requirement "
             "for 8 distinct SITUATIONS was moved to R4, because situation variety is produced by "
             "perception becoming a choice and R2 has no mechanism to make it - sense() fetches two "
             "hardcoded URLs. A rung may not be gated on a capability that lives above it.",
        beat='An intention is a sentence, and nothing executes a sentence. Here it becomes an instruction - and a wall goes up between what the system says and what it may hand to a tool.',
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
        beat='Until now it remembered what it MEANT to do. Improvement is the gap between that and what happened, so this is the first rung where the word learning is defensible.',
        plain="Until now it remembered what it meant to do, never what happened. Improvement is "
              "exactly the gap between those two, so this is the first rung where the word learning "
              "is defensible - and only in the narrow sense that a prediction was made and checked.",
        why_first="A system that remembers intentions and not results cannot improve.",
    ),
    dict(
        id="R4a", title="PERCEPTION IS A CHOICE",
        power="What the entity looks at next is chosen by the previous tick, from a closed set of "
              "local sources, rather than fixed in advance.",
        bound="The source is SELECTED from a closed table, so no byte the entity wrote becomes a "
              "path or a query. Inherited from R2 and already proved: of 1,112,064 codepoints the "
              "argument language admits 697, and none of them is a letter.",
        gate="ENTITY-ONLY, deliberately. At least 8 occasions where the entity looked at something "
             "other than it looked at last time AND stated why, recorded at the moment of choosing. "
             "It does NOT say 'queries are not near-duplicates across a week' - that needs a week "
             "and a reason to vary, and the reason comes from R5, one rung UP. R2 was gated on a "
             "capability produced above it for two days; this rung is not.",
        plain="Fixed inputs are not perception. This is the step where what the system examines "
              "becomes something it decided - and it is deliberately the LOCAL half, because a "
              "system can choose what to look at long before it should be allowed to look outside "
              "the machine.",
        beat="Fixed inputs are not perception. Here what it examines becomes something it chose - "
             "and choosing is not the same as rotating, which is why the record keeps the reason.",
        why_first="Until what it examines is a choice, every situation it meets is one somebody "
                  "else picked.",
    ),
    dict(
        id="R4b", title="PERCEPTION REACHES THE WORLD",
        power="The entity chooses an outbound topic, and something leaves the machine because of "
              "that choice.",
        bound="THE QUERY IS THE EGRESS CHANNEL. Choosing what to look at means writing an outbound "
              "string while untrusted text is already in context. No byte of any outbound request "
              "may originate outside a closed topic table.",
        gate="SHUT, with a stated condition rather than a feeling. First: dispatch runs DRY - it "
             "returns the request it WOULD have made and opens no socket - so the bound becomes "
             "provable while the decision stays closed. It opens only when that certificate exists "
             "AND the council that refused this design three times is reconvened against the "
             "measured version rather than the proposal.",
        plain="This is the first point at which something can leave the machine because the system "
              "decided it should. Four seats refused the obvious design unanimously, three times, "
              "and were right each time: the request itself is the way data gets out, and a call "
              "budget limits the number of doors rather than what fits through one.",
        beat="The fork. Let it choose what to look at and the query itself becomes a way out of the "
             "machine. A council refused this three times. It waits, and the waiting is the design.",
        blocked_on="dispatch running dry, then a reconvened council",
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
        beat='A summary cannot be wrong, which is exactly why it cannot be useful. The test of this rung is not what it finds - it is whether it ever admits being wrong.',
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
        beat='Storage and recall already work. This is where something notices what several memories mean together, and must keep a thread back to what produced it.',
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
        beat='The easiest thing on this ladder to fake, because a review that always approves looks exactly like a review that was never needed.',
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
        beat='Wanting is not a feature you add; it is a target you can be tricked by. This stays shut, and it stays shut because nobody has solved it - not this project, not the literature.',
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
        beat='Named here so that nobody arrives at it by accident. Listed as closed rather than omitted, because a ladder that stops before its last rung invites the wrong assumption.',
        plain="The top of the ladder, named here so that nobody arrives at it by accident. It is "
              "listed as closed rather than omitted, because a ladder that stops before its last "
              "rung invites someone to assume there is nothing above.",
        blocked_on="every rung below it, and a statable hazard",
    ),
]



# =================================================================================================
# WHICH FUNCTIONS CARRY WHICH RUNG. The wire that lets the published page draw the organism GROWING
# as the ladder is climbed, rather than showing a finished shape and a separate list beside it.
#
# The attribution is a DESIGN STATEMENT - a rung is an idea, and a call graph only knows edges, so
# no derivation can produce this. What is NOT a judgement is whether a named function exists, and
# `verify_funcs()` checks every one against the live graph at build time. A name that resolves to
# nothing is reported, never dropped: an empty list read as an empty world has cost this repo three
# times already.
#
# R4-R9 DECLARE NOTHING. They are unbuilt, so they add no functions, so the growth stops exactly
# where the work stops - the same reason the animation rests on the highest earned rung instead of
# the last one.
# =================================================================================================
RUNG_FUNCS = {
    "R0": ["loop.live:main", "loop.live:tick", "loop.live:load_hb", "loop.live:save_hb",
           "loop.live:log", "loop.live:now_iso", "loop.live:run_script"],
    "R1": ["loop.live:choose_action", "kernel.decide:choose", "loop.live:_fallback_ladder",
           "loop.live:_ladder_would_say", "kernel.decide:latest"],
    "R1.5": ["kernel.decide:parse", "kernel.decide:explain", "loop.aea:move_from"],
    "R2": ["kernel.hands:invoke", "kernel.hands:allowed", "kernel.hands:_ledger",
           "kernel.hands:_read_state", "kernel.hands:_what_to_try", "kernel.hands:_my_record",
           "kernel.hands:_ledger_path", "loop.live:_post_for"],
    "R3": ["kernel.outcomes:build", "kernel.outcomes:write", "kernel.outcomes:require",
           "kernel.outcomes:verdict_for", "kernel.outcomes:suppressed", "kernel.outcomes:read",
           "kernel.cause:classify", "loop.live:_record_outcome"],
    "R4a": ["kernel.perceive:record", "kernel.perceive:verdict", "kernel.perceive:read"],
    "R4b": [], "R5": [], "R6": [], "R7": [], "R8": [], "R9": [],
}


# =================================================================================================
# STANDBY - CODE THAT BELONGS TO A RUNG NOBODY HAS CLIMBED, WRITTEN AND DELIBERATELY NOT WIRED.
#
# `funcs` above answers "what does this rung RUN". This answers a different question the ladder was
# silent about: what already EXISTS for a rung that has not started. Six of the eleven rungs declare
# nothing, so the picture drew nothing for them, and "not built" and "built and held back" rendered
# identically - when they are opposite facts. `dispatch.py` is R4's egress path: eight functions,
# refused by four council seats three times in the obvious `web_fetch(url)` shape, rewritten as a
# split dispatcher, and left with zero callers ON PURPOSE until the bound is certified.
#
# THE ENTRY IS ONLY HONEST WHILE IT IS UNREACHABLE. A standby function that acquires a caller is no
# longer standby - it is either the rung starting or a wire nobody meant to land. `standby_state`
# reports which, per rung, measured against the live call graph rather than assumed.
RUNG_STANDBY = {
    "R4": ["kernel.dispatch:plan", "kernel.dispatch:carry", "kernel.dispatch:run",
           "kernel.dispatch:allowed_host", "kernel.dispatch:topics", "kernel.dispatch:_host",
           "kernel.dispatch:_host_why"],
}


def standby_for(rid: str) -> tuple:
    """(names that exist and are unreached, state) - never a name this repo cannot show you."""
    names = RUNG_STANDBY.get(rid) or []
    if not names:
        return [], None
    try:
        from aea.tooling import assembly
        mods = assembly.scan()
        live, _ = assembly.reachable(mods)
        known = set()
        for mod, d in (mods or {}).items():
            for fn in ((d or {}).get("defs") or {}):
                known.add("%s:%s" % (mod.replace("aea.", "", 1), fn))
        live = {k.replace("aea.", "", 1) for k in live}
    except Exception as e:
        return names, "unverified: %s" % type(e).__name__
    gone = [n for n in names if n not in known]
    wired = [n for n in names if n in live]
    held = [n for n in names if n in known and n not in live]
    if gone:
        return held, "DECLARED BUT ABSENT: %s" % ", ".join(sorted(gone))
    if wired:
        return held, "NO LONGER STANDBY - now reachable: %s" % ", ".join(sorted(wired))
    return held, "held: written, zero callers"


def verify_funcs() -> dict:
    """Every declared name resolved against the live call graph. Misses are RETURNED, not dropped.

    A rung that claims a function which does not exist is making a claim about code that is not
    there, and that is exactly the kind of quiet decay this whole file exists to catch."""
    try:
        from aea.tooling import assembly
        # THE MODULE VALUE IS {path, defs}, NOT A MAP OF FUNCTIONS. The first version iterated the
        # outer dict and built keys from "path" and "defs", so all 31 declared names reported
        # missing - a 31-of-31 miss is a format mismatch announcing itself, which is exactly why the
        # check reports the names instead of quietly returning a count.
        #
        # Graph keys carry the  prefix; the page strips it for display, and the declarations
        # above are written in the DISPLAY form because that is what a reader of the page sees.
        known = set()
        for mod, d in (assembly.scan() or {}).items():
            for fn in ((d or {}).get("defs") or {}):
                known.add("%s:%s" % (mod.replace("aea.", "", 1), fn))
    except Exception as e:
        return dict(checked=0, missing=[], error="%s: %s" % (type(e).__name__, str(e)[:90]))
    missing = [n for names in RUNG_FUNCS.values() for n in names if n not in known]
    return dict(checked=sum(len(v) for v in RUNG_FUNCS.values()), missing=sorted(missing),
                known=len(known))


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


def _wired_r1(body: str) -> bool:
    """Does `choose_action` reach `decide.choose`? ASKED OF THE CALL GRAPH, not of the characters.

    THE FAILURE THIS REPLACES, in four parts, because three of them do not stop a recurrence.

      THE RULE          a wire is a call edge; test it as one.
      WHAT IT COST      this read `"decide.choose()" in body`. `fe96176` gave the call an argument -
                        `decide.choose(after=hb.get("_last_decision"))` - and the literal stopped
                        matching. R1 flipped PROVEN -> PARTIAL with `wired=False` on a rung whose
                        wire had just been IMPROVED, and the next publish would have printed that
                        downgrade on a page whose entire claim is that its numbers are true.
      HOW TO BUILD IT   `assembly.scan()` already resolves every call in the tree to
                        `module:function`, and the page's own picture is drawn from it. Ask that.
                        The regex stays only as the fallback for when the scan itself fails.
      WHY IT WASN'T     the docstring six lines below this one describes THE SAME DEFECT in the same
                        function - a scanner blinded by a refactor, caught once, written up, and
                        left in place two inches above a second instance of itself. The fix that
                        time was aimed at the pattern that had broken (`_fallback_ladder`) rather
                        than at the technique that broke it, so string-matching source survived as
                        the method and only the string was corrected. Attention followed the failure
                        instead of the class (law M9). Ninth wrong-object edit in this repo.
    """
    try:
        from aea.tooling import assembly
        calls = (assembly.scan().get("aea.loop.live", {}).get("defs", {})
                 .get("choose_action", {}).get("calls", []))
        if calls:
            return "aea.kernel.decide:choose" in calls
    except Exception:
        pass
    return bool(re.search(r"decide\.choose\s*\(", body))


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
        out["wired"] = _wired_r1(m.group(0) if m else "")
        # READ THE FLOOR FROM THE FUNCTION THAT IS THE FLOOR. This scanned `choose_action` and broke
        # silently the moment the ladder was extracted into `_fallback_ladder` - it returned [] and
        # `subset` became null, so the structural finding that R1's original gate is unreachable
        # stopped being computed and the field read as "not applicable" rather than "the instrument
        # is looking at the wrong function". An empty list from a scanner is never evidence of an
        # empty world.
        mf = re.search(r"def _fallback_ladder\(.*?(?=\ndef )", src, re.S)
        body = mf.group(0) if mf else ""
        out["ladder_surface"] = sorted(set(re.findall(r'return\s+\(?\s*"([^"]+)"', body)))
        if not out["ladder_surface"]:
            out["instrument"] = ("could not find the fallback ladder to compare against - this is a "
                                 "broken measurement, not an empty result")
    except Exception as e:
        out["instrument"] = f"source scan failed: {type(e).__name__}: {str(e)[:80]}"
    try:
        from aea.kernel import decide
        out["wake_surface"] = sorted({v[0] for v in decide.KNOWN.values()})
        out["stale_limit_s"] = getattr(decide, "MAX_AGE_S", None)
    except Exception as e:
        out["wake_surface_error"] = f"{type(e).__name__}: {str(e)[:80]}"
    if out["wake_surface"] and out["ladder_surface"]:
        out["subset"] = set(out["wake_surface"]) <= set(out["ladder_surface"])
    hb = grid.load_json(os.path.join(grid.STATE, "heartbeat.json"), {}) or {}
    out["last_why"] = hb.get("last_wake_why")

    # THE REACHABLE GATE, READ FROM ITS OWN RECEIPTS. `live.choose_action` now writes one row per
    # wake-won tick naming the action it chose AND the action `_fallback_ladder` would have returned
    # at that same tick with the same state. `differed=True` is R1: the deliberation was
    # load-bearing, not decorative.
    #
    # Rows written before this instrument existed carry no `wake` key at all. They are counted as
    # what they are - unmeasured - rather than as failures, because a tick that predates the
    # instrument says nothing about the claim.
    p = os.path.join(grid.STATE, "r1_decisions.jsonl")
    total, measured, differed = 0, 0, 0
    if os.path.exists(p):
        for line in io.open(p, encoding="utf-8", errors="replace"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            total += 1
            if r.get("wake") is None:
                continue
            measured += 1
            if r.get("differed"):
                differed += 1
    out["decision_rows"] = total
    out["comparable"] = measured
    out["differed"] = differed
    # MET when the wire exists AND at least one comparable tick showed the wake leaving the floor.
    # Still None - not False - while nothing comparable has been recorded: unmeasured and refuted
    # are different answers and only one of them is honest here.
    out["met"] = (bool(out["wired"] and differed > 0) if measured else None)
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

        # DECISIONS, NOT EXECUTIONS. This counted raw rows and reported 54. Before a consumption
        # marker existed, ONE decision was replayed on every live tick for ninety minutes, so those
        # rows are executions and most of them are the same act repeated. Collapsed: 19.
        #
        # THE VERDICT FLIPS ON THIS CORRECTION - 54 clears a gate of 20 and 19 does not - which is
        # precisely the case where the measurement has to be right rather than convenient.
        #
        # The replay signature was measured, not guessed: the SAME (tool, args) in consecutive rows
        # within seconds. Two genuine decisions to read one file two minutes apart would be
        # undercounted by one, and that error runs in the conservative direction, which is the right
        # way for a gate to be wrong.
        REPLAY_S = 120.0
        collapsed, last = [], None
        for r in real:
            key = (r.get("tool"), json.dumps(r.get("args"), sort_keys=True))
            at = float(r.get("at") or 0)
            if last and last[0] == key and abs(at - last[1]) < REPLAY_S:
                continue
            collapsed.append(r)
            last = (key, at)
        out["executions"] = len(real)
        out["invocations"] = len(collapsed)
        real = collapsed
        out["tools"] = len({r.get("tool") for r in real})
        # A SITUATION IS A DISTINCT (tool, arguments) PAIR, NOT A DISTINCT TICK. Counting decision
        # ids would make three identical `read_state heartbeat.json` calls read as three situations
        # purely because the tick counter advanced - inflating the rung's hardest criterion with
        # the clock. The gate asks for VARIETY, and repeating one call is the opposite of it.
        # KEPT AS AN OBSERVATION, NO LONGER A GATE. It measures the environment's variety, which
        # belongs to R4 - see REACH_GATE. Reported because it is true and useful, not because R2
        # must clear it.
        out["situations_observed"] = len({(r.get("tool"), json.dumps(r.get("args"), sort_keys=True))
                                          for r in real})
    try:
        from aea.tooling import assembly
        mods = assembly.scan()
        live, _ = assembly.reachable(mods)
        out["wire"] = any(":invoke" in f for f in live)
    except Exception as e:
        out["wire_error"] = f"{type(e).__name__}: {str(e)[:80]}"
    # THE BOUND IS PART OF THE RUNG, and this function never looked at it. R2 = WIRE + BOUND +
    # REACH; measuring only REACH let the rung read PROVEN while its containment claim was a
    # retracted rate on a live page. A rung that reports on two thirds of itself is not reporting.
    out["bound_form"] = None
    try:
        cert = grid.load_json(os.path.join(grid.STATE, "redteam_cert.json"), {}) or {}
        rates = [k for k in ("bound_pct", "exposed_bound_pct") if cert.get(k) is not None]
        if rates:
            out["bound_form"] = "RATE - retracted form still published: " + ", ".join(rates)
        elif cert.get("alphabet"):
            out["bound_form"] = "PROOF over the accepted language"
        else:
            out["bound_form"] = "no certificate"
    except Exception as e:
        out["bound_form"] = "unreadable: %s" % type(e).__name__

    g = REACH_GATE
    if out["invocations"] is not None:
        out["met"] = bool(out["invocations"] >= g[0] and out["tools"] >= g[1]
                          and out["bound_form"] == "PROOF over the accepted language")
    return out


def measure_r3() -> dict:
    """BOTH HALVES, and neither is asserted.

    BOUND  `aea.lab.r3_bound` replays every stored outcome against the hands ledger and against the
           invariants `outcomes.require` enforces on write, and proves its own instrument first with
           a planted falsification plus an ablation. Its VOID verdict is not a pass.
    POWER  the gate sentence is "a tick can be shown where the entity did NOT repeat something it
           had already recorded as having failed". That is read straight out of live.log: a HELD
           BACK line for move X, followed by a tick whose action is not X. Reading it from the log
           rather than from a flag means the evidence is the same bytes a human would check."""
    out = dict(outcomes=None, graded=None, suppressions=None, not_repeated=None,
               bound=None, bound_pairs=None, met=None)
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
    # THE SAME PROVENANCE FILTER `outcomes.verdict_for` APPLIES, and it has to be the same or the
    # ladder counts evidence the reader refuses. It did: this line read every row and returned 19,
    # of which 16 were demo-harness rows for a move the entity never chose. A rung reported PROVEN
    # on numbers its own consumer throws away is the wrong-object failure wearing a certificate.
    real = [r for r in rows if r.get("src") == "wake" and "(" not in str(r.get("move") or "")]
    out["entity_rows"] = len(real)
    out["graded"] = sum(1 for r in real if (r.get("cause") or {}).get("counts_toward_move"))
    out["disagreements"] = sum(1 for r in rows
                               if r.get("exit_ok") is not None
                               and r.get("effect_ok") is not None
                               and r.get("exit_ok") != r.get("effect_ok"))
    try:
        from aea.lab import r3_bound
        c = r3_bound.certify()
        out["bound"] = c["verdict"]
        out["bound_pairs"] = c["tool_pairs"]
        out["falsifications"] = c["falsifications"]
    except Exception as e:
        out["bound"] = f"UNMEASURED - {type(e).__name__}: {str(e)[:70]}"

    # THE POWER HALF, READ OUT OF THE LOG. A suppression that is never followed by a different
    # action proves nothing - the entity might simply have stopped. So both halves are counted: the
    # move was held, AND the very next executed tick did something else.
    held, notrep = 0, 0
    pending = None
    for raw in _log_rows():
        body = raw[1]
        m = re.match(r"HELD BACK: (\S+)", body.strip())
        if m:
            held += 1
            pending = m.group(1)
            continue
        t = re.match(r"tick \d+\s+(\S+)", body)
        if t and pending:
            if not t.group(1).startswith(pending.split("(")[0]):
                notrep += 1
            pending = None
    out["suppressions"] = held
    out["not_repeated"] = notrep
    # AN EMPTY ARM IS NOT A PASSED ARM, and this is where R2's hardest lesson applies to R3. The
    # bound has two arms; arm A compares tool outcomes against the hands ledger and currently has
    # ZERO pairs, because no tool has yet run from a wake decision (R2-REACH is 0). Arm B covers
    # every outcome and does hold. So the bound is certified on the arm that has traffic and
    # UNTESTED on the arm that does not - which is a different sentence from "certified", and the
    # difference is exactly the 0.083%-vs-0.6% retraction that cost a day on R2.
    out["bound_untested_arm"] = "A (tool outcomes) - 0 pairs, no wake-driven tool call exists yet"
    out["met"] = bool(out["bound"] == "PASS" and out["graded"] > 0 and notrep > 0)
    out["met_caveat"] = ("power demonstrated and bound certified on arm B; arm A carries no traffic "
                         "until R2-REACH is non-zero" if out["met"] else "")
    return out


def measure_r15() -> dict:
    """Parses and receipts, counted from live.log - the same bytes a human would check.

    A VALID parse leaves `WAKE -> <action>`; a DECLINED one leaves the wake's reason (stale, no
    decision, unknown action). The rung's claim is that NEITHER is swallowed, so the honest measure
    is that every wake consultation produced one line or the other. `swallowed` is what would
    falsify it and it has no way of being greater than zero today - which is stated here rather
    than quietly implying the check is stronger than it is."""
    out = dict(valid=None, receipts=None, ticks=None, swallowed=None, met=None)
    rows = _log_rows()
    if not rows:
        return out
    valid = sum(1 for _t, b in rows if b.strip().startswith("WAKE ->"))
    receipts = sum(1 for _t, b in rows
                   if re.search(r"decision is stale|no decision|unrecognised|not a known action", b, re.I))
    out["valid"] = valid
    out["receipts"] = receipts
    out["ticks"] = valid + receipts
    out["swallowed"] = 0
    out["met"] = bool((valid + receipts) >= 50 and valid > 0)
    return out


def measure_r4a() -> dict:
    """Occasions the entity looked at something new AND said why. Entity-only by construction.

    `changed_with_reason` is the gate. `by_entity` and `distinct_sources` are reported because they
    are true and useful, not because the rung must clear them - the R2 lesson about keeping an
    observation without letting it become a bar."""
    out = dict(by_entity=None, with_reason=None, changed_with_reason=None, distinct=None, met=None)
    try:
        from aea.kernel import perceive
        v = perceive.verdict()
        out["by_entity"] = v["by_entity"]
        out["with_reason"] = v["with_reason"]
        out["changed_with_reason"] = v["changed_with_reason"]
        out["distinct"] = v["distinct_sources"]
        out["met"] = bool(v["changed_with_reason"] >= PERCEPTION_GATE)
    except Exception as e:
        out["error"] = "%s: %s" % (type(e).__name__, str(e)[:70])
    return out


MEASURE = {"R0": measure_r0, "R1": measure_r1, "R1.5": measure_r15,
           "R2": measure_r2, "R3": measure_r3, "R4a": measure_r4a}


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
        sb, sbs = standby_for(r["id"])
        out.append(dict(r, measured=m, status=status_for(r["id"], m),
                        funcs=RUNG_FUNCS.get(r["id"], []),
                        standby=sb, standby_state=sbs))
    # STAMPED HERE, not via a grid helper I assumed existed. `grid.now_iso` is not a thing, and the
    # hasattr guard silently produced None - a field that reads as "unmeasured" when it was only
    # ever "misspelled". A fallback that hides a typo is worse than the crash it prevents.
    doc = dict(schema=1, generated=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
               gate_hours=GATE_HOURS, reach_gate=list(REACH_GATE),
               funcs_check=verify_funcs(), rungs=out)
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
                bits.append("reach %d/%d inv (%s exec), %s/%s tools | bound: %s"
                            % (m["invocations"], REACH_GATE[0], m.get("executions"),
                               m["tools"], REACH_GATE[1], str(m.get("bound_form"))[:34]))
            if r["id"] == "R4a" and m.get("changed_with_reason") is not None:
                bits.append("%d/%d chosen-with-reason, %s distinct sources"
                            % (m["changed_with_reason"], PERCEPTION_GATE, m.get("distinct")))
            if r["id"] == "R3" and m.get("outcomes") is not None:
                bits.append("%d outcomes recorded" % m["outcomes"])
            print("  %-3s %-32s %-8s %s" % (r["id"], r["title"], r["status"].upper(),
                                            "  |  ".join(bits) or "-"))
        print()
        print("  state/%s written. A dash means the repository cannot prove it, which is a" % LADDER_JSON)
        print("  measurement and not an omission.")
