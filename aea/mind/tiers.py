"""tiers.py - THE TIERED MIND. Different rods own different organs, composed into one voice.

WHY THIS EXISTS, and it is a psychology finding before it is an engineering one.

Human conversation runs on a turn gap of about 200 milliseconds. Stivers et al. measured it across
ten languages on four continents and found the median between 0 and 300ms regardless of culture or
language structure - it is not a style, it is how the machinery works. The consequences for a
machine that talks are measured too: past ~300ms a delay is perceived unconsciously, past ~500ms it
is noticed, and past 1 second people start talking over the agent or leaving.

Our measured time to first audible syllable was 4.24 seconds.

No rod reachable from this machine closes that gap. The fastest measured time to first token is
0.287s and the voice needs another ~0.5s on top, so the floor for a REAL answer is roughly 0.8s
even with the best rod on the board - and the rod that gives a good answer is slower than the rod
that gives a fast one. That trade is the whole problem, and one rod cannot win both sides of it.

So the fix is the one conversation itself uses: SAY SOMETHING TRUE IMMEDIATELY WHILE THE REAL
ANSWER IS STILL BEING WRITTEN. People do this constantly - "hmm", "right", "let me think" - and the
dialogue-systems literature calls them backchannels and filled pauses. They hold the floor, they
signal that you were heard, and they measurably reduce the perceived wait. Crucially for this
project they are HONEST: "let me check that" is a true statement about what is happening, not a
claim about what the machine is. It is a receipt, not a boast.

THE ORGANS, and every assignment below is a MEASUREMENT, not a preference (2026-07-29, n=3 per rod,
one short spoken turn, recorded in `state/rods.json` under `conversational`):

    REFLEX   meta/llama-3.2-3b-instruct              ttfb 0.287s   whole turn 0.626s
    VOICE    nvidia/llama-3.3-nemotron-super-49b-v1  ttfb 0.366s   whole turn 1.506s
    DEPTH    nvidia/nemotron-3-ultra-550b-a55b       ttfb 1.803s   the strongest, when it is worth it
    HANDS    measured per rod by aea.kernel.hands.probe - transport failures are NOT refusals

The rod converse.py used for everything was DEPTH, chosen in July for its Castilian accent. When
the job changed to English nothing re-checked it, and it is 6x the reflex rod's time to first token.
That is law M5: a measurement can go stale, so live knowledge has to be able to re-enter selection.

WHAT THIS IS NOT. It is not a council. x11 measured a cross-rod council TYING its best member at 5x
the cost, and a squad approving its own proposals is not independence. Nothing here votes. Each
organ owns a job it was measured to be best at, and the composition is a ROUTE, not a debate.
"""
from __future__ import annotations

import os
import time

from aea.kernel import grid

# ---------------------------------------------------------------------------------------------
# THE ASSIGNMENTS. Each carries the measurement that earned it, so a stale pick is visible.
# ---------------------------------------------------------------------------------------------
ORGANS = {
    "reflex": dict(
        plant="nvidia", model="meta/llama-3.1-8b-instruct", budget=6,
        ttfb=0.456, whole=0.724, tools=True, tool_seconds=1.1,
        why="the fastest rod measured to do BOTH halves of the job. `llama-3.2-3b-instruct` is "
            "faster to first token (0.287s) and CANNOT call a tool: it emits "
            "`<|python_tag|>{\"name\": \"calc\"...}` as plain text, which no endpoint parses into "
            "tool_calls. Picking it on speed alone put a rod in the acting seat that can only "
            "talk about acting - law M10, fitness is per task SHAPE, not per rod"),
    "voice": dict(
        plant="nvidia", model="nvidia/llama-3.3-nemotron-super-49b-v1", budget=9,
        ttfb=0.366, whole=1.506,
        why="second fastest to first token AND large enough to hold a character; the quality rod "
            "that does not cost the conversational feel"),
    "depth": dict(
        plant="nvidia", model="nvidia/nemotron-3-ultra-550b-a55b", budget=12,
        ttfb=1.803, whole=2.050,
        why="strongest reasoning available here; too slow to be the default voice, correct when "
            "the question actually earns the wait"),
}

# The last rung is LOCAL. ollama never rate-limits and never leaves the machine, so the
# conversation can continue when every hosted pool is saturated. Slow, and present.
LOCAL = dict(plant="ollama", model="nemotron-3-nano:4b", budget=45,
             why="local floor; ~5.8s warm, ~21s cold VRAM load, never throttles, never leaves")

# ---------------------------------------------------------------------------------------------
# HOLDING PHRASES. Spoken while the real answer is written.
#
# EVERY ONE OF THESE MUST BE TRUE WHEN IT IS SAID. That is not a style rule, it is the honesty law
# at the microphone: a filler that says "I'm looking that up" while nothing is being looked up is a
# fabricated status, and this system already learned what unvalidated speech costs when Whisper's
# non-speech artifacts were answered aloud and written into the record as facts about a person.
#
# So they are grouped by WHAT IS ACTUALLY HAPPENING, and the caller picks the group that matches.
# ---------------------------------------------------------------------------------------------
HOLDING = {
    "thinking": ("Let me think about that.", "Give me a second.", "Hm, one moment."),
    "tool": ("Let me check.", "Looking that up now.", "One second, checking."),
    "fetching": ("Fetching that now.", "Let me pull that up."),
}


def hold(kind: str = "thinking", n: int = 0) -> str:
    """A true statement about what is happening right now, said to hold the floor.

    Varied by call index rather than randomly: the lab forbids `Math.random`-style nondeterminism
    in anything that has to be reproducible, and a rotating phrase is enough to stop it sounding
    like a recording."""
    opts = HOLDING.get(kind) or HOLDING["thinking"]
    return opts[n % len(opts)]


def organ(name: str) -> dict:
    """Look up an organ, failing CLOSED. An unknown organ name is a bug in the caller, and
    returning a default rod would hide it behind a working conversation (law B1)."""
    o = ORGANS.get(name)
    if not o:
        raise KeyError("no organ %r; have %s" % (name, ", ".join(sorted(ORGANS))))
    return o


def ladder(*names) -> list:
    """Build a fallback ladder as (plant, model, budget) triples, ending at the LOCAL floor.

    The ladder shape converse.py already used, but assembled from measured organs instead of a
    hand-typed list that nothing re-checks."""
    out = []
    for n in names:
        o = organ(n)
        out.append((o["plant"], o["model"], o["budget"]))
    out.append((LOCAL["plant"], LOCAL["model"], LOCAL["budget"]))
    return out


def refresh_from_store() -> dict:
    """RE-READ the measured latencies and report any organ that is no longer the best choice.

    A measurement can go stale (law M5) and this file is exactly the kind of place a stale pick
    hides - it looks authoritative because it carries a number. This does NOT re-assign anything
    on its own: it reports, and a human decides. Autonomy is granted, never taken (law G5).
    """
    doc = grid.load_json(os.path.join(str(grid.STATE), "rods.json"), {"rods": {}})
    # THE REFLEX SEAT NEEDS BOTH PROPERTIES, so the staleness check reads BOTH stores. Comparing
    # on speed alone is what put a rod that cannot call a tool into the acting seat; a checker
    # that repeats the original mistake would keep recommending it forever.
    tooldoc = grid.load_json(os.path.join(str(grid.STATE), "tool_rods.json"), {"rods": {}})
    can_call = set()
    for rid, r in (tooldoc.get("rods") or {}).items():
        if r.get("pass"):
            can_call.add(rid.split("/", 1)[1] if rid.startswith("nvidia/") else rid)
    rows = []
    for rid, r in (doc.get("rods") or {}).items():
        c = r.get("conversational") or {}
        if c.get("ttfb_median"):
            rows.append((c["ttfb_median"], rid, rid in can_call))
    rows.sort()
    eligible = [x for x in rows if x[2]]
    report = {"measured_rods": len(rows), "tool_capable": len(eligible),
              "fastest": rows[:5], "fastest_eligible": eligible[:3], "drift": []}
    cur = ORGANS["reflex"]["model"]
    if eligible and eligible[0][1] != cur:
        report["drift"].append(
            "reflex is %s (ttfb %.3fs) but the fastest TOOL-CAPABLE rod is now %s (ttfb %.3fs)"
            % (cur, ORGANS["reflex"]["ttfb"], eligible[0][1], eligible[0][0]))
    if rows and not rows[0][2]:
        report["note"] = ("the fastest rod overall (%s, %.3fs) is NOT tool-capable and is "
                          "deliberately not seated" % (rows[0][1], rows[0][0]))
    return report


def board() -> str:
    L = ["THE TIERED MIND - which rod owns which organ, and the measurement that earned it",
         "=" * 96,
         "%-9s %-46s %8s %8s" % ("organ", "rod", "ttfb", "whole")]
    for n, o in ORGANS.items():
        L.append("%-9s %-46s %7.3fs %7.3fs" % (n, o["model"], o["ttfb"], o["whole"]))
    L.append("%-9s %-46s %8s %8s" % ("local", LOCAL["model"], "-", "-"))
    L.append("")
    L.append("TARGET, from the turn-taking literature: a person expects a response gap near 200ms,")
    L.append("notices one past 500ms, and starts talking over the agent past 1s. Our measured time")
    L.append("to first audible syllable was 4.24s, so the reflex tier speaks a TRUE holding phrase")
    L.append("while the answering tier is still writing.")
    r = refresh_from_store()
    L.append("")
    L.append("STALENESS CHECK (%d rods timed, %d of them measured to call a tool):"
             % (r["measured_rods"], r["tool_capable"]))
    for d in r["drift"]:
        L.append("   DRIFT: " + d)
    if not r["drift"]:
        L.append("   no drift: the reflex seat holds the fastest TOOL-CAPABLE rod measured")
    if r.get("note"):
        L.append("   note: " + r["note"])
    return "\n".join(L)


if __name__ == "__main__":
    print(board())
