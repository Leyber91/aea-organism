"""x09 - IS THERE ANYTHING ON THIS BENCH THE PLAYER CAN FAIL? The blocker under the skipped rungs.

WHY THIS EXISTS. journey_check.py now fails because the playable sequence jumps L1 to L4, skipping THE
READOUT, THE FRAME and THE CRITIC. Naming the skip was easy. The reason for it turned out to be structural,
and it is not in any design document:

  ALL FIVE TASKS IN THE BENCH BANK ARE BUILT TO BE PASSED. t-01 echoes `PROBE ONLINE`, t-03 extracts a
  literal from a line, t-04 reads a number out of its own context, t-05 echoes a JSON object. t-02 is the
  only arithmetic. Every one is a `contains` check on trivially derivable output.

THE READOUT, THE FRAME and THE CRITIC all exist to RESCUE A FAILURE. With no failure available, there is
nothing for them to rescue, so the only difference the bench can show a player is cost and reach - which is
exactly the rung the game jumped to. The skip was not an oversight. It was the only rung the bench could
demonstrate.

WHAT THIS MEASURES, on the hearth the game actually fires (ollama, local, free):

  1  does the hearth FAIL t-02, the bank's only arithmetic? if it passes 8/8, the bank has no failure at
     all and every free rung is unbuildable until a task is added.
  2  does it fail WORDCOUNT, the task x02 measured? that is the candidate t-06.
  3  does the FITTED FRAME - one that names the method - convert that failure on THIS fuel? x02 measured
     0/8 to 8/8 on nvidia's 3b. The game fires ollama, and law IV says the same composition on different
     fuel is a different organism, so x02's result does not transfer. It has to be re-measured here.
  4  does the POSTURE FRAME - the `bench` template that is the ONLY non-trivial scaffold the bench
     currently offers - do anything? x01 measured posture frames at +38 to +107% input tokens for zero
     gain. If that reproduces on the hearth, then the frame the game can seat today is the one the lab
     proved worthless, and an L2 mission built on it would claim a win that did not happen.

The fitted frame is quoted VERBATIM from aea/lab/experiments/x02_fitted_frame.py so the comparison is to
the measured artefact and not to a paraphrase of it. Ground truth is local and exact.

Run: python -m aea.lab.x09_hearth_failure
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import re
import time

from aea.bench.bench_core import SCAFFOLDS, TASKS
from aea.kernel import grid
from aea.lab import harness as H
from aea.mind import fuel

N = 8
MAXTOK = 300

# TWO TEMPERATURES, and the first run of this file taught why.
#
# It ran at 0.0 with n=8 and every cell came back with ONE DISTINCT REPLY across all eight trials - ollama
# at temperature 0 is deterministic, so n=8 was n=1 wearing the harness floor's clothes. MIN_N=8 exists
# because "3 trials cannot separate 2/3 from 3/3"; eight identical trials separate nothing at all. The floor
# was satisfied on paper and empty in substance.
#
# 0.2 IS NOT AN ARBITRARY SECOND POINT - it is the temperature THE GAME ACTUALLY FIRES AT. bench_core never
# sets one, so every real bench draw goes out at grid.call_openai's default of 0.2. A measurement taken at
# 0.0 does not describe the game, and that mismatch would have been invisible without the determinism check.
#
# Both temperatures run so the determinism is DATA rather than an audit note, and `distinct` is reported per
# cell so a collapsed cell can never again be read as n=8.
TEMPS = (0.0, 0.2)
GAME_TEMP = 0.2

# The local hearth ladder, in the order energy.ladder('local','private') returns it. Three rods because
# law IV: one rod is one organism, not a result.
RODS = [("ollama", "qwen2.5:7b"), ("ollama", "granite4.1:8b"), ("ollama", "llama3.1:8b")]

WORDS = "the mouth draws power through the ladder and the measure closes the wire"      # 13 words
FITTED = ("To count words: split the sentence on spaces, number each token 1,2,3..., then report the "
          "FINAL index. Show the numbered list, then the count alone on the last line.")

WORDCOUNT = "Count the words in the sentence below and reply with ONLY the number.\n" + WORDS


def _last_number_is(want: str):
    def check(text: str) -> bool:
        nums = re.findall(r"-?\d+", (text or "").replace(",", ""))
        return bool(nums) and nums[-1] == want
    return check


def _contains(want: str):
    return lambda text: want.lower() in (text or "").lower()


# THE CELLS. Each is (id, prompt, check, note) - the prompt is what actually reaches the rod, so the frame
# arms carry their framing inline exactly as bench_core's scaffold part would apply it.
CELLS = [
    ("t-02_bare", TASKS["t-02"]["prompt"], _contains("391"), "391",
     "the bank's only arithmetic - if this passes 8/8 the bank has no failure to rescue"),
    ("wordcount_bare", WORDCOUNT, _last_number_is("13"), "13",
     "the candidate t-06 - x02's task, unframed, on the hearth"),
    ("wordcount_posture", SCAFFOLDS["bench"].replace("{prompt}", WORDCOUNT), _last_number_is("13"), "13",
     "the ONLY non-trivial frame the bench can seat today - x01 measured its kind at zero gain"),
    ("wordcount_fitted", FITTED + "\n\n" + WORDCOUNT, _last_number_is("13"), "13",
     "the frame that names the METHOD - x02 measured 0/8 to 8/8 on nvidia's 3b"),
]


def readout(text: str):
    """THE READOUT (candidate C-87, L1): read the answer out of the WORK rather than the summary.

    Zero tokens, zero latency, pure local parsing - the final index of the rod's own enumeration. This is
    an ARM, not an analysis step, because the first run found the phenomenon on this hearth: llama3.1:8b
    enumerated the sentence to 13 correctly and then reported 14. The frame did its job; the readout lost
    it. Scoring both `stated` and `from_work` on the same reply prices the composition at no extra cost.
    """
    idx = [int(m.group(1)) for m in re.finditer(r"(?m)^\s*(\d{1,2})\.\s+\S", text or "")]
    return max(idx) if idx else None


def _trial(rod, prompt, check, want, i, temp):
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": prompt}],
                     max_tokens=MAXTOK, temperature=temp)
    if not r.get("ok"):
        return {"trial": i, "ok": False, "error": r.get("error")}
    text = r.get("text") or ""
    w = readout(text)
    return {"trial": i, "ok": True, "pass": bool(check(text)), "raw": text[-400:],
            "from_work": w, "pass_with_readout": bool(check(text) or (w is not None and str(w) == want)),
            "enumerated": w is not None,
            "tok_in": r.get("prompt_tokens") or 0, "tok_out": r.get("tokens") or 0}


def cell(rod, cid, prompt, check, want, note, temp):
    # max_workers=4 rather than 8: ollama is VRAM-bound and oversubscription makes it slower, not faster
    # (the D13 lesson about ONNX thrashing, one layer up).
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        trials = [f.result() for f in
                  [pool.submit(_trial, rod, prompt, check, want, i, temp) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [t for t in trials if t["ok"]]
    # DISTINCT IS THE HONEST n. Eight identical replies are one measurement repeated eight times, and
    # reporting them as 8 is the same error class as counting our own impatience as a rod's defect.
    distinct = len({t["raw"] for t in ok})
    row = {"rod": "%s/%s" % rod, "cell": cid, "note": note, "temperature": temp,
           "passes": sum(1 for t in ok if t["pass"]), "scored": len(ok),
           "passes_with_readout": sum(1 for t in ok if t["pass_with_readout"]),
           "enumerated": sum(1 for t in ok if t["enumerated"]),
           "distinct_replies": distinct, "effective_n": distinct,
           "errors": [t.get("error") for t in trials if not t["ok"]][:2],
           "tok_in": sum(t.get("tok_in", 0) for t in ok),
           "tok_out": sum(t.get("tok_out", 0) for t in ok),
           "prompt_chars": len(prompt),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=temp,
                              attempts=len(trials), failures=len(trials) - len(ok)),
           "trials": trials}
    print("  t=%.1f %-16s %-20s stated %d/%-2d  +readout %d/%-2d  distinct=%d  tok_in=%d"
          % (temp, rod[1], cid, row["passes"], row["scored"], row["passes_with_readout"],
             row["scored"], distinct, row["tok_in"]), flush=True)
    return row


def run():
    print("x09 - the hearth bank: %d rods x %d cells x n=%d x temps %s (the game fires at %.1f)"
          % (len(RODS), len(CELLS), N, TEMPS, GAME_TEMP))
    rows = []
    for temp in TEMPS:
        for rod in RODS:
            for cid, prompt, check, want, note in CELLS:
                rows.append(cell(rod, cid, prompt, check, want, note, temp))

    # EVERY VERDICT IS READ AT THE GAME'S TEMPERATURE. The 0.0 arms are kept as the determinism receipt,
    # not as the basis of a decision about a game that does not run at 0.0.
    at_game = [r for r in rows if r["temperature"] == GAME_TEMP]

    def rate(rod, cid, key="passes"):
        r = next((x for x in at_game if x["rod"] == rod and x["cell"] == cid), None)
        return (r[key] / r["scored"]) if r and r["scored"] else None

    findings, verdicts, diagnosis = [], {}, {}
    for rod in ["%s/%s" % r for r in RODS]:
        short = rod.rsplit("/", 1)[-1]
        t02, bare = rate(rod, "t-02_bare"), rate(rod, "wordcount_bare")
        post, fit = rate(rod, "wordcount_posture"), rate(rod, "wordcount_fitted")
        fit_ro = rate(rod, "wordcount_fitted", "passes_with_readout")
        enum = rate(rod, "wordcount_fitted", "enumerated")
        verdicts[rod] = {"t02": t02, "bare": bare, "posture": post, "fitted": fit,
                         "fitted_plus_readout": fit_ro, "enumerated": enum}
        if t02 is not None and t02 >= 1.0:
            findings.append("%s passes t-02 - the bank's only arithmetic is not a failure for it" % short)
        if bare is not None and bare <= 0.5:
            findings.append("%s FAILS wordcount bare (%.0f%%) - a real failure the free rungs could rescue"
                            % (short, 100 * bare))
        if None not in (bare, fit) and fit - bare >= 0.25:
            findings.append("%s: the FITTED frame converts it, %.0f%% to %.0f%%" % (short, 100 * bare,
                                                                                    100 * fit))
        if None not in (bare, post) and abs(post - bare) < 0.15:
            findings.append("%s: the POSTURE frame changes nothing (%.0f%% vs %.0f%%)"
                            % (short, 100 * post, 100 * bare))

        # THE DIAGNOSIS PER ROD. THE_JOURNEY.md's own finding is that the climb is a diagnosis rather than a
        # collection - which row you need is a function of which rod you hold. This computes that per rod,
        # and the FRAME+READOUT case is the cumulative claim: neither part alone is enough.
        if bare is not None and bare >= 0.9:
            diagnosis[short] = "needs nothing - passes bare"
        elif fit is not None and fit >= 0.9:
            diagnosis[short] = "needs THE FRAME alone"
        elif None not in (fit, fit_ro) and fit_ro - fit >= 0.25:
            diagnosis[short] = ("needs THE FRAME **and** THE READOUT - the frame produced correct work "
                                "(%.0f%% enumerated) and the rod misreported it; the readout costs 0 tokens"
                                % (100 * (enum or 0)))
            findings.append("%s: THE CUMULATIVE CASE - frame alone %.0f%%, frame+readout %.0f%%. Neither "
                            "part alone converts it." % (short, 100 * fit, 100 * fit_ro))
        elif enum is not None and enum < 0.5:
            diagnosis[short] = "the frame does not take at all - it ignores the named method"
        else:
            diagnosis[short] = "fails with every free lever measured here"

    any_fail = any(v["bare"] is not None and v["bare"] < 1.0 for v in verdicts.values())
    convert = [k.rsplit("/", 1)[-1] for k, v in verdicts.items()
               if None not in (v["bare"], v["fitted"]) and v["fitted"] - v["bare"] >= 0.25]
    cumulative = [k.rsplit("/", 1)[-1] for k, v in verdicts.items()
                  if None not in (v["fitted"], v["fitted_plus_readout"])
                  and v["fitted_plus_readout"] - v["fitted"] >= 0.25]
    # THE LADDER'S FIRST PICK IS THE ROD THE GAME ACTUALLY REACHES. A rung that works on the third rod down
    # is not a rung the default mission can show.
    first = "%s/%s" % RODS[0]
    first_ok = verdicts.get(first, {})
    first_works = any((first_ok.get(k) or 0) >= 0.9 for k in ("fitted", "fitted_plus_readout"))

    if not any_fail:
        verdict = ("NO FAILURE AVAILABLE ON THE HEARTH at the game's temperature. Neither THE FRAME nor THE "
                   "READOUT has anything to rescue, and an L2 mission cannot be built honestly here.")
    elif cumulative:
        verdict = ("THE L2 RUNG IS BUILDABLE AND THE CUMULATIVE CLAIM HAS A RECEIPT ON THE GAME'S OWN FUEL. "
                   "On %s the frame produces correct work and the rod misreports it, so THE FRAME and THE "
                   "READOUT are JOINTLY necessary and neither alone converts the failure - which is exactly "
                   "'everything above it, plus one part'. Needed: wordcount as t-06, a fitted per-task frame "
                   "in SCAFFOLDS, and a readout part. %s"
                   % (", ".join(cumulative),
                      ("The ladder's first pick (%s) also works, so the default mission can show it."
                       % RODS[0][1]) if first_works else
                      ("WARNING: the ladder's FIRST pick (%s) is not one of them, so the mission must pin "
                       "a rod or the player sees a lever that does nothing." % RODS[0][1])))
    elif convert:
        verdict = ("THE L2 RUNG IS BUILDABLE on %s: wordcount as t-06 plus a fitted per-task frame in "
                   "SCAFFOLDS. %s" % (", ".join(convert),
                                      "" if first_works else
                                      "WARNING: the ladder's FIRST pick (%s) is not among them."
                                      % RODS[0][1]))
    else:
        verdict = ("THE HEARTH FAILS, BUT NO FREE LEVER RESCUES IT on this fuel. x02's result does not "
                   "transfer to ollama - law IV again, the same composition on different fuel is a "
                   "different organism. An L2 mission here would show a frame that does nothing.")

    # THE DETERMINISM RECEIPT, reported as a first-class result rather than left in the trials.
    det = {}
    for t in TEMPS:
        cells_t = [r for r in rows if r["temperature"] == t and r["scored"]]
        det["t=%.1f" % t] = {"cells": len(cells_t),
                             "collapsed_to_one_reply": sum(1 for r in cells_t
                                                           if r["distinct_replies"] <= 1),
                             "median_effective_n": (sorted(r["effective_n"] for r in cells_t)
                                                    [len(cells_t) // 2] if cells_t else None)}

    rep = {"id": "x09_hearth_failure", "design_version": 2,
           "question": "does the bench bank contain a failure the free rungs could rescue, on the hearth "
                       "and at the temperature the game actually fires?",
           "measures": ["C-04", "C-19", "C-23", "C-87"], "n": N, "temperatures": list(TEMPS),
           "game_temperature": GAME_TEMP,
           "decides": "whether the skipped L2 rung can be built honestly, on which rod, and what it costs",
           "rows": rows, "per_rod": verdicts, "diagnosis": diagnosis, "determinism": det,
           "findings": findings, "verdict": verdict,
           "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}

    d = os.path.join(grid.STATE, "lab", "runs", "x09_hearth_failure")
    os.makedirs(d, exist_ok=True)
    rid = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    p = os.path.join(d, "%s.json" % rid)
    if os.path.exists(p):
        raise ValueError("refusing to overwrite evidence at %s" % p)
    rep["run_id"] = rid
    grid.atomic_save_json(p, rep)
    ip = os.path.join(grid.STATE, "lab", "INDEX.json")
    idx = grid.load_json(ip, {"runs": []})
    idx.setdefault("runs", []).append({"experiment": rep["id"], "run_id": rid, "at": rep["at"],
                                       "check_id": "per-cell", "n": N, "design_version": 2,
                                       "rods": ["%s/%s" % r for r in RODS],
                                       "measures": rep["measures"], "verdicts": [],
                                       "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


if __name__ == "__main__":
    r = run()
    print()
    print("DETERMINISM (the honest n):")
    for k, v in r["determinism"].items():
        print("  %s  %d of %d cells collapsed to ONE distinct reply   median effective n = %s"
              % (k, v["collapsed_to_one_reply"], v["cells"], v["median_effective_n"]))
    print()
    print("DIAGNOSIS PER ROD (read at the game's temperature %.1f):" % r["game_temperature"])
    for k, v in r["diagnosis"].items():
        print("  %-16s %s" % (k, v))
    print()
    for f in r["findings"]:
        print("  -", f)
    print()
    print("VERDICT:", r["verdict"])
    print("EVIDENCE  state/lab/runs/x09_hearth_failure/%s.json" % r["run_id"])
