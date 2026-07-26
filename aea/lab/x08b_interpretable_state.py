"""x08b - THE HANDOFF WHEN THE STATE IS NOT A NUMBER. What x08 answered in its easiest possible form.

x08 handed a checkpoint from one rod to another mid-chain and measured zero degradation in both
directions. That result is real and it is also nearly free, because the checkpoint held an INTEGER. Any rod
that can read `-3` can double it; there is no interpretation step to fail. So the fuel-crossing question
was answered where it could not have come out any other way, and the interesting version was left standing:

  a VALUE survives any handoff. a PLAN might not.

THE CLAIM UNDER TEST. If the carried state holds working notes in a rod's own phrasing - a partial
structure, an idiom, a way of writing the world down - can a DIFFERENT rod read that phrasing and continue
the same work? This is where identity across fuel actually bites, and it is what C-80 has to hold to be
load-bearing rather than decorative.

WHY IT IS A 2x4 FACTORIAL AND NOT FOUR ARMS. If free-form handoffs degrade, that alone does not locate the
cost: free notes might simply be a worse way to carry state for ANY rod, including the one that wrote them.
So representation is crossed with the rod plan:

  REPRESENTATION   free    the rod writes its notes however it likes, seeded with a prose sentence
                   schema  the rod must write exactly six canonical lines, `bN: shelf M`
  ROD PLAN         A 9b alone   B 20b alone   C handoff 9b->20b   D handoff 20b->9b

The measurement that answers the claim is the INTERACTION: (handoff - alone) inside free, against
(handoff - alone) inside schema. If the penalty appears only under free notes, the cost is in
REPRESENTATION and a shared canonical form is the fix. If it appears in both, the crossing itself is
expensive. If it appears in neither, phrasing is portable and C-80 holds in substance.

THE TASK RESISTS ONE-BREATH SHORTCUTS AND SATURATION. Six boxes on nine shelves, thirty events. A third of
the events are REFERENTIAL - "boxes b2 and b5 exchange shelves", "box b4 is moved onto the same shelf as
box b1" - so they cannot be applied without reading the current state. The state is therefore load-bearing
at every step rather than at the end. Ground truth is computed locally in Python for free.

SCORING IS GRADED, 0..6 boxes correct, deliberately. Three of this project's experiments have been voided
or flattered by the ceiling effect (chapter II's opening, most of x03/x04, and x08's own verdict). A graded
score has no cliff at the top: even if every arm passes often, per-box accuracy still separates them.

Two extra readout calls in the handoff arms record the state AT the crossing - once from the rod handing
off, once from the rod that picked it up - so the damage, if any, is measured where it happens rather than
inferred from the final answer. Raw notes are stored verbatim; the lesson from x07 is that storing the
interpretation instead of the evidence makes a parser fix cost a full re-run.

Run: python -m aea.lab.x08b_interpretable_state
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import random
import re
import sys
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.mind import checkpoint as CP

BOXES = ["b1", "b2", "b3", "b4", "b5", "b6"]
SHELVES = list(range(1, 10))
LENGTH = 30
HANDOFF_AT = 15
N = 8
TEMP = 0.0
SEED = 1729

# THE STEP CAP, AND WHY IT IS A VARIABLE RATHER THAN A CONSTANT.
#
# Run 20260725T140401Z used 1200 and it CONFOUNDED the headline comparison: the free arms hit the cap 32 to
# 53 times each while the schema arms hit it 0 to 1 times, so "free-form carries worse" was partly "our cap
# cut the free notes". Restricting to uncut trials could not rescue it either - only 0, 1, 2 and 0 trials per
# free arm survived, because free-form notes hit the cap in nearly every trial.
#
# 3500 is chosen so truncation is RARE rather than absent. Suppressing the growth entirely (by instructing a
# length limit) would destroy the variable under test: free-form notes growing without bound is a REAL
# property of the representation - the run above produced a 4801-char note that was the rod's own
# deliberation rather than the state. So the growth is measured as a curve (`notes_curve`) and the cap is
# raised until it stops manufacturing the result.
STEP_MAXTOK = 3500
READOUT_MAXTOK = 1000

NINE = ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2")
TWENTY = ("nvidia", "openai/gpt-oss-20b")


# --- THE WORLD. Deterministic events, local ground truth, no RNG at run time. -----------------------

def events(n: int = LENGTH) -> list:
    """`n` events as (kind, args, sentence). Seeded once, so any run reproduces any other.

    The kinds are interleaved i%3 rather than sampled, so the mix is fixed by construction and cannot
    drift between arms: exactly two thirds of the events are REFERENTIAL (swap, shift), meaning they
    cannot be applied without reading the current state.

    WHY THERE IS NO "move onto the same shelf as box X". That was the first version's third op, and it
    COLLAPSES the world: ten of them left six boxes on three distinct shelves, at which point the lazy
    answer "everything is on shelf 1" scores 0.5 per box and eats most of the headroom the graded score
    exists to protect. `shift` keeps the referential requirement without collapsing the state.
    """
    rng = random.Random(SEED)
    out = []
    for i in range(n):
        kind = ("move", "swap", "shift")[i % 3]
        if kind == "move":
            b, s = rng.choice(BOXES), rng.choice(SHELVES)
            out.append((kind, (b, s), "box %s is moved to shelf %d." % (b, s)))
        elif kind == "swap":
            b, c = rng.sample(BOXES, 2)
            out.append((kind, (b, c), "boxes %s and %s exchange shelves." % (b, c)))
        else:
            b, k = rng.choice(BOXES), rng.choice((1, 2, 3))
            out.append((kind, (b, k), "box %s is moved %d %s further along, wrapping from shelf 9 back "
                        "round to shelf 1." % (b, k, "shelf" if k == 1 else "shelves")))
    return out


def truth(n: int = LENGTH) -> dict:
    """The final box -> shelf map, computed locally. Shelves hold any number of boxes."""
    st = {b: i + 1 for i, b in enumerate(BOXES)}
    for kind, args, _ in events(n):
        if kind == "move":
            st[args[0]] = args[1]
        elif kind == "swap":
            st[args[0]], st[args[1]] = st[args[1]], st[args[0]]
        else:
            st[args[0]] = (st[args[0]] - 1 + args[1]) % len(SHELVES) + 1
    return st


def lazy_baseline(n: int = LENGTH) -> dict:
    """What the two cheapest non-answers score, per box. Reported beside every arm so a high score
    cannot be read as understanding when it is really the shape of the truth table."""
    exp = truth(n)
    start = {b: i + 1 for i, b in enumerate(BOXES)}
    mode = max(set(exp.values()), key=lambda s: sum(1 for v in exp.values() if v == s))
    return {"never_changed": round(sum(1 for b in BOXES if start[b] == exp[b]) / len(BOXES), 3),
            "all_on_%d" % mode: round(sum(1 for b in BOXES if exp[b] == mode) / len(BOXES), 3),
            "distinct_shelves": len(set(exp.values()))}


def truth_at(step: int) -> dict:
    return truth(step)


# --- REPRESENTATION. The variable under test. -------------------------------------------------------

SEED_NOTES = {
    # PROSE on purpose. Seeding the free arm with the canonical lines would hand it the schema and
    # collapse the two conditions into one.
    "free": ("Every box starts on the shelf that carries its own number: b1 is on shelf 1, b2 on shelf 2, "
             "b3 on shelf 3, b4 on shelf 4, b5 on shelf 5 and b6 on shelf 6."),
    "schema": "\n".join("%s: shelf %d" % (b, i + 1) for i, b in enumerate(BOXES)),
}

STEP_RULE = {
    "free": ("Rewrite your notes so that they account for the event and so that a reader with no other "
             "information could say where every box is. Use whatever wording you find clearest. "
             "Reply with ONLY your notes."),
    "schema": ("Reply with ONLY six lines, each exactly in the form `bN: shelf M`, one line per box, in "
               "order b1 to b6. No other text, no commentary."),
}

READOUT = ("These are the notes:\n\n%s\n\nUsing ONLY these notes, state where each box is now. "
           "Reply with ONLY six lines, each exactly in the form `bN: shelf M`, in order b1 to b6. "
           "Do not explain, do not show your working, do not add any other text.")

REPAIR = ("Reformat the following into exactly six lines, each exactly in the form `bN: shelf M`, in "
          "order b1 to b6. Take the values from the text; if a box's shelf is genuinely not stated, "
          "write `bN: shelf unknown`. Output the six lines and nothing else.\n\n%s")

_THINK = re.compile(r"<think>.*?</think>|<thinking>.*?</thinking>", re.S | re.I)


def _clean(text: str) -> str:
    """Strip reasoning traces. grid.call_openai falls back to `reasoning_content` when content is empty,
    so a thinking rod can otherwise write its scratchpad into the notes and the next rod inherits it."""
    return _THINK.sub("", text or "").strip()


def _parse(text: str) -> tuple:
    """(box -> shelf, mode) from a readout.

    TWO PASSES, AND THE MODE IS RECORDED. The first version used one loose regex and silently misread
    "Shelf 4 holds b1. Shelf 9 holds b2." as a SHIFTED map - it matched `b1` and then took the 9 from the
    next sentence, producing a confidently wrong answer that would have been charged to the handoff. So:
    strict line-anchored form first (which is what the readout prompt demands), and a per-clause loose
    pass only as a fallback, with the mode carried into the evidence so a parser artefact stays visible.
    """
    clean = _clean(text)
    strict = {}
    for line in clean.splitlines():
        m = re.match(r"\s*[-*\d.)\s]*b\s*([1-6])\b\D{0,12}?([0-9]{1,2})\b", line, re.I)
        if m:
            strict["b%s" % m.group(1)] = int(m.group(2))
    if len(strict) == len(BOXES):
        return strict, "strict"
    # LOOSE PASS. Per clause, BOTH orders, and ONLY where the clause is unambiguous.
    #
    # Both orders because "b1 is on shelf 4" and "shelf 4 holds b1" are the same claim about the world,
    # and scoring the second as zero would charge a formatting miss to the handoff.
    #
    # THE SINGLE-NUMBER RULE is what the smoke test bought. The 20b deliberated instead of answering and
    # wrote "b5 moved 2 shelves ahead from shelf 4 to shelf 6"; the previous loose pass took the 2 and
    # scored b5 wrong when the rod had it right. A clause carrying more than one number cannot be read
    # without guessing which number is the answer, so it is SKIPPED and counted, never guessed.
    loose, ambiguous = dict(strict), 0
    for frag in re.split(r"[.;,\n]", clean):
        if not re.search(r"\bb\s*[1-6]\b", frag, re.I):
            continue
        nums = re.findall(r"\d{1,2}", re.sub(r"\bb\s*([1-6])\b", " ", frag, flags=re.I))
        if len(nums) != 1:
            ambiguous += 1
            continue
        for m in re.finditer(r"\bb\s*([1-6])\b\D{0,16}?([0-9]{1,2})\b", frag, re.I):
            loose.setdefault("b%s" % m.group(1), int(m.group(2)))
        for m in re.finditer(r"\bshel[fv]e?s?\s*([0-9]{1,2})\b\D{0,20}?\bb\s*([1-6])\b", frag, re.I):
            loose.setdefault("b%s" % m.group(2), int(m.group(1)))
    mode = "loose" if len(loose) > len(strict) else "partial"
    if len(loose) < len(BOXES) and ambiguous:
        mode += "+ambiguous%d" % ambiguous
    return loose, mode


def _score(got: dict, exp: dict) -> int:
    return sum(1 for b in BOXES if got.get(b) == exp[b])


# --- THE WALK --------------------------------------------------------------------------------------

def _ask(rod, prompt, max_tokens):
    """Returns (clean text, was-it-cut, raw response).

    TRUNCATION IS DETECTED BY A TOKEN-CAP PROXY, not by finish_reason: grid.call_openai does not surface
    finish_reason at all, so nothing in the lab can currently see a cut reply. The smoke test produced one
    - a readout that ran out of budget mid-word while deliberating - and a cut readout scored as lost state
    would be the truncation bug over again, one experiment later. The proxy can false-positive on a reply
    that legitimately ends at the cap; it is recorded rather than acted on silently.
    """
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": prompt}],
                     max_tokens=max_tokens, temperature=TEMP)
    txt = _clean(r.get("text") or "") if r.get("ok") else ""
    return txt, bool(r.get("ok")) and (r.get("tokens") or 0) >= max_tokens - 2, r


def _readout(rod, notes):
    """One readout, plus ONE repair attempt when the reply is not readable as six lines.

    The repair exists because the question under test is whether the STATE crossed, not whether the rod
    obeyed a formatting instruction. A reasoning rod that answers correctly inside a paragraph of working
    must not be scored as having lost the state. The repair is counted, so its frequency is visible.
    """
    txt, cut, r = _ask(rod, READOUT % notes, READOUT_MAXTOK)
    got, mode = _parse(txt)
    used = [r]
    if len(got) < len(BOXES) or cut:
        fix, cut2, r2 = _ask(rod, REPAIR % (txt or notes), 500)
        used.append(r2)
        got2, mode2 = _parse(fix)
        if len(got2) > len(got):
            got, mode, txt, cut = got2, mode2 + "+repaired", txt + "\n---REPAIR---\n" + fix, cut2
        else:
            mode += "+repair_failed"
    return got, mode, txt, cut, used


def _walk(name, rep, plan, trial):
    ck_name = "x08b_%s_%d" % (name, trial)
    CP.wipe(ck_name)
    ck = CP.Checkpoint(ck_name, {"notes": SEED_NOTES[rep], "step": 0})
    tally = {"calls": 0, "tok_in": 0, "tok_out": 0, "stalls": 0, "cuts": 0, "repairs": 0}
    cross, curve = {}, []

    def bill(*rs):
        for r in rs:
            tally["calls"] += 1
            tally["tok_in"] += r.get("prompt_tokens") or 0
            tally["tok_out"] += r.get("tokens") or 0

    for i, (_, _, sentence) in enumerate(events(LENGTH)):
        rod = plan(i)

        # AT THE CROSSING, twice: what the outgoing rod believed, then what the incoming rod believed
        # after its first rewrite. Measured where the damage would happen, not inferred from the end.
        if i == HANDOFF_AT and plan(i - 1) != rod:
            got, mode, raw, cut, used = _readout(plan(i - 1), ck.read()["notes"])
            bill(*used)
            tally["repairs"] += "repaired" in mode
            cross["before"] = {"rod": "%s/%s" % plan(i - 1), "score": _score(got, truth_at(i)),
                               "parsed": got, "parse_mode": mode, "raw": raw,
                               "notes_handed_over": ck.read()["notes"]}

        notes, cut, r = _ask(rod, "You are keeping the only working notes on a warehouse. Nothing else "
                                  "remembers the state; these notes are all that carries forward.\n\n"
                                  "YOUR NOTES SO FAR:\n%s\n\nNEW EVENT: %s\n\n%s"
                                  % (ck.read()["notes"], sentence, STEP_RULE[rep]), STEP_MAXTOK)
        bill(r)
        tally["cuts"] += cut

        if not notes:
            # A DROPPED STEP IS A STALL, not the end of the trial. Abandoning the walk would discard the
            # graded score and make the fault invisible; keeping the previous notes records it as the real
            # cost it is - the event is lost and the final answer pays for it.
            tally["stalls"] += 1
        else:
            ck.write(rod="%s/%s" % rod, note=sentence, notes=notes, step=i + 1)
        # THE GROWTH CURVE. A representation that grows is a representation with a deadline.
        curve.append(len(ck.read()["notes"]))

        if "before" in cross and "after" not in cross and notes:
            got, mode, raw, cut, used = _readout(rod, notes)
            bill(*used)
            tally["repairs"] += "repaired" in mode
            cross["after"] = {"rod": "%s/%s" % rod, "score": _score(got, truth_at(i + 1)),
                              "parsed": got, "parse_mode": mode, "raw": raw, "notes_after": notes}

    last = plan(LENGTH - 1)
    final_notes = ck.read()["notes"]
    got, mode, raw, cut, used = _readout(last, final_notes)
    bill(*used)
    tally["repairs"] += "repaired" in mode
    exp = truth(LENGTH)
    out = {"score": _score(got, exp), "parsed": got, "parse_mode": mode, "readout_raw": raw,
           "final_notes": final_notes, "notes_chars": len(final_notes),
           "crossing": cross or None, "revisions": ck.revision,
           "fuel_trail": ck.fuel_trail(), "crossed_fuel": ck.crossed_fuel(),
           "checkpoint": ck_name, "notes_curve": curve}
    out.update(tally)
    return out


PLANS = {
    "A_9b_alone":        lambda i: NINE,
    "B_20b_alone":       lambda i: TWENTY,
    "C_handoff_9_to_20": lambda i: NINE if i < HANDOFF_AT else TWENTY,
    "D_handoff_20_to_9": lambda i: TWENTY if i < HANDOFF_AT else NINE,
}


def arm(rep, plan_name):
    name = "%s_%s" % (rep, plan_name)
    plan = PLANS[plan_name]
    pool = _futures.ThreadPoolExecutor(max_workers=N)
    t0 = time.time()
    try:
        res = [f.result() for f in [pool.submit(_walk, name, rep, plan, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    per_box = sum(r["score"] for r in res) / (len(BOXES) * len(res))
    exact = sum(1 for r in res if r["score"] == len(BOXES))
    cr = [r["crossing"] for r in res if r.get("crossing")]
    row = {"arm": name, "representation": rep, "plan": plan_name,
           "per_box": round(per_box, 4), "exact": exact, "n": len(res),
           "scores": [r["score"] for r in res], "stalls": sum(r["stalls"] for r in res),
           "cuts": sum(r["cuts"] for r in res), "repairs": sum(r["repairs"] for r in res),
           "calls": sum(r["calls"] for r in res), "tok_in": sum(r["tok_in"] for r in res),
           "tok_out": sum(r["tok_out"] for r in res),
           "notes_chars_median": sorted(r["notes_chars"] for r in res)[len(res) // 2],
           "curve_mean": [round(sum(c[i] for c in (t["notes_curve"] for t in res)
                                    if len(c) > i) / max(1, sum(1 for t in res
                                    if len(t["notes_curve"]) > i)))
                          for i in range(LENGTH)],
           "parse_modes": {m: sum(1 for r in res if r["parse_mode"] == m)
                           for m in sorted({r["parse_mode"] for r in res})},
           "wall_s": round(time.time() - t0, 1),
           "crossed_fuel": all(r["crossed_fuel"] for r in res) if "handoff" in plan_name else False,
           "fuel_trails": sorted({" -> ".join(r["fuel_trail"]) for r in res}),
           "crossing_before": (round(sum(c["before"]["score"] for c in cr if "before" in c)
                                     / max(1, sum(1 for c in cr if "before" in c)), 2) if cr else None),
           "crossing_after": (round(sum(c["after"]["score"] for c in cr if "after" in c)
                                    / max(1, sum(1 for c in cr if "after" in c)), 2) if cr else None),
           "trials": res}
    print("  %-24s per-box %.2f  exact %d/%-2d  stall=%d cut=%d fix=%d  calls=%-4d %6.1fs  "
          "cross %s->%s  parse %s" %
          (name, per_box, exact, len(res), row["stalls"], row["cuts"], row["repairs"],
           row["calls"], row["wall_s"], row["crossing_before"], row["crossing_after"],
           row["parse_modes"]), flush=True)
    return row


CEILING = 0.99


def verdict_from(rows: list) -> dict:
    """The verdict, computed from rows ALONE so a saved run can be re-read without re-spending tokens.

    THE SATURATION RULE IS PER CONDITION, not global, and that distinction is the whole point. The first
    version asked only whether EVERY arm was at the ceiling. But this design can saturate in one
    representation and not the other - and it did: canonical lines held 1.00 across the board while the
    free-form arms had headroom. A global rule would have called that a clean confirmation of "the cost is
    in representation", when what is actually established is narrower: at a difficulty where canonical
    state crosses fuel perfectly, free-form state does or does not. Whether canonical form would ALSO
    break on a harder chain is untested, and the verdict has to say so.
    """
    by = {r["arm"]: r for r in rows}

    def pb(rep, pn):
        r = by.get("%s_%s" % (rep, pn))
        return r["per_box"] if r else None

    out = {"penalty": {}, "saturated": [], "headroom": [], "verdict": None, "established": [],
           "not_established": []}
    for rep in ("free", "schema"):
        vals = [pb(rep, p) for p in PLANS]
        if any(v is None for v in vals):
            continue
        alone = max(pb(rep, "A_9b_alone"), pb(rep, "B_20b_alone"))
        hand = max(pb(rep, "C_handoff_9_to_20"), pb(rep, "D_handoff_20_to_9"))
        out["penalty"][rep] = round(hand - alone, 3)
        (out["saturated"] if min(vals) >= CEILING else out["headroom"]).append(rep)

    p, sat, head = out["penalty"], out["saturated"], out["headroom"]
    if len(p) < 2:
        out["verdict"] = "INCOMPLETE - both representations must run to read the interaction."
        return out

    for rep in sat:
        out["established"].append("%s: a handoff introduced no measurable degradation (penalty %+.2f), "
                                  "and the crossing readouts confirm two rods wrote each checkpoint"
                                  % (rep, p[rep]))
        out["not_established"].append("%s: every arm sat at the ceiling, so nothing here prices a handoff "
                                      "UNDER STRESS - the task was not hard enough to show a cost" % rep)

    if not head:
        out["verdict"] = ("NO RESOLUTION - both representations saturated. State crossed fuel intact in "
                          "every arm, which is real and cheap, but the comparison has no headroom in "
                          "either condition. A harder chain is owed before the representation question "
                          "can be answered at all.")
        return out

    if "free" in head and "schema" in sat:
        if p["free"] <= -0.10:
            out["verdict"] = ("THE COST IS IN REPRESENTATION - BOUNDED. Handing over free-form notes cost "
                              "%+.2f per box, on a task where canonical lines crossed fuel PERFECTLY in "
                              "every arm. So at this difficulty a rod's own phrasing is not portable and a "
                              "declared form is, which is what C-80 has to hold. BOUNDED because the "
                              "canonical condition was at the ceiling: it is untested whether a declared "
                              "form also survives a chain hard enough to hurt it." % p["free"])
        else:
            out["verdict"] = ("PHRASING IS PORTABLE AT THIS DIFFICULTY. Free-form notes had headroom "
                              "(arms below the ceiling) and the handoff still cost %+.2f per box - a rod "
                              "read another rod's own phrasing and continued the same work. Canonical "
                              "lines were saturated, so the two forms cannot be ranked against each "
                              "other here." % p["free"])
        return out

    if len(head) == 2:
        if p["free"] <= -0.10 and p["schema"] > -0.05:
            out["verdict"] = ("THE COST IS IN REPRESENTATION. Free-form %+.2f against canonical %+.2f, "
                              "both conditions with headroom - the cleanest form of this result."
                              % (p["free"], p["schema"]))
        elif p["free"] <= -0.10 and p["schema"] <= -0.10:
            out["verdict"] = ("THE CROSSING ITSELF COSTS. Both forms degraded on handoff (%+.2f free, "
                              "%+.2f canonical), so the loss is not about phrasing - a fuel change breaks "
                              "continuity even in a declared form." % (p["free"], p["schema"]))
        else:
            out["verdict"] = ("PHRASING IS PORTABLE. Handoff cost %+.2f free and %+.2f canonical, both "
                              "with headroom - a rod can continue another rod's working notes."
                              % (p["free"], p["schema"]))
        return out

    out["verdict"] = ("PARTIAL - %s saturated, %s had headroom. Penalties %s. Read the crossing rows "
                      "before concluding." % (",".join(sat) or "none", ",".join(head) or "none", p))
    return out


def stratify(rows: list) -> dict:
    """Per-arm score over ALL trials, and over only the trials that never hit the token cap.

    WHY THIS IS NECESSARY AND WHY IT IS NOT ENOUGH. The free arms hit `max_tokens` 32 to 47 times each while
    the schema arms hit it 0 to 1 times: free-form notes grow and canonical lines do not. A cut note loses
    state MECHANICALLY, so part of "free-form carries worse" is "my cap cut the free notes" - a defect in the
    instrument, not a property of the representation.

    Restricting to uncut trials controls for it inside the data already collected. It is not a clean fix:
    the surviving trials are a SELECTED subset (the ones whose notes stayed compact), so they are biased
    toward the runs where free-form behaved most like schema. That biases the comparison TOWARD finding no
    difference, which is the safe direction for a claim that free-form is worse - but it cannot support the
    opposite claim. The unconfounded measurement needs a higher cap, and that is x08c.
    """
    out = {}
    for r in rows:
        trials = r.get("trials") or []
        clean = [t for t in trials if not t.get("cuts")]
        out[r["arm"]] = {
            "per_box_all": r["per_box"], "n_all": len(trials),
            "per_box_uncut": (round(sum(t["score"] for t in clean) / (len(BOXES) * len(clean)), 3)
                              if clean else None),
            "n_uncut": len(clean),
            "cuts": r.get("cuts"),
            "notes_chars_median": r.get("notes_chars_median")}
    return out


def read_latest(run_id: str | None = None) -> dict:
    """Re-interpret a saved run. The evidence is immutable; the reading is not."""
    d = os.path.join(grid.STATE, "lab", "runs", "x08b_interpretable_state")
    files = sorted(f for f in os.listdir(d) if f.endswith(".json"))
    if not files:
        raise ValueError("no runs saved under %s" % d)
    fn = ("%s.json" % run_id) if run_id else files[-1]
    rep = grid.load_json(os.path.join(d, fn), None)
    v = verdict_from(rep["rows"])
    print("RUN %s  (%s)" % (rep.get("run_id"), rep.get("at")))
    print("lazy baseline per box: %s" % rep.get("lazy_baseline"))
    for r in rep["rows"]:
        print("  %-24s per-box %.2f  exact %d/%d  stall=%s cut=%s fix=%s  cross %s->%s"
              % (r["arm"], r["per_box"], r["exact"], r["n"], r.get("stalls"), r.get("cuts"),
                 r.get("repairs"), r.get("crossing_before"), r.get("crossing_after")))
    print()
    print("TRUNCATION CONTROL - score over all trials, then over uncut trials only")
    st = stratify(rep["rows"])
    for arm, s in st.items():
        print("  %-24s all %.2f (n=%d)   uncut %s (n=%d)   cuts=%s  notes_chars_med=%s"
              % (arm, s["per_box_all"], s["n_all"],
                 ("%.2f" % s["per_box_uncut"]) if s["per_box_uncut"] is not None else "  - ",
                 s["n_uncut"], s["cuts"], s["notes_chars_median"]))
    print()
    print("penalty per box (best handoff - best single): %s" % v["penalty"])
    print("saturated: %s   headroom: %s" % (v["saturated"] or "none", v["headroom"] or "none"))
    for e in v["established"]:
        print("  ESTABLISHED     %s" % e)
    for e in v["not_established"]:
        print("  NOT ESTABLISHED %s" % e)
    print()
    print("VERDICT (recomputed): %s" % v["verdict"])
    heavy = [a for a, s in st.items() if (s["cuts"] or 0) > 5]
    if heavy:
        print()
        print("CONFOUND, NAMED: %s hit the token cap more than 5 times. Any between-condition claim that "
              "rests on those arms is confounded by the cap and NOT by representation. The WITHIN-arm "
              "crossing comparison (before -> after at the handoff) is unaffected, because both readouts "
              "were taken under the same cap." % ", ".join(heavy))
    if rep.get("verdict") and rep["verdict"] != v["verdict"]:
        print()
        print("NOTE the verdict stored at run time used the weaker global saturation rule and is "
              "SUPERSEDED by the line above. Stored: %s" % rep["verdict"][:160])
    return {"run": rep, "reading": v}


def run():
    print("x08b - %d boxes, %d events (a third referential), handoff at %d, n=%d"
          % (len(BOXES), LENGTH, HANDOFF_AT, N))
    print("ground truth: %s" % truth(LENGTH))
    print("lazy baselines (per box): %s" % lazy_baseline(LENGTH))
    rows = []
    for rep in ("schema", "free"):
        for pn in PLANS:
            rows.append(arm(rep, pn))
    by = {r["arm"]: r for r in rows}

    def pb(rep, pn):
        return by["%s_%s" % (rep, pn)]["per_box"]

    verdict = None
    try:
        pen = {}
        for rep in ("free", "schema"):
            alone = max(pb(rep, "A_9b_alone"), pb(rep, "B_20b_alone"))
            hand = max(pb(rep, "C_handoff_9_to_20"), pb(rep, "D_handoff_20_to_9"))
            pen[rep] = round(hand - alone, 3)

        # SATURATION GUARD, inherited from x08's mistake. A comparison whose arms all sit at the top has
        # no headroom and cannot separate "the handoff is free" from "the task was too easy to show a
        # cost". Graded scoring makes this far less likely here, which is why it is graded.
        if min(r["per_box"] for r in rows) >= 0.99:
            verdict = ("NO RESOLUTION - every arm scored >=0.99 per box, so the comparison has no "
                       "headroom. The task is too easy to price a handoff.")
        elif pen["free"] < -0.10 and pen["schema"] >= -0.05:
            verdict = ("THE COST IS IN REPRESENTATION, NOT IN THE CROSSING. Handing over free-form notes "
                       "cost %+.2f per box while handing over canonical lines cost %+.2f. State crosses "
                       "fuel only in a form both rods can read, so C-80 is load-bearing ONLY with a "
                       "declared representation - a rod's own phrasing is not portable."
                       % (pen["free"], pen["schema"]))
        elif pen["free"] < -0.10 and pen["schema"] < -0.10:
            verdict = ("THE CROSSING ITSELF COSTS. Both representations degraded on handoff (%+.2f free, "
                       "%+.2f schema), so the loss is not about phrasing - a fuel change breaks continuity "
                       "even in a canonical form, and the thirty-five files behave as strangers."
                       % (pen["free"], pen["schema"]))
        elif pen["free"] >= -0.10 and pen["schema"] >= -0.10:
            verdict = ("PHRASING IS PORTABLE. Handoffs cost %+.2f per box under free-form notes and %+.2f "
                       "under canonical lines - within noise of the single-rod arms in both conditions. A "
                       "rod can read another rod's working notes and continue the same work, so C-80 "
                       "carries interpretable state and not only values." % (pen["free"], pen["schema"]))
        else:
            verdict = ("MIXED - handoff penalty %+.2f free, %+.2f schema. The interaction runs the wrong "
                       "way for a representation account; read the crossing rows before concluding."
                       % (pen["free"], pen["schema"]))
        pens = pen
    except KeyError:
        pens = None

    rep_ = {"id": "x08b_interpretable_state",
            "question": "can a rod read ANOTHER rod's working notes and continue the same work?",
            "measures": ["C-80", "C-16", "C-84"], "n": N, "temperature": TEMP,
            "boxes": len(BOXES), "length": LENGTH, "handoff_at": HANDOFF_AT, "seed": SEED,
            "step_max_tokens": STEP_MAXTOK, "readout_max_tokens": READOUT_MAXTOK,
            "ground_truth": truth(LENGTH), "lazy_baseline": lazy_baseline(LENGTH),
            "handoff_penalty_per_box": pens,
            "rows": rows, "verdict": verdict,
            "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}

    d_ = os.path.join(grid.STATE, "lab", "runs", "x08b_interpretable_state")
    os.makedirs(d_, exist_ok=True)
    rid = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    p = os.path.join(d_, "%s.json" % rid)
    if os.path.exists(p):
        raise ValueError("refusing to overwrite evidence at %s" % p)
    rep_["run_id"] = rid
    grid.atomic_save_json(p, rep_)
    ip = os.path.join(grid.STATE, "lab", "INDEX.json")
    idx = grid.load_json(ip, {"runs": []})
    idx.setdefault("runs", []).append({"experiment": rep_["id"], "run_id": rid, "at": rep_["at"],
                                       "check_id": "boxes-correct-of-6", "n": N,
                                       "rods": ["%s/%s" % NINE, "%s/%s" % TWENTY],
                                       "measures": rep_["measures"], "verdicts": [],
                                       "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep_


if __name__ == "__main__":
    if "--read" in sys.argv:
        i = sys.argv.index("--read")
        read_latest(sys.argv[i + 1] if len(sys.argv) > i + 1 else None)
    else:
        r = run()
        print()
        print("PENALTY (handoff - best single, per box):", r["handoff_penalty_per_box"])
        print("VERDICT:", r["verdict"])
        print("EVIDENCE  state/lab/runs/x08b_interpretable_state/%s.json" % r["run_id"])
        print()
        read_latest(r["run_id"])
