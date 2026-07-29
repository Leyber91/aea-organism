# RESUME - read this first after the context is compressed

*2026-07-29. Written deliberately before compaction. Everything below is on disk and pushed
(`ebdb705` on `wip/checkpoint-2026-07-22`). Nothing important lives only in the conversation.*

---

## THE ONE THING TO CARRY

**Nine of the eleven wrong beliefs this session came from an instrument, a record, or a reading of
one - not from a model.** Whisper was fine, the mic was fine, the speakers were fine, the rods were
fine. What was broken: how a receipt was read, which field name was guessed, what a scorer assumed,
and twice, me putting myself inside a timing-critical measurement loop.

Before believing any finding, ask what would have to be true of the INSTRUMENT for it to be false,
and test that first.

---

## STATE

```
committed + pushed   ebdb705  38 files, 7082 insertions
battery              173/174, every error direction at zero
selfcheck            7 invariants, 46 frozen behaviours
crystals             11 (6 HOLDING) - diary/CRYSTALS_VOICE.md
```

**Read in this order:** `diary/NOTES_VOICE_2026-07-29.md` (every defect, four-part format) ->
`diary/CRYSTALS_VOICE.md` (the lessons, derived from runs) -> `diary/VOICE_QUALITIES.md` (how to
test it with a person).

---

## SETTLED - do not re-litigate

- **whisper-base is adequate.** All five previously-failing phrases transcribed perfectly at 26dB
  SNR. Every mishearing traced to input level, which swings **25x** (peak 0.012 to 0.315). I was
  one command from downloading whisper-small **twice**, both times on evidence about the signal.
- **edge-tts is the right mouth.** ~0.5s flat, one round trip. Local Kokoro is rtf 0.27-0.31 and
  3x slower. NVIDIA serves NO TTS on our REST path (102 models, only riva-translate).
- **The GPU is real but unreachable from the speech stack.** RTX 3500 Ada, 12GB, ~10GB free.
  sherpa-onnx is compiled CPU-only and bundles its own onnxruntime, so `provider="cuda"` is
  accepted and ignored (cpu 0.330s vs cuda 0.413s). `pip install onnxruntime-gpu` does NOTHING.
- **Emotion labels are refused on evidence.** Interspeech 2025 SER winner: macro-F1 0.4316 on
  natural speech. Same pipeline scores 75.00% acted vs 42.58% spontaneous. Annotator agreement
  kappa 0.23. The best valence results come from reading the WORDS, so a "mood" number sold as
  heard-in-your-voice is the transcript re-scored for sentiment.
- **Conversation lives in the LAYER, not the model** (Luis's call). Moshi is 200ms and cannot call
  a tool. `duet.py` proves two different rods converse through our layer at 0.958 fidelity.

---

## THE ARCHITECTURE

```
ear      whisper-base local, ~0.2-0.5s, adaptive noise floor
mind     aea/mind/tiers.py - reflex(llama-3.1-8b 0.456s) / voice(super-49b 0.366s) / depth(550b)
         SPECULATIVE PARALLEL DISPATCH: smart rod streams while fast rod decides on tools
mouth    edge-tts, sentence-chunked, barge-in 0.019s, 73 chained thinking sounds
hands    calc/read_state/list_tools/self_map local; web_search/web_fetch behind --online
prosody  measured every turn, NEVER given to the speaking rod, only NOTICES a change
```

---

## OPEN, ranked

1. **Renders take 2.76s for TWELVE characters** after any idle gap; 0.92s on the next call. NOT
   CPU contention - measured 0.5-0.8s alone, in a thread, and under whisper decoding flat out.
   The connection goes cold between turns. Per-chunk timing is now instrumented; the next live
   run should show whether it is one pathological render or many.
2. **Barge-in is built and never armed.** 0.019s at the audio layer, but nothing in the loop sets
   the stop event - the mic is closed while it speaks. Arming it means echo handling.
3. **One turn fell to the 550b and took 24.21s to first audio.** The ladder's latency budgets
   (reflex 6s, voice 9s, depth 12s) are ~20x the measured TTFB and do not bite.
4. **`converse` and `listen` are still orphaned by design.** Luis's decision: presence-triggered,
   not scheduled - detect he is at the machine (Windows last-input time, no sensor), offer, and
   open the mic only if he answers.
5. Tool self-IMPROVEMENT. It can list its tools; it cannot change them.
6. RAG over `design/` (3.4MB, 198 files) with a local embedder for the sensitive zone.

---

## THE NEXT RUN

`aea/io/blackbox.py` is built and **off by default**. Turn it on with
`python -m aea.io.blackbox --on`, and every turn stores the AUDIO beside the TRANSCRIPT plus the
signal stats, so the ear is judged from inside instead of inferred from its output.

Luis's framing, and it is the right one: *"like in Interstellar going into Gargantua - outside the
black hole you couldn't get the data, only once you are inside."* Every wrong conclusion about the
ear tonight came from having only one side of that boundary.

`python -m aea.io.blackbox` reports the ratio that settles it: if artifacts arrive at a much lower
peak than clean transcripts, the ear is STARVED and a bigger model buys nothing.

**Everything under `state/blackbox/` is gitignored. His voice never leaves the machine.**
