# RECAP - the voice, end to end. What exists, what it measures, what is still wrong.

*2026-07-29. Written at Luis's request: "analyze all the products that we did, make a recap, save
the progress, and fine tune the algorithm." This is the single document to read before touching the
voice again. It supersedes nothing - `NOTES_VOICE_2026-07-29b.md` holds the failures in four-part
form, `CRYSTALS_VOICE.md` holds the transferable rules, `RESEARCH_CONVERSATION.md` holds the plan.
This is the map of the whole thing.*

---

## 1 - THE PRODUCTS. What was actually built.

### The pipeline (`aea/organs/converse.py`, ~2100 lines)

```
EAR      whisper-base local, ~0.3s
         adaptive room floor (20th percentile, asymmetric tracking)
         hysteresis gate ANCHORED TO THIS UTTERANCE'S OWN PEAK, not only the room
         semantic endpoint: transcribe at each 0.45s pause, ask "is this finished"
         re-arms on resumed speech; hard silence ceiling at 1.6s
         20s max utterance (was 9s - real sentences run 12-16s)

MIND     speculative parallel dispatch: the smart rod streams the reply while a fast
         rod decides on tools, so the good model does the talking
         deterministic tool pre-filter; arithmetic COMPUTED before the rod is called
         reply budget in SECONDS of speech, scaled to what was asked

MOUTH    edge-tts, sentence-chunked, render-ahead, ~0.5s a chunk
         73 cached thinking sounds, context-selected, never generated at speak time

GUARDS   tool theatre stripped in code       (a narrated call is a fabricated receipt)
         vocative opener stripped in code    (with a finite-verb guard)
         meta-preamble stripped in code      ("here's my response, adhering to...")
         emotion attribution stripped        (it may never tell a person what they feel)
         self-falsehood + memory-denial COUNTED and printed, judged against real state
         doubt from decode instability -> it ASKS instead of answering a guess
```

### The instruments

| module | what it measures | needs a person |
|---|---|---|
| `aea/lab/battery.py` | 283 deterministic cases across 8 suites | no |
| `aea/lab/earbench.py --corpus` | the model alone, on his real recordings | no |
| `aea/lab/earbench.py --noise` | words lost to room noise, swept 30-6 dB | no |
| `aea/lab/earbench.py --loopback` | the FULL chain through the real microphone | no |
| `aea/lab/earbench.py --duet` | **a whole two-sided conversation, out loud** | no |
| `aea/io/blackbox.py` | audio kept beside transcript, both sides | during a real session |
| `aea/tooling/selfcheck.py` | 7 whole-system invariants, 46 frozen behaviours | no |

**The duet is the one that matters most and it is the newest.** Luis: *"You're only expressing when
he's saying something, and then it's like he is reading a list instead of having a conversation on
the other side."* He was right. Twenty isolated clips score well and prove nothing about a
conversation. The duet plays a person with a second TTS voice, has a small rod write that person's
next line FROM THE MACHINE'S REPLY, and drives the real `converse` program as a subprocess - never
a re-implementation, because every defect found this session lived in the seams a re-implementation
would skip.

---

## 2 - WHAT THE MEASUREMENTS SAY

### Fixed, with numbers

| | before | after |
|---|---|---|
| real tool calls | **1 in 35 turns**, four receipts invented and spoken | every arithmetic turn computes and speaks a real result |
| dead air before thinking | 23/35 turns hit the cap, **4.1s** of empty room | **0.32s** median (12-clip), 1.19s (20-clip) |
| a story | **43 characters** | **1,076 characters**, 5 chunks |
| the vocative tic | **30 of 32** replies opened "Luis, <exclamation>!" | stripped at the decoder |
| self-description | "cloud-based, cannot access your machine" (false) | "a bit of both - remote thinking, local program" |
| duet transcript accuracy | **43% WER** median | **2%** WER median |
| battery | 174 cases | **283 cases**, 282 pass |

### Measured and NOT fixed

- **Reply length was 30 seconds.** `budget 5s/430c` produced 30.5s and 31.6s of speech on
  consecutive duet turns. 430 characters *is* 29 seconds at 15 chars/s - the cap was doing exactly
  what it said and what it said was wrong. **Recalibrated today in seconds** (6s chat / 14s
  question / 70s depth) but NOT yet re-measured in a duet.
- **Time to reply: median 42s, worst 93s** in the duet. Dominated by the 30s replies above, so the
  recalibration should move it hard - unverified.
- **Two ear failures survive** at 30 dB SNR with a clean voice: "what are your laws" -> "Where you
  lost", "what are you not able to do". Lexical, not acoustic.
- **The render mystery.** 0.54s on the bench, 1.5-6.0s live. Five hypotheses dead with controls.
  Unknown.

### Settled by measurement - do not re-litigate

- **Noise is not the problem.** Swept against his OWN room noise: median WER **0.0% at every SNR
  from 30 dB down to 6 dB**, perfect count only 15/20 -> 12/20 across 24 dB. His live SNR ran
  17.5-31.7 dB. The room he has cannot explain a single mishearing.
- **Level is not the problem.** Peak 0.096 transcribed perfectly; peak 0.510 did not.
- **Trimming the dead tail fixes nothing** (0 of 5), **onset padding fixes nothing** (0 of 5).
- **whisper is deterministic here** - 0 drift across 23 re-runs, so all of the above hold.
- Therefore: the residual ear failures are **the model**, and whisper-small is now a properly
  motivated 20-minute experiment against `--loopback` rather than a guess. It was nearly bought
  three times on evidence that was about the signal.

---

## 3 - THE ALGORITHM, TUNED. Every constant that moved today, and why.

| constant | was | now | why |
|---|---|---|---|
| `MAX_UTTER` | 9.0 | **20.0** | duet: EVERY turn reported "9.0s of audio". Real sentences run 12-16s, so the rod answered half a question - and the truncation destabilised the decodes enough to trip the repair prompt on a turn heard correctly. One wrong constant, three symptoms. |
| `probed` | latched once | **re-armed** | one mid-sentence pause disarmed the only fast exit for the whole turn |
| `SILENCE_CEILING` | (none) | **1.6s** | backstop for when the gate drifts under the room |
| `CEIL_REF` | `floor*3` | **0.12 x utterance peak** | the first version drifted with the floor it was checking. A threshold derived from the room cannot be a check on the room. |
| `HOLD_REF` | (none) | **0.04 x utterance peak** | lifts the hold gate off the room; 0.06 caused the session's first false cut, so it was lowered |
| `HANGOVER_DANGLING` | (none) | **2.4s** | the probe could only ever end a turn SOONER; a verdict of "he is mid-sentence" changed nothing and he got cut off anyway |
| `PROBE_GAP` | (none) | **1.0s** | so re-armed probes cannot stack |
| `MAX_SENTENCES` at call sites | hardcoded 2 | **per-turn budget** | the computed budget was never read |
| `reply_budget` | 190/430/1600 chars | **6s/14s/70s** | see above - characters hid half a minute |
| `SPEAK_RATE` | implicit | **15.0 explicit** | budgets are now written in the unit a waiting person actually feels |
| `DOUBT_ASK` | (none) | **0.34** | ask rather than answer a transcript the decodes disagreed about |

**The pattern in that table:** almost every fix replaces a value derived from the drifting thing it
was supposed to check, or a value expressed in a unit nobody can feel. Those are the two failure
shapes worth looking for next.

---

## 4 - WHAT IS STILL OPEN, RANKED

1. **Re-measure the duet with the new budgets.** The single highest-value next run. 6s/14s/70s
   should take time-to-reply from 42s to something conversational, and it is untested.
2. **R0 - the FTO ledger.** Measure the gap the LISTENER hears: last speech frame -> first sample
   played, seven marks, one row a turn. Every stage is timed separately today, which is exactly how
   4.1s of dead room hid between a 0.3s ear and a 0.5s mouth.
3. **R2 - arm barge-in.** The mechanism exists and nothing sets the stop event. Needs the self-echo
   gate FIRST: 60s of the machine talking with the mic open, zero self-triggers.
4. **R3 - the filler as a delay signal.** Gate at 700ms predicted wait, prolongation ladder capped
   at 2, `promise_kept` metric that disables fillers below 0.9. This is "it sounds like one bit".
5. **The render mystery.** Time it INSIDE the live process. Do not guess it.
6. **whisper-small**, tested against `--loopback`, on the two surviving lexical failures.

---

## 5 - THE HONEST LIST OF WHAT I GOT WRONG TODAY

Kept because the pattern is the point, and it is the same pattern every time.

- **The open microphone slows the renderer** - dead, 1.1x.
- **The dead tail starves whisper** - dead, trimming fixed 0 of 5.
- **The onset is clipped** - dead, padding fixed 0 of 5, and a control moved too.
- **The loopback's lost opening words** - my harness, playing audio before opening the microphone.
  I was one edit from raising `PREROLL` to fix a defect that does not exist.
- **The duet's 80% WER on turn 1** - my parser, scoring the receipt bracket as spoken words. The
  ear had been perfect.
- **The duet's "echo leak"** - my detector, firing on a four-word artifact that shared two words
  with a 300-character reply.
- **The privacy grep that reported clean on a dirty file** - a shell heredoc ate the backslashes.
  The repo's own recorded law, broken while acting on the repo's own recorded law.
- **My own arithmetic fix contradicting my own honesty fix** - the calculator ran and the guard
  then told the model it had no calculator.

**Six of eight are the instrument, not the subject.** That is the same ratio as the previous
session (nine of eleven) and it is now the most reliable prediction in this project: when a
measurement surprises you, the harness is more likely wrong than the thing being measured. Ask what
would have to be true of the INSTRUMENT for the finding to be false, and test that first.
