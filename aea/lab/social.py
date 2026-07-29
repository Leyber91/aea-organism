"""social.py - MEASURE THE CONVERSATION ON MANY DIMENSIONS AT ONCE.

Luis, 2026-07-30: "now when you are getting data, you amplify the parameters that you need to take.
Because if we amplify the parameters on many dimensions, we will get it more right than we're
getting it. And it's crucial."

He is right, and the reason is specific rather than general. Up to now a party run reported three
numbers: names used, content reused, distinct speakers. Three numbers cannot tell the difference
between the two failures that actually matter and that look identical from outside:

    a conversation that is REAL but boring
    a conversation that is FAKE but lively

and they need opposite fixes. More dimensions is not more rigour for its own sake - it is the only
way those two separate.

THE ONE THAT MATTERS MOST, and nothing measured it before: VOICE COLLAPSE. Four characters running
on one model with four prompts will drift toward a single register - same sentence length, same
hedges, same vocabulary - while every individual line still reads fine. It is invisible turn by
turn and obvious across a transcript, which is exactly the shape of defect a per-turn eye misses.
`distinctiveness` and `convergence` below are built for it: if the four are collapsing, no amount
of prompt work is the fix and the architecture has to change.

WHAT IS MEASURED HERE IS BEHAVIOUR, NOT MIND. Every column is a count over text. "Dominance" is
share of words, not a personality; "role" is a pattern of speech acts, not an identity. The claim
ceiling holds here as everywhere: these are correlates, and the moment one gets described as a
trait somebody has, this file has been misread.

    python -m aea.lab.social                    read the last party run
    python -m aea.lab.social --file X.json      read a specific one
"""
from __future__ import annotations

import json
import math
import os
import re
import statistics
import sys

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# SPEECH ACTS, keyed to a closed vocabulary of surface markers. Crude by design and honest about
# it: a model classifier per turn would cost a call per line and drift between runs, and the point
# of these columns is to be comparable ACROSS runs, which a deterministic rule is and a model is
# not (law W2).
ACTS = {
    "question":   re.compile(r"\?\s*$|^\s*(?:what|why|how|who|when|where|do|does|did|is|are|can|"
                             r"could|would|should|isn'?t|aren'?t)\b", re.I),
    "disagree":   re.compile(r"\b(?:but|however|actually|i disagree|that'?s not|no,|isn'?t|"
                             r"i don'?t think|wrong|except|although)\b", re.I),
    "agree":      re.compile(r"\b(?:exactly|agreed|that'?s right|fair enough|true|yes,|good point|"
                             r"i think you'?re right|makes sense)\b", re.I),
    "summarise":  re.compile(r"\b(?:so (?:what|we|you'?re)|in other words|to be clear|what you'?re "
                             r"saying|the point is|so far)\b", re.I),
    "story":      re.compile(r"\b(?:once|i remember|used to|there was|my (?:grand|friend|brother|"
                             r"sister|mother|father)|reminds me)\b", re.I),
    "hedge":      re.compile(r"\b(?:maybe|perhaps|i guess|sort of|kind of|might|possibly|i suppose|"
                             r"probably)\b", re.I),
    "commit":     re.compile(r"\b(?:i think|i believe|i'?d say|in my view|the truth is|always|"
                             r"never)\b", re.I),
}


def _w(t: str) -> list:
    return re.findall(r"[a-z']+", (t or "").lower())


def _content(t: str) -> set:
    """Content words only - the function words are what everybody shares, so leaving them in makes
    every speaker look similar and hides exactly the collapse this is looking for."""
    STOP = set(("the a an and or but of to in on at for from with by is are was were be been am i "
                "you he she it we they me him her us them my your his its our their this that these "
                "those as if so not no do does did have has had will would can could should may "
                "might must about into over under just very really more most much some any all "
                "what why how who when where which than then there here now").split())
    return set(w for w in _w(t) if len(w) > 2 and w not in STOP)


def _jaccard(a: set, b: set) -> float:
    return len(a & b) / max(len(a | b), 1)


def per_turn(turns: list) -> list:
    """One row per turn, many columns. The raw material everything below is derived from."""
    rows = []
    names = {t["who"] for t in turns}
    for i, t in enumerate(turns):
        txt = t["text"]
        w = _w(txt)
        sents = [s for s in re.split(r"(?<=[.!?])\s+", txt) if s.strip()]
        named = [n for n in names if n != t["who"] and re.search(rf"\b{n}\b", txt, re.I)]
        # HOW FAR BACK DID IT REACH. The single best signal that this is a conversation rather than
        # a list: a turn that reuses content words from many turns ago is remembering, and one that
        # only echoes the previous line is reacting. Reported as the DISTANCE, because reaching
        # back two turns is normal and reaching back nine is the thing worth counting.
        cw = _content(txt)
        reach = 0
        for j in range(max(0, i - 12), i - 1):
            if len(cw & _content(turns[j]["text"])) >= 2:
                reach = max(reach, i - j)
        rows.append(dict(
            i=i, who=t["who"], chars=len(txt), words=len(w),
            sentences=len(sents),
            mean_sent=round(len(w) / max(len(sents), 1), 1),
            ttr=round(len(set(w)) / max(len(w), 1), 3),      # type-token: vocabulary richness
            named=named, addressed=bool(named),
            reach=reach,
            acts=[k for k, p in ACTS.items() if p.search(txt)],
        ))
    return rows


def distinctiveness(turns: list) -> dict:
    """ARE THE FOUR ACTUALLY DIFFERENT, and are they staying different.

    Two numbers, and the second is the one to watch:
      SEPARATION  mean pairwise vocabulary distance between speakers over the whole run.
                  1.0 = no shared content words, 0.0 = identical registers.
      CONVERGENCE separation in the FIRST half minus separation in the SECOND. Positive means they
                  are collapsing toward one voice as the conversation goes on - the characteristic
                  failure of one model wearing four prompts, and invisible line by line.
    """
    who = sorted({t["who"] for t in turns})
    if len(who) < 2:
        return {}

    def sep(ts):
        vocab = {n: _content(" ".join(t["text"] for t in ts if t["who"] == n)) for n in who}
        pairs = [(a, b) for i, a in enumerate(who) for b in who[i + 1:]]
        ds = [1.0 - _jaccard(vocab[a], vocab[b]) for a, b in pairs if vocab[a] and vocab[b]]
        return (statistics.mean(ds) if ds else 0.0), dict(
            (f"{a}/{b}", round(1.0 - _jaccard(vocab[a], vocab[b]), 3)) for a, b in pairs)

    whole, pairwise = sep(turns)
    h = len(turns) // 2
    first, _ = sep(turns[:h])
    second, _ = sep(turns[h:])
    # Sentence-length and richness spread: two speakers can share vocabulary and still sound
    # different if one talks in bursts and the other in paragraphs. If BOTH this and the vocabulary
    # separation are low, they are one voice.
    rows = per_turn(turns)
    by = {n: [r for r in rows if r["who"] == n] for n in who}
    lens = {n: statistics.mean([r["words"] for r in v]) for n, v in by.items() if v}
    return dict(separation=round(whole, 3), pairwise=pairwise,
                first_half=round(first, 3), second_half=round(second, 3),
                convergence=round(first - second, 3),
                length_spread=round((max(lens.values()) - min(lens.values())) if lens else 0, 1),
                length_by=dict((n, round(v)) for n, v in lens.items()))


def structure(turns: list) -> dict:
    """WHO TALKS TO WHOM, WHO HOLDS THE FLOOR, AND WHO ENDED UP PLAYING WHAT.

    Roles here are EMERGENT and measured, never assigned: whoever asks the most questions is the
    questioner in this conversation, whether or not their persona says so. That gap - the role the
    prompt gave them versus the role they actually played - is one of the most useful things this
    module can show, because a persona that never manifests is a costume nobody wore.
    """
    who = sorted({t["who"] for t in turns})
    rows = per_turn(turns)
    words = {n: sum(r["words"] for r in rows if r["who"] == n) for n in who}
    total = max(sum(words.values()), 1)
    # who answers whom: an edge from A to B when B spoke immediately after A, or A named B
    edges: dict = {}
    for i, r in enumerate(rows):
        if i:
            edges[(rows[i - 1]["who"], r["who"])] = edges.get((rows[i - 1]["who"], r["who"]), 0) + 1
        for n in r["named"]:
            edges[(r["who"], n)] = edges.get((r["who"], n), 0) + 1
    acts = {n: {} for n in who}
    for r in rows:
        for a in r["acts"]:
            acts[r["who"]][a] = acts[r["who"]].get(a, 0) + 1
    roles = {}
    for n in who:
        a = acts[n]
        turns_n = max(sum(1 for r in rows if r["who"] == n), 1)
        roles[n] = max(a, key=a.get) if a else "-"
        acts[n] = dict(sorted(((k, round(v / turns_n, 2)) for k, v in a.items()),
                              key=lambda x: -x[1]))
    # GINI OF THE FLOOR. One number for "is this a conversation or a lecture with an audience".
    # 0.0 = everybody talks equally, toward 1.0 = one speaker dominates.
    shares = sorted(words[n] / total for n in who)
    n = len(shares)
    gini = (sum((2 * i - n + 1) * s for i, s in enumerate(shares)) / (n * sum(shares))
            if sum(shares) else 0.0)
    silent = [n for n in who if words[n] == 0]
    return dict(floor_share=dict((n, round(words[n] / total, 3)) for n in who),
                gini=round(gini, 3), roles=roles, acts=acts,
                edges=dict((f"{a}->{b}", c) for (a, b), c in sorted(edges.items(), key=lambda x: -x[1])),
                silent=silent)


def flow(turns: list) -> dict:
    """DOES IT MOVE, AND DOES IT REMEMBER."""
    rows = per_turn(turns)
    reaches = [r["reach"] for r in rows if r["reach"]]
    h = len(turns) // 2
    topic_a, topic_b = _content(" ".join(t["text"] for t in turns[:h])), \
                       _content(" ".join(t["text"] for t in turns[h:]))
    return dict(
        # A turn that reaches back MORE than two is remembering rather than merely reacting.
        recall_turns=sum(1 for r in rows if r["reach"] > 2),
        recall_depth_max=max(reaches) if reaches else 0,
        recall_depth_mean=round(statistics.mean(reaches), 1) if reaches else 0.0,
        addressed=sum(1 for r in rows if r["addressed"]),
        # 0 = the second half is about exactly what the first half was (stuck), 1 = nothing in
        # common (incoherent). A real conversation drifts; it does not teleport and it does not sit.
        topic_drift=round(1.0 - _jaccard(topic_a, topic_b), 3),
        questions=sum(1 for r in rows if "question" in r["acts"]),
        disagreements=sum(1 for r in rows if "disagree" in r["acts"]),
        hedges=sum(1 for r in rows if "hedge" in r["acts"]),
    )


def report(turns: list, extra: dict = None) -> str:
    d, s, f = distinctiveness(turns), structure(turns), flow(turns)
    rows = per_turn(turns)
    L = ["=" * 96, f"SOCIAL ANALYSIS - {len(turns)} turns, {len(set(t['who'] for t in turns))} speakers",
         "=" * 96]
    L.append("\nARE THEY ACTUALLY DIFFERENT PEOPLE")
    L.append(f"  vocabulary separation      {d.get('separation', 0):.3f}   "
             f"(1.0 = nothing shared, 0.0 = one voice)")
    L.append(f"  first half -> second half  {d.get('first_half', 0):.3f} -> {d.get('second_half', 0):.3f}"
             f"   convergence {d.get('convergence', 0):+.3f}")
    if d.get("convergence", 0) > 0.05:
        L.append("     >>> THEY ARE COLLAPSING toward one voice. Prompt work will not fix this.")
    elif d.get("convergence", 0) < -0.05:
        L.append("     >>> They are DIVERGING as they talk - the characters are separating.")
    else:
        L.append("     >>> Holding separate.")
    L.append(f"  turn length by speaker     {d.get('length_by', {})}  spread {d.get('length_spread', 0)}")
    for k, v in sorted(d.get("pairwise", {}).items(), key=lambda x: x[1])[:3]:
        L.append(f"  closest pair               {k}  {v:.3f}"
                 + ("   <- these two sound alike" if v < 0.75 else ""))

    L.append("\nWHO HELD THE FLOOR")
    for n, sh in sorted(s["floor_share"].items(), key=lambda x: -x[1]):
        bar = "#" * int(sh * 40)
        L.append(f"  {n:8s} {sh:5.1%} {bar}")
    L.append(f"  gini {s['gini']:.3f}   "
             + ("balanced" if s["gini"] < 0.2 else
                "one voice dominating" if s["gini"] > 0.4 else "uneven"))
    if s["silent"]:
        L.append(f"  NEVER SPOKE: {', '.join(s['silent'])}   <- a cast member who is not in the room")

    L.append("\nTHE ROLE EACH ONE ACTUALLY PLAYED (measured, not assigned)")
    for n, r in s["roles"].items():
        L.append(f"  {n:8s} {r:10s} {s['acts'][n]}")

    L.append("\nWHO ANSWERED WHOM")
    for k, v in list(s["edges"].items())[:8]:
        L.append(f"  {k:22s} {v}")

    L.append("\nDOES IT MOVE, AND DOES IT REMEMBER")
    L.append(f"  turns reaching back >2     {f['recall_turns']}/{len(turns)}   "
             f"deepest {f['recall_depth_max']} turns, mean {f['recall_depth_mean']}")
    L.append(f"  addressed someone by name  {f['addressed']}/{len(turns)}")
    L.append(f"  topic drift first->second  {f['topic_drift']:.3f}   "
             + ("stuck on one thing" if f["topic_drift"] < 0.5 else
                "incoherent - no thread" if f["topic_drift"] > 0.93 else "moving"))
    L.append(f"  questions {f['questions']}   disagreements {f['disagreements']}   "
             f"hedges {f['hedges']}")

    L.append("\nPER TURN")
    L.append(f"  {'#':>3} {'who':8s} {'wds':>4} {'sent':>4} {'ttr':>5} {'back':>4}  acts")
    for r in rows:
        L.append(f"  {r['i']+1:3d} {r['who']:8s} {r['words']:4d} {r['sentences']:4d} "
                 f"{r['ttr']:5.2f} {r['reach']:4d}  {','.join(r['acts'])[:44]}")
    if extra:
        L.append("\nRUN")
        for k, v in extra.items():
            L.append(f"  {k:26s} {v}")
    return "\n".join(L)


def analyse(path: str = "") -> dict:
    p = path or os.path.join(str(grid.STATE), "lab", "party", "party.json")
    d = grid.load_json(p, {})
    turns = d.get("turns") or []
    if not turns:
        print(f"no turns in {p}")
        return {}
    print(report(turns))
    out = dict(distinctiveness=distinctiveness(turns), structure=structure(turns),
               flow=flow(turns), per_turn=per_turn(turns))
    grid.atomic_save_json(os.path.join(str(grid.STATE), "lab", "party", "social.json"), out)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    analyse(a[a.index("--file") + 1] if "--file" in a else "")
