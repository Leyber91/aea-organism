# THE VOICE, CONSOLIDATED - what exists, what it learned, and what it became

*2026-07-29 to 07-30. Luis: "time to recap the voice functionality, and to consolidate all the
lessons we had, main language English, the spanish room was a test." This is the one document to
read. The four-part failure records are in `NOTES_VOICE_2026-07-29b.md`, the transferable rules in
`CRYSTALS_VOICE.md`, and the two research passes in `RESEARCH_CONVERSATION.md` and
`RESEARCH_SOCIAL_AGENTS.md`.*

---

## 1 - WHAT EXISTS

**English is the language.** The Spanish room was a test; the cast, prompts and prohibitions all
exist in Spanish (`CAST_ES`, `PROHIBITIONS_ES`, `GUIDE_ES`) and are kept, because building them
proved the layer is language-independent - but everything ships and is measured in English.

### The one-person loop (`aea/organs/converse.py`)

```
EAR      whisper-base local ~0.3s. Adaptive room floor. Hysteresis gate anchored to THIS
         utterance's own peak, not the room. Semantic endpoint that RE-ARMS. Hard silence
         ceiling. 20s max utterance.
MIND     speculative parallel dispatch - the smart rod streams while a fast rod triages tools.
         Arithmetic COMPUTED, never delegated. Reply budget in SECONDS of speech.
MOUTH    edge-tts, sentence-chunked, render-ahead. 73 cached thinking sounds.
REPAIR   doubt() from decode instability -> it ASKS instead of answering a guess.
GUARDS   tool theatre, vocative openers, meta-preambles, emotion attribution - all stripped in
         CODE. Self-falsehood and memory-denial counted against real state.
```

### The many-voice layer

| module | what it is |
|---|---|
| `aea/io/mixer.py` | ONE output stream, N sources summed in one callback. Constant-power pan, soft limiter, per-source stop. |
| `aea/lab/party.py` | four characters, guide-not-script, persistent selves, bidding for the floor, overlap |
| `aea/mind/persona.py` | a persistent self per speaker: memory, impressions, commitments, separate stores |
| `aea/lab/social.py` | many-dimension analysis, including voice-collapse detection and the noise floor |
| `aea/mind/council.py` | **what it became**: several expert opinions on one question, in text, with the disagreement kept |

### The instruments

`aea/lab/battery.py` (283 cases, 8 suites) - `earbench --corpus/--noise/--loopback/--duet` -
`aea/io/blackbox.py` - `aea/tooling/selfcheck.py` (7 invariants, 46 frozen behaviours).

---

## 2 - THE NUMBERS THAT SURVIVED

**Everything below has zero or near-zero run-to-run spread.** Anything that did not is in section 3.

| | before | after |
|---|---|---|
| real tool calls | **1 in 35 turns**, four receipts invented and spoken | every arithmetic turn speaks a real result |
| dead air before thinking | 23/35 turns hit the cap, **4.1s** of empty room | **0.32s** median |
| a story | **43 characters** | **1,076 characters**, 85s of speech |
| the vocative tic | 30 of 32 replies opened "Luis, <exclamation>!" | stripped at the decoder |
| duet transcript accuracy | **43% WER** | **2%** |
| turns produced (party) | 1-3 of 12 | **11-12 of 12** |
| speakers with a voice | REN had **zero speech acts** | all four, zero silent, every run |
| floor at 26 turns | - | **gini 0.194, balanced** |

**Settled by measurement, do not re-litigate:**

- **Noise is not the problem.** Swept against his own room noise: median WER **0.0% at every SNR
  from 30 dB down to 6 dB**. His live SNR was 17.5-31.7.
- **Level is not the problem.** Peak 0.096 transcribed perfectly; peak 0.510 did not.
- **Trimming the dead tail fixes nothing** (0 of 5). **Onset padding fixes nothing** (0 of 5).
- **The GPU is unreachable** from the speech stack - sherpa-onnx is compiled CPU-only.
- **Emotion labels are refused on evidence** - SER macro-F1 0.4316 on natural speech.
- Therefore the residual ear failures are **the model**, and whisper-small is finally a motivated
  20-minute experiment against `--loopback` rather than a guess.

---

## 3 - WHAT I REPORTED THAT WAS NOISE

Kept at the top level because it is the most useful thing in this document.

`social.compare()` runs N conversations under identical conditions and reports the spread. Against
that spread, three of the four gains I had reported were **inside the instrument's own noise**:

| | claimed gain | actual run-to-run spread |
|---|---|---|
| convergence | 0.040 | **0.098 - 0.143** |
| gini | 0.038 | **0.103 - 0.184** |
| length spread | 7.0 | **15.7 - 19.5** |

They were single runs against single runs, different topics, temperature 0.95. **An anecdote with a
decimal point is still an anecdote.** No comparison in this project counts until the noise floor of
the metric is known.

And the test I should have run first: every run was 8-12 turns while **the documented persona wall
is at turn 8.** I was measuring below the interesting region the whole time. At 26 turns the floor
self-balances and the characters still hold apart.

---

## 4 - THE LESSONS, CONSOLIDATED

Ordered by how often they came back wearing a new costume.

### The instrument is more likely wrong than the subject

Session one: nine of eleven wrong beliefs came from an instrument. Session two: **six of eight**.
The list, and each one nearly caused a fix to a defect that did not exist:

- the loopback played audio before opening the microphone -> "the onset is being clipped"
- the duet parser scored the receipt bracket as spoken words -> "80% WER" on a perfect turn
- the echo detector fired on a four-word artifact sharing two words with a long reply
- the health metric counted frames only while a voice was sounding -> "6% of the audio is missing"
  on a perfectly healthy idle bus
- a shell heredoc ate backslashes -> a privacy grep reported CLEAN on a dirty file
- the WER scorer paired "okay so" with an unrelated sentence and scored it 550%

**Ask what would have to be true of the INSTRUMENT for the finding to be false, and test that
first.**

### A value computed and never read is a value never computed

Three times, in three different files, in two days:

- `reply_budget()` returned (700, 1600, 14) for a story and both call sites passed the constant 2
- `grid.think_off()` is measured per model family, frozen in the golden tests, and was **called by
  nothing** - which is why a reasoning rod returned zero characters and another spoke its scratchpad
- the `HOW THEY SOUND` prompt paragraph described a signal that had stopped being sent hours earlier

Test the WIRING, not the function. The function passed its own test every time.

### Bound the quantity you care about, never a proxy for it

- `MAX_SENTENCES = 2` bounded sentences when the thing that mattered was seconds of speech
- `reply_budget` in characters hid half a minute: 430 characters IS 29 seconds at 15 chars/s
- `max_tokens = 130` bounded generation to control speech, and starved the thinking
- `CEIL_REF = floor * 3` derived a check on the room from the room's own drifting estimate

**A threshold derived from the thing it is checking cannot check it.**

### Attention follows effort, not risk

The interesting function gets the docstring and the reasoning; the two-character call site gets
nothing. Every defect above lived in the cheap part. **Deliberately re-read the argument you did
not change.**

### Two correct rules compose into a false sentence

The arithmetic prefetch removed `calc` from the offer; the no-tools guard then told the model it had
no calculator - while the real answer sat in its context. Neither rule was wrong. Only a whole turn
through a real rod shows this class, which is why `--once` now runs after every guard change.

### Persistence raises the price of every unguarded output

A reasoning rod's scratchpad, spoken once, is forgotten. Stored, it becomes a belief the character
holds forever and is answerable to. The same leak costs more the moment there is a store.

### A guard that can eat what it guards

The meta-reject dropped a line AND burned the turn, so the conversation ran three turns of twelve.
The parrot check could swallow a legitimate one-word reply. **A guard needs a path for the thing it
refuses**, or it silently deletes participants.

---

## 5 - WHAT THE VOICE WORK BECAME

`aea/mind/council.py`. Everything learned in a room with speakers turned out not to be about voice:

- **different rods** because one model in four prompts converges, and sycophancy is trained in
- **first-person seeds** because adjectives are the worst-measured persona condition
- **prohibitions plus a mechanical loop detector** because agents recognise a loop and cannot leave
- **a held seat** because at four members you cannot express the committed minority that prevents
  convergence, so it is hard-coded
- **`think_off` wired**, and a runaway-only token cap

A council that agrees with itself is a more expensive single opinion. So dissent is measured and
never smoothed, and unanimity is reported as a finding about the COUNCIL first.

First real use, on this project's own open question, produced a test nobody here had thought of:
*"whether the 6s tail is a hard ceiling (quota, throttle) or a long tail (GC, page fault). If it's a
ceiling, pre-render hits it too. Need one histogram of live-loop render times, not an average."*

---

## 6 - OPEN, RANKED

1. **The echo gate.** Written after the live run heard its own speakers and recorded them as a
   person, but **NOT TESTED**. The gate before any microphone opens again: the machine talks to
   itself for 60s with the mic open and must capture **zero** turns.
2. **The render mystery.** 0.54s bench, 1.5-6s live, five hypotheses dead with controls. Take the
   council's advice: a histogram, not an average, to tell a ceiling from a tail.
3. **Barge-in.** Built, never armed. Needs 1.
4. **The filler as a delay signal** - gate at 700ms predicted wait, prolongation ladder, a
   `promise_kept` metric that disables it below 0.9. This is "it sounds like one bit".
5. **The FTO ledger** - measure the gap the LISTENER hears, from last speech frame to first sample.
6. **whisper-small**, against `--loopback`, on the two surviving lexical failures.
