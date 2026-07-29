"""prosody.py - HOW IT WAS SAID, not just what was said. The cheap half of what Moshi does.

THE PROBLEM, MEASURED (convbench axis 3, 2026-07-29). The same sentence - "I really need you to do
this now" - was spoken five ways: neutral, fast, slow, high, low. Whisper returned the IDENTICAL
transcript all five times. Prosody retained: 0.00. Every bit of urgency, hesitation and emphasis
was destroyed before the mind saw a single token, and no faster rod or better prompt can recover
what the transcription stage threw away.

Moshi solves this by never leaving the audio domain: audio in, audio out, one model, ~10GB of VRAM
resident. That is not sustainable here and it also cannot call a tool, which is the thing this
entity has to be able to do.

THE INSIGHT THIS MODULE IS BUILT ON: we do not need the audio to REACH the mind. We need the
INFORMATION IN IT to. Pitch, energy, speech rate and pause structure are a few hundred
milliseconds of numpy on samples we are ALREADY CAPTURING and ALREADY THROWING AWAY. Measured as
numbers and handed to the mind as a short factual annotation, they restore most of what the
transcript deleted, at roughly zero cost and zero VRAM.

  transcript alone  "I really need you to do this now"
  with this module  "I really need you to do this now"  [spoken fast, louder than usual, pitch
                     falling, no hesitation]

THE LINE THAT DOES NOT MOVE: THIS REPORTS ACOUSTICS AND NEVER EMOTION. "Pitch rose 40 percent
above your baseline" is a measurement. "You sound angry" is an inference about a person's inner
state drawn from a microphone, and this system does not make those - the claim ceiling applies to
claims about the HUMAN as much as claims about the machine. The mind receives the numbers and does
its own interpreting, out loud, where it can be corrected.

RELATIVE TO A BASELINE, NEVER ABSOLUTE. "Loud" means nothing across different people, microphones
and rooms; D13 already paid for treating an absolute audio threshold as meaningful when a noise
floor of 0.0265 made the ear deaf to speech peaking at 0.0168. Everything here is expressed against
a rolling per-speaker baseline, and until that baseline exists the answer is a DASH, not a guess.
"""
from __future__ import annotations

import math

SR_DEFAULT = 16000
FRAME = 0.040                  # 40ms analysis frame - long enough for one pitch period at 50Hz
HOP = 0.020                    # 20ms hop
F0_MIN, F0_MAX = 60.0, 400.0   # human speech; below is rumble, above is whistle
VOICED_RATIO = 0.30            # autocorrelation peak must reach this to count as voiced

# How far from baseline before it is worth SAYING. Under these, the annotation stays silent rather
# than reporting noise as signal - a channel that comments on every turn teaches the mind nothing.
RATE_DELTA = 0.20              # 20% faster/slower than this speaker's norm
ENERGY_DELTA = 0.35            # 35% louder/quieter
PITCH_DELTA = 0.15             # 15% higher/lower median pitch


def _frames(x, sr: int):
    n = int(FRAME * sr)
    h = int(HOP * sr)
    for i in range(0, max(0, len(x) - n), h):
        yield x[i:i + n]


def f0_track(samples, sr: int = SR_DEFAULT) -> list:
    """Fundamental frequency per voiced frame, by autocorrelation.

    Autocorrelation rather than a neural pitch model on purpose: it is a few lines of numpy, costs
    single-digit milliseconds, has no weights to download and no VRAM. Octave errors are possible
    and tolerable here, because every number is consumed as a RATIO against the same speaker's own
    baseline measured by the same estimator - a systematic bias cancels, and only a change matters.
    """
    import numpy as np
    x = np.asarray(samples, dtype="float32")
    if x.size < int(FRAME * sr):
        return []
    lo, hi = int(sr / F0_MAX), int(sr / F0_MIN)
    out = []
    for fr in _frames(x, sr):
        fr = fr - fr.mean()
        e = float(np.sqrt(np.mean(fr ** 2)))
        if e < 1e-4:
            continue
        ac = np.correlate(fr, fr, mode="full")[len(fr) - 1:]
        if ac[0] <= 0:
            continue
        ac = ac / ac[0]
        seg = ac[lo:hi]
        if seg.size == 0:
            continue
        k = int(np.argmax(seg))
        if seg[k] < VOICED_RATIO:                 # unvoiced (a fricative, or silence)
            continue
        lag = lo + k
        if lag > 0:
            out.append(sr / lag)
    return out


def measure(samples, sr: int = SR_DEFAULT, text: str = "") -> dict:
    """The raw acoustics of one utterance. Numbers only - no adjectives, no interpretation."""
    import numpy as np
    x = np.asarray(samples, dtype="float32")
    if x.size == 0:
        return {}
    dur = len(x) / sr
    # energy over VOICED frames only: averaging in the silences makes a loud short phrase look
    # quiet purely because it was followed by a pause
    frame_rms = [float(np.sqrt(np.mean((f - f.mean()) ** 2))) for f in _frames(x, sr)]
    if not frame_rms:
        return {}
    peak = max(frame_rms)
    speech = [r for r in frame_rms if r > peak * 0.20]
    energy = sum(speech) / len(speech) if speech else 0.0
    # internal pauses: runs of low frames INSIDE the utterance, which is hesitation rather than
    # the endpoint silence that ends it
    quiet = [r <= peak * 0.15 for r in frame_rms]
    runs, cur = [], 0
    for q in quiet:
        if q:
            cur += 1
        elif cur:
            runs.append(cur * HOP); cur = 0
    pauses = [p for p in runs if p >= 0.15]
    f0 = f0_track(x, sr)
    words = len([w for w in (text or "").split() if w.strip()])
    speech_dur = max(0.05, dur - sum(runs))
    out = dict(
        duration=round(dur, 3),
        speech_duration=round(speech_dur, 3),
        energy=round(energy, 5),
        peak=round(peak, 5),
        words=words,
        rate_wps=round(words / speech_dur, 2) if words else None,
        pauses=len(pauses),
        pause_total=round(sum(pauses), 2),
    )
    if f0:
        f0s = sorted(f0)
        med = f0s[len(f0s) // 2]
        out.update(f0_median=round(med, 1), f0_voiced_frames=len(f0),
                   f0_p10=round(f0s[int(len(f0s) * 0.10)], 1),
                   f0_p90=round(f0s[int(len(f0s) * 0.90)], 1))
        # terminal contour: the last quarter against the middle. A rise at the end is the single
        # most informative prosodic cue in English - it separates a question from a statement, and
        # the transcript only carries that when the speaker's words happened to make it explicit.
        if len(f0) >= 8:
            tail = f0[int(len(f0) * 0.75):]
            body = f0[:int(len(f0) * 0.75)]
            if tail and body:
                bm = sorted(body)[len(body) // 2]
                tm = sorted(tail)[len(tail) // 2]
                out["f0_slope"] = round((tm - bm) / bm, 3) if bm else None
    return out


def update_baseline(base: dict, m: dict, alpha: float = 0.25) -> dict:
    """Roll this speaker's norm forward. Exponential, so it tracks a person changing position or
    microphone without one loud turn redefining them - which is exactly the failure D13 recorded
    when a noise floor was set by `max()` and one transient deafened the ear for the whole session.
    """
    base = dict(base or {})
    base["n"] = int(base.get("n", 0)) + 1
    for k in ("energy", "rate_wps", "f0_median", "speech_duration"):
        v = m.get(k)
        if v is None:
            continue
        cur = base.get(k)
        base[k] = v if cur is None else round(cur * (1 - alpha) + v * alpha, 5)
    return base


def describe(m: dict, base: dict) -> str:
    """The annotation handed to the mind. Acoustics only, and SILENT when nothing is unusual.

    Returns "" rather than a reassuring "spoken normally", because an annotation on every single
    turn is noise that the mind learns to ignore, and because absence is the honest rendering of
    "nothing here differs from this speaker's norm" (law H1: a dash, never a guess).
    """
    if not m:
        return ""
    n = int((base or {}).get("n", 0))
    if n < 3:
        # NOT ENOUGH BASELINE TO COMPARE AGAINST. Saying "spoken quickly" against two samples is a
        # measurement pretending to be one. The channel stays quiet until it has earned the right
        # to speak, and says so if asked.
        return ""
    bits = []
    r, br = m.get("rate_wps"), (base or {}).get("rate_wps")
    if r and br:
        d = (r - br) / br
        if d > RATE_DELTA:
            bits.append("faster than usual")
        elif d < -RATE_DELTA:
            bits.append("slower than usual")
    e, be = m.get("energy"), (base or {}).get("energy")
    if e and be:
        d = (e - be) / be
        if d > ENERGY_DELTA:
            bits.append("louder than usual")
        elif d < -ENERGY_DELTA:
            bits.append("quieter than usual")
    f, bf = m.get("f0_median"), (base or {}).get("f0_median")
    if f and bf:
        d = (f - bf) / bf
        if d > PITCH_DELTA:
            bits.append("higher pitched than usual")
        elif d < -PITCH_DELTA:
            bits.append("lower pitched than usual")
    s = m.get("f0_slope")
    if s is not None:
        if s > 0.08:
            bits.append("pitch rising at the end")
        elif s < -0.08:
            bits.append("pitch falling at the end")
    if m.get("pauses", 0) >= 2 and m.get("pause_total", 0) >= 0.5:
        bits.append(f"{m['pauses']} pauses mid-sentence")
    return ", ".join(bits)


# ---------------------------------------------------------------- NOTICING, not narrating
# Luis, after hearing it comment on his voice ten turns running: "maybe humans don't like that all
# the time, sometimes, but more about IF SOMETHING WRONG HAPPENED. Let's say someone was talking
# and shut up before a moment, then it can ask, what is happening? Why did you just shut up?"
#
# That is the correct design and it is the one the research independently recommended: fire on a
# CHANGE, not on every turn, and ASK rather than diagnose. A signal that fires every turn carries
# no information, which is why continuous commentary felt intrusive AND useless at the same time.
#
# THE CRITICAL DETAIL, learned the expensive way: what reaches the mind is a TOKEN, never a
# description. Given "spoke 60% shorter than usual with falling pitch" the model narrates the
# measurement back at the person - measured, ten turns out of ten. Given `cut_short` there is
# nothing to narrate, and the only thing it can do with it is ask.
NOTICE_COOLDOWN = 4          # turns. A noticing that fires often is commentary again.
SHORT_RATIO = 0.45           # this turn under 45% of their usual length
QUIET_RATIO = 0.55           # under 55% of their usual energy
LONG_PAUSE = 1.2             # seconds of internal pause


def notice(m: dict, base: dict, since_last: int = 99) -> str:
    """Has something CHANGED enough to be worth asking about. Returns a token, or "".

    Returns at most ONE token, and usually nothing - that is the point. Requires an established
    baseline (law H1: without one there is nothing to deviate from, and a guess is worse than a
    gap) and a cooldown, so it cannot slide back into narrating every turn.
    """
    if not m or int((base or {}).get("n", 0)) < 5 or since_last < NOTICE_COOLDOWN:
        return ""
    dur, bdur = m.get("speech_duration"), (base or {}).get("speech_duration")
    e, be = m.get("energy"), (base or {}).get("energy")
    # CUT SHORT - Luis's own example: they were going somewhere and stopped.
    if dur and bdur and dur < bdur * SHORT_RATIO and m.get("words", 0) <= 4:
        return "cut_short"
    # TRAILED OFF - a long internal pause and then nothing much after it.
    if m.get("pauses", 0) >= 2 and m.get("pause_total", 0) >= LONG_PAUSE:
        return "trailed_off"
    # WENT QUIET - well under their own usual level, sustained across the whole utterance.
    if e and be and e < be * QUIET_RATIO and (dur or 0) > 0.8:
        return "went_quiet"
    return ""


# What the mind is told, for each token. A short instruction to ASK - never a measurement, and
# never a claim about what the person feels. The wording is the ceiling: "you noticed" is about
# the machine's observation, not about their inner state.
NOTICE_PROMPT = {
    "cut_short": "They started saying something and stopped much sooner than they usually do. "
                 "Ask what happened, briefly and without making it a big deal.",
    "trailed_off": "They paused in the middle and trailed off. Gently invite them to finish the "
                   "thought. Do not guess what it was.",
    "went_quiet": "They are speaking much more quietly than they normally do with you. Check in "
                  "once, lightly. Do not tell them how they feel or why.",
}


def annotate(samples, sr: int, text: str, base: dict) -> tuple:
    """One call for the caller: -> (annotation_or_empty, raw_measurements, updated_baseline)."""
    m = measure(samples, sr, text)
    note = describe(m, base)
    return note, m, update_baseline(base, m)


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from aea.io import listen
    if len(sys.argv) > 1 and sys.argv[1].endswith(".wav"):
        s, sr = listen.read_wav(sys.argv[1])
        m = measure(s, sr, " ".join(sys.argv[2:]))
        for k, v in sorted(m.items()):
            print(f"  {k:20s} {v}")
    else:
        print(__doc__)
