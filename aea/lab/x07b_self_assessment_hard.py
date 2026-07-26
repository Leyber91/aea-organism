"""x07b - SELF-ASSESSMENT WHERE FAILURE IS ABUNDANT, and whether it is RELATIVE rather than absent.

x07 asked five rods "will you get this right?" across the five-task bank and got ZERO of twelve honest
predictions on the cells they failed. My own guard refused a grid-level verdict: twelve parseable failure
cells is below the threshold of twenty, because the bank is too easy for these rods. So the direction was
unambiguous and the claim was underpowered, and the diary recorded the re-run as owed.

THE FIX FOR POWER. The 50-step chain fails constantly - nemotron-9b 9/16, groq-70b 0/8, nemotron-550b 1/7
in one breath (x06). Failure cells will be plentiful instead of scarce.

THE ADDITION THAT COULD OVERTURN x07'S READING, and it is the reason this is not just a re-run. x07 asked
one absolute question and got a flat no. But self-knowledge might exist as a COMPARATIVE judgement while
being absent as an absolute one: a rod that cannot say "I will fail this" might still say YES at ten steps
and NO at fifty. If it can, ceiling-detect is partly free after all - not as an oracle, but as a difficulty
ranking - and C-26's L4 placement needs qualifying rather than confirming. So every rod is asked at BOTH
lengths, and the discriminating number is the DIFFERENCE:

  discrimination = P(says YES | 10 steps) - P(says YES | 50 steps)

If that is near zero while its real accuracy drops between the two, the rod is not tracking difficulty at
all and x07's finding holds at power. If it is clearly positive, a rod knows the chain got harder, and the
placement argument changes shape.

THE THIRD MEASUREMENT, which is a floor rather than a score. x07 turned up a candidate item outside the 86:
asked whether it would get a question right, llama-3.2-3b replied `7` - it attempted the arithmetic instead
of the question about itself. The ABILITY TO REPRESENT A QUESTION ABOUT ONESELF is a capability, and one rod
did not have it. Here it is counted explicitly as `answered_task_instead` rather than pooled into
"unparseable", because a rod that cannot host the meta-level is a different fact from a rod that hedged.

Run: python -m aea.lab.x07b_self_assessment_hard
"""
from __future__ import annotations

import concurrent.futures as _futures
import os
import re
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.lab.x06_long_chain import START, chain, truth
from aea.lab.x07_self_assessment import _yesno
from aea.mind import fuel

N = 12
TEMP = 0.0
LENGTHS = (10, 50)

RODS = [
    ("nvidia", "meta/llama-3.2-3b-instruct"),               # the rod that could not host the meta-level
    ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2"),        # 9/16 in one breath at 50 - the drifter
    ("nvidia", "openai/gpt-oss-20b"),                       # 8/8 at 200 - the control that SHOULD say yes
    ("groq",   "llama-3.3-70b-versatile"),                  # 0/8 at 50, and confidently yes in x07
    ("nvidia", "nvidia/nemotron-3-ultra-550b-a55b"),        # 1/7 at 50 - big fuel, still drifts
]


def _task_text(n: int) -> str:
    return ("Start with the value %d and apply these %d operations in order:\n%s\n\n"
            "Reply with ONLY the final number." % (START, n, "\n".join(
                "%d. %s" % (i + 1, op) for i, op in enumerate(chain(n)))))


def _answered_task_instead(raw: str, yn) -> bool:
    """The x07 signature: asked about itself, the rod answers the arithmetic.

    Counted separately from a hedge because it is a FLOOR, not an error rate - the meta-level does not
    exist for that rod, which is a capability claim and not a calibration one.
    """
    if yn is not None or not raw:
        return False
    t = raw.strip()
    return bool(re.search(r"-?\d", t)) and not re.search(r"\b(YES|NO)\b", t, re.I)


def _trial(rod, n, i):
    out = {"trial": i, "length": n}
    task = _task_text(n)

    # 1 PROSPECTIVE. The length is stated in the prompt, so a rod that tracks difficulty has what it needs.
    r1 = H.call_gated(rod[0], rod[1], [{"role": "user", "content":
                      "You will be asked to do the task below in a single reply. Before attempting it, "
                      "judge whether YOU will get it exactly right. Reply with ONLY the single word YES "
                      "or NO.\n\nTASK:\n" + task}], max_tokens=500, temperature=TEMP)
    out["prospective_raw"] = (r1.get("text") or "") if r1.get("ok") else None
    out["prospective"] = _yesno(out["prospective_raw"])
    out["answered_task_instead"] = _answered_task_instead(out["prospective_raw"], out["prospective"])

    # 2 THE ATTEMPT. One breath, the whole chain, ground truth computed locally.
    r2 = H.call_gated(rod[0], rod[1], [{"role": "user", "content": task}],
                      max_tokens=1600, temperature=TEMP)
    if not r2.get("ok"):
        out["actual"], out["error"] = None, r2.get("error")
        return out
    answer = r2.get("text") or ""
    nums = re.findall(r"-?\d+", answer.replace(",", ""))
    out["given"] = int(nums[-1]) if nums else None
    out["actual"] = (out["given"] == truth(n))
    out["answer_raw"] = answer[-600:]

    # 3 RETROSPECTIVE. Its own answer in front of it.
    r3 = H.call_gated(rod[0], rod[1], [{"role": "user", "content":
                      "TASK:\n" + task + "\n\nAN ANSWER WAS GIVEN: %s\n\nIs that answer correct? Reply "
                      "with ONLY the single word YES or NO." % out["given"]}],
                      max_tokens=500, temperature=TEMP)
    out["retrospective_raw"] = (r3.get("text") or "") if r3.get("ok") else None
    out["retrospective"] = _yesno(out["retrospective_raw"])
    out["tok_in"] = sum((r.get("prompt_tokens") or 0) for r in (r1, r2, r3))
    out["tok_out"] = sum((r.get("tokens") or 0) for r in (r1, r2, r3))
    return out


def cell(rod, n):
    pool = _futures.ThreadPoolExecutor(max_workers=8)
    try:
        trials = [f.result() for f in [pool.submit(_trial, rod, n, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    scored = [t for t in trials if t.get("actual") is not None]
    failed = [t for t in scored if not t["actual"]]

    def agree(key, subset):
        u = [t for t in subset if t.get(key) is not None]
        return sum(1 for t in u if t[key] == t["actual"]), len(u)

    pro_all, pro_n = agree("prospective", scored)
    ret_all, ret_n = agree("retrospective", scored)
    pro_f, pro_fn = agree("prospective", failed)
    ret_f, ret_fn = agree("retrospective", failed)
    yes = [t for t in scored if t.get("prospective") is True]
    row = {"rod": "%s/%s" % rod, "length": n, "expected": truth(n),
           "actual_pass": sum(1 for t in scored if t["actual"]), "scored": len(scored),
           "said_yes": len(yes), "said_yes_n": len([t for t in scored if t.get("prospective") is not None]),
           "prospective_agree": pro_all, "prospective_n": pro_n,
           "retrospective_agree": ret_all, "retrospective_n": ret_n,
           "honest_on_failure_pro": pro_f, "pro_fail_n": pro_fn,
           "honest_on_failure_ret": ret_f, "ret_fail_n": ret_fn,
           "failures": len(failed),
           "answered_task_instead": sum(1 for t in trials if t.get("answered_task_instead")),
           "unparseable_meta": sum(1 for t in trials if t.get("prospective") is None),
           "tok_in": sum(t.get("tok_in", 0) for t in trials),
           "fuel": fuel.stamp(rod[0], rod[1], n=N, temperature=TEMP,
                              attempts=len(trials), failures=len(trials) - len(scored)),
           "trials": trials}
    print("  %-42s len=%-3d actual %2d/%-2d  said-YES %2d/%-2d  honest-on-fail %2d/%-2d  "
          "task-instead %d" % (rod[1][:41], n, row["actual_pass"], row["scored"], row["said_yes"],
                               row["said_yes_n"], row["honest_on_failure_pro"], row["pro_fail_n"],
                               row["answered_task_instead"]), flush=True)
    return row


def run():
    print("x07b - %d rods x lengths %s x n=%d x 3 probes (truth: %s)"
          % (len(RODS), LENGTHS, N, {n: truth(n) for n in LENGTHS}))
    rows = [cell(rod, n) for rod in RODS for n in LENGTHS]

    # DISCRIMINATION, per rod: does it say YES less often as the chain gets longer, and does its real
    # accuracy actually drop? Both halves are needed - a rod that says NO more often on a task it also
    # passes equally well is not tracking difficulty, it is just gloomier about long prompts.
    disc = {}
    for rod in RODS:
        k = "%s/%s" % rod
        a = next((r for r in rows if r["rod"] == k and r["length"] == LENGTHS[0]), None)
        b = next((r for r in rows if r["rod"] == k and r["length"] == LENGTHS[-1]), None)
        if not a or not b or not a["said_yes_n"] or not b["said_yes_n"] or not a["scored"] or not b["scored"]:
            continue
        disc[k] = {"yes_short": round(a["said_yes"] / a["said_yes_n"], 3),
                   "yes_long": round(b["said_yes"] / b["said_yes_n"], 3),
                   "acc_short": round(a["actual_pass"] / a["scored"], 3),
                   "acc_long": round(b["actual_pass"] / b["scored"], 3)}
        disc[k]["discrimination"] = round(disc[k]["yes_short"] - disc[k]["yes_long"], 3)
        disc[k]["real_drop"] = round(disc[k]["acc_short"] - disc[k]["acc_long"], 3)

    tot_f = sum(r["pro_fail_n"] for r in rows)
    hit_f = sum(r["honest_on_failure_pro"] for r in rows)
    tot_r = sum(r["ret_fail_n"] for r in rows)
    hit_r = sum(r["honest_on_failure_ret"] for r in rows)

    # BOTH ARMS, and the first run of this file is why. `honest_on_failure` counts only the cells a rod
    # FAILED, so a rod that says NO to everything scores 1.00 by construction with no predictive skill.
    # Run 20260726T064600Z printed "21 of 21, x07 IS OVERTURNED" on exactly that artifact:
    # llama-3.2-3b said NO to all 24 of its cells, passed 12 and failed 12, and every failure was
    # counted as honesty. A one-sided metric cannot see a false alarm. This is the fourth instrument
    # defect in the project and the first one in a VERDICT rather than in a detector or a cap.
    TP = TN = FP = FN = 0
    per_rod = {}
    for rod in RODS:
        k = "%s/%s" % rod
        sel = [t for r in rows if r["rod"] == k for t in r["trials"]
               if t.get("actual") is not None and t.get("prospective") is not None]
        if not sel:
            per_rod[k] = {"n": 0, "note": "no parseable predictions: cannot host the meta-question"}
            continue
        p = [t for t in sel if t["actual"]]
        f = [t for t in sel if not t["actual"]]
        tp = sum(1 for t in p if t["prospective"])
        fp = sum(1 for t in f if t["prospective"])
        TP, FN, FP, TN = TP + tp, FN + (len(p) - tp), FP + fp, TN + (len(f) - fp)
        per_rod[k] = {"n": len(sel), "passed": len(p),
                      "yes_given_pass": [tp, len(p)], "yes_given_fail": [fp, len(f)],
                      "accuracy": round((tp + (len(f) - fp)) / len(sel), 3),
                      "discrimination": (round(tp / len(p) - fp / len(f), 3) if p and f else None)}
    n_pred = TP + TN + FP + FN
    acc = (TP + TN) / n_pred if n_pred else None
    base = max(TP + FN, TN + FP) / n_pred if n_pred else None   # always-say-the-majority
    p_yes_pass = TP / (TP + FN) if (TP + FN) else None
    p_yes_fail = FP / (FP + TN) if (FP + TN) else None

    verdict, qualifier = None, None
    if tot_f < 20:
        verdict = ("STILL UNDERPOWERED - only %d parseable failure cells. The chain did not fail enough "
                   "either, and the threshold of 20 stands." % tot_f)
    elif acc is None:
        verdict = "NO PARSEABLE PREDICTIONS ANYWHERE. Nothing to score."
    elif acc - base < 0.10:
        verdict = ("NO SKILL AT POWER: the predictor scores %.2f against %.2f for always saying the "
                   "majority answer, inside the band. The one-sided 'honest on failure' figure is %d of "
                   "%d and it is an artifact of rods that decline everything." % (acc, base, hit_f, tot_f))
    else:
        verdict = ("SKILL AT POWER: the predictor scores %.2f against %.2f for always saying the "
                   "majority answer." % (acc, base))
    if p_yes_fail is not None and p_yes_pass is not None:
        verdict += (" ASYMMETRY: P(YES|will fail) = %.2f and P(YES|will pass) = %.2f, so a YES is worth "
                    "%s and a NO is worth %s."
                    % (p_yes_fail, p_yes_pass,
                       "trusting" if p_yes_fail <= 0.1 else "little",
                       "little" if p_yes_pass >= 0.4 else "trusting"))
    skilled = [k for k, v in per_rod.items() if v.get("discrimination") is not None
               and v["discrimination"] >= 0.5]
    blind = [k for k, v in per_rod.items() if v.get("discrimination") == 0.0]
    if skilled or blind:
        verdict += (" IT IS A FUEL PHENOTYPE: %d rod(s) discriminate (%s) and %d predict identically "
                    "whatever will happen (%s). Self-knowledge is a property of the fuel, not of the "
                    "architecture, which is Law IV again."
                    % (len(skilled), ", ".join(k.rsplit("/", 1)[-1] for k in skilled) or "none",
                       len(blind), ", ".join(k.rsplit("/", 1)[-1] for k in blind) or "none"))

    # THE QUALIFIER IS SEPARATE FROM THE VERDICT, because it can hold even when the verdict is a flat no:
    # absolute self-knowledge and comparative self-knowledge are different capabilities.
    good = [k for k, v in disc.items() if v["discrimination"] >= 0.3 and v["real_drop"] >= 0.2]
    flat = [k for k, v in disc.items() if abs(v["discrimination"]) < 0.15 and v["real_drop"] >= 0.2]
    if good:
        qualifier = ("COMPARATIVE self-knowledge is PRESENT in %d of %d rods (%s): they said YES less "
                     "often as the chain lengthened, on a task where their real accuracy also dropped. "
                     "A rod cannot say whether it will fail, but it can tell that this is harder than "
                     "that - so ceiling-detect is partly free as a RANKING, and C-26's L4 placement "
                     "covers the oracle, not the ranking."
                     % (len(good), len(disc), ", ".join(k.rsplit("/", 1)[-1] for k in good)))
    elif flat:
        qualifier = ("COMPARATIVE self-knowledge is ABSENT too: %d rods lost real accuracy between %d and "
                     "%d steps and did not change their prediction (%s). Not even a difficulty ranking is "
                     "available from the inside, which strengthens L4 rather than qualifying it."
                     % (len(flat), LENGTHS[0], LENGTHS[-1], ", ".join(k.rsplit("/", 1)[-1] for k in flat)))

    rep = {"id": "x07b_self_assessment_hard",
           "question": "at power, can a rod predict its own failure - and can it at least rank difficulty?",
           "measures": ["C-26", "C-17", "C-15"], "n": N, "temperature": TEMP, "lengths": list(LENGTHS),
           "decides": "whether x07's 0-of-12 holds at power, and whether comparative self-knowledge "
                      "qualifies the L4 placement of C-26",
           "rows": rows, "discrimination": disc, "per_rod_calibration": per_rod,
           "summary": {"prospective_honest_on_failure": [hit_f, tot_f],
                       "retrospective_honest_on_failure": [hit_r, tot_r],
                       "confusion": {"TP": TP, "TN": TN, "FP": FP, "FN": FN},
                       "accuracy": acc, "majority_baseline": base,
                       "p_yes_given_pass": p_yes_pass, "p_yes_given_fail": p_yes_fail,
                       "answered_task_instead": sum(r["answered_task_instead"] for r in rows),
                       "verdict": verdict, "qualifier": qualifier},
           "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}

    d = os.path.join(grid.STATE, "lab", "runs", "x07b_self_assessment_hard")
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
                                       "check_id": "exact-final-value", "n": N,
                                       "rods": ["%s/%s" % r for r in RODS],
                                       "measures": rep["measures"], "verdicts": [],
                                       "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


if __name__ == "__main__":
    r = run()
    s = r["summary"]
    print()
    print("PROSPECTIVE   honest on the cells it failed: %d of %d" % tuple(s["prospective_honest_on_failure"]))
    print("RETROSPECTIVE honest on the cells it failed: %d of %d" % tuple(s["retrospective_honest_on_failure"]))
    print("ANSWERED THE TASK INSTEAD OF THE META-QUESTION: %d" % s["answered_task_instead"])
    print()
    for k, v in r["discrimination"].items():
        print("  %-42s yes %.2f->%.2f  real %.2f->%.2f  disc %+.2f"
              % (k.rsplit("/", 1)[-1], v["yes_short"], v["yes_long"], v["acc_short"], v["acc_long"],
                 v["discrimination"]))
    print()
    print("VERDICT:  ", s["verdict"])
    print("QUALIFIER:", s["qualifier"])
    print("EVIDENCE  state/lab/runs/x07b_self_assessment_hard/%s.json" % r["run_id"])
