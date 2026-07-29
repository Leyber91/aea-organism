"""party.py - FOUR VOICES IN ONE ROOM, HAVING AN ACTUAL CONVERSATION.

Luis, 2026-07-30, on why the earlier tests were not conversations:

    "before we were doing a series of phrases but we weren't having a conversation, was a list of
    sentences and the other part was actually replying to it. But in this case we need a GUIDE to
    the conversation - but is a guide, not a script - so it carries the replies of the conversation
    as we advance. Kind of when you have a conversation with someone and have different topics, you
    don't just isolate topics, you learn about the person and recall moments of the conversation.
    You create an image of that person in front of you."

That is the whole specification and it names the two things every scripted test gets wrong:

    NOT A SCRIPT     the guide says what the conversation should REACH, never what anyone says.
                     Lines are written live, from the transcript so far. A script produces speakers
                     who talk past each other in the right order, which reads as four monologues
                     interleaved - the exact failure he saw in `--loopback`.

    AN IMAGE OF THE  each speaker keeps a running picture of everyone else, updated as they go, and
    OTHER PERSON     is asked to use it. Without this, topics are isolated: turn 9 shows no sign of
                     having heard turn 3, nobody is ever reminded of anything, and no relationship
                     accumulates. WITH it, a speaker can say "you said earlier you didn't trust it"
                     - which is what makes a conversation feel like one.

THE AUDIO. See `aea/io/mixer.py` for why this is one stream and not four players. Here the
consequences are: renders go out four-at-a-time on a ThreadPoolExecutor (MEASURED 7.26x faster than
sequential - it is a network round trip, so it is genuinely parallel under the GIL), and playback
goes to one mixer bus with a pan position per speaker.

SEPARATION IS NOT DECORATION. Four overlapping voices are unintelligible unless they differ. Each
character gets its own voice, its own pitch and rate offset, and its own place in the stereo field,
because those are the cues a listener uses to pull one talker out of several. The cartoon and the
monster are load-bearing.

    python -m aea.lab.party                 8 turns, polite floor (no overlap)
    python -m aea.lab.party --overlap 0.35  35% of turns start before the last one finishes
    python -m aea.lab.party --turns 14 --topic "whether the machine should be allowed to lie"
    python -m aea.lab.party --mute          no audio, text only - the logic on its own
"""
from __future__ import annotations

import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from aea.kernel import grid
from aea.io import mixer as mx
from aea.io import speak
from aea.mind import tiers
from aea.mind.persona import Persona

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = os.path.join(str(grid.STATE), "lab", "party")


class Character:
    """A speaker: a voice, a place in the room, a way of thinking, a ROD, and a persistent self.

    TWO THINGS MAKE THESE FOUR DIFFERENT, and they are not equally important.

    THE ROD is the cheap one. Each character draws on a different model where one is available
    (8B / 49B / 550B are all wired and measured), which gives genuinely different priors instead of
    one model impersonating four people through prompt instructions. Real, free, and shallow.

    THE PERSISTENT SELF is the one that matters - `aea/mind/persona.py`. What each one remembers,
    what it has come to think of the others, and what it has already committed to out loud. Two
    characters on the SAME model with different memories diverge further than two on different
    models with none, because a model is a capacity to produce text and a self is a constraint on
    which text gets produced.
    """

    def __init__(self, name, voice, pitch="", rate="", pan=0.0, gain=1.0, persona="", tier="voice"):
        self.name, self.voice, self.pitch, self.rate = name, voice, pitch, rate
        self.pan, self.gain, self.persona = pan, gain, persona
        self.tier = tier
        self.self = Persona(name, persona=persona)     # loads from disk if this one has lived before

    @property
    def rod(self) -> dict:
        return tiers.organ(self.tier)

    @property
    def impressions(self) -> dict:
        """Kept as a plain dict view so the reporting code reads the same as before the store
        landed - but it is now backed by disk and survives the process."""
        return {o: v["text"] for o, v in self.self.impressions.items()}

    def render(self, text: str, idx: int) -> str:
        p = os.path.join(OUT, f"_{self.name.lower()}_{idx % 6}.mp3")
        ok = speak.edge_render(text, p, voice=self.voice, rate=self.rate, pitch=self.pitch)
        return p if ok else ""


# THE CAST. Voices confirmed present by asking edge-tts (322 voices, 47 English) rather than
# remembering them, and the pitch/rate offsets confirmed to move the audio - duration went 2.57s ->
# 1.78s (cartoon) and -> 3.29s (monster) on the same sentence.
#
# Pan positions are spread deliberately: two voices at the same position are the hardest case for a
# listener, so nobody shares a seat. Gain is trimmed by character because a high fast voice reads as
# louder than a low slow one at equal amplitude.
#
# THE TIER ASSIGNMENT IS NOT DECORATION EITHER. A 550B rod that speaks rarely and briefly costs
# almost nothing per conversation, so GRAVE - who by design says one flat sentence and stops - is
# the right place to spend the slowest model. PIP is fast and impulsive and gets the 8B, which is
# the fastest rod measured (ttfb 0.456s) and whose shallower priors read as exactly that.
CAST = [
    Character("PIP", "en-US-AnaNeural", pitch="+55Hz", rate="+22%", pan=-0.75, gain=0.85,
              tier="reflex",
              persona="Cartoonish and fast. Excitable, jumps to conclusions, asks the naive "
                      "question nobody else will ask, and is often accidentally right. Short "
                      "sentences. Enthusiastic but not stupid."),
    Character("GRAVE", "en-GB-ThomasNeural", pitch="-45Hz", rate="-16%", pan=0.75, gain=1.15,
              tier="depth",
              persona="A deep, slow, monstrous voice. Speaks rarely and briefly, and when it does "
                      "it is the flat uncomfortable truth nobody wanted said. Never cruel. Dry."),
    Character("MIRA", "en-GB-SoniaNeural", pitch="+0Hz", rate="+0%", pan=-0.25, gain=1.0,
              tier="voice",
              persona="Careful and precise. Asks for evidence, notices when someone has moved the "
                      "goalposts, and summarises what has actually been agreed. The one who keeps "
                      "the conversation honest."),
    Character("REN", "en-US-ChristopherNeural", pitch="-10Hz", rate="+6%", pan=0.25, gain=1.0,
              tier="voice",
              persona="Warm, curious, tells short stories to make a point, and pulls the others "
                      "back to what they said earlier. Disagrees by asking a better question."),
]

# THE GUIDE. Not lines - PLACES THE CONVERSATION SHOULD REACH. It advances when the group has
# genuinely got there, and a speaker is nudged toward the next one only if the talk has stalled.
# Nobody is ever handed a sentence.
GUIDE = [
    "get to know each other a little - who is who, what each of them is like",
    "someone brings up a machine that can talk, and what that would actually mean",
    "disagreement: is a machine that sounds like it understands actually understanding",
    "someone recalls something another said EARLIER and uses it against them, or for them",
    "what would convince each of them, concretely - name a test",
    "land somewhere: what they now think, and what they still disagree about",
]


# The model talking ABOUT the task instead of doing it. Every pattern here was emitted verbatim by
# a rod in a real run; the list is a corpus, not an imagination (law M8).
_META = re.compile(
    r"(?:^|(?<=[.!?]\s))\s*(?:the user (?:is |has )?ask(?:s|ing|ed)?|let me (?:analyz|think|"
    r"consider|break)|i (?:need|should|will|am going) to (?:continue|respond|analyz|reply|stay)|"
    r"as (?:the character |)\w+[,:]? i (?:should|need|will)|here(?:'s| is) (?:my|the) "
    r"(?:line|reply|response) as \w+|okay,? (?:so )?(?:i|let)'?s?\b[^.!?\n]{0,40}(?:in character|"
    r"as \w+ would))[^.!?\n]{0,120}[.:!?]?",
    re.I)

# A private impression that came back as its own label and nothing else. The model echoed the
# instruction instead of answering it, and an empty impression stored as text is worse than no
# impression: it occupies the slot and stops it being rebuilt.
_EMPTY_IMPRESSION = re.compile(r"^\s*(?:private\s+)?impression(?:\s+of\s+\w+)?\s*:?\s*$", re.I)


def _render_and_load(who: Character, line: str, idx: int) -> tuple:
    """Network render AND mp3 decode, both on a worker thread. Returns (float32 mono, sr).

    Kept as one unit deliberately: splitting them put the decode back on whichever thread called
    `play_file`, which in the party is the main thread, which is the thread the audio callback is
    competing with for the GIL."""
    import soundfile as sf
    p = who.render(line, idx)
    if not p:
        return (None, 0)
    x, sr = sf.read(p, dtype="float32")
    if getattr(x, "ndim", 1) > 1:
        x = x.mean(axis=1)
    return (x, sr)


def transcript_text(turns: list, last: int = 24) -> str:
    return "\n".join(f"{t['who']}: {t['text']}" for t in turns[-last:])


def update_impression(me: Character, other: str, turns: list, rod: dict) -> str:
    """Rebuild ME's picture of OTHER from what has actually been said.

    Luis: "you learn about the person and recall moments of the conversation. You create an image
    of that person in front of you." This is that, literally - and it is REBUILT from the
    transcript rather than appended to, so a first impression that turned out wrong can be
    corrected the way a real one is."""
    said = [t["text"] for t in turns if t["who"] == other]
    # WHAT THEY SAID IN EARLIER SESSIONS COUNTS TOO. Without this the impression is rebuilt from
    # today's transcript alone and a relationship can never be older than one conversation, which
    # is the amnesia this whole store exists to end.
    past = [m["text"] for m in me.self.memories if m.get("about") == other][-6:]
    if len(said) + len(past) < 2:
        return me.self.impression_of(other)
    said = past + said
    try:
        r = grid.call_openai(
            rod["plant"], rod["model"],
            [{"role": "system", "content":
              f"You are {me.name}. {me.persona}\nYou have been talking with {other}. In ONE short "
              f"sentence, say what you have come to think of them - their manner, what they care "
              f"about, and anything they said that stuck with you. Write it as a private "
              f"impression, not as speech. No preamble."},
             {"role": "user", "content": f"Things {other} has said:\n" + "\n".join(f"- {s}" for s in said[-6:])}],
            70, 0.7, 30)
        imp = (r.get("text") or "").strip().split("\n")[0]
        imp = re.sub(r"^\s*(?:private\s+)?impression(?:\s+of\s+\w+)?\s*:\s*", "", imp, flags=re.I)
        # STAGE DIRECTIONS GET INTO THE STORE TOO. Measured: an impression came back as
        # "*pauses, observing GRAVE* Their manner is a slow, deliberate storm cloud..." - the model
        # performing the act of forming an impression. Harmless in a transcript, but this text is
        # injected into a prompt every future turn, so the performance would compound.
        imp = re.sub(r"\*[^*]{0,60}\*", " ", imp).strip()
        if imp and not _EMPTY_IMPRESSION.match(imp) and len(imp) > 12:
            me.self.set_impression(other, imp)
    except Exception:
        pass
    return me.self.impression_of(other)


def next_line(me: Character, turns: list, goal: str, rod: dict, addressed: str = "") -> str:
    """Write what ME says next. From the conversation, never from a script."""
    others = [c.name for c in CAST if c.name != me.name]
    # EVERYTHING THIS SPEAKER BRINGS TO THE TURN, from its own store: what it thinks of the others,
    # what it has already committed to, and the few older memories worth reaching for. Keyed on the
    # last thing said, so retrieval is about THIS moment rather than a dump of the whole record.
    recent = turns[-1]["text"] if turns else goal
    brief = me.self.brief(others, query=recent)
    sys_p = (
        f"You are {me.name}, one of four people talking OUT LOUD in a room.\n"
        f"WHO YOU ARE: {me.persona}\n"
        f"THE OTHERS: {', '.join(others)}\n"
        + (brief + "\n" if brief else "")
        + f"WHERE THE CONVERSATION IS TRYING TO GET: {goal}\n"
        "That is a DIRECTION, not a script. Do not announce it, do not summarise it, and do not "
        "force it - get there the way a real conversation does, or stay where you are if that is "
        "more honest.\n"
        "HOW TO SPEAK: one or two sentences, out loud, as this character. React to what was just "
        "said. Use their names occasionally, not every time. When it fits, REFER BACK to something "
        "someone said earlier in this conversation - that is what makes it a conversation and not "
        "a list of topics. NEVER repeat back what was just said - if you agree, say what it makes "
        "you think; if you are asking the same thing, ask a sharper version of it. Do not claim "
        "someone said something they did not say. Never stage directions, never asterisks, never "
        "quote marks around your line, never say your own name first. Just the words you say."
        + (f"\n{addressed} just spoke to you directly - answer them." if addressed else ""))
    try:
        r = grid.call_openai(rod["plant"], rod["model"],
                             [{"role": "system", "content": sys_p},
                              {"role": "user", "content": transcript_text(turns) +
                               f"\n\n{me.name}:"}],
                             110, 0.95, 40)
        t = (r.get("text") or "").strip()
    except Exception:
        return ""
    t = re.sub(r"<think>.*?</think>", " ", t, flags=re.S | re.I)
    t = re.sub(r"^\s*%s\s*:\s*" % re.escape(me.name), "", t, flags=re.I)
    # META-REASONING LEAK. MEASURED on the first persistent run, from the 550B rod, SPOKEN as
    # GRAVE's line and then stored by `commit()` as a belief GRAVE now holds:
    #     "The user is asking me to continue the conversation as GRAVE. Let me analyze the
    #      situation:"
    # A reasoning rod writes its scratchpad as ordinary prose when there is no <think> tag, and
    # this is worse than the same leak in converse: there it would be said once and forgotten,
    # here it enters a PERSISTENT store as something the character believes and will be held to
    # for every future session. A persistent memory raises the cost of every unguarded output,
    # which is the price of persistence and has to be paid at the door.
    t = _META.sub(" ", t).strip()
    t = re.sub(r"[*_#`]+", "", t).strip().strip('"').strip()
    t = " ".join(t.split("\n")[0:2]).strip()
    # CUT AT A SENTENCE, NEVER AT A CHARACTER. A hard [:320] ended a turn on "are actually com",
    # which is not a short reply - it is a broken one, and spoken aloud it sounds like the speaker
    # was cut off. Same rule as `trim` in converse: better unsaid than half-said.
    if len(t) > 320:
        cut = max(t.rfind(". ", 0, 320), t.rfind("? ", 0, 320), t.rfind("! ", 0, 320))
        t = t[:cut + 1] if cut > 60 else t[:320].rsplit(" ", 1)[0]
    # PARROTING. Measured on the first muted run: PIP answered MIRA by repeating MIRA's question
    # back almost word for word. A model handed a transcript and told to "react" will sometimes
    # react by echoing, and an echo reads as the most broken thing a group conversation can do -
    # it is the moment a listener stops believing anyone is listening.
    if turns:
        prev = set(re.findall(r"[a-z']{4,}", turns[-1]["text"].lower()))
        mine = set(re.findall(r"[a-z']{4,}", t.lower()))
        if prev and mine and len(prev & mine) / len(mine) > 0.75:
            return ""
    return t


def pick_speaker(turns: list, last: str) -> tuple:
    """FLOOR CONTROL - who talks next, and are they answering someone.

    The simplest policy that is not round-robin, which is the tell of a fake group: if the last
    line named somebody, that person has been SELECTED and answers (current-speaker-selects-next,
    the strongest rule in the conversation-analysis account). Otherwise somebody self-selects, and
    whoever has been quiet longest is likeliest - a crude stand-in for the fact that people who
    have not spoken are under more pressure to.
    """
    if turns:
        txt = turns[-1]["text"]
        for c in CAST:
            if c.name != last and re.search(rf"\b{c.name}\b", txt, re.I):
                return c, turns[-1]["who"]
    spoke_at = {c.name: -1 for c in CAST}
    for i, t in enumerate(turns):
        spoke_at[t["who"]] = i
    cands = [c for c in CAST if c.name != last]
    cands.sort(key=lambda c: spoke_at[c.name])
    # Weights must be built FROM the candidate list, never from a fixed literal: on turn one
    # nobody has spoken, so `last` is empty and all four are candidates against a three-long
    # constant. Quietest first, and the tail decays so the group does not become a round-robin -
    # which is the tell of a fake conversation.
    weights = [max(1, 2 ** (len(cands) - 1 - i)) for i in range(len(cands))]
    return random.choices(cands, weights=weights, k=1)[0], ""


def run(turns_wanted: int = 8, overlap: float = 0.0, topic: str = "", mute: bool = False,
        device=None, seed: int = 7) -> dict:
    random.seed(seed)
    os.makedirs(OUT, exist_ok=True)
    rod = tiers.organ("reflex")
    guide = list(GUIDE)
    if topic:
        guide.insert(2, topic)
    bus = None if mute else mx.Mixer(device=device).start()
    pool = ThreadPoolExecutor(max_workers=4)
    for c in CAST:
        c.self.open_session()

    print("=" * 98)
    print(f"THE PARTY - {len(CAST)} voices, one room, one sound card"
          + ("  [MUTED - logic only]" if mute else ""))
    for c in CAST:
        s = c.self.stats()
        print(f"  {c.name:6s} {c.rod['model'].rsplit('/', 1)[-1][:26]:26s} pan {c.pan:+.2f}  "
              f"pitch {c.pitch or '-':>6s}  session #{s['sessions']}  "
              f"{s['memories']} memories, {s['commitments']} commitments, knows {s['impressions']}")
    print(f"  floor: {'overlap %d%% of turns' % (overlap*100) if overlap else 'polite - one at a time'}")
    print("=" * 98)

    turns: list = []
    last = ""
    stage, said_in_stage = 0, 0
    pending = None                      # the previous speaker's audio, still sounding
    t_start = time.time()

    for n in range(turns_wanted):
        goal = guide[min(stage, len(guide) - 1)]
        who, addressed = pick_speaker(turns, last)
        # REBUILD THE IMAGE before speaking, every few turns - this is what lets turn 9 remember
        # turn 3. Done on the fast rod and off the critical path of the audio.
        # EVERY speaker builds an image, not only the ones who happen to land on an even turn.
        # The first version updated impressions for `who` on n % 2, and two of four characters
        # finished the conversation having formed no picture of anyone - which is exactly the
        # isolated-topics failure this whole mode exists to prevent, reintroduced by a scheduling
        # convenience.
        if n >= 2:
            for c in CAST:
                for o in [x.name for x in CAST if x.name != c.name]:
                    if o not in c.impressions or n % 3 == 0:
                        update_impression(c, o, turns, rod)
        line = next_line(who, turns, goal, who.rod, addressed)
        if not line:
            continue
        turns.append(dict(who=who.name, text=line))
        # THE ASYMMETRY THAT MAKES THEM SEPARATE. The speaker records this as something IT SAID and
        # is bound by; the other three record it as something they HEARD FROM someone. Same line,
        # four different memories, and only one of them is a commitment. A shared log would make
        # this one mind with four voices, which is the trick we are trying to stop doing.
        who.self.remember(line, kind="said")
        who.self.commit(line)
        for c in CAST:
            if c.name != who.name:
                c.self.remember(line, kind="heard", about=who.name)
        last = who.name
        said_in_stage += 1
        if said_in_stage >= max(2, turns_wanted // len(guide)) and stage < len(guide) - 1:
            stage, said_in_stage = stage + 1, 0

        mark = f" -> {addressed}" if addressed else ""
        print(f"\n  [{n+1:02d}] {who.name}{mark}")
        print(f"       {line}")

        if mute:
            continue
        # RENDER **AND DECODE** OFF THE MAIN THREAD. Both, not just the render - the first version
        # rendered in the pool and then called `play_file`, which does the mp3 decode on whatever
        # thread asked. That decode is CPU work holding the GIL while the audio callback needs it,
        # and it is part of why the bus lost 6% of its frames. Everything expensive now happens on
        # a worker and the bus receives a finished float array.
        fut = pool.submit(_render_and_load, who, line, n)
        try:
            samples, srate = fut.result(timeout=90)
        except Exception:
            samples, srate = None, 0
        if samples is None:
            print("       (render failed)")
            continue
        # THE OVERLAP DECISION. With `overlap`, this voice starts while the previous one is still
        # sounding - which is the thing the mixer exists for and the thing a single sd.play() can
        # never do. Without it, we wait, which is the polite floor.
        if pending is not None and (overlap <= 0 or random.random() > overlap):
            bus.wait(pending, timeout=60)
        elif pending is not None:
            time.sleep(0.35)            # a real interruption lands mid-phrase, not at a boundary
            print(f"       (over {turns[-2]['who']})")
        pending = bus.play(samples, srate, gain=who.gain, pan=who.pan, name=who.name)

    if not mute:
        bus.wait(timeout=90)
        h = bus.health()
        # THE HEALTH LINE REPORTS THE RATIO, NOT THE FLAG. `output_underflow` was measured reading
        # 0 while half the callbacks never happened, so a bus that lost half its audio would have
        # printed "underruns 0" and been believed. Frames written against the wall clock cannot
        # lie the same way.
        print(f"\n  bus: realtime {h['realtime']:.4f} "
              f"{'(kept up)' if h['ok'] else '(FELL BEHIND - audio is missing)'}"
              f"   peak {h['peak']:.3f}   underflow flags {h['flags']} (advisory only)")
        bus.stop()
    pool.shutdown(wait=False)

    # SAVE, and this is the line that separates an entity from a costume. Everything above is a
    # performance until it survives the process exiting.
    for c in CAST:
        c.self.save()

    print("\n" + "=" * 98)
    print("WHAT EACH ONE IS TAKING WITH IT - persisted to state/personas/, survives this process")
    print("=" * 98)
    for c in CAST:
        s = c.self.stats()
        print(f"  {c.name}  ({s['memories']} memories, {s['commitments']} commitments)")
        for o, imp in c.impressions.items():
            print(f"     of {o:6s} {imp[:92]}")
        for cm in c.self.commitments[-2:]:
            print(f"     said   {cm['claim'][:92]}")
    # DID IT ACTUALLY CARRY? The measurable difference between a conversation and a list: do later
    # turns name earlier speakers, and do they reuse earlier content words.
    names = {c.name for c in CAST}
    callbacks = sum(1 for t in turns[3:] if any(re.search(rf"\b{o}\b", t["text"], re.I)
                                                for o in names - {t["who"]}))
    early = set(re.findall(r"[a-z]{5,}", " ".join(t["text"].lower() for t in turns[:3])))
    late = [t for t in turns[len(turns)//2:]]
    recalls = sum(1 for t in late if len(early & set(re.findall(r"[a-z]{5,}", t["text"].lower()))) >= 2)
    print(f"\n  turns {len(turns)}   wall {time.time()-t_start:.0f}s")
    print(f"  addressed each other by name : {callbacks}/{max(len(turns)-3,1)} of later turns")
    print(f"  reused earlier content       : {recalls}/{max(len(late),1)} of second-half turns")
    print(f"  distinct speakers            : {len({t['who'] for t in turns})}/{len(CAST)}")
    res = dict(turns=turns, callbacks=callbacks, recalls=recalls,
               impressions={c.name: c.impressions for c in CAST})
    grid.atomic_save_json(os.path.join(OUT, "party.json"),
                          dict(at=time.strftime("%Y-%m-%d %H:%M:%S"), **res))
    return res


if __name__ == "__main__":
    a = sys.argv[1:]

    def arg(f, d=None):
        return a[a.index(f) + 1] if f in a and a.index(f) + 1 < len(a) else d

    run(turns_wanted=int(arg("--turns", 8)), overlap=float(arg("--overlap", 0.0)),
        topic=arg("--topic", "") or "", mute="--mute" in a,
        device=(int(arg("--device")) if arg("--device") else None))
