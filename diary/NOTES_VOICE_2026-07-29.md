# NOTES - THE VOICE, THE TIERS, AND THE HANDS (2026-07-29, second session of the day)

*Written because Luis asked for notes that accumulate. Every defect below carries the four parts
law W8 requires: the rule, the failure that paid for it, HOW IT SHOULD HAVE BEEN BUILT, and WHY the
knowledge that would have prevented it was present and not applied. The fourth is the only one that
stops recurrence.*

**The one line:** we set out to make the voice fast and found the voice was never slow. Eleven
defects, nine of them in our own instruments or records, against zero models behaving unexpectedly.
D18 again, and this time it included the reading of a receipt.

---

## 0 · WHAT CHANGED

```
converse.py    ENGLISH end to end. Streamed mind, sentence-chunked speech, barge-in, tools.
grid.py        + stream_openai()  SSE transport, deltas, receipt filled in place
speak.py       + say_stream() sentence pipeline + warm() + split_sentences()
tiers.py       NEW. aea/mind/tiers.py - which rod owns which organ, and the measurement that earned it
rods.json      + `conversational` block on 21 rods: ttfb/ttlt measured on a real spoken turn
tool_rods.json + 10 rods probed for tool calling, including the two that were UNMEASURED
```

Selfcheck: **7 invariants PASS, 46 frozen behaviours hold, 113 modules.**

---

## 1 · THE MEASUREMENT THAT OVERTURNED THE HANDOFF

The handoff said *"VOICE synthesis is the bottleneck at 14.7s of a 16.2s turn."* It is not, and it
never was. The receipt prints `voz {render}s+{play}s` and **14.7 was the PLAY field** - the audio's
own duration. The entity was not slow at talking. It said too much, and could not be stopped.

```
chars   edge render (warm)   audio produced   rtf
    3          0.51s             1.78s        0.29
   35          0.46s             3.29s        0.14
  196          0.61s            13.27s        0.05
  367          0.75s            24.41s        0.03
```

**edge-tts render is ~0.5s FLAT at any length** - it is one network round trip, not a per-character
cost. A 367-character reply is 24.4 SECONDS of speech.

**No engine is worth switching to on this machine.**

| engine | render | rtf | notes |
|---|---|---|---|
| edge es/en neural | 0.51s | 0.079 | free, natural, cloud |
| kokoro-en-v0_19 (local, on disk) | 1.82s | 0.31 | English voice; 3x slower |
| kokoro-multi-lang-v1_1 (on disk, never referenced in code) | 1.33s | 0.25 | en+zh only, emitted `Unknown token` on Spanish |
| NVIDIA hosted TTS | - | - | **does not exist on our REST path** |

`/v1/models` returns 102 ids; the only speech-shaped ones are `riva-translate-*`, which is text
translation. Magpie TTS resolves to `grpc.nvcf.nvidia.com:443` - a different protocol, a different
client, cloud-only. **Chatterbox / CosyVoice2 / Fish S2 all quote their latency ON A GPU** (Fish's
100ms is on an H200). This machine measured `torch 2.13.0+cpu, cuda_available=False`. A CUDA build
is a decision, not a default.

**Honest latency, n=4, warm, after everything:**

```
TTFB (mind, first token)   median 1.40s   range 0.93-2.28
TTFA (first audible)       median 4.24s   range 2.36-5.29
```

The mind is ~80% of the wait. The voice is ~13%.

---

## 2 · THE PSYCHOLOGY, WHICH IS THE ARCHITECTURE

Human conversation runs on a turn gap of about **200ms** - Stivers et al. 2009, ten languages, four
continents, culture-independent. Past ~300ms a delay is perceived unconsciously; past ~500ms it is
noticed; past **1 second people talk over the agent or leave**.

We are at 4.24s and **no rod reachable from here closes that gap**. The fastest measured time to
first token is 0.287s and the voice needs ~0.5s on top, so the floor for a real answer is ~0.8s
even with the best rod - and the rod that answers WELL is slower than the rod that answers FAST.

So the fix is the one conversation itself uses: **say something true immediately while the real
answer is still being written.** The dialogue-systems literature calls these backchannels and
filled pauses; they hold the floor and measurably reduce perceived wait. They are honesty-safe
because "let me check" is a TRUE statement about what is happening - a receipt, not a claim.

**The state of the art we cannot reach, and why it is recorded anyway:** Voice Activity Projection
(Ekstedt & Skantze) predicts both speakers 2s ahead from 30s of context and detects turn-shifts,
backchannels and interruptions. Full-duplex models (Moshi/Kyutai) run parallel user-audio,
assistant-audio and inner-monologue streams at ~200ms. Both need a GPU. **Semantic endpointing is
the piece that transfers to CPU**, and it is implemented (see defect 9).

---

## 3 · THE TIERED MIND (aea/mind/tiers.py)

Luis: *"maybe we need a chain of models, different parts, different functionality, and it comes
together as one."* The measured data says this is right, and says exactly how.

```
organ    rod                                      ttfb    whole   tools
reflex   meta/llama-3.1-8b-instruct              0.456s  0.724s   PASS 1.1s
voice    nvidia/llama-3.3-nemotron-super-49b-v1  0.366s  1.506s   PASS 3.0s
depth    nvidia/nemotron-3-ultra-550b-a55b       1.803s  2.050s   unstable
local    ollama/nemotron-3-nano:4b                  -       -     PASS
```

**This is NOT a council.** x11 measured a cross-rod council TYING its best member at 5x cost.
Nothing here votes. Each organ owns a job it was MEASURED best at; the composition is a route.

`tiers.refresh_from_store()` re-reads both stores and reports drift, but **never re-assigns** -
autonomy is granted, not taken (law G5).

---

## 4 · THE DEFECTS, each with all four parts

### D-1 · The receipt was structurally dead (law M9, the worst one)
- **Failure:** the turn line reported `ttfb None` for a rod that had answered in 1.677s. The receipt
  dict came back with `keys=[]` - completely empty.
- **Cause:** `speakable` stops at the 2-sentence cap. `return` raises `GeneratorExit` into
  `think_stream` AT THE YIELD, so `receipt.update(rec)` after the loop never ran.
- **Should have been:** the update in a `finally`, from the first version.
- **Why not prevented:** law M9 was READ ALOUD at the start of this session - "the component you
  wrote fastest is the one you checked least" - and then a three-line aggregation was written fast
  and not checked. This is the SECOND session in a row where a three-line aggregation was
  structurally dead (`[] and append()` was the last one). **The shape to watch is: cheap glue that
  moves a value from a producer to a consumer.**

### D-2 · The streaming path could not enforce a latency budget
- **Failure:** a rod with a declared 9s budget produced first audio at 14.4s.
- **Cause:** `timeout` on a stream is an INACTIVITY budget per socket read. It bounds time to first
  token and nothing after it, so a slow-streaming rod runs unbounded.
- **Should have been:** a wall-clock deadline checked inside the delta loop from the start.
- **Why not prevented:** the previous session recorded "`timeout=None` means a generous INACTIVITY
  budget, never a deadline" and I applied that knowledge to the VALUE and not to the SEMANTICS.
  The same sentence contained the answer.

### D-3 · A fabricated number spoken aloud
- **Failure:** "The result is 414,419,987." Correct: 415,074,227. Said with confidence, out loud.
- **Cause:** the tool did not run; the model did the arithmetic in its head. AND the stored history
  already contained the wrong number from a previous turn, so the rod read its own error as
  established fact and repeated it.
- **Should have been:** provenance on the stored turn from the start, so a later turn can tell a
  computed value from a guessed one.
- **Why not prevented:** D13 already recorded this EXACT mechanism at the microphone ("an
  unvalidated input does not stay an input: it becomes a fabricated memory, recited later with
  confidence"). It was recorded for INPUTS and never carried to OUTPUTS. **Fixed:** stored turns
  now carry `tools: [{tool, out}]`.

### D-4 · remember() wrote the model's reasoning into a person's permanent facts
- **Failure:** **8 of 9 stored "facts" about a real person were chain-of-thought.** Live since
  2026-07-24, across eight sessions with a real human being. Samples:
  *"The user wants me to extract ALL durable facts about the person"*, *"1. `el: Que es eso?` - No fact"*.
- **Cause:** `_strip_think()` removes `<think>` TAGS. This rod leaked reasoning as plain prose, so
  nothing matched, and every line became a fact.
- **Should have been:** a deterministic `is_fact()` gate from the start, or `json_schema` structured
  output (the previous session measured **9 of 9 rods pass strict json_schema** and concluded
  "always send the schema").
- **Why not prevented:** the schema finding was written down the day before and applied to the
  scout and not to the memory organ. **Fixed:** `is_fact()` - closed meta vocabulary, 110-char cap,
  single-sentence rule. Tested against the REAL leaked text, 9/9. Stores purged.

### D-5 · Stage directions were spoken aloud
- **Failure:** the voice said the word "pause". The rod wrote `*pause*`; the markdown stripper
  removed the asterisks and left the word to be read.
- **Should have been:** delete what the markers MARK, not just the markers.
- **Why not prevented:** the stripper was written for markdown formatting and never asked what a
  model actually puts between asterisks. First over-fix deleted `**Bold**` entirely - so the final
  rule is a CLOSED VOCABULARY of directions (law M8: a category is defined by its corpus).

### D-6 · The reflex seat was filled on ONE axis
- **Failure:** assigned `llama-3.2-3b-instruct` for being fastest (0.287s). It **cannot call a
  tool** - it emits `<|python_tag|>{"name": "calc"...}` as plain text. The acting seat held a rod
  that can only talk about acting.
- **Should have been:** probed for BOTH properties before seating.
- **Why not prevented:** I had quoted D17/M10 ("fitness is per task SHAPE, not per rod") in this
  same session, then picked on a single number. **Fixed:** reflex = `llama-3.1-8b-instruct`,
  measured on both. The staleness checker now reads BOTH stores, so it cannot re-recommend the
  rod I just rejected.

### D-7 · Three of eight fast rods emit tool calls as TEXT
- Not our defect, but a nameable failure class: `<|python_tag|>` (llama-3.2-3b), `<toolcall>`
  (nemotron-mini-4b), ```` ```json ```` (ising-calibration-1.5-31b). The rod WANTS to call the tool
  and the endpoint never parses it into `tool_calls`. **Capable rod, unwired transport** - and it
  reads as "cannot call tools" to anyone who does not look at the text.

### D-8 · A failed render costs ~9 seconds of silence
- `play_fast` fails on a missing file, `play_mp3` falls to PowerShell WPF, which waits up to 8s for
  a `NaturalDuration` that never arrives. Any render failure = nine dead seconds. **Open.**

### D-9 · A fixed hangover makes every complete sentence pay for the incomplete ones
- 1.15s of silence before the turn even starts processing - 5x the natural human gap before the
  mind has thought at all. **Fixed:** semantic endpointing. At 0.45s, transcribe and ask whether the
  utterance is FINISHED; if yes, answer now; if it dangles ("what is the capital of"), wait the full
  hangover. Deterministic (law W2), conservative (unsure -> wait), 14/14 on unit cases. The
  transcript is REUSED, saving a second whisper pass.

### D-10 · The verification path did not pay the production costs
- `--once` returned before the boot warm and measured a 1.5s cold render as normal. **Fixed.**
- Cold render is 1.18-1.82s, warm is 0.46-0.75s. D13 learned this for whisper ("warm it at boot")
  and it was never carried to the mouth.

### D-12 · The entity described powers it did not have
- **Failure:** an offline seat holding only `calc`/`read_state`/`list_tools` told a person it could
  *"fetch live public web pages ... and even search the web."* All three are REFUSED there.
- **Cause:** `_list_tools` computed availability against a hardcoded `"public"` zone and never saw
  the actual seat, so it read out the whole registry as though it were capability.
- **Should have been:** answered for THIS seat from the first line - the gate already knows.
- **Why not prevented:** the honesty law was read as being about NUMBERS. It is not: describing a
  power you do not have is the same failure as reporting a measurement you did not take. **Fixed:**
  `invoke` passes `_zone`/`_allow` to tools declaring `wants_context`, and the output is split into
  what it can do here and what is refused here, with the reason.

### D-13 · `--mute` silently skipped the work it was meant to verify
- **Failure:** `say_stream` returned before consuming the generator, so the mind never ran and the
  tools never fired. The turn reported `rod failed` for a rod that was never asked.
- **Should have been:** mute means MAKE NO SOUND, never DO NO WORK.
- **Why not prevented:** the mute branch was a two-line early return - the cheap half again (M9),
  written while the expensive streaming pipeline beside it was audited line by line. **Fixed.**

### D-14 · Two instruments disagreed about the same bytes
- **Failure:** `web_search` parsed ZERO results from a perfectly good 23KB page. DDG lite writes
  `class='result-link'` in SINGLE quotes; the parser demanded double.
- **The interesting half:** the probe that "verified" the endpoint counted `result-link` as a bare
  substring, which matched, so the endpoint read as confirmed while the parser was broken. **A
  verification that is more permissive than the thing it verifies confirms nothing.** Match the
  verifier's strictness to the consumer's, or it is not a control.
- **Fixed:** quote-agnostic, anchored on `rel="nofollow"` + href, verified against the live page.

### D-11 · My own survey filtered on a field that does not exist
- Guessed `status` where the store has `nvidia_catalog_state`, matched nothing, and printed
  "0 served chat rods" as though it were a finding. Caught in one pass because the answer was
  already known (102 rods are served). **A detector that has never been shown a positive it must
  catch has not been tested, only run.**

---

## 5 · THE OUTBOUND BOUNDARY, DECIDED

Luis asked for this to be decided deliberately. It is:

```
default    calc, read_state          local, no network, permitted in every zone
--online   + web_fetch, json_get     public zone only; the EXACT URL is printed AND spoken first
--no-tools nothing                   so the plain conversational path stays measurable alone
```

**Reasoning:** the companion holds real personal facts about whoever it talks to. Law B3 - a read
tool is an outbound channel the moment the model writes the address - so giving that same context
`web_fetch` by default puts every stored fact one composed hostname away from leaving. The
state-the-URL-first protocol is copied from NVIDIA's `aiq-research`.

`send_email` and `spend` remain declared, implementation-free, and refused out loud.

---

## 6 · WHAT IS STILL OPEN

| # | item | verdict |
|---|---|---|
| 1 | ~~A real web SEARCH tool~~ **DONE** - `web_search` via lite.duckduckgo.com, no key, 1.14s, public zone only, query printed before it goes | SHIPPED |
| 2 | ~~Tool self-awareness~~ **DONE** - `list_tools`, seat-aware, derived from the registry | SHIPPED (awareness only; IMPROVING its own tools is untouched) |
| 3 | D-8, the 9-second silent render failure | FINISH, small |
| 4 | Barge-in is built and **never tested against a live microphone** - only a synthetic stop event | FINISH |
| 5 | `MODEL` in converse.py is still the 550b for `remember()`; the tiers should own that too | LATER |
| 6 | The 550b tool probe is unstable (81.9s, connection closed). Depth tier is unproven for tools | LATER |
| 7 | RAG over `design/` (3.4MB, 198 files) - needs a LOCAL embedder for the sensitive zone | LATER |
| 8 | 59 unread model cards, tool census undercount - `fit.py` still must not be wired on bad inputs | LATER |
| 9 | VAP / full-duplex - needs a GPU. Revisit only if a CUDA build happens | KILL until GPU |

---

## 6b · PART TWO - THE LAYER, THE GPU, AND THE PROSODY CHANNEL

### THE CORRECTION THAT MATTERS MOST: THIS MACHINE HAS A GPU

```
NVIDIA RTX 3500 Ada Generation Laptop GPU   compute 8.9   CUDA 13.2
12,282 MiB VRAM   |   ~9,964 MiB FREE
torch 2.13.0+cpu  cuda_built: None    <- the CPU-ONLY BUILD
onnxruntime       NOT INSTALLED       <- so whisper AND kokoro run on CPU right now
```

I wrote "this machine has no GPU" from `cuda_available=False` and built three recommendations on
it - Moshi unreachable, Chatterbox unreachable, CUDA "a decision you could make". **`+cpu` is the
CPU-only build of torch; that flag only ever proved TORCH could not see a GPU.** A software fact
read as a hardware fact. Luis caught it. Every latency in this file is a CPU number measured on a
machine with an idle Ada card. *Why not prevented:* the session's own rule is "ask the live thing,
never the description of it" - and `nvidia-smi` is the live thing, one command away, never run.

### THE ARCHITECTURE, DECIDED (Luis): CONVERSATION LIVES IN THE LAYER, NOT THE MODEL

Moshi puts dialogue inside the weights: ~200ms, and **no tools, no permission gate, no zones**,
locked to one 10GB model. Our layer owns turn-taking, endpointing, barge-in, prosody, tools and
the gate - measurable per axis, and any rod plugs in. `aea/lab/duet.py` is the falsification test:
two DIFFERENT rods converse through the REAL audio path (tts -> speakers -> whisper -> prosody).
Nothing is passed as a string, so the loop pays the full tax.

**Measured, 6 turns:** fidelity median **0.958** (worst 0.926) - the layer destroys ~4% of words
per hop ("mind" heard as "mine"). A text-passing demo would have reported 1.000 and taught nothing.

### THE MEASUREMENT THAT REDESIGNED THE MIND

Duet time-to-first-token, 49B: **0.384 / 0.469 / 0.473 / 0.629s**. The 8B: **0.456s**.
**A big rod is not slow to START, only to FINISH** - and length is already capped. So putting the
small rod in the talking seat bought nothing and cost all the depth. Luis heard it immediately.

Now **SPECULATIVE PARALLEL DISPATCH**: the smart rod starts streaming the reply while the fast rod
decides, in parallel, whether a tool is needed. The first chunk needs ~1-2s to accumulate; the
verdict lands at ~0.7s, so the decision almost always arrives before a syllable is committed. No
tool -> the smart stream already flowed, zero added latency. Tool -> the draft is discarded unspoken.

### AXIS 3 CLOSED WITHOUT A 10GB MODEL: aea/io/prosody.py

The transcript is WHAT was said. This measures HOW, off samples we already capture and were
throwing away - F0 by autocorrelation, energy over voiced frames, speech rate, pause structure.

```
same sentence, five deliveries    DISTINCT TRANSCRIPTS 1 of 5
                                  DISTINCT ANNOTATIONS 4 of 5
prosody retained  0.00 -> 0.75    at 7-11ms, ZERO VRAM, no download
```

End to end, same words, different behaviour:
```
(no annotation)                        -> "Sure, Luis, I'm listening. What's on your mind?"
[heard: much slower than usual,        -> "I'm listening. Take your time."
 quieter, 3 pauses mid-sentence]
```

**THE LINE THAT DOES NOT MOVE:** it reports ACOUSTICS, never emotion. "Pitch rose 40% above your
baseline" is a measurement; "you sound angry" is an inference about a person's inner state drawn
from a microphone. The claim ceiling applies to claims about the HUMAN too. Everything is relative
to a rolling per-speaker baseline and stays SILENT until it has 3 samples - a dash, never a guess.

### FOUR MORE DEFECTS

- **D-15 · the annotation was spoken aloud.** duet turn 6: `VEL > [hheard: slower than usual] That's
  a perceptive observation...`. The rule lived in the system prompt only. *Why not prevented:* law
  B5 is in this repo's own law file - a rule the model can talk past is a decoration - and I wrote
  a prompt-only rule the same hour I quoted it. **Fixed in code:** bracketed spans are stripped
  before speech, unconditionally.
- **D-16 · the sentence cap did not bound duration.** A rod emitted **30.6s of speech inside two
  sentences**, past whisper's own 30s ceiling. Counting sentences bounds a GRAMMATICAL unit; a
  person waiting experiences SECONDS. **Fixed:** `MAX_SPOKEN_CHARS = 320`.
- **D-17 · a model over-read the prosody channel.** `ORA > That significant drop in tone and pause
  in your speech suggests a possible discrepancy between your claimed efficiency and actual
  performance` - it treated a text-to-speech artifact as evidence about another model's honesty.
  The channel invites over-interpretation and the prompt now forbids diagnosing feelings. **Open:
  a model can still narrate the measurement as insight.**
- **D-18 · tool over-triggering, and the prompt fix failed exactly as recorded.** `llama-3.1-8b`
  called `list_tools` for "Hey, how's it going?" under a prompt that said in plain words to answer
  NO unless a fact was needed. *Why not prevented:* the PREVIOUS session recorded "a systematic
  tool-calling bias that **SURVIVED an explicit written exclusion**", and I reached for better
  wording anyway. **Fixed structurally:** `tools_for()` - a deterministic pre-filter that does not
  OFFER a schema unless the words plausibly need one, so ZERO is a real answer (law W2). 10/10
  unit, 4/4 end to end.

### BARGE-IN, TWO ROUNDS

`0.829s -> 0.019s`. The audio always stopped in ~30ms; the FUNCTION waited, first on a full queue
(2.3s), then on a `join` of a producer stuck inside a ~0.5s `edge_render` it could not abandon.
There was nothing to wait for. **Do not join a daemon you have already told to stop.**

### THE SCOREBOARD NOW (aea/lab/convbench.py, six axes)

```
axis                  ours      human    moshi        note
ear accuracy           8/8      ~100%    n/a          LEVEL
endpoint correct       8/8        -      VAP-class    0 false cuts, 0 late takes
tool calling         works        -      NONE         WE ARE AHEAD
prosody retained      0.75       1.00    1.00         was 0.00
barge-in stop       0.019s      0.20s    native       AHEAD of the human floor
response gap         2.16s      0.20s    0.25s        9x - the remaining gap
```

**Still to close on the gap, none of it needing a 10GB model:** `onnxruntime-gpu` (ear 0.25 -> ~0.05,
mouth local on the idle Ada card), and a streaming ASR model (~80-300MB) so the transcript exists
WHILE you talk and the ear leaves the critical path entirely.

## 6c · THE BATTERY, AND WHAT MANY CASES FOUND THAT HAND-PICKED ONES HID

`python -m aea.lab.battery --fast` (147 cases, 0.07s) · `--audio` (44 cases, ~40s)
`python -m aea.lab.crystallize --write` -> `diary/CRYSTALS_VOICE.md`

Run in BATCHES with a fix between each, because a four-hour sweep that is wrong in its first ten
minutes wastes four hours - this project has already lost two experiments to exactly that.

```
batch 1   133/147  90.5%   4 false cuts, 7 late takes, 1 false memory
batch 2   139/147  94.6%   after splitting dangling words from hanging tails
batch 3   145/147  98.6%   after mood detection replaced the length proxy
batch 4   146/147  99.3%   0 false cuts, 0 spurious tools, 0 false memories
audio      42/44   95.5%   ear 18/20 semantic, prosody 24/24
```

**THE TWO ERROR DIRECTIONS ARE REPORTED APART, and that is the point of the design.** A false cut
truncates a person mid-thought and cannot be undone; a late take only makes them wait. One combined
accuracy number would let a detector trade the unrecoverable error for the tolerable one and still
look improved. Same for the memory gate, where a false positive POISONS a person's permanent record.

**One failure is left standing on purpose.** "I am not sure about that" is held open because it ends
on `that`. Removing `that` would make "I think that" a false cut. Keeping the conservative side is
the correct trade, not an unfixed bug - and it is recorded so nobody "fixes" it later.

**PROSODY REPLICATED ACROSS THREE SENTENCES x SEVEN DELIVERIES:**
```
'I really need you to do this now'   1 distinct transcript, 6 distinct annotations
'That is not what I asked you for'   1 distinct transcript, 6 distinct annotations
'Can you take a look at this'        1 distinct transcript, 5 distinct annotations
```

**OPEN, AND IT IS NOT A CRYSTAL BECAUSE IT IS NOT RESOLVED (law U5):** whisper-base fails on SHORT
questions carrying domain words. `"What are your laws"` transcribed as **"Where you lost."** and
`"The endpointer waits too long before replying"` as `"The end point awaits too long before
applying."` Those are precisely the shape of the self-knowledge questions the new `self_map`
routing depends on, so the ear is now a live risk to the feature built on top of it. Candidate
fixes, unmeasured: a bigger whisper on the idle GPU, or a small domain bias list.

## 6d · THE GPU PATH IS NOT WHAT I SAID IT WAS (measured 2026-07-29, late)

I recommended `pip install onnxruntime-gpu` as "the largest remaining latency win", to put whisper
and Kokoro on the idle Ada card. **That would have done nothing.** Asked directly:

```
sherpa_onnx.OfflineRecognizer.from_whisper(..., provider="cuda")
  -> "Please compile with -DSHERPA_ONNX_ENABLE_GPU=ON.
      Available providers: CPUExecutionProvider, . Fallback to cpu!"

decode, best of 3, same 3.26s clip:   cpu 0.330s   cuda 0.413s   directml 0.366s
cuda vs cpu = 0.80x  (noise; it ran on CPU in all three arms)
```

**The installed sherpa-onnx wheel is compiled CPU-only and bundles its own onnxruntime**, so a pip
`onnxruntime-gpu` is invisible to it. The provider argument is accepted and ignored, which is the
worst kind of API: it looks like it worked.

**The real options for GPU speech, none of them measured yet:**
- a GPU-enabled sherpa-onnx build (their releases ship separate CUDA wheels)
- `faster-whisper` (CTranslate2, native CUDA) for the ear
- Kokoro through torch+CUDA rather than through sherpa, for the mouth

**Why this was not prevented, and it is the same shape as the `cuda_available` error hours
earlier:** a capability was inferred from a PACKAGE NAME rather than asked of the running library.
`provider="cuda"` constructing without an exception was treated as evidence; it is not. The check
that settles it is a TIMING COMPARISON against the CPU arm, which takes ten seconds to run and was
not run until Luis asked for the pending work. **Ask the live thing, and when the live thing accepts
a flag, make it prove the flag did something.**

## 6e · THE PENDING WORK THAT DID NOT NEED LUIS (done after the battery)

**D-8 CLOSED.** A failed render cost ~9s of silence: `play_fast` failed on a missing file and the
WPF fallback then sat in its own 8-second `NaturalDuration` wait for audio that would never exist.
Guarded at the top. **Measured 9s -> 0.000s** on missing file, empty path, and truncated file.
*The rule:* a fallback is for a DIFFERENT WAY to do the job, never for a job that cannot be done.

**THE ENTITY NOW SPEAKS WITHOUT BEING LAUNCHED.** `live.speak_brief()` runs on a successful wake
brief, so the first thing it says aloud is content it generated as its own work rather than a
greeting invented to have something to say. `aea.io.speak` moved from ORPHANED to wake-reachable
(23 -> 24). Three guards, each shown a case it must refuse, 5/5:

```
opt-in disabled (the default)          silent
outside quiet hours (default 8-22)     silent, and says why in the log
brief too thin ("(grid busy)")         silent - NOT spoken as "nothing to report" (law H3)
brief missing                          silent
a real brief, enabled, in hours        SPOKE 152 chars
```

*The defect this test caught:* the first version used `re` without importing it, **inside a
try/except that would have swallowed the NameError forever**. The entity would simply never have
spoken, silently, with nothing wrong in the heartbeat. A guard that fails closed and says nothing
is indistinguishable from a guard with nothing to guard against.

**DELIBERATELY NOT DONE:** `converse` and `listen` are still orphaned, and should stay that way
until Luis decides. Making the EAR wake-reachable means a machine that opens a microphone on a
schedule. That is a surveillance decision, not an engineering one.

**THE EAR MISHEARING IS A MODEL LIMIT, NOT A CONFIG ONE.** `"What are your laws"` -> `"Where you
lost."` survives everything reachable from here:
- `decoding_method="modified_beam_search"` -> `"Only greedy_search is supported at present for
  whisper"`. Beam search, which is what recovers from an early wrong token, is not available.
- the GPU providers fall back to CPU (see 6d), so no bigger model gets cheaper.

So the remedy is a BIGGER EAR, which is a download decision rather than a code change:
whisper-base is 74M parameters; `small` is 244M and would cost roughly 3x the current 0.2-0.5s
decode - still inside the 2.16s response budget. **Not downloaded: a ~500MB fetch is Luis's call.**
Until then, short domain questions are a known live risk to the `self_map` routing built on them.

## 6f · THE EAR WAS NEVER THE PROBLEM, AND MY INSTRUMENT SAID IT WAS FIVE TIMES

Luis, live: "I'm feeling it's transcribing my words bad." He was right that it was. Everything
about WHY was wrong, including in this file an hour earlier.

**The finding.** `aea/io/earcheck.py` records a known phrase, measures the signal, transcribes it
locally, and names which of three causes is failing. Run properly, at a good level:

```
heard: 'okay so'                        <- had become "Creysau"
heard: 'What are your laws?'            <- had become "Where you lost"
heard: 'Hit me with the question.'      <- had become "and not meet with the question"
heard: 'So, okay, you can hear me now. Take your time.'   (off-script, natural, perfect)
SNR median 26 dB   peak median 0.248   voiced 40-64%
```

**whisper-base is fine.** Every phrase that failed in conversation transcribes perfectly once the
signal arrives. **I was one command from downloading whisper-small twice**, on evidence that was
never about the model.

**THE REAL DEFECT: the signal is unstable, and the gate was not.** Measured in one evening -
room floor 0.0026, 0.0028, 0.0054, 0.0129 (5x), and his speech peak 0.012 to 0.315 (25x). The
endpointer calibrated its floor ONCE per process. A gate set at boot is deaf within minutes when he
drops, and triggers on keystrokes when the room rises: that is where the `[Music]`, `[clap]` and
`[Balloon Sound]` ghost turns came from. **Fixed:** the floor is now a 20th percentile of a rolling
6s window of NON-SPEECH frames, rising slowly and falling fast. Replayed against the measured
sequence: **18 ghost-trigger ticks -> 0**, with quiet speech still heard.

**MY INSTRUMENT REPORTED `MODEL` FIVE TIMES ON A PERFECT RUN.** `verdict()` scored word-error
against the phrase I ASKED for, so a person speaking naturally - the exact behaviour being measured
- read as model failure. Fixed: the model is blamed only when the transcript is a non-speech
ARTIFACT (bracketed, or the classic "Thank you." on silence), never when it is merely DIFFERENT.
*Why not prevented:* D18's rule is to ask what would have to be true of the INSTRUMENT for a
finding to be false. Applied all session to other people's code; not to the scorer I wrote
minutes earlier. **Fourth time today.**

**AND I DESYNCHRONISED THE TEST BY BEING IN IT.** The first two runs counted "3-2-1-GO" and
recorded a fixed window; I then posted "Go" into the chat, which arrived seconds later, and Luis
spoke to MY cue. Reading the envelopes afterwards showed speech at the START of one window, at the
END of another, and phrase five's window containing phrase four. **An instrument that requires its
operator to be punctual is measuring the operator.** Fixed: it now waits for speech and records
until you stop, exactly like the real capture path, with no cue to miss.

## 6g · NOTICING, NOT NARRATING (Luis's design, and it is better than mine)

After hearing it comment on his voice ten turns running: *"maybe humans don't like that all the
time, sometimes, but more about IF SOMETHING WRONG HAPPENED. Let's say someone was talking and shut
up before a moment, then it can ask, what is happening?"*

That is the design the SER research independently recommended, arrived at from the experience
rather than the literature. A signal that fires every turn carries no information, which is why
continuous commentary felt intrusive AND useless simultaneously.

**THE MECHANISM THAT MAKES IT HONEST:** what reaches the speaking rod is a **TOKEN**, never a
description. Given "spoke 60% shorter than usual with falling pitch" the model narrates the
measurement back at the person - measured, 10 of 10 turns. Given `cut_short`, there is nothing to
narrate and the only available move is to ask. `prosody.notice()` returns one of three tokens
(`cut_short`, `trailed_off`, `went_quiet`), requires 5 baseline samples, and has a 4-turn cooldown.
5/5 on test, silent without a baseline, silent on cooldown.

**A THIRD ROUTE THE HISTORY OPENED.** After cutting the annotation from the rod, it STILL commented
on his tone. The store held 28 turns and **10 of 14 machine turns talked about pitch or delivery**,
seeded back as history at boot - its own past output was its style guide. D3's mechanism one level
up: removing a capability is not enough when its consequences are already written down. Filtered.

## 7 · THE TRANSFERABLE MOVE FROM THIS SESSION

**Read the receipt before believing the number on it.** Every wrong belief this session came from a
correctly-produced number being read as something it was not: `play` read as synthesis, `ttfb None`
read as a slow rod, a transport 503 read as a rod that cannot call tools, a reasoning trace read as
a fact about a person, and a missing field read as an empty world. The models were fine. **Nine of
eleven defects were in an instrument, a record, or a reading of one** - which is D18, now counted a
second time and holding.

**And the corollary Luis named:** *the same knowledge keeps being present and unapplied.* Four of
the defects above were prevented in writing, the day before, in a file loaded at boot - applied to
the component that was being agonised over and not to the one beside it. Recording the rule again
does nothing. What might work is recording the SHAPE: **when you apply a lesson, ask out loud which
OTHER component in this same change has the same shape.**
