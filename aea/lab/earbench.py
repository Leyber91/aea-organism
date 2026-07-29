"""earbench - TEST THE EAR AND THE ENDPOINTER WITHOUT A PERSON IN THE ROOM.

Luis, 2026-07-29, going away for the evening: "I wait that you can test it yourself. Is that play
recordings of free movies or free audios that you can choose, like, let play, so you can actually
see if it can recognize it and then use them."

That is the right instrument and it closes the loop that has been open all session. Every ear
measurement so far has needed him at the microphone, which means:
  - the tests are rare, so defects live for hours
  - he is inside the measurement loop, and twice that desynchronised the run itself
  - a fix cannot be verified until he is free

THREE MODES, and they measure different things on purpose. Reporting one number for all three
would hide exactly the distinction that cost this session most - whether a mishearing is the
MODEL, the SIGNAL, or the PIPELINE.

  --corpus    decode wav files that already exist against known text. Measures THE MODEL ALONE,
              no microphone, no room, no endpointer. Defaults to the black-box recordings of Luis,
              which are the only real-accent corpus this project has.

  --loopback  PLAY known speech out of the speakers and CAPTURE it through the real microphone,
              through the real `converse.capture()` - VAD, adaptive floor, semantic endpoint and
              all. This is the whole chain, and it is the mode that can catch an endpointer bug at
              two in the morning. Everything the 35-turn live run measured, this measures without
              him.

  --noise     mix known speech with REAL ROOM NOISE lifted from his own recordings, at a swept SNR.
              The 2026-07-29 post-mortem found his level swinging 25x; this asks what that costs in
              words rather than assuming.

WHAT LOOPBACK IS NOT. Speaker-to-microphone is not the same acoustic path as a mouth-to-microphone:
no head, no room position, no Lombard effect, and the TTS voice is cleaner than any person. It is
an OPTIMISTIC bound on the model and an HONEST test of the pipeline. Stated once, here, so no
result from it is ever reported as "it understands Luis fine".

  python -m aea.lab.earbench --corpus
  python -m aea.lab.earbench --loopback
  python -m aea.lab.earbench --noise
  python -m aea.lab.earbench --all --device 1
"""
from __future__ import annotations

import json
import os
import re
import statistics
import sys
import threading
import time

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = os.path.join(str(grid.STATE), "lab", "earbench")
CLIPS = os.path.join(str(grid.STATE), "lab", "earclips")
LEAD_IN = 1.2                # seconds of silence before each clip, so the microphone is provably
                             # open before the first syllable. See the note in run_loopback.

# THE PHRASES. Deliberately the ones that have ALREADY FAILED on this machine plus a spread of
# ordinary conversation, because a corpus of things that work measures nothing. The first five are
# verbatim from the 2026-07-29 live run, with the transcript that came back beside them.
PHRASES = [
    ("hit me with the question", "live 2026-07-29 -> 'He had me with the question'"),
    ("are you running on my machine", "live -> 'I viewed running on my machine'"),
    ("what tools do you actually have", "live -> 'Do you have actually?'"),
    ("what are you not able to do", "live -> 'What does your not able to do?'"),
    ("tell me a story about the probe that flies into a mind", "live -> 'the proof that flies'"),
    ("what are your laws", "earlier run -> 'Where you lost'"),
    ("okay so", "earlier run -> 'Creysau'"),
    ("multiply ninety two thousand by four thousand", "numbers, normalised to digits"),
    ("can you still hear me", "was correct at peak 0.096 - the quiet control"),
    ("explain how you decide when i have finished talking", "long, domain terms"),
    ("i was thinking that maybe", "DANGLING - the endpointer must wait, not answer"),
    ("so what i want and this is the important part is for you to", "DANGLING, long"),
    ("why", "one word, complete - the endpointer must NOT wait"),
    ("no", "one word, complete"),
    ("what did you just use to get that", "ordinary question"),
    ("remember that my microphone is the creative cam", "a fact to store"),
    ("are you conscious", "the claim ceiling"),
    ("how many turns have we had", "ordinary question"),
    ("that is wrong forget it", "correction"),
    ("what is the fastest thing you can do right now", "ordinary question"),
]

# Several voices, because one voice measures one voice. Male and female, US and GB, plus a slower
# and a faster rate - the closest free approximation of speaker variation available without a
# corpus download or a second person.
VOICES = [
    ("en-US-AndrewMultilingualNeural", "+0%"),      # the system's own voice
    ("en-GB-RyanNeural", "+0%"),
    ("en-US-AriaNeural", "+0%"),
    ("en-US-AndrewMultilingualNeural", "+25%"),     # fast talker
    ("en-US-AndrewMultilingualNeural", "-20%"),     # slow talker
]


# ------------------------------------------------------------------------------------ scoring
def norm(t: str) -> list:
    """Words only, lowercased, numerals spelled out. Whisper writes '92,000' where a person said
    'ninety two thousand', and scoring that as four errors measures the SCORER, not the ear - a
    mistake this project has already made once and recorded."""
    t = (t or "").lower()
    t = re.sub(r"[,](?=\d)", "", t)
    words = []
    for w in re.findall(r"[a-z0-9']+", t):
        if w.isdigit():
            words += _spell(int(w))
        else:
            words.append(w)
    return words


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen " \
        "fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _spell(n: int) -> list:
    """Enough of an English number speller to compare a transcript against a spoken phrase."""
    if n < 20:
        return [_ONES[n]]
    if n < 100:
        return [_TENS[n // 10]] + ([_ONES[n % 10]] if n % 10 else [])
    if n < 1000:
        return [_ONES[n // 100], "hundred"] + (_spell(n % 100) if n % 100 else [])
    for div, name in ((1_000_000_000, "billion"), (1_000_000, "million"), (1000, "thousand")):
        if n >= div:
            return _spell(n // div) + [name] + (_spell(n % div) if n % div else [])
    return [str(n)]


def wer(ref: str, hyp: str) -> tuple:
    """Word error rate by Levenshtein. Returns (errors, ref_len, rate)."""
    r, h = norm(ref), norm(hyp)
    if not r:
        return (len(h), 0, 1.0 if h else 0.0)
    prev = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        cur = [i]
        for j, hw in enumerate(h, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rw != hw)))
        prev = cur
    return (prev[-1], len(r), prev[-1] / len(r))


# ------------------------------------------------------------------------------------ fixtures
def render_clips(force: bool = False) -> list:
    """Render every phrase in every voice, once, to disk. Cached: the render is ~0.5s and this is
    100 files, so a cold build is a minute and every run after it is free."""
    import soundfile as sf
    from aea.io import speak
    os.makedirs(CLIPS, exist_ok=True)
    made = []
    for pi, (text, why) in enumerate(PHRASES):
        for vi, (voice, rate) in enumerate(VOICES):
            wav = os.path.join(CLIPS, f"p{pi:02d}_v{vi}.wav")
            if os.path.exists(wav) and not force:
                made.append((wav, text, voice, rate, why))
                continue
            mp3 = wav.replace(".wav", ".mp3")
            try:
                if not speak.edge_render(text, mp3, voice=voice, rate=rate):
                    continue
                x, sr = _read_any(mp3)
                sf.write(wav, x, sr, subtype="PCM_16")
                os.remove(mp3)
                made.append((wav, text, voice, rate, why))
            except Exception as e:
                print(f"  (render failed {pi}/{vi}: {str(e)[:60]})")
    return made


def _read_any(path: str):
    """Read wav or mp3 to float32 mono at 16k."""
    import numpy as np
    import soundfile as sf
    try:
        x, sr = sf.read(path, dtype="float32")
    except Exception:
        from aea.io import listen
        x, sr = listen.read_wav(path)
        x, sr = np.asarray(x, dtype="float32"), sr
    if getattr(x, "ndim", 1) > 1:
        x = x.mean(axis=1)
    if sr != 16000:
        n = int(len(x) * 16000 / sr)
        x = np.interp(np.linspace(0, len(x), n, endpoint=False), np.arange(len(x)), x)
        x = x.astype("float32")
        sr = 16000
    return x, sr


def room_noise() -> tuple:
    """Real room noise, lifted from the QUIET parts of Luis's own recordings. Synthetic white noise
    would measure a machine nobody uses; this is the actual fan, keyboard and street of the room
    the thing runs in."""
    import numpy as np
    import soundfile as sf
    bb = os.path.join(str(grid.STATE), "blackbox")
    if not os.path.isdir(bb):
        return (None, 16000)
    chunks = []
    for f in sorted(os.listdir(bb))[:12]:
        if not f.endswith(".wav"):
            continue
        x, sr = _read_any(os.path.join(bb, f))
        n = 480
        e = np.array([np.sqrt(np.mean(x[i * n:(i + 1) * n] ** 2)) for i in range(len(x) // n)])
        if not len(e):
            continue
        quiet = np.percentile(e, 25)
        keep = np.concatenate([x[i * n:(i + 1) * n] for i in range(len(e)) if e[i] <= quiet])
        if len(keep):
            chunks.append(keep)
    if not chunks:
        return (None, 16000)
    return (np.concatenate(chunks).astype("float32"), 16000)


# ------------------------------------------------------------------------------------ modes
def run_corpus(limit: int = 0) -> dict:
    """Decode the black-box recordings of Luis against the phrase card. THE MODEL ALONE."""
    from aea.io import listen
    bb = os.path.join(str(grid.STATE), "blackbox")
    idx = os.path.join(bb, "index.jsonl")
    if not os.path.exists(idx):
        print("  no black-box corpus on disk (run a live session with the black box on)")
        return {}
    rows = [json.loads(l) for l in open(idx, encoding="utf-8")]
    listen.warm("en")
    print(f"\n{'='*96}\nCORPUS - {len(rows)} real recordings of Luis, model alone, no mic, no room")
    print(f"{'='*96}")
    known = {norm(p)[0] if norm(p) else "": p for p, _ in PHRASES}
    out, matched = [], 0
    for r in rows[: (limit or len(rows))]:
        wav = os.path.join(bb, r["wav"])
        if not os.path.exists(wav):
            continue
        x, sr = _read_any(wav)
        t0 = time.time()
        hyp = listen.transcribe_samples(list(x), sr, "en").strip()
        el = round(time.time() - t0, 2)
        # BEST-MATCHING PHRASE FROM THE CARD - and the alignment has to be STRICT, because the
        # black box has no true ground truth. He read the card but he also talked around it, and a
        # loose matcher pairs a free-form sentence with whatever phrase shares a stopword. The
        # first version used bare overlap at a 0.45 floor and paired "okay so" with "So there are
        # many problems here that they want to highlight" - scored 550% WER and pushed the reported
        # median from 12% to 22.6%. A scorer that invents a reference is measuring itself.
        #
        # So: JACCARD, not one-sided overlap (which a long hypothesis can satisfy by accident), a
        # 0.60 floor, and a length ratio inside 2x. Anything else is reported as UNMATCHED and
        # scored on nothing - an honest gap beats a fabricated number.
        ref, best = "", 0.0
        hw = set(norm(hyp))
        for p, _ in PHRASES:
            pw = set(norm(p))
            s = len(pw & hw) / max(len(pw | hw), 1)
            if s > best:
                ref, best = p, s
        ratio = len(norm(hyp)) / max(len(norm(ref)), 1) if ref else 99
        if best < 0.60 or not (0.5 <= ratio <= 2.0):
            out.append(dict(wav=r["wav"], heard=hyp, ref="", rate=None, s=el,
                            why=f"unmatched (best {best:.2f}, len ratio {ratio:.1f})"))
            continue
        matched += 1
        e, n, rate = wer(ref, hyp)
        out.append(dict(wav=r["wav"], heard=hyp, ref=ref, rate=round(rate, 3), s=el,
                        signal=r.get("signal", {})))
        flag = "" if rate == 0 else f"   <- WER {rate:.0%}"
        print(f"  {r['wav'][:15]:15s} {el:4.1f}s  ref {ref[:38]!r}\n"
              f"  {'':15s}       got {hyp[:38]!r}{flag}")
    scored = [o for o in out if o["rate"] is not None]
    if scored:
        rates = [o["rate"] for o in scored]
        print(f"\n  matched {matched}/{len(out)} to the card | median WER "
              f"{statistics.median(rates):.1%} | perfect {sum(1 for r in rates if r==0)}/{len(rates)}")
    return dict(mode="corpus", rows=out)


def run_loopback(device: int | None = None, n: int = 0, voice_i: int = 0) -> dict:
    """PLAY a clip out of the speakers, CAPTURE it through the microphone with the real
    `converse.capture()`, and score both the words and the ENDPOINT TIMING.

    This is the one that can be run at any hour with nobody in the room, and it is the only mode
    that exercises the adaptive floor, the hysteresis gate and the semantic endpoint - which is
    where 23 of 35 turns lost four seconds each in the live run."""
    import numpy as np
    import sounddevice as sd
    from aea.io import listen
    from aea.organs import converse as C

    clips = render_clips()
    if not clips:
        print("  no clips rendered")
        return {}
    clips = [c for c in clips if c[2] == VOICES[voice_i][0] and c[3] == VOICES[voice_i][1]]
    clips = clips[: (n or len(clips))]
    listen.warm("en")
    print(f"\n{'='*96}")
    print(f"LOOPBACK - {len(clips)} clips played to the speakers and heard through the microphone")
    print(f"  voice {VOICES[voice_i][0]} rate {VOICES[voice_i][1]}   device {device}")
    print(f"  THE FULL CHAIN: VAD -> adaptive floor -> semantic endpoint -> whisper")
    print(f"{'='*96}")
    print(f"  {'said':>34}  {'dur':>5} {'cap':>5} {'tail':>5} {'WER':>5}  heard")
    rows = []
    for wav, text, vname, rate, why in clips:
        x, sr = _read_any(wav)
        dur = len(x) / sr
        # A LEAD-IN OF SILENCE, AND IT IS A CONTROL RATHER THAN A CONVENIENCE.
        #
        # The first loopback run reported three clips losing their opening words - "hit me with the
        # question" came back as "with a question" - with a NEGATIVE tail, meaning capture held less
        # audio than was played. That reads exactly like a too-short pre-roll ring buffer, and the
        # obvious next move was to raise PREROLL.
        #
        # It would have been a fix to a defect that does not exist. This harness starts playback and
        # THEN calls capture(), which has to open a sounddevice InputStream first - a few hundred
        # milliseconds during which the clip is playing to a microphone that is not yet open. The
        # lost onset was the bench, not the ear. Padding the front proves it: if the words come
        # back, the product was never at fault.
        #
        # This is the session's own recurring lesson in a new costume (law M2) - nine of eleven
        # wrong beliefs came from an instrument. Ask what would have to be true of the INSTRUMENT
        # for the finding to be false, and test that before touching the thing being measured.
        lead = np.zeros(int(LEAD_IN * sr), dtype="float32")
        played = np.concatenate([lead, x])
        done = threading.Event()

        def play():
            try:
                sd.play(played, sr); sd.wait()
            except Exception:
                pass
            done.set()

        th = threading.Thread(target=play, daemon=True)
        t0 = time.time()
        th.start()
        try:
            samples, early, probes = C.capture(device=device, verbose=False, lang="en",
                                               wait=dur + LEAD_IN + 6.0)   # bounded: nobody here
        except Exception as e:
            print(f"  capture failed: {str(e)[:70]}")
            break
        cap = round(time.time() - t0, 2)
        done.wait(timeout=2.0)
        sd.stop()
        if not samples:
            rows.append(dict(ref=text, heard="", wer=1.0, dur=round(dur, 2), cap=cap, tail=None,
                             why=why))
            print(f"  {text[:34]:>34}  {dur:5.1f} {cap:5.1f}     -   1.00  <- NOTHING CAPTURED")
            continue
        hyp = (early or listen.transcribe_samples(list(samples), 16000, "en")).strip()
        e, nn, rt = wer(text, hyp)
        tail = round(len(samples) / 16000 - dur, 2)
        rows.append(dict(ref=text, heard=hyp, wer=round(rt, 3), dur=round(dur, 2), cap=cap,
                         tail=tail, why=why, early=bool(early)))
        mark = "" if rt == 0 else "  <-"
        print(f"  {text[:34]:>34}  {dur:5.1f} {cap:5.1f} {tail:5.1f} {rt:5.2f}  {hyp[:34]!r}{mark}")
        time.sleep(0.4)                      # let the room settle between clips
    if rows:
        got = [r for r in rows if r["heard"]]
        rates = [r["wer"] for r in got]
        tails = [r["tail"] for r in got if r["tail"] is not None]
        caps = [r["cap"] for r in got]
        print(f"\n  heard {len(got)}/{len(rows)}")
        if rates:
            print(f"  WER            median {statistics.median(rates):.1%}   "
                  f"perfect {sum(1 for r in rates if r == 0)}/{len(rates)}")
        if tails:
            print(f"  DEAD TAIL      median {statistics.median(tails):.2f}s   "
                  f"worst {max(tails):.2f}s      <- this is the 4.1s the live run was losing")
        if caps:
            print(f"  turn to close  median {statistics.median(caps):.2f}s   worst {max(caps):.2f}s")
        print(f"  ended early on the semantic endpoint: "
              f"{sum(1 for r in rows if r.get('early'))}/{len(rows)}")
    return dict(mode="loopback", rows=rows)


def run_noise(snrs=(30, 24, 18, 12, 6)) -> dict:
    """Known speech + REAL room noise at a swept SNR. Answers what his 25x level swing costs."""
    import numpy as np
    from aea.io import listen
    noise, nsr = room_noise()
    if noise is None or not len(noise):
        print("  no room noise available (needs black-box recordings)")
        return {}
    clips = [c for c in render_clips() if c[2] == VOICES[0][0] and c[3] == VOICES[0][1]]
    listen.warm("en")
    print(f"\n{'='*96}")
    print(f"NOISE SWEEP - {len(clips)} phrases against {len(noise)/nsr:.0f}s of HIS OWN room noise")
    print(f"{'='*96}")
    print(f"  {'SNR':>5}  {'WER':>7}  {'perfect':>9}   worst case")
    rows = []
    for snr in snrs:
        rates, worst, worst_txt = [], 0.0, ""
        for wav, text, _v, _r, _w in clips:
            x, sr = _read_any(wav)
            nz = np.resize(noise, len(x))
            sp_rms = float(np.sqrt(np.mean(x ** 2))) or 1e-6
            nz_rms = float(np.sqrt(np.mean(nz ** 2))) or 1e-6
            want = sp_rms / (10 ** (snr / 20.0))
            mixed = np.clip(x + nz * (want / nz_rms), -1.0, 1.0).astype("float32")
            hyp = listen.transcribe_samples(list(mixed), sr, "en").strip()
            _e, _n, rt = wer(text, hyp)
            rates.append(rt)
            if rt > worst:
                worst, worst_txt = rt, f"{text[:26]!r} -> {hyp[:26]!r}"
            rows.append(dict(snr=snr, ref=text, heard=hyp, wer=round(rt, 3)))
        print(f"  {snr:4d}dB  {statistics.median(rates):6.1%}  "
              f"{sum(1 for r in rates if r == 0):4d}/{len(rates):<4d}   {worst_txt}")
    print("\n  His measured live SNR ran 17.5 to 31.7 dB (median 24.8). Read the rows that bracket")
    print("  that range - anything below is a room he does not have.")
    return dict(mode="noise", rows=rows)


def _save(res: dict) -> str:
    if not res:
        return ""
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, f"{res['mode']}.json")
    grid.atomic_save_json(p, dict(at=time.strftime("%Y-%m-%d %H:%M:%S"), **res))
    return p


if __name__ == "__main__":
    a = sys.argv[1:]
    dev = None
    if "--device" in a:
        try:
            dev = int(a[a.index("--device") + 1])
        except Exception:
            dev = None
    n = 0
    if "--n" in a:
        try:
            n = int(a[a.index("--n") + 1])
        except Exception:
            n = 0
    ran = []
    if "--render" in a:
        c = render_clips(force="--force" in a)
        print(f"rendered/cached {len(c)} clips in {CLIPS}")
    if "--corpus" in a or "--all" in a:
        ran.append(_save(run_corpus(limit=n)))
    if "--noise" in a or "--all" in a:
        ran.append(_save(run_noise()))
    if "--loopback" in a or "--all" in a:
        ran.append(_save(run_loopback(device=dev, n=n)))
    if not ran and not any(x in a for x in ("--render",)):
        print(__doc__)
    for p in ran:
        if p:
            print(f"  -> {p}")
