"""x11 - DOES A COUNCIL REACH ABOVE ITS FUEL? Chapter II's third claim, the one never measured.

THE STATE OF THE CHAPTER. Claim 1 is settled in its narrow form (carried state repairs a rod that drifts,
11/11 vs 9/16, p=0.0216) and x10 added support from a second direction (the ceiling is not ordered by size -
a 70b fails what a 9b passes). Claim 2 is substantially answered by x08 and x08b. Claim 3 has ONE OBSERVATION
AND ZERO MEASUREMENT: three rods asked whether a system storing state in 35 files is one self or many gave
three different answers. Disagreement was observed; benefit never was.

THE COMPARISON THAT CAN FAIL, AND IT IS NOT THE OBVIOUS ONE. A council will beat the AVERAGE of its members
almost trivially - averaging away bad draws is what voting does. That result would be worthless here, because
a council that beats its average but not its BEST MEMBER has not reached above its fuel; it has solved a
rod-selection problem that ceiling-detect (C-26, L4, one cheap call against a calibration table) already
solves for a fraction of the cost. So the discriminating comparison is:

    DOES THE COUNCIL BEAT ITS BEST MEMBER, AND IS IT WORTH N TIMES THE CALLS?

Both halves are reported, always. A council that ties its best member at 5x the cost is a NEGATIVE result and
this file says so.

FOUR ARMS on one task with real headroom - the 50-step chain in one breath, where x06 measured intermediate
failure rates (9b 9/16, 550b 1/7, groq-70b 0/8) rather than the saturation that has now voided or flattered
four comparisons in this project:

  A  SOLO              each rod alone, one call            - the baseline, and the source of "best member"
  B  SELF-CONSISTENCY  ONE rod, K samples, majority vote   - a council of one rod with itself
  C  CROSS-ROD COUNCIL K different rods, majority vote     - a council across fuel
  D  PEER DEBATE       K rods see each other's answers, revise once, then vote   - C-77, the census item

WHY ARM B NEEDS A TEMPERATURE AND x10 SUPPLIED IT. Self-consistency voting requires the rod to actually vary
between samples. x10 measured the effective-n curve and found the median effective n is 1-2 at the product's
0.2 and that plants collapse to ONE distinct reply in most cells at 0.0. **Majority voting over identical
samples is not a council, it is one answer counted K times.** So B runs at a temperature where variation
exists, and the distinct-sample count is recorded per vote so a collapsed council is visible rather than
reported as a 5-voice agreement.

Ground truth is computed locally, for free. Every vote records its full ballot, so a tie or a collapse can be
re-read from the evidence rather than inferred from a score.

Run: python -m aea.lab.x11_the_council
"""
from __future__ import annotations

import collections
import concurrent.futures as _futures
import os
import re
import sys
import time

from aea.kernel import grid
from aea.lab import harness as H
from aea.lab.x06_long_chain import START, chain, truth
from aea.mind import fuel

LENGTH = 50
N = 8                 # votes per arm
K = 5                 # council size
SOLO_TEMP = 0.2       # the product's own
VOTE_TEMP = 0.7       # arm B needs variation to vote over at all - x10's determinism curve

# The council. Deliberately MIXED in size and plant: if a council only works among equals, that is a
# different architecture than if a 1b can contribute to a verdict alongside a 550b.
COUNCIL = [
    ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2"),
    ("nvidia", "openai/gpt-oss-20b"),
    ("nvidia", "mistralai/mistral-small-4-119b-2603"),
    ("groq",   "llama-3.3-70b-versatile"),
    ("nvidia", "nvidia/nemotron-3-super-120b-a12b"),
]
DEBATERS = COUNCIL[:3]

# THE WEAK POOL - candidates for the sharp test, drawn from rods x06 measured as failing the 50-step chain.
# Membership is NOT taken on trust: arm E measures every candidate's solo rate IN THE SAME RUN and keeps only
# the ones that actually fail, because x10 showed sampling-based cells do not reproduce across runs.
WEAK_POOL = [
    ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2"),      # 1/8 measured, 9/16 in x06 - the drifter
    ("nvidia", "meta/llama-3.2-3b-instruct"),             # 0/8 measured
    ("nvidia", "meta/llama-3.2-1b-instruct"),             # 0/8 measured, distinct=1
]
# DROPPED FROM THE POOL, and the reason is about the rig rather than the rods.
#   groq/llama-3.3-70b        returned 1 of 8 calls - a RATE LIMIT from x10 and x11 hammering the plant,
#                             not a defect. Each blocked call costs 5 retries with exponential backoff.
#   nemotron-3-ultra-550b     answers in ~40s, so eight sequential votes alone exceed the harness cap.
# The first attempt at this arm was KILLED AT TEN MINUTES because the run was launched with a timeout
# above the tool's own maximum, losing four completed arms that had never been written to disk. Keeping
# the pool to fast rods is what makes the arm finish inside the cap and reach `atomic_save_json`.


def task_text(n: int = LENGTH) -> str:
    return ("Start with the value %d and apply these %d operations in order:\n%s\n\n"
            "Reply with ONLY the final number." % (START, n, "\n".join(
                "%d. %s" % (i + 1, op) for i, op in enumerate(chain(n)))))


def _num(text: str):
    nums = re.findall(r"-?\d+", (text or "").replace(",", ""))
    return int(nums[-1]) if nums else None


def ask(rod, prompt, temp, max_tokens=1600):
    r = H.call_gated(rod[0], rod[1], [{"role": "user", "content": prompt}],
                     max_tokens=max_tokens, temperature=temp)
    if not r.get("ok"):
        return None, r
    return _num(r.get("text") or ""), r


def majority(ballot: list):
    """The winner and its margin. A TIE RETURNS None - never break a tie toward the first voter, which
    would silently make the council a lookup of whoever happens to be listed first."""
    votes = [b for b in ballot if b is not None]
    if not votes:
        return None, 0, 0
    c = collections.Counter(votes).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        return None, c[0][1], len(set(votes))
    return c[0][0], c[0][1], len(set(votes))


def arm_solo(rod, exp):
    def one(i):
        got, r = ask(rod, task_text(), SOLO_TEMP)
        return {"got": got, "ok": got is not None, "hit": got == exp,
                "tok_in": r.get("prompt_tokens") or 0, "tok_out": r.get("tokens") or 0}
    pool = _futures.ThreadPoolExecutor(max_workers=4)
    try:
        trials = [f.result() for f in [pool.submit(one, i) for i in range(N)]]
    finally:
        pool.shutdown(wait=True)
    ok = [t for t in trials if t["ok"]]
    return {"arm": "A_solo", "rod": "%s/%s" % rod, "hits": sum(1 for t in ok if t["hit"]),
            "scored": len(ok), "calls": len(trials), "distinct": len({t["got"] for t in ok}),
            "tok_in": sum(t["tok_in"] for t in trials), "trials": trials}


def arm_self_consistency(rod, exp):
    """One rod, K samples, majority. A council of one rod with itself - and the cheapest kind to build."""
    def one_vote(i):
        pool = _futures.ThreadPoolExecutor(max_workers=K)
        try:
            res = [f.result() for f in [pool.submit(ask, rod, task_text(), VOTE_TEMP) for _ in range(K)]]
        finally:
            pool.shutdown(wait=True)
        ballot = [g for g, _ in res]
        win, margin, spread = majority(ballot)
        return {"ballot": ballot, "winner": win, "margin": margin, "distinct_in_ballot": spread,
                "hit": win == exp, "collapsed": spread <= 1,
                "tok_in": sum((r.get("prompt_tokens") or 0) for _, r in res)}
    votes = [one_vote(i) for i in range(N)]
    return {"arm": "B_self_consistency", "rod": "%s/%s" % rod,
            "hits": sum(1 for v in votes if v["hit"]), "scored": N, "calls": N * K,
            "collapsed_votes": sum(1 for v in votes if v["collapsed"]),
            "tok_in": sum(v["tok_in"] for v in votes), "votes": votes}


def arm_cross_rod(exp):
    """K DIFFERENT rods, one sample each, majority. The council across fuel."""
    def one_vote(i):
        pool = _futures.ThreadPoolExecutor(max_workers=K)
        try:
            res = [f.result() for f in
                   [pool.submit(ask, rod, task_text(), SOLO_TEMP) for rod in COUNCIL]]
        finally:
            pool.shutdown(wait=True)
        ballot = [g for g, _ in res]
        win, margin, spread = majority(ballot)
        return {"ballot": ballot, "by_rod": {"%s/%s" % r: b for r, b in zip(COUNCIL, ballot)},
                "winner": win, "margin": margin, "distinct_in_ballot": spread, "hit": win == exp,
                "tok_in": sum((r.get("prompt_tokens") or 0) for _, r in res)}
    votes = [one_vote(i) for i in range(N)]
    return {"arm": "C_cross_rod", "rod": "council of %d" % K,
            "hits": sum(1 for v in votes if v["hit"]), "scored": N, "calls": N * K,
            "tok_in": sum(v["tok_in"] for v in votes), "votes": votes}


def arm_debate(exp):
    """C-77 peer_debate: each rod sees the others' answers and may revise, THEN they vote.

    The revision prompt shows the peers' numbers without saying which is right - nothing in it asserts a
    correct answer, so a rod that changes its mind is changing it on the disagreement alone.
    """
    def one_vote(i):
        pool = _futures.ThreadPoolExecutor(max_workers=len(DEBATERS))
        try:
            first = [f.result() for f in
                     [pool.submit(ask, rod, task_text(), SOLO_TEMP) for rod in DEBATERS]]
        finally:
            pool.shutdown(wait=True)
        opening = [g for g, _ in first]
        peers = ", ".join(str(g) for g in opening)
        rev_prompt = (task_text() + "\n\nIndependent attempts at this task returned: %s\n"
                      "They do not all agree. Work the chain again and reply with ONLY your final "
                      "number." % peers)
        pool = _futures.ThreadPoolExecutor(max_workers=len(DEBATERS))
        try:
            second = [f.result() for f in
                      [pool.submit(ask, rod, rev_prompt, SOLO_TEMP) for rod in DEBATERS]]
        finally:
            pool.shutdown(wait=True)
        revised = [g for g, _ in second]
        win, margin, spread = majority(revised)
        w0, _, _ = majority(opening)
        return {"opening": opening, "revised": revised, "winner": win, "margin": margin,
                "distinct_in_ballot": spread, "hit": win == exp, "hit_before_debate": w0 == exp,
                "changed_minds": sum(1 for a, b in zip(opening, revised) if a != b),
                "tok_in": sum((r.get("prompt_tokens") or 0) for _, r in first + second)}
    votes = [one_vote(i) for i in range(N)]
    return {"arm": "D_peer_debate", "rod": "debate of %d" % len(DEBATERS),
            "hits": sum(1 for v in votes if v["hit"]), "scored": N,
            "hits_before_debate": sum(1 for v in votes if v["hit_before_debate"]),
            "changed_minds": sum(v["changed_minds"] for v in votes),
            "calls": N * len(DEBATERS) * 2, "tok_in": sum(v["tok_in"] for v in votes), "votes": votes}


def arm_weak_council(members, exp):
    """THE SHARP VERSION OF CLAIM 3: a council in which EVERY MEMBER FAILS SOLO.

    The first run of this file exposed why it is needed. `gpt-oss-20b` scores 8/8 on the 50-step chain, and a
    council containing a member that already saturates CANNOT demonstrate reaching above its fuel - it can
    only tie, and the tie would be reported as a negative result when it is really the ceiling effect for the
    fifth time in this project.

    So the members here are chosen from THIS RUN's solo rates (never a previous run's - x10 showed
    sampling-based cells do not reproduce across runs), and every one of them fails. The question becomes the
    one worth asking: **when nobody in the room can do it, does the room still find the answer?**

    THE DECIDING DETAIL IS ERROR CORRELATION, which the ballot records. If wrong answers are UNCORRELATED the
    majority can still land on truth, because the one right answer is the only thing they can agree on. If
    the rods drift the same way - and arithmetic drift has structure - the council will be confidently wrong
    TOGETHER, and a majority vote will launder that into a verdict. `agreed_on_wrong` counts exactly that.
    """
    def one_vote(i):
        pool = _futures.ThreadPoolExecutor(max_workers=len(members))
        try:
            res = [f.result() for f in
                   [pool.submit(ask, rod, task_text(), SOLO_TEMP) for rod in members]]
        finally:
            pool.shutdown(wait=True)
        ballot = [g for g, _ in res]
        win, margin, spread = majority(ballot)
        return {"ballot": ballot, "by_rod": {"%s/%s" % r: b for r, b in zip(members, ballot)},
                "winner": win, "margin": margin, "distinct_in_ballot": spread,
                "hit": win == exp, "agreed_on_wrong": bool(win is not None and win != exp and margin >= 2),
                "any_member_right": any(b == exp for b in ballot),
                "tok_in": sum((r.get("prompt_tokens") or 0) for _, r in res)}
    votes = [one_vote(i) for i in range(N)]
    return {"arm": "E_weak_council", "rod": "weak council of %d" % len(members),
            "members": ["%s/%s" % r for r in members],
            "hits": sum(1 for v in votes if v["hit"]), "scored": N,
            "agreed_on_wrong": sum(1 for v in votes if v["agreed_on_wrong"]),
            "truth_was_present": sum(1 for v in votes if v["any_member_right"]),
            "calls": N * len(members), "tok_in": sum(v["tok_in"] for v in votes), "votes": votes}


def _save(rep: dict, rods: list) -> dict:
    """Write the evidence. Factored out so every arm subset reaches it, which the first run did not."""
    d = os.path.join(grid.STATE, "lab", "runs", "x11_the_council")
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
                                       "check_id": "exact-final-value", "n": rep.get("n"),
                                       "rods": rods, "measures": rep["measures"], "verdicts": [],
                                       "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


def run(weak_only: bool = False):
    exp = truth(LENGTH)
    print("x11 - the council. chain of %d, ground truth %d, n=%d votes, K=%d%s"
          % (LENGTH, exp, N, K, "   [WEAK ARM ONLY]" if weak_only else ""), flush=True)
    rows = []

    if weak_only:
        print("\n  E - qualifying the weak pool (solo, t=%.1f)" % SOLO_TEMP, flush=True)
        for rod in WEAK_POOL:
            r = arm_solo(rod, exp)
            rows.append(r)
            print("    %-46s %d/%-2d  distinct=%d" % (r["rod"][:45], r["hits"], r["scored"],
                                                      r["distinct"]), flush=True)
        weak = [r for r in WEAK_POOL
                if next(x for x in rows if x["rod"] == "%s/%s" % r)["scored"]
                and next(x for x in rows if x["rod"] == "%s/%s" % r)["hits"]
                / next(x for x in rows if x["rod"] == "%s/%s" % r)["scored"] < 0.5]
        print("    -> seated %d of %d, every one failing solo" % (len(weak), len(WEAK_POOL)), flush=True)
        if len(weak) < 3:
            print("    ABORT: a weak council needs at least 3 failing members.", flush=True)
            return None
        wr = arm_weak_council(weak, exp)
        rows.append(wr)
        print("    %-46s %d/%-2d  agreed-on-wrong=%d  truth-in-ballot=%d/%d"
              % (wr["rod"], wr["hits"], wr["scored"], wr["agreed_on_wrong"],
                 wr["truth_was_present"], wr["scored"]), flush=True)
        rate = wr["hits"] / wr["scored"]
        if rate >= 0.5:
            v = ("THE WEAK COUNCIL REACHES ABOVE ITS FUEL: %d of %d correct from %d members who ALL fail "
                 "solo. Their errors are uncorrelated enough that the one right answer is the only thing "
                 "they can agree on. Claim 3 HOLDS in its sharp form." % (wr["hits"], wr["scored"], len(weak)))
        elif wr["agreed_on_wrong"] >= wr["scored"] / 2:
            v = ("THE WEAK COUNCIL AGREES ON WRONG ANSWERS: %d of %d votes reached a MAJORITY that was "
                 "wrong. The rods drift together, so voting launders correlated error into a verdict. "
                 "Claim 3 FAILS, and a council is actively dangerous here because it manufactures "
                 "confidence." % (wr["agreed_on_wrong"], wr["scored"]))
        else:
            v = ("THE WEAK COUNCIL FINDS NOTHING: %d of %d, truth present in %d of %d ballots. No majority "
                 "forms, or it forms on noise. Claim 3 FAILS: a council of rods that cannot do the task is "
                 "a more expensive way to not do the task."
                 % (wr["hits"], wr["scored"], wr["truth_was_present"], wr["scored"]))
        rep = {"id": "x11_the_council", "arm_subset": "E_weak_council_only",
               "question": "when nobody in the room can do it, does the room still find the answer?",
               "measures": ["C-77", "C-03", "C-30"], "n": N, "length": LENGTH, "expected": exp,
               "solo_temperature": SOLO_TEMP, "decides": "chapter II claim 3, sharp form",
               "rows": rows, "verdict": [v],
               "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}
        _save(rep, [("%s/%s" % r) for r in WEAK_POOL])
        return rep

    print("\n  A - SOLO (each member alone, t=%.1f)" % SOLO_TEMP)
    for rod in COUNCIL:
        r = arm_solo(rod, exp)
        rows.append(r)
        print("    %-46s %d/%-2d  distinct=%d  calls=%d"
              % (r["rod"][:45], r["hits"], r["scored"], r["distinct"], r["calls"]), flush=True)

    best = max((r for r in rows if r["arm"] == "A_solo" and r["scored"]),
               key=lambda r: r["hits"] / r["scored"])
    best_rate = best["hits"] / best["scored"]
    print("    -> BEST MEMBER: %s at %.2f" % (best["rod"], best_rate))

    print("\n  B - SELF-CONSISTENCY (one rod, K=%d samples, t=%.1f)" % (K, VOTE_TEMP))
    for rod in COUNCIL[:3]:
        r = arm_self_consistency(rod, exp)
        rows.append(r)
        print("    %-46s %d/%-2d  collapsed votes=%d  calls=%d"
              % (r["rod"][:45], r["hits"], r["scored"], r["collapsed_votes"], r["calls"]), flush=True)

    print("\n  C - CROSS-ROD COUNCIL (K=%d rods, majority)" % K)
    r = arm_cross_rod(exp)
    rows.append(r)
    print("    %-46s %d/%-2d  calls=%d" % (r["rod"], r["hits"], r["scored"], r["calls"]), flush=True)
    cross = r

    print("\n  D - PEER DEBATE (%d rods, one revision round)" % len(DEBATERS))
    r = arm_debate(exp)
    rows.append(r)
    print("    %-46s %d/%-2d  (before debate %d/%-2d)  minds changed=%d  calls=%d"
          % (r["rod"], r["hits"], r["scored"], r["hits_before_debate"], r["scored"],
             r["changed_minds"], r["calls"]), flush=True)
    debate = r

    # E - THE SHARP TEST. Every candidate's solo rate is measured IN THIS RUN, and only actual failures are
    # seated. A council containing a member that already saturates cannot demonstrate reaching above anything.
    print("\n  E - qualifying the weak pool (solo, t=%.1f)" % SOLO_TEMP)
    solo_rate = {}
    for rod in WEAK_POOL:
        key = "%s/%s" % rod
        got = next((x for x in rows if x["arm"] == "A_solo" and x["rod"] == key), None)
        if got is None:
            got = arm_solo(rod, exp)
            rows.append(got)
            print("    %-46s %d/%-2d  distinct=%d" % (key[:45], got["hits"], got["scored"],
                                                      got["distinct"]), flush=True)
        solo_rate[key] = (got["hits"] / got["scored"]) if got["scored"] else None

    weak = [r for r in WEAK_POOL
            if solo_rate.get("%s/%s" % r) is not None and solo_rate["%s/%s" % r] < 0.5]
    print("    -> seated %d of %d (all with solo rate below 0.50): %s"
          % (len(weak), len(WEAK_POOL), ", ".join(r[1].rsplit("/", 1)[-1] for r in weak)))
    weak_row = None
    if len(weak) >= 3:
        print("\n  E - WEAK COUNCIL (%d members, EVERY ONE fails solo)" % len(weak))
        weak_row = arm_weak_council(weak, exp)
        rows.append(weak_row)
        print("    %-46s %d/%-2d  agreed-on-wrong=%d  truth-in-ballot=%d/%d  calls=%d"
              % (weak_row["rod"], weak_row["hits"], weak_row["scored"], weak_row["agreed_on_wrong"],
                 weak_row["truth_was_present"], weak_row["scored"], weak_row["calls"]), flush=True)
    else:
        print("\n  E - SKIPPED: only %d member(s) failed solo; a weak council needs at least 3." % len(weak))

    # THE VERDICT. Against the BEST MEMBER, never the average, and the cost is named beside it.
    cross_rate = cross["hits"] / cross["scored"]
    deb_rate = debate["hits"] / debate["scored"]
    sc = [x for x in rows if x["arm"] == "B_self_consistency"]
    best_sc = max(sc, key=lambda x: x["hits"] / x["scored"]) if sc else None
    sc_rate = (best_sc["hits"] / best_sc["scored"]) if best_sc else None

    lines = []
    if cross_rate > best_rate + 0.15:
        lines.append("CROSS-ROD COUNCIL REACHES ABOVE ITS BEST MEMBER: %.2f against %.2f, at %dx the calls. "
                     "Claim 3 holds - a council is not a rod-selection problem in disguise."
                     % (cross_rate, best_rate, K))
    elif cross_rate >= best_rate - 0.05:
        lines.append("CROSS-ROD COUNCIL TIES ITS BEST MEMBER: %.2f against %.2f, at %dx the calls. That is a "
                     "NEGATIVE result for claim 3 - ceiling-detect plus the best rod buys the same accuracy "
                     "for a fifth of the cost, and C-26 already sits at L4 to do exactly that."
                     % (cross_rate, best_rate, K))
    else:
        lines.append("CROSS-ROD COUNCIL IS WORSE THAN ITS BEST MEMBER: %.2f against %.2f. Voting DILUTED the "
                     "strong rod - the majority of a mixed council can be wrong together."
                     % (cross_rate, best_rate))
    if sc_rate is not None:
        lines.append("SELF-CONSISTENCY (one rod voting with itself) reached %.2f against that rod's solo "
                     "rate, at %dx the calls. Collapsed ballots: %d of %d - a ballot with one distinct "
                     "value is one answer counted %d times, not a council."
                     % (sc_rate, K, sum(x["collapsed_votes"] for x in sc), len(sc) * N, K))
    lines.append("PEER DEBATE moved %.2f -> %.2f with %d minds changed across %d votes. A debate that "
                 "changes no minds is a vote with extra steps; one that changes minds toward a WRONG "
                 "consensus is worse than no debate."
                 % (debate["hits_before_debate"] / debate["scored"], deb_rate,
                    debate["changed_minds"], debate["scored"]))

    # THE SHARP TEST'S OWN VERDICT. This is the one that actually decides claim 3, because a council
    # containing a saturated member cannot demonstrate reaching above anything.
    if weak_row:
        wr = weak_row["hits"] / weak_row["scored"]
        present = weak_row["truth_was_present"]
        if wr >= 0.5:
            lines.append("THE WEAK COUNCIL REACHES ABOVE ITS FUEL: %d of %d correct from %d members who ALL "
                         "fail solo. When nobody in the room can do it, the room still found it - their "
                         "errors are uncorrelated enough that the one right answer is the only thing they "
                         "can agree on. Claim 3 HOLDS in its sharp form."
                         % (weak_row["hits"], weak_row["scored"], len(weak)))
        elif weak_row["agreed_on_wrong"] >= weak_row["scored"] / 2:
            lines.append("THE WEAK COUNCIL AGREES ON WRONG ANSWERS: %d of %d votes reached a MAJORITY that "
                         "was wrong (truth was present in only %d of %d ballots). The rods drift together, "
                         "so voting launders correlated error into a verdict. Claim 3 FAILS, and worse - a "
                         "council is actively dangerous here, because it manufactures confidence."
                         % (weak_row["agreed_on_wrong"], weak_row["scored"], present, weak_row["scored"]))
        else:
            lines.append("THE WEAK COUNCIL FINDS NOTHING: %d of %d, truth present in %d of %d ballots. No "
                         "majority forms, or it forms on noise. Claim 3 FAILS - a council of rods that "
                         "cannot do the task is a more expensive way to not do the task."
                         % (weak_row["hits"], weak_row["scored"], present, weak_row["scored"]))

    rep = {"id": "x11_the_council",
           "question": "does a council reach above its best member, and is it worth N times the calls?",
           "measures": ["C-77", "C-03", "C-30"], "n": N, "council_size": K, "length": LENGTH,
           "expected": exp, "solo_temperature": SOLO_TEMP, "vote_temperature": VOTE_TEMP,
           "decides": "chapter II claim 3", "rows": rows,
           "best_member": {"rod": best["rod"], "rate": round(best_rate, 3)},
           "verdict": lines,
           "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())}

    d = os.path.join(grid.STATE, "lab", "runs", "x11_the_council")
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
                                       "rods": ["%s/%s" % r for r in COUNCIL],
                                       "measures": rep["measures"], "verdicts": [],
                                       "path": os.path.relpath(p, grid.STATE).replace("\\", "/")})
    grid.atomic_save_json(ip, idx)
    return rep


if __name__ == "__main__":
    r = run(weak_only="--weak-only" in sys.argv)
    if r is None:
        raise SystemExit(1)
    print()
    for line in r["verdict"]:
        print("  -", line)
    print()
    print("EVIDENCE  state/lab/runs/x11_the_council/%s.json" % r["run_id"])
