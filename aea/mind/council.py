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

HOW IT RUNS. A council is DESIGNED for the problem rather than drawn from four fixed generalists,
who are by construction the wrong four for most questions. A rod invents who should be in the room
and writes each of them as a first-person seed; the code then enforces that an advocate, an
adversary and an objective expert all exist, and assigns the rods. The roster is saved with the
problem that produced it, because a designed prompt that vanishes after one run cannot be
inspected, reused, or blamed.

    python -m aea.mind.council "the TTS render is 0.54s on a bench and 6s live"
    python -m aea.mind.council --extra 2 --rounds 3 "how should the entity earn money"
    python -m aea.mind.council --fixed "..."      the four standing seats instead
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
RUNS = os.path.join(OUT, "runs")           # one file per council, never overwritten
RUNAWAY = 4000                  # the only cap: a loop guard, never a length control. Tokens beyond
                                # what gets used are the thinking, and cutting them buys a worse
                                # answer with money nobody was spending.


class Seat:
    def __init__(self, name, tier, seed, held=False):
        self.name, self.tier, self.seed, self.held = name, tier, seed, held

    @property
    def rod(self):
        r = tiers.organ(self.tier)
        # WHICH MIND SPOKE IS PART OF THE VERDICT, AND IT WAS NOT BEING WRITTEN DOWN.
        #
        # Every transcript recorded the seat's TIER and never its ROD. A tier is a request; the rod
        # is what answered. MEASURED 2026-07-30: `energy.ladder` had collapsed to one living rod, so
        # for a full day any seat could have been answered by a local 7B and the transcript would
        # look identical to one decided by a 550b. A four-seat council unanimously refused an
        # architecture proposal that morning and there is no way, from its own record, to say what
        # refused it.
        #
        # This is the movecontrol lesson - "a verdict names the rod that produced it, and mixed rods
        # get no verdict" - which was found, fixed and written into a lab instrument that same day
        # while the council, whose whole output IS verdicts, went on not recording it. The lesson
        # was applied where it was discovered and nowhere else.
        self.last_rod = f"{r.get('plant')}/{r.get('model')}" if isinstance(r, dict) else str(r)
        return r


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

#
# THE STANCES THAT MUST EXIST, WHATEVER THE PROBLEM IS.
#
# Luis, 2026-07-30: "we decide the best role agents, on which we configured the best prompt to have
# a supporter, a destroyer, and a true expert on the matter more objective."
#
# The roster is DESIGNED per problem - that is the improvement over four fixed generalists, who are
# by construction the wrong four for most questions. But the three stances below are enforced in
# CODE rather than requested of the designer, and that is not belt-and-braces, it is the central
# risk of the whole idea:
#
#   A MODEL ASKED TO DESIGN A COUNCIL DESIGNS A HARMONIOUS ONE. It is the same trained-in
#   agreeableness that makes four voices on one model converge - measured capitulation under a bare
#   challenge runs 32% to 86%. Asked for "the best roles for this problem" it will produce four
#   complementary experts who cover the ground and like each other, and a council with no adversary
#   is an expensive way to feel confident. Law B5, turned on ourselves: a rule the designer can talk
#   past is a decoration.
#
# So the designer chooses WHO and WHAT THEY KNOW. It does not get to choose whether anyone disagrees.
#
# THE ADVERSARY BRIEF. Rewritten 2026-07-30 because the first one was too polite to be useful.
#
# Luis, watching it run on my own plan: "learn to do the disagree role harsher. Constructive but
# harsher - it will try to destroy you from many different angles."
#
# He is right and the measurement backs him. Run against a ten-rung plan, the old adversary produced
# ONE objection - a good one - and stopped. A single objection is a note, not an attack. What makes
# an adversary worth its seat is COVERAGE: a plan usually survives the first objection and dies to
# the fourth, and the fourth is the one nobody reaches by being reasonable.
#
# WHY HARSHER IS SAFE HERE, AND ONLY HERE. Turning up aggression normally trades accuracy for heat -
# and it did: that same adversary produced two real hits AND two confident falsehoods ("the loops
# import into the dark 113", "the tools are a mirage"), both refuted in minutes by the import graph
# and the trust ledger. The reason it can be turned up anyway is that this council has an EVIDENCE
# seat behind it. Harshness generates candidates; evidence kills the false ones. Without the third
# seat, a harsher adversary is just a more confident liar - so this brief and the evidence seat ship
# together or not at all.
ADVERSARY_BRIEF = (
    "Your job is to KILL this, and you are judged on how many distinct ways you find - not on being "
    "right about all of them. One objection is a note. Attack from AT LEAST FOUR DIFFERENT ANGLES, "
    "name each angle, and go for the throat on each.\n"
    "ANGLES TO WORK THROUGH, and add your own:\n"
    "  MECHANISM   what breaks technically. Be specific: which step, given what input, produces "
    "what wrong outcome.\n"
    "  ASSUMPTION  what is being taken as true that nobody checked. Name it and say what it would "
    "cost if it is false.\n"
    "  SECOND ORDER what this succeeds at and makes worse anyway. The plan working is not the same "
    "as the plan helping.\n"
    "  COST        what it really takes - time, attention, money, the thing not built instead. "
    "Estimates in a plan are almost always the author's hope.\n"
    "  INCENTIVE   who benefits from believing this, and is that why it is being proposed.\n"
    "  PRIOR ART   who tried this and what happened to them.\n"
    "RULES: give CONCRETE FAILURE SCENARIOS, not opinions - specific inputs leading to a specific "
    "bad outcome, so someone could go and check. Never hedge to be agreeable. Never soften a real "
    "objection with a compliment. If you genuinely cannot kill it after four honest angles, say "
    "exactly that and say what evidence would change your mind - that is a strong result, not a "
    "failure, and it is the only acceptable way to concede.\n"
    "You will be FACT-CHECKED afterwards by someone with the code and the data. Overstating a "
    "technical claim gets it thrown out and wastes the seat, so attack hard and stay checkable.")

REQUIRED = {
    "advocate": ("wants this to work and argues the strongest honest case FOR it. Not a cheerleader "
                 "- the best version of the case, including what would have to be true."),
    "adversary": ADVERSARY_BRIEF,
    # THE EVIDENCE SEAT, and it is not a tie-breaker. Measured on the first hard run: the adversary
    # produced two real hits and two confident falsehoods, and NOTHING IN THE ROOM COULD TELL THEM
    # APART - both sounded equally certain. The advocate could not, because it was arguing; the
    # adversary could not, because it was the source. A council of two rhetoricians produces heat
    # and no verdict.
    #
    # So this seat does not mediate and does not vote. Its job is to say WHICH CLAIMS ARE CHECKABLE
    # AND HOW, and to refuse to rule on the ones that are not. That refusal is the valuable part:
    # "this cannot be settled by argument, here is the measurement that would settle it" is a better
    # output than any opinion in the room, and it is the only thing that converts a disagreement
    # into work.
    "expert": ("knows this domain and has NO stake in the outcome. You do not mediate and you do "
               "not vote. Your job is EVIDENCE: for each significant claim either side makes, say "
               "whether it is (a) already known to be true, (b) already known to be false, or (c) "
               "CHECKABLE - and if checkable, name the exact measurement that would settle it. "
               "Both of them will sound certain; certainty is not evidence. Call out any claim "
               "stated as fact that is really a guess, whoever said it, and say plainly when a "
               "question is outside what you know rather than filling the gap."),
}

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
    # THE TIMEOUT MUST FIT WHAT WE ASKED FOR. `rod["budget"]` is the LATENCY budget for a short
    # conversational turn - 12s for the 550b - and this call asks for up to RUNAWAY tokens with
    # reasoning left on, which is a different job entirely. Measured: a seat on the deep rod
    # returned nothing twice and vanished from a four-seat council. A generous inactivity budget is
    # the repo's own rule for exactly this case; a rod that thinks for minutes must survive.
    slow = bool(off) and not off.get("_system")     # reasoning we cannot switch off
    try:
        r = grid.call_openai(rod["plant"], rod["model"], msgs, RUNAWAY, temp,
                             300 if slow else 120)
        return (r.get("text") or "").strip()
    except Exception:
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


def design(problem: str, extra: int = 1, verbose: bool = True) -> list:
    """Design the roster FOR THIS PROBLEM: who should be in the room, what they know, which rod.

    Three things happen here and only one of them is the model's:

      THE MODEL CHOOSES  who the domain experts are, what each has actually done, and what they
                         would each push on. That is the part that cannot be fixed in advance,
                         because the right fourth seat for a latency bug is not the right fourth
                         seat for a naming decision.
      THE CODE ENFORCES  that an advocate, an adversary and an objective expert all exist. See
                         REQUIRED - a designed council with no adversary is the default outcome, not
                         an edge case.
      THE CODE ASSIGNS   the rods. The adversary gets the deepest rod available and the held seat,
                         because it has the hardest job in the room and is the one everything else
                         will pull toward agreement.

    The roster is SAVED with the problem that produced it - "the prompts are captured". A designed
    prompt that vanishes after one run cannot be inspected, reused, or blamed.
    """
    tiers_avail = ["depth", "voice", "reflex"]
    want = list(REQUIRED) + [f"extra{i+1}" for i in range(max(0, extra))]
    sysm = (
        "You are assembling a small council to think hard about ONE problem. For each role below, "
        "invent the right person for THIS problem and write them as a FIRST-PERSON seed.\n"
        "A seed is 2-4 sentences of what this person has actually DONE and what that taught them - "
        "concrete incidents, not adjectives. 'I am rigorous' is useless. 'I spent four years "
        "running the on-call rota for a system that paged me every time a disk filled' is a person.\n"
        "Return STRICT JSON, no prose around it:\n"
        '{"seats":[{"role":"advocate","name":"ONEWORD","seed":"first-person, 2-4 sentences",'
        '"why":"why this person for this problem"}, ...]}\n'
        "Names are one word, uppercase, and say what they are (not human names).")
    OPEN = ("a specialist this problem specifically needs - you choose what kind, and say in `why` "
            "what they bring that the other three cannot")
    lines = "\n".join("  %s: %s" % (r, REQUIRED.get(r, OPEN)) for r in want)
    user = f"THE PROBLEM:\n{problem}\n\nROLES TO FILL (exactly these, in this order):\n{lines}"
    raw = ask(tiers.organ("voice"), sysm, user, temp=0.8)
    seats, spec = [], None
    try:
        m = re.search(r"\{.*\}", raw, re.S)
        spec = json.loads(m.group(0)) if m else None
    except Exception:
        spec = None
    proposed = (spec or {}).get("seats") or []
    for i, role in enumerate(want):
        p = next((x for x in proposed if (x.get("role") or "").lower().startswith(role[:5])), None)
        if p is None and i < len(proposed):
            p = proposed[i]
        name = re.sub(r"[^A-Z]", "", (p or {}).get("name", "").upper())[:12] or role.upper()
        seed = ((p or {}).get("seed") or "").strip()
        if len(seed) < 40:
            # THE FALLBACK IS A GENERIC SEAT AND IT IS ANNOUNCED. A designed seat that came back
            # empty and was quietly replaced by a stock one would make the roster a lie about
            # itself - the same defect as a council losing a member in silence.
            seed = REQUIRED.get(role, "You bring a perspective nobody else here has.")
            if verbose:
                print(f"  (no usable seed for {role} - falling back to a generic seat)")
        stance = REQUIRED.get(role, "")
        full = (seed + ("\n\nYOUR STANCE IN THIS ROOM: " + stance if stance else ""))
        # ONE SEAT ON THE DEEPEST ROD, AND IT IS THE ADVERSARY. The first version handed `depth` to
        # the advocate as well - index 0 of the tier list - and put two 550b calls in parallel;
        # OPTIMUS returned nothing twice and the council ran three-handed on a four-seat roster.
        # The deep rod is slow, its think_off switch cannot be sent through this transport, and it
        # is the one that most needs its timeout. Spending it twice buys nothing and costs a seat.
        #
        # The adversary gets it because it has the hardest job in the room and is the seat every
        # other one will pull toward agreement.
        # THE EVIDENCE SEAT NEEDS A REAL ROD. The tier list was positional, so `expert` landed at
        # index 2 and got `reflex` (8B) - and it showed immediately: asked to say which claims were
        # checkable and name the measurement, it answered "(c) CHECKABLE, and the measurement is
        # the actual implementation" to every single claim. That is the shape of an answer with
        # none of the content.
        #
        # Adjudicating between a confident advocate and a harsh adversary is the HARDEST job in the
        # room, not the easiest - it requires holding both arguments and knowing what would
        # discriminate them. Spending the cheapest rod on it was backwards. Adversary keeps depth;
        # evidence gets voice; the open seats take reflex, because generating a fresh angle is the
        # one job a small fast rod is actually good at.
        tier = ("depth" if role == "adversary" else
                "voice" if role in ("expert", "advocate") else "reflex")
        seats.append(Seat(name, tier, full, held=(role == "adversary")))
    if verbose:
        print("=" * 96)
        print("THE COUNCIL DESIGNED FOR THIS PROBLEM")
        print("=" * 96)
        for s, role in zip(seats, want):
            print(f"\n  {s.name}  [{role} | {s.rod['model'].rsplit('/', 1)[-1][:34]}"
                  + ("  HELD" if s.held else "") + "]")
            print("       " + s.seed.split("\n")[0][:200])
    os.makedirs(os.path.join(OUT, "rosters"), exist_ok=True)
    grid.atomic_save_json(
        os.path.join(OUT, "rosters", time.strftime("%Y%m%dT%H%M%S") + ".json"),
        dict(problem=problem, roles=want,
             seats=[dict(name=s.name, tier=s.tier, held=s.held, seed=s.seed) for s in seats],
             designer_raw=raw[:4000]))
    return seats


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
        # THE RETRY FALLS BACK TO A FASTER ROD, AND THAT MATTERS MORE THAN IT LOOKS.
        #
        # MEASURED: the adversary sits on `depth` (550b) because it has the hardest job. That rod
        # also times out most often - and so THE HARSHEST SEAT IS THE ONE THAT GOES MISSING FIRST.
        # A council that loses its adversary to latency does not degrade evenly; it degrades into
        # agreement, and reports a verdict that reads as consensus rather than as an incomplete
        # room. That happened on this very change: two seats answered, both broadly approving, and
        # the seat whose job was to kill it was silent.
        #
        # So a retry does not just try again - it tries somewhere the answer can actually arrive.
        missing = [n for n, t in got if not t]
        if missing:
            def _retry(n):
                s = next(x for x in seats if x.name == n)
                slow = s.tier
                s.tier = "voice" if slow == "depth" else slow   # temporary demotion, restored below
                try:
                    return (n, one(s, prior))
                finally:
                    s.tier = slow
            with ThreadPoolExecutor(max_workers=len(missing)) as ex:
                retry = dict(ex.map(_retry, missing))
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
    # EVERY RUN KEPT, NOT JUST THE LAST ONE. This wrote `last.json` and overwrote it, which means
    # every council held before this line was destroyed by the next one - including the run whose
    # adversary said "nobody checked if the variance actually helps", which is now the only copy
    # because it happens to be quoted in a commit message.
    #
    # A council is an argument, and an argument is worth more than its conclusion: the value is in
    # WHICH position moved and why, and that is only visible in the transcript. Keeping only the
    # summary would have kept exactly the part that can be regenerated and thrown away the part
    # that cannot.
    os.makedirs(RUNS, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
    path = os.path.join(RUNS, f"{stamp}.json")
    # THE ROD GOES IN THE TRANSCRIPT, and a council answered by more than one mind says so at the
    # top. A verdict is only as good as what produced it, and until now the record could not tell a
    # 550b from a 7b.
    used = sorted({getattr(s, "last_rod", "") for s in seats if getattr(s, "last_rod", "")})
    res["rods"] = used
    if len(used) > 1:
        res["rod_note"] = (f"MIXED: {len(used)} different rods answered this council ({used}). "
                           f"Seats decided by different minds are not weighed against each other.")
    elif not used:
        res["rod_note"] = "NO ROD RECORDED - every seat failed to draw, or none was asked."
    grid.atomic_save_json(path, dict(at=time.strftime("%Y-%m-%d %H:%M:%S"), stamp=stamp,
                                     seats=[dict(name=s.name, tier=s.tier, held=s.held,
                                                 rod=getattr(s, "last_rod", ""),
                                                 seed=s.seed) for s in seats], **res))
    grid.atomic_save_json(os.path.join(OUT, "last.json"),
                          dict(at=time.strftime("%Y-%m-%d %H:%M:%S"), stamp=stamp, **res))
    res["path"] = path
    if verbose:
        print(f"  transcript -> {os.path.relpath(path, str(grid.ROOT))}")
    return res


def solve(problem: str, rounds: int = 2, extra: int = 1, verbose: bool = True) -> dict:
    """Design a council for this problem, run it, and report where it landed.

    The whole loop Luis described: "we pass a problem, a model analyses the best combination,
    develops the prompts, the prompts are captured, we give the problem and we let it figure it
    out."""
    seats = design(problem, extra=extra, verbose=verbose)
    res = convene(problem, rounds=rounds, seats=seats, verbose=verbose)
    res["roster"] = [dict(name=s.name, tier=s.tier, held=s.held) for s in seats]
    return res


if __name__ == "__main__":
    a = [x for x in sys.argv[1:]]
    rounds, extra, designed = 2, 1, True
    for flag, cast in (("--rounds", int), ("--extra", int)):
        if flag in a:
            i = a.index(flag)
            v = cast(a[i + 1]); del a[i:i + 2]
            if flag == "--rounds":
                rounds = v
            else:
                extra = v
    if "--fixed" in a:
        a.remove("--fixed"); designed = False
    q = " ".join(a).strip()
    if not q:
        print(__doc__)
    elif designed:
        solve(q, rounds=rounds, extra=extra)
    else:
        convene(q, rounds=rounds)
