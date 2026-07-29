# SAY THIS - the ear check, five phrases

*Read this card, not my chat messages. I am deliberately out of the loop this time - the last run
was ruined because you were speaking to my "Go" instead of the terminal's, and the recording
windows and your voice ended up in different places.*

---

## HOW IT WORKS NOW

There is **no countdown**. For each phrase it will:

1. **Say the phrase out loud to you**
2. Print `listening (room 0.0028, speak when ready)...`
3. **Wait** - as long as you need, up to 25 seconds
4. Print `(got you - keep going, stop when done)` the moment it hears you
5. Stop recording ~1.3s after you stop talking

**Take your time.** Nothing is on a clock. If it says `still waiting... your peak 0.004 vs gate
0.006` you are below the trigger - get closer or speak up.

---

## THE FIVE PHRASES

Say each one **exactly as written**, at a normal conversational level, the way you would actually
talk to it. Do not over-enunciate - that measures a version of you that never uses the thing.

### 1. "Okay so"

Two words. This is the phrase that came back as **"Creysau"** and cut you off mid-thought.

### 2. "What are your laws"

Four words with a domain term. Came back as **"Where you lost."**

### 3. "Hit me with the question"

Came back as **"and not meet with the question."** *(Already transcribed perfectly once at a good
level - this confirms it.)*

### 4. "It's just that I feel like when I talk you don't understand all my words"

The long one. Long sentences have always come back clean, so this is the control: if a long
sentence fails at a good level, the model really is the limit.

### 5. "Multiply ninety two thousand by four thousand"

Numbers. Whisper normalises spoken numerals to digits, which is correct and which my first scoring
attempt wrongly counted as a failure.

---

## WHAT IT IS MEASURING

For each phrase it reports:

```
signal: peak 0.315  SNR 22dB  voiced 39%  clipped 0
```

| | good | bad |
|---|---|---|
| **peak** | 0.1 to 0.5 | under 0.05 means the mic is barely hearing you |
| **SNR** | above 20dB | under 15dB and no software can recover it |
| **voiced** | 30%+ | low means most of the recording is room, not you |
| **clipped** | 0 | above 50 means the gain is too high |

Then it names ONE cause: **MIC**, **ROOM**, or **MODEL**. Those need three different fixes and
guessing between them is how an hour disappears.

---

## WHAT WE ALREADY KNOW

- **Your level swings 25x** between utterances, from 0.012 to 0.315. That is the real problem, not
  the model.
- **whisper-base is good enough.** At peak 0.202 it transcribed "Hit me with the question" word for
  word - the exact phrase that failed in conversation. Do not let me talk you into a 636MB
  download until this run says otherwise.
- **The Odyssey monitor is your audio output** and it works. You confirmed hearing the test tones.
- **Device 1 is the V3 cam.** MME truncates the name at 31 characters, so "Microphone (Creative
  Live! Cam " is the same physical mic as the full-named entries 7 and 14 - and the only one of the
  three that carries signal at all.

---

## RUN IT

```
python -m aea.io.earcheck --device 1 --keep
```

Then just follow the terminal. Ignore me until it finishes.
