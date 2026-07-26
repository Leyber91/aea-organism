"""x19 - THE UNMEASURED PAIR. The two creatures on the World 1 plate that no part has ever been tried on.

The bestiary paints every creature with a STATE: a part opens it, a part harms it, or nothing reaches it.
Two entries cannot be painted, and the art direction had to invent a fourth swatch for them:

  Rogans vacui   asks what you wanted instead of filling the hole. 16 of 304. NO part has ever been
                 tested against it. The only intervention on record is supplying the goal, which deletes
                 the behaviour rather than improving the creature
  Iterans sui    collapses into a verbatim loop. The annex claimed 28 instances "all on the trap battery
                 under a fitted frame". Those 28 are DETECTOR ARTIFACTS: the `degenerate` flag firing on
                 ordinary markdown tables, one rod, four subsets, two of them frameless. Scanning every
                 stored reply in the project for real verbatim repetition returns THREE

A plate that teaches "seat a part, the creature opens" cannot carry two creatures whose state is a guess.

WHAT THIS MEASURES, AND WHAT IT DELIBERATELY DOES NOT. Both behaviours live in the REPLY. Only the SHAPE
components can reach them: `goal` and `frame` change what is sent. `readout` and `validation` act after
the reply exists and cannot change a word of it, so testing them here would be theatre with a known
answer. Four shape conditions, and the design is honest that it is four rather than sixteen.

THE PRIOR THAT MAKES THIS WORTH RUNNING. Asking is not distributed across the region. Re-reading x12 by
rod:

    cerebras/gpt-oss-120b      12 of 44    27.3%
    ollama/qwen3:0.6b           1 of 64     1.6%
    ollama/granite4.1:3b        1 of 64     1.6%
    ollama/granite4.1:8b        1 of 64     1.6%
    groq/llama-3.1-8b-instant   1 of 61     1.6%
    groq/llama-3.3-70b          0 of  7     0.0%

Twelve of the sixteen asks came from ONE PLANT. If that holds at power, `Rogans vacui` is not the region's
rare conscience, it is a FUEL PHENOTYPE, and Law IV says so plainly: the same construct on different fuel
is a different organism. The creature would then teach something better than rarity - where you find it
tells you what you are standing on.

POWER. Asking runs near 5% pooled and 27% on one rod. n=8 cannot see that move; n=20 per cell pools to 160
per condition, which separates 5% from 20%. The 640 calls are the price of not painting a guess.

Run: python -m aea.lab.x19_the_unmeasured_pair
"""
from __future__ import annotations

import concurrent.futures as _futures
import re

from aea.lab import overseer as OV
from aea.lab.organism import Organism
from aea.lab.x12_L0_goal_presence import _ASKS
from aea.lab.x16_the_organisms import TASKS
from aea.mind import fuel

N = 20
TEMP = 0.2
BAND = 0.10

# SHAPE conditions only. A read component cannot change what the rod said.
CONDITIONS = [
    ("bare",       []),                    # the hole: data, no objective, no procedure
    ("goal",       ["goal"]),              # the hole is filled with an objective
    ("frame",      ["frame"]),             # filled with a procedure and no objective
    ("goal+frame", ["goal", "frame"]),     # both
]

RODS = [
    ("cerebras", "gpt-oss-120b"),                        # the asker: 12 of 44 in x12
    ("nvidia",   "nvidia/nemotron-3-ultra-550b-a55b"),   # the looper: real loops in x10 and x18
    ("ollama",   "granite4.1:3b"),                       # neither, and it needs a frame to score at all
    ("groq",     "llama-3.1-8b-instant"),                # neither
]


# --- THE LOOP DETECTOR, and it replaces the one that produced the retracted 28 ------------------------
#
# `overseer._degenerate` splits on whitespace and looks for a token run. Markdown analysis defeats it:
# bullet rows, pipe tables and repeated unit strings ("ms", "|") produce runs that are structure rather
# than collapse. It fired 28 times in x18 and not one of them is a loop.
#
# This one strips the structure first, then requires repetition in the CONTENT. It also catches the form
# the old one missed entirely: repetition with no whitespace between copies, `TheTheTheTheThe`, which is
# what the two real nemotron loops actually look like.
_STRUCT = re.compile(r"[|*_#>`\-=\[\]()]+")


def looped(text: str, min_reps: int = 6) -> bool:
    t = _STRUCT.sub(" ", text or "")
    toks = [w for w in t.split() if w]
    for size in (1, 2, 3):
        for i in range(max(0, len(toks) - size * min_reps)):
            unit = toks[i:i + size]
            # A loop is repeated LANGUAGE. A run with no letters in it is a numeric or symbolic column,
            # which is the shape that produced the 28 false positives this detector replaces.
            if not any(ch.isalpha() for ch in "".join(unit)):
                continue
            if all(toks[i + k * size:i + (k + 1) * size] == unit for k in range(min_reps)):
                return True
    # No-whitespace repetition: TheTheTheTheTheThe
    return bool(re.search(r"(\w{2,10})\1{4,}", text or ""))


def _trial(org, task, i):
    # keep_full because BOTH detectors read the body of the reply, not its answer. The first pass of
    # this experiment scored `rec["raw"]`, which is the last 320 characters, and 74% of replies in this
    # project are longer than that. Asking appears at the START of a reply. That run measured 1 of 511
    # against x12's 16 of 304 on the identical regex and it was reading the wrong end.
    rec = org.run(task, temperature=TEMP, keep_full=True)
    full = rec.get("text") or ""
    rec["asked"] = bool(_ASKS.search(full))
    rec["looped"] = looped(full)
    rec.pop("text", None)                 # scored, not stored: 640 full replies would bloat the ledger
    rec["asked_at"] = (full[:_ASKS.search(full).start()].count("\n") if rec["asked"] else None)
    return rec


def cell(led, cond_name, keys, rod, task_id):
    org = Organism(["call"] + keys, rod, label=cond_name)
    t = TASKS[task_id]
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        recs = [f.result() for f in [pool.submit(_trial, org, t, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [r for r in recs if r["ok"]]
    for r in recs:
        led.note_flags(r["flags"])
    row = {"condition": cond_name, "subset": sorted(keys), "rod": "%s/%s" % rod, "task": task_id,
           "ran": len(recs), "ok": len(ok),
           "asked": sum(1 for r in ok if r["asked"]),
           "looped": sum(1 for r in ok if r["looped"]),
           "correct": sum(1 for r in ok if not r["flags"] and r["answer"] == t["truth"]),
           "clean": sum(1 for r in ok if not r["flags"]),
           "distinct": len({(r.get("raw") or "")[-160:] for r in ok}),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                              attempts=len(recs), failures=len(recs) - len(ok)),
           "records": recs}
    led.add(row)
    print("    %-11s %-30s %-11s asked %2d/%-2d  looped %2d  correct %2d/%-2d  distinct %d"
          % (cond_name, rod[1].rsplit("/", 1)[-1][:29], task_id, row["asked"], row["ok"],
             row["looped"], row["correct"], row["clean"], row["distinct"]), flush=True)
    return row


def run():
    led = OV.Ledger("x19_the_unmeasured_pair", {
        "what": "do any parts reach Rogans vacui or Iterans sui, and is asking a plant property",
        "why": "two creatures on the World 1 plate carry a state no measurement supports",
        "scope": "SHAPE components only; read components cannot change the reply",
        "n": N, "temperature": TEMP, "band": BAND,
        "conditions": [c[0] for c in CONDITIONS],
        "rods": ["%s/%s" % r for r in RODS], "tasks": list(TASKS),
        "ask_detector": "x12._ASKS, reused verbatim so the 16-of-304 stays comparable",
        "loop_detector": "x19.looped, replaces overseer._degenerate which produced 28 false positives",
        "supersedes": "20260726T063157Z, which scored both detectors over rec['raw'] - the LAST 320 "
                      "characters. 74% of replies in this project are longer than that (median 1294) "
                      "and asking appears at the START of a reply. That run read 1 ask in 511 against "
                      "x12's 16 in 304 on the identical regex, and several of x12's own hits are "
                      "invisible in a 320-char tail. Its LOOP result stands (a loop runs to the cap, so "
                      "the tail is the loop); its ASK result does not. This run scores full text."})
    total = len(CONDITIONS) * len(RODS) * len(TASKS) * N
    print("x19 - %d conditions x %d rods x %d tasks x n=%d = %d calls\n"
          % (len(CONDITIONS), len(RODS), len(TASKS), N, total), flush=True)
    for cond_name, keys in CONDITIONS:
        print("  [%s]" % cond_name, flush=True)
        for rod in RODS:
            for task_id in TASKS:
                if led.has(condition=cond_name, rod="%s/%s" % rod, task=task_id):
                    continue
                cell(led, cond_name, keys, rod, task_id)

    rows = led.doc["rows"]

    def pool_by(field, **sel):
        s = [r for r in rows if all(r[k] == v for k, v in sel.items())]
        tot = sum(r["ok"] for r in s)
        return (sum(r[field] for r in s), tot)

    by_condition = {c: {"asked": pool_by("asked", condition=c), "looped": pool_by("looped", condition=c)}
                    for c, _ in CONDITIONS}
    by_rod = {"%s/%s" % r: {"asked": pool_by("asked", rod="%s/%s" % r),
                            "looped": pool_by("looped", rod="%s/%s" % r)} for r in RODS}

    def rate(pair):
        h, t = pair
        return (h / t) if t else None

    v = []

    # ROGANS. Is asking a construct property or a fuel property?
    #
    # TWO CORRECTIONS, both from the first pass of this file. (1) SCOPE: asking can only occur where the
    # hole exists, so pooling across `goal` and `frame` - which force it to zero by construction -
    # divides every plant's rate by four and compresses the spread toward nothing. Rate the bare
    # condition only. (2) SPREAD IS TOP MINUS BOTTOM, not top minus second. The first version asked "is
    # the leader an outlier" and reported 0.01 on a set where two plants asked at ~17% and two never
    # asked at all. The interesting split is the floor, not the runner-up.
    ask_rates = {}
    for r in RODS:
        k = "%s/%s" % r
        sel = [x for x in rows if x["rod"] == k and x["condition"] == "bare"]
        tot = sum(x["ok"] for x in sel)
        if tot:
            ask_rates[k] = sum(x["asked"] for x in sel) / tot
    if ask_rates:
        top = max(ask_rates, key=ask_rates.get)
        spread = ask_rates[top] - min(ask_rates.values())
        v.append("ASKING BY PLANT: " + ", ".join(
            "%s %.0f%%" % (k.rsplit("/", 1)[-1], 100 * r) for k, r in
            sorted(ask_rates.items(), key=lambda kv: -kv[1])))
        # THE FLOOR GUARD. A spread of 0.00 across plants means "evenly distributed" only if the
        # behaviour occurred. When every cell is zero the spread is zero by construction and the
        # distribution question is undecidable. The first pass of this experiment printed "ASKING IS
        # EVENLY DISTRIBUTED, spread 0.01, x12's rod skew was small-n noise" off a total of ONE ask in
        # 511 calls. That is the same one-sided-metric error x07b made, in a different costume.
        total_asks = sum(h for h, _ in (x["asked"] for x in by_condition.values()))
        if total_asks < 5:
            v.append("UNDECIDABLE ON DISTRIBUTION: %d asks in the whole run. Every plant reads ~0%%, so "
                     "the spread is zero by construction and says nothing about whether asking is a "
                     "fuel property. What it does say is that THE BEHAVIOUR DID NOT REPRODUCE: x12 saw "
                     "16 of 304 on the identical detector." % total_asks)
        elif spread >= BAND:
            silent = [k for k, r in ask_rates.items() if r == 0.0]
            v.append("ROGANS VACUI IS A FUEL PHENOTYPE. On the bare condition %s asks %.0f%% and %d "
                     "plant(s) never ask at all (%s), a spread of %.2f, %.0fx the band. Law IV: it is "
                     "not the region's conscience, it is some plants'. WHERE YOU FIND IT TELLS YOU WHAT "
                     "YOU ARE STANDING ON."
                     % (top.rsplit("/", 1)[-1], 100 * ask_rates[top], len(silent),
                        ", ".join(k.rsplit("/", 1)[-1] for k in silent) or "none",
                        spread, spread / BAND))
        else:
            v.append("ASKING IS EVENLY DISTRIBUTED across plants (spread %.2f, inside the band, on %d "
                     "asks). It is a property of the construct, and x12's rod skew was small-n noise."
                     % (spread, total_asks))

    bare_ask, goal_ask = rate(by_condition["bare"]["asked"]), rate(by_condition["goal"]["asked"])
    frame_ask = rate(by_condition["frame"]["asked"])
    if None not in (bare_ask, frame_ask):
        d = frame_ask - bare_ask
        v.append("A PROCEDURE WITH NO OBJECTIVE moves asking %+.2f (bare %.0f%% -> frame %.0f%%). %s"
                 % (d, 100 * bare_ask, 100 * frame_ask,
                    "That is a part reaching ROGANS." if abs(d) >= BAND else
                    "Inside the band: THE FRAME does not reach ROGANS either."))
    if None not in (bare_ask, goal_ask):
        v.append("THE GOAL takes asking %.0f%% -> %.0f%%. Filling the hole removes the behaviour; it does "
                 "not improve the creature." % (100 * bare_ask, 100 * goal_ask))

    # ITERANS. Does the loop reproduce at all, and is the frame really its trigger?
    loops = {c: by_condition[c]["looped"] for c, _ in CONDITIONS}
    n_loops = sum(h for h, _ in loops.values())
    if n_loops == 0:
        v.append("ITERANS SUI DID NOT REPRODUCE in %d calls. Three sightings across the whole project and "
                 "none here: it stays UNMEASURED on the plate, and the annex claim that a frame triggers "
                 "it has no support at any n." % total)
    else:
        v.append("ITERANS SUI: " + ", ".join("%s %d/%d" % (c, h, t) for c, (h, t) in loops.items()))
        framed = loops["frame"][0] + loops["goal+frame"][0]
        unframed = loops["bare"][0] + loops["goal"][0]
        v.append("Frame present %d, frame absent %d. %s"
                 % (framed, unframed,
                    "The frame is the trigger, as the annex guessed." if framed > 2 * max(unframed, 1)
                    else "The frame is NOT established as the trigger."))

    led.done(by_condition=by_condition, by_rod=by_rod, verdict=v)
    return led.doc


if __name__ == "__main__":
    # SELF-CHECK. The loop detector is verified against every known case before a call is spent, because
    # the finding this experiment corrects was caused by an unverified detector.
    POS = ["The user isThe needThe|TheTheTheWeThe\nTheThe\nTheTheTheTheTheThe",
           "ah ah ah ah ah ah ah ah",
           "We need to count words<unk><unk><unk><unk><unk><unk><unk><unk><unk><unk>"]
    NEG = ["* **Plant Beta** has the slowest single run (**Run b: 300 ms**) and the highest variance "
           "(range of 200 ms vs Alpha's 160 ms).\n*   **Run e (alpha)** is the overall winner.",
           "| plant | ms |\n|---|---|\n| alpha | 120 |\n| beta | 300 |\n| alpha | 250 |\n| beta | 100 |",
           "No, no, no, no, no, no",
           "1. the 2. mouth 3. draws 4. power 5. through 6. the 7. ladder 8. and 9. the 10. measure"]
    for t in POS:
        assert looped(t), "MISSED a real loop: %r" % t[:40]
    for t in NEG:
        assert not looped(t), "FALSE POSITIVE on structure: %r" % t[:40]
    print("loop detector: %d real loops caught, %d structural texts cleared\n" % (len(POS), len(NEG)))

    d = run()
    print("\nASKING AND LOOPING, BY CONDITION\n")
    print("%-12s %14s %14s" % ("condition", "asked", "looped"))
    for c, _ in CONDITIONS:
        a, l = d["by_condition"][c]["asked"], d["by_condition"][c]["looped"]
        print("%-12s %9d /%-4d %9d /%-4d" % (c, a[0], a[1], l[0], l[1]))
    print("\nBY PLANT\n")
    print("%-46s %14s %14s" % ("rod", "asked", "looped"))
    for k, x in d["by_rod"].items():
        print("%-46s %9d /%-4d %9d /%-4d"
              % (k[-45:], x["asked"][0], x["asked"][1], x["looped"][0], x["looped"][1]))
    print("\noverseer:", d["overseer"])
    print()
    for line in d["verdict"]:
        print(" -", line)
    print("\nEVIDENCE  state/lab/runs/x19_the_unmeasured_pair/%s.json" % d["run_id"])
