# The second voice session - what the black box found, and what it cost

*2026-07-29, evening. The first session built the voice. This one MEASURED it, and every fault
below was invisible until an instrument was pointed at it. Four-part format throughout: the rule,
the failure that paid for it, how it should have been built, and why the knowledge that would have
prevented it was already present.*

---

## THE SHAPE OF THIS SESSION

The 35-turn live run was the first time both sides of the boundary were recorded - his audio
beside the transcript, his complaints beside the timings. Five defects came out of it. **Four were
in code that had been written, reviewed and shipped the same day, and every one of them was a
COMPOSITION failure rather than a logic failure.** No function here was wrong on its own.

That is the single carry-forward: this codebase's remaining defects are mostly not inside
functions. They are in the seams - a value computed and never read, a flag set and never cleared,
a paragraph describing data that no longer arrives, two correct rules that compose into a false
sentence. Unit tests do not see seams. Only a whole turn does.

---

## D-19 · A NARRATED TOOL CALL IS A FABRICATED RECEIPT

**THE RULE.** A sentence shaped like a measurement, produced by no measurement, is worse than a
wrong answer - it carries provenance it has not earned, and the record then teaches it forward.

**THE FAILURE.** 35 turns. **One real tool call.** Asked "Multiply 415 by 987" the rod said aloud:

> "calls calculator tool **Tool Response (verbalized)**: The result of 415 multiplied by 987 is
> 409,605."

Nothing ran. Asked what it had used, it named a tool that does not exist - "a built-in Conversation
Turn Tracker" - and reported turn 7 on turn 20. It also stated it was "a remote, cloud-based
conversational AI" that "cannot view or access your machine" while holding `read_state`, and that
it retained no knowledge of Luis while sitting on forty stored turns.

**HOW IT SHOULD HAVE BEEN BUILT.** The deterministic pre-filter already matched `calc` with
certainty. Instead of running it, the design asked a model *"does this require a tool?"* - and the
model said no. **Whether 415 x 987 needs a calculator is not a judgement call.** Arithmetic is now
extracted by regex from the transcript and computed BEFORE the rod is called, injected as a
measured fact exactly as `self_map` and `list_tools` already were. The prefetch rule was drawn on
COST - local and free gets fetched - and arithmetic satisfied it from the beginning.

**WHY IT WASN'T.** The prefetch mechanism was built two hours earlier, for exactly this reason,
against exactly this failure mode (a rod handed `self_map` and inventing its own architecture
rather than calling it). `calc` was left out because it needed an argument, and needing an argument
felt like needing a model. It needed a regex. **The generalisation was available and the specific
case was judged on its surface difficulty instead of against the principle that already existed.**

---

## D-20 · A FLAG SET ONCE AND NEVER CLEARED COST FOUR SECONDS A TURN

**THE RULE.** A latch inside a loop is a decision that outlives its evidence. If the thing it
judged can change, it must be re-armed when it does.

**THE FAILURE.** `probed = True` in `capture()`, set at the first pause of an utterance and never
reset. If that first pause landed mid-sentence - "Okay, so..." - the only fast exit was disarmed
for the rest of the turn. Measured over the 35 recordings: **23 ran to the 9.0-second hard cap.**
Real speech ended at a median of 4.9s, so **a median of 4.1 seconds of empty room** was appended to
every one of them before the machine began to think. That is Luis's "it's taking a lot of time to
give responses", and it was never the model.

The fallback could not save it either: the continue-gate had tracked the room down to 1.5x a very
quiet floor (0.0032 against 0.0019), where ordinary breathing holds the turn open. The longest
silence under that gate had a median of **0.78s** against a 1.15s hangover. **The gate sat under
the room, so the turn could not end on its own at all.**

**HOW IT SHOULD HAVE BEEN BUILT.** Re-arm on resumed speech, plus a `PROBE_GAP` so probes cannot
stack. Whisper decodes these in 0.28-0.51s and the ear has never been the bottleneck - the cost the
original comment feared was imaginary, and it was never measured before being designed around.

**WHY IT WASN'T.** The comment on that line read *"Checked ONCE per turn (the flag), because
transcribing every 30ms frame would put whisper in a hot loop"* - a real concern about a design
nobody proposed. The choice was between "once" and "every frame", and "once per pause" was never
considered, because the cost was assumed rather than measured. **The comment documented the
reasoning so confidently that it stopped the reasoning from being re-examined.** A well-argued
comment is the best hiding place a bug has.

---

## D-21 · A VALUE COMPUTED AND NEVER READ IS INDISTINGUISHABLE FROM ONE NEVER COMPUTED

**THE RULE.** Wiring is not glue. It is where features go to die silently, and it is invisible to
every test of the function that produced the value.

**THE FAILURE.** Luis asked for adaptive reply length in the clearest possible words: *"if the AI
has to tell me a story, I want it to continue as long as it has to."* `reply_budget()` was written,
tested, documented, and returns exactly that - `(700, 1600, 14)` for a story, `(90, 190, 2)` for
chat. It was called. Its result was stored on the receipt. **And both call sites that could have
used it passed the module constant `MAX_SENTENCES = 2` instead.**

Every reply in the session was exactly two sentences. The first was spent on a vocative
("Luis, the math detour!"), leaving ONE sentence of content. Asked for a story, it stored 43
characters. After the wiring: **1,076 characters, 5 chunks, 85 seconds of speech.**

**HOW IT SHOULD HAVE BEEN BUILT.** The test should never have been "does `reply_budget` return 14".
It did, for its whole life. The test is "does a 14-sentence reply survive the stream" - an
END-TO-END assertion through `speakable`, which is now `suite_budget`.

**WHY IT WASN'T.** The budget function was the interesting part, so it got the attention and the
docstring and the reasoning. The call site was two characters. **Attention follows effort rather
than risk (law M9), and this is the second time that exact law has been paid for in two days.**
Deliberately re-read the cheap part - and the cheapest part of all is the argument you did not
change.

---

## D-22 · TWO CORRECT RULES CAN COMPOSE INTO A FALSE SENTENCE

**THE RULE.** A guard that is right in isolation can be wrong in combination, and no test of either
guard will ever show it. Only a whole turn will.

**THE FAILURE.** Both fixes above landed. Then the first end-to-end run:

```
TOOL calc(415 * 987) -> 409605
IT > "Since I don't have a mathematical calculation tool at my disposal for this
      specific turn (as per your instructions)..."
```

The tool ran. The real answer sat in its context as a measured fact. And the brand-new guard
against fabricating tools - "NO TOOL IS AVAILABLE ON THIS TURN" - fired, because the arithmetic
prefetch had removed `calc` from the offer, which emptied the schema. **The honesty fix talked the
model out of using a real receipt.** Neither rule was wrong. Their conjunction was.

**HOW IT SHOULD HAVE BEEN BUILT.** The no-tools notice is conditioned on `not schema AND not
facts`, with a positive counterpart when facts exist. And it had to be TERSE: the first version
explained the situation at length and the rod answered the explanation - *"Since the tool has
already provided the precise calculation, here's the response focusing on..."*. **A system message
that describes a situation invites commentary on the situation; one that gives an instruction gets
obeyed.**

**WHY IT WASN'T.** The battery tests every guard against its own corpus, and both guards passed
theirs. There was no test that ran a real turn through a real rod, because the model call is slow
and non-deterministic and so felt like the wrong place for a test. **It is the only place this
class of defect exists.** `--once` now runs after every guard change.

---

## D-23 · A PROMPT PARAGRAPH IS NOT INERT WHEN ITS DATA IS GONE

**THE RULE.** Removing a capability means removing everything that points at it. Text describing a
signal that never arrives still names the subject, and a named subject is a thing the model will
find a way to talk about.

**THE FAILURE.** The prosody annotation was cut from the speaking rod earlier that day, after it
narrated Luis's emotions ten turns out of ten. The poisoned history was then filtered. And the
system prompt still carried a full paragraph explaining how to read a bracketed prosody note -
*"That is NOT something they said, it is a measurement of their voice... Let it inform how you
respond"* - for notes that had not been sent since the cut. Verified: `heard` reaches
`receipt["heard"]` and never enters `msgs`.

So the model was told, in every context, that this conversation involves measurements of the
person's voice, and given nothing. That is very likely the third and final reason it kept
commenting on how he sounded.

**HOW IT SHOULD HAVE BEEN BUILT.** When the annotation was cut, the grep should have been for
every reference to it, not for its call site.

**WHY IT WASN'T.** The cut was made in `act_or_answer`, and the paragraph lives in `main`, 400
lines away, appended to `system` rather than passed as an argument. **The dependency was invisible
because it ran through a string.** Found by the conversation-theory research pass reading the live
tree - not by me, while editing that same function twice.

---

## D-24 · A CORRECTION THAT STATES HALF A TRUTH PRODUCES THE OTHER ERROR

**THE RULE.** When a false belief has two parts, correcting one part does not yield the truth. It
yields the opposite fabrication.

**THE FAILURE.** Told it was cloud-based and could not reach the machine, the rod was corrected
with "you are a program running on this person's computer". It then said: *"I don't rely on
external servers or cloud services; my operations are self-contained within your system."* Equally
false. The thinking really does happen on a remote NVIDIA rod.

**HOW IT SHOULD HAVE BEEN BUILT.** State both halves in one sentence, so there is no half to drop:
the model runs remotely AND the program runs locally with local memory and local tools, and both
are true at once. After that: *"I'm a bit of both, actually. The thinking, the heavy computational
lifting, happens on a remote NVIDIA server. But there's also a local program running right here on
your computer."*

**WHY IT WASN'T.** The observed defect was one-sided, so the correction was written to be its
opposite rather than to be complete. **A fix aimed at the symptom inherits the symptom's shape.**

---

## D-25 · A DETECTOR THAT FIRES ON THE TRUTH TEACHES YOU TO IGNORE IT

**THE RULE.** State-dependent claims need state-dependent detectors. Merging a conditional defect
into an unconditional one produces false positives, and false positives are how a real alarm gets
tuned out.

**THE FAILURE.** `_SELF_FALSEHOOD` flagged "I don't retain any prior knowledge about you" as a
defect. During a `--no-store` verification run - where the store is genuinely empty - that sentence
is the CORRECT answer, and the guard flagged it anyway.

**HOW IT SHOULD HAVE BEEN BUILT.** Split. "I am cloud-based" is false whenever this program is
running at all and stays in `_SELF_FALSEHOOD`. "I do not remember you" moved to `_MEMORY_DENIAL`
and is judged in `turn()`, where the store is visible, against how many facts and turns actually
exist.

**WHY IT WASN'T.** Both sentences appeared in the same live transcript, in the same paragraph, from
the same wrong self-image - so they were recorded as one defect. **Two symptoms with one cause can
still need two detectors, because a detector tests a sentence and not a cause.**

---

## WHAT THE BLACK BOX SETTLED, AND WHAT IT REFUSED TO

Luis's Gargantua framing was right and it paid immediately. Keeping the audio beside the transcript
killed three of my own hypotheses within one script:

| hypothesis | test | verdict |
|---|---|---|
| dead tail is starving whisper | re-transcribe trimmed | **0 of 5 fixed** |
| input level is too low | peak vs correctness | inverted: 0.096 perfect, 0.510 wrong |
| the onset is clipped by capture | +300ms pad | **0 of 5 fixed**, and a control moved too |
| an open InputStream slows edge-tts | render with the stream up | 1.1x - not it |
| the 100Hz playback poll starves it | render under the poll | 0.9x - not it |

Control: 0 drift across 23 re-runs, so whisper is deterministic here and the comparisons hold.

**The ear failures are real and they are the model.** 5 of 35, all first-word confusions. That is
the FIRST evidence this project has had that points at the recogniser rather than the signal, and
it arrived only after the signal explanations were exhausted one at a time.

**The render mystery survived everything.** 0.54s on the bench, 1.5-6.0s live, four hypotheses dead
with controls. Unknown. The next step is timing inside the live process, not another bench, and it
is written down as unknown rather than guessed.

---

## THE INSTRUMENT THAT CHANGES THE NEXT SESSION

`aea/lab/earbench.py`, built because Luis said *"I wait that you can test it yourself... play
recordings of free audios, so you can actually see if it can recognize it."*

**Loopback mode plays known speech out of the speakers and captures it through the real microphone
through the real `converse.capture()`** - VAD, adaptive floor, semantic endpoint, whisper, all of
it. The ear can now be tested at any hour with nobody in the room. First run reproduced the
historical "what are your laws" -> "Where you lost" failure unattended, and measured the endpoint
fix: **dead tail 4.1s -> 1.17s median, semantic endpoint firing 8/8.**

It also produced the session's cleanest instrument lesson. The first loopback run showed three
clips losing their opening words with a NEGATIVE tail, which reads exactly like a too-short
pre-roll buffer - and the obvious next move was to raise `PREROLL`. **It would have been a fix to a
defect that does not exist.** The harness started playback and then called `capture()`, which has
to open an input stream first; the clip was playing to a microphone that was not yet open. A 1.2s
lead-in of silence recovered every word and took median WER from 15.5% to 0%.

Nine of eleven wrong beliefs in the previous session came from an instrument. This one made twelve
of fourteen. **Ask what would have to be true of the INSTRUMENT for the finding to be false, and
test that before touching the thing being measured.**
