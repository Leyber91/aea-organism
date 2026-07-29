"""speak.py - the entity's VOICE. Three engines, one interface, privacy-zoned (2026-07-19):

  EDGE (default for normal speech): Microsoft neural voices via the edge-tts pip package -
     genuinely natural (AndrewMultilingual), free, no key, server-side. CLOUD: the text goes to
     Microsoft, so it is BLOCKED for sensitive-zone speech (cloud_ok=False) - same law as the
     browser voice. Normal replies already transited hosted no-train rods, so the exposure class
     is unchanged.
  KOKORO: Kokoro-82M local quality voice. The sherpa-onnx path is EDR-dead; the TORCH path on
     Fooocus's python is PROVEN (voice_test_kokoro.wav, rtf 0.39 warm) - wiring it as the
     sensitive-mode natural voice is ticket G3's remaining step.
  SAPI (floor + the FAST option): Windows built-in System.Speech - robotic but INSTANT and
     unkillable. Forced with voice="sapi"; the terminal fallback for everything.

  python speak.py "text"                      # say it (kokoro if installed, else sapi)
  python speak.py --fast "text"               # force the instant sapi engine
  python speak.py --brief                     # read today's brief aloud
  python speak.py --voices                    # list voices (kokoro speakers + sapi)
  python speak.py --sid 3 "text"              # pick a kokoro speaker
  python speak.py --narrate script.txt out/   # RECORD a presentation: one wav per paragraph + playlist
Stdlib only: subprocess to the sherpa exe / PowerShell. Voice choice lives in identity.json:
  "voice": "kokoro:3"  (engine:speaker)  or  "Microsoft David Desktop" (sapi name).
"""
from __future__ import annotations
import subprocess, sys, os, json, time, re

from aea.kernel import grid
HERE = os.path.dirname(os.path.abspath(__file__))
IDENTITY = os.path.join(grid.STATE, "identity.json")
VDIR = os.path.join(grid.ROOT, "voice")
KOKORO = os.path.join(VDIR, "kokoro-en-v0_19")
SPEAKERS = ["af", "af_bella", "af_nicole", "af_sarah", "af_sky",
            "am_adam", "am_michael", "bf_emma", "bf_isabella", "bm_george", "bm_lewis"]
DEFAULT_SID = 3          # af_sarah - warm, clear US female; change via identity.json "voice": "kokoro:N"

# Engine note (2026-07-11): the sherpa-onnx standalone EXE is blocked by AppLocker on this
# corporate machine, so Kokoro runs through the sherpa-onnx PYTHON wheel instead - python.exe
# carries the trust, the extension DLLs ride along. Same model, same local privacy.
_tts = None              # lazy singleton: pay the ~2-5s model load once per process


def _identity() -> dict:
    try:
        return json.load(open(IDENTITY, encoding="utf-8"))
    except Exception:
        return {}


def kokoro_available() -> bool:
    if not os.path.exists(os.path.join(KOKORO, "model.onnx")):
        return False
    try:
        import sherpa_onnx  # noqa: F401
        return True
    except ImportError:
        return False


def _engine():
    global _tts
    if _tts is None:
        import sherpa_onnx
        cfg = sherpa_onnx.OfflineTtsConfig(
            model=sherpa_onnx.OfflineTtsModelConfig(
                kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
                    model=os.path.join(KOKORO, "model.onnx"),
                    voices=os.path.join(KOKORO, "voices.bin"),
                    tokens=os.path.join(KOKORO, "tokens.txt"),
                    data_dir=os.path.join(KOKORO, "espeak-ng-data")),
                num_threads=4))
        _tts = sherpa_onnx.OfflineTts(cfg)
    return _tts


# ------------------------------------------------------------------ KOKORO: human voice + files
def kokoro_render(text: str, out_wav: str, sid: int = DEFAULT_SID, speed: float = 1.0,
                  timeout: int = 600) -> dict:
    """Render text to a wav. Returns dict(ok, seconds_audio, seconds_gen, rtf)."""
    if not text.strip():
        return dict(ok=False, error="empty text")
    t0 = time.time()
    try:
        audio = _engine().generate(text, sid=int(sid), speed=speed)
        import wave, struct
        samples = audio.samples                       # floats in [-1, 1]
        with wave.open(out_wav, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(audio.sample_rate)
            w.writeframes(struct.pack(f"<{len(samples)}h",
                          *(max(-32768, min(32767, int(s * 32767))) for s in samples)))
        gen = round(time.time() - t0, 1)
        dur = round(len(samples) / audio.sample_rate, 1)
        return dict(ok=True, seconds_audio=dur, seconds_gen=gen,
                    rtf=round(gen / dur, 2) if dur else None, path=out_wav)
    except Exception as e:
        return dict(ok=False, error=str(e)[:160])


def play_wav(path: str, timeout: int = 600) -> bool:
    ps = f"(New-Object Media.SoundPlayer '{path}').PlaySync()"
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0
    except Exception:
        return False


# ------------------------------------------------------------------ EDGE: natural neural voice (cloud)
EDGE_VOICE = "en-US-AndrewMultilingualNeural"     # the 2024 conversation-optimized tier

def edge_available() -> bool:
    try:
        import edge_tts  # noqa: F401
        return True
    except ImportError:
        return False


def edge_render(text: str, mp3: str, voice: str | None = None, timeout: int = 300,
                rate: str = "", pitch: str = "") -> bool:
    """Render text to an mp3. IN-PROCESS first - MEASURED 1.56s vs 6.15s for the subprocess path,
    which pays a fresh python startup on every single call. Subprocess stays as the fallback.

    `rate` is an edge-tts speed offset like "+25%" or "-20%", empty for normal. Added 2026-07-29
    for `lab/earbench`, which needs a FAST and a SLOW talker to test the endpointer against speaker
    variation - with one speaking rate the bench measures one speaking rate.

    `pitch` is an offset like "+40Hz" or "-35Hz". Added for the multi-speaker party: when four
    voices overlap, a listener can only follow them if they are SEPARABLE, and pitch separation is
    one of the few cues that survives being summed into one mono-ish bus alongside stereo position.
    A cartoon voice and a monster voice are not decoration here - they are the thing that makes
    overlapping speech legible rather than mush."""
    v = voice or EDGE_VOICE
    kw = {}
    if rate:
        kw["rate"] = rate
    if pitch:
        kw["pitch"] = pitch
    try:
        import asyncio, edge_tts
        asyncio.run(edge_tts.Communicate(text[:1200], v, **kw).save(mp3))
        if os.path.exists(mp3) and os.path.getsize(mp3) >= 400:
            return True
    except Exception:
        pass                                      # a running loop / network blip -> subprocess
    try:
        cmd = [sys.executable, "-m", "edge_tts", "--voice", v,
               "--text", text[:1200], "--write-media", mp3]
        if rate:
            cmd += ["--rate", rate]
        if pitch:
            cmd += ["--pitch", pitch]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) >= 400
    except Exception:
        return False


def play_fast(path: str) -> bool:
    """Decode + play IN-PROCESS (soundfile -> sounddevice). MEASURED: the PowerShell MediaPlayer
    below costs 5-10s per call for an assembly load + process spawn - it turned 7.5s of speech
    into an 18s wait. This path costs ~0.1s. Blocks until the audio ends (half-duplex)."""
    try:
        import soundfile as sf, sounddevice as sd
        data, sr = sf.read(path, dtype="float32")
        sd.play(data, sr)
        sd.wait()
        return True
    except Exception:
        return False


def play_mp3(path: str, timeout: int = 300) -> bool:
    """Play an mp3 and BLOCK until it finishes (the half-duplex guarantee: callers rely on this
    returning only once the room is quiet again). Fast in-process path first, WPF as fallback."""
    # THERE IS NOTHING TO PLAY, SO DO NOT SPEND NINE SECONDS DISCOVERING THAT. MEASURED
    # 2026-07-29: a failed render left no file, `play_fast` failed on the missing path, and the WPF
    # fallback below then sat in its own 8-second `NaturalDuration` wait for audio that was never
    # going to exist - nine seconds of dead silence in the middle of a conversation, on the exact
    # turn that had already gone wrong. A fallback is for a DIFFERENT way to do the job, never for
    # a job that cannot be done.
    if not path or not os.path.exists(path) or os.path.getsize(path) < 400:
        return False
    if play_fast(path):
        return True
    ps = ("Add-Type -AssemblyName presentationCore; "
          f"$p = New-Object System.Windows.Media.MediaPlayer; $p.Open([uri]'{path}'); $p.Play(); "
          "$t0 = Get-Date; while (-not $p.NaturalDuration.HasTimeSpan -and "
          "((Get-Date) - $t0).TotalSeconds -lt 8) { Start-Sleep -Milliseconds 100 }; "
          "if ($p.NaturalDuration.HasTimeSpan) { "
          "Start-Sleep -Milliseconds ([int]$p.NaturalDuration.TimeSpan.TotalMilliseconds + 300) }; "
          "$p.Close()")
    try:
        p = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode == 0
    except Exception:
        return False


# ------------------------------------------------------------------ STREAMED SPEECH (2026-07-29)
# MEASURED, and the measurement is why this exists. edge-tts render is ~0.5s FLAT regardless of
# length - 3 chars costs 0.51s and 367 chars costs 0.75s, because it is one network round trip.
# The number that was being read as "voice is slow" was the PLAY field of the receipt, which is
# the audio's own duration: a 367-char reply is 24.4s of speech. The entity was not slow at
# talking. It was saying too much, and could not be stopped once it started.
#
# So the fix is not a faster engine (none is: local Kokoro measured rtf 0.25-0.31 against edge's
# 0.079, and speaks Castilian with an English accent). The fix is to cut the reply into sentences,
# start playing the first one while the rest is still rendering, and make every sentence boundary
# a point where a person can interrupt.
_SENT_END = re.compile(r"[.!?…](?=\s|$)|[\n]+")
_CALL = [0]               # monotonic per-process, so an abandoned producer thread (barge-in no
                          # longer joins one) cannot overwrite a file a LATER turn is playing
_MIN_CHUNK = 8            # shorter than this is a fragment; keep accumulating rather than pay a
                          # round trip to say "Si." on its own line


def split_sentences(text: str) -> list[str]:
    """Cut on sentence ends, keeping the punctuation. Fragments below _MIN_CHUNK are glued to the
    next piece so the pipeline never spends a whole round trip on two characters."""
    out, buf = [], ""
    for part in re.split(r"(?<=[.!?…])\s+|\n+", text):
        part = part.strip()
        if not part:
            continue
        buf = (buf + " " + part).strip() if buf else part
        if len(buf) >= _MIN_CHUNK:
            out.append(buf); buf = ""
    if buf:
        if out:
            out[-1] = out[-1] + " " + buf
        else:
            out.append(buf)
    return out


def say_stream(pieces, voice: str | None = None, stop=None, mute: bool = False,
               on_chunk=None, filler: str = "", filler_n: int = 0,
               filler_text: str = "") -> dict:
    """Speak an ITERATOR OF TEXT DELTAS while it is still being produced.

    `pieces` may be a plain string, a list, or a generator (grid.stream_openai's deltas). Text is
    assembled into sentences; a background thread renders sentence N+1 while sentence N is playing,
    so time-to-first-audio is ONE render (~0.5s) instead of the whole reply, and stays there no
    matter how long the reply turns out to be.

    `stop` is a threading.Event. When it is set the speech halts - immediately inside the current
    sentence, not merely at the next one - which is what makes barge-in possible. A half-duplex
    guarantee that cannot be broken by the person speaking is not politeness, it is a system that
    talks over him.

    Returns a RECEIPT: ok, ttfa (the number that decides whether this feels like a conversation),
    chunks, spoken, render_s, play_s, engine, interrupted. Never a bare bool - a silent failure
    must not be able to masquerade as a spoken reply (the same rule as `converse.say`).
    """
    import queue, threading
    v = voice or EDGE_VOICE
    rec = dict(ok=False, ttfa=None, chunks=0, spoken="", render_s=0.0, play_s=0.0,
               engine=v, interrupted=False, error=None, filler_s=0.0)
    if isinstance(pieces, str):
        pieces = [pieces]
    if mute:
        # MUTE MEANS MAKE NO SOUND, NOT DO NO WORK. Returning here without consuming `pieces` left
        # the generator untouched, so the mind never ran and the tools never fired - and the caller
        # reported "rod failed" for a rod that was never asked. A verification path that silently
        # skips the thing being verified is worse than no verification (found 2026-07-29 the first
        # time --mute was used on the tiered turn).
        text = "".join(p for p in pieces)
        rec.update(ok=bool(text.strip()), engine="muted", spoken=text.strip(),
                   chunks=1 if text.strip() else 0, ttfa=None)
        return rec
    stop = stop or threading.Event()
    q: "queue.Queue" = queue.Queue(maxsize=4)
    _CALL[0] += 1
    call = _CALL[0]
    t_start = time.time()

    def produce():
        """Assemble deltas into sentences and render each one ahead of the player."""
        buf, idx = "", 0
        try:
            for piece in pieces:
                if stop.is_set():
                    break
                buf += piece
                while True:                       # a delta can complete more than one sentence
                    m = _SENT_END.search(buf)
                    if not m:
                        break
                    head, tail = buf[:m.end()].strip(), buf[m.end():]
                    if len(head) < _MIN_CHUNK:
                        break                     # too short to be worth a round trip; let it grow
                    buf = tail
                    idx += 1
                    q.put(_render_chunk(head, v, idx, call))
            if buf.strip() and not stop.is_set():
                idx += 1
                q.put(_render_chunk(buf.strip(), v, idx, call))
        except Exception as e:                    # a dead producer must not hang the player forever
            q.put(dict(error=str(e)[:160], text="", path=None, render=0.0))
        finally:
            q.put(None)                           # the sentinel is in `finally` so it is ALWAYS sent

    th = threading.Thread(target=produce, daemon=True)
    th.start()
    fills = 0
    while True:
        if rec["chunks"] == 0 and filler and not stop.is_set():
            # THE THINKING SOUNDS COVER THE WHOLE WAIT, NOT THE START OF IT.
            #
            # Luis, after the first live run: "it doesn't do the mmm, uhm while thinking, it does
            # it 1 second, not until it gets the reply." He is right, and the old behaviour was
            # worse than nothing: one 0.4s "hmm" followed by four to eight more seconds of dead
            # silence MARKS the gap instead of filling it, drawing attention to the exact thing it
            # was meant to cover.
            #
            # People chain them - "hmm... let me think... okay so" - so this keeps emitting while
            # the answer is still being written, varying the sound each time (choose_filler will
            # not repeat inside its window) and leaving FILLER_GAP of quiet between so it reads as
            # thinking rather than stuttering.
            #
            # THE HONESTY LINE IS UNCHANGED, and it is what bounds the loop: a sound may only play
            # while the mind is STILL WORKING. The moment a chunk is ready the loop exits and the
            # real answer plays. Nothing is ever emitted over a finished thought. MAX_FILLS stops
            # it babbling forever if a rod has silently died.
            try:
                item = q.get(timeout=(FILLER_AFTER if fills == 0 else FILLER_GAP))
            except Exception:
                if fills >= MAX_FILLS:
                    item = q.get()          # something is wrong; wait it out in silence
                else:
                    rec["filler_s"] = round(
                        rec.get("filler_s", 0.0)
                        + maybe_filler(filler, filler_n + fills, stop, said=filler_text,
                                       log=rec.setdefault("fillers", [])), 3)
                    fills += 1
                    rec["fills"] = fills
                    continue
        else:
            item = q.get()
        if item is None:
            break
        rec["render_s"] += item.get("render", 0.0)
        rec.setdefault("renders", []).append(round(item.get("render", 0.0), 2))
        if item.get("error"):
            rec["error"] = item["error"]
            continue
        if stop.is_set():
            rec["interrupted"] = True
            break
        if item.get("path"):
            if rec["ttfa"] is None:
                rec["ttfa"] = round(time.time() - t_start, 2)
            t1 = time.time()
            _play_interruptible(item["path"], stop)
            rec["play_s"] += time.time() - t1
            rec["chunks"] += 1
            rec["spoken"] = (rec["spoken"] + " " + item["text"]).strip()
            if on_chunk:
                try:
                    on_chunk(item["text"])
                except Exception:
                    pass
            if stop.is_set():
                rec["interrupted"] = True
                break
    if rec["interrupted"]:
        # RETURN THE FLOOR IMMEDIATELY. Two rounds of measurement on this:
        #   round 1  the producer sat on a full queue and `join` waited it out -> 2.3s late
        #   round 2  queue drained and join cut to 0.5s -> still 0.829s late (convbench axis 5)
        # The remaining cost was the join itself: the producer can be INSIDE edge_render, a ~0.5s
        # network call it cannot abandon, so any join at all pays for it. There is nothing to wait
        # for - the audio device is already stopped and the thread is a daemon that checks `stop`
        # before it renders again. Waiting for it only keeps the microphone shut while the person
        # is already speaking, which is the exact failure being fixed.
        stop.set()
        try:
            while True:
                q.get_nowait()
        except Exception:
            pass
    else:
        th.join(timeout=0.5)                      # clean end: let the producer close its own file
    rec["render_s"] = round(rec["render_s"], 2)
    rec["play_s"] = round(rec["play_s"], 2)
    rec["ok"] = rec["chunks"] > 0
    return rec


# ---------------------------------------------------------------- THINKING SOUNDS (2026-07-29)
# Luis: "fill the gaps of thinking as the conversation progresses, like those human sounds -
# hmm, mmmm, let me think about it - making it more human."
#
# THE MEASUREMENT THAT MAKES THIS THE BIGGEST REMAINING WIN. Silence after the person stops
# talking is 2.16s (endpointer 0.45 + ear 0.25 + mind 0.60 + mouth 0.86). Human conversation runs
# on a ~200ms gap, and past 1s people talk over the agent. We cannot make the mind faster. We CAN
# stop the gap being silent, which is what people do: a filled pause holds the floor, signals "I
# have the turn and I am working", and measurably reduces the perceived wait.
#
# THEY MUST BE PRE-RENDERED. Synthesising one costs ~0.5s, which is the very thing being covered.
# Rendered once at boot and cached on disk, playback is ~50ms - so the first sound arrives at
# roughly 0.4s instead of 2.16s, with no faster rod and no GPU.
#
# THE HONESTY LINE, AND IT DECIDES WHEN THEY MAY FIRE. A filler played while the mind is genuinely
# still generating is a TRUE signal of a true state - a receipt, like every other number here. One
# played after the answer is already in hand is theatre: a performance of deliberation that did not
# happen, which is exactly the interiority the claim ceiling forbids this system from asserting.
# So it fires ONLY on a real wait, at most once per turn, and never once audio is ready.
# GROUPED BY WHAT IS ACTUALLY TRUE AT THAT MOMENT, not by variety for its own sake. Six sounds on
# rotation becomes a tic inside a minute; and worse, a sound borrowed from the wrong state is a
# small lie - "checking" while nothing is being checked is the same defect as a fabricated number,
# just shorter. So the caller names the STATE and only sounds true of that state can play.
#
#   ack    they just told us something and it landed. A receipt, not a claim.
#   think  a question is being worked on right now by a rod that has not returned.
#   tool   a real tool call is in flight - this is the only group allowed to say "checking".
#   short  a sub-second gap where anything with words would be too much.
THINKING_SOUNDS = {
    "ack":   ("Mm.", "Mhm.", "Right.", "I see.", "Okay.", "Got it.", "Yeah.", "Sure.",
              "Ah, okay.", "Right, yeah."),
    "think": ("Hmm.", "Hmm, let me think.", "Let me think about that.", "Good question.",
              "Hmm, let's see.", "Give me a second.", "Let me get that right.",
              "Hm, okay.", "Let's see."),
    "tool":  ("One sec, checking.", "Let me look.", "Checking now.", "Hold on, looking.",
              "Give me a moment.", "Pulling that up."),
    "short": ("Hmm.", "Mm.", "Ah.", "Mhm.", "Hm."),
}
FILLER_AFTER = 0.45       # only if the real answer has not arrived by here. Under this the gap is
                          # inside the band a person does not consciously notice, and filling it
                          # would add a tic to a turn that was already fast enough.
FILLER_GAP = 1.30         # quiet between chained sounds. Long enough to read as thinking rather
                          # than stuttering, short enough that the silence never reasserts itself.
MAX_FILLS = 5             # ~9s of covered wait. Past that something has gone wrong and babbling
                          # at a person is worse than an honest silence.
_FILLERS: dict = {}


def grow_fillers(n_per_kind: int = 14, voice: str | None = None, verbose: bool = True) -> int:
    """GENERATE more thinking sounds with a small rod, then render and cache them. Run OFFLINE.

    Luis: "shouldn't we get a very small model to give us different examples... because at the end
    we don't want to have the same relative answer." He is right that a hand-typed tuple is a
    finite personality, and a listener clocks a fixed set fast.

    THE CONSTRAINT THAT SHAPES THE SOLUTION: a filler cannot be generated at speaking time. The
    render alone is ~0.5s, which is the whole gap it exists to cover, and a model call on top makes
    it worse than silence. So generation happens HERE, offline, once - a small rod writes the
    variations, they are rendered to disk, and at conversation time the pool is just bigger. Model
    variety, zero runtime cost.

    It never replaces the hand-written set, only extends it: those were chosen to be TRUE of a
    specific state, and a generated line that quietly promises something ("I'll look that up") in
    the THINKING group would be a fabricated status. Anything long, questioning, or containing a
    verb of action is dropped rather than trusted.
    """
    from aea.kernel import grid as _grid
    from aea.mind import tiers as _tiers
    o = _tiers.organ("reflex")
    v = voice or EDGE_VOICE
    tag = re.sub(r"[^a-zA-Z0-9]+", "", v)[-18:]
    d = os.path.join(_grid.STATE, "fillers", tag)
    os.makedirs(d, exist_ok=True)
    ASK = {
        "ack": "brief acknowledgements a listener makes to show they heard, like 'Mm.' or 'Right.'",
        "think": "short things someone says while still thinking, like 'Hmm, let me think.'",
        "tool": "short things someone says while actually looking something up right now",
        "short": "very short hesitation noises, one or two syllables, like 'Hmm.' or 'Ah.'",
    }
    added = 0
    for kind, desc in ASK.items():
        have = list(THINKING_SOUNDS.get(kind, ()))
        prompt = (f"List {n_per_kind} DIFFERENT English {desc}\n"
                  f"Rules: each on its own line, no numbering, no quotes, MAX 5 words, natural "
                  f"spoken English, no emoji. They will be spoken aloud by a machine that must not "
                  f"promise anything it is not doing. Do not repeat any of these:\n"
                  + "\n".join(have))
        r = _grid.call_openai(o["plant"], o["model"], [{"role": "user", "content": prompt}],
                              max_tokens=220, temperature=1.0, timeout=o["budget"])
        if not r.get("ok"):
            if verbose:
                print(f"  {kind}: rod failed ({str(r.get('error'))[:50]})")
            continue
        seen = {s.lower().strip(" .!") for s in have}
        fresh = []
        for line in (r.get("text") or "").splitlines():
            s = re.sub(r"^[\s\-\*\d\.\)]+", "", line).strip().strip('"')
            low = s.lower().strip(" .!")
            if (not s or len(s) > 34 or len(s.split()) > 5 or low in seen
                    or s.endswith("?") or re.search(r"\b(i'?ll|i am going|let me get|checking on|"
                                                    r"searching|i will)\b", low)):
                continue                       # a promise is not a filler
            seen.add(low)
            fresh.append(s if s[-1] in ".!" else s + ".")
        base = len(THINKING_SOUNDS.get(kind, ()))
        for i, s in enumerate(fresh):
            p = os.path.join(d, f"{kind}_{base + i}.mp3")
            if edge_render(s, p, voice=v) and _trim_silence(p):
                added += 1
        if verbose:
            print(f"  {kind}: +{len(fresh)} generated  {fresh[:4]}")
    _FILLERS.clear()                           # force a re-scan so the new files are picked up
    prime_fillers(v)
    return added


def prime_fillers(voice: str | None = None) -> int:
    """Render every thinking sound ONCE and cache it to disk. Returns how many are ready.

    Called at boot beside `warm()`. Cached across runs, so this costs ~15s the first time on a
    given voice and nothing afterwards. If it has NOT run, `maybe_filler` does nothing rather than
    rendering on demand - paying 0.5s to cover a 0.5s gap is worse than the silence it replaces."""
    global _FILLERS
    if _FILLERS:
        return sum(len(v) for v in _FILLERS.values())
    v = voice or EDGE_VOICE
    tag = re.sub(r"[^a-zA-Z0-9]+", "", v)[-18:]
    d = os.path.join(grid.STATE, "fillers", tag)
    os.makedirs(d, exist_ok=True)
    import glob as _glob
    out: dict = {}
    for kind, sounds in THINKING_SOUNDS.items():
        got = []
        for i, s in enumerate(sounds):
            p = os.path.join(d, f"{kind}_{i}.mp3")
            if os.path.exists(p) and os.path.getsize(p) > 400:
                got.append(p); continue
            if edge_render(s, p, voice=v) and _trim_silence(p):
                got.append(p)
        # PICK UP ANYTHING `grow_fillers` LEFT ON DISK. The hand-written tuple is the floor, not
        # the whole pool - building the paths only from that tuple meant every generated sound was
        # rendered, cached, and then never played, which is the quietest kind of dead code.
        for p in sorted(_glob.glob(os.path.join(d, f"{kind}_*.mp3"))):
            if p not in got and os.path.getsize(p) > 400:
                got.append(p)
        out[kind] = got
    _FILLERS = out
    return sum(len(x) for x in out.values())


def _trim_silence(path: str, pad: float = 0.06) -> bool:
    """Cut the leading and trailing silence off a cached filler, in place.

    MEASURED 2026-07-29: edge-tts pads short utterances heavily - "Mm." rendered as 1.78 SECONDS,
    almost all of it silence, and "One sec, checking." as 2.66s. A filler longer than the gap it
    covers does not fill the gap, it BECOMES the gap and delays the real answer. This is the whole
    reason the sounds are cached rather than used as rendered."""
    try:
        import numpy as np
        import soundfile as sf
        data, sr = sf.read(path, dtype="float32")
        if data.ndim > 1:
            data = data.mean(axis=1)
        if data.size == 0:
            return False
        thr = max(float(np.abs(data).max()) * 0.02, 1e-4)
        loud = np.where(np.abs(data) > thr)[0]
        if loud.size == 0:
            return False
        a = max(0, loud[0] - int(pad * sr))
        b = min(len(data), loud[-1] + int(pad * sr))
        sf.write(path.replace(".mp3", ".wav"), data[a:b], sr, subtype="PCM_16")
        return True
    except Exception:
        return False


_RECENT: list = []        # the last few fillers played, so none repeats inside a short window
_NOREPEAT = 4


def choose_filler(kind: str, said: str = "") -> str:
    """Pick a cached sound FROM THE SHAPE OF WHAT THEY JUST SAID, and never one used recently.

    Luis, 2026-07-29: "they need to be in context of the conversation as well. If not, people will
    notice a pattern." Correct on both counts, and the second is the binding constraint: generating
    a filler per turn would cost a ~0.5s render, which is the very gap it exists to cover. So the
    context-sensitivity has to be FREE, which means selecting rather than generating.

    Two mechanisms, both deterministic:
      SHAPE   a question gets a thinking sound, a statement about themselves gets an
              acknowledgement, a long multi-clause question gets one that buys more time. That is
              genuine responsiveness to the turn, not decoration.
      MEMORY  nothing repeats within the last few played. A listener clocks a REPEAT far faster
              than they clock a small vocabulary, so the no-repeat window does more work than the
              raw count does.
    """
    t = (said or "").strip()
    low = t.lower()
    if kind not in ("tool",):
        is_q = t.endswith("?") or bool(re.match(
            r"^(what|how|why|when|where|who|which|can|could|would|should|do|does|did|is|are|will)\b",
            low))
        hard = len(t) > 90 or t.count(",") >= 2
        if kind == "think" and not is_q:
            kind = "ack"                     # they told us something; receive it, do not "think"
        elif is_q and hard:
            kind = "think"                   # a real question deserves the sound that buys time
        elif is_q and len(t) < 30:
            kind = "short"                   # a quick question gets a quick noise
    pool = list((_FILLERS or {}).get(kind) or (_FILLERS or {}).get("short") or [])
    if not pool:
        return ""
    fresh = [p for p in pool if p not in _RECENT] or pool
    # deterministic within the fresh set: a stable hash of the utterance, so the same thing said
    # twice picks the same sound and the behaviour stays reproducible for the bench
    pick = fresh[sum(ord(c) for c in low[:40]) % len(fresh)]
    _RECENT.append(pick)
    del _RECENT[:-_NOREPEAT]
    return pick


def maybe_filler(kind: str = "think", n: int = 0, stop=None, said: str = "",
                 log: list = None) -> float:
    """Play ONE cached thinking sound TRUE OF THE CURRENT STATE. Seconds spent, 0.0 if none.

    `log` collects WHICH sound played and for how long. Added 2026-07-29 because Luis said the
    thinking sounds were "one bit, it doesn't sound very human" and NOTHING in the receipt could
    confirm or deny it - the turn line reported a total and never a name, so there was no way to
    tell 73 varied sounds from the same one played 73 times. An unmeasurable complaint cannot be
    fixed, and the pool being large was an assumption about the code rather than an observation of
    the run (law M2: instrument the thing you are wrong about)."""
    p = choose_filler(kind, said)
    if not p:
        return 0.0
    import threading
    w = p.replace(".mp3", ".wav")            # the trimmed copy, when one exists
    t0 = time.time()
    _play_interruptible(w if os.path.exists(w) else p, stop or threading.Event())
    el = round(time.time() - t0, 3)
    if log is not None:
        log.append(f"{kind}/{os.path.basename(p).rsplit('_', 1)[-1].replace('.mp3','')} {el}s")
    return el


def warm(voice: str | None = None) -> float:
    """Pay the cold-connection cost ONCE, at boot, instead of on the first thing anyone says.

    MEASURED 2026-07-29: first render in a process 1.18-1.82s, every render after it 0.46-0.75s.
    The gap is TLS + the edge session, not the model. Renders two words to a throwaway file and
    returns the seconds spent, so the caller can print a real number rather than trust this."""
    t0 = time.time()
    try:
        edge_render("Ready.", os.path.join(grid.STATE, "_warm.mp3"), voice=voice or EDGE_VOICE)
    except Exception:
        pass
    return round(time.time() - t0, 2)


def _render_chunk(text: str, voice: str, idx: int, call: int = 0) -> dict:
    """One sentence -> one mp3 on disk. Distinct filenames: the player reads chunk N while the
    producer writes N+1, and a shared path would have them fighting over the same bytes.

    The `call` component matters since barge-in stopped joining the producer: an interrupted render
    thread stays alive long enough to finish the edge_render it was inside, and with only `idx % 6`
    it would write that dead audio over a file the NEXT turn was already playing."""
    path = os.path.join(grid.STATE, f"_stream_{call % 4}_{idx % 6}.mp3")
    t0 = time.time()
    ok = edge_render(text, path, voice=voice)
    el = time.time() - t0
    # PER-CHUNK TIMING, because the summed number cannot answer the question. Live turns report
    # render_s of 2.6 to 7.9 while the same call benches at 0.5s alone, 0.54s in a worker thread,
    # and 0.55s with whisper decoding flat out - CPU contention was the leading hypothesis and it
    # is DEAD. The remaining candidates need per-chunk evidence to separate: ONE pathological
    # render (a subprocess fallback, ~6s measured) versus MANY ordinary ones (the text is being
    # split into more chunks than expected).
    if el > 1.5:
        print(f"      [slow render {el:.2f}s for {len(text)} chars: {text[:40]!r}]", flush=True)
    return dict(text=text, path=path if ok else None, render=el, chars=len(text),
                error=None if ok else "render failed")


def _play_interruptible(path: str, stop) -> bool:
    """Play, but check the stop flag while the audio runs so a person can cut in MID-SENTENCE.
    sd.wait() blocks uninterruptibly, so poll in short slices and sd.stop() on the flag."""
    try:
        import soundfile as sf, sounddevice as sd
        data, sr = sf.read(path, dtype="float32")
        sd.play(data, sr)
        while sd.get_stream().active:
            if stop.is_set():
                sd.stop()
                return False
            time.sleep(0.01)      # 10ms, not 30ms. Humans retake the floor within ~200ms and the
                                  # poll is now a rounding error against that rather than 15% of it
        return True
    except Exception:
        return play_mp3(path)                     # never go silent: fall back to the blocking path


def edge_speak(text: str, timeout: int = 300, voice: str | None = None) -> bool:
    """Generate with edge-tts (mp3) then play via WPF MediaPlayer. Cloud - never for sensitive text."""
    mp3 = os.path.join(grid.STATE, "_live_edge.mp3")
    try:
        if not edge_render(text, mp3, voice=voice, timeout=timeout):
            return False
        return play_mp3(mp3, timeout=timeout)
    except Exception:
        return False


# ------------------------------------------------------------------ SAPI: the instant fallback
def sapi_speak(text: str, rate: int = 0, voice: str | None = None, timeout: int = 300) -> bool:
    ps = ("Add-Type -AssemblyName System.Speech; "
          "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
          f"$s.Rate = {int(rate)}; "
          + (f"try {{ $s.SelectVoice('{voice}') }} catch {{ }}; " if voice else "")
          + "$t = [Console]::In.ReadToEnd(); $s.Speak($t)")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                           input=text, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0
    except Exception:
        return False


# ------------------------------------------------------------------ the one interface
def speak(text: str, voice: str | None = None, rate: int = 0, cloud_ok: bool = True) -> bool:
    """Say it. voice: None -> identity.json -> edge (natural) when cloud_ok, else local engines.
    cloud_ok=False (sensitive zone) NEVER uses the cloud voice - the boundary is code, not a promise."""
    if not text.strip():
        return False
    try:
        from aea.kernel import pulse
        pulse.emit("voice", "speak", text[:80])
    except Exception:
        pass
    voice = voice or _identity().get("voice") or "edge"
    if voice == "edge" and not cloud_ok:
        voice = "kokoro:%d" % DEFAULT_SID if kokoro_available() else "sapi"
    if voice == "edge" and edge_available():
        if edge_speak(text):
            return True
        # cloud voice failed - fall through to the local floor, never go silent
        voice = "sapi"
    if voice.startswith("kokoro") and kokoro_available():
        sid = int(voice.split(":")[1]) if ":" in voice else DEFAULT_SID
        wav = os.path.join(VDIR, "_live.wav")
        r = kokoro_render(text, wav, sid=sid)
        if r["ok"]:
            return play_wav(wav)
        # fall through to sapi on any kokoro failure - the voice must never go silent
    return sapi_speak(text, rate=rate, voice=None if voice.startswith(("kokoro", "sapi", "edge")) else voice)


def narrate(script_path: str, out_dir: str, sid: int | None = None) -> list[dict]:
    """RECORD A PRESENTATION: split the script on blank lines (one block per slide/paragraph),
    render each to out_dir/part_NN.wav + a playlist.m3u. Returns the per-part render stats."""
    text = open(script_path, encoding="utf-8").read()
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    os.makedirs(out_dir, exist_ok=True)
    sid = sid if sid is not None else DEFAULT_SID
    results = []
    print(f"NARRATION: {len(blocks)} parts -> {out_dir}  (voice {SPEAKERS[sid]})")
    for i, block in enumerate(blocks, 1):
        wav = os.path.join(out_dir, f"part_{i:02d}.wav")
        r = kokoro_render(block, wav, sid=sid)
        results.append(r)
        print(f"  part {i:02d}: " + (f"{r['seconds_audio']}s audio in {r['seconds_gen']}s (rtf {r['rtf']})"
                                     if r["ok"] else f"FAILED {r.get('error')}"))
    with open(os.path.join(out_dir, "playlist.m3u"), "w", encoding="utf-8") as f:
        f.write("\n".join(f"part_{i:02d}.wav" for i in range(1, len(blocks) + 1)))
    ok = sum(1 for r in results if r["ok"])
    print(f"  -> {ok}/{len(blocks)} parts rendered; playlist.m3u written")
    return results


def list_voices() -> str:
    out = []
    if kokoro_available():
        out.append("KOKORO (human, local): " + ", ".join(f"{i}={n}" for i, n in enumerate(SPEAKERS)))
    else:
        out.append("KOKORO: not installed (voice/ missing)")
    ps = ("Add-Type -AssemblyName System.Speech; "
          "(New-Object System.Speech.Synthesis.SpeechSynthesizer).GetInstalledVoices() | "
          "ForEach-Object { $_.VoiceInfo.Name }")
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                       capture_output=True, text=True, timeout=30)
    out.append("SAPI (instant): " + ", ".join((r.stdout or "").split("\n")).strip())
    return "\n".join(out)


def main():
    a = sys.argv[1:]
    if "--voices" in a:
        print(list_voices()); return
    if "--narrate" in a:
        i = a.index("--narrate")
        sid = int(a[a.index("--sid") + 1]) if "--sid" in a else None
        narrate(a[i + 1], a[i + 2] if i + 2 < len(a) else os.path.join(HERE, "narration"), sid=sid)
        return
    sid = int(a[a.index("--sid") + 1]) if "--sid" in a else None
    fast = "--fast" in a
    words = [x for x in a if not x.startswith("--") and (sid is None or x != str(sid))]
    text = " ".join(words) or "I am online, running locally, on free power."
    if "--brief" in a:
        path = os.path.join(grid.STATE, "brief_output.md")
        try:
            text = open(path, encoding="utf-8").read().replace("#", "").replace("*", "").replace("_", " ")
        except Exception as e:
            print(f"no brief to read: {e}"); return
        name = _identity().get("name", "your entity")
        text = f"Good morning Luis. This is {name}. " + text
    voice = "sapi" if fast else (f"kokoro:{sid}" if sid is not None else None)
    print("spoke" if speak(text, voice=voice) else "TTS failed")


if __name__ == "__main__":
    main()
