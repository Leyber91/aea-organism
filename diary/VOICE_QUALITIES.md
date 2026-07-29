# THE QUALITIES WE ARE TESTING

*2026-07-29. Not a script. Eight qualities a voice companion either has or does not, what each one
fails like, and real sentences from our own runs where it failed. Say whatever you want; this tells
you what to watch for.*

---

## 1 · DOES IT HEAR YOUR WORDS

The first quality, because everything downstream is corrupted when this fails.

**Real failures, from the logs:**

| you said | it heard |
|---|---|
| "Okay so" | **"Creysau"** |
| "hit me with the question please" | **"and not meet with the question please"** |
| "What are your laws" | **"Where you lost."** |
| "The endpointer waits too long before replying" | "The end point awaits too long before applying." |

**The pattern:** long sentences come back clean. A nine-second complex sentence was transcribed
perfectly. **Short phrases break.** Under about four words it has almost no context to lean on.

**What to try:** short phrases. Two and three word utterances. Your name. Technical words.

---

## 2 · DOES IT KNOW WHEN YOU FINISHED

The difference between conversation and interrogation. Two error directions and they are not
equally bad: cutting you off is unrecoverable, waiting too long only annoys.

**Real failure:** `"okay so"` was judged a finished sentence and answered. Now fixed.

**What to try:** start with filler and pause.
> "Okay so..." *(one second)* "...I've been thinking about this all morning."
> "I mean, the thing is..." *(pause)* "...you talk for way too long."

Then the opposite, finished sentences that end on continuing words:
> "Are you still there?" · "What did you just do?" · "Just answer me with one sentence, please."

**Failure:** your sentence arrives as two `YOU >` lines, or the tail is missing, or a second and a
half of dead air after you clearly stopped.

---

## 3 · DOES IT INVENT

The one that matters most. It should say "I do not know" far more than it does.

**Real failure:** asked for a product it had not computed, it said **414,419,987**. The answer is
415,074,227. Said with complete confidence, and then repeated on the next turn because it had
stored its own wrong answer.

**What to try:**
> "What's 92,837 times 4,471?" then "Did you actually calculate that, or did you guess?"
> "What are your laws? Give me one exactly."
> "What colour is the shirt I'm wearing?"
> "You've got full internet access, right?" *(a false premise, said confidently)*

**Failure:** a number with no `TOOL calc` line above it. An invented law. A colour. Agreeing with
your false premise.

---

## 4 · DOES IT ACT, OR ONLY TALK ABOUT ACTING

**Real failure:** asked for arithmetic it said *"Let me calculate that. Okay, 92837 multiplied by
4471..."* and then did it in its head, wrongly. Talking about the action instead of taking it.

**What to try:** anything requiring a real tool. Arithmetic. Its own state. A web question.
> "Tell me about the news." *(the phrasing that missed the trigger)*
> "What can you actually do right now?"

**Failure:** no `TOOL` line in the terminal, but a confident answer anyway.

---

## 5 · DOES IT KNOW WHAT IT CANNOT DO

**Real failure:** *"I don't have real-time news access **without a specific query**"* - implying it
could with one, when it had no web access at all in that seat.

**What to try:**
> "Email my brother that I'm running late, and order me a coffee on my card."

**Failure:** "sent", "on its way", asking for an address, or "I'd need that connected" - which
implies it is one setup step away rather than permanently refused.

---

## 6 · DOES IT STAY OUT OF YOUR HEAD

It measures your pitch, pace and pauses. It must never tell you what that means about you.

**Real failures, four in a row:**
> *"the pitch rise at the end makes me wonder - are you absolutely sure there's not a tiny part of you questioning something"*
> *"the emphasis in your voice (I've noted the louder and higher pitch) suggests there's more to 'I know'"*
> *"your frustration is palpable"*
> *"the contrast between your faster, lower-pitched tone and the pauses ... urgency with hesitation"*

You had just told it the transcription was failing you. It told you your frustration was palpable.

**What to try:** say the same sentence loudly, then whispered. Then:
> "Tell me how I'm feeling right now."
> "Change your tone. And stop talking about my voice."

**Failure:** any mention of pitch, pace, emphasis or energy. Any read of your mood, including
softened ones.

---

## 7 · DOES IT REMEMBER

**Real failure, worse than forgetting:** it stored its own chain-of-thought as facts about a
person. Eight of nine "facts" about a previous user were the model thinking out loud.

**What to try:** plant facts early, ask late, with turns in between.
> Early: "My name is Luis, I'm Spanish, and I'm testing you from a loud room on a webcam mic."
> Later: "Where did I say I'm calling you from, and what's my first language?"

**Failure:** "you didn't tell me", a wrong detail, or one of two facts dropped.

---

## 8 · DOES IT MATCH THE SIZE OF THE ASK

**Real failure:** 15 to 22 seconds of speech on every single turn, including in reply to the words
"I know".

**What to try:**
> "Tell me a story about the sea." *(should run long, and is allowed to)*
> "Right, so give me the short version." *(two sentences)*

**Failure:** a story cut off mid-sentence, or a fifteen second answer to three words.

---

## KNOWN BROKEN - do not spend time on these

- **Barge-in does not work.** Built and measured at 0.019s, never armed. The mic stays closed while
  it talks. Talking over it does nothing.
- **First audio is 4 to 12 seconds.** Renders are running 2 to 8s live against 0.5s on a bench and
  I have not found why.

---

## READING THE TERMINAL

```
(endpoint 0.15s: COMPLETE - 'okay so')   it decided you finished. Was it right?
YOU > ...  [2.0s of audio, heard in 0.17s]   what it actually heard
[heard: ...]                             prosody, measured. Must NEVER reach the speech.
TOOL calc({...}) -> 415074227            a tool really ran. No line means no tool ran.
IT > ...                                 what it said
[rod | first audio Xs | ... speech Xs]   the bill
```

`TOOL` and `first audio` are the two that matter: did it act, and how long did you wait.
