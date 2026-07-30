"""council.py - SEVERAL OPINIONS ON ONE QUESTION, AND THE DISAGREEMENT KEPT INTACT.

Luis, 2026-07-30: "now is time to get the data learn from it... You can do now conversational text
conversations if you like to check at the point that a council of opinions is needed. we know how to
manage different filter personalities, like different experts talking."

This is where the four-voice work pays off as something the entity actually uses. Everything here
was learned out loud, in a room, with speakers - and none of it needed to be about voice:

  DIFFERENT RODS       one model wearing four prompts converges. Measured, and not fixable by
                       prompting: sycophancy is trained in, and a same-model population drifts to a
                       shared convention on its own. Different priors are the cheap real fix.
  FIRST-PERSON SEEDS   one line of adjectives is the demographics-only condition, the worst
                       persona seeding ever measured - 74% of the human ceiling against 83% for
                       seeds built from concrete incidents.
  PROHIBITIONS         the four named multi-agent failure modes - thanking, announcing, restating,
                       self-answering - written as negative constraints, plus a mechanical loop
                       detector, because the documented failure is that agents RECOGNISE the loop
                       and still cannot leave it.
  A HELD SEAT          one member that does not move. At four members you cannot express the
                       committed minority that prevents convergence, so it is hard-coded.
  think_off            measured per model family and, until today, called by nothing.

WHAT A COUNCIL IS FOR, AND THE ONE WAY IT FAILS. A council that agrees with itself is a more
expensive single opinion with more words. The output that matters is not the synthesis - it is
WHAT SURVIVED DISAGREEMENT, and what did not. So dissent is measured, reported, and never smoothed:
if every member agrees, that is reported as a finding about the question and about the council,
because unanimity among four models on one machine is more likely to be a shared prior than a truth.

    python -m aea.mind.council "should the render mystery be chased or worked around"
    python -m aea.mind.council --rounds 3 "is persistent memory worth the honesty risk"
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from aea.kernel import grid
from aea.mind import tiers

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = os.path.join(str(grid.STATE), "council")
RUNAWAY = 4000                  # the only cap: a loop guard, never a length control. Tokens beyond
                                # what gets used are the thinking, and cutting them buys a worse
                                # answer with money nobody was spending.


class Seat:
    def __init__(self, name, tier, seed, held=False):
        self.name, self.tier, self.seed, self.held = name, tier, seed, held

    @property
    def rod(self):
        return tiers.organ(self.tier)


# THE SEATS. First-person and concrete, for the reason in the header - "be sceptical" produces
# sceptical nothing, while "I have shipped three things that worked in a demo and died in a week"
# produces a position. Each on a different rod where one is available.
SEATS = [
    Seat("BUILDER", "reflex",
         "I ship things. I have also shipped three things that worked in a demo and died the first "
         "week somebody real touched them, so when I hear a plan I am hearing for the part that has "
         "not been built yet and is being described as if it had. I ask what the first version is "
         "and what it costs. I do not care whether an idea is good in general; I care what happens "
         "on Tuesday."),
    Seat("SKEPTIC", "voice",
         "My job is the failure mode. Not pessimism - I am not bored by things working, I just know "
         "that the way something breaks is usually visible before it breaks and everyone is looking "
         "at the happy path. I ask what has to be true for this to work, and then which of those "
         "things nobody has checked. I have been wrong by being too cautious and I would rather be "
         "wrong that way.", held=True),
    Seat("USER", "voice",
         "I keep asking who this is for. Not as a rhetorical move - I mean literally, which person, "
         "doing what, at what moment. Most of what gets built is built for the person building it, "
         "and you can tell because nobody can describe the moment it gets used. I ask people to "
         "describe that moment and I notice when they cannot."),
    Seat("HISTORIAN", "depth",
         "I remember what was tried. Usually somebody did this already, and usually it neither "
         "worked nor failed - it worked in a narrower way than anyone remembers. So I ask what the "
         "closest prior attempt was and what actually happened to it, and I am careful about the "
         "difference between a thing that failed and a thing that was abandoned."),
]

PROHIBITIONS = (
    "NEVER thank anyone for their point. NEVER announce what you are about to say - say it. "
    "NEVER restate the previous speaker before responding. NEVER ask a question you then answer "
    "yourself. NEVER end by inviting the others to continue. Do not hedge to be agreeable: if you "
    "think someone is wrong, say which part and why.")


def ask(rod: dict, system: str, user: str, temp: float = 0.7) -> str:
    """One call, reasoning handled. See `aea/lab/party.ask` for the measurement behind this - a
    reasoning rod on a small budget returns NOTHING, or returns its scratchpad because `content` was
    empty and the transport falls back to `reasoning_content`."""
    off = grid.think_off(rod["model"])
    msgs = []
    if off.get("_system"):
        msgs.append({"role": "system", "content": off["_system"]})
    msgs += [{"role": "system", "content": system}, {"role": "user", "content": user}]
    try:
        r = grid.call_openai(rod["plant"], rod["model"], msgs, RUNAWAY, temp,
                             max(rod.get("budget", 40), 60))
        return (r.get("text") or "").strip()
    except Exception as e:
        return ""


def _clean(t: str, name: str) -> str:
    t = re.sub(r"<think>.*?</think>", " ", t or "", flags=re.S | re.I)
    t = re.sub(r"^\s*%s\s*[:,\-]?\s+" % re.escape(name), "", t, flags=re.I)
    # The meta-reject from the party, unchanged: a reasoning rod narrating the task is not an
    # opinion, and no amount of stripping turns it into one.
    if re.search(r"\bthe user\b|\bmy character\b|\bas an ai\b|\bthe (?:prompt|instructions?)\b",
                 t, re.I):
        return ""
    return re.sub(r"[*_#`]+", "", t).strip().strip('"').strip()


def _content(t: str) -> set:
    STOP = set(("the a an and or but of to in on at for from with by is are was were be been am i "
                "you it we they this that as if so not no do does did have has had will would can "
                "could should just very really more what why how who when where think about it's "
                "there their them then than").split())
    return set(w for w in re.findall(r"[a-z']{4,}", (t or "").lower()) if w not in STOP)


def convene(question: str, rounds: int = 2, seats: list = None, verbose: bool = True) -> dict:
    """Put the question to every seat, let them read each other, and keep the disagreement.

    Round 1 is INDEPENDENT and that is not an implementation detail. If they see each other first,
    the first answer anchors the rest and what comes back is one opinion with three endorsements -
    which is the specific way a council becomes theatre. They read each other only from round 2, and
    the change from round 1 to round 2 is itself reported: a seat that abandons its position the
    moment it sees the others is measured, not trusted."""
    seats = seats or SEATS
    log = {s.name: [] for s in seats}
    t0 = time.time()

    def one(s, prior_text):
        held = ("\nYou hold your position. If the others converge and you still think they are "
                "wrong, say so plainly and say what would change your mind." if s.held else "")
        sysm = (f"You are {s.name}, one of {len(seats)} people asked for an opinion.\n"
                f"WHO YOU ARE: {s.seed}\n"
                "Answer in 3-6 sentences of plain spoken English. Lead with your actual position, "
                "then the reason. Name the thing you are least sure about. If you do not know, say "
                "so - a council of four confident guesses is worse than one honest gap.\n"
                + PROHIBITIONS + held)
        user = f"THE QUESTION: {question}"
        if prior_text:
            user += ("\n\nWHAT THE OTHERS SAID (you have not spoken since):\n" + prior_text
                     + "\n\nYou may change your mind - if you do, say which argument moved you. You "
                       "may also hold. Do not agree just because they agree.")
        return _clean(ask(s.rod, sysm, user), s.name)

    for r in range(rounds):
        prior = ""
        if r:
            prior = "\n\n".join(f"{n}: {log[n][-1]}" for n in log if log[n])
        if verbose:
            print(f"\n{'=' * 96}\nROUND {r + 1}"
                  + ("  (independent - nobody has seen anyone else)" if r == 0
                     else "  (they have now read each other)"))
            print("=" * 96)
        with ThreadPoolExecutor(max_workers=len(seats)) as ex:
            got = list(ex.map(lambda s: (s.name, one(s, prior)), seats))
        # ONE RETRY FOR AN EMPTY SEAT. Measured on the first real run: USER returned nothing in
        # round 2 and simply vanished from the council, so the question was answered by three
        # opinions while the report still said four. A silent seat is not an abstention - nobody
        # decided to abstain - and a council that loses a member without saying so is reporting a
        # narrower range than it had.
        missing = [n for n, t in got if not t]
        if missing:
            with ThreadPoolExecutor(max_workers=len(missing)) as ex:
                retry = dict(ex.map(
                    lambda n: (n, one(next(s for s in seats if s.name == n), prior)), missing))
            got = [(n, t or retry.get(n, "")) for n, t in got]
            still = [n for n, t in got if not t]
            if still and verbose:
                print(f"\n  (no answer from {', '.join(still)} after a retry - the council is "
                      f"{len(seats) - len(still)} seats this round, not {len(seats)})")
        for name, text in got:
            if text:
                log[name].append(text)
            if verbose:
                print(f"\n  {name}  [{next(s.tier for s in seats if s.name == name)}]")
                print("       " + (text or "(no answer)").replace("\n", "\n       ")[:900])

    # WHERE THEY LANDED, measured rather than asserted. Pairwise agreement on content words is
    # crude and it is deliberately crude: the alternative is asking a model whether they agreed,
    # which is one more opinion pretending to be a measurement.
    finals = {n: v[-1] for n, v in log.items() if v}
    names = sorted(finals)
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
    sim = {}
    for a, b in pairs:
        wa, wb = _content(finals[a]), _content(finals[b])
        sim[f"{a}/{b}"] = round(len(wa & wb) / max(len(wa | wb), 1), 3)
    # `moved` MEASURES VOCABULARY, NOT POSITION, and that limit is stated because the number looks
    # like it means more than it does. A seat that rewrites its answer from scratch while holding
    # exactly the same view scores high here; measured on the first real run, HISTORIAN scored 0.91
    # having gone from one phrasing to another of the same "hold". It is a flag to go and READ the
    # two rounds, never a claim that somebody changed their mind. Distinguishing a rewrite from a
    # reversal needs a judgement, and a judgement here would be a fifth opinion pretending to be a
    # measurement.
    moved = {}
    for n, v in log.items():
        if len(v) >= 2:
            first, last = _content(v[0]), _content(v[-1])
            moved[n] = round(1.0 - len(first & last) / max(len(first | last), 1), 3)

    res = dict(question=question, rounds=rounds, log=log, finals=finals,
               agreement=sim, moved=moved, seconds=round(time.time() - t0, 1))
    if verbose:
        print(f"\n{'=' * 96}\nWHERE THEY LANDED\n{'=' * 96}")
        if sim:
            hi = max(sim.values()); lo = min(sim.values())
            print(f"  pairwise overlap  " + "  ".join(f"{k} {v:.2f}" for k, v in sim.items()))
            print(f"  most aligned      {max(sim, key=sim.get)} {hi:.2f}")
            print(f"  furthest apart    {min(sim, key=sim.get)} {lo:.2f}   <- read these two first")
            if lo > 0.55:
                print("  >>> THEY ALL AGREE. Treat that as a finding about the COUNCIL before you")
                print("      treat it as one about the question - four models on one machine share")
                print("      priors, and unanimity is the cheapest thing for them to produce.")
        if moved:
            print(f"  moved after reading each other: "
                  + "  ".join(f"{k} {v:.2f}" for k, v in sorted(moved.items(), key=lambda x: -x[1])))
            top = max(moved, key=moved.get)
            if moved[top] > 0.75:
                print(f"  >>> {top} abandoned its round-1 position almost entirely. That is either")
                print(f"      a good argument or a soft seat; read its round 1 and decide which.")
        print(f"  {res['seconds']}s")
    os.makedirs(OUT, exist_ok=True)
    grid.atomic_save_json(os.path.join(OUT, "last.json"),
                          dict(at=time.strftime("%Y-%m-%d %H:%M:%S"), **res))
    return res


if __name__ == "__main__":
    a = [x for x in sys.argv[1:]]
    rounds = 2
    if "--rounds" in a:
        i = a.index("--rounds")
        rounds = int(a[i + 1]); del a[i:i + 2]
    q = " ".join(a).strip()
    if not q:
        print(__doc__)
    else:
        convene(q, rounds=rounds)
