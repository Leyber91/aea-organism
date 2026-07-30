# CRYSTALS - THE VOICE SESSION (2026-07-29)

*Derived from `state/lab/battery/*.json` by `python -m aea.lab.crystallize`. Do not edit by hand: every status below is re-read from the last battery run, so a lesson and its evidence cannot drift apart.*

**Law U5:** crystallise on a RESOLVED IMPASSE, never on success. A green suite produces nothing here. HOLDING means the expensive thing has not come back.
**Status: 6 HOLDING, 5 NO PROBE**


## C-V1 - A dangling-word list must hold words that CANNOT end a sentence

**HOLDING** - 3 case(s) pass in the run of 2026-07-29 13:38

- **Rule.** Build a suffix test from words that cannot END an utterance, never from words that often continue one.
- **Paid for by.** `have`, `that`, `there` and `do` were in the dangling list, so four complete questions were held open for the full 1.15s hangover with nothing to wait for.
- **How it should have been built.** Two separate sets: function words that genuinely cannot close a clause (articles, prepositions, conjunctions, possessives), and a HANGING TAIL check for a modal or bare subject with no predicate - applied only to statements.
- **Why the knowledge was present and not applied.** The list was written from intuition about which words 'feel unfinished' and never shown a complete sentence ending in one. A detector that has only seen positives has not been tested, only run (D18) - and it was written in the same hour that quoted D18.

## C-V2 - Grammatical mood, not length, decides whether a hanging word matters

**HOLDING** - 2 case(s) pass in the run of 2026-07-29 13:38

- **Rule.** When two cases differ by a property, test THAT property. A correlated proxy will be wrong in both directions.
- **Paid for by.** Gating the hanging-tail check on utterance LENGTH rejected 'What time is it' and 'Are you still there' while accepting 'I was thinking that maybe we should'.
- **How it should have been built.** Detect interrogative mood - a wh-word in the first two positions, or subject-auxiliary inversion - and skip the hanging-tail check for questions only.
- **Why the knowledge was present and not applied.** Length correlated with the right answer on the first few cases I tried by hand, so it looked like the rule. Law B2 was already in the law file: test the property, never a proxy for it. Twelve more cases in a batch exposed in seconds what hand-picked examples had hidden.

## C-V3 - A gate is only proven when tested APART from its only caller

**HOLDING** - 1 case(s) pass in the run of 2026-07-29 13:38

- **Rule.** Test a check in isolation, not through the one function that happens to call it.
- **Paid for by.** `is_fact('NOTHING')` returned True. The refusal token was filtered by `remember()` instead, so the gate was correct only by coincidence of its call site - and would have silently admitted 'NOTHING' as a permanent fact from any other caller.
- **How it should have been built.** The refusal tokens belong inside the gate, so it is correct wherever it is used.
- **Why the knowledge was present and not applied.** It was written as a helper for one function and tested only through that function. Correctness that depends on the caller is not a property of the check.

## C-V4 - A rule in the prompt is a decoration; put it in code

**HOLDING** - 3 case(s) pass in the run of 2026-07-29 13:38

- **Rule.** Anything the model must never say aloud is stripped in code, not requested in the system prompt.
- **Paid for by.** Three separate leaks in one session, each after an explicit written instruction: the prosody annotation spoken as '[hheard: slower than usual]', the meta preamble 'Here's my response, adhering to the VOICE and HONESTY RULES:', and '*pause*' read out as the word 'pause'.
- **How it should have been built.** Strip bracketed spans, meta preambles, stage directions and list markers in the delta pipeline, before a syllable can be rendered.
- **Why the knowledge was present and not applied.** Law B5 - a permission the model can talk past is a decoration - was in the law file and quoted in this session, and applied to TOOLS while the speech path was left to a prompt. A law applied in one place and not the one beside it is the recurring shape.

## C-V9 - The machine may report a measurement and ASK; it may not tell a person what they feel

**HOLDING** - 4 case(s) pass in the run of 2026-07-29 13:38

- **Rule.** Assertions about a human's inner state are stripped in code. Questions survive, because a question invites correction and costs nothing when it is wrong.
- **Paid for by.** A rod turned a text-to-speech artifact into 'a possible discrepancy between your claimed efficiency and actual performance' - reading prosody as evidence about another party's honesty. Pointed at a person instead of a model, that is a machine telling someone how they feel from a microphone.
- **How it should have been built.** A deterministic strip over a closed emotion lexicon, in the delta pipeline beside the bracket-stripper, running on every emitted piece rather than the finished reply.
- **Why the knowledge was present and not applied.** The evidence says the claim could never have been earned: the winning system at the Interspeech 2025 SER challenge scored macro-F1 0.4316 on natural speech; the same pipeline scores 75.00% on ACTED corpora and 42.58% on spontaneous, so acted data inflates by ~32 points; cross-corpus spans 15.03-66.91%, the low end below chance; annotator agreement on MSP-Podcast is Fleiss kappa 0.23 with 19.4% of clips never reaching a label at all. And the best VALENCE results are earned by transformers reading the WORDS - so a mood claim presented as heard in a voice is the transcript re-scored for sentiment, a fabricated provenance. The honesty law already forbade this; nobody had checked whether the number behind it existed.

## C-V5 - Fitness is per task shape: a smaller rod is not a cheaper big rod

**NO PROBE** - recorded from the session, no automated case behind it yet

- **Rule.** Before seating a rod, measure it on the ACTUAL task, not on a proxy for the task.
- **Paid for by.** The reflex seat was filled by time-to-first-token alone. `llama-3.2-3b` is fastest (0.287s) and CANNOT call a tool - it emits `<|python_tag|>{...}` as plain text - so the acting seat held a rod that could only talk about acting. Later, the background reviewer on the 49b answered in 2.5s and found nothing on three planted defects the 550b caught.
- **How it should have been built.** Probe every candidate on BOTH axes the seat requires, and let the staleness checker read both stores so it cannot re-recommend the rod that was rejected.
- **Why the knowledge was present and not applied.** Law M10 was quoted in this session, an hour before the seat was filled on one number.

## C-V10 - A signal that fires every turn carries no information

**NO PROBE** - recorded from the session, no automated case behind it yet

- **Rule.** A derived channel must fire on a CHANGE and stay silent otherwise, and what reaches the model is a TOKEN naming the move, never a description of the measurement.
- **Paid for by.** The prosody annotation was appended to every user turn. In six minutes of real conversation the model led with it TEN times out of ten, and when Luis said the transcription was failing him it told him his frustration was palpable. Cutting the annotation off did not stop it: the store held 10 of 14 machine turns talking about his voice, seeded back as history, so its own past output taught it again.
- **How it should have been built.** Fire only on a measured shift from that speaker's own baseline, with a cooldown, and hand the model an INSTRUCTION ('ask what happened, briefly') rather than the numbers. A token has nothing to narrate. Filter the habit out of seeded history too.
- **Why the knowledge was present and not applied.** I predicted this in writing - logged it as D-17 'open', with three adversarial critics warning about it - and shipped the channel anyway behind a prompt-level guard. The model was never disobeying: it was being helpful about the most novel thing in its context, every time. An output filter cannot remove a TOPIC.

## C-V11 - An instrument that needs its operator to be punctual measures the operator

**NO PROBE** - recorded from the session, no automated case behind it yet

- **Rule.** A measurement with a human step must wait for the human, never the reverse.
- **Paid for by.** earcheck counted 3-2-1-GO and recorded a fixed window. I posted 'Go' into the chat, arriving seconds later, and Luis spoke to MY cue. Envelopes afterwards showed speech at the START of one window, the END of another, and phrase five's window holding phrase four. Every transcript was scored against the wrong target and I read it as evidence about whisper.
- **How it should have been built.** Open the mic, wait as long as it takes for speech to start, record until it stops - the same trigger-and-hangover path the real system uses.
- **Why the knowledge was present and not applied.** I inserted myself into a timing-critical loop to be helpful and became the largest source of error in it. Generalises past audio: when a measurement has a human step, the instrument sets the pace or it is measuring latency in the chat.

## C-V6 - Read the value; never trust the field name you expected

**NO PROBE** - recorded from the session, no automated case behind it yet

- **Rule.** Open the store and look before writing code against its keys.
- **Paid for by.** Five times in one session: `status` for `nvidia_catalog_state` (printed '0 served chat rods' as a finding), `reachable` for `counts.reachable_from_wake` (rendered every number as a dash), `checks[].status` for `.ok`, `class="..."` for `class='...'` (parsed zero results from a good 23KB page), and `cuda_available` read as a hardware fact when `torch+cpu` can never report otherwise.
- **How it should have been built.** One `print(list(d))` before the first line of consuming code.
- **Why the knowledge was present and not applied.** Each guess was locally plausible and cost a whole diagnosis. This is ONE habit, not five defects, and it is the single most transferable lesson of the session.

## C-V7 - A metric that punishes a correct answer is the instrument, not the model

**HOLDING** - 1 case(s) pass in the run of 2026-07-29 05:19

- **Rule.** When a measurement says the subject failed, check what the SCORER would have to believe for that to be true.
- **Paid for by.** The ear transcribed a spoken numeral as '92,837' - exactly right - and scored WER 0.86 and a semantic MISS, twice, because the normaliser only mapped single digits.
- **How it should have been built.** Strip numeric tokens from both sides and compare the remaining words; score numbers on their own terms.
- **Why the knowledge was present and not applied.** D18's transferable move is to ask what would have to be true of the INSTRUMENT for a finding to be false. It was applied all session to other people's code and not to the scoring function written thirty seconds earlier.

## C-V8 - Free local knowledge is fetched, never requested from the model

**NO PROBE** - recorded from the session, no automated case behind it yet

- **Rule.** Split tools by COST: local and free is pre-fetched deterministically; anything that spends or reaches outward stays model-decided.
- **Paid for by.** Offered `self_map`, a rod declined to call it and invented 'I'm built using a transformer... around a dozen components' about its own structure - the exact fabrication the tool exists to prevent.
- **How it should have been built.** Detect the question deterministically, call the tool, and inject the result as fact. Offering a tool is a hope; the model may decline into invention.
- **Why the knowledge was present and not applied.** Tool-calling was treated as the general mechanism for getting facts, when for free local reads there is no decision worth delegating.

---

# THE SECOND SESSION - 2026-07-29 evening

> **Renumbered.** These were first written as C-V9 to C-V16 and collided with three
> crystals of the same number from the earlier session. Found by an audit that COUNTED the
> register instead of trusting it - the same class as every other defect here, one level up:
> the record of the lessons had a lesson-shaped hole in it.

*Eight more, from the 35-turn black-box run and the fixes it forced. The pattern across all eight:
**not one is a wrong function.** Every one lives in a seam - a value computed and never read, a flag
set and never cleared, a paragraph pointing at data that stopped arriving, two correct rules
composing into a false sentence. Unit tests do not see seams. Only a whole turn does.*

## C-V17 - A narrated tool call is a fabricated receipt

- **Rule.** A sentence shaped like a measurement, produced by no measurement, is worse than a wrong answer: it carries provenance it has not earned, and the record teaches it forward.
- **Paid for by.** 35 live turns, ONE real tool call. "calls calculator tool Tool Response (verbalized): The result of 415 multiplied by 987 is 409,605" - spoken aloud, nothing ran. Asked afterwards what it used, it named a tool that does not exist.
- **How it should have been built.** Never delegate a settled question to a model. The pre-filter already matched `calc` with certainty; extract the expression by regex and COMPUTE it, then inject the result as a measured fact.
- **Why the knowledge was present and not applied.** The prefetch mechanism existed for exactly this, built two hours earlier against exactly this failure mode. `calc` was excluded because it needs an argument, and needing an argument felt like needing a model. It needed a regex. The specific case was judged on its surface difficulty instead of against the principle that already covered it.

## C-V18 - A latch inside a loop outlives its evidence

- **Rule.** If the thing a flag judged can change, the flag must be re-armed when it does. And every wait needs a hard ceiling measured against something that cannot drift.
- **Paid for by.** `probed = True`, set at the first pause and never cleared. 23 of 35 turns ran to the 9-second cap; real speech ended at a median of 4.9s, so 4.1s of empty room was appended to each. The fallback could not fire either - the gate had tracked down to 1.5x a very quiet floor, under the room itself.
- **How it should have been built.** Re-arm on resumed speech, plus a `SILENCE_CEILING` measured against an ABSOLUTE level. A self-referential threshold cannot detect its own drift. Loopback after: dead tail 4.1s -> 0.32s median, worst 1.97s.
- **Why the knowledge was present and not applied.** The comment on that line justified the latch with a cost that was never measured - "transcribing every 30ms frame would put whisper in a hot loop" - a real concern about a design nobody proposed. The choice was framed as once-versus-every-frame, and once-per-pause was never considered. A well-argued comment is the best hiding place a bug has.

## C-V19 - A value computed and never read is one never computed

- **Rule.** Test the WIRING, not the function. "Does reply_budget return 14" passed for its whole life while nothing read the 14.
- **Paid for by.** Luis asked for adaptive length in plain words. `reply_budget()` returned (700, 1600, 14) for a story; both call sites passed the constant `MAX_SENTENCES = 2`. A story stored 43 characters. After wiring: 1,076 characters, 5 chunks, 85 seconds of speech.
- **How it should have been built.** An end-to-end assertion through `speakable`, which is now `suite_budget`.
- **Why the knowledge was present and not applied.** The budget function was the interesting part, so it got the docstring and the reasoning; the call site was two characters. Attention follows effort rather than risk (law M9) - the second time that exact law was paid for in two days. The cheapest part of all is the argument you did not change.

## C-V20 - Two correct rules can compose into a false sentence

- **Rule.** A guard that is right in isolation can be wrong in combination, and no test of either guard will show it. Only a whole turn will.
- **Paid for by.** `TOOL calc(415 * 987) -> 409605` followed by "Since I don't have a mathematical calculation tool at my disposal for this specific turn...". The arithmetic prefetch removed `calc` from the offer, which emptied the schema, which tripped the brand-new no-tools guard. The honesty fix talked the rod out of using a real receipt.
- **How it should have been built.** Condition on `not schema AND not facts`, with a positive counterpart when facts exist - and keep it TERSE. A system message that DESCRIBES a situation invites commentary on the situation; one that gives an instruction gets obeyed.
- **Why the knowledge was present and not applied.** The battery tests every guard against its own corpus and both guards passed theirs. No test ran a real turn through a real rod, because model calls are slow and non-deterministic and so felt like the wrong place for a test. It is the only place this class of defect exists. `--once` now runs after every guard change.

## C-V21 - Prompt text is not inert when its data is gone

- **Rule.** Removing a capability means removing everything that points at it. Text describing a signal that never arrives still names the subject, and a named subject is something the model will find a way to talk about.
- **Paid for by.** The prosody annotation was cut from the speaking rod and the poisoned history filtered, and the system prompt still carried a full paragraph teaching the model how to read prosody notes - for notes that had not been sent in hours. Very likely the third and final reason it kept commenting on how he sounded.
- **How it should have been built.** When the annotation was cut, grep for every reference to it, not for its call site.
- **Why the knowledge was present and not applied.** The cut was made in `act_or_answer`; the paragraph lives in `main`, 400 lines away, appended to a string rather than passed as an argument. The dependency was invisible because it ran through text. Found by the conversation-theory research pass reading the live tree - not by me, while editing that same function twice.

## C-V22 - A correction that states half a truth produces the other error

- **Rule.** When a false belief has two parts, correcting one part does not yield the truth. It yields the opposite fabrication.
- **Paid for by.** "I'm a remote, cloud-based AI, I can't access your machine" was corrected with "you are a program running on his computer" - and it then said "I don't rely on external servers or cloud services; my operations are self-contained within your system." Equally false; the rod really is remote.
- **How it should have been built.** State both halves in one sentence so there is no half to drop. After: "I'm a bit of both, actually. The thinking happens on a remote NVIDIA server, but there's also a local program running right here on your computer."
- **Why the knowledge was present and not applied.** The observed defect was one-sided, so the correction was written to be its opposite rather than to be complete. A fix aimed at a symptom inherits the symptom's shape.

## C-V23 - A detector that fires on the truth teaches you to ignore it

- **Rule.** State-dependent claims need state-dependent detectors, judged where the state is visible.
- **Paid for by.** The honesty guard flagged "I don't retain any prior knowledge about you" as a defect during a `--no-store` verification run, where the store really was empty and the sentence was the correct answer.
- **How it should have been built.** Split. "I am cloud-based" is unconditionally false while this program is running. "I do not remember you" moved to `_MEMORY_DENIAL` and is judged in `turn()` against how many facts and stored turns actually exist.
- **Why the knowledge was present and not applied.** Both sentences came from the same paragraph of the same transcript, from the same wrong self-image, so they were recorded as one defect. Two symptoms of one cause can still need two detectors, because a detector tests a sentence and not a cause.

## C-V24 - Ask what would have to be true of the INSTRUMENT, before touching the subject

- **Rule.** The harness is a hypothesis too, and it is the one nobody tests.
- **Paid for by.** Twice in one hour. (1) The first loopback run showed three clips losing their opening words with a NEGATIVE tail - textbook too-short pre-roll, and the obvious next move was raising `PREROLL`. The harness started playback before `capture()` had opened its input stream; the clip was playing to a microphone that was not yet open. A 1.2s lead-in recovered every word and took median WER from 15.5% to 0%. It would have been a fix to a defect that does not exist. (2) The privacy grep for a leaked absolute path reported CLEAN on a dirty file, because a shell heredoc ate the backslashes - the repo's own recorded law, broken twice while acting on the repo's own recorded law.
- **How it should have been built.** Write the check to a real file and run the file. Put a control on a harness result before believing it.
- **Why the knowledge was present and not applied.** Both laws were already written down, one of them by me the day before. Knowledge applied to the subject under test is not automatically applied to the thing doing the testing - and the instrument is where attention is lowest precisely because it is not the interesting part.
