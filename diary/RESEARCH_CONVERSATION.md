# RESEARCH - conversation theory, turned into changes

*2026-07-29. Luis: "do a deep research for conversation theory on how to make the artificial
intelligence more sound like a conversation and apply all those lessons."*

Sixty agents across six lenses - turn-taking, backchannels/fillers, grounding and repair, response
design, entrainment, and spoken-dialogue-systems engineering. Every claim carrying a citation or a
hard number was then handed to an independent agent told to REFUTE it, defaulting to refuted when
unsure, because a fabricated citation written into a laws file gets trusted forever. What survives
is below.

**READ THE NUMBERS TABLE FIRST.** It is the densest part and it tags every row: `DOC` documented in
the literature, `LOCAL` measured on this machine, `INF` engineering inference to be validated,
`VENDOR` a vendor benchmark rather than peer review. That tagging is the difference between a
target and a guess, and it is why this document can be implemented from.

## WHAT ALREADY LANDED (2026-07-29, same evening)

The research pass read the live tree, so it marks these itself. Recorded here so nobody
re-implements them:

- **R1 (part)** vocative stripped at the decoder + the dead `HOW THEY SOUND` paragraph deleted.
  The paragraph was ITS catch, not mine - it described prosody notes that had not been sent for
  hours, naming the topic of his voice in every context while supplying no signal.
- **R4 (part)** the semantic endpoint re-arms instead of latching once per turn. Measured:
  23 of 35 turns had been running to the 9s cap; loopback now shows dead tail 4.1s -> 1.17s.
- **R9 (part)** `reply_budget` actually reaches `speakable` and `trim`. A story went from 43
  characters to 1,076.
- Plus, outside this plan's scope: the tool-theatre stripper, deterministic arithmetic, the
  true two-part self-description, and `aea/lab/earbench.py` for unattended testing.

## THE HONEST STATUS OF THE REST

R0 (the FTO ledger), R2 (barge-in), R3 (the filler ladder), R5-R8 and R10-R13 are NOT built. R2 in
particular is ~6h and needs echo cancellation before it can be armed at all - arming it without
that makes the machine interrupt itself, which is worse than having no barge-in. They are ranked
here in the order engineering should take them, and the sequencing note at the bottom is the
author's, not mine.

---

All paths below are repo-relative (privacy guard). I read the live code before ranking, so the plan is against what is actually in the tree on 2026-07-29, not against the 35-turn session that produced the fault list. Five of the reported faults have already been fixed in the working tree today and are marked [LANDED] so nobody re-implements them.

---

# 1 - THE RANKED CHANGES

Ranked by perceived naturalness gained per hour of implementation. R0 is a prerequisite, not a feature — nothing below it is falsifiable without it.

---

### R0 - The stage ledger: measure FTO, not TTFA (prerequisite, ~3h)
**Where** `aea/io/speak.py:225 say_stream` receipt, `aea/organs/converse.py:780 capture` and `:1651 turn`.
**Change** The receipt reports `ttfa` measured from the start of `say_stream`. That number excludes the 4.1 s of dead room the endpointer appends and the whisper pass. Log **FTO = t(first audio sample played) − t(last user speech frame)** with seven marks: last-speech-frame, VAD-silence-start, endpoint-verdict, transcript-final, first-LLM-token, first-TTS-chunk-rendered, first-sample-played. Append one JSONL row per turn to `state/voice_fto.jsonl`. Log a paired `first_content_audio` series so a filler cannot game it.
**Values** Gate 1 (this week): p50 FTO <= 1500 ms, p90 <= 2500 ms. Gate 2: p50 <= 800 ms, p90 <= 1500 ms. Fail if `first_content_audio − first_audio > 1500 ms`.
**Test** Run `--once` ten times with a scripted WAV played into the loopback; assert the seven marks are monotonic and sum to FTO within 30 ms.
**Breaks if naive** Measuring from `capture()` return instead of the last speech frame hides exactly the 4.1 s that is the fault. The anchor must be the last frame above `cont`, captured inside the loop, not the loop's exit.

---

### R1 - Kill the vocative-plus-exclamation at the decoder, and delete the dead prompt paragraph (~1h)
**Where** `aea/organs/converse.py:254 strip_opener`, `:1614` system-prompt assembly, `aea/io/speak.py:637 _render_chunk`.
**Change** Three edits. (a) `strip_opener` currently fires only when the first sentence contains the name **and** ends in `!` **and** is <=6 words. Split it: strip a leading vocative independently of the exclamation (`^\s*NAME\s*[,!:—-]+\s*`), and skip the strip if the remainder has no finite verb. (b) Strip `!` from every string handed to `edge_render` — the exclamation is also driving the synthesiser to an over-excited contour, so this improves the voice independent of semantics. (c) **Delete the `HOW THEY SOUND:` paragraph at `:1614`.** The prosody annotation no longer reaches the model (`receipt["heard"] = heard` at `:1273` is the only consumer), so that paragraph now introduces the topic of the user's voice into every context while supplying no signal — precisely the mechanism the session log blames for the habit surviving its own removal.
**Values** Vocative permitted only at session start, after a >30 s gap, or after a repair sequence; hard cap 1 in 10 turns via a counter on `turn_n`. Never turn-initial: casual-conversation corpora put vocatives predominantly turn-final. Target validation-opener rate **20-25%**, not 0.
**Test** Replay the 35-turn store through `strip_opener` + the new lint; assert vocative-initial <= 1/10 and that no reply loses its only finite verb. Then one live 10-turn run, count by ear.
**Breaks if naive** Stripping at the mouth leaves the model still generating it, so `"Luis, the math detour!"` becomes `"the math detour!"` — a verbless fragment. The finite-verb guard is load-bearing. Also, driving validation to zero produces a colder fake than the tic.

---

### R2 - Arm barge-in — the interrupt path is built and unwired (~6h, highest ratio of the real work)
**Where** `aea/organs/converse.py:1655` (`stop = threading.Event()` is created and **never set**), `aea/io/speak.py:660 _play_interruptible`.
**Change** The whole interrupt mechanism exists: `stop`, `_CALL` generation counter, chunk-boundary abort. Nothing listens. Add a mic watcher thread during playback. Two stages: (1) **self-echo gate first** — you own the exact playback buffer, so suppress mic frames whose energy envelope correlates with playback at the measured device delay; fall back to `webrtc-audio-processing` (AEC3, 16 kHz / 10 ms frames, real-time on commodity CPU) only if envelope gating proves fragile. (2) **Trigger** requires BOTH >=300 ms continuous voiced energy AND a partial transcript of >=2 words not in the backchannel stoplist (`mm, mhm, yeah, right, ok, uh-huh, sure`). On trigger, set `stop`, flush the chunk queue.
**Values** 300 ms continuous energy; sub-300 ms bursts are continuers and must NOT abort. Insert a ~200 ms silent gap at each chunk boundary and run the VAD only inside it, to dodge echo entirely on the cheap path.
**Test** Non-negotiable gate: the system talks to itself for 60 s with the mic open and produces **zero** self-triggers. Only then enable the interrupt. Then: interrupt a long reply 10 times, measure stop-latency <= one chunk.
**Breaks if naive** Without the echo gate the system interrupts itself, which reads as far more broken than having no barge-in. And `"no"` and `"wait"` are <=2 words — the stoplist must never suppress them.
**Why this rank** Barge-in changes the economics of every threshold below it: with a working interrupt, the cost of an eager endpoint decision drops from a whole reply to ~300 ms, which is what lets R4 be aggressive.

---

### R3 - Rebuild the filler as a delay signal, not a status LED (~5h)
**Where** `aea/io/speak.py:406 THINKING_SOUNDS`, `:416 FILLER_AFTER`, `:559 choose_filler`, `:600 maybe_filler`, the fill loop at `:290`.
**Change** Five edits, all in the mouth.
- **Gate.** Do not emit anything when predicted time-to-first-audio < **700 ms** (raise `FILLER_AFTER` from 0.45 to 0.70). Predict from the rolling p50 in the R0 ledger for this route plus whether `tools_for()` returned non-empty.
- **Two-key selection.** Re-index the 73 clips as a 2×2: {turn-initial, inter-chunk} × {short <800 ms, long >=2.5 s}. Bin by listening to all 73 once, not by filename. The two keys interact (at unit boundaries speakers tolerate a longer pause before marking it), so treat the table as a lookup, not as orthogonal axes.
- **Prolongation, the missing second device.** `MAX_FILLS = 5` with `FILLER_GAP = 1.30` currently chains five *interchangeable* clips — that is the same one bit played five times. Replace with a re-fill ladder: at 900 ms past the filler tail emit a **prolonged** variant of the same vowel class at −3 dB; at 1.2 s past that, one more; **hard cap two**, then fall through to a spoken account (`"still pulling that up"`) or abort. Pre-render ~10 prolonged variants (600-900 ms) — one afternoon against the existing bank. The choice of filler announces an upcoming delay; prolonging it signals a delay already in progress. The system has device one and no device two.
- **Rate budget.** Shared budget of **~17 fillers per 1000 spoken words** across turn-initial and inter-chunk, over a 20-turn window; uh:um ≈ 52:48 as a fixed voice parameter. At ~30 words/reply that is ~0.5 fillers per reply, against the current ~1.0.
- **One voice.** Render fillers in the same edge voice as the reply (already true — `prime_fillers(voice)`), and verify no bank clip is a different speaker.
- **Promise contract.** Log `promise_kept` per filler. If the rate falls below **0.9**, disable the filler path entirely: an unreliable delay signal is worse than silence.
**Test** Replay 50 turns of recorded latencies through the selector offline; assert filler count/1000 words ∈ [12, 22], no clip repeats within 10 turns, and promise_kept >= 0.9. Then Luis listens to 10 live turns and says whether the wait feels held.
**Breaks if naive** A ladder four deep sounds like a skipping record. An `um` before a 200 ms gap reads as hesitancy about the *content*, and the listener attributes it to stance, not to the clock. And the honest outcome of the gate is that fillers almost never fire — that is correct, not a bug.

---

### R4 - Endpointing as a dynamic threshold, not a fixed one (~4h) — re-arming is [LANDED]
**Where** `aea/organs/converse.py:74 HANGOVER_FAST`, `:94 PROBE_GAP`, `:101 HANGOVER`, the probe block at `:900`.
**Already landed** The single-shot probe is fixed (`probed = False` on resumed speech). That alone removes the 23-of-35 turns that ran to the 9.0 s cap.
**Change** Make the threshold per-turn rather than constant, computed at turn start from features already in hand: turn index, whether the system's last utterance was a question, partial word count, and whether the partial ends on a dangling conjunction (`_DANGLING` at `:495` already encodes this) versus a complete clause. Route the three prosodic turn-yielding cues into the same shift — final pitch slope, energy trajectory over the final 200 ms, final-syllable lengthening — computed from `aea/io/prosody.py` which already runs f0 tracking at 40 ms/20 ms. **Do not put any of this in the prompt.**
**Values** 3 yielding cues -> hangover 250 ms; 0 cues -> 900 ms; clamp to [250, 900]. Hard ceiling: end the turn at **1.6 s** of silence regardless of the semantic verdict. Published operating curve for the tradeoff: **9.9% false-cut at a 300 ms budget vs 4.5% at 600 ms**; start at a 5% cut-in budget, which costs ~550 ms.
**Test** Log two error events per turn: cut-in (user resumes within 1.5 s of system speech onset) and dead-air (>1.5 s past genuine stop). Sweep the threshold offline over the blackbox audio in `aea/io/blackbox.py` and publish the false-cut/latency curve for this room and this speaker.
**Breaks if naive** Pitch tracking on a single noisy mic is unreliable; a wrong cue count is worse than a flat threshold. Disable the cue when voicing confidence is low, and clamp the shift. Also: never re-run the semantic check on a 100 ms poll — the poller must be a pure feature rule, escalating to whisper at most twice per turn (`PROBE_GAP = 1.0` already enforces this).

---

### R5 - Speculative generation on stable partials — the only route below 1 s (~8h, highest ceiling)
**Where** `aea/organs/converse.py:900` (probe block) into `:1222 act_or_answer`.
**Change** This is the arithmetic that makes the current shape impossible rather than merely slow: whisper 0.3 s + endpoint + generation + edge render 0.5 s is a serial chain that *starts at silence*, so the floor is the sum. Humans cannot hit a 200 ms gap either — producing one word takes ~600 ms, a simple sentence ~1500 ms — so they start planning before the other person stops. Run whisper on a rolling 3 s window every ~250 ms during speech; trust only tokens older than ~300 ms (whisper-base churns at the trailing edge); cache by token-suffix hash. When `utterance_looks_complete()` first returns true on a partial, fire the main rod with a 400 ms debounce. On continued speech, cancel and re-fire. On final transcript, **keep the draft only if the appended text does not change the speech-act class** (same question type, no negation, no new named entity); else discard. Pre-render the first TTS chunk of a kept draft during the user's remaining speech, so first audio is a file read.
**Values** Max 1 speculation in flight. Skip entirely when CPU load > 70%. `listen.THREADS = 4` is a measured optimum on this box — do not raise it to feed speculation. Measured local: 49B TTFT 0.384-0.629 s, 8B 0.456 s, so the win is real and comes from the *start*, not from a smaller rod.
**Test** Log kept/discarded ratio and, separately, the user-correction rate on kept-draft turns. A high keep rate with rising corrections means the act-class guard is too loose. Compare p50 FTO with speculation on vs off over 20 turns each.
**Breaks if naive** On CPU, speculative decode competes with whisper and edge render for the same cores and can make the median *worse* while improving the best case. Measure headroom first. Second failure: a kept draft answers the utterance the user was *about* to finish.

---

### R6 - Swap the completion heuristic for a distilled CPU end-of-turn classifier (~3h + license review)
**Where** `aea/organs/converse.py:554 utterance_looks_complete`.
**Change** The current check is hand-written word-set logic (`_DANGLING`, `_HANGING_TAIL`, `_SHORT_COMPLETE`, `_SCAFFOLD`). Replace as the primary with LiveKit's turn-detector v1-mini ONNX (Qwen2.5-0.5B-Instruct fine-tune, distilled from a 7B teacher, quantised and backbone-pruned to run **CPU-only under 500 MB RAM**), fed the last four turns plus the current partial, through `onnxruntime` in-process. Keep the heuristic as the fallback in the middle confidence band.
**Values** Code is Apache-2.0; **model weights are under LiveKit's own model license — check it before shipping**. Do not reach for the v1 audio-branch model; it takes audio directly and is heavier.
**Test** Score both the classifier and the current heuristic against the 35-turn blackbox with hand-labelled true endpoints. Adopt only if the false-cut rate is lower at equal latency. Keep the 1.6 s hard ceiling underneath either.
**Breaks if naive** A classifier trained on call-centre-style dialogue may be miscalibrated for one specific speaker in a specific room. Measure on your own log before trusting it.

---

### R7 - Route prosody to a continuer timer instead of the prompt (~3h)
**Where** `aea/io/prosody.py:93 measure` -> new consumer in `capture()`.
**Change** When the endpoint check says "still going", the system currently waits in silence — the documented meaning of a continuer is exactly *"go on, I am not taking the floor"*, so it is the correct output for that state. Rule, no model needed: while the user holds the floor and the endpoint verdict is not-finished, if the energy contour shows an intra-turn pause **>500 ms after at least 1.2 s of speech**, play a 200-300 ms continuer at **−6 to −9 dB**. Log trigger points for a week; fit a lightGBM regressor on that log only if the heuristic proves coarse (acoustic-only backchannel-timing regression reaches ~130 ms MAE at negligible inference cost).
**Test** Count continuers per minute against the turn log; a continuer must never be followed by system speech within 300 ms.
**Breaks if naive** A continuer is a commitment *not* to take the floor. Backchannel then speak = the system lied and will collide mid-word. Suppress any continuer within 300 ms of the decision to speak.

---

### R8 - Grounding flag and in-place repair (~5h)
**Where** `aea/organs/converse.py:1676` (`turns.append`) and the store writer at `:1690`.
**Change** A heard utterance is written into history before it is grounded, so one mishearing conditions every later turn, and a user correction *appends* rather than replaces — leaving both readings in context. Add `grounded: bool` per entry. A user turn is presented, not grounded, until the next exchange passes without repair initiation. Detect repair with a local matcher fired **before** the rod call (`no`, `I said`, `what?`, `huh?`, `I meant` + Spanish). On a hit: rewrite the previous user entry in place and **delete** the wrong assistant reply. Keep the last two turns of raw PCM in a ring buffer (`blackbox.keep` already stores audio) so the corrected reading is re-decoded, not guessed.
**Also** Add a `revise` event checked at each chunk boundary in `say()`: a late signal (second decode, tool result) stops after the current chunk, plays a cached local repair frame, and resumes from the corrected transcript. Max exposure to a wrong answer becomes one chunk (~0.5 s) instead of the whole reply.
**Values** Repair-initiation budget: **1 per 84 s** of conversation, threshold 0.15 on the combined doubt score. Above threshold but over budget -> use an embedded correction (weave the corrected term into the first clause) instead of a question.
**Test** Measure the doubt score's separation on the 35-turn log's known mishears before trusting the threshold. Assert never >1 initiation per 84 s.
**Breaks if naive** `"no, I don't think so"` is disagreement, not repair. Require the matcher AND a doubt signal on the prior turn before rewriting. Never delete audio, only the text entry. And gate `revise` on two agreeing signals — a mid-reply cutoff on a false alarm is more jarring than a slightly-off answer finished cleanly.

---

### R9 - Action-class reply budgets and the story preface (~3h) — the cap fix is [LANDED]
**Where** `aea/organs/converse.py:1140 reply_budget`, wired at `:1662`.
**Already landed** `reply_budget` now reaches `speakable` (was passing the constant `MAX_SENTENCES = 2` at both call sites). The flat 2-sentence cap is gone.
**Change** The remaining gap is the short end. Add an acknowledgement class: roughly a quarter of all conversational moves are sub-clausal (Switchboard: backchannel/acknowledge 19%, agree/accept 5%, appreciation 2%, yes/no answers 2%), and the current floor is `(90, 190, 2)`. Have the parallel fast rod emit an action label in the same call it already makes for tool use, mapping to: acknowledge = 1-3 words; polar answer = answer token + <=1 clause; wh-answer = 1-2 units; account = 3-6 units; narrative = via preface only. Default to wh-answer at low confidence. For narrative, emit a one-line preface naming shape and cost, then a ~700 ms window — silence or any non-stop token counts as go-ahead.
**Values** Reference points: interpausal units mean 1680 ms / median 1227 ms; corpus mean 6.6 words per turn. Hard ceiling 6 units. Preface at most 1 per N turns, and never twice in a row.
**Test** Log label vs budget vs whether the user re-prompted, for a week, before trusting the short branches.
**Breaks if naive** A misclassified action gives a three-word reply to a question that needed an explanation — worse than a uniform cap because the user cannot learn around it. And "there are three parts to that" delivered 30 times out of 32 is the vocative tic in a new costume. Ship the long branch only **after** R2 (barge-in), never before.

---

### R10 - Function-word entrainment (~2h, cheap and measurable)
**Where** a new pass in `build_system` at `:178`.
**Change** Per turn, compute `-|count_user(w)/N_user - count_asst(w)/N_asst|` over a fixed 25-word high-frequency list, rolling 10-turn window. Take the 6-8 words the assistant most under-uses and inject one system line: *"prefer these exact function words where natural: …"*. Drop the injection entirely on turns already matched within threshold.
**Values** High-frequency-word entrainment predicts human naturalness ratings at 63.76% vs a 50% baseline; correlates with task success r = 0.341 (p = 0.018). Cap the injected list at 8.
**Test** Log the aggregate entrainment score per session as a live honesty number; it should drift up across a session.
**Breaks if naive** Extending the list to content words produces audible parroting, and with a distinctive speaker it reads as mockery. The cited evidence covers function/cue words only and does not test content words either way. Injection as an instruction can also make the model over-fire the words in one reply instead of drifting.

---

### R11 - Inter-chunk seam filler and the 200 ms boundary (~2h)
**Where** `aea/io/speak.py:290` (the play loop).
**Change** When chunk N finishes and N+1 is not rendered, the system emits a silent seam mid-sentence — the most machine-like artefact in a streamed TTS pipeline, and exactly where humans put a short `uh` (within-unit filler rate is 30-63% of the boundary rate). Insert a short uh-class token there instead of a gap, from the **same shared budget** as turn-initial fillers. Non-final chunks must be rendered with continuation punctuation (comma, no terminal stop) so edge-tts does not put a final fall on a mid-turn unit.
**Test** Count seams per session. If they are frequent, the honest read is that chunking is too aggressive (`_MIN_CHUNK = 8` at `speak.py:202`) and the filler is papering over a fixable render problem.
**Breaks if naive** Doubles fillers per turn. One shared budget or nothing.

---

### R12 - Pre-answer inbreath (~2h, do it only if the sample matches)
**Where** `aea/io/speak.py`, new asset + one branch in the fill loop.
**Change** Play one short inbreath the moment the endpoint commits, when predicted latency > ~500 ms, before the rod has produced anything. It occupies the 0.3-0.7 s window the filler system currently mis-serves, it is pre-linguistic so it can never narrate or name the user, and it costs no model call. Answers preceded by an audible inbreath had a **modal latency of 576 ms vs 100 ms** without one (7 Dutch dyads, correlational).
**Test** A/B on 10 turns each; the question is whether the wait feels held.
**Breaks if naive** A breath that does not match the TTS voice's spectral profile lands in the uncanny valley and gets described in the same words as the current sounds. Cut it from edge-tts output in the same voice; if it cannot be made to match, **drop it** rather than ship a mismatched one.

---

### R13 - The spoken-register lint (~2h)
**Where** a deterministic pass before `speakable` yields.
**Change** Compute lexical density over the existing 35-turn store — that is the baseline, twenty lines of Python. Then lint before TTS: strip ordinal scaffolding (`First,… Second,…`), strip colons introducing lists, truncate enumerations to 3 items plus a completer (`and that kind of thing`), delete closing summary sentences.
**Values** Monitor spoken lexical density **< 40%** (spoken texts generally fall below; written at or above).
**Test** Density per session against the 35-turn baseline, plus a count of surviving ordinal markers (target 0).
**Breaks if naive** Density is blunt: you can hit 38% by adding function words and saying less. Use it as a red flag on the transcript, never as a generation objective. Truncation is lossy — if the answer genuinely has five items, route it to the preface protocol instead.

---

# 2 - THE NUMBERS

`DOC` = documented in the literature. `LOCAL` = measured on this machine, already in the repo. `INF` = engineering inference from the evidence, to be validated. `VENDOR` = vendor/community benchmark, not peer-reviewed.

| Quantity | Value | Kind | Use |
|---|---|---|---|
| Modal floor-transfer offset | ~200 ms | DOC | The perceptual target |
| Median between-turn interval | 205 ms (mean 275) | DOC | — |
| Transitions under 200 / 500 ms | 51-55% / 70-82% | DOC | — |
| Cross-language median gap, 10 languages | ~0 ms (Japanese) to ~+470 ms (Danish) | DOC | Do not over-tune to English |
| English mean offset | 236 ms | DOC | — |
| Jefferson standard maximum silence | ~1 s | DOC | Past this, repair work starts |
| Dispreference crossover | ~700 ms | DOC | Gradient, not a cliff |
| **Filler gate floor** | **700 ms predicted** | INF | Raise `FILLER_AFTER` 0.45 -> 0.70 |
| **Hard silence ceiling** | **1600 ms** | INF | End the turn regardless of verdict |
| Dynamic hangover range | 250-900 ms (3 cues -> 0 cues) | INF | Clamp; from `prosody.py` |
| Endpoint operating curve | 9.9% false-cut @ 300 ms; 4.5% @ 600 ms | VENDOR | Pick a false-cut budget first |
| Endpoint mean latency at target | 295 ms @ 10% cut-in; 543 ms @ 5% | VENDOR | Start at 5% |
| Dynamic-threshold latency win | up to 24% | DOC | vs a fixed threshold |
| Single-word production latency | ~600 ms | DOC | Why detect-then-respond cannot work |
| Simple-sentence production | ~1500 ms | DOC | — |
| Interpausal unit, Switchboard | mean 1680 ms, median 1227 ms | DOC | Unit budget sizing |
| Sub-clausal share of moves | ~26-28% | DOC | The missing acknowledge class |
| Mean words per turn (one corpus) | 6.6 | DOC | Task-oriented corpus, not universal |
| Filler rate, median speaker | 17.3 / 1000 words (range 1.2-88.5) | DOC | The shared budget |
| uh : um ratio, median speaker | 52 : 48 | DOC | Fixed voice parameter |
| Filled pauses as share of tokens | 2.5% | DOC | ~1 per 40 words |
| Within-unit filler rate vs boundary | 30-63% (13 and 27 vs 43 /1000) | DOC | Justifies R11 |
| Delay after um vs uh | 4.12 s vs 1.00 s | DOC | Two-key binning |
| Prolongation variance explained (delay before filler) | 90-92% | DOC | The missing second device |
| Filler-choice variance explained (delay after) | 86-96% | DOC | — |
| Re-fill ladder | 900 ms, then +1.2 s, cap 2 | INF | Replaces `MAX_FILLS = 5` |
| No-repeat window | 10 turns | INF | Currently `_NOREPEAT = 4` |
| Promise-kept floor | 0.90, else disable fillers | INF | — |
| Pre-answer inbreath latency | 576 ms vs 100 ms | DOC | Small sample, correlational |
| Backchannel timing MAE, acoustic-only | ~130 ms | DOC | CPU-reachable |
| Continuer trigger | >500 ms pause after >=1.2 s speech | INF | −6 to −9 dB, 200-300 ms |
| Continuer suppression window | 300 ms before speaking | INF | Non-negotiable |
| Barge-in trigger | >=300 ms voiced + >=2 non-stoplist words | INF | Sub-300 ms = continuer |
| Chunk-boundary gap | ~200 ms | INF | VAD listens only here |
| Other-initiated repair rate, humans | 1 per 1.4 min (95% within 4.13 min) | DOC | Budget: 1 per 84 s |
| Clarify threshold | P(misheard) > 0.15 | INF | From local cost model |
| Emotional validation, LLM vs human | 76% vs 22% | DOC | Target 20-25%, not 0 |
| Face-preservation excess over humans | +45 pp across 11 models | DOC | Why prompt bans fail |
| Function-word entrainment -> naturalness | 63.76% vs 50% baseline | DOC | R10 |
| Entrainment -> task success | r = 0.341, p = 0.018 | DOC | — |
| Spoken lexical density | < 40% content words | DOC | Monitor only |
| Spoken list length | 3 + completer | DOC | — |
| Question-asking optimum (interior, not extreme) | ~65.7% of turns | DOC | The principle, not the number |
| **Current p50 FTO** | **4200 ms (worst 30 000)** | LOCAL | The thing being fixed |
| Turns hitting the 9.0 s cap | 23 of 35 | LOCAL | Fixed by re-arming [LANDED] |
| Median real speech end | 4.9 s; 4.1 s of empty room appended | LOCAL | — |
| Whisper-base decode, short clip | 0.28-0.51 s | LOCAL | Probes are not the bottleneck |
| Edge render, cold vs warm | 1.18-1.82 s vs 0.46-0.75 s | LOCAL | `warm()` at boot [LANDED] |
| Rod TTFT, 49B vs 8B | 0.384-0.629 s vs 0.456 s | LOCAL | A big rod is not slow to start |
| Speech rate | ~15 chars/s | LOCAL | Budget arithmetic |
| Whisper threads, measured optimum | 4 | LOCAL | Do not raise for speculation |
| Vocative-initial replies | 30 of 32 (94%) | LOCAL | Target <= 1 in 10 |
| Prosody narration | 10 of 10 turns; 10 of 14 machine turns in the store | LOCAL | Never into the prompt |

---

# 3 - WHAT THIS HARDWARE CANNOT DO — named once, do not research again

1. **Full-duplex speech models (Moshi-class).** ~200 ms replies with genuine overlap. Requires a GPU. Already recorded in `converse.py:74`; `cuda_available = False`, torch is CPU-only.
2. **Voice Activity Projection.** A transformer predicting both speakers' next ~2 s at 50 Hz. The real solution to endpointing, barge-in and backchannels at once. GPU. The CPU-reachable share is the three-cue heuristic (R4) plus the ~130 ms acoustic backchannel regression (R7), and that is close enough that the ceiling is not worth chasing.
3. **Neural prosody generation / incremental TTS.** edge-tts renders whole strings; you cannot prolong a syllable, cliticise a filler onto the previous word (`and-uh`), or apply continuation intonation at synthesis time. Prolongation must be **pre-rendered variants**, and mid-turn falls must be avoided by punctuation, not by prosody control. Drop the clitic-attachment half of the filler literature entirely rather than fake it.
4. **The audio-branch end-of-turn models.** LiveKit Turn Detector v1 encodes user audio directly across 14 languages and is heavier; only the **text/transcript v1-mini** (<500 MB, CPU) is in reach.
5. **Token-level ASR confidence.** sherpa-onnx whisper-base as wired in `aea/io/listen.py` returns text, not logprobs. Confidence must come from disagreement between successive decodes of the growing buffer, not from the model.
6. **Neural AEC.** WebRTC AEC3 (classical, 10 ms frames) is the ceiling. Anything learned is out.
7. **Per-turn filler generation.** Generating a filler with a small rod costs a ~0.5 s render — the exact gap it exists to cover. Selection from a bank is not a compromise, it is the only correct design.

---

# 4 - THE PRINCIPLES

Six rules. Each one, applied earlier, would have prevented a named measured fault.

1. **Measure the gap the listener hears, not the stage you own.** Latency is the offset from the user's last speech frame to the first sample played; every stage that is timed separately hides its contribution. *(Would have caught the 4.2 s median long before the 35-turn session: 0.3 s ear + 0.5 s mouth never explained it, and nothing measured the 4.1 s of dead room between them.)*
2. **A rule the model can talk past is a decoration — enforce it at the decoder.** Prompts are advisory; strippers, budgets and counters are binding. *(The vocative opener survived an explicit prompt ban on 30 of 32 turns. So did the tool-calling bias, and so did the prosody narration — the last one with no prosody in its context at all.)*
3. **Never let one number stand for a decision the system never makes.** A single global cap is the tell that no per-turn fitting is happening. *(The flat `MAX_SENTENCES = 2` made acknowledgement, answer and story the same shape, and a computed `reply_budget` sat unread at the call site for a whole session.)*
4. **Every signal the system emits must be a true prediction, and it must be kept.** A filler is a promise about the length of the wait; if the promise cannot be kept above 90% of the time, emit silence instead. *(73 interchangeable clips carry one bit and then break the promise with 4 s of silence, or five chained clips, which is the same bit five times.)*
5. **Hearing is not understanding: nothing enters the record until the next turn passes without repair, and a correction rewrites rather than appends.** *(One mishearing conditioned every later turn, and the machine's own unverified output became a remembered fact the next turn cited.)*
6. **Every decision that can be wrong must be re-armed, and every wait must have a hard ceiling.** A one-shot judgement cannot recover from its own wrong answer. *(One mid-sentence pause disarmed the only fast exit permanently; 23 of 35 turns then ran to the 9 s cap.)*

---

**Sequencing note for engineering:** R0 -> R1 -> R2 -> R3 -> R4 in that order. R9's long branch and R5's speculation are both unsafe before R2 is armed and verified with the 60-second self-talk test. R6 is a swap-in that can proceed in parallel; R10-R13 are independent and can be picked up by anyone.