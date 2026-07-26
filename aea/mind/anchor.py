"""anchor.py - THE COMBINATION CONTRACT: how any subset of modules, in any order, composes into an AEA.

Luis, 2026-07-25: "each module needs anchors to be at the end working as the whole aea... even if
someone takes another path, but that will be the magic of the other creatures... like dna is universal
and let to completely different outcomes."

DNA's universal interface is the codon: one fixed contract, wildly different organisms. This is ours.
An ANCHOR is the six things a module must declare so that a composition can be checked without anyone
having decided in advance what the right composition is:

    closes     which canonical items (C-nn) it embodies        - so a path can be scored against the census
    slot       head | mid | tail                               - the only ordering constraint
    consumes   what it needs present in the chain              - so an impossible order is refused, not run
    produces   what it adds for later parts                    - the edge that lets order matter
    cost       MEASURED tokens + calls + wall-clock            - never estimated; provenance recorded
    requires   THE PRECONDITION: when it earns its cost        - the walk's first law, made executable

THE PRECONDITION IS THE WHOLE DESIGN. Steps 2 and 3 of the walk measured the same law twice: a
capability added without its precondition is pure tax, and sometimes harmful (a generic frame took
strict-JSON from 3/3 to 0/3; grounding on a known answer cost +160% input for zero gain). Declaring
that precondition is what makes ARBITRARY ORDER SAFE - the composition can tell you which of your
organs are earning their keep and which are dead weight, on any path, without a designer's blessing.

So there is no correct assembly. There are compositions whose parts are justified and compositions
carrying tax, and the difference is measurable. That is the room for other creatures to be better
than ours.
"""
from __future__ import annotations

ANCHORS: dict = {}


def anchor(id, name, closes, slot, consumes, produces, cost, requires, provenance, verify=None):
    ANCHORS[id] = dict(id=id, name=name, closes=closes, slot=slot, consumes=list(consumes),
                       produces=list(produces), cost=cost, requires=requires,
                       provenance=provenance, verify=verify)
    return ANCHORS[id]


# ---------------------------------------------------------------------------------------------
# THE ANCHORED MODULES. Every `cost` below was MEASURED this session, and `provenance` says where -
# an unmeasured cost is a guess wearing a number's clothes.
# ---------------------------------------------------------------------------------------------

anchor("tap", "THE DRAW", ["C-01"], "head",
       consumes=["task"], produces=["answer"],
       cost={"calls": 1, "tok_in": 77, "tok_out": 64, "ms": 650},
       requires=lambda c: (True, "a construct without a draw cannot act at all"),
       provenance="the Hall door 1 - bare draw on gpt-oss-20b")

# CORRECTED 2026-07-25 by lab x01_generic_frame, and the correction goes against my own earlier claim.
# Chapter I asserted a generic frame DESTROYS strict-JSON (3/3 -> 0/3, n=3, one rod). Re-measured at
# n=8 on FIVE rods (1b/3b/9b/20b/70b, three families, two providers) the destruction DOES NOT
# REPRODUCE: delta 0 on all four rods that reached the scored floor. What the frame does do is cost -
# input tokens +38% to +107% and median latency up to 4.7x (llama-3.2-1b: 682ms -> 3184ms) for no
# measured change in capability. So an unfitted frame is TAX, not POISON. The precondition below is
# unchanged and still correct, but it now rests on the POSITIVE finding only (a fitted frame took
# 0/3 -> 3/3, itself still n=3 and still owed a re-run), not on a harm that survived measurement.
# Retained rather than deleted: a retracted claim with its receipt is worth more than a clean file.
anchor("scaffold", "THE FRAME", ["C-04", "C-19", "C-23"], "mid",
       consumes=["task"], produces=["fitted_prompt"],
       cost={"calls": 0, "tok_in": 34, "tok_out": 0, "ms": 0},
       requires=lambda c: (bool(c.get("bare_fails")) and bool(c.get("frame_fitted")),
                           "pays ONLY when the rod fails bare AND the frame names the method; "
                           "an unfitted frame is measured TAX (+38..107% input tokens, up to 4.7x "
                           "latency, zero capability change on 4 of 5 rods at n=8)"),
       provenance="step 2 + 2b (fitted frame 0/3 -> 3/3, n=3, OWED a re-run) + lab x01 n=8 x 5 rods "
                  "which RETRACTED the 3/3 -> 0/3 toxicity claim")

anchor("recall", "RECALL", ["C-02", "C-13", "C-84"], "mid",
       consumes=["task"], produces=["grounding"],
       cost={"calls": 2, "tok_in": 288, "tok_out": -24, "ms": 3100},
       requires=lambda c: (bool(c.get("rod_cannot_know")),
                           "pays ONLY when the rod genuinely cannot know; on a knowable question "
                           "it cost +160% input for zero gain"),
       provenance="step 3b - grounded 0/3 -> 3/3; embed LOCAL so 0 cloud tokens, 18.7s cold/3.1s warm")

anchor("ladder", "THE LADDER", ["C-16", "C-67"], "mid",
       consumes=["task"], produces=["reach", "fall_through"],
       cost={"calls": 1, "tok_in": 0, "tok_out": 0, "ms": 5500},
       requires=lambda c: (bool(c.get("hearth_insufficient")) and c.get("zone") != "sensitive",
                           "pays only when the free rod cannot pass; the ward overrules it outright, "
                           "and the big rod measured 8x SLOWER, not faster"),
       provenance="M02 cost 1u; the Hall door 4 - llama-3.3-70b 6222ms vs 770ms")

anchor("governor", "THE METER", ["C-14", "C-26"], "mid",
       consumes=[], produces=["restraint"],
       cost={"calls": 0, "tok_in": 0, "tok_out": 0, "ms": 1},
       requires=lambda c: (bool(c.get("shared_capacity")),
                           "pays when capacity is shared - it prevents a brownout it never reports"),
       provenance="local only; the meter check measured 1.0ms")

anchor("hand", "THE HAND", ["C-29", "C-47", "C-52"], "mid",
       consumes=["task"], produces=["action"],
       cost={"calls": 1, "tok_in": 75, "tok_out": 0, "ms": 1250},
       requires=lambda c: (bool(c.get("needs_action")),
                           "the schema is billed on EVERY call whether a tool fires or not - "
                           "+75 tok_in measured for two tools, so versatility is a standing tax"),
       provenance="the Hall door 6 - tools attached took in 74 -> 149; round trip = 2 calls")

anchor("ward", "THE WARD", ["C-18", "C-50", "C-78"], "mid",
       consumes=["answer"], produces=["verdict"],
       cost={"calls": 1, "tok_in": 75, "tok_out": 8, "ms": 800},
       requires=lambda c: (bool(c.get("output_released")),
                           "doubles the cycle (x2.14 measured) - pays only when the output "
                           "actually reaches something that matters"),
       provenance="the Hall door 4 - guarded draw 1387ms vs 648ms bare")


# THE JUDGE MUST OVERRULE, NOT ADVISE (measured 2026-07-25, judge matrix). Two flows were compared on
# the same task and the same answers. When the judge returns FEEDBACK and the weak rod then revises:
# 7/8 collapses to 2/8 - destructive. When the judge STATES THE CORRECTED ANSWER ITSELF: baseline 3/6
# rises to 6/6. The critique was never the problem; handing the verdict back to the model that was
# already wrong is the problem.
#
# AND THE FUEL LAW (Luis, same day): the architecture is NOT fuel-independent. This module's viability
# is a function of the rod judging. Measured on the identical task: groq/llama-3.3-70b 6/6 ·
# nvidia/gpt-oss-20b 5/6 · nvidia/llama-3.2-3b 5/6 · nvidia/nemotron-nano-9b 3/6 (no repair at all).
# The same composition on different fuel is a different organism, so a precondition that ignores the
# rod is only half a precondition.
anchor("critic", "THE CRITIC", ["C-50", "C-78", "C-43"], "mid",
       consumes=["answer"], produces=["verdict"],
       cost={"calls": 1, "tok_in": 370, "tok_out": 90, "ms": 880},
       requires=lambda c: (bool(c.get("answer_may_be_wrong")) and bool(c.get("judge_overrules"))
                           and bool(c.get("judge_capable")),
                           "needs THREE things: a separate call (0/9 found in one breath, 9/9 apart); "
                           "the judge must OVERRULE not advise (advice-then-revise collapsed 7/8 to "
                           "2/8); and the JUDGE ROD must be capable (nemotron-9b repaired nothing, "
                           "groq-70b repaired everything)"),
       provenance="step 4 + the judge matrix - separation, overrule-not-advise, and the fuel law")

# THE READOUT - discovered by measurement 2026-07-25 (lab x02), and it closes NOTHING in the census,
# because the census does not contain it. Candidate item 87: the 86 were found by auditing what the
# architecture already described; this one was found by watching a rod work.
#
# WHAT WAS MEASURED. On the word-count task with a fitted frame, groq/llama-3.3-70b produced the
# correct enumeration in 8 of 8 trials - "1. the ... 13. wire" - and then stated the total as 11, or
# 10. Every single time. The frame did its job perfectly; the model's SUMMARY OF ITS OWN WORK was
# wrong. Reading the answer off the work instead of off the last line takes that rod from 0/8 to 8/8
# at zero tokens and ~0ms, because it is a local regex over text already paid for.
#
# THE GENERAL LAW, and it is not small: WHEN A FRAME NAMES A METHOD, THE ANSWER IS IN THE WORK, AND
# THE MODEL'S SELF-REPORT IS AN UNRELIABLE NARRATOR OF IT. Every architecture that asks a model to
# "show your steps then give the answer" is trusting the least reliable line of the output. This is
# also why it must be checked per rod: llama-3.2-3b reported its own work correctly 8/8, so the
# extractor is pure redundancy there, and gpt-oss-20b emits no enumeration at all so there is nothing
# to read - the precondition below is what keeps it from becoming another always-on organ.
anchor("readout", "THE READOUT", [], "tail",
       consumes=["answer"], produces=["receipt"],
       cost={"calls": 0, "tok_in": 0, "tok_out": 0, "ms": 0},
       requires=lambda c: (bool(c.get("work_is_structured")) and bool(c.get("selfreport_unreliable")),
                           "pays ONLY when the frame produced structured work AND that rod misreports "
                           "it; measured 0/8 -> 8/8 on groq-70b, and 0 gain on llama-3.2-3b which "
                           "reports its own work correctly"),
       provenance="lab x02_fitted_frame - re-analysed off stored trial text at zero token cost")

anchor("scorer", "THE MEASURE", ["C-15", "C-60"], "tail",
       consumes=["answer"], produces=["receipt"],
       cost={"calls": 0, "tok_in": 0, "tok_out": 0, "ms": 0},
       requires=lambda c: (True, "measurement is FREE - 0ms measured; there is never a reason to omit it"),
       provenance="the Hall door 2 - SCORE stage measured 0ms")


# ---------------------------------------------------------------------------------------------
# THE COMPOSITION CHECK - runs on ANY order, blesses none of them
# ---------------------------------------------------------------------------------------------

def compose(order: list, ctx: dict | None = None) -> dict:
    """Check a composition. Returns what is legal, what is justified, what it costs, what it closes.

    This never says "wrong order". It says which parts EARN their cost in this context and which are
    tax - which is the only honest thing a checker can say when there is no correct path.
    """
    ctx = ctx or {}
    seen, produced, rows = [], set(ctx.get("given", [])), []
    illegal, tax, closes = [], [], set()
    cost = {"calls": 0, "tok_in": 0, "tok_out": 0, "ms": 0}

    for i, pid in enumerate(order):
        a = ANCHORS.get(pid)
        if not a:
            illegal.append((pid, "not an anchored module"))
            continue
        # slot law: the only hard ordering constraint
        if a["slot"] == "head" and i != 0:
            illegal.append((pid, "%s is a head - it must open the chain" % a["name"]))
        if a["slot"] == "tail" and i != len(order) - 1:
            illegal.append((pid, "%s is a tail - it must close the chain" % a["name"]))
        # dependency law: consume what nothing produced -> the order is impossible, not merely poor
        missing = [c for c in a["consumes"] if c not in produced and c not in ("task",)]
        if missing:
            illegal.append((pid, "needs %s, which nothing before it produces" % ", ".join(missing)))
        ok, why = a["requires"](ctx)
        if not ok:
            tax.append((pid, a["name"], why))
        for k in cost:
            cost[k] += a["cost"].get(k, 0)
        closes |= set(a["closes"])
        produced |= set(a["produces"])
        seen.append(pid)
        rows.append({"id": pid, "name": a["name"], "slot": a["slot"], "justified": ok,
                     "why": why, "cost": a["cost"], "closes": a["closes"]})

    # WASTE IS MULTI-DIMENSIONAL. Found by using this checker on its own output 2026-07-25: a
    # token-only waste figure reported PATH D as 0% waste while carrying an unjustified LADDER that
    # cost 5.5 SECONDS and a whole network call for zero tokens. A part whose price is TIME was
    # invisible to a metric denominated in tokens. Waste is now the WORST dimension, not the
    # convenient one.
    waste = {}
    for dim in ("tok_in", "calls", "ms"):
        tot = sum(ANCHORS[r["id"]]["cost"].get(dim, 0) for r in rows)
        just = sum(ANCHORS[r["id"]]["cost"].get(dim, 0) for r in rows if r["justified"])
        waste[dim] = round(100.0 * (tot - just) / tot, 1) if tot else 0.0
    worst = max(waste, key=lambda k: waste[k])
    return {"order": order, "rows": rows, "illegal": illegal, "tax": tax,
            "cost": cost, "closes": sorted(closes),
            "waste": waste, "waste_pct": waste[worst], "waste_worst_dim": worst,
            "legal": not illegal}


def coverage() -> dict:
    """Which canonical items the anchored set can close at all - the census, from the module side."""
    c = set()
    for a in ANCHORS.values():
        c |= set(a["closes"])
    return {"anchored_modules": len(ANCHORS), "closes": sorted(c), "count": len(c)}


# ---------------------------------------------------------------------------------------------
# THE MUTATION CHANNEL — how the contract learns it was wrong
#
# Luis, 2026-07-25: "there could be other ways we didn't think that would be fully functional, we
# don't know."  He is right, and step 4 proved it on my own instrument: I designed the plan+critique
# prompt and predicted its cheap single-call form would work. It found ZERO errors in nine trials.
# The measurement corrected the designer.
#
# So `requires` above is NOT a law. It is a HYPOTHESIS about when a part earns its cost, and the only
# authority is what actually happened. This channel exists so a composition that the checker calls
# wasteful can be RUN ANYWAY, and can win. Nothing here gates execution - it only records surprise.
#
# That is the whole of evolution, and none of it is design:
#   VARIATION   any order is runnable, including ones no one intended
#   MEASUREMENT the receipt, not the prediction
#   SELECTION   what performed, whatever the checker said
#   HEREDITY    a precondition that keeps losing gets revised, and the revision persists
# ---------------------------------------------------------------------------------------------

import os as _os
import time as _time


def _obs_path():
    from aea.kernel import grid
    return _os.path.join(grid.STATE, "anchor_observations.json")


def observe(order: list, ctx: dict, outcome: dict, baseline: dict | None = None, note: str = "") -> dict:
    """Record what a composition ACTUALLY did against what compose() predicted.

    outcome: {"pass": bool|None, "tok_in": int, "calls": int, "ms": int}  - all measured.
    A composition the checker called wasteful that nevertheless PASSED is a SURPRISE: the prediction
    lost to the world, and the precondition it rests on is due for revision. Surprises are the only
    honest source of new architecture - they are the mutations that worked.
    """
    from aea.kernel import grid
    pred = compose(order, ctx)
    predicted_waste = pred["waste_pct"]
    passed = outcome.get("pass")
    # a surprise is a composition that was predicted to be mostly tax and worked anyway,
    # or one predicted clean that failed
    # A SURPRISE REQUIRES A BASELINE. Corrected 2026-07-25 after chasing a false positive: the rule
    # used to fire whenever a wasteful composition PASSED, which is meaningless - an overpowered
    # composition passes trivially. Measured: PATH D (89% predicted waste) and PATH B (0%) both scored
    # 3/3 on the same task, PATH D at 1.7x tokens and 3.3x wall clock. It worked. It was not worth it.
    # Those are different claims and only the second can refute a precondition.
    surprise = None
    base = (baseline or {}).get("pass") if baseline else None
    if baseline is None:
        surprise = None   # no baseline -> not judgeable, and saying otherwise would be the old bug
    elif passed is True and base is not True and predicted_waste >= 50:
        surprise = ("outperformed the justified baseline at %.0f%% predicted waste - "
                    "a precondition is too strict" % predicted_waste)
    elif passed is False and predicted_waste == 0:
        surprise = "failed with every part justified - a precondition is missing"

    rec = {"at": _time.strftime("%Y-%m-%d %H:%M UTC", _time.gmtime()),
           "order": list(order), "ctx": {k: v for k, v in ctx.items() if not callable(v)},
           "predicted_waste_pct": predicted_waste, "predicted_legal": pred["legal"],
           "outcome": outcome, "baseline": baseline, "surprise": surprise, "note": note}
    st = grid.load_json(_obs_path(), {"observations": []})
    st.setdefault("observations", []).append(rec)
    grid.atomic_save_json(_obs_path(), st)
    return rec


def surprises() -> list:
    """Every recorded case where the world disagreed with the checker. The revision queue."""
    from aea.kernel import grid
    st = grid.load_json(_obs_path(), {"observations": []})
    return [o for o in st.get("observations", []) if o.get("surprise")]
