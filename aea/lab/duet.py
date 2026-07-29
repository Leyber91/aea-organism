"""duet.py - TWO MODELS HOLD A CONVERSATION THROUGH THE LAYER, with no human in the loop.

Luis, 2026-07-29: "we want this to be a LAYER OVER THE MODEL. We don't want the model to do the
conversation itself."

That is the thesis, and this is the experiment that can falsify it. If conversational ability lives
in the layer rather than in the weights, then TWO DIFFERENT RODS - neither of them trained for
dialogue, neither aware the other is a model - should be able to hold a conversation through it.
If the ability actually lives in the model, this will produce two monologues.

IT RUNS THROUGH THE REAL PIPELINE, WHICH IS THE ONLY REASON IT PROVES ANYTHING:

    rod A writes  ->  edge-tts SPEAKS it to real audio  ->  whisper HEARS the audio back
                  ->  prosody MEASURES how it sounded   ->  rod B receives transcript + annotation
                  ->  rod B writes ...

Nothing is passed as a string between the two rods. Every turn is synthesised to audio and
transcribed back, so the loop pays the FULL cost of the layer - transcription error, endpointing,
prosody, latency - exactly as it does with a person. A version that handed text straight across
would be measuring nothing but two prompts (law B2: test the property, never a proxy for it).

  python -m aea.lab.duet                    6 turns, silent, prints the transcript + numbers
  python -m aea.lab.duet --turns 10 --aloud play it through the speakers so a human can listen

WHAT IT MEASURES, and the interesting one is the third:
  fidelity   what A SAID vs what B HEARD, word-level. This is the layer's tax, and it is the
             number a text-passing demo would hide entirely.
  gap        wall-clock per turn, decomposed into mind / mouth / ear
  prosody    how often the annotation channel carried something, since a flat exchange should
             produce fewer notes than an animated one
"""
from __future__ import annotations

import os
import re
import statistics
import sys
import time

from aea.kernel import grid
from aea.io import listen, prosody, speak
from aea.mind import tiers

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

WORK = os.path.join(str(grid.STATE), "duet")

# TWO DIFFERENT RODS, DELIBERATELY. Same rod twice would be a model talking to itself, which tests
# nothing about whether the LAYER carries the conversation. Both are measured tool-callers and
# both are fast enough to keep the exchange inside a listenable rhythm (state/rods.json).
SPEAKERS = [
    dict(name="ORA", plant="nvidia", model="meta/llama-3.1-8b-instruct",
         voice="en-US-AndrewMultilingualNeural",
         persona="You are curious and direct. You ask short real questions."),
    dict(name="VEL", plant="nvidia", model="nvidia/llama-3.3-nemotron-super-49b-v1",
         voice="en-US-AvaMultilingualNeural",
         persona="You are thoughtful and concrete. You give specific answers, never vague ones."),
]

SEED = "So what do you actually think about running a mind on somebody's laptop?"

FRAME = ("You are having a SPOKEN conversation. Your reply is read aloud, so write to be HEARD: "
         "ONE or TWO short sentences, no lists, no formatting, no emoji, no stage directions. "
         "You are a machine and you never pretend otherwise. Do not restate what was just said. "
         "Sometimes a bracketed note like [heard: slower than usual] follows their line - that is "
         "a MEASUREMENT of their voice, not words they said. Never read it aloud.")


def _words(t):
    return re.findall(r"[a-z0-9']+", (t or "").lower())


def fidelity(said: str, heard: str) -> float:
    """Fraction of A's words that survived the round trip into B's ears. 1.0 is perfect.

    This is THE number that a text-passing demo cannot produce, and it is the honest price of the
    layer: every point below 1.0 is meaning the architecture destroyed on the way through."""
    a, b = set(_words(said)), set(_words(heard))
    return round(len(a & b) / max(1, len(a)), 3)


def one_turn(sp: dict, history: list, incoming: str, note: str, aloud: bool, idx: int) -> dict:
    """One rod hears, thinks, and speaks. Returns the receipt for that turn."""
    msgs = [{"role": "system", "content": FRAME + "\n" + sp["persona"]
             + f"\nYou are called {sp['name']}."}]
    for who, text in history[-8:]:
        msgs.append({"role": "assistant" if who == sp["name"] else "user", "content": text})
    msgs.append({"role": "user",
                 "content": incoming + (f"   [heard: {note}]" if note else "")})

    t0 = time.time()
    rec: dict = {}
    parts = []
    for piece in grid.stream_openai(sp["plant"], sp["model"], msgs, max_tokens=90,
                                    temperature=0.8, timeout=12, receipt=rec):
        parts.append(piece)
    said = re.sub(r"\s+", " ", "".join(parts)).strip()
    said = re.sub(r"\*[^*]{1,40}\*", " ", said).strip()
    # cap at two sentences, the same bound the live organ enforces
    sents = [s for s in re.split(r"(?<=[.!?])\s+", said) if s.strip()][:2]
    said = " ".join(sents).strip()
    t_mind = time.time() - t0

    if not said:
        return dict(ok=False, speaker=sp["name"], said="", error=rec.get("error"),
                    t_mind=round(t_mind, 2))

    # SPEAK IT FOR REAL - to a file, and optionally to the speakers
    os.makedirs(WORK, exist_ok=True)
    mp3 = os.path.join(WORK, f"t{idx:02d}_{sp['name']}.mp3")
    t1 = time.time()
    ok = speak.edge_render(said, mp3, voice=sp["voice"])
    t_mouth = time.time() - t1
    if not ok:
        return dict(ok=False, speaker=sp["name"], said=said, error="render failed",
                    t_mind=round(t_mind, 2))
    if aloud:
        speak.play_mp3(mp3)

    # HEAR IT BACK through the real ear, from the real audio
    wav = mp3.replace(".mp3", ".wav")
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
        sf.write(wav, data, sr, subtype="PCM_16")
        samples, sr = listen.read_wav(wav)
    except Exception as e:
        return dict(ok=False, speaker=sp["name"], said=said, error=f"audio: {e}")

    t2 = time.time()
    heard = listen.transcribe_samples(samples, sr, "en").strip()
    t_ear = time.time() - t2

    return dict(ok=True, speaker=sp["name"], said=said, heard=heard, samples=samples, sr=sr,
                t_mind=round(t_mind, 2), t_mouth=round(t_mouth, 2), t_ear=round(t_ear, 2),
                ttfb=rec.get("ttfb"), fidelity=fidelity(said, heard),
                audio_s=round(len(samples) / sr, 2), path=mp3)


def run(turns: int = 6, aloud: bool = False) -> dict:
    print("=" * 88)
    print("DUET - two rods in conversation, THROUGH the real audio layer")
    print("=" * 88)
    for s in SPEAKERS:
        print(f"  {s['name']:4s} {s['model']:44s} {s['voice']}")
    print(f"  every turn: mind -> edge-tts -> REAL AUDIO -> whisper -> prosody -> the other rod")
    print(f"  {'playing aloud' if aloud else 'silent (pass --aloud to hear it)'}\n")
    listen.warm("en")
    speak.warm(SPEAKERS[0]["voice"])

    history, rows = [], []
    incoming, note = SEED, ""
    base = {}
    print(f"  SEED > {SEED}\n")
    for i in range(turns):
        sp = SPEAKERS[i % 2]
        r = one_turn(sp, history, incoming, note, aloud, i)
        if not r.get("ok"):
            print(f"  {sp['name']} FAILED: {r.get('error')}")
            break
        # measure HOW it sounded, off the same audio the next rod will "hear"
        note, _m, base = prosody.annotate(r["samples"], r["sr"], r["heard"], base)
        rows.append(r)
        history.append((sp["name"], r["said"]))
        incoming = r["heard"]          # THE NEXT ROD GETS WHAT WAS HEARD, NOT WHAT WAS SAID
        print(f"  {sp['name']} > {r['said']}")
        if r["heard"].lower().strip(" .,!?") != r["said"].lower().strip(" .,!?"):
            print(f"        heard as: {r['heard']}")
        print(f"        [ttfb {r['ttfb']}s mind {r['t_mind']}s mouth {r['t_mouth']}s "
              f"ear {r['t_ear']}s | {r['audio_s']}s speech | fidelity {r['fidelity']}]"
              + (f"  [heard: {note}]" if note else ""))
        print()

    if not rows:
        print("  no turns completed")
        return {}

    print("=" * 88)
    print("WHAT THE LAYER COST")
    print("=" * 88)
    fid = [r["fidelity"] for r in rows]
    mind = [r["t_mind"] for r in rows]
    mouth = [r["t_mouth"] for r in rows]
    ear = [r["t_ear"] for r in rows]
    print(f"  turns completed        {len(rows)}")
    print(f"  fidelity  median       {statistics.median(fid):.3f}   worst {min(fid):.3f}")
    print(f"  mind      median       {statistics.median(mind):.2f}s")
    print(f"  mouth     median       {statistics.median(mouth):.2f}s")
    print(f"  ear       median       {statistics.median(ear):.2f}s")
    print(f"  layer round trip       {statistics.median(mouth) + statistics.median(ear):.2f}s"
          f"   (mouth + ear, the tax a text-passing demo would hide)")
    perfect = sum(1 for f in fid if f >= 0.999)
    print(f"  turns heard perfectly  {perfect}/{len(rows)}")
    print()
    print("  THE THESIS UNDER TEST: if the conversation lives in the LAYER, two rods that were")
    print("  never trained to converse with each other should hold a coherent exchange here.")
    print("  Read the transcript above and judge that; the numbers only say what it cost.")
    print(f"\n  audio: {WORK}")
    return dict(turns=len(rows), fidelity=statistics.median(fid), rows=rows)


if __name__ == "__main__":
    a = sys.argv[1:]
    n = int(a[a.index("--turns") + 1]) if "--turns" in a else 6
    run(turns=n, aloud="--aloud" in a)
