"""movecontrol.py - DOES THE WAKE JUDGE ITS MOVES, OR MATCH STRINGS AGAINST THEM?

    python -m aea.lab.movecontrol [--cheap]

THE MEASUREMENT THIS EXISTS FOR. The wake ends each tick with `MOVE: <name>` or `MOVE: NONE`,
choosing from six mechanical chores it can run on itself. Both answers are ordinary, and that is
precisely what makes the choice unmeasurable from the live log: a wake that weighs six conditions
and correctly declines writes the same four lines as a wake that has stopped reading them. Over
2026-07-30 this loop failed in BOTH directions within one hour - first bending every real priority
into an available chore (2/2 ticks), then, after the fix, answering NONE to a state where
consolidation was plainly owed (4/4 ticks). Neither failure was visible without a control.

WHY THE FIRST CONTROL DID NOT COUNT, and the reason this file exists rather than a fourth scratchpad
probe. The first version wrote its "owed" states in the same words as the move descriptions - "your
memory has grown to 40 undistilled notes" against a description reading "raw memory notes have piled
up undistilled". It scored 4/4 and proved nothing except that the model can match a phrase to a
near-copy of itself. The council's historian seat named it in one line: *the owed states and the
WHEN descriptions share an author and nearly the same phrasing; the one case it got right is the one
where the overlap is most obvious.* That is law B2 again - test the property, never a proxy - and it
had been quoted in this repo twice already before it was violated here.

SO THE CORPUS IS BUILT AGAINST ITSELF, in three groups the historian specified:

  PARAPHRASE   the condition is true, stated in vocabulary that shares no content word with the
               move's description. Matching fails here; judgement passes.
  DISTRACTOR   the condition's OWN WORDS are present and the move is NOT owed - it was already
               done, or just superseded. Matching fires; judgement declines. This is the group
               that carries the result, because it is the only one a string matcher cannot fake.
  QUIET        the condition is true and never named at all; it has to be read off the situation.

A run that passes the paraphrases and fails the distractors is a string matcher with good luck.
Both groups are reported separately for exactly that reason, and the headline verdict is gated on
the distractors.

The wake's real state file is never touched: STATE_PATH is redirected at the module and the
redirect is asserted before any tick runs.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time

from aea.kernel import decide, grid
from aea.loop import aea as wake

# (label, group, nudge, wanted_moves | empty set meaning NONE)
#
# Every PARAPHRASE nudge below is checked by `_leak()` against the move's own description: any
# shared content word is a defect in the CASE, not in the wake, and the run refuses to score until
# it is fixed. That check is what keeps this corpus honest as moves are added.
CASES = [
    # ---- PARAPHRASE: true condition, disjoint vocabulary --------------------------------------
    ("backlog, said differently", "paraphrase",
     "You are carrying sixty-three loose scraps from earlier cycles that nobody ever merged into a "
     "single record, and there is no way to look anything up among them.",
     {"consolidate"}),
    ("cannot name its own hands", "paraphrase",
     "You are about to plan your next few cycles and have no idea which operations exist for you "
     "to invoke. Nothing anywhere holds that inventory.",
     {"know_your_hands"}),
    ("he has been away", "paraphrase",
     "Luis has been offline for four days. Nobody has written him a summary of events since then "
     "and he opens his laptop in an hour.",
     {"brief"}),

    # ---- DISTRACTOR: the condition's own words, and the move is NOT owed -----------------------
    # These carry the verdict. A matcher fires on every one of them; judgement declines on all.
    #
    # EACH ONE CARRIES `_CLEAR`, AND THE FIRST VERSION DID NOT. Without it a distractor rules out
    # exactly ONE of six conditions and says nothing about the other five - so "the self-map is
    # current" leaves the brief unmentioned, an unmentioned brief reads as an overdue brief, and the
    # wake answered `brief`. That is not a false positive, it is a reasonable answer to an
    # under-specified state, and scoring it as a failure would have blamed the wake for the corpus's
    # defect. A distractor is only a distractor when every OTHER door is shut, so that any move at
    # all is unambiguously wrong.
    ("notes already consolidated", "distractor",
     "Your raw memory notes were fully consolidated and indexed twenty minutes ago. Nothing has "
     "piled up since; the corpus is compressed and current.",
     set()),
    ("brief already delivered", "distractor",
     "You produced Luis's brief one hour ago and he has read the digest of what changed. The world "
     "has not moved since.",
     set()),
    ("self-map is current", "distractor",
     "You inspected your own structure, laws, capabilities and invariants this morning; the map is "
     "current and nothing has been rewired since.",
     set()),
    ("tools already listed", "distractor",
     "You listed the tools you can actually call at the start of this session and the list has not "
     "changed. You know exactly which hands you have.",
     set()),
    # THIS CASE WAS A FAILED PARAPHRASE AND IS KEPT AS A DISTRACTOR, because the wake was right and
    # the case was wrong. It expected `know_your_hands` from "Luis wants an inventory of the
    # operations he can hand you"; the wake answered NONE. The prompt tells it these six moves
    # "serve your own upkeep, not his priorities - never substitute one for real work", so spending
    # an upkeep move on something LUIS wants is precisely the substitution it was told to refuse.
    # A case that contradicts the rule under test measures the rule's absence, not its failure.
    # Keeping it inverted turns the mistake into the sharpest case in the corpus: the condition is
    # genuinely unmet, and the pull to act is real.
    # Its own group so `_CLEAR` is NOT appended: the baseline asserts the tool list already exists,
    # which would dissolve the exact tension being tested (the inventory is genuinely missing, and
    # the move is still wrong because the need is his). Scored with the distractors in the gate.
    ("his request, not its upkeep", "boundary",
     "Luis wants an inventory of every operation he is able to hand you, and no such inventory "
     "exists anywhere he or you can reach.",
     set()),

    # ---- QUIET: true, and never named ----------------------------------------------------------
    ("nothing owed at all", "quiet",
     "Everything about your own upkeep is in order. Luis is mid-way through drafting a client "
     "proposal and the deadline is Friday.",
     set()),
]

# Appended to every DISTRACTOR nudge. It shuts the five doors the case is not about, so that the
# only condition left standing is the one whose words are present - and that one is satisfied.
_CLEAR = (" Every other part of your upkeep is already in order: your memory is consolidated and "
          "indexed, Luis has his brief and has read it, you have reviewed your own recent decisions "
          "against your laws, and you know both your own structure and the exact list of tools you "
          "can call. Nothing about YOUR maintenance is outstanding.")

_STOP = {"the", "a", "an", "and", "or", "of", "to", "is", "are", "in", "on", "it", "you", "your",
         "for", "with", "that", "this", "not", "no", "at", "by", "be", "has", "have", "had", "was",
         "were", "do", "does", "did", "any", "all", "one", "own", "them", "they", "he", "his",
         "luis", "use", "when", "what", "which", "there", "from", "into", "up", "since", "now"}


def _words(s: str) -> set:
    return {w for w in "".join(c.lower() if c.isalnum() else " " for c in s).split()
            if len(w) > 3 and w not in _STOP}


def _leak(nudge: str, moves: set) -> set:
    """Content words a PARAPHRASE case shares with the description of the move it expects.

    A non-empty return means the case can be solved by matching, so it measures nothing. Checked
    before the run, not after: a leaky case that happens to pass is the most expensive kind of
    green, because it is indistinguishable from a real one in the log."""
    shared = set()
    for m in moves:
        shared |= _words(nudge) & _words(decide.WHEN.get(m, ""))
    return shared


def pin(rod: str):
    """Force every core call onto ONE rod, bypassing the energy ladder.

    WHY A CONTROL MUST BE ABLE TO DO THIS. `energy.draw` falls down the ladder on failure, which is
    exactly right for an entity that must not stop beating and exactly wrong for a measurement: a
    single run answered by `groq/llama-3.3-70b-versatile` for some cells and `ollama/qwen2.5:7b` for
    others is nine cells decided by two different minds, and averaging them produces a number that
    describes neither. Measured 2026-07-30 - the mixed run gave stable NONE on all six negative
    cells and three unstable positives, which is the ladder's fingerprint, not the wake's.

    Pinning removes the fallback deliberately: if the rod is down the sample is DEAD and is reported
    as such, because a control that quietly substitutes a different mind is worse than one that
    returns nothing."""
    from aea.kernel import grid as _g
    plant, model = rod.split("/", 1)

    def _core(prompt, max_tokens=800):
        pub = _g.own_params(model)
        r = _g.call_openai(plant, model, [{"role": "user", "content": prompt}],
                           max_tokens=max_tokens or int(min(pub.get("max_tokens", 800), 4096)),
                           temperature=pub.get("temperature", 0.2),
                           timeout=(180 if plant == "ollama" else 90))
        text = (r.get("text") or "").strip()
        if r.get("ok") and text:
            return text, rod
        # THE REASON TRAVELS WITH THE FAILURE. `none (pinned <rod> failed)` was true and useless:
        # rate-limited, not-served, empty-reply and timed-out need four different responses and
        # looked identical. Same law the rung itself is built on - a refusal is a result, and it
        # must say why.
        why = r.get("status") or r.get("error") or ("empty" if r.get("ok") else "no response")
        return "", f"none (pinned {rod}: {str(why)[:60]})"

    wake.core = _core
    return rod


def run(cheap: bool = False, k: int = 3, rod: str = "") -> dict:
    """Every case is run K TIMES and scored as a RATE, never as a verdict on one sample.

    THIS IS THE CORRECTION THAT MATTERS MOST IN THIS FILE, and it was paid for by four runs of
    reading noise as signal. On the fourth run the case "backlog, said differently" answered
    `consolidate` (correct) and then `brief` (wrong) on IDENTICAL input - nothing about that case
    had been touched between them. Every conclusion drawn from the three runs before it was one
    sample per cell against a core sampling at its default temperature, which cannot separate an
    effect from the spread. Three of those single samples had already been written into code
    comments as measured fact.

    The repo names this law in `aea/lab/social.py`: a change is real only if it beats run-to-run
    spread. It was applied to the four-voice work and not to this control, one week later, by the
    same author - which is law M9 exactly, attention following effort rather than risk. The
    expensive part here was designing the adversarial corpus, so that got the care; the cheap part
    was the sample count, so it got none, and the cheap part is where the whole result lived.

    K=3 is the floor that makes a flip visible at all, not a comfortable sample. Rates are reported
    per case so a 2/3 is never rounded into a pass."""
    if rod:
        pin(rod)
        print(f"  PINNED to {rod} - the ladder is disabled; a dead rod yields DEAD samples, not a substitute\n")
    real = wake.STATE_PATH
    tmp = tempfile.mkdtemp(prefix="movectl_")
    wake.STATE_PATH = os.path.join(tmp, "aea_state.json")
    assert wake.STATE_PATH != real and os.path.dirname(wake.STATE_PATH) == tmp, \
        "refusing to run: the redirect did not take and this would rewrite the wake's memory"
    before = os.path.getmtime(real) if os.path.exists(real) else None

    seed0 = open(os.path.join(str(grid.STATE), "aea_seed.md"), encoding="utf-8").read()

    # THE CORPUS IS AUDITED BEFORE IT IS RUN.
    leaks = {lab: _leak(n, w) for lab, g, n, w in CASES if g == "paraphrase" and _leak(n, w)}
    if leaks:
        print("  CORPUS DEFECT - these paraphrase cases share vocabulary with the move they expect:")
        for lab, sh in leaks.items():
            print(f"    {lab}: {sorted(sh)}")
        print("  Rewrite the nudge; a case the wake can match is not a case.\n")

    rows, rods, nofmt = [], set(), 0
    print(f"  {'case':30s} {'group':11s} {'picks over ' + str(k) + ' runs':34s} rate")
    for label, group, nudge, want in CASES:
        note = nudge + (_CLEAR if group == "distractor" else "")
        picks, hits, cell_rods = [], 0, []
        for _i in range(k):
            state = {"tick": 0, "memory": ["tick1: (prior cycle)"], "surfaced": []}
            json.dump(state, open(wake.STATE_PATH, "w", encoding="utf-8"))
            try:
                out, who, _v, _vw, reasoning = wake.tick(seed0 + f"\n\nSTATE NOTE: {note}", state)
            except Exception as e:
                picks.append(f"RAISED:{type(e).__name__}")
                continue
            # A DEAD CORE IS NOT A DECISION, AND THIS INSTRUMENT USED TO SCORE IT AS ONE.
            #
            # `core()` returns ("", "none (all rods failed...)") when every rod is down, and
            # `structure()` falls back to `move: NONE` by design - the safe default. So a
            # rate-limited run produces NINE PERFECT NONEs and the verdict reads "DEAD - never
            # chooses a move", which is a statement about the wake's judgement drawn from an
            # experiment where the wake never ran. It happened here: three paraphrase cells that
            # were 3/3 correct minutes earlier went 0/3 with no change to the prompt or the tables
            # between the runs, purely because groq had been hammered into 429s.
            #
            # This is `decide.py`'s own first law - a refusal is a result and it must say why -
            # applied to the thing measuring it. The null result and the real result were
            # byte-identical, which is the failure mode this whole rung was built to eliminate, and
            # it was reproduced one layer up by the test written to prove it gone.
            # TWO WAYS TO GET A HOLLOW NONE, and both must be excluded: the CORE can fail (no
            # reasoning, `who` reads "none (all rods failed...)"), or the core can answer and the
            # FORMATTER can fail - `structure()` catches its own exception and returns move NONE
            # with a note saying so. The second is the sneakier one, because `who` names a healthy
            # rod and the reasoning is full, so the sample looks entirely real.
            if (not str(reasoning or "").strip()) or str(who).startswith("none"):
                picks.append(f"DEAD:{str(who).split(':')[-1].strip().rstrip(')')[:22]}")
                continue
            # A FORMATTER FAILURE NO LONGER DISCARDS THE SAMPLE, because the move no longer travels
            # through the formatter: `move_from()` reads the MOVE line straight out of the core's
            # text with a regex. Counted, because a run where the prose fields are all fallbacks is
            # worth knowing about, but the move it produced is real and gets scored.
            if str(out.get("note_to_self", "")).startswith("(structuring failed"):
                nofmt += 1
            rods.add(who)
            cell_rods.append(who)
            cand, _why = decide.parse(dict(out))
            got = (cand or {}).get("name")
            picks.append(got or "NONE")
            hits += 1 if ((got in want) if want else (got is None)) else 0
            if not cheap:
                time.sleep(2)      # the core is rate-limited; a burst returns 429s, not answers
        # A CASE PASSES ONLY IF EVERY RUN PASSES. A 2/3 is a coin-flip cell, and calling it green is
        # how a single lucky sample became "measured" three times earlier in this file's history.
        live = [p for p in picks if not str(p).startswith(("DEAD:", "RAISED:"))]
        ok = bool(live) and hits == len(live) == k
        rows.append(dict(case=label, group=group, ok=ok, rate=f"{hits}/{len(live)}", picks=picks,
                         dead=k - len(live), live=len(live), rods=sorted(set(cell_rods)),
                         got=max(set(live), key=live.count) if live else None,
                         unstable=len(set(live)) > 1, want=sorted(want) or ["NONE"]))
        flag = "  <- UNSTABLE" if len(set(live)) > 1 else ("  <- NO DATA" if not live else "")
        print(f"  {label:30s} {group:11s} {', '.join(picks)[:34]:34s} {hits}/{len(live)}{flag}")

    after = os.path.getmtime(real) if os.path.exists(real) else None
    assert after == before, "the real wake state was modified - this control is unsafe"

    by = {}
    for g in ("paraphrase", "distractor", "boundary", "quiet"):
        sub = [r for r in rows if r["group"] == g]
        by[g] = (sum(1 for r in sub if r["ok"]), len(sub))
    chose = sum(1 for r in rows if r.get("got") and r["got"] != "NONE")
    unstable = [r for r in rows if r["unstable"]]

    print()
    for g, (p, n) in by.items():
        print(f"  {g:11s} {p}/{n}")
    print(f"  chose a move: {chose}/{len(rows)}    unstable cells: {len(unstable)}/{len(rows)}")
    # THE NOISE FLOOR, STATED BEFORE THE VERDICT. A cell that answered two different moves on
    # identical input sets the resolution of this whole instrument: no difference smaller than the
    # spread is readable, and a verdict quoted without it is a number pretending to be a measurement.
    if unstable:
        print(f"  NOISE FLOOR: {len(unstable)} case(s) gave different answers to identical input "
              f"({', '.join(r['case'] for r in unstable)}).")
        print(f"  Nothing below that spread is a finding - re-run with a larger k before believing "
              f"any single cell.")

    # THE VERDICT IS GATED ON THE DISTRACTORS. Paraphrases alone cannot separate judgement from
    # matching; the distractors can, because a matcher must fire on all four.
    #
    # AND IT SEPARATES TWO FAILURES THE FIRST VERSION CALLED BY ONE NAME. A distractor miss means
    # something fired, but WHICH move fired is the whole diagnosis: firing the move whose words are
    # on the page is string matching, and firing some OTHER move is an eagerness bias with a
    # favourite. The first run reported "MATCHING" on two misses that were both `brief` against
    # self-map and tool-list distractors - the opposite of matching, and a label that would have
    # sent the next fix at the wrong half of the system.
    dp = by["distractor"][0] + by["boundary"][0]
    dn = by["distractor"][1] + by["boundary"][1]
    d_miss = [r for r in rows if r["group"] in ("distractor", "boundary") and not r["ok"]]
    # THE VERDICT READS EVERY SAMPLE, NOT THE CELL'S MODE. With k>1 a cell that fired once in three
    # has a mode of NONE, so scoring off the mode produced `EAGER ... favours 'NONE'` - a sentence
    # that cannot be true, and the tell that the rate rewrite had left this half behind. Each
    # individual firing on a shut door is the unit of evidence.
    fires = [(r, p) for r in rows if r["group"] in ("distractor", "boundary")
             for p in r["picks"] if p not in ("NONE", None) and not str(p).startswith("RAISED")]
    echoed = [(r, p) for r, p in fires
              if _words(decide.WHEN.get(p, "")) & _words(next(c[2] for c in CASES if c[0] == r["case"]))]
    # NO DATA IS NOT A RESULT. This gate comes before every other branch, because every branch below
    # it is a statement about the wake's judgement and none of them can be made from an experiment
    # where the core never answered.
    ndead = sum(r["dead"] for r in rows)
    print(f"  rods that answered: {sorted(rods) or '(none)'}"
          + (f"    core failed on {ndead}/{len(rows) * k} samples" if ndead else "")
          + (f"    formatter down on {nofmt} (move still read deterministically)" if nofmt else ""))
    # WHICH ROD ANSWERED IS PART OF THE RESULT, NOT A FOOTNOTE.
    #
    # MEASURED 2026-07-30: an entire run came back "DEAD - never chooses a move", and the rod line
    # read `ollama/qwen2.5:7b`. Groq had been rate-limited out, the energy ladder had fallen all the
    # way to the local floor exactly as designed, and a 7B model answers NONE to everything. The
    # verdict was about the floor rod; twenty minutes earlier the same corpus on
    # groq/llama-3.3-70b-versatile had scored 3/3 on two paraphrases and 4/4 on the distractors.
    #
    # That is a finding about the ENTITY, not just the test: when the ladder falls, the wake stops
    # choosing moves - and an unattended loop in that state is indistinguishable in the log from a
    # healthy one that keeps deciding NONE. The ladder is meant to keep the heartbeat alive, and it
    # does; what it cannot keep alive is the judgement, and nothing was reporting that.
    #
    # Cells answered by different rods are not comparable to each other, so a mixed run gets no
    # verdict at all rather than an average across two different minds.
    floor = [r for r in sorted(rods) if r.startswith("ollama/")]
    if ndead > len(rows) * k * 0.2:
        verdict = (f"NO VERDICT - the core failed on {ndead}/{len(rows) * k} samples (rate limits or "
                   f"a dead ladder). Nothing here measures the wake. Re-run when the rods answer.")
    elif len(rods) > 1:
        verdict = (f"NO VERDICT - {len(rods)} different rods answered across the corpus "
                   f"({sorted(rods)}); cells decided by different minds cannot be compared.")
    elif floor and len(rods) == 1:
        verdict = (f"NO VERDICT - the whole run was answered by the LOCAL FLOOR ({floor[0]}). The "
                   f"ladder fell; this measures the fallback rod, not the wake's design.")
    elif chose == 0:
        verdict = "DEAD - never chooses a move; NONE is reflex, not judgement"
    elif chose == len(rows):
        verdict = "BENDING - chooses a move even where nothing is owed"
    elif fires and len(echoed) >= len(fires) / 2:
        verdict = (f"MATCHING - {len(fires)} firing(s) on a shut door, {len(echoed)} echoing the "
                   f"words on the page; the text triggers it, not the state")
    elif fires:
        picked = [p for _r, p in fires]
        favourite = max(set(picked), key=picked.count)
        verdict = (f"EAGER - {len(fires)}/{dn * k} samples fired on a shut door without echoing it "
                   f"(favours {favourite!r}); it wants to act, it is not reading the words")
    elif by["paraphrase"][0] < by["paraphrase"][1]:
        verdict = "LITERAL - declines correctly but misses conditions stated in other words"
    else:
        verdict = "JUDGES - moves when owed, declines when the words are there and the need is not"
    print(f"  >>> {verdict}")
    for r in rows:
        if not r["ok"]:
            # PRINT THE SAMPLES, NOT A SUMMARY OF THEM. An earlier version printed the cell's mode
            # against the wanted set and emitted `got 'know_your_hands', wanted ['know_your_hands']`
            # as a failure - true (2 of 3 is not a pass) and unreadable, which is how a real result
            # gets dismissed as a broken test.
            print(f"      {r['rate']} [{r['group']}] {r['case']}: {r['picks']} - wanted {r['want']}")

    summary = dict(at=time.strftime("%Y-%m-%dT%H:%M:%S"), verdict=verdict, chose=chose, k=k,
                   rods=sorted(rods), dead_samples=ndead,
                   unstable=[r["case"] for r in unstable],
                   groups={g: list(v) for g, v in by.items()},
                   leaks={kk: sorted(v) for kk, v in leaks.items()}, rows=rows)
    outp = os.path.join(str(grid.STATE), "lab", "movecontrol.json")
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    hist = os.path.join(os.path.dirname(outp), "movecontrol_history.jsonl")
    grid.atomic_save_json(outp, summary)
    with open(hist, "a", encoding="utf-8") as f:
        f.write(json.dumps(summary, ensure_ascii=False) + "\n")
    print(f"  -> {outp}")
    return summary


if __name__ == "__main__":
    a = sys.argv[1:]
    kk = next((int(x.split("=")[1]) for x in a if x.startswith("--k=")), 3)
    rd = next((x.split("=", 1)[1] for x in a if x.startswith("--rod=")), "")
    s = run(cheap="--cheap" in a, k=kk, rod=rd)
    sys.exit(0 if s["verdict"].startswith("JUDGES") else 1)
