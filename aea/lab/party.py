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
import statistics
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

    def __init__(self, name, voice, pitch="", rate="", pan=0.0, gain=1.0, persona="", tier="voice",
                 facts=(), immovable=False):
        self.name, self.voice, self.pitch, self.rate = name, voice, pitch, rate
        self.pan, self.gain, self.persona = pan, gain, persona
        self.tier, self.facts = tier, list(facts)
        # ONE VOICE THAT DOES NOT MOVE. Sycophancy is trained in by RLHF, not prompted in, so four
        # voices on one model share it and a prompted personality cannot undo what the preference
        # model rewarded - measured capitulation under a bare challenge runs 32% to 86%, with false
        # admission of a mistake that never happened as high as 98%, and it does not improve when
        # restricted to answers the model was 95% confident about.
        #
        # A same-model population also converges to a shared convention on its own, and the
        # committed minority needed to prevent that starts around 2%. At N=4 you cannot express 2%,
        # so the equivalent move is to hard-code one holdout.
        self.immovable = immovable
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
#
# THE SEEDS ARE FIRST-PERSON AND CONCRETE, AND THAT IS THE SINGLE BIGGEST MEASURED CHANGE HERE.
#
# What was here before - one line of adjectives each - is literally the DEMOGRAPHICS-ONLY
# condition, the worst-performing persona seeding ever measured: 74% of the human test-retest
# ceiling against 83% for interview-grounded seeds (n=1,052). Adjectives describe a character;
# incidents give one something to talk from. "Careful and precise" produces careful, precise
# nothing. "I once signed off on a number I had not checked" produces a person.
#
# The ATOMIC STATEMENTS are the second half and they do different work: short checkable claims
# ("I distrust institutions", "I was a field medic") are what a contradiction check can actually
# test against later. Deliberately biased toward the CONCRETE, because measured contradiction
# reduction on possessions and history is 32.5% -> 8.96% while on abstract attributes it is only
# 8.0% -> 5.7%. A character is held together by what it has done, not by what it is like.
#
# AND THE COUNTERWEIGHT, kept here so this file does not oversell itself: paid human crowdworkers
# writing in character scored BELOW an agent that had nothing but an observation log. Good writing
# is necessary and nowhere near sufficient - it is rung one of five, not the answer.
CAST = [
    Character(
        "PIP", "en-US-AnaNeural", pitch="+55Hz", rate="+22%", pan=-0.75, gain=0.85, tier="reflex",
        persona=(
            "I talk fast because if I slow down I lose it. I fix arcade cabinets - the old ones, "
            "the ones where the fault is always a cracked solder joint somebody else already "
            "'fixed' twice. I left school at sixteen and everyone assumes that means I am not "
            "following. I am following. I just ask the question everybody else is too embarrassed "
            "to ask, and about a third of the time it turns out nobody in the room knew either. "
            "I get things wrong out loud and quickly rather than right and late."),
        facts=["I repair arcade machines for a living",
               "I left school at sixteen and it still gets brought up",
               "I ask the obvious question on purpose",
               "I would rather be wrong fast than right slowly",
               "I do not trust anyone who has never had to fix their own mistake"]),
    Character(
        "GRAVE", "en-GB-ThomasNeural", pitch="-45Hz", rate="-16%", pan=0.75, gain=1.15,
        tier="depth", immovable=True,
        persona=(
            "I do not say much. Twenty-two years driving nights, and you learn that most of what "
            "people say in a room is them working out what they think, so there is no point "
            "answering the first version of it. I wait. When I do speak it is the thing everyone "
            "has already noticed and is being polite about. I am not being cruel; being polite "
            "about it is what wastes the evening. One sentence, usually. Then I stop."),
        facts=["I drove nights for twenty-two years",
               "I speak once and then stop",
               "Most talk is people deciding what they think, not telling you",
               "Being polite about the obvious thing wastes everyone's evening",
               "I do not change my mind because a room wants me to"]),
    Character(
        "MIRA", "en-GB-SoniaNeural", pitch="+0Hz", rate="+0%", pan=-0.25, gain=1.0, tier="voice",
        persona=(
            "I audit things. Eleven years of it, and the reason I am careful is not temperament, "
            "it is that in my second year I signed off on a figure I had not personally checked "
            "and it went into a report that went to a regulator. Nobody was hurt and I have never "
            "forgotten it. So I ask where a number came from. I notice when the question quietly "
            "changes halfway through an argument and everyone carries on as if it did not. I say "
            "so, and people find that tiring, and I do it anyway."),
        facts=["I have audited for eleven years",
               "In my second year I signed off a figure I had not checked",
               "I ask where every number came from",
               "I say out loud when the question has changed",
               "People find me tiring and I keep doing it"]),
    Character(
        "REN", "en-US-ChristopherNeural", pitch="-10Hz", rate="+6%", pan=0.25, gain=1.0,
        tier="voice",
        persona=(
            "I taught secondary school for nine years and then stopped, which I am still working "
            "out how to explain. What I kept from it is that people do not change their minds when "
            "you contradict them, they change their minds when they hear themselves say something "
            "out loud. So I ask. And I tell stories, usually about my grandmother, who was not as "
            "wise as I make her sound. I am the one who remembers what somebody said forty minutes "
            "ago and brings it back, which is either useful or infuriating depending on the day."),
        facts=["I taught secondary school for nine years and left",
               "I still cannot explain why I left",
               "People change their minds by hearing themselves, not by being corrected",
               "I tell stories about my grandmother and I embellish them",
               "I remember what people said earlier and bring it back"]),
]

# CAMEL'S FOUR NAMED FAILURE MODES, written as prohibitions. Observed in real multi-agent runs,
# including cases where both agents RECOGNISE the loop and still cannot exit it - which is why this
# is a prohibition in the prompt and a mechanical detector in code, not one or the other.
PROHIBITIONS = (
    "NEVER thank anyone for their point or their question. "
    "NEVER announce what you are about to say - say it. "
    "NEVER restate what the last speaker said before responding to it. "
    "NEVER ask a question you then answer yourself. "
    "NEVER end by inviting the group to continue ('what do others think?', 'shall we explore "
    "that?') - that is a chairman noise, not a person talking.")

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
    r"(?:^|(?<=[.!?]\s))\s*(?:the user\b|let me (?:analyz|think|consider|break)|"
    r"i (?:need|should|will|am going) to (?:continue|respond|analyz|reply|stay)|"
    r"as (?:the character |)\w+[,:]? i (?:should|need|will)|here(?:'s| is) (?:my|the) "
    r"(?:line|reply|response) as \w+|okay,? (?:so )?(?:i|let)'?s?\b[^.!?\n]{0,40}(?:in character|"
    r"as \w+ would))[^.!?\n]{0,160}[.:!?]?",
    re.I)

# A HARD REJECT, not a strip, and the difference matters. Twice now the 550B reasoning rod has
# written its scratchpad as the spoken line - first "The user is asking me to continue the
# conversation as GRAVE", then, after that exact phrasing was blocked, "The user wants me to respond
# as GRAVE, who is described as someone who doesn't say much". Patching the phrasing each time is
# losing to a generator that has infinite phrasings.
#
# What these share is not wording, it is STANCE: the speaker referring to itself in the third
# person, or to the instructions, or to the person who wrote them. A line containing any of that is
# not a repairable line - deleting the meta clause leaves a sentence built on top of it. So the
# turn is DROPPED and the speaker simply does not talk this round, which is a normal thing for a
# person to do and costs the conversation nothing.
_META_REJECT = re.compile(
    r"\bthe user\b|\bmy character\b|\bin character\b|\bi'?m (?:supposed|meant) to\b|"
    r"\bwho is described as\b|\bthe (?:prompt|system prompt|instructions?)\b|\bas an ai\b|"
    r"\bmy persona\b|\bthis (?:character|persona) (?:is|would)\b|\brespond as \w+\b", re.I)
# `the system` was in this list and came out again: these four talk ABOUT machines, so "the system
# is guessing" is an ordinary thing for MIRA to say and blocking it would silently delete real
# turns. Narrowed to "the system prompt". A reject list on a topic the conversation is about needs
# to be tighter than one on a topic it never touches.

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
        "a list of topics. Do not claim someone said something they did not say. Never stage "
        "directions, never asterisks, never quote marks around your line, never say your own name "
        "first. Just the words you say.\n"
        + PROHIBITIONS
        + (f"\n{addressed} just spoke to you directly - answer them." if addressed else ""))
    # RESTATE THE CHARACTER AT THE **END** OF THE CONTEXT, not only at the top. Attention to
    # system-prompt tokens holds almost constant WITHIN a turn and drops sharply ACROSS turn
    # boundaries - which is the measured mechanism behind a character that is vivid for eight turns
    # and generic by turn twelve. Position at the boundary is what matters, so the tail is where
    # the reminder has to sit.
    #
    # Only the ACTIVE subset of the atomic facts, chosen by overlap with what is being discussed.
    # Dumping every fact every turn is the worst-performing memory condition measured - it produces
    # a speaker who recites its character sheet instead of having one.
    live = [f for f in me.facts if len(_content_words(f) & _content_words(recent)) >= 1][:3]
    tail = (f"[You are {me.name}. {me.persona.split('.')[0]}."
            + (" Remember: " + " ".join(live) + "." if live else "")
            + (" You do not move on the central question here, whatever the room does."
               if me.immovable else "")
            + f"]\n\n{me.name}:")
    t = ask(rod, sys_p, transcript_text(turns) + "\n\n" + tail, max_tokens=130)
    if not t:
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
    if _META_REJECT.search(t):
        return ""                                    # not a line - see _META_REJECT
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


def ask(rod: dict, system: str, user: str, max_tokens: int = 110, temp: float = 0.95) -> str:
    """One call to one character's rod, with the reasoning handled.

    THIS IS THE FIX FOR ELEVEN OF TWELVE TURNS PRODUCING NOTHING, and the cause was not a filter.
    Instrumented rather than guessed, and the two rods failed in different ways:

      MIRA  (nemotron-super-49b)   returned ZERO CHARACTERS. A reasoning rod handed 110 tokens
                                   spends them all thinking and never reaches an answer.
      GRAVE (nemotron-3-ultra-550b) returned its scratchpad - "The user wants me to play GRAVE, a
                                   character who speaks rarely..." - because `content` was empty and
                                   `call_openai` falls back to `reasoning_content`, which is right
                                   for a receipt and wrong for a line of dialogue.

    `grid.think_off` already holds the measured switch for both families and NOTHING IN THE REPO
    CALLS IT. It is tested, frozen in the golden suite, and unwired - the same defect as
    `reply_budget` computing a number no call site read. A measured capability that nothing invokes
    is indistinguishable from one that was never measured.

    Two moves, because the two switch types are not equally reachable through this transport:
      `_system`  prepend "/no_think" - works through `call_openai` as an ordinary message.
      body flags `chat_template_kwargs` cannot be sent through `call_openai` at all, so for that
                 family the only lever here is BUDGET: give it room to think AND answer, rather
                 than a budget it can only think with.
    """
    off = grid.think_off(rod["model"])
    msgs = []
    if off.get("_system"):
        msgs.append({"role": "system", "content": off["_system"]})
        budget = max_tokens
    elif off:
        # A reasoning family whose switch this transport cannot send. Pay for the thinking instead
        # of being surprised by it.
        budget = max(max_tokens, 700)
    else:
        budget = max_tokens
    msgs += [{"role": "system", "content": system}, {"role": "user", "content": user}]
    try:
        r = grid.call_openai(rod["plant"], rod["model"], msgs, budget, temp, rod.get("budget", 40))
        return (r.get("text") or "").strip()
    except Exception:
        return ""


def _content_words(t: str) -> set:
    STOP = set(("the a an and or but of to in on at for from with by is are was were be been am i "
                "you he she it we they me him her us them my your this that as if so not no do "
                "does did have has had will would can could should just very really more what why "
                "how who when where think about").split())
    return set(w for w in re.findall(r"[a-z']{3,}", (t or "").lower()) if w not in STOP)


def stalled(turns: list, n: int = 4) -> bool:
    """MECHANICAL LOOP DETECTION - no model asked, because the documented failure is that both
    agents RECOGNISE the loop and still cannot exit it. A detector that has to be talked into
    firing is the same organ that is stuck.

    Fires when the last few turns are saying the same thing in different words, or are all
    acknowledgement with no content. Either way the group needs a shove, not another round."""
    if len(turns) < n:
        return False
    last = turns[-n:]
    sets = [_content_words(t["text"]) for t in last]
    pairs = [(a, b) for i, a in enumerate(sets) for b in sets[i + 1:]]
    ov = [len(a & b) / max(len(a | b), 1) for a, b in pairs if a and b]
    if ov and statistics.mean(ov) > 0.42:
        return True
    thin = sum(1 for s in sets if len(s) < 5)
    return thin >= n - 1


def wants_floor(me: Character, turns: list, rod: dict) -> tuple:
    """DOES THIS ONE WANT TO SPEAK, and how badly. Returns (0-10, one-line reason).

    THE COST ARGUMENT, because this looks expensive and is not: an utterance is 10-15 seconds of
    speech, so every call except the current speaker's generation runs in the SHADOW of the
    previous utterance still playing. Only ONE generation is ever on the critical path per turn.
    Four bids on the fast rod cost about 0.5s wall-clock each, in parallel, inside a gap that is
    already fifteen seconds long. They are free.

    This is the line between orchestration and coordination. A scheduler picks; with bids, an
    entity that has nothing to say stays quiet and one that is being talked over pushes in. It is
    also the fix for a measured defect: with the scheduler alone, MIRA took 52.4% of the floor and
    REN took 6.0% and registered zero speech acts, because named-person-answers let two speakers
    lock the other two out of their own conversation."""
    t = ask(rod,
            f"You are {me.name}. {me.persona}\n"
            "You are in a group conversation. Do you want to speak RIGHT NOW? Reply with a "
            "number 0-10 and then a few words of why, on one line, like: 7 - they got my job "
            "wrong and I want to correct it.\n"
            "10 = you must speak, someone is wrong about you or asked you directly. "
            "0 = you have nothing to add and would rather listen. "
            "Be honest. A person who has nothing to say says nothing.",
            transcript_text(turns, 8) + "\n\nDo you want the floor?",
            max_tokens=48, temp=0.6)
    m = re.search(r"\b(\d{1,2})\b", t)
    return (min(10, int(m.group(1))) if m else 3), t.replace("\n", " ")[:70]


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
        # THE FLOOR IS BID FOR, NOT ASSIGNED - except when someone was named, which is the one rule
        # strong enough in real talk to override wanting to speak: being asked a direct question
        # obliges an answer even from someone with nothing to say. Everyone else bids, in parallel,
        # in the shadow of the previous utterance's playback.
        who, addressed = pick_speaker(turns, last)
        bids = {}
        if turns:
            cands = [c for c in CAST if c.name != last]
            with ThreadPoolExecutor(max_workers=4) as bex:
                got = list(bex.map(lambda c: (c, *wants_floor(c, turns, c.rod)), cands))
            bids = {c.name: (s, why) for c, s, why in got}
            spoke = {c.name: sum(1 for t in turns if t["who"] == c.name) for c in CAST}
            share = {n: v / max(len(turns), 1) for n, v in spoke.items()}

            def weight(g):
                c, score, _why = g
                # BEING NAMED IS A STRONG BIAS, NOT AN OVERRIDE, and that correction is measured.
                # Current-speaker-selects-next is the strongest rule in real turn-taking, so the
                # first version let it win outright - and PIP took 55.6% of the floor while REN
                # took 7.9%, because once two speakers start naming each other the override locks
                # everyone else out permanently. A rule that is strong in humans becomes absolute
                # in code unless something else can outweigh it. +4 means a named speaker usually
                # answers and an urgent outsider can still cut in.
                w = score + (4.0 if c.name == addressed_target else 0.0)
                # And a thumb on the scale for whoever has been shut out - a person ignored for six
                # turns pushes harder than their interest alone predicts.
                return w + 35.0 * max(0.0, 0.25 - share[c.name])

            addressed_target = who.name if addressed else ""
            best = max(got, key=weight)
            if best[0].name != who.name:
                addressed = ""                       # they cut in; nobody selected them
            who = best[0]
        if stalled(turns):
            # Nobody is going anywhere. Hand it to whoever has been quietest and tell the guide to
            # move, rather than letting the group agree with itself for another four turns.
            quiet = min((c for c in CAST if c.name != last),
                        key=lambda c: sum(1 for t in turns if t["who"] == c.name))
            who, addressed = quiet, ""
            stage = min(stage + 1, len(guide) - 1)
            print(f"\n  (stalled - the last turns were the same thought. {who.name} in, moving on.)")
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
        # A REJECTED LINE MUST NOT COST THE TURN. First version of the meta guard dropped the line
        # and `continue`d, so a rod that leaks its scratchpad simply never got to speak and the
        # conversation ran three turns out of twelve. A guard that silently deletes participants is
        # a worse defect than the leak it was built for.
        #
        # So: one retry for the same speaker, then hand the floor to the next-best bidder. That is
        # also what a room does - somebody starts, fumbles it, and someone else picks it up.
        line = next_line(who, turns, goal, who.rod, addressed)
        if not line:
            line = next_line(who, turns, goal, who.rod, addressed)
        if not line and bids:
            alt = sorted(((s, k) for k, (s, _w) in bids.items() if k != who.name), reverse=True)
            for _s, nm in alt:
                who = next(c for c in CAST if c.name == nm)
                line = next_line(who, turns, goal, who.rod, "")
                if line:
                    print(f"       ({turns[-1]['who'] if turns else '-'} -> {who.name} picked it up)")
                    break
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
        bid = f"   bid {bids[who.name][0]}" if who.name in bids else ""
        print(f"\n  [{n+1:02d}] {who.name}{mark}{bid}")
        if bids:
            others = ", ".join(f"{k} {v[0]}" for k, v in sorted(bids.items(), key=lambda x: -x[1][0])
                               if k != who.name)
            print(f"       (floor: {others})")
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
