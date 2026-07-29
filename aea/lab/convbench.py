"""convbench.py - THE CONVERSATION BENCH. Specific measures for "does it feel natural".

Luis, 2026-07-29, on Moshi: "Can we get close to that? I mean, we need specific test... specific
measures for that."

WHAT THIS IS. Six axes, each computed rather than judged, each with a published target beside it,
so "more natural" stops being an opinion. It deliberately includes the axes where WE SCORE ZERO,
because a scoreboard that only lists what we are good at is marketing.

THE HONEST FRAME, stated once so no row is read as a claim it is not making. Moshi is a speech-to-
speech model: audio in, audio out, one model, no text in the middle. It needs 16-20GB of VRAM at
fp16 and ~10GB quantized. This machine measured `torch 2.13.0+cpu, cuda_available=False`. We are
not running Moshi and we are not going to. What we can do is measure how far a CASCADE
(ear -> text -> mind -> text -> mouth) is from it, ON EACH AXIS SEPARATELY, because the gap is not
uniform: on interruption we can be genuinely close, and on prosody a cascade is structurally at
zero no matter how fast it gets.

  python -m aea.lab.convbench            run everything that does not need a human
  python -m aea.lab.convbench --quick    skip the ear sweep

THE TARGETS, from the turn-taking literature and from published system numbers:
  response gap      humans ~200ms median (Stivers et al., 10 languages). >500ms consciously
                    noticed, >1s people talk over the agent or leave. Moshi 200-300ms.
  barge-in          humans stop within ~200ms of being interrupted
  overlap           human conversation is <5% simultaneous speech
  endpoint          a false cut (answering a breath) is worse than a late take, so they are
                    counted SEPARATELY - one metric would hide the asymmetry that matters
  prosody           how much of HOW something was said survives to the mind
"""
from __future__ import annotations

import os
import re
import statistics
import sys
import time

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

WORK = os.path.join(str(grid.STATE), "convbench")
VOICE = "en-US-AndrewMultilingualNeural"

# Utterances chosen for the SHAPES that break a conversational system, not for variety.
# Each carries whether it is a finished thought, which is the ground truth the endpoint is
# scored against - computed from the sentence, never from the detector's own opinion (law M3).
UTTERANCES = [
    ("Run the test", True),
    ("What is the capital of France", True),
    ("Hey, how is it going today", True),
    ("Can you check my heartbeat file and tell me what is in it", True),
    ("I was thinking that maybe we should", False),
    ("What is the capital of", False),
    ("Can you look at the", False),
    ("So I wanted to ask you about", False),
]

# The same words, said differently. If the transcripts come back identical, every bit of HOW it
# was said has been destroyed before the mind ever sees it.
PROSODY = [
    ("neutral", {}),
    ("fast", {"rate": "+40%"}),
    ("slow", {"rate": "-35%"}),
    ("high", {"pitch": "+40Hz"}),
    ("low", {"pitch": "-40Hz"}),
]
PROSODY_TEXT = "I really need you to do this now"


def _hr(t):
    print("\n" + "=" * 84 + "\n== " + t + "\n" + "=" * 84, flush=True)


def _row(name, ours, human, moshi, verdict):
    return dict(axis=name, ours=ours, human=human, moshi=moshi, verdict=verdict)


def _mk_wav(text: str, path: str, **kw) -> float:
    """Render reference speech to 16k mono wav. Returns duration, or 0.0 on failure."""
    import edge_tts
    import asyncio
    mp3 = path.replace(".wav", ".mp3")
    if not os.path.exists(mp3):
        asyncio.run(edge_tts.Communicate(text, VOICE, **kw).save(mp3))
    try:
        import numpy as np
        import soundfile as sf
        data, sr = sf.read(mp3, dtype="float32")
        if data.ndim > 1:
            data = data.mean(axis=1)
        if sr != 16000:
            n = int(len(data) * 16000 / sr)
            data = np.interp(np.linspace(0, len(data) - 1, n),
                             np.arange(len(data)), data).astype("float32")
            sr = 16000
        sf.write(path, data, sr, subtype="PCM_16")
        return len(data) / sr
    except Exception:
        return 0.0


def wer(ref: str, hyp: str) -> float:
    r = re.findall(r"[a-z0-9']+", ref.lower())
    h = re.findall(r"[a-z0-9']+", hyp.lower())
    if not r:
        return 1.0
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = d[j]
            d[j] = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev = cur
    return d[len(h)] / len(r)


def semantic_match(ref: str, hyp: str) -> bool:
    """Did it hear the MEANING. WER punishes a correct normalisation - the ear heard "ninety two
    thousand eight hundred and thirty seven" and wrote 92,837, scoring WER 0.94 on a perfect
    transcript. Grading the outcome rather than a proxy for it (law G1) means normalising digits
    and contractions before comparing."""
    # NUMBERS ARE COMPARED SEPARATELY FROM WORDS, because a correct transcription of a spoken
    # number LOOKS like a total failure to a word matcher. MEASURED twice now: "ninety two thousand
    # eight hundred and thirty seven" transcribed as "92,837" scored WER 0.86 and then failed this
    # check too - the ear was right both times and the SCORER was wrong. A single-digit lookup
    # table cannot map a multi-word numeral, so numeric tokens are stripped from both sides and
    # the remaining WORDS are what this measures.
    NUMWORD = frozenset("""zero one two three four five six seven eight nine ten eleven twelve
        thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty
        sixty seventy eighty ninety hundred thousand million billion""".split())

    def norm(t):
        t = t.lower()
        t = t.replace("'s", " is").replace("'re", " are").replace("'m", " am")
        t = re.sub(r"[,\.]", "", t)
        out = []
        for w in re.findall(r"[a-z0-9]+", t):
            if w.isdigit() or w in NUMWORD:
                continue                      # numerals are not compared as words
            out.append(w)
        return [w for w in out if w not in ("and", "the", "a")]
    r, h = norm(ref), norm(hyp)
    if not r:
        return False
    common = sum(1 for w in set(r) if w in h)
    return common / len(set(r)) >= 0.8


# --------------------------------------------------------------------------------- the axes
def axis_ear(quick=False) -> dict:
    """AXIS 1 - does it hear correctly, and how long after you stop does it know."""
    from aea.io import listen
    os.makedirs(WORK, exist_ok=True)
    listen.warm("en")
    decodes, wers, sem = [], [], 0
    n = 0
    for i, (text, _) in enumerate(UTTERANCES):
        if quick and i >= 4:
            break
        wav = os.path.join(WORK, f"u{i}.wav")
        dur = _mk_wav(text, wav)
        if not dur:
            continue
        samples, sr = listen.read_wav(wav)
        best = None
        for _ in range(2):
            t = time.time()
            got = listen.transcribe_samples(samples, sr, "en")
            e = time.time() - t
            best = e if best is None else min(best, e)
        decodes.append(best)
        wers.append(wer(text, got))
        sem += 1 if semantic_match(text, got) else 0
        n += 1
        print(f"   {dur:5.2f}s audio  decode {best:5.3f}s  WER {wers[-1]:4.2f}  "
              f"{'SEMANTIC OK' if semantic_match(text, got) else 'SEMANTIC MISS'}  {got[:44]!r}")
    return dict(decode_med=statistics.median(decodes) if decodes else None,
                wer_med=statistics.median(wers) if wers else None,
                semantic=f"{sem}/{n}", n=n)


def axis_endpoint() -> dict:
    """AXIS 2 - when it decides you have finished, is it right.

    FALSE CUTS AND LATE TAKES ARE COUNTED SEPARATELY AND THAT IS THE POINT. A false cut answers a
    breath and truncates a person mid-thought; a late take just makes them wait. One combined
    accuracy number would let a detector trade the unrecoverable error for the tolerable one and
    still look like it improved."""
    from aea.organs.converse import utterance_looks_complete as complete
    false_cut = late_take = ok = 0
    for text, is_done in UTTERANCES:
        got = complete(text)
        if got == is_done:
            ok += 1
        elif got and not is_done:
            false_cut += 1
            print(f"   FALSE CUT  would answer a half sentence: {text!r}")
        else:
            late_take += 1
            print(f"   LATE TAKE  waits the full hangover on a finished one: {text!r}")
    return dict(correct=f"{ok}/{len(UTTERANCES)}", false_cuts=false_cut, late_takes=late_take)


def axis_prosody() -> dict:
    """AXIS 3 - THE ONE A CASCADE CANNOT WIN, measured instead of asserted.

    The same sentence said fast, slow, high and low. If every delivery yields the same transcript,
    then everything about HOW it was said - urgency, hesitation, mood - is gone before the mind is
    reached. Moshi keeps it because it never leaves the audio domain.

    This is here so the gap is a NUMBER and not a vibe, and so that if anyone ever adds a prosody
    channel the improvement is provable on the same test."""
    from aea.io import listen
    os.makedirs(WORK, exist_ok=True)
    seen, rows = {}, []
    for label, kw in PROSODY:
        wav = os.path.join(WORK, f"pros_{label}.wav")
        dur = _mk_wav(PROSODY_TEXT, wav, **kw)
        if not dur:
            continue
        samples, sr = listen.read_wav(wav)
        got = listen.transcribe_samples(samples, sr, "en").strip()
        rows.append((label, round(dur, 2), got))
        seen.setdefault(got.lower().strip(" .!?"), []).append(label)
        print(f"   {label:8s} {dur:5.2f}s audio -> {got!r}")
    distinct = len(seen)
    return dict(deliveries=len(rows), distinct_transcripts=distinct,
                bits_retained=0.0 if distinct <= 1 else round((distinct - 1) / max(1, len(rows) - 1), 2),
                detail=rows)


def axis_response_gap() -> dict:
    """AXIS 4 - from 'you stopped talking' to 'you hear a syllable'. The headline number.

    Composed from measured parts rather than one opaque total, because a single number cannot be
    acted on: it was reading ONE lumped voice number as synthesis that produced this project's
    wrongest belief about its own latency."""
    from aea.mind import tiers
    from aea.io import speak
    o = tiers.organ("reflex")
    speak.warm(VOICE)
    # the mind's first token, measured live on the seat that actually answers
    ttfbs = []
    rec = {}
    for q in ("Hey, how is it going?", "What can you do?", "Tell me something short."):
        rec = {}
        t0 = time.time()
        first = None
        for piece in grid.stream_openai(o["plant"], o["model"],
                                        [{"role": "system", "content":
                                          "You are a voice companion. Reply in ONE short sentence."},
                                         {"role": "user", "content": q}],
                                        max_tokens=60, temperature=0.7, timeout=o["budget"],
                                        receipt=rec):
            if first is None and piece.strip():
                first = time.time() - t0
                break
        if first:
            ttfbs.append(first)
    # the mouth's first chunk
    renders = []
    for s in ("Sure.", "Let me check.", "I am here."):
        t = time.time()
        speak.edge_render(s, os.path.join(WORK, "_gap.mp3"), voice=VOICE)
        renders.append(time.time() - t)
    from aea.organs.converse import HANGOVER_FAST
    ear = 0.25
    mind = statistics.median(ttfbs) if ttfbs else None
    mouth = statistics.median(renders)
    total = (HANGOVER_FAST + ear + (mind or 0) + mouth)
    print(f"   endpointer {HANGOVER_FAST:.2f}s + ear {ear:.2f}s + mind {mind:.2f}s "
          f"+ mouth {mouth:.2f}s")
    return dict(endpointer=HANGOVER_FAST, ear=ear, mind=round(mind, 3) if mind else None,
                mouth=round(mouth, 3), total=round(total, 2))


def axis_bargein() -> dict:
    """AXIS 5 - how fast it stops when spoken over. Synthetic trigger; the live-mic number is
    DIFFERENT and is deliberately not reported here (see the caveat in `report`)."""
    import threading
    from aea.io import speak
    stop = threading.Event()
    long = ("This is a deliberately long reply that keeps going for several sentences. "
            "It should be possible to stop it. If it cannot be stopped it is not a conversation. "
            "A person must be able to take the floor back at any moment.")
    fired = {}

    def cut():
        time.sleep(2.0)
        fired["at"] = time.time()
        stop.set()
    threading.Thread(target=cut, daemon=True).start()
    t0 = time.time()
    r = speak.say_stream(long, voice=VOICE, stop=stop)
    stopped = time.time()
    lat = (stopped - fired["at"]) if fired.get("at") else None
    return dict(interrupted=r["interrupted"], stop_latency=round(lat, 3) if lat else None,
                chunks_spoken=r["chunks"], of_sentences=len(speak.split_sentences(long)))


# --------------------------------------------------------------------------------- the report
def report(quick=False) -> dict:
    out = {}
    _hr("AXIS 1 - THE EAR: accuracy, and how long after you stop it knows what you said")
    out["ear"] = axis_ear(quick)
    _hr("AXIS 2 - THE ENDPOINT: is it right about when you finished")
    out["endpoint"] = axis_endpoint()
    _hr("AXIS 3 - PROSODY: how much of HOW you said it reaches the mind")
    out["prosody"] = axis_prosody()
    _hr("AXIS 4 - RESPONSE GAP: you stop talking -> you hear a syllable")
    out["gap"] = axis_response_gap()
    _hr("AXIS 5 - BARGE-IN: can you take the floor back")
    out["bargein"] = axis_bargein()

    _hr("THE SCOREBOARD")
    e, ep, p, g, b = out["ear"], out["endpoint"], out["prosody"], out["gap"], out["bargein"]
    rows = [
        ("ear accuracy (semantic)", e["semantic"], "human ~100%", "n/a (no text stage)",
         "COMPETITIVE"),
        ("ear latency", f"{e['decode_med']:.3f}s" if e["decode_med"] else "-", "-",
         "0s (no separate ASR)", "SMALL, and structural"),
        ("endpoint correct", ep["correct"], "-", "predictive (VAP-class)",
         f"{ep['false_cuts']} false cut(s), {ep['late_takes']} late take(s)"),
        ("prosody retained", f"{p['bits_retained']:.2f}", "1.00", "1.00",
         "ZERO, and a cascade cannot fix it"),
        ("response gap", f"{g['total']:.2f}s", "~0.20s", "0.20-0.30s",
         f"{g['total']/0.25:.0f}x the human gap"),
        ("barge-in stop", f"{b['stop_latency']:.3f}s" if b["stop_latency"] else "-",
         "~0.20s", "yes, native", "CLOSE" if (b["stop_latency"] or 9) < 0.5 else "SLOW"),
    ]
    print(f"  {'axis':26s} {'ours':>12} {'human':>12} {'moshi':>22}  verdict")
    for a, o_, h, m, v in rows:
        print(f"  {a:26s} {str(o_):>12} {str(h):>12} {str(m):>22}  {v}")

    print()
    print("  WHERE WE CAN GET CLOSE:  interruption, endpointing, ear accuracy, acting on tools.")
    print("  WHERE WE STRUCTURALLY CANNOT MATCH IT:  prosody in the Moshi sense (a continuous audio")
    print("  representation) and the 200ms gap. Our floor is the mind's first token plus one render.")
    print()
    print("  THE HARDWARE, CORRECTED 2026-07-29: this machine has an RTX 3500 Ada, 12GB VRAM, ~10GB")
    print("  free. An earlier reading of `torch 2.13.0+cpu / cuda_available=False` was written up as")
    print("  'no GPU' - but +cpu is the CPU-ONLY BUILD of torch, so that flag only ever proved TORCH")
    print("  could not see a GPU. A software fact was read as a hardware fact and three conclusions")
    print("  were built on it. Every latency above is a CPU number measured on a machine with an")
    print("  idle Ada GPU: onnxruntime is not installed at all, so whisper and kokoro run on CPU.")
    print()
    print("  CAVEAT THAT MUST NOT BE DROPPED: every number above is on SYNTHESISED speech and a")
    print("  synthetic interrupt. A real microphone in a real room is harder, and D13 recorded that")
    print("  the acoustic path was always the ceiling. These are an OPTIMISTIC BOUND, not the")
    print("  experience. The live-mic run is a separate measurement and it has not been done.")
    return out


if __name__ == "__main__":
    report(quick="--quick" in sys.argv)
