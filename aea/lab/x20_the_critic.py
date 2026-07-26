"""x20 - THE CRITIC. World 2's first assemblable repair part, and the test its whole world rests on.

THE SITUATION THIS RUN EXISTS TO RESOLVE. World 2 is THE CORRECTOR, the REPAIR class, and it has seven
components. Four are seatable and NOT ONE OF THEM IMPROVES AN ANSWER:

    MEASURE      inert   (a gauge by design - x13, fooled 0 of 153)
    CLOCK        inert   (a diagnostic channel - Tardus erroris, 8.18x on ONE rod, 0.95 on another)
    READOUT      inert   (x17 and x18 both, median +0.04)
    VALIDATION   harmful (x17 harmful, x18 conditional -0.18; on the rod that needs nothing, 7/7 -> 0/7)

The other three - CRITIC, LADDER, COUNCIL - have never been in the catalogue and carry the entire
"prevention dominates repair" claim. **A world named REPAIR currently contains nothing that repairs.**

THE CRITIC is the cheapest of the three to build: one more call on the same fuel with the first answer
in the prompt. It is now seated in `organism.py` at a new REPAIR stage, and this run puts it through the
same lattice, the same noise band and the same rods as every other component, so its number is
comparable rather than special.

COST IS A FIRST-CLASS OUTCOME HERE, not a footnote. World 1 was free; World 2's entire premise is that
seeing costs. Every cell records tokens with and without the critic, so the price is measured.

THE BATTERY IS DELIBERATELY MIXED. `x18` established that counting tasks flatter components, because
the method fully specifies the answer. Traps do not: a rod that "knows" the method still answers 10 on
bat-and-ball. If the critic only pays on traps, that is a finding about WHEN to seat it rather than a
null result.

    Run: python -m aea.lab.x20_the_critic
"""
from __future__ import annotations

import concurrent.futures as _futures
import itertools
import statistics

from aea.lab import overseer as OV
from aea.lab.organism import Organism
from aea.lab.x16_the_organisms import TASKS as COUNT_TASKS
from aea.lab.x18_second_battery import TASKS as TRAP_TASKS
from aea.mind import fuel

N = 8
TEMP = 0.2
BAND = 0.10                      # measured, not chosen: x16 ran one assembly twice and got 0.70 / 0.60

# The shape components the critic sits above, so its margin is read against a real assembly rather than
# against a bare call. Four subsets, each with and without the critic.
BASES = [[], ["goal"], ["frame"], ["goal", "frame"]]

TASKS = {"vowelcount": COUNT_TASKS["vowelcount"],      # counting: the method specifies the answer
         "batball": TRAP_TASKS["batball"],             # trap: the method does NOT defeat the intuition
         "aggregate": TRAP_TASKS["aggregate"]}         # aggregate: many intermediates to get wrong

RODS = [
    ("ollama", "granite4.1:3b"),                        # needs the frame: 0.00 bare
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),    # needs nothing: 0.93 bare. The rod with nothing to repair
    ("groq",   "llama-3.1-8b-instant"),                 # middling, and cheap to run
]

# ── THE SEALED OPENING ────────────────────────────────────────────────────────────────────────────
# Written before a single call. Chapter III went 1-for-4 on its predictions and the three losses were
# worth more than the win, because they had been written down and could not be quietly adjusted.
PREDICTIONS = {
    "1_critic_pays_on_traps": {
        "claim": "median margin on the TRAP tasks is >= +0.10, outside the band",
        "why": "a trap is where a first answer is confidently wrong, which is the only condition a "
               "second look can exploit. If the critic pays anywhere, it pays here"},
    "2_critic_inert_on_counting": {
        "claim": "median margin on the COUNTING task is inside the band, |m| < 0.10",
        "why": "x18: when the method fully specifies the answer there is nothing left to repair, which "
               "is exactly why the readout scored inert on that battery"},
    "3_cost_under_3x": {
        "claim": "median token cost with the critic is under 3.0x the cost without",
        "why": "the 6.4x prior came from a 50-step chain where the reply itself was enormous. A smoke "
               "test on one short task measured 2.4x"},
    "4_critic_corrupts_UNSCORED_IN_RUN_1": {
        "claim": "at least one cell where the critic makes a CORRECT answer wrong. corrupted >= 1",
        "why": "a critic asked to check will sometimes 'fix' something that was already right. If this "
               "never happens the instrument is not actually re-deciding, only echoing"},
    "5_nothing_to_repair_on_the_strong_rod": {
        "claim": "on nemotron-3-ultra-550b the critic's margin is inside the band or negative",
        "why": "the prior receipt found nothing to repair on 4 of 5 rods, and this is the rod that "
               "passes bare. A part with an unmet precondition buys nothing (Chapter III)"},
}


def subsets_with_critic():
    for b in BASES:
        yield list(b), list(b) + ["critic"]


def cell(led, keys, rod, task_id):
    org = Organism(["call"] + keys, rod, label="+".join(keys) or "call only")
    t = TASKS[task_id]
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        recs = [f.result() for f in [pool.submit(org.run, t, temperature=TEMP) for _ in range(N)]]
    finally:
        pool.shutdown(wait=True)
    clean = [r for r in recs if r["ok"] and not r["flags"]]
    for r in recs:
        led.note_flags(r["flags"])
    toks = [r["tok_out"] for r in clean if r.get("tok_out")]
    firsts = [r["tok_out_first"] for r in clean if r.get("tok_out_first")]
    row = {"key": "|".join(sorted(keys)), "subset": sorted(keys), "rod": "%s/%s" % rod,
           "task": task_id, "has_critic": "critic" in keys,
           "clean": len(clean), "ran": len(recs),
           "correct": sum(1 for r in clean if r["answer"] == t["truth"]),
           "repaired": sum(1 for r in clean if r.get("repaired")),
           # CORRUPTED: the critic moved an answer that was already right. Only knowable with the critic
           # seated, because `tok_out_first` marks the pre-critic answer's call.
           "tok_out_median": statistics.median(toks) if toks else None,
           "tok_first_median": statistics.median(firsts) if firsts else None,
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                              attempts=len(recs), failures=len(recs) - len(clean)),
           "records": recs}
    led.add(row)
    print("    %-22s %-24s %-11s correct %d/%-2d  repaired %d  tok %s"
          % (row["key"] or "(call only)", rod[1].rsplit("/", 1)[-1][:23], task_id,
             row["correct"], row["clean"], row["repaired"], row["tok_out_median"]), flush=True)
    return row


def run():
    led = OV.Ledger("x20_the_critic", {
        "what": "does a second call on the same fuel repair anything, and what does it cost",
        "why": "World 2 is named REPAIR and its four seatable parts measure inert, inert, inert, harmful",
        "sealed_predictions": PREDICTIONS,
        "n": N, "temperature": TEMP, "band": BAND,
        "supersedes": "20260726T160259Z, which unioned both calls' flags so a critic cell was discarded "
                      "if EITHER reply was messy. 25% of critic trials survived against 60% without, "
                      "23 of 36 critic cells had zero clean trials, and only 8 paired cells had n>=4 on "
                      "both sides. Worse, it discarded exactly the trials a critic exists for: a messy "
                      "first answer is the critic's INPUT. Flags now describe the critic's own reply.",
        "rods": ["%s/%s" % r for r in RODS], "tasks": list(TASKS),
        "bases": ["+".join(b) or "call only" for b in BASES]})
    plan = []
    for base, withc in subsets_with_critic():
        plan += [base, withc]
    total = len(plan) * len(RODS) * len(TASKS) * N
    print("x20 - %d assemblies x %d rods x %d tasks x n=%d = %d calls "
          "(critic cells fire twice, so real calls are higher)\n"
          % (len(plan), len(RODS), len(TASKS), N, total), flush=True)
    for keys in plan:
        print("  [%s]" % ("+".join(sorted(keys)) or "call only"), flush=True)
        for rod in RODS:
            for task_id in TASKS:
                if led.has(key="|".join(sorted(keys)), rod="%s/%s" % rod, task=task_id):
                    continue
                cell(led, keys, rod, task_id)

    rows = led.doc["rows"]

    def sel(keys, rod=None, task=None):
        k = "|".join(sorted(keys))
        return [r for r in rows if r["key"] == k and (rod is None or r["rod"] == rod)
                and (task is None or r["task"] == task)]

    def score(keys, **kw):
        s = sel(keys, **kw)
        tot = sum(r["clean"] for r in s)
        return (sum(r["correct"] for r in s) / tot) if tot else None

    margins = {"all": [], "trap": [], "counting": [], "by_rod": {}}
    for base, withc in subsets_with_critic():
        for task_id in TASKS:
            b, p = score(base, task=task_id), score(withc, task=task_id)
            if None in (b, p):
                continue
            m = round(p - b, 3)
            margins["all"].append(m)
            margins["counting" if task_id == "vowelcount" else "trap"].append(m)
        for rod in RODS:
            k = "%s/%s" % rod
            b, p = score(base, rod=k), score(withc, rod=k)
            if None not in (b, p):
                margins["by_rod"].setdefault(k, []).append(round(p - b, 3))

    def med(xs):
        return round(statistics.median(xs), 3) if xs else None

    cost = []
    for r in rows:
        if r["has_critic"] and r["tok_out_median"] and r["tok_first_median"]:
            cost.append(r["tok_out_median"] / r["tok_first_median"])
    cost_median = round(statistics.median(cost), 2) if cost else None
    # CORRUPTION, scored properly this time. Run 1's expression compared a cell's correct COUNT against
    # a RATE from a different selection and was meaningless. A corruption is a paired cell where the
    # critic's accuracy is below its own baseline by more than the band, on the same rod and task.
    corrupted = 0
    for base, withc in subsets_with_critic():
        for task_id in TASKS:
            for rod in RODS:
                k = "%s/%s" % rod
                b, p2 = score(base, rod=k, task=task_id), score(withc, rod=k, task=task_id)
                if None not in (b, p2) and (p2 - b) <= -BAND:
                    corrupted += 1

    v, verdicts = [], {}
    mt, mc, ma = med(margins["trap"]), med(margins["counting"]), med(margins["all"])
    verdicts["1_critic_pays_on_traps"] = (mt is not None and mt >= BAND)
    verdicts["2_critic_inert_on_counting"] = (mc is not None and abs(mc) < BAND)
    verdicts["3_cost_under_3x"] = (cost_median is not None and cost_median < 3.0)
    verdicts["4_critic_corrupts"] = corrupted >= 1
    strong = "nvidia/nvidia/nemotron-3-ultra-550b-a55b"
    ms = med(margins["by_rod"].get(strong, []))
    verdicts["5_nothing_to_repair_on_the_strong_rod"] = (ms is not None and ms < BAND)

    won = sum(1 for x in verdicts.values() if x)
    v.append("SEALED PREDICTIONS: %d of %d held." % (won, len(verdicts)))
    for k, ok in verdicts.items():
        v.append("  %-38s %s" % (k, "HELD" if ok else "LOST"))
    v.append("MARGIN: traps %s, counting %s, overall %s (band %.2f)" % (mt, mc, ma, BAND))
    v.append("COST: median %sx the tokens of the same assembly without a critic" % cost_median)
    if ma is not None and abs(ma) < BAND:
        v.append("THE CRITIC IS INERT TOO. That makes FIVE of World 2's seven components measured and "
                 "not one of them improving an answer, and the world's name becomes a claim with "
                 "nothing behind it. THE CORRECTOR would have to become THE WITNESS: a world that "
                 "grants sight rather than repair.")
    elif ma is not None and ma >= BAND:
        v.append("THE CRITIC PAYS. World 2 has its first real repair part, and its price is the "
                 "mechanic: %sx tokens for %+.2f accuracy." % (cost_median, ma))
    else:
        v.append("THE CRITIC IS HARMFUL. A second look makes it worse, which would make World 2 a world "
                 "where every instrument the player owns costs and damages.")

    led.done(margins=margins, medians={"trap": mt, "counting": mc, "all": ma},
             cost_median=cost_median, corrupted=corrupted,
             predictions=PREDICTIONS, prediction_results=verdicts, verdict=v)
    return led.doc


if __name__ == "__main__":
    print("SEALED OPENING - written before any call\n")
    for k, p in PREDICTIONS.items():
        print("  %-38s %s" % (k, p["claim"]))
    print()
    d = run()
    print("\nRESULT\n")
    for line in d["verdict"]:
        print(" ", line)
    print("\noverseer:", d["overseer"])
    print("EVIDENCE  state/lab/runs/x20_the_critic/%s.json" % d["run_id"])
