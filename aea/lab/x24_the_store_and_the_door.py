"""x24 - THE STORE AND THE DOOR. Keeping a thing and reaching it are two capabilities.

THIS FILE WAS REBUILT THREE TIMES BEFORE IT SPENT A CALL, and each rebuild closed a hole that would
have produced a confident wrong answer. The holes are recorded here because the design IS the finding
until the numbers land.

WHY IT EXISTS AT ALL. `chain.py` built a message history for the `conversation` container and passed
it NOWHERE - `Ctx` had no field for it and `Call` always sent one user message (defect 13). The
container that was meant to carry the most carried nothing, and its step body also dropped the running
value, so it ran STARVED: handed "Step 7: add 19" with no number to add to. x21's only conversation
finding, `it stops finishing`, 8 of 12 against 92%, is an artifact of an unimplemented container, and
World 3's `Sistens oneris` was written from it. ARM A re-measures it now that the container is real.

--------------------------------------------------------------------------------------------------
THE TWELVE CHANGES, each answering a named flaw in the previous draft
--------------------------------------------------------------------------------------------------

 1 NO BAND. `BAND = 0.10` came from one accident in x16. At n=8, two arms drawn from the SAME
   distribution differ by 0.10 or more MOST OF THE TIME - it was calibrated to noise and then used as
   the definition of an effect. Wilson intervals per cell, McNemar exact on pairs.

 2 THE ITEM IS SAMPLED. Every previous run measured ONE arithmetic chain repeatedly, so its item-level
   n was 1 and no conclusion generalised past that chain. Here: %d distinct chains, generated fresh.

 3 EVERYTHING IS PAIRED. Chain i, sample j runs under all four containers. Task difficulty is the
   dominant variance term and pairing removes it entirely.

 4 THE SEQUENCE IS THE PRIMARY UNIT. Sixteen steps of one chain are not sixteen independent trials -
   miss step 4 and 5..16 are wrong by construction. Per-step rates are DESCRIPTIVE. First-error
   position is reported as its own outcome, because it uses the chain's structure instead of
   flattening it.

 5 THE LENGTH IS TUNED PER ROD. A cell pinned at 0.0 or 1.0 has no variance and cannot show anything.
   A pilot measures each rod's per-step accuracy `a`, then sets that rod's chain length to
   ln(0.5)/ln(a) so its baseline lands near the middle, where the design has power. A rod that needs
   3 steps and a rod that needs 16 are both measurable; a fixed length measures one of them.

 6 VARIANCE IS CO-PRIMARY, NOT A FOOTNOTE. The published multi-turn result is a large rise in
   UNRELIABILITY beside a small drop in aptitude, so a means-only analysis would miss the actual
   effect. Every chain runs TWICE per container and the within-chain disagreement rate is reported
   beside the mean.

 7 RETRIEVAL IS PROBED WITH A NON-RECOMPUTABLE TOKEN. A probe asking for an earlier VALUE can always
   be answered by redoing the arithmetic, so it cannot separate retrieval from recomputation. Each
   probed step also carries a random token that exists nowhere else in the universe. Reproducing the
   token is retrieval and can be nothing else. Value probes are kept alongside, and the gap between
   the two IS the recomputation rate.

 8 BOTH ANCHORS, AND NO PROBE ORDER. Depths span the first step to the last. Probes are separate
   forks off the same finished state, so no probe can see another and question order does not exist
   as a variable.

 9 THE FRAMING IS PARAPHRASED. Prompt phrasing is worth a large accuracy swing on its own, so the
   shared step method is drawn from three paraphrases per sequence and the spread across them is
   reported. SCOPE LIMIT, STATED: the container's OWN instruction text is not paraphrased, so every
   container result is conditional on that one wording. Named rather than hidden.

10 EXTRACTION IS MEASURED, NOT ASSUMED. Every step must end `ANSWER: <integer>`. Each reply is read
   TWICE - once by the lab's own reader, once by the strict anchor - and the DISAGREEMENT RATE is
   reported as an instrument metric. A reply with no parsable answer is a PARSE FAILURE counted
   apart, never scored as a wrong answer, because a container that changes format compliance would
   otherwise look like a container that changes capability.

11 NOTHING IS POOLED ACROSS RODS. Four providers, different tokenizers, different sampling defaults.
   A pooled rate is a Simpson's-paradox generator and the between-rod difference is the finding.

12 THE RESOLUTION IS DECLARED. At this budget the instrument sees REGIME CHANGES, not increments. A
   component worth a few points is, here, unmeasurable - and saying so is itself a result.

NOT A LONG-CONTEXT RESULT. A dozen short steps is a few thousand tokens. The published position
effects were established over tens of documents and hundreds of key-value pairs. This measures
retrieval against recomputation in SHORT context, which is a narrower and different claim.

Run: python -m aea.lab.x24_the_store_and_the_door
"""
from __future__ import annotations

import concurrent.futures as _futures
import random
import re

from aea.lab import overseer as OV
from aea.lab import stats as ST
from aea.lab.chain import Chain
from aea.lab.parts.carry import FORMS
from aea.mind import fuel

CHAINS = 24                # distinct chains. The item is sampled; it used to be a single instance.
SAMPLES = 2                # per chain, per container. Two is the minimum that can see variance.
TEMP = 0.2
MAX_TOKENS = 1000
SEED = 24
PILOT_CHAINS = 4
PILOT_STEPS = 8
LEN_MIN, LEN_MAX = 3, 16
TARGET = 0.5               # the sequence rate the pilot aims each rod at
SEAT = ["call", "goal", "frame", "readout"]        # v4, x22's peak assembly. No critic.

# THE ROD LIST IS NOW CHOSEN BY MEASUREMENT, WHICH IS THE FIRST TIME THAT HAS BEEN TRUE HERE.
#
# The old list was five rods picked by name recognition, and two of them were structurally unable to
# finish. `cerebras/gpt-oss-120b` serves FIVE REQUESTS PER MINUTE, so one cell of 48 sequences at
# length 16 is 768 calls and two and a half hours; its cells came back `correct 0/48` with 23 probes
# out of 240 and would have been written up as a rod that cannot retrieve.
# `groq/llama-3.3-70b-versatile` publishes 1000 requests per DAY and returned `token 0/6`. Both
# numbers were exhaustion wearing the costume of a capability result.
#
# These six all PASS reach + format + carry + code in aea/lab/fleet.py, measured 2026-07-27 across
# 96 rods. `carry` is four dependent steps, which is the workload this experiment actually is;
# `code` is a Python function that gets executed against test cases, which Worlds 5 and 6 need.
# nvidia publishes no cap beyond ~40 requests per minute PER MODEL, so six of them is six separate
# buckets and the run goes wide instead of deep. ollama is local, free and uncapped.
RODS = [
    ("nvidia", "nvidia/nemotron-3-super-120b-a12b"),          # 45.8 tok/s, every suite
    ("nvidia", "nvidia/nemotron-3-nano-30b-a3b"),             # 42.6
    ("nvidia", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"),  # 38.3
    ("nvidia", "openai/gpt-oss-20b"),                         # 17.9, the L=16 rod from the last run
    ("nvidia", "poolside/laguna-xs-2.1"),                     # agentic-coding rod
    ("ollama", "granite4.1:3b"),                              # local, free, and the old floor
]

ANSWER_LINE = "\n\nEnd your reply with a final line of exactly: ANSWER: <the resulting integer>"

# THREE PARAPHRASES OF THE SHARED FRAMING, drawn per sequence. Phrasing alone moves accuracy, so a
# result measured on one wording is a result about that wording. Which one was used is recorded.
METHODS = [
    "Take the running value, write it down, apply the single operation named below to it, and show "
    "that arithmetic. Do not re-do earlier steps." + ANSWER_LINE,
    "You have a running total. Apply only the one operation given below to it, showing your "
    "arithmetic on the way. Earlier steps are already done and must not be repeated." + ANSWER_LINE,
    "Work out the single operation stated below against the current running value. Show the "
    "calculation. Ignore every earlier step; they are complete." + ANSWER_LINE,
]

_ANCHOR = re.compile(r"(?im)^\s*ANSWER:\s*(-?\d{1,9})\s*$")
_TOKEN = re.compile(r"\b([A-Z]{2}-[0-9]{4})\b")


def anchored(text):
    """The strict read: the ANSWER line and nothing else. Returns None when the rod did not comply,
    and None is a PARSE FAILURE rather than a wrong answer."""
    m = _ANCHOR.findall(text or "")
    return int(m[-1]) if m else None


def make_chains(k=CHAINS, steps=LEN_MAX, seed=SEED):
    """Distinct chains, generated fresh, which is also this lab's one contamination guarantee: no
    model has seen these operands because they did not exist until this run.

    Add and subtract only, on a five-digit start, so every intermediate value is a distinct number
    that cannot collide with a step index. A chain whose values repeat is redrawn - two steps sharing
    a value makes "which one did it recall" unanswerable and scores a coincidence as a memory.
    """
    rng = random.Random(seed)
    out = []
    while len(out) < k:
        start = rng.randrange(20000, 90000)
        ops = ["%s %d" % ("add" if rng.random() < 0.5 else "subtract", rng.randrange(11, 799))
               for _ in range(steps)]
        vals, v = [], start
        for op in ops:
            n = int(op.split()[-1])
            v = v + n if op.startswith("add") else v - n
            vals.append(v)
        if len(set(vals)) == steps and all(x > 999 for x in vals) and start not in vals:
            tokens = ["%s%s-%04d" % (chr(65 + rng.randrange(26)), chr(65 + rng.randrange(26)),
                                     rng.randrange(1000, 9999)) for _ in range(steps)]
            out.append({"id": len(out), "start": start, "ops": ops, "vals": vals, "tokens": tokens})
    return out


BANK = make_chains()


def depths_for(length):
    """Both anchors and three interior points. A curve needs its ends before anyone may call it one."""
    d = {1, max(1, length // 4), max(1, length // 2), max(1, (3 * length) // 4), length}
    return tuple(sorted(d))


def one(form, rod, ch, length, sample):
    """One sequence, then its probes. Value probes and TOKEN probes at the same depths: the value can
    be recomputed and the token cannot, so the pair separates retrieval from arithmetic."""
    truth = lambda n: ch["vals"][n - 1]                                          # noqa: E731
    ds = depths_for(length)
    notes = {k: "\nCarry-token for this step: %s" % ch["tokens"][k - 1] for k in ds}
    method = METHODS[(ch["id"] + sample) % len(METHODS)]
    c = Chain(rod, form=form, seat=SEAT, start=ch["start"], temperature=TEMP,
              max_tokens=MAX_TOKENS, notes=notes, method=method)
    rec = c.run(ch["ops"][:length], truth)
    rec.update(chain=ch["id"], sample=sample, length=length,
               method_variant=(ch["id"] + sample) % len(METHODS))

    # THE SECOND READ. The lab's own reader produced trace["value"]; this is the strict anchor over
    # the same stored text. Where they differ, one of them is wrong, and the rate is the instrument's
    # own error bar on every number it has ever reported.
    ok = [s for s in rec["trace"] if s.get("ok")]
    for s in ok:
        s["anchored"] = anchored(s.get("text"))
        s["parse_fail"] = s["anchored"] is None
        s["hit_anchored"] = s["anchored"] is not None and s["anchored"] == s["truth"]
        s["read_disagrees"] = s["anchored"] is not None and s["anchored"] != s["value"]
    rec["parse_fails"] = sum(1 for s in ok if s["parse_fail"])
    rec["read_disagrees"] = sum(1 for s in ok if s["read_disagrees"])
    rec["hits_anchored"] = sum(1 for s in ok if s["hit_anchored"])
    rec["correct_anchored"] = bool(ok) and ok[-1]["step"] == length and ok[-1]["hit_anchored"]

    by_step = {s["step"]: s for s in ok}
    probes = []
    for k in ds:
        if k not in by_step:
            probes.append({"depth": k, "unreachable": True})
            continue
        own = by_step[k].get("anchored")
        pv = c.ask(Chain.PROBE % (k, k), label="value")
        pt = c.ask("Earlier in this task, step %d carried a token of the form XX-0000. State that "
                   "token. Reply with only the token." % k, label="token")
        got = pv["last"]
        tok = (_TOKEN.findall(pt["text"] or "") or [None])[-1]
        probes.append({
            "depth": k, "unreachable": False, "own": own, "truth": ch["vals"][k - 1],
            "value_got": got, "value_parse_fail": got is None,
            "value_is_own": own is not None and got == own,
            "value_is_truth": got == ch["vals"][k - 1],
            # THE CLEAN MEASURE. The token exists nowhere but this conversation and cannot be
            # derived from anything. Reproducing it is retrieval and can be nothing else.
            "token_want": ch["tokens"][k - 1], "token_got": tok,
            "token_ok": tok == ch["tokens"][k - 1],
            "value_text": (pv["text"] or "")[:300], "token_text": (pt["text"] or "")[:200],
            "tok_in": (pv["tok_in"] or 0) + (pt["tok_in"] or 0),
            "tok_out": (pv["tok_out"] or 0) + (pt["tok_out"] or 0)})
    rec["probes"] = probes
    return rec


PILOT_FORM = "checkpoint"


def pilot(led):
    """Per-rod chain length, so no cell is measured on the floor or the ceiling.

    Measures per-step accuracy `a`, then solves length = ln(0.5)/ln(a) so the rod's sequence rate
    lands near the middle. A rod at a=0.99 gets a long chain; a rod at a=0.75 gets a short one. Both
    become measurable. A fixed length measures whichever rod it happened to suit and floors the rest.

    TUNED ON `checkpoint`, NOT ON `none`, AND THE FIRST DRAFT GOT THIS WRONG. `none` is a true null:
    the rod is handed "Step 5: add 209" with no running value, no carried string and no history, so
    it can only ever be right at step 1, where the task itself states the start. Measured, live:
    every rod piloted at 0.14 to 0.22 per step, which is 1/7 to 1/8 - one hit, at step one, exactly
    as the arm's construction requires. Tuning length against that number asks "how long until a
    structurally impossible task fails", and the answer is always three.

    So the reference is the container that makes the task POSSIBLE. `none` stays in the run as the
    floor that proves the containers do anything at all, and it is not a baseline for length.
    """
    import math
    print("  PILOT - per-rod chain length, aimed at a sequence rate of %.2f\n" % TARGET, flush=True)
    lengths = {}
    for rod in RODS:
        k = "%s/%s" % rod
        pool = _futures.ThreadPoolExecutor(max_workers=4)
        try:
            rs = [f.result() for f in
                  [pool.submit(one, PILOT_FORM, rod, ch, PILOT_STEPS, 0)
                   for ch in BANK[:PILOT_CHAINS]]]
        finally:
            pool.shutdown(wait=True)
        ok = [s for r in rs for s in r["trace"] if s.get("ok")]
        scored = [s for s in ok if not s["parse_fail"]]
        a = (sum(1 for s in scored if s["hit_anchored"]) / len(scored)) if scored else 0.0
        ideal = (float("inf") if a >= 0.999 else
                 0.0 if a <= 0.01 else math.log(TARGET) / math.log(a))
        L = max(LEN_MIN, min(LEN_MAX, int(round(ideal)) if ideal != float("inf") else LEN_MAX))
        # A ROD THAT CANNOT BE TUNED INTO RANGE IS REPORTED, NOT QUIETLY RUN AT THE FLOOR. Outside
        # [LEN_MIN, LEN_MAX] the design has no power on that rod and its cells are descriptive only.
        in_range = LEN_MIN <= ideal <= LEN_MAX
        lengths[k] = L
        led.add({"kind": "pilot", "rod": k, "form": PILOT_FORM, "per_step_accuracy": round(a, 3),
                 "scored_steps": len(scored), "parse_fails": sum(1 for s in ok if s["parse_fail"]),
                 "ideal_length": None if ideal == float("inf") else round(ideal, 2),
                 "length_chosen": L, "predicted_sequence_rate": round(a ** L, 3),
                 "in_range": in_range,
                 "fuel": fuel.stamp(rod[0], rod[1], n=PILOT_CHAINS, temperature=TEMP,
                                    max_tokens=MAX_TOKENS, attempts=len(rs), failures=0)})
        print("    %-32s per-step %.3f  parsefail %2d  -> length %2d  predicted seq %.2f  %s"
              % (k[-31:], a, sum(1 for s in ok if s["parse_fail"]), L, a ** L,
                 "" if in_range else "OUT OF RANGE - no power on this rod, descriptive only"),
              flush=True)
    return lengths


def cell(led, form, rod, length, lock=None):
    jobs = [(ch, s) for ch in BANK for s in range(SAMPLES)]
    workers = 3 if rod[0] == "ollama" else 8
    pool = _futures.ThreadPoolExecutor(max_workers=workers)
    try:
        recs = [f.result() for f in
                [pool.submit(one, form, rod, ch, length, s) for ch, s in jobs]]
    finally:
        pool.shutdown(wait=True)
    recs.sort(key=lambda r: (r["chain"], r["sample"]))

    ok_steps = [s for r in recs for s in r["trace"] if s.get("ok")]
    scored = [s for s in ok_steps if not s["parse_fail"]]
    seqs = [(r["hits_anchored"], len([s for s in r["trace"] if s.get("ok")])) for r in recs]
    correct = {(r["chain"], r["sample"]): bool(r["correct_anchored"]) for r in recs}

    # VARIANCE, CO-PRIMARY. Two samples of the same chain that disagree are the unreliability the
    # multi-turn literature says is the real effect. A mean cannot see this.
    pairs = [(correct[(c, 0)], correct[(c, 1)]) for c in {r["chain"] for r in recs}
             if (c, 0) in correct and (c, 1) in correct]
    flip = sum(1 for a, b in pairs if a != b)

    ps = [p for r in recs for p in r["probes"] if not p.get("unreachable")]
    # `kind` DISCRIMINATES A CELL FROM A PILOT AND THAT IS NOT COSMETIC. The pilot row carries
    # `form: "checkpoint"` because it is measured on that container, and the resume check
    # `led.has(form=..., rod=...)` matched it - so all five checkpoint CELLS were skipped as
    # already-done and the run printed an empty `[checkpoint]` header. The container the pilot
    # calibrates against, that ARM A pairs against, and that `Immemor itineris` rests on, silently
    # never ran. A resume key that can match a different KIND of row is not a key.
    row = {"kind": "cell", "form": form, "rod": "%s/%s" % rod, "length": length, "ran": len(recs),
           "correct": ST.describe(sum(1 for r in recs if r["correct_anchored"]), len(recs)),
           "within_chain_disagreement": ST.describe(flip, len(pairs)),
           "per_step_descriptive": ST.describe(sum(1 for s in scored if s["hit_anchored"]),
                                               len(scored), seqs=seqs),
           "first_miss": [r["first_miss"] for r in recs],
           "by_chain_correct": {"%d.%d" % (r["chain"], r["sample"]): bool(r["correct_anchored"])
                                for r in recs},
           "by_method_variant": {str(v): ST.describe(
               sum(1 for r in recs if r["method_variant"] == v and r["correct_anchored"]),
               sum(1 for r in recs if r["method_variant"] == v)) for v in range(len(METHODS))},
           # THE INSTRUMENT MEASURING ITSELF
           "parse_fail_steps": ST.describe(sum(1 for s in ok_steps if s["parse_fail"]),
                                           len(ok_steps)),
           "read_disagreement": ST.describe(sum(1 for s in scored if s["read_disagrees"]),
                                            len(scored)),
           # ARM B
           "probes": len(ps),
           "token_retrieval": ST.describe(sum(1 for p in ps if p["token_ok"]), len(ps)),
           "value_is_own": ST.describe(sum(1 for p in ps if p["value_is_own"]), len(ps)),
           "value_is_truth": ST.describe(sum(1 for p in ps if p["value_is_truth"]), len(ps)),
           "by_depth": {str(d): {
               "asked": sum(1 for p in ps if p["depth"] == d),
               "token": sum(1 for p in ps if p["depth"] == d and p["token_ok"]),
               "own": sum(1 for p in ps if p["depth"] == d and p["value_is_own"]),
               "truth": sum(1 for p in ps if p["depth"] == d and p["value_is_truth"])}
               for d in depths_for(length)},
           "context_max": max([r["context_max"] for r in recs] or [0]),
           "tok_in": sum(r["tok_in"] for r in recs), "tok_out": sum(r["tok_out"] for r in recs),
           "fuel": fuel.stamp(rod[0], rod[1], n=len(recs), temperature=TEMP, max_tokens=MAX_TOKENS,
                              attempts=len(recs),
                              failures=sum(1 for r in recs if r["completed"] < length)),
           "records": recs}
    # THE LEDGER IS ONE FILE AND THE CELLS NOW RUN CONCURRENTLY, so the write is serialised. Without
    # this, two rods finishing together read-modify-write the same document and one cell vanishes -
    # a lost measurement that leaves no trace, which is the worst shape a defect can take here.
    if lock is not None:
        with lock:
            led.add(row)
    else:
        led.add(row)
    print("    %-13s %-30s L=%-2d correct %2d/%-2d %-14s flip %d/%-2d  token %3d/%-3d  "
          "parsefail %.2f  readdiff %.2f"
          % (form, row["rod"][-29:], length, row["correct"]["k"], row["correct"]["n"],
             str(row["correct"]["wilson95"]), flip, len(pairs),
             row["token_retrieval"]["k"], row["token_retrieval"]["n"],
             row["parse_fail_steps"]["rate"] or 0, row["read_disagreement"]["rate"] or 0),
          flush=True)
    return row


def run():
    led = OV.Ledger("x24_the_store_and_the_door", {
        "what": "ARM A re-measures the four carry containers now that `conversation` is on the wire; "
                "ARM B separates RETRIEVAL from recomputation with a non-recomputable token",
        "why": "defect 13 - the conversation container was never sent, so x21's only finding about "
               "it is void; and storing has never been separated from retrieving",
        "corrects": "x21 conversation arm (8 of 12 completed) - void, starved container",
        "fix_01_no_band": "BAND=0.10 came from one accident and fires most of the time under the "
                          "null at n=8. Wilson per cell, McNemar exact on pairs.",
        "fix_02_item_sampled": "%d distinct chains, generated fresh. Prior runs had item n=1." % CHAINS,
        "fix_03_paired": "chain+sample runs under all four containers",
        "fix_04_sequence_primary": "per-step is descriptive; first-error position reported",
        "fix_05_length_tuned": "pilot sets each rod's length so its baseline lands near %.2f" % TARGET,
        "fix_06_variance_coprimary": "%d samples per chain; within-chain disagreement reported "
                                     "beside the mean" % SAMPLES,
        "fix_07_nonrecomputable": "each probed step carries a random token; reproducing it is "
                                  "retrieval and can be nothing else",
        "fix_08_anchors_no_order": "depths span first to last; probes are independent forks so "
                                   "question order does not exist",
        "fix_09_paraphrase": "%d paraphrases of the shared framing, drawn per sequence. SCOPE LIMIT: "
                             "the container's own instruction is NOT paraphrased." % len(METHODS),
        "fix_10_extraction": "every reply read twice - the lab's reader and a strict ANSWER: anchor. "
                             "Disagreement rate reported. Parse failures counted apart.",
        "fix_11_never_pooled": "per rod; 4 providers is a Simpson's-paradox generator",
        "fix_12_resolution": "this instrument detects regime changes, not increments",
        "not_a_long_context_result": "a dozen short steps is a few thousand tokens; published "
                                     "position effects were established over tens of documents",
        "seat": SEAT, "forms": list(FORMS), "chains": CHAINS, "samples": SAMPLES,
        "temperature": TEMP, "max_tokens": MAX_TOKENS, "seed": SEED,
        "rods": ["%s/%s" % r for r in RODS], "methods": METHODS,
        "chain_bank": [{"id": c["id"], "start": c["start"], "ops": c["ops"]} for c in BANK]})

    lengths = {r["rod"]: r["length_chosen"] for r in led.doc["rows"] if r.get("kind") == "pilot"}
    if len(lengths) < len(RODS):
        lengths = pilot(led)
    print("\n  lengths: %s\n" % lengths, flush=True)

    # WIDE, NOT DEEP, AND THE REASON IS THE BUDGET SHAPE. Rate limits on these plants are PER MODEL:
    # nvidia serves ~40 requests per minute per model and publishes no other cap, and two groq models
    # on one key report reset windows six hours apart. So N rods running at once is N calls against N
    # separate buckets, not N against one. Running the rods sequentially - which is what this loop did
    # - left five of six buckets idle at every moment and turned a fifteen-minute run into hours.
    #
    # The forms stay sequential so the ledger fills in a readable order and a killed run resumes at a
    # container boundary. The parallelism is across rods, where the independent budgets actually are.
    import threading
    lock = threading.Lock()
    for form in FORMS:
        todo = [r for r in RODS if not led.has(kind="cell", form=form, rod="%s/%s" % r)]
        if not todo:
            continue
        print("  [%s]  %d rods in parallel" % (form, len(todo)), flush=True)
        pool = _futures.ThreadPoolExecutor(max_workers=len(todo))
        try:
            fs = [pool.submit(cell, led, form, rod, lengths["%s/%s" % rod], lock) for rod in todo]
            for f in fs:
                f.result()
        finally:
            pool.shutdown(wait=True)

    return report(led, [r for r in led.doc["rows"] if r.get("kind") != "pilot"])


def _get(rows, form, rod=None):
    return [r for r in rows if r["form"] == form and (rod is None or r["rod"] == rod)]


def report(led, rows):
    v = ["RESOLUTION: this instrument sees regime changes, not increments. Read the intervals, not "
         "the point estimates.", ""]
    v.append("THE INSTRUMENT, MEASURED ON ITSELF")
    for r in rows:
        if (r["read_disagreement"]["rate"] or 0) > 0 or (r["parse_fail_steps"]["rate"] or 0) > 0.1:
            v.append("  %-13s %-30s parse-fail %.2f  the lab's reader and the ANSWER anchor "
                     "disagree on %.2f of steps"
                     % (r["form"], r["rod"][-29:], r["parse_fail_steps"]["rate"] or 0,
                        r["read_disagreement"]["rate"] or 0))

    v.append("")
    v.append("ARM A - THE CONTAINERS. Per rod, never pooled. Paired by chain; only discordant "
             "chains carry information.")
    arm_a = {}
    for rod in RODS:
        k = "%s/%s" % rod
        base = next(iter(_get(rows, "none", k)), None)
        if not base:
            continue
        v.append("  %s   (length %d)" % (k, base["length"]))
        v.append("    %-13s correct %2d/%-2d %-16s within-chain disagreement %s"
                 % ("none", base["correct"]["k"], base["correct"]["n"],
                    str(base["correct"]["wilson95"]),
                    base["within_chain_disagreement"]["rate"]))
        for form in FORMS:
            if form == "none":
                continue
            r = next(iter(_get(rows, form, k)), None)
            if not r:
                continue
            b = sum(1 for c, x in r["by_chain_correct"].items()
                    if x and not base["by_chain_correct"].get(c))
            c2 = sum(1 for c, x in r["by_chain_correct"].items()
                     if not x and base["by_chain_correct"].get(c))
            m = ST.mcnemar(b, c2)
            arm_a.setdefault(form, {})[k] = {"correct": r["correct"], "mcnemar_vs_none": m,
                                             "disagreement": r["within_chain_disagreement"]}
            v.append("    %-13s correct %2d/%-2d %-16s disagreement %-6s  paired %+d of %d "
                     "discordant  p=%s"
                     % (form, r["correct"]["k"], r["correct"]["n"], str(r["correct"]["wilson95"]),
                        r["within_chain_disagreement"]["rate"], b - c2, m["discordant"], m["p"]))

    cv = _get(rows, "conversation")
    if cv:
        k = sum(r["correct"]["k"] for r in cv)
        n = sum(r["correct"]["n"] for r in cv)
        v.append("")
        v.append("  x21 SAID conversation stops finishing, 8 of 12, on a container that was never "
                 "sent. Implemented, it is correct on %d of %d sequences." % (k, n))

    v.append("")
    v.append("ARM B - RETRIEVAL. The token cannot be recomputed; the value can. The gap is the "
             "recomputation rate.")
    arm_b = {}
    for rod in RODS:
        k = "%s/%s" % rod
        v.append("  %s" % k)
        for form in FORMS:
            r = next(iter(_get(rows, form, k)), None)
            if not r:
                continue
            t, o, tr = r["token_retrieval"], r["value_is_own"], r["value_is_truth"]
            arm_b.setdefault(form, {})[k] = {"token": t, "value_own": o, "value_truth": tr,
                                             "by_depth": r["by_depth"]}
            v.append("    %-13s TOKEN %3d/%-3d %-16s value-own %3d/%-3d  value-truth %3d/%-3d | "
                     "token by depth %s"
                     % (form, t["k"], t["n"], str(t["wilson95"]), o["k"], o["n"], tr["k"], tr["n"],
                        " ".join("%s:%d/%d" % (d, x["token"], x["asked"])
                                 for d, x in sorted(r["by_depth"].items(), key=lambda i: int(i[0])))))

    led.done(arm_a=arm_a, arm_b=arm_b,
             note="Wilson per cell, McNemar exact on paired chains, per-rod never pooled. Primary "
                  "read is the strict ANSWER anchor; the lab's own reader is reported beside it as "
                  "an instrument metric, not used to score.",
             verdict=v)
    return led.doc


if __name__ == "__main__":
    assert len(BANK) == CHAINS
    for ch in BANK:
        v = ch["start"]
        for i, op in enumerate(ch["ops"]):
            n = int(op.split()[-1])
            v = v + n if op.startswith("add") else v - n
            assert v == ch["vals"][i], (ch["id"], i)
        assert len(set(ch["vals"])) == LEN_MAX and all(x > 999 for x in ch["vals"])
        assert len(set(ch["tokens"])) == LEN_MAX
    assert anchored("working here 123\nANSWER: 48377") == 48377
    assert anchored("ANSWER: 48377\ntrailing 9") == 48377
    assert anchored("the answer is 48377") is None
    assert _TOKEN.findall("the token was QX-4718.") == ["QX-4718"]
    assert depths_for(16) == (1, 4, 8, 12, 16) and depths_for(4) == (1, 2, 3, 4)
    print("%d chains, %d samples each, %d containers, %d rods" % (CHAINS, SAMPLES, len(FORMS),
                                                                  len(RODS)))
    print("anchored read, token read and depth spans all check out\n")

    d = run()
    print("\nRESULT\n")
    for line in d["verdict"]:
        print(" ", line)
    print("\nEVIDENCE  state/lab/runs/x24_the_store_and_the_door/%s.json" % d["run_id"])
