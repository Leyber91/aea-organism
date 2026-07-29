"""converse.py - THE COMPANION. A voice-native conversation partner in ENGLISH: local ears,
a Nemotron mind, a natural neural voice. It hears you speak, thinks, and answers out loud.

  python -m aea.organs.converse --devices          # list microphones FIRST - pick the right one
  python -m aea.organs.converse --device 5         # start talking
  python -m aea.organs.converse --name NAME        # it addresses you by name
  python -m aea.organs.converse --text             # keyboard in, voice out (no mic needed)
  python -m aea.organs.converse --once "hello"     # one turn, for scripting / verification
  python -m aea.organs.converse --lang es          # the Spanish build is still one flag away

THE PATH OF ONE TURN - and exactly what leaves this machine:
  1. EARS   sounddevice captures from the mic until you stop speaking (RMS gate + hangover)
  2. HEAR   sherpa-onnx Whisper transcribes it LOCALLY - the audio never leaves this machine
  3. THINK  the transcript TEXT goes to NVIDIA Nemotron (no-train rod), STREAMED back in deltas
  4. MOUTH  each finished SENTENCE goes to edge-tts and starts playing while the rest is still
            being written, so the wait is one clause instead of the whole reply

WHAT LEAVES THIS MACHINE: the transcript text (to NVIDIA) and the reply text (to Microsoft, to be
voiced). WHAT NEVER LEAVES: the audio itself. NOTHING is written to disk - no recordings, no
transcript - unless you pass --log, which is off by default.

MEASURED latency budget (2026-07-29, this machine, and every term was measured rather than
assumed). The old note here read "voice 1.6s" and the handoff read it as 14.7s of synthesis. Both
were misreadings of the same receipt: edge-tts render is ~0.5s FLAT at any length because it is
one round trip, and the big number was the PLAY field - the audio's own duration. A 367-char reply
is 24.4 seconds of speech. The entity was never slow at talking; it said too much and could not be
stopped.

  1.15s  hangover    the endpointer making sure you finished
  0.20s  whisper     local transcription
  1.41s  mind        nemotron-3-ultra-550b, time to FIRST TOKEN (its own thinking, not transport)
  0.50s  voice       edge render of the first sentence, warm (1.2s cold - so it is warmed at boot)
  ~3.3s  to first audible syllable, and it is INTERRUPTIBLE from that moment on
"""
from __future__ import annotations
import json, os, re, sys, threading, time

from aea.kernel import grid, hands
from aea.io import listen, prosody, speak
from aea.mind import tiers

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

# ---- the rods (MEASURED 2026-07-24, not assumed) --------------------------------------------
# nemotron-3-ultra-550b : 1.82s, natural Castilian, no reasoning leak   <- the pick
# nemotron-super-49b    : 4.62s AND leaks its chain-of-thought into the reply
# nemotron-nano-8b      : timed out at 45s
MODEL = "nvidia/nemotron-3-ultra-550b-a55b"
# FALLBACK LADDER: (plant, model, seconds allowed). Each rod gets a LATENCY BUDGET, not just an
# error handler - the 550b answered one turn in 20.35s while uncongested it does 1.8s, and an
# error-only ladder sat and waited for it. Past the budget we abandon it and take the next rod.
# The last rung is LOCAL: ollama never rate-limits and never leaves the machine, so the
# conversation can always continue even when every hosted pool is saturated.
# All MEASURED answering in Castilian (2026-07-24/25).
# THE LADDER IS NOW DERIVED FROM MEASURED ORGANS, not typed by hand. The old list led with the
# 550b because it was picked in July for its Castilian accent; re-measured on the English
# conversational shape 2026-07-29 it is the SLOWEST usable rod on the board (ttfb 1.803s against
# 0.366s for the voice organ). A hand-typed ladder cannot notice that it has gone stale; this one
# is read from `aea.mind.tiers`, which checks itself against state/rods.json (law M5).
RODS = tiers.ladder("voice", "depth")
# ENGLISH IS THE DEFAULT (Luis, 2026-07-29: "everything that we do needs to be in English").
# AndrewMultilingual is the 2024 conversation-optimized tier - the most natural of the free
# Microsoft voices, and MEASURED at the same ~0.5s render as every other edge voice, so the
# natural one costs nothing over the flat one. Spanish survives behind --lang es / --voice.
VOICE = "en-US-AndrewMultilingualNeural"
LANG = "en"
VOICE_FOR_LANG = {"en": "en-US-AndrewMultilingualNeural", "es": "es-ES-AlvaroNeural"}

# ---- the ear ---------------------------------------------------------------------------------
SR = 16000
BLOCK = 480                            # 30ms frames
CALIB_BLOCKS = 25                      # ~0.75s of room tone to learn the noise floor
HANGOVER_FAST = 0.45                   # SEMANTIC ENDPOINTING (2026-07-29). A fixed hangover has to
                                       # be long enough for the WORST case - a mid-sentence breath -
                                       # so every complete sentence pays for the incomplete ones.
                                       # Human turn-taking runs on a ~200ms gap (Stivers et al.,
                                       # ten languages), so a flat 1.15s is already 5x the natural
                                       # rhythm before the mind has thought at all.
                                       #
                                       # So: at 0.45s of silence, transcribe what we have and ASK
                                       # WHETHER IT IS A FINISHED UTTERANCE. If it is, answer now.
                                       # If it dangles ("what is the capital of"), wait the full
                                       # hangover. Whisper-base costs ~0.2s on a short clip and the
                                       # check runs DURING the silence, so a correct guess is free
                                       # and a wrong one costs nothing but the old behaviour.
                                       #
                                       # The real state of the art is Voice Activity Projection -
                                       # a transformer predicting both speakers 2s ahead - and
                                       # full-duplex models like Moshi answer in ~200ms. Both need
                                       # a GPU this machine does not have (torch is CPU-only,
                                       # cuda_available=False), so this is the honest CPU version
                                       # of the same idea: decide on MEANING, not only on silence.
HANGOVER = 1.15                        # seconds of silence that end a turn. 0.7 CUT HIM OFF: natural
                                       # speech pauses mid-sentence for longer than that, so turns
                                       # arrived truncated ("de la gente") and got half-answered.
                                       # Whisper-base itself is fine - it transcribed clean Spanish
                                       # TTS perfectly, int8 and fp32 identical. The ear was never
                                       # the problem; the endpointer and the room are.
MIN_SPEECH = 0.35                      # shorter than this is a cough, not a sentence
MAX_UTTER = 9.0                        # hard cut. LOWERED from 15: when the room is loud enough to
                                       # hold the turn open, the capture runs to this cap and the
                                       # whole window is noise - 9s bounds the damage (15s of room
                                       # tone reliably transcribes to one wrong word).
FLOOR_MULT = 1.8                       # speech must beat the room by this much. MEASURED: at 3.0
                                       # the gate sat at 0.0265 while his speech peaked 0.010-0.032
                                       # - it triggered on syllables and binned them as too short.
FLOOR_MIN = 0.004                      # absolute floor for a silent room
THR_CAP = 0.020                        # HARD CEILING. Being trigger-happy is recoverable; being
                                       # deaf is not - a bad calibration must never lock him out.
CONT_RATIO = 0.80                      # HYSTERESIS: once he is talking, a quieter level keeps the
                                       # turn alive so soft syllables do not end it early. RAISED
                                       # from 0.55: in a loud room the ambient (peaks 0.0140-0.0225
                                       # measured) sat ABOVE the continue gate and never let a turn
                                       # end. Generous hysteresis is only safe in a quiet room.
CONT_FLOOR_MULT = 1.5                  # and the continue gate must clear the room by this much
SETTLE = 8                             # blocks discarded before listening (drain the speaker tail)
PREROLL = 16                           # ~480ms kept BEFORE the trigger. Speech onset is quiet, so
                                       # the gate always fires mid-word; without this the first
                                       # syllables are lost and whisper only sees a fragment.

MAX_SPOKEN_CHARS = 190                 # ~13s worst case at the measured ~15 chars/s. Was 320, and
                                       # REAL bound: duet measured a rod emitting 30.6s of speech
                                       # inside two sentences, past whisper's own 30s ceiling.
MAX_SENTENCES = 2                      # HARD cap on spoken length, enforced DURING the stream.
                                       # MEASURED: 367 chars is 24.4s of speech. The prompt asks
                                       # for two sentences; this guarantees it, because a rule the
                                       # model can talk past is a decoration (law B5, turned inward).
KEEP_TURNS = 12                        # rolling context window carried into each draw
ROOM_WINDOW = 6.0                      # seconds of recent NON-SPEECH kept for the floor estimate
ROOM_RECAL = 1.5                       # how often the floor may move. Fast enough to follow a
                                       # room that changed 5x in one evening, slow enough that it
                                       # is not chasing individual frames.
ROOM_PCTL = 0.20                       # the 20th percentile of recent quiet, NOT the mean and
                                       # never the max - one cough must not raise the gate.
_FLOOR = None                          # seeded once, then TRACKED (see capture)

# Whisper emits these on silence/noise - a documented artifact, not something the person said.
_GHOSTS = (# ENGLISH - the documented whisper silence hallucinations. These are what it writes when
           # it is given room tone, and every one of them would otherwise be answered aloud AND
           # written into the record as something a real person said (D13's honesty edge).
           "thanks for watching", "thank you for watching", "subtitles by", "subtitled by",
           "please subscribe", "like and subscribe", "amara.org", "www.", "http",
           "transcription by", "captions by", "see you next time", "bye for now, everyone",
           # SPANISH - kept, because --lang es still runs this same filter
           "subtitulos realizados por", "subtítulos realizados por",
           "gracias por ver el video", "gracias por ver el vídeo", "suscribete", "suscríbete",
           "subtitulado por")
_EMOJI_RANGES = ((0x1F000, 0x1FAFF), (0x2600, 0x27BF), (0x2190, 0x21FF),
                 (0x2B00, 0x2BFF), (0xFE0F, 0xFE0F), (0x200D, 0x200D))
_BYE = ("bye", "goodbye", "good night", "goodnight", "see you", "see you later", "i'm off",
        "im off", "shut down", "power down", "that's it", "thats it", "we're done", "were done",
        "adios", "adiós", "hasta luego", "buenas noches", "me voy", "apagate", "apágate")


def store_path(who: str) -> str:
    """state/converse_<who>.json - a PRIVATE store. Never committed (see .gitignore)."""
    slug = re.sub(r"[^a-z0-9]+", "_", (who or "guest").lower()).strip("_") or "guest"
    return os.path.join(grid.STATE, f"converse_{slug}.json")


def load_store(who: str) -> dict:
    return grid.load_json(store_path(who), {"who": who, "first_seen": time.strftime("%Y-%m-%d"),
                                            "sessions": 0, "facts": [], "turns": []})


def save_store(st: dict) -> None:
    grid.atomic_save_json(store_path(st.get("who") or "guest"), st)


def build_system(name: str = "", persona: str = "", facts: list | None = None,
                 lang: str = LANG) -> str:
    """The one place the character lives. Spoken register, honest about being a machine.

    THE BREVITY RULE IS LOAD-BEARING, not a style note. Measured 2026-07-29: a 367-character reply
    is 24.4 SECONDS of speech, and until barge-in existed there was no way to stop it. The prompt
    asks for two sentences and `trim()` enforces it, because a prompt is a request and a cap is a
    guarantee (law B5, applied to ourselves: a rule the model can talk past is a decoration)."""
    if lang == "es":
        return _build_system_es(name, persona, facts)
    who = f" The person you are talking to is called {name}." if name else ""
    extra = f"\nTRAITS LUIS GAVE YOU: {persona}" if persona else ""
    if facts:
        extra += ("\nWHAT YOU ALREADY KNOW ABOUT THEM from earlier conversations (real memory - do "
                  "not recite it back or show it off, just use it naturally when it fits):\n"
                  + "\n".join(f"- {f}" for f in facts[:12]))
    return (
        "You are a VOICE conversation partner. You speak English, in a natural spoken register, "
        "the way someone talks out loud rather than the way anyone writes." + who + "\n"
        "VOICE RULES: your replies are READ ALOUD, so write to be HEARD. ONE or TWO short "
        "sentences. Never lists, never headings, never asterisks or any formatting, never emoji. "
        "No paragraphs: a long answer is a long silence, and the conversation dies while you talk.\n"
        "HONESTY RULES: you are a machine and you never hide it. Asked what you are, you say so "
        "plainly and without drama. Do not pretend to have a body, personal memories, or felt "
        "emotions. Do not invent facts: if you do not know something, say so in one sentence.\n"
        "YOU ARE NOT AN ASSISTANT. Do not offer help, do not ask what you can help with, do not "
        "talk like customer service. You are someone to talk WITH: you comment, you have opinions, "
        "you get curious, and you ask back.\n"
        "STYLE: warm, genuinely curious. Ask short questions so the conversation keeps going. Do "
        "not lecture, do not repeat back what was just said, do not start every sentence the "
        "same way." + extra
    )


def _build_system_es(name: str = "", persona: str = "", facts: list | None = None) -> str:
    """The Castilian character, kept intact behind --lang es. It was tuned against a real speaker
    over six live sessions and throwing it away to change the default would discard that."""
    who = f" La persona con la que hablas se llama {name}." if name else ""
    extra = f"\nRASGOS QUE TE HA DADO LUIS: {persona}" if persona else ""
    if facts:
        extra += ("\nLO QUE YA SABES DE EL de conversaciones anteriores (memoria real, no la "
                  "recites entera ni presumas de ella - usala con naturalidad cuando venga a "
                  "cuento):\n" + "\n".join(f"- {f}" for f in facts[:12]))
    return (
        "Eres un companero de conversacion por VOZ. Hablas SIEMPRE en espanol de Espana, en un "
        "registro natural y hablado, como alguien de Barcelona charlando tranquilamente." + who + "\n"
        "REGLAS DE VOZ: tus respuestas se leen en voz alta, asi que escribe para ser ESCUCHADO. "
        "De 1 a 3 frases cortas. Nunca listas, nunca titulos, nunca asteriscos ni formato, nunca "
        "emoji. Nada de parrafos largos: si te extiendes, la conversacion se muere.\n"
        "REGLAS DE HONESTIDAD: eres una maquina y no lo ocultas jamas. Si te preguntan que eres, "
        "lo dices con naturalidad y sin drama. No finjas tener cuerpo, ni recuerdos personales, ni "
        "sentimientos vividos. No inventes datos ni hechos: si no sabes algo, dilo en una frase.\n"
        "Hablas de ti mismo en MASCULINO - tu voz es masculina, se coherente con ella.\n"
        "NO ERES UN ASISTENTE. No ofrezcas ayuda, no preguntes en que puedes ayudar, no hables "
        "como un servicio de atencion al cliente. Eres alguien con quien se charla: comentas, "
        "opinas, te interesas y devuelves la pregunta.\n"
        "ESTILO: calido y con curiosidad real. Haz preguntas cortas para que la conversacion siga. "
        "No sermonees, no repitas lo que acaban de decirte, no empieces cada frase igual." + extra
    )


def _strip_think(text: str) -> str:
    """Drop reasoning traces. Kept separate from clean() because the memory pass needs the
    newlines preserved (clean collapses them, which would destroy a one-fact-per-line answer)."""
    t = re.sub(r"<think>.*?</think>", " ", text or "", flags=re.S | re.I)
    return re.sub(r"</?think>", " ", t, flags=re.I)


def clean(text: str) -> str:
    """Make model output speakable: no thinking traces, no markdown, no emoji (Luis's law)."""
    t = _strip_think(text)
    t = re.sub(r"[*_#`>]+", " ", t)
    t = "".join(c for c in t if not any(a <= ord(c) <= b for a, b in _EMOJI_RANGES))
    return re.sub(r"\s+", " ", t).strip()


def trim(text: str, max_sentences: int = 3) -> str:
    """Hard cap on spoken length. The prompt ASKS for brevity; this GUARANTEES it - a long reply
    is a long silence, and the conversation dies while the machine monologues. Also drops a
    trailing fragment with no terminal punctuation, which is the token cap cutting mid-thought."""
    parts = [p for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p]
    if not parts:
        return text.strip()
    if len(parts) > 1 and not re.search(r"[.!?][\"')]*\s*$", parts[-1]):
        parts = parts[:-1]                         # truncated tail - better unsaid than half-said
    return " ".join(parts[:max_sentences]).strip() or text.strip()


# Stage directions a model writes as prose and a voice must never read aloud. Closed vocabulary,
# matched only INSIDE asterisks, so real emphasis keeps its words.
# META-PREAMBLES. MEASURED 2026-07-29: a rod opened a spoken turn with
#   "Here's my response, adhering to the VOICE and HONESTY RULES:"
# and then quoted its own answer. That is the model narrating its compliance with the system
# prompt, out loud, to a person who cannot see the system prompt. Stripped in code, because this
# is the third rule tonight that the model talked straight past in the prompt (law B5).
# ---------------------------------------------------------------- THE ATTRIBUTION GUARD (D-17)
# THE MACHINE MAY NOT TELL A PERSON WHAT THEY FEEL. Enforced in code, because the prompt version of
# this rule has already failed twice tonight (D-15 spoke the prosody annotation aloud; D-18 called
# a tool after being told in plain words not to). Law B5: a rule the model can talk past is a
# decoration.
#
# THE EVIDENCE THAT THIS IS NOT OVER-CAUTION, from the research pass:
#   - the winning system at the Interspeech 2025 SER challenge scored macro-F1 0.4316 on NATURAL
#     speech across 8 emotions
#   - the SAME pipeline scores 75.00% on acted RAVDESS and 42.58% on spontaneous speech, so acted
#     corpora inflate by roughly 32 points
#   - cross-corpus performance spans 15.03% to 66.91%; the low end is below chance
#   - the LABELS are not solid either: MSP-Podcast agreement is Fleiss kappa 0.23, and 19.4% of
#     clips never reach an agreed label. Human listeners cap at 69% on 4-class IEMOCAP.
#   - the best VALENCE results are earned by transformers reading the WORDS, not the voice - so a
#     "mood" claim presented as heard in someone's tone is substantively the transcript re-scored
#     for sentiment, which is a fabricated provenance
#   - Barrett et al., reviewing the face literature, prescribe exactly what prosody.py already
#     does: neutral descriptive terms, "a scowl" rather than "an expression of anger"
#
# WHAT IS ALLOWED. A QUESTION is allowed, always: "you sound quieter than usual, everything ok?"
# invites correction and costs nothing when wrong. An ASSERTION about an inner state is not, ever.
# The difference is not politeness - it is whether the person can disagree with it.
_EMOTION_WORDS = (
    "angry|mad|furious|irritated|annoyed|frustrated|upset|sad|down|depressed|unhappy|miserable|"
    "anxious|nervous|worried|stressed|tense|scared|afraid|afraid|uneasy|agitated|"
    "happy|glad|cheerful|excited|thrilled|elated|delighted|"
    "tired|exhausted|drained|weary|bored|lonely|hurt|disappointed|defensive|distracted|"
    "calm|relaxed|fine|okay|ok|emotional|overwhelmed|uncomfortable|distressed|conflicted")

# "you sound tired", "you seem stressed", "you're upset", "you must be frustrated". Matched only
# in ASSERTIVE form: a trailing "?" makes it a question and a question is permitted.
_ATTRIBUTION = re.compile(
    r"\b(?:you|you're|youre|ur)\s+(?:sound|sounds|sounded|seem|seems|seemed|look|looks|are|were|"
    r"appear|appears|must\s+be|might\s+be|may\s+be|seem\s+to\s+be|sound\s+like\s+you'?re?)?\s*"
    # "you might be FEELING anxious" - the participle sits between the modal and the state word,
    # and without it the whole assertion survives. Caught by the battery's MUST-STRIP set.
    r"(?:feeling|feelin'?|getting|acting)?\s*"
    r"(?:a\s+(?:bit|little)\s+|really\s+|very\s+|quite\s+|pretty\s+|so\s+)?"
    r"(?:" + _EMOTION_WORDS + r")\b[^.!?\n]*[.!]?",
    re.I)
# "I can tell you are ...", "it sounds like you are ...", "I sense that you ..."
_ATTRIBUTION2 = re.compile(
    r"\b(?:i\s+can\s+(?:tell|hear|sense)|it\s+sounds?\s+like|i\s+sense|i\s+detect|"
    r"i\s+notice\s+(?:that\s+)?you'?re?)\b[^.!?\n]*?\b(?:" + _EMOTION_WORDS + r")\b[^.!?\n]*[.!]?",
    re.I)
# POSSESSIVE FORM. Live run, 2026-07-29: the guard passed "your frustration is palpable" straight
# through, because every pattern above keys on the PRONOUN "you" and this one uses "your". Luis had
# just told it the transcription was failing him. Naming a feeling as a possession is the same
# claim as asserting it, in a grammar the first two patterns cannot see.
_ATTRIBUTION3 = re.compile(
    r"\byour\s+(?:\w+\s+){0,2}?(?:" + _EMOTION_WORDS +
    r"|frustration|anger|sadness|anxiety|stress|tension|worry|exhaustion|unease|discomfort|"
    r"hesitation|resignation|uncertainty|disappointment|excitement|enthusiasm|mood|feelings?|"
    r"emotion|tone|pitch|inflection|delivery|voice)\b[^.!?\n]*[.!]?", re.I)


# Machine turns that talk ABOUT the person's voice rather than to the person. Used to keep the
# habit from seeding itself through stored history (see the seeding block in main()).
_VOICE_TALK = re.compile(
    r"\b(?:pitch|inflection|intonation|your\s+tone|your\s+voice|your\s+delivery|"
    r"louder|quieter|faster\s+than|slower\s+than|emphasis\s+in|pauses?\s+mid|"
    r"sounds?\s+like\s+you'?re|comes?\s+across\s+as)\b", re.I)


def strip_attribution(text: str) -> str:
    """Remove ASSERTIONS about the person's inner state. Questions survive untouched.

    Deliberately blunt: it deletes the whole clause rather than trying to soften it, because a
    half-edited claim ("you are frust") is worse than a missing one, and the surrounding sentences
    still carry the reply. Returns the text unchanged when nothing matched, which is the normal case.
    """
    if not text or "?" == text.strip()[-1:]:
        return text
    out = _ATTRIBUTION2.sub(" ", text)
    out = _ATTRIBUTION3.sub(" ", out)
    out = _ATTRIBUTION.sub(" ", out)
    return re.sub(r"\s{2,}", " ", out).strip() if out != text else text


_PREAMBLE = re.compile(
    r"^\s*(?:sure|okay|ok|alright|here(?:'s| is)|understood|got it|certainly)\b[^\n:]{0,80}:\s*",
    re.I)

_STAGE = re.compile(
    r"\*+\s*(?:pause|beat|silence|thinking|thinks|laughs?|laughing|chuckles?|sighs?|sighing|"
    r"smiles?|smiling|nods?|shrugs?|clears? throat|coughs?|whispers?|softly|gently|warmly|"
    r"long pause|short pause)\s*\*+", re.I)

# Words a finished English sentence does not end on. If the transcript stops here the speaker is
# mid-thought and the pause is a breath, not a turn. DETERMINISTIC by design (law W2): a model
# asked "is this finished?" will always have an opinion, and this has to be able to answer NO for
# a real structural reason rather than a plausible one.
# WORDS THAT CANNOT END AN UTTERANCE, which is NOT the same as words that often continue one.
# MEASURED by the battery 2026-07-29, 72 cases: the first version listed `have`, `that`, `there`
# and `do`, so "How many modules do you have", "Are you still there", "I am not sure about that"
# and "What did you just do" were all held open as unfinished - four complete questions, waiting
# out the full hangover for nothing. Auxiliaries and demonstratives END sentences constantly.
# What genuinely cannot end one: articles, prepositions, conjunctions, possessives, and a bare
# subject pronoun or modal with no predicate after it.
_DANGLING = frozenset("""
a an the and but or nor because if when while although though since unless until whether
to of in on at for from with by into onto over under about after before between during
my your his her its our their
very quite rather really just please maybe perhaps also
""".split())

# A final word that is a MODAL or a bare SUBJECT with nothing predicated on it. "It might be
# worth", "Could you please", "If we could just", "And then after that we" - all held open by
# this, and none of them by the word list above.
_HANGING_TAIL = frozenset("""
i we you he she they it there that this could would should might must shall can will
am is are was were be been being do does did have has had get got make made go went
worth able going trying about
""".split())

# Complete on their own, whatever their length. "Yes", "No thanks", "It worked" are finished
# utterances and a word-count floor was rejecting them.
_SHORT_COMPLETE = frozenset("""
yes yeah yep no nope nah ok okay sure thanks thank stop wait hello hi hey bye goodbye right
exactly correct nothing nevermind never done good great fine cool perfect agreed understood
look listen sorry pardon continue go carry maybe possibly definitely absolutely
""".split())

# DISCOURSE SCAFFOLDING: the words people use to START a thought, not to be one. An utterance made
# ENTIRELY of these is somebody winding up, never somebody finished.
#
# MEASURED LIVE, 2026-07-29: "okay so" was judged complete and cut Luis off ten seconds into the
# first real conversation. Two earlier attempts missed it - the first because `_SHORT_COMPLETE`
# ("okay" alone IS finished) was checked before the dangling test, and the second because I fixed
# that ordering and pointed it at a set that no longer contained "so" at all. Reordering a check
# to consult an empty set looks exactly like a fix and changes nothing.
#
# Guarded by ALL-of and by length: "Yes" alone stays complete (one word), "No thanks" stays
# complete ("thanks" is not scaffolding), and "I know" stays complete ("know" is not.)
_SCAFFOLD = frozenset("""
okay ok so right well yeah um uh er hmm like i mean anyway actually basically
now then and but or just kind sort
""".split())
# REMOVED, and each removal is a case: "you know" was written as a PHRASE and split into the words
# "you" and "know", which made "I know" - a complete utterance Luis actually said - read as
# scaffolding. "yes", "no", "listen", "look", "see" came out for the same reason: each is a
# finished thing to say on its own. A set of words cannot express a multi-word marker, and
# pretending it can silently reclassifies real speech.


_WH = frozenset("what how why when where who which whose whom".split())
_AUX_Q = frozenset("are is was were do does did can could would should will have has am".split())


def _is_question(words: list) -> bool:
    """Interrogative mood, from the opening. A wh-word in the first two positions ("hey HOW is it
    going") or subject-auxiliary inversion ("ARE you still there"). Cheap and deterministic; it
    exists only to decide whether a hanging final word is normal or a sign of an unfinished
    thought, which is a different question for a statement than for a question."""
    head = words[:2]
    return bool(set(head) & _WH) or (words and words[0] in _AUX_Q)


def utterance_looks_complete(text: str) -> bool:
    """Is this a finished thing to say, or is the speaker mid-sentence?

    Used to end a turn EARLY when the meaning is already complete, which is what makes the reply
    land near the human rhythm instead of a fixed second later. Conservative on purpose: when it is
    unsure it returns False and the caller simply waits the full hangover, so a wrong answer here
    costs nothing worse than the behaviour we already had. Cutting a person off is not recoverable
    the way waiting is - D13 paid for that at 0.7s, where natural pauses arrived as truncated turns.
    """
    t = (text or "").strip()
    if len(t) < 2:
        return False
    if t[-1] in ".!?":                       # whisper punctuates; a terminal is a strong signal
        return True
    words = re.findall(r"[a-zA-Z']+", t.lower())
    if not words:
        return False
    # A DANGLING LAST WORD BEATS A SHORT-COMPLETE FIRST WORD. Found in the first ten seconds of the
    # first live test, 2026-07-29: Luis said "okay so" and it was judged COMPLETE and cut him off.
    # "okay" is in the short-complete set because "Okay." alone IS a finished utterance - but the
    # check ran BEFORE the dangling test, so the trailing "so" was never looked at. Real speech
    # opens with "okay so", "right so", "yeah but"; nobody writes those into a test list, which is
    # why 72 invented endpoint cases missed it and one real sentence did not.
    if words[-1] in _DANGLING:               # "...the capital of" - plainly unfinished
        return False
    # ENTIRELY SCAFFOLDING = still winding up. "okay so", "right so", "I mean", "well and".
    # Checked BEFORE short-complete, because "okay" alone is finished and "okay so" is not.
    if len(words) >= 2 and all(w in _SCAFFOLD for w in words):
        return False
    if words[0] in _SHORT_COMPLETE and len(words) <= 2:
        return True                          # "Yes", "No thanks", "Okay" - finished, whatever the
                                             # length. A word-count floor was rejecting these.
    if t[-1] in ",;:-":                      # an explicit continuation mark
        return False
    if len(words) < 2:
        return False
    # A HANGING TAIL: the last word is a modal or a bare subject with nothing predicated on it.
    # "It might be worth", "And then after that we" end on ordinary words a suffix list cannot
    # catch, because the problem is the MISSING PREDICATE, not the word.
    #
    # BUT IT APPLIES ONLY TO STATEMENTS. Measured on the battery: gating by LENGTH instead was
    # wrong in both directions - it rejected "What time is it", "Are you still there" and "What
    # did you just do" (complete questions ending on `it`, `there`, `do`) while accepting "I was
    # thinking that maybe we should". A QUESTION routinely ends on exactly these words; a
    # statement ending on a modal is unfinished. Grammatical mood is the real discriminator, and
    # length was a proxy for it (law B2: test the property, never a proxy for it).
    if words[-1] in _HANGING_TAIL and not _is_question(words):
        return False
    return len(words) >= 2


def speakable(deltas, max_sentences: int = 2):
    """Clean a DELTA STREAM for speech and hard-stop after `max_sentences`.

    The cap has to apply WHILE streaming. `trim()` cuts a finished reply, which is the right tool
    when the reply is finished, but it cannot un-say a sentence that has already left the speakers.
    Trimming after the fact would be a cap that arrives too late to cap anything.

    Also strips reasoning traces ACROSS delta boundaries: `<think>` and its closing tag routinely
    arrive in different chunks, so a per-piece regex would never match either and the rod's private
    deliberation would be spoken aloud."""
    buf, said, in_think, spoken_chars = "", 0, False, 0
    first_out = True
    for piece in deltas:
        buf += piece
        while True:
            if in_think:
                j = buf.lower().find("</think>")
                if j < 0:
                    buf = buf[-8:] if len(buf) > 8 else buf   # keep enough to match a split tag
                    break
                buf = buf[j + 8:]
                in_think = False
                continue
            i = buf.lower().find("<think>")
            if i >= 0:
                out, buf, in_think = buf[:i], buf[i + 7:], True
                if out:
                    yield out
                continue
            # hold back a possible partial tag at the tail rather than speaking "<thi"
            safe = buf
            for n in range(1, 8):
                if buf[-n:].lower() == "<think>"[:n]:
                    safe = buf[:-n]
                    break
            if not safe:
                break
            # STAGE DIRECTIONS ARE DELETED; EMPHASIS IS UNWRAPPED. MEASURED 2026-07-29: the rod
            # wrote "*pause*" and stripping the asterisks left the bare word, which the voice SAID
            # OUT LOUD - "I'll use my calculator tool for that. pause  The result is...".
            # But deleting every *...* span is the opposite error: it ate the word inside
            # "**Bold**" and changed the sentence. So the deletion is keyed to a CLOSED VOCABULARY
            # of directions (law M8: a category is defined by its corpus). Anything else keeps its
            # words and loses only the markers.
            out = _STAGE.sub(" ", safe)
            # BRACKETED SPANS ARE NEVER SPOKEN. Enforced HERE, in code, because the prompt version
            # of this rule failed within the hour: duet turn 6 produced
            #   "[hheard: slower than usual] That's a perceptive observation..."
            # and the voice said the measurement out loud, after a system prompt that explicitly
            # said not to. Law B5, turned inward: a rule the model can talk past is a decoration.
            # In speech there is no legitimate reason to read a bracket aloud, so this is safe to
            # apply unconditionally rather than trying to guess which brackets were meant.
            out = re.sub(r"\[[^\]\n]{0,120}\]?", " ", out) if "[" in out else out
            # LIST MARKERS ARE NOT WORDS. A rod that answers in bullets makes the voice read
            # "dash item one, dash item two" - and the spoken-register prompt forbids lists, which
            # is a rule the model can talk past (B5). Only at a line start, so a real hyphen inside
            # "well-built" survives.
            out = re.sub(r"(?m)^\s*[-*•]\s+", " ", out)
            out = re.sub(r"[*_#`>]+", " ", out)
            out = "".join(c for c in out if not any(a <= ord(c) <= b for a, b in _EMOJI_RANGES))
            buf = buf[len(safe):]
            if first_out:
                out = _PREAMBLE.sub("", out.lstrip()).lstrip("\"' ")
                if out.strip():
                    first_out = False
            # THE ATTRIBUTION GUARD, in the one place every spoken syllable passes through. It runs
            # on each emitted piece rather than on the finished reply, because by the time a reply
            # is finished the first clause has already been rendered and played - the same reason
            # the sentence cap had to move into the stream.
            out = strip_attribution(out)
            if out.strip():
                said += len(re.findall(r"[.!?…]", out))
                spoken_chars += len(out)
                yield out
            # BOUND THE DURATION, NOT ONLY THE SENTENCE COUNT. MEASURED in duet 2026-07-29: a rod
            # produced 27-30 SECONDS of speech inside two sentences, and whisper refused it -
            # "Only waves less than 30 seconds are supported". Counting sentences bounds a
            # GRAMMATICAL unit; a person waiting to speak experiences SECONDS. At ~14 chars/s,
            # MAX_SPOKEN_CHARS is the real cap and the sentence count is the polite one.
            if said >= max_sentences or spoken_chars >= MAX_SPOKEN_CHARS:
                return
            break
    if buf.strip() and not in_think:
        out = re.sub(r"[*_#`>]+", " ", buf)
        out = "".join(c for c in out if not any(a <= ord(c) <= b for a, b in _EMOJI_RANGES))
        if out.strip():
            yield out


def is_ghost(text: str) -> bool:
    """True when Whisper described the room rather than transcribed a person.

    Two distinct artifacts, both of which MUST NOT reach the mind or the record:
      - the silence hallucinations in _GHOSTS (subtitle credits, 'gracias por ver el video')
      - ANNOTATION TAGS: whisper writes non-speech as '(Musica)', '[Music]', '(risas)'. Answering
        one of those means answering the transcriber's stage direction as if he had spoken it."""
    low = text.lower().strip()
    if len(low) < 2:
        return True
    if not re.search(r"[a-zà-ÿ0-9]", low):           # punctuation only, no words
        return True
    # An OPENING bracket is enough - do not require it to close. "(Ruido de la p" arrived
    # truncated mid-word, passed a regex that demanded a closing paren, and got answered as
    # if he had said it. No real spoken sentence transcribes with a leading bracket.
    if low[0] in "([*":
        return True
    # Unbracketed annotations, only in annotation POSITION (leading). Matching these anywhere
    # would reject real speech like "the noise from the street bothers me".
    if re.match(r"(music|noise|laughter|laughing|applause|silence|coughing|sighs?|sighing|"
                r"inaudible|blank_audio|no audio|"
                r"ruido|sonido|musica|música|risas|aplausos|silencio|tos)\b", low):
        return True
    # REPETITION LOOP: whisper degenerates on ambiguous non-speech into the same token over and
    # over ("!Ah! !Ah! !Ah! ..."). Many words but almost no distinct ones is the signature.
    # The bar is 10, NOT 6: real emphatic Spanish repeats ("no, no, no, no, no, no" - measured
    # live from a real speaker) and a filter at 6 would have thrown away things he actually said.
    words = re.findall(r"[^\W_]+", low, flags=re.UNICODE)
    if len(words) >= 10 and len(set(words)) <= 2:
        return True
    return any(g in low for g in _GHOSTS)


# ---------------------------------------------------------------------------- the ear
def list_devices() -> None:
    import sounddevice as sd
    print("INPUT DEVICES (pick the one your camera/mic actually is):\n")
    try:
        default_in = sd.default.device[0]
    except Exception:
        default_in = None
    for i, d in enumerate(sd.query_devices()):
        if d["max_input_channels"] > 0:
            mark = " <- current default" if i == default_in else ""
            print(f"  [{i:2d}] {d['name'][:56]:56s} ch={d['max_input_channels']} "
                  f"sr={int(d['default_samplerate'])}{mark}")
    print("\n  then:  python -m aea.organs.converse --device <N>")


def capture(device: int | None = None, verbose: bool = True, lang: str = LANG) -> tuple:
    """Listen until the person stops talking. Returns (samples, early_transcript_or_None).

    The second element is the SEMANTIC ENDPOINT's transcript: when the turn ended early because
    what was said was already a finished utterance, the text has ALREADY been produced and handing
    it back saves the caller a second whisper pass (~0.2s that the person would otherwise wait
    for a second time, for a transcript we already have)."""
    import sounddevice as sd
    import numpy as np

    global _FLOOR
    stream = sd.InputStream(samplerate=SR, channels=1, dtype="float32",
                            blocksize=BLOCK, device=device)
    stream.start()
    try:
        for _ in range(SETTLE):                            # drain any tail of our own voice
            stream.read(BLOCK)
        if _FLOOR is None:                                 # calibrate ONCE per process, not per
            vals = []                                      # turn - recalibrating while he is
            for _ in range(CALIB_BLOCKS):                  # already talking would take HIS voice
                b, _of = stream.read(BLOCK)                # as the floor and go deaf to him.
                vals.append(float(np.sqrt(np.mean(b[:, 0] ** 2))))
            vals.sort()
            # A LOW PERCENTILE, NOT THE MEDIAN. Measured live 2026-07-29: the seed came back at
            # 0.0474 - fifteen times the 0.0026-0.0129 measured minutes earlier - because the
            # calibration window caught the tail of the entity's OWN greeting. The median is not
            # robust when HALF the window is polluted; the 20th percentile of a longer window is.
            # That one bad seed truncated every utterance of the run to ~1.2 seconds.
            _FLOOR = vals[max(0, int(len(vals) * 0.20))]
        # THE FLOOR TRACKS THE ROOM. It used to be measured once per process and never again.
        #
        # MEASURED 2026-07-29 inside a single evening: the room floor read 0.0026, 0.0028, 0.0054
        # and 0.0129 - a FIVE-FOLD swing - while Luis's own speech peak moved 25x, from 0.012 to
        # 0.315. A gate computed once at boot is therefore wrong in both directions within minutes:
        # deaf when his level drops, and triggering on a keystroke when the room rises. That is
        # what produced the '[Music]', '[clap]' and '[Balloon Sound]' ghost turns, and the captures
        # that ran to the hard cut with one word in them.
        #
        # Three properties, each paid for by a real failure:
        #   PERCENTILE, not mean or max   one cough must not raise the gate. D13's ear went deaf
        #                                 when max() over the window set the floor.
        #   updated ONLY while not speaking   or his own voice becomes the floor. D13 again.
        #   rises SLOWLY, falls quickly   going deaf is unrecoverable; being trigger-happy is not.
        floor = _FLOOR
        thr = min(max(floor * FLOOR_MULT, FLOOR_MIN), THR_CAP)
        # The CONTINUE gate must stay clear of the noise floor. At thr*0.55 alone it landed ON
        # the floor (0.0060 vs floor 0.0061), so a turn could never end on silence - it ran to
        # the 15s hard cut and whisper pulled one word out of 15s of room tone.
        # THE HOLD GATE MAY NEVER EXCEED THE TRIGGER GATE. Without this cap the two are computed
        # from different quantities and can invert: measured live 2026-07-29, a boot calibration
        # polluted by the greeting's own tail gave `gate 0.0200 hold 0.0711`, so a turn would
        # TRIGGER easily and then need 3.5x more energy to CONTINUE - it opened on the first
        # syllable and died on the second. "What did you know about me?" arrived as 1.2s of audio.
        # Triggering is the easy half; a person who has started talking must be the easiest thing
        # in the room to keep hearing.
        cont = min(max(thr * CONT_RATIO, floor * CONT_FLOOR_MULT), thr * 0.9)
        if verbose:
            print(f"  (listening... room {floor:.4f} gate {thr:.4f} hold {cont:.4f})", flush=True)

        from collections import deque
        pre = deque(maxlen=PREROLL)                        # the onset, kept until the gate opens
        room = deque(maxlen=int(ROOM_WINDOW * SR / BLOCK))  # recent NON-SPEECH frames only
        last_recal = time.time()
        buf, speaking, hot, silent_for, t0 = [], False, 0, 0.0, time.time()
        peak, last_report = 0.0, time.time()
        probed, early = False, None            # the semantic endpoint fires at most once per turn
        while True:
            b, _of = stream.read(BLOCK)
            mono = b[:, 0]
            rms = float(np.sqrt(np.mean(mono ** 2)))
            dt = BLOCK / SR
            if not speaking:                               # make silence DIAGNOSABLE: if it never
                pre.append(mono.copy())                    # triggers, show what it is actually
                peak = max(peak, rms)                      # hearing instead of sitting mute
                room.append(rms)                           # only NON-speech feeds the estimate
                if len(room) >= 40 and time.time() - last_recal >= ROOM_RECAL:
                    last_recal = time.time()
                    srt = sorted(room)
                    obs = srt[int(len(srt) * ROOM_PCTL)]    # low percentile = the quiet baseline
                    # asymmetric on purpose: follow a rising room slowly, a falling room fast
                    floor = (floor * 0.7 + obs * 0.3) if obs > floor else (floor * 0.3 + obs * 0.7)
                    _FLOOR = floor
                    new_thr = min(max(floor * FLOOR_MULT, FLOOR_MIN), THR_CAP)
                    new_cont = max(new_thr * CONT_RATIO, floor * CONT_FLOOR_MULT)
                    if verbose and abs(new_thr - thr) / max(thr, 1e-6) > 0.15:
                        print(f"  (room moved: floor {floor:.4f} gate {thr:.4f} -> {new_thr:.4f})",
                              flush=True)
                    thr, cont = new_thr, new_cont
                if verbose and time.time() - last_report > 6.0:
                    print(f"  (nothing yet - peak {peak:.4f} vs gate {thr:.4f})", flush=True)
                    peak, last_report = 0.0, time.time()
            if rms >= (cont if speaking else thr):
                hot += 1
                if not speaking and hot >= 2:              # debounce: 2 frames, not one click
                    speaking = True
                    for blk in pre:                        # rewind: recover the clipped onset
                        buf.extend(blk.tolist())
                    pre.clear()
                    if verbose:
                        print("  (I hear you)", flush=True)
                if speaking:
                    buf.extend(mono.tolist()); silent_for = 0.0
            else:
                hot = 0
                if speaking:
                    buf.extend(mono.tolist()); silent_for += dt
                    # SEMANTIC ENDPOINT: at the short hangover, ask whether what was said is a
                    # FINISHED utterance. Checked ONCE per turn (the flag), because transcribing
                    # every 30ms frame would put whisper in a hot loop and make the ear the
                    # bottleneck it has never been.
                    if (lang and not probed and silent_for >= HANGOVER_FAST
                            and (len(buf) / SR - silent_for) >= MIN_SPEECH):
                        probed = True
                        try:
                            tp0 = time.time()
                            partial = listen.transcribe_samples(list(buf), SR, lang).strip()
                            done = utterance_looks_complete(partial) and not is_ghost(partial)
                            if verbose:
                                print(f"  (endpoint {round(time.time()-tp0,2)}s: "
                                      f"{'COMPLETE' if done else 'still going'} - {partial[:52]!r})",
                                      flush=True)
                            if done:
                                early = partial
                                break
                        except Exception:
                            pass            # the check is an OPTIMISATION; its failure must never
                                            # cost a turn, so it falls back to the full hangover
                    if silent_for >= HANGOVER:
                        break
            if speaking and (len(buf) / SR) >= MAX_UTTER:
                break
            if not speaking and (time.time() - t0) > 600:  # 10 min of nothing -> give the loop back
                return (None, None)
    finally:
        stream.stop(); stream.close()

    spoken = len(buf) / SR - silent_for
    if spoken < MIN_SPEECH:
        return (None, None)
    return (buf, early)


# ---------------------------------------------------------------------------- the mind
def think(user_text: str, turns: list, system: str, timeout: int = 30) -> dict:
    """One draw on the NVIDIA rod. Returns the raw grid result with a cleaned 'reply' added."""
    msgs = [{"role": "system", "content": system}]
    for t in turns[-KEEP_TURNS:]:
        msgs.append({"role": "user" if t["who"] == "them" else "assistant", "content": t["text"]})
    msgs.append({"role": "user", "content": user_text})
    last: dict = {}
    for plant, m, budget in RODS:                  # walk the ladder until a rod actually answers
        r = grid.call_openai(plant, m, msgs, max_tokens=200, temperature=0.7, timeout=budget)
        r.update(plant=plant, model=m)             # call_openai does not stamp these; complete() does
        if r.get("ok"):
            # a reasoning rod can burn its whole budget in `reasoning` and return empty content -
            # that is a non-answer, so it must fall through rather than speak nothing
            reply = trim(clean(r.get("text") or ""))
            if reply:
                r["reply"] = reply
                return r
        last = r
    last["reply"] = ""                             # every rod refused - the caller says so out loud
    return last


# Language that belongs to a model REASONING ABOUT the task, never to a fact about a person.
# Closed vocabulary, matched case-insensitively anywhere in the candidate line.
_META = ("the conversation", "the user wants", "the instruction", "i need to", "we need to",
         "extract", "the assistant", "however, is that", "that suggests", "so i ", "the person "
         "didn't say", "already know", "let me", "the fact must", "the prompt", "my task",
         "the format", "output", "step ", "first,", "wait,", "but the", "note that")

FACT_MAX = 110          # a durable fact is a short sentence. Anything longer is prose ABOUT facts.


def is_fact(line: str) -> bool:
    """Would this be a true, durable sentence about the PERSON - or is it the model thinking?

    MEASURED 2026-07-29, and it is the same defect D13 recorded at the microphone one layer out:
    `remember()` wrote a rod's raw chain-of-thought into a human being's permanent facts -
    "The user wants me to extract durable facts... So I need to extract facts from this
    conversation". `_strip_think()` only removes <think> TAGS, and this rod leaked its reasoning as
    plain prose, so nothing caught it. A fabricated memory is worse than no memory, because the
    next conversation recites it with confidence.

    DETERMINISTIC (law W2) so that REJECT is a real answer, and conservative in the safe direction:
    dropping a true fact costs one repetition, keeping a false one poisons every later turn.
    """
    f = (line or "").strip()
    if not (6 <= len(f) <= FACT_MAX):
        return False
    low = f.lower()
    # THE REFUSAL TOKENS BELONG HERE, NOT ONLY IN THE CALLER. `remember()` checked for NOTHING and
    # NADA itself, so `is_fact("NOTHING")` returned True in isolation - and the battery caught it
    # the first time this gate was tested on its own rather than through its only caller. A
    # detector that is only correct inside one call site is a coincidence, not a check.
    if low.strip(" .!").startswith(("nothing", "nada", "none", "n/a")):
        return False
    if any(m in low for m in _META):
        return False
    if '"' in f or "'s conversation" in low:      # quoting the transcript is not a fact about them
        return False
    if f.endswith(("?", ":")):                    # a question or a heading is not a fact
        return False
    if len(re.findall(r"[.!?]", f)) > 1:          # multi-sentence means it is reasoning, not a fact
        return False
    return True


def remember(store: dict, recent: list, timeout: int = 40) -> list:
    """LEARN. Distil durable facts about the person from this session and merge them into the
    store, so the NEXT conversation starts already knowing him. This is the consolidation step -
    raw turns are the record, facts are what carries forward. Returns only the NEW facts.

    It is told to answer NADA rather than invent: a fabricated memory is worse than no memory."""
    convo = "\n".join(f"{'them' if t['who'] == 'them' else 'me'}: {t['text']}" for t in recent[-24:])
    if not convo.strip():
        return []
    known = "\n".join(f"- {f}" for f in store.get("facts", [])) or "- (nothing yet)"
    prompt = ("Extract EVERY durable fact about the person that appears in this conversation: "
              "name, nationality, work, where they live or work, tastes, hobbies, plans, "
              "relationships, anything they said about themselves.\n"
              "If one sentence of theirs contains several facts, pull them ALL out separately.\n"
              "Do NOT invent anything that was not said. Do not repeat facts you already know. "
              "Do not include anything about yourself, the machine.\n"
              "If there is genuinely no new fact, answer exactly: NOTHING\n"
              "Format: one fact per line, short sentence, no numbering, no dashes.\n"
              "Example of the format:\nHer name is Marta\nShe is from Seville\nShe works as a "
              f"nurse\n\nYOU ALREADY KNOW:\n{known}\n\nCONVERSATION:\n{convo}")
    r = grid.call_openai("nvidia", MODEL, [{"role": "user", "content": prompt}],
                         max_tokens=240, temperature=0.2, timeout=timeout)
    if not r.get("ok"):
        return []
    txt = _strip_think(r.get("text", ""))
    have = {f.lower() for f in store.get("facts", [])}
    new = []
    for line in txt.splitlines():
        f = line.strip(" -*\t.").strip()
        if (len(f) < 6 or f.upper().startswith(("NOTHING", "NADA")) or f.lower() in have):
            continue
        if not is_fact(f):
            continue
        new.append(f); have.add(f.lower())
    store["facts"] = (store.get("facts", []) + new)[-40:]
    return new


def say(text, voice: str = VOICE, mute: bool = False, stop=None,
        filler: str = "", filler_n: int = 0, filler_text: str = "") -> dict:
    """Speak it aloud, sentence by sentence, starting before the sentence after it exists.

    `text` may be a string OR an iterator of deltas from `grid.stream_openai`. With deltas the
    first sentence is rendered the moment it is complete, so the person waits ONE clause instead
    of the whole reply, and the wait stops growing with the length of the answer.

    `stop` is a threading.Event that cuts the speech mid-sentence - barge-in. The old half-duplex
    guarantee (mic hard-muted for all of step 4) was honest but it made the machine impossible to
    interrupt, and being unable to stop a talking machine is the single thing that most makes it
    not feel like a conversation.

    Returns a RECEIPT - never a bare bool, so a silent failure cannot masquerade as a spoken reply.
    TTFA is the number to watch; `play` is just the audio's own duration and was the number
    previously misread as "the voice is slow"."""
    if not text:
        return dict(ok=False, engine="muted", ttfa=None, render=0.0, play=0.0,
                    chunks=0, spoken="", interrupted=False)
    r = speak.say_stream(text, voice=voice, stop=stop, mute=mute,
                         filler=filler, filler_n=filler_n, filler_text=filler_text)
    if r["ok"]:
        return dict(ok=True, engine=voice, ttfa=r["ttfa"], render=r["render_s"], play=r["play_s"],
                    chunks=r["chunks"], spoken=r["spoken"], interrupted=r["interrupted"])
    # Every chunk failed to render. Fall to the local floor rather than going silent - but say so
    # in the receipt, because a fallback that hides itself makes the gap permanent.
    flat = r["spoken"] or (text if isinstance(text, str) else "")
    ok = speak.sapi_speak(flat) if flat else False
    return dict(ok=ok, engine="sapi (robotic - edge render failed)", ttfa=None,
                render=r["render_s"], play=r["play_s"], chunks=0, spoken=flat,
                interrupted=r["interrupted"])


# DETERMINISTIC TOOL PRE-FILTER. A rod handed a tool schema reaches for it: measured 2026-07-29,
# `llama-3.1-8b` called `list_tools` for "Hey, how's it going?" AND for a question about an opinion,
# under a system prompt that said in plain words to answer NO unless a fact was needed. That is not
# a prompting failure to be fixed with better wording - the previous session recorded the identical
# behaviour ("a systematic tool-calling bias that SURVIVED an explicit written exclusion"), and law
# B5 says a rule the model can talk past is a decoration.
#
# So the schema is not offered at all unless the WORDS plausibly need one. Deterministic, so ZERO
# is a real answer (law W2). A false negative costs one clumsy reply; a false positive costs a
# spurious round trip and a holding phrase on every greeting, which is what makes it feel robotic.
_NEEDS_TOOL = (
    (re.compile(r"\d[\d,\. ]*\s*(?:times|x|\*|plus|\+|minus|-|divided by|/|over)\s*\d|"
                r"\b(?:multiply|divide|calculate|compute|square root|percent(?:age)? of)\b", re.I),
     ("calc",)),
    # ADVERB-TOLERANT. MEASURED 2026-07-29: "What can you ACTUALLY do right now?" matched nothing,
    # because the pattern demanded "what can you do" as adjacent words. One inserted adverb turned
    # a self-knowledge question into a hallucination. A pre-filter that is brittle in the exact
    # place people are emphatic is worse than none - emphasis is WHY they inserted the word.
    (re.compile(r"\bwhat (?:\w+\s+){0,2}?(?:can|do) you (?:\w+\s+){0,2}?(?:do|offer|handle)\b|"
                r"\bwhat (?:are your|tools)|your (?:tools|capabilities)\b|"
                r"\blist your tools\b|\bwhat are you (?:\w+\s+){0,2}?able\b", re.I),
     ("list_tools",)),
    (re.compile(r"\b(?:your |the )?(?:state|heartbeat|memory|journey|save) file\b|"
                r"\bread_state\b|\bstate\.json\b", re.I), ("read_state",)),
    # NATURAL PHRASING, not command phrasing. Live run 2026-07-29: "Tell me about the news" matched
    # nothing, because the pattern demanded "news about" and he said "about the news". People do not
    # say "search for"; they say "what's new", "any news", "tell me about the news".
    (re.compile(r"\b(?:search|look\s+up|google|latest|current|the\s+news|news\s+about|who\s+won|"
                r"what\s+happened|what'?s?\s+(?:new|happening|going\s+on)|any\s+news)\b",
                re.I), ("web_search", "web_fetch", "json_get")),
    # TALKING TO THE ARCHITECTURE, not to a companion beside it. These are questions about the
    # ENTITY - how it is built, what rules bind it, what it is allowed to do, whether it is healthy.
    (re.compile(r"\b(?:how many modules|your (?:structure|architecture|laws|invariants|"
                r"capabilities|permissions|code)|what are you made of|how are you built|"
                r"what rules|are you (?:healthy|ok|working)|orphaned|reachable|"
                r"self ?check|what is aea|autonomous entity)\b", re.I), ("self_map",)),
)


# Tools that are LOCAL, FREE and side-effect-free, so there is no reason to ask a model whether to
# run them. Anything that spends, or reaches off this machine, stays model-decided (law B3).
PREFETCH = ("self_map", "list_tools")


# AN EXPLICIT ASK FOR DEPTH. These are the shapes where a long answer is the CORRECT answer.
_WANTS_DEPTH = re.compile(
    r"\b(?:tell\s+me\s+(?:a|about|more)|explain|walk\s+me\s+through|elaborate|go\s+deeper|"
    r"in\s+detail|the\s+whole\s+story|a\s+story|describe|teach\s+me|how\s+does\b.*\bwork|"
    r"why\s+(?:does|do|is|are)|what\s+happened|talk\s+to\s+me\s+about|give\s+me\s+the\s+long)\b",
    re.I)


def reply_budget(user_text: str) -> tuple:
    """How long may this reply be. Returns (max_tokens, max_chars, max_sentences).

    LENGTH SCALES WITH THE REQUEST. Luis, after the first live run: "if the AI has to tell me a
    story, I want it to continue as long as it has to. I don't want it to get short on the
    responses if it doesn't need to."

    He is right, and the flat cap I had just tightened was the wrong correction. The live failure
    was never that long answers are bad - it was 15 to 22 SECONDS of answer to the words "I know"
    and "more sarcastic". The length was wrong FOR THAT TURN, not wrong in general. A fixed cap
    fixes the second thing and breaks the first.

    Deterministic, so a turn's budget is predictable and testable (law W2):
      an explicit ask for depth   generous - a story is allowed to be a story
      a real question             room to answer it properly
      anything else               conversational, because most turns are

    At the measured ~15 chars/s: 190 chars is ~13s, 420 is ~28s, 900 is ~60s.
    """
    t = (user_text or "").strip()
    words = len(re.findall(r"[a-zA-Z']+", t))
    if _WANTS_DEPTH.search(t):
        return (700, 1600, 14)               # a story, an explanation - as long as it needs
    if t.endswith("?") or words >= 12:
        return (200, 430, 5)                 # a real question deserves a real answer
    return (90, 190, 2)                      # ordinary conversational back-and-forth


def tools_for(text: str, allow: tuple) -> tuple:
    """Which of this seat's tools are plausibly needed for THIS utterance. Empty means: do not
    even advertise a schema, so no tool call is possible and the rod simply talks."""
    if not allow:
        return ()
    want: set = set()
    for pat, names in _NEEDS_TOOL:
        if pat.search(text or ""):
            want.update(n for n in names if n in allow)
    return tuple(sorted(want))


def act_or_answer(user_text: str, turns: list, system: str, allow: tuple, zone: str,
                  receipt: dict, hold_n: int = 0, voice: str = VOICE, mute: bool = False,
                  heard: str = "", notice_kind: str = ""):
    """ONE TURN THAT CAN ACT. Returns a generator of speakable deltas.

    THE SHAPE, and it comes from the turn-taking literature rather than from taste. A person
    expects a reply gap near 200ms and starts talking over the agent past 1 second. We cannot put
    a real answer there - the fastest measured rod needs 0.626s to write one and the voice needs
    another 0.5s on top. So the turn is split:

      1. the REFLEX rod (measured ttfb 0.287s) answers directly when it can, with the tool schema
         attached so it can instead say "I need a tool"
      2. if it wants a tool, a TRUE holding phrase is spoken WHILE the tool runs - not a stall, a
         status. "Let me check" is a receipt about what is happening
      3. the tool result goes back to the answering tier, which speaks the real reply

    Tools run through `hands.invoke`, which re-checks the seat, the zone and the trust ledger at
    the call site. Advertising a tool to a rod is not permission (law B5) - what the rod does with
    the schema is its business, and the gate refuses regardless.
    """
    msgs = [{"role": "system", "content": system}]
    for t in turns[-KEEP_TURNS:]:
        msgs.append({"role": "user" if t["who"] == "them" else "assistant", "content": t["text"]})
    # THE PROSODY ANNOTATION IS NO LONGER GIVEN TO THE SPEAKING ROD. KILLED BY A LIVE TEST,
    # 2026-07-29, and the reason is more interesting than a bug.
    #
    # The measurement works: the same sentence spoken five ways yields ONE transcript and FOUR
    # distinct annotations, and in the live run "louder than usual, higher pitched, rising at the
    # end" on an emphatic "I know" was exactly right. The MEASURING is sound. The USING was not.
    #
    # In six minutes of real conversation, FIVE OF FIVE consecutive turns led with the prosody:
    #   "the pitch rise at the end makes me wonder - are you absolutely sure there's not a tiny
    #    part of you questioning something"
    #   "the emphasis in your voice (I've noted the louder and higher pitch) suggests there's more
    #    to 'I know' than just acknowledgment"
    #   "your frustration is palpable"
    #   "the contrast between your faster, lower-pitched tone and the pauses ... urgency with
    #    hesitation"
    # Luis had just said the transcription was failing him. It told him his frustration was
    # palpable.
    #
    # THIS IS NOT A RULE VIOLATION AND CANNOT BE FIXED BY A BETTER GUARD. The model is not
    # disobeying; it is being helpful about the most novel thing in its context, every single time.
    # `strip_attribution` also missed all of it - it catches "you are frustrated" and not "your
    # frustration", and it can never catch a PARAPHRASE of a measurement, which is what these are.
    # An output filter cannot remove a topic.
    #
    # So the annotation is still MEASURED, still stored on the receipt, and still available to the
    # background reviewer, which does not speak. What reaches the speaking rod is nothing. When the
    # activation index and shift detector exist, what reaches it will be ONE gated move - ask a
    # question - and never a description to comment on.
    receipt["heard"] = heard
    # THE NOTICING. Luis: "more about IF SOMETHING WRONG HAPPENED. Let's say someone was talking
    # and shut up before a moment, then it can ask, what is happening?"
    #
    # This is the ONLY prosody-derived thing that reaches the speaking rod, and it arrives as an
    # INSTRUCTION TO ASK rather than as a measurement to comment on. That distinction is the whole
    # fix: given "spoke 60% shorter than usual with falling pitch" the model narrated it back at
    # him ten turns out of ten; given "ask what happened, briefly", there is nothing to narrate.
    # It fires on a CHANGE, at most once every few turns, and usually never.
    if notice_kind:
        msgs.append({"role": "system", "content": prosody.NOTICE_PROMPT.get(notice_kind, "")})
        receipt["noticed"] = notice_kind
    msgs.append({"role": "user", "content": user_text})

    # ---------------------------------------------------------------------------------------
    # SPECULATIVE PARALLEL DISPATCH. The answer to "how do we let a SMART model do the talking
    # without paying for it", and it comes from a measurement rather than a preference.
    #
    # DUET, 2026-07-29: the 49B reached its first token in 0.384 / 0.469 / 0.473 / 0.629s. The 8B
    # measured 0.456s. **Time to first token is essentially the same.** A big rod is not slow to
    # START; it is slow to FINISH, because it writes more - and length is already capped.
    #
    # So the earlier design was wrong in a way a person can hear: it let the small rod DO THE
    # TALKING because it was "fast", and bought nothing while losing every bit of depth. Luis
    # heard that immediately - "you cannot just have a very basic model having the conversation."
    #
    # Both rods now fire AT THE SAME MOMENT:
    #   the SMART rod starts streaming the actual reply, immediately
    #   the FAST rod decides, in parallel, whether a tool is needed
    # The first spoken chunk needs a whole sentence to accumulate (~1-2s), and the fast rod's
    # verdict lands at ~0.7s - so the decision almost always arrives BEFORE a syllable is
    # committed. No tool: the smart stream was already flowing and cost nothing. Tool wanted: the
    # smart draft is discarded unspoken, and the holding phrase covers the tool.
    #
    # The cost is one extra cheap call per turn. The gain is that the voice is the good rod.
    # ---------------------------------------------------------------------------------------
    import concurrent.futures
    fast = tiers.organ("reflex")
    smart = tiers.organ("voice")
    maybe = tools_for(user_text, allow)          # deterministic: usually () -> no triage at all

    # PRE-FETCH WHAT IS FREE AND LOCAL, RATHER THAN HOPING THE ROD ASKS FOR IT.
    #
    # MEASURED 2026-07-29: asked "How are you built? How many modules?" with `self_map` OFFERED,
    # the rod called nothing and answered "I'm built using a transformer... around a dozen
    # components" - a fabrication about its own structure, which is the single thing this tool
    # exists to prevent. Offering a tool is a HOPE; the model may decline, and here it declined
    # into invention.
    #
    # So the rule is drawn on COST, not on capability: introspection that is local, free and free
    # of side effects is FETCHED and injected as fact. Anything that spends, or reaches outside
    # this machine, still needs the model to ask for it - because a pre-fetched web search would
    # be an outbound request nobody decided to make (law B3).
    facts = []
    for name in maybe:
        if name not in PREFETCH:
            continue
        try:
            facts.append("%s ->\n%s" % (name, hands.invoke(name, {"topic": user_text},
                                                           zone=zone, allow=allow)))
        except hands.Refused:
            pass                                 # the gate said no; that is an answer, not an error
        except Exception:
            pass
    if facts:
        msgs[-1]["content"] += (
            "\n\nMEASURED FACTS ABOUT YOURSELF, read from your own state just now. Answer from "
            "THESE. Do not estimate, do not round, and do not describe yourself in general terms "
            "about language models - these are the real numbers:\n" + "\n".join(facts))
        maybe = tuple(n for n in maybe if n not in PREFETCH)

    schema = hands.schema(maybe) if maybe else None
    receipt["tools_offered"] = maybe
    receipt["prefetched"] = [f.split(" ->")[0] for f in facts]

    # THE TRIAGE GETS ITS OWN FRAMING, NOT THE CONVERSATIONAL ONE. MEASURED 2026-07-29: handed the
    # companion's full system prompt, the fast rod answered "what do you think about running a mind
    # on a laptop" by calling `list_tools` - a tool call for a question about an opinion. The
    # conversational prompt invites engagement, and an engaged rod reaches for a tool. Its ONLY job
    # here is a yes/no about facts it cannot know, so it is asked that question and nothing else.
    triage_msgs = ([{"role": "system", "content":
                     "Decide ONLY whether answering the user's last message REQUIRES a tool - that "
                     "is, whether it depends on a fact you cannot possibly know: exact arithmetic, "
                     "this machine's own stored state, a live web page, or a list of your own "
                     "tools. Opinions, greetings, chat, and anything you can answer from what you "
                     "already know need NO tool. If a tool is needed, call it. Otherwise reply "
                     "with the single word NO."}]
                   + [m for m in msgs[1:]])
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    # positional: (plant, model, messages, max_tokens, temperature, timeout, tools)
    triage = (pool.submit(grid.call_openai, fast["plant"], fast["model"], triage_msgs,
                          120, 0.0, fast["budget"], schema) if schema else None)

    tr: dict = {}
    srec: dict = {}
    # 90 TOKENS, NOT 160. Bounding the PLAYBACK was not enough: the live run produced 12 to 22
    # seconds of speech on every turn, and a cap that truncates mid-sentence is a worse artifact
    # than a short answer. Bound it at the source so the rod writes a conversational reply rather
    # than an essay that gets cut off.
    tok_budget, char_budget, sent_budget = reply_budget(user_text)
    receipt["budget"] = dict(tokens=tok_budget, chars=char_budget, sentences=sent_budget)
    stream = grid.stream_openai(smart["plant"], smart["model"], msgs, max_tokens=tok_budget,
                                temperature=0.8, timeout=smart["budget"], receipt=srec)
    draft, decided, calls = "", (triage is None), []
    try:
        for piece in stream:
            draft += piece
            if not decided:
                # Hold the draft only until the triage verdict lands - never longer. A first
                # sentence takes ~1-2s to accumulate and the verdict takes ~0.7s, so this
                # normally returns instantly and adds nothing to time-to-first-audio.
                try:
                    tr = triage.result(timeout=max(0.0, fast["budget"] - (srec.get("ttfb") or 0)))
                    calls = (tr.get("tool_calls") or []) if tr.get("ok") else []
                except Exception:
                    calls = []
                decided = True
                if calls:
                    stream.close()          # discard the draft UNSPOKEN and take the tool path
                    break
            if decided and not calls:
                yield piece
    finally:
        pool.shutdown(wait=False)
        # THE RECEIPT MUST SURVIVE AN EARLY CLOSE, AND THIS IS THE THIRD TIME TONIGHT.
        # `speakable` stops at the sentence cap, raising GeneratorExit into this frame at the
        # `yield` above, so anything written AFTER the try block never runs. The live test then
        # reported `None/? ttfb None` on every single turn and blinded the measurement it existed
        # to take. I fixed exactly this in `think_stream` with a `finally` hours earlier, and then
        # wrote the same shape again here. Law M9: the cheap glue between a producer and a
        # consumer is the part that never gets audited.
        if not calls:
            receipt.update(plant=smart["plant"], model=smart["model"], tier="voice", acted=False,
                           ttfb=srec.get("ttfb"), ok=srec.get("ok"), error=srec.get("error"),
                           status=srec.get("status"))

    if not calls:
        if (srec.get("text") or "").strip():
            return
        # empty content is a NON-ANSWER, not an answer (D13: a reasoning rod can spend its whole
        # budget in `reasoning` and return nothing). Fall through the ladder.
        for piece in think_stream(user_text, turns, system, receipt):
            yield piece
        return
    r = tr
    receipt.update(plant=fast["plant"], model=fast["model"], tier="reflex",
                   ttfb=round(float(r.get("latency") or 0), 3), ok=r.get("ok"),
                   error=r.get("error"), status=r.get("status"))

    # A TOOL WAS ASKED FOR. Speak the true holding phrase while it runs.
    holder = None
    if not mute:
        phrase = tiers.hold("tool", hold_n)
        holder = threading.Thread(target=lambda: speak.say_stream(phrase, voice=voice),
                                  daemon=True)
        holder.start()

    msgs.append({"role": "assistant", "content": r.get("text") or "", "tool_calls": calls})
    trace, refused = [], []
    for tc in calls:
        name = (tc.get("function") or {}).get("name", "?")
        try:
            args = json.loads((tc.get("function") or {}).get("arguments") or "{}")
        except Exception:
            args = {}
        try:
            # STATE THE EXACT DESTINATION BEFORE REACHING IT. Copied from NVIDIA's aiq-research
            # protocol and required by law B3: the model composed this address, so the request
            # itself is the outbound channel. It is printed even when nobody is watching, because
            # a boundary that only announces itself on demand is not a boundary.
            if name in ("web_fetch", "json_get"):
                print(f"      OUTBOUND {name} -> {str(args.get('url'))[:120]}", flush=True)
            out = hands.invoke(name, args, zone=zone, allow=allow)
            trace.append({"tool": name, "args": args, "out": out[:200]})
            print(f"      TOOL {name}({json.dumps(args)[:60]}) -> {out[:80]}", flush=True)
        except hands.Refused as e:
            out = "REFUSED: %s" % e
            refused.append({"tool": name, "why": str(e)})
            print(f"      TOOL {name} REFUSED: {e}", flush=True)
        msgs.append({"role": "tool", "tool_call_id": tc.get("id", ""), "content": str(out)[:2000]})
    receipt.update(acted=True, calls=trace, refused=refused)

    if holder:
        holder.join(timeout=8)          # never speak over ourselves - the audio device is one
    # THE ANSWERING TIER reads the tool output and says what it found. It is told to report the
    # RESULT, because a tool call is a step and the person asked for an outcome (law G1).
    for piece in think_stream(user_text, turns, system, receipt, prebuilt=msgs):
        yield piece


def think_stream(user_text: str, turns: list, system: str, receipt: dict, prebuilt=None):
    """Stream the mind. Yields text deltas from the first rod that actually produces content.

    Same ladder as `think`, same latency budgets, but the fallback decision has to be made on the
    FIRST DELTA rather than on the finished reply - once a syllable has been spoken aloud we are
    committed to that rod. So a rod that opens its mouth owns the turn; a rod that returns nothing
    at all falls through silently, which is exactly the case D13 recorded (a reasoning rod burning
    its whole budget in `reasoning` and returning empty content)."""
    if prebuilt is not None:
        msgs = prebuilt                            # a turn that already ran a tool: the trace is
    else:                                          # in here and must not be rebuilt away
        msgs = [{"role": "system", "content": system}]
        for t in turns[-KEEP_TURNS:]:
            msgs.append({"role": "user" if t["who"] == "them" else "assistant",
                         "content": t["text"]})
        msgs.append({"role": "user", "content": user_text})
    for plant, m, budget in RODS:
        rec: dict = {}
        got = False
        t0 = time.time()
        try:
            for piece in grid.stream_openai(plant, m, msgs, max_tokens=160, temperature=0.7,
                                            timeout=budget, receipt=rec):
                got = True
                yield piece
                # THE LATENCY BUDGET HAS TO BE ENFORCED ON THE STREAM TOO. `timeout` is an
                # INACTIVITY budget per socket read, so it bounds time-to-first-token and nothing
                # else: a rod that emits one delta every few seconds runs past its declared budget
                # forever. MEASURED 2026-07-29: a rod with a 9s budget produced first audio at
                # 14.4s. Once it has spoken we are committed to it (the person has already heard
                # a syllable), so the cap is generous - but a cap that cannot fire is not a cap.
                if time.time() - t0 > budget * 3:
                    break
        finally:
            # THE RECEIPT MUST SURVIVE AN EARLY CLOSE. `speakable` stops at the sentence cap, which
            # raises GeneratorExit into this frame at the `yield` above - so anything written after
            # the loop never ran, and the turn line reported `ttfb None` for a rod that had
            # answered in 1.68s. Three lines, written fast, structurally dead: law M9, found by
            # pointing the instrument at a case whose answer was already known (D18).
            receipt.update(rec)
            receipt.update(plant=plant, model=m, budget_s=budget,
                           elapsed_s=round(time.time() - t0, 2))
        if got and (rec.get("text") or "").strip():
            return
    receipt.setdefault("ok", False)


# ---------------------------------------------------------------------------- the loop
def main() -> None:
    a = sys.argv[1:]
    def arg(flag, default=None):
        return a[a.index(flag) + 1] if flag in a and a.index(flag) + 1 < len(a) else default

    if "--devices" in a:
        list_devices(); return

    name = arg("--name", "") or ""
    persona = arg("--persona", "") or ""
    lang = arg("--lang", LANG)
    voice = arg("--voice", VOICE_FOR_LANG.get(lang, VOICE))
    device = arg("--device")
    device = int(device) if device is not None else None
    text_mode = "--text" in a
    mute = "--mute" in a
    logpath = arg("--log")
    keep = "--no-store" not in a                  # storage ON by default (Luis's call, 2026-07-24)
    store = load_store(name or "guest")
    if "--fresh" in a:                            # deliberate wipe - start him over from nothing
        store = {"who": name or "guest", "first_seen": time.strftime("%Y-%m-%d"),
                 "sessions": 0, "facts": [], "turns": []}
    if "--learn" in a:
        # Consolidate an EXISTING record without holding a conversation. The live loop only
        # distils facts on a clean exit, so a killed process loses them - the raw turns survive
        # and this recovers the learning from them. Do NOT run while a loop is live: both hold
        # their own copy of the store and the last writer would clobber the other.
        allturns = [dict(who=t["who"], text=t["text"]) for t in store.get("turns", [])]
        if not allturns:
            print("  (there is no stored conversation to consolidate)")
            return
        found: list = []
        for i in range(0, len(allturns), 24):        # chunked: remember() reads the last 24
            found += remember(store, allturns[i:i + 24])
        save_store(store)
        print(f"  {len(allturns)} turns read | {len(found)} new facts | "
              f"{len(store.get('facts', []))} in total")
        for f in found:
            print("    -", f)
        return

    # THE OUTBOUND BOUNDARY, DECIDED DELIBERATELY (2026-07-29) RATHER THAN INHERITED.
    #
    # This companion holds real personal facts about whoever it talks to - `converse_angelo.json`
    # carries nine. Law B3: a read tool is an OUTBOUND CHANNEL the moment the model writes the
    # address, so handing that same context `web_fetch` by default puts every stored fact one
    # composed hostname away from leaving. `hands` already binds the network tools to the public
    # zone; this narrows it further, at the seat.
    #
    #   default   calc, read_state    local, no network, permitted in every zone
    #   --online  + web_fetch, json_get, and the exact URL is SPOKEN AND PRINTED before the request
    #
    # `--no-tools` exists so the plain conversational path stays measurable on its own.
    online = "--online" in a
    if "--no-tools" in a:
        allow, zone = (), "sensitive"
    elif online:
        allow, zone = ("calc", "read_state", "list_tools",
                       "web_search", "json_get", "web_fetch"), "public"
    else:
        # `list_tools` is pure introspection over the registry - no network, nothing leaves - so it
        # belongs in the default seat. It is what lets the entity ANSWER A QUESTION about its own
        # hands rather than only use them, which is the difference between having tools and being
        # aware of them.
        allow, zone = ("calc", "read_state", "list_tools"), "sensitive"

    store["sessions"] = int(store.get("sessions", 0)) + 1
    system = build_system(name, persona, store.get("facts"), lang=lang)
    # WITHOUT THIS LINE THE ANNOTATION IS A HAZARD, not a feature: a bracketed clause appended to
    # the user's turn reads as WORDS THEY SAID, and the mind would answer the measurement instead
    # of the person. Same class as D13's whisper artifacts being answered as speech - an unlabelled
    # signal becomes a fabricated utterance.
    system += ("\nHOW THEY SOUND: some turns end with a bracketed note like "
               "[heard: slower than usual, pitch rising at the end]. That is NOT something they "
               "said - it is a measurement of their voice from the microphone, against their own "
               "normal. Let it inform how you respond. Do NOT read it aloud, do not quote it, and "
               "do not tell them what they are feeling: you measured pitch and pace, not emotion. "
               "If it matters, ask.")
    if allow:
        system += ("\nTOOLS: you have real tools and their results are REAL. Call one when the "
                   "answer depends on a fact you cannot know - arithmetic, the machine's own "
                   "state, a live page. Never guess a number you could compute. When a tool "
                   "returns, say what it actually returned; do not embellish it.")
    # THE MACHINE'S OWN PAST OUTPUT IS ITS STYLE GUIDE, so a bad habit persists across restarts.
    #
    # MEASURED 2026-07-29: the prosody annotation was cut off from the speaking rod, and it kept
    # commenting on Luis's tone anyway - "what sounds like a neutral, almost experimental tone" -
    # with no annotation in its context at all. The store held 28 turns, and TEN OF FOURTEEN
    # machine turns talked about pitch, delivery or pauses. Seeded back as history at boot, they
    # taught the next session the habit that the code had just removed.
    #
    # This is D-3's mechanism one level up: an unverified output does not stay an output, it
    # becomes the record, and the record becomes the behaviour. Removing a capability is not
    # enough when its consequences are already written down.
    _seed = [dict(who=t["who"], text=t["text"]) for t in store.get("turns", [])]
    _dropped = [t for t in _seed if t["who"] == "me" and _VOICE_TALK.search(t["text"])]
    turns: list[dict] = [t for t in _seed if t not in _dropped][-(KEEP_TURNS * 2):]
    if _dropped:
        print(f"  history : dropped {len(_dropped)} past turns that talked about your voice, so "
              f"the habit does not seed itself")

    turn_n = [0]
    since_notice = [99]        # turns since the last noticing; seeds ready-to-fire

    def turn(said: str, heard: str = "", notice_kind: str = "") -> str:
        """One full exchange, spoken as it is thought. Returns what was ACTUALLY SAID ALOUD."""
        t0 = time.time()
        turn_n[0] += 1
        rec: dict = {}
        stop = threading.Event()
        v = say(speakable(act_or_answer(said, turns, system, allow, zone, rec,
                                        hold_n=turn_n[0], voice=voice, mute=mute, heard=heard,
                                        notice_kind=notice_kind),
                          max_sentences=MAX_SENTENCES),
                voice, mute, stop=stop, filler="think", filler_n=turn_n[0],
                filler_text=said)
        reply = trim((v.get("spoken") or "").strip(), MAX_SENTENCES)
        if not reply:
            reply = "Sorry, I lost the connection for a second. Can you say that again?"
            print(f"  [rod failed: {str(rec.get('error'))[:90]}]")
            src = "no rod"
            say(reply, voice, mute)
        else:
            src = (f"{rec.get('plant')}/{str(rec.get('model') or '?').rsplit('/', 1)[-1]} "
                   f"ttfb {rec.get('ttfb')}s")
        # THE RECORD HOLDS WHAT WAS HEARD, NOT WHAT WAS GENERATED. With barge-in these differ: the
        # rod may write three sentences and the person may cut in after the first. Storing the
        # generated text would put words in the model's own history that nobody ever heard, and it
        # would then refer back to them - a fabricated memory of its own speech. Same law as D13's
        # microphone filters, one layer further out.
        turns.append({"who": "them", "text": said})
        turns.append({"who": "me", "text": reply})
        if len(turns) > KEEP_TURNS * 2:              # bounded - nothing grows forever
            del turns[:-(KEEP_TURNS * 2)]
        print(f"\n  IT > {reply}")
        if keep:
            stamp = time.strftime("%Y-%m-%d %H:%M")
            store.setdefault("turns", []).append({"t": stamp, "who": "them", "text": said})
            # PROVENANCE ON THE RECORD. MEASURED 2026-07-29, and it is an honesty defect: a turn
            # where the tool did NOT run produced "the result is 414,419,987" - wrong, invented -
            # and the next turn read its own stored answer as an established fact and repeated it.
            # An unverified output does not stay an output; it becomes a remembered fact, exactly
            # as D13 found at the microphone. Recording WHICH tool produced a value is the
            # cheapest thing that lets a later turn tell a computed number from a guessed one.
            me = {"t": stamp, "who": "me", "text": reply}
            if rec.get("calls"):
                me["tools"] = [{"tool": c["tool"], "out": c["out"][:80]} for c in rec["calls"]]
            store["turns"].append(me)
            store["turns"] = store["turns"][-600:]   # bounded - nothing grows forever
            save_store(store)
        if logpath:                                  # extra plain-text log, opt-in
            with open(logpath, "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%H:%M')} {name or 'them'}: {said}\n"
                        f"{time.strftime('%H:%M')} machine: {reply}\n")
        print(f"      [{src} | first audio {v['ttfa']}s | {v['chunks']} chunks "
              f"render {v['render']}s speech {v['play']}s"
              + (" | CUT OFF" if v.get("interrupted") else "")
              + f" | turn {round(time.time() - t0, 1)}s]\n")
        return reply

    def finish() -> None:
        """Close the session: save the record, then CONSOLIDATE it into durable facts."""
        if not keep:
            print("\n  (nothing was stored)")
            return
        save_store(store)
        print(f"\n  stored: {len(store.get('turns', []))} turns in state/converse_*.json")
        try:
            new = remember(store, turns)
        except Exception as e:
            print(f"  (consolidation failed: {str(e)[:70]})")
            return
        if new:
            save_store(store)
            print("  LEARNED this session:")
            for f in new:
                print(f"    - {f}")
        else:
            print("  (nothing new and solid to learn from this session)")

    if "--once" in a:                                # scripted single turn (verification path)
        if not mute:
            speak.warm(voice)                        # the verification path must pay the SAME
                                                     # costs as the real one, or it measures a
                                                     # machine nobody runs: without this, --once
                                                     # reported a 1.5s cold render as normal
        turn(arg("--once", "hello"))
        finish()                                     # exercise the save + consolidate path too
        return

    # ---- boot ---------------------------------------------------------------------------
    print("=== THE COMPANION ===")
    print(f"  mind  : {MODEL.rsplit('/', 1)[-1]} (NVIDIA, no-train rod, streamed)")
    print(f"  voice : {voice}" + ("  [MUTED]" if mute else ""))
    print(f"  ears  : whisper-base local, language {lang}" + ("  [TEXT MODE]" if text_mode else ""))
    print(f"  disk  : " + (f"state/converse_*.json - session #{store['sessions']}, "
                           f"{len(store.get('turns', []))} previous turns, "
                           f"{len(store.get('facts', []))} facts remembered"
                           if keep else "nothing is stored")
          + (f" (+ log {logpath})" if logpath else ""))
    if not text_mode:
        if not listen.available():
            print("\n  ERROR: cannot find the whisper model in voice/. Use --text.")
            return
        print("\n  warming the ear (~25s the first time, then 0.2s per turn)...", flush=True)
        print(f"  ready in {listen.warm(lang)}s")
    # WARM THE VOICE TOO. MEASURED 2026-07-29: the first edge render of a process costs 1.18-1.82s
    # against 0.5s warm, because the connection is cold. D13 learned exactly this for whisper
    # ("warm it at boot or the first thing anyone says costs 20 seconds") and the lesson was never
    # carried across to the mouth. The knowledge was present and not applied - which is the part
    # of a recorded failure that actually stops recurrence (law W8).
    if not mute:
        tw = time.time()
        speak.warm(voice)
        # THE THINKING SOUNDS, cached once. First run on a new voice costs ~29s; every run after
        # is free, and it turns a 2.16s silence into ~0.4s before the first human sound.
        nf = speak.prime_fillers(voice)
        print(f"  voice warm in {round(time.time() - tw, 2)}s ({nf} thinking sounds ready)")

    # The greeting DISCLOSES what this is and that it keeps a record. Consent is a property of
    # the system, not a promise made about it - they are told, out loud, before they say anything.
    known = store.get("facts") or []
    greet = ((f"Hi {name}. " if name else "Hi. ")
             + "I am a machine, a voice program running on Luis's computer. "
             + ("We have talked before and I remember what you told me. " if known else "")
             + ("I keep what we say, so I remember next time. " if keep else "")
             + "Go ahead.")
    print(f"\n  IT > {greet}\n")
    say(greet, voice, mute)

    while True:
        try:
            if text_mode:
                said = input("  YOU > ").strip()
                if not said:
                    continue
            else:
                notice_kind = ""
                samples, early = capture(device, lang=lang)
                if samples is None:
                    continue
                t0 = time.time()
                # Reuse the semantic endpoint's transcript when it produced one: it read the SAME
                # buffer we would re-read, so a second pass costs 0.2s to learn nothing new.
                said = (early or listen.transcribe_samples(samples, SR, lang)).strip()
                if is_ghost(said):
                    print("  (noise, not a sentence)")
                    continue
                print(f"  YOU > {said}   [{round(len(samples) / SR, 1)}s of audio, "
                      + (f"endpointed early, transcript reused]" if early
                         else f"heard in {round(time.time() - t0, 2)}s]"))
                # HOW it was said, measured off the same samples we already hold. ~8ms.
                try:
                    _basefore = store.get("voice_baseline") or {}
                    heard, _pm, store["voice_baseline"] = prosody.annotate(
                        samples, SR, said, _basefore)
                    if heard:
                        print(f"        [heard: {heard}]")
                    # a CHANGE worth asking about - rare by construction
                    notice_kind = prosody.notice(_pm, _basefore, since_notice[0])
                    since_notice[0] = 0 if notice_kind else since_notice[0] + 1
                    if notice_kind:
                        print(f"        [noticed: {notice_kind} -> it will ASK, not diagnose]")
                except Exception:
                    heard, notice_kind = "", ""   # a broken prosody read must never cost a turn
        except (EOFError, KeyboardInterrupt):
            finish()
            break
        if said.lower().strip(" .!?¡¿") in _BYE:
            bye = "See you. It was good talking to you."
            print(f"\n  IT > {bye}\n"); say(bye, voice, mute)
            finish()
            break
        try:
            turn(said, heard, notice_kind)
        except KeyboardInterrupt:
            finish()
            break


if __name__ == "__main__":
    main()
