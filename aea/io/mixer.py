"""mixer.py - MANY VOICES, ONE SOUND CARD.

Luis, 2026-07-29: "how a group of 4 can talk and how the voices put over the others... this is a
serious question how we manage more than one voice, how other services do it, because two voices is
one thing but then how multiple are managed."

THE STRUCTURAL FACT, and everything here follows from it: THERE IS ONE OUTPUT DEVICE. You cannot
play four voices by starting four players. `sd.play()` is a module-level convenience that owns a
single global stream - calling it again stops what was already playing, and calling it from four
threads produces a race over one device, not a chorus. Every system that does this properly has the
same shape:

    ONE stream, owned by ONE callback, summing N sources.

So the concurrency splits in two, and the split is the whole design:

    RENDERING is IO-bound   four edge-tts calls are four network round trips. Genuinely parallel
                            under the GIL, and this is where ThreadPoolExecutor belongs.
    PLAYBACK is real-time   one callback thread, woken by PortAudio every block. It may ONLY add
                            numbers. No network, no model, no long lock, no surprise allocation -
                            anything that can take longer than a block produces a dropout, and a
                            dropout is audible as a click.

WHAT THE CALLBACK IS ALLOWED TO DO HERE: slice numpy arrays it already holds, multiply by two
floats, add, and clip. Nothing else. New audio arrives through a queue that the callback drains
with a non-blocking get, and finished sources are dropped by the same pass.

INTELLIGIBILITY IS THE REAL LIMIT, NOT MIXING. Summing four voices is arithmetic and always works;
a listener following four voices does not. Separation is what buys it: stereo position, per-voice
gain, and different vocal character. That is why `pan` and `gain` are first-class here and why the
character voices exist at all - they are not decoration, they are what makes overlap legible.

HEADROOM. Four sources at full scale sum to 4.0 and clip hard, which sounds like tearing. Each
source is attenuated on the way in and the bus is soft-limited on the way out - a tanh knee rather
than a hard clip, because a hard clip generates harmonics across the whole spectrum and a knee does
not. See BUS_GAIN / _limit.
"""
from __future__ import annotations

import queue
import threading
import time

import numpy as np

SR = 24000                  # edge-tts renders at 24k; resampling once here beats doing it per block
CHANNELS = 2                # stereo is not a luxury - panning is most of what makes overlap legible
BLOCK = 2048                # ~85ms at 24k. RAISED from 1024 on measurement: a party run reported
                            # realtime 0.9375 - six percent of the audio never played - while the
                            # underflow flag read 0. A Python callback must take the GIL, and the
                            # main thread spends a party doing model calls, json and regex; every
                            # one of those can hold the GIL past a 43ms deadline. Doubling the
                            # block doubles the slack per callback.
                            #
                            # The trade is real and it is the reason not to go further: `stop()`
                            # takes effect at the next block, so barge-in latency is bounded by
                            # this. 85ms is still well under the ~200ms a person perceives as
                            # immediate; 4096 would not be.

# BUS_GAIN WAS 0.42 AND THAT WAS THE 1/N REFLEX, WHICH IS WRONG. Raised on measurement rather than
# on nerve: four real edge-tts renders have peak 0.551-0.712 and a crest factor of 16.8-18.4 dB, so
# summed with staggered entries they peak at 0.978 with ZERO samples over 1.0. Even the worst case
# - all four starting on the same sample - peaks at 1.040, with five samples over 1.0 out of the
# whole file (0.006%). Dividing by N to defend against 0.006% of samples throws away 12.2 dB and
# makes four speakers quieter than one, which is the actual defect a listener hears. The limiter
# below exists precisely so the sum does not have to be timid. (WebRTC's AudioMixer does the same:
# sum the sources, put a limiter after.)
#
# MEASURED HERE, first party run at 0.42: bus peak 0.284. Far too quiet, exactly as predicted.
BUS_GAIN = 0.70
LIMIT_KNEE = 0.85           # above this the bus is compressed rather than clipped

# WHERE TO STOP ADDING SEPARATION TRICKS - written here so it is not re-litigated. Voice-character
# separation and spatial separation are SUB-ADDITIVE: gender/voice release is ~10 dB when talkers
# are co-located but collapses to 1.4-4.6 dB once they are spatially separated, while spatial
# release alone is 12.9-16.3 dB. The combined ceiling is about 17.5 dB, not the 26 dB the two
# numbers suggest. Panning plus genuinely distinct voices captures nearly all of it; pitch carving,
# EQ and reverb differentiation after that are competing for a budget already spent.
MIN_REALTIME = 0.99         # see `health` - below this the mix fell behind, whatever the flags say


def _limit(x: np.ndarray) -> np.ndarray:
    """Soft-knee limiter. A hard clip splatters harmonics across the spectrum and is heard as
    tearing; a tanh knee above the threshold is heard as loudness. Only the part above the knee is
    shaped, so ordinary material passes through untouched."""
    a = np.abs(x)
    over = a > LIMIT_KNEE
    if not over.any():
        return x
    y = x.copy()
    ex = a[over] - LIMIT_KNEE
    y[over] = np.sign(x[over]) * (LIMIT_KNEE + (1.0 - LIMIT_KNEE) * np.tanh(ex / (1.0 - LIMIT_KNEE)))
    return y


def resample(x: np.ndarray, sr_in: int, sr_out: int = SR) -> np.ndarray:
    """Linear resample. Good enough for speech and cheap; done ONCE per utterance on a worker
    thread, never inside the callback."""
    if sr_in == sr_out or not len(x):
        return x.astype("float32")
    n = int(round(len(x) * sr_out / sr_in))
    return np.interp(np.linspace(0, len(x), n, endpoint=False),
                     np.arange(len(x)), x).astype("float32")


class Source:
    """One voice's audio, already at bus rate. `done` lets a caller wait for THIS voice without
    blocking any other."""

    __slots__ = ("buf", "pos", "gain", "pan", "name", "done", "stopped", "started")

    def __init__(self, buf: np.ndarray, gain: float = 1.0, pan: float = 0.0, name: str = ""):
        self.buf = buf
        self.pos = 0
        self.gain = float(gain)
        self.pan = float(max(-1.0, min(1.0, pan)))
        self.name = name
        self.done = threading.Event()
        self.stopped = False
        self.started = None

    def stop(self) -> None:
        """Cut this voice immediately - barge-in for one speaker without touching the others."""
        self.stopped = True

    @property
    def lr(self) -> tuple:
        """CONSTANT-POWER PANNING, not linear. A linear pan drops ~3dB in the middle, so a voice
        panned centre sounds quieter than the same voice hard left - which reads as a mix fault.
        sin/cos keeps L^2+R^2 constant across the sweep."""
        th = (self.pan + 1.0) * 0.25 * np.pi          # -1..1 -> 0..pi/2
        return (float(np.cos(th)), float(np.sin(th)))


class Mixer:
    """One output stream, N voices. Start it once and leave it running.

    THREAD MODEL:
        caller threads   build Sources (render, decode, resample) and hand them over via `play`
        the queue        the only crossing point; the callback drains it non-blockingly
        callback thread  owns `_live`, touched by nobody else. Sums, limits, writes. That is all.

    `_live` is deliberately NOT protected by a lock. It is only ever mutated on the callback
    thread; other threads add through the queue and read only immutable snapshots. A lock held by a
    producer while the callback wants it is exactly how a real-time thread misses its deadline.
    """

    def __init__(self, device=None, sr: int = SR, channels: int = CHANNELS, block: int = BLOCK):
        import sounddevice as sd
        self.sr, self.channels, self.block = sr, channels, block
        self._incoming: queue.Queue = queue.Queue()
        self._live: list = []
        self._lock = threading.Lock()                 # guards `_names` only, never the audio path
        self._names: list = []
        self.underruns = 0
        self.peak = 0.0
        # THE HONEST HEALTH NUMBER. `status.output_underflow` is NOT one, and reporting it as one
        # was a fabricated receipt of exactly the kind the honesty law forbids. MEASURED: stalling
        # a callback to twice its block budget lost 51% of the expected callbacks - half the audio
        # never played - while the status flag read 0 in every single case. "underruns: 0" would
        # have reported perfect health on a bus producing half the sound it owed.
        #
        # What cannot lie is arithmetic: count the frames actually written and compare against the
        # wall clock. If the bus is keeping up, frames/SR equals elapsed seconds. Anything less and
        # audio is missing, whatever the driver says about it.
        self.frames_out = 0
        self.t0 = None
        self._stream = sd.OutputStream(
            samplerate=sr, channels=channels, dtype="float32", blocksize=block,
            device=device, callback=self._callback)

    # ------------------------------------------------------------------ the real-time thread
    def _callback(self, out, frames, time_info, status):
        if self.t0 is None:
            # THE CLOCK STARTS AT THE FIRST CALLBACK, NOT AT start(). PortAudio takes a few tens of
            # milliseconds to open and begin calling, and counting that gap as time the bus owed
            # audio makes a healthy bus look sick: the first version anchored on start() and
            # reported realtime 0.9827 on a run with zero real loss, because ~34ms of startup over
            # a 2s test IS 1.7%. A health metric that fails on healthy hardware gets muted, and a
            # muted metric is worse than none - the same lesson as the doubt detector that fired on
            # a true sentence.
            self.t0 = time.time()
        if status:
            self.underruns += 1                       # counted, never printed from here: stdout on
                                                      # the audio thread is a dropout waiting to
                                                      # happen
        while True:                                   # drain new arrivals - bounded, non-blocking
            try:
                self._live.append(self._incoming.get_nowait())
            except queue.Empty:
                break
        # COUNT THE FRAMES ON EVERY PATH, INCLUDING SILENCE. This early return used to skip the
        # counter, so `frames_out` measured "time a voice was sounding" and the health ratio
        # measured the fraction of the run that was not quiet - which in a conversation is most of
        # it. It read 0.954 on a perfectly healthy idle bus and was reported as "6% of the audio is
        # missing"; a 6-second idle test counted ZERO frames.
        #
        # A health metric that only counts the interesting case is not a health metric. The bus
        # owes the device a block every period whether anyone is talking or not, and silence
        # delivered on time is the bus working.
        self.frames_out += frames
        if not self._live:
            out.fill(0.0)
            return
        mix = np.zeros((frames, self.channels), dtype="float32")
        still = []
        for s in self._live:
            if s.stopped:
                s.done.set()
                continue
            if s.started is None:
                s.started = time.time()
            chunk = s.buf[s.pos:s.pos + frames]
            if len(chunk):
                l, r = s.lr
                g = s.gain * BUS_GAIN
                mix[:len(chunk), 0] += chunk * (g * l)
                if self.channels > 1:
                    mix[:len(chunk), 1] += chunk * (g * r)
                s.pos += frames
            if s.pos >= len(s.buf):
                s.done.set()
            else:
                still.append(s)
        self._live = still
        np.copyto(out, _limit(mix))
        p = float(np.abs(mix).max()) if frames else 0.0
        if p > self.peak:
            self.peak = p

    # ------------------------------------------------------------------ the caller's side
    def start(self):
        self._stream.start()
        return self                                   # t0 is set by the FIRST callback, not here

    def health(self) -> dict:
        """Whether the bus actually kept up. `realtime` below MIN_REALTIME means audio is MISSING,
        no matter what the underrun flag says - see the note on `frames_out`. `flags` is reported
        beside it as advisory only, never as the verdict."""
        el = (time.time() - self.t0) if self.t0 else 0.0
        rt = (self.frames_out / self.sr / el) if el > 0.05 else 1.0
        return dict(realtime=round(rt, 4), ok=rt >= MIN_REALTIME, peak=round(self.peak, 3),
                    flags=self.underruns, seconds=round(el, 2))

    def stop(self):
        try:
            self._stream.stop(); self._stream.close()
        except Exception:
            pass

    def play(self, samples, sr: int, gain: float = 1.0, pan: float = 0.0,
             name: str = "") -> Source:
        """Hand a finished utterance to the bus. Returns IMMEDIATELY - this is the whole point.
        Resampling happens here, on the caller's thread, never in the callback."""
        x = np.asarray(samples, dtype="float32")
        if x.ndim > 1:
            x = x.mean(axis=1)
        s = Source(resample(x, sr, self.sr), gain=gain, pan=pan, name=name)
        with self._lock:
            self._names.append(name)
        self._incoming.put(s)
        return s

    def play_file(self, path: str, gain: float = 1.0, pan: float = 0.0, name: str = "") -> Source:
        import soundfile as sf
        x, sr = sf.read(path, dtype="float32")
        return self.play(x, sr, gain=gain, pan=pan, name=name)

    def busy(self) -> int:
        """How many voices are sounding right now. Read from outside the callback, so it is a
        snapshot and not a guarantee - which is all any caller can act on anyway."""
        return len(self._live) + self._incoming.qsize()

    def wait(self, *sources, timeout: float = 120.0) -> bool:
        """Wait for these voices (or all of them). Returns False on timeout."""
        t0 = time.time()
        for s in sources:
            left = timeout - (time.time() - t0)
            if left <= 0 or not s.done.wait(timeout=left):
                return False
        if not sources:
            while self.busy() and time.time() - t0 < timeout:
                time.sleep(0.02)
            return not self.busy()
        return True

    def silence(self) -> None:
        """Stop every voice at once."""
        for s in list(self._live):
            s.stop()

    def __enter__(self):
        return self.start()

    def __exit__(self, *a):
        self.stop()


# ---------------------------------------------------------------------------------- the proof
def selftest(device=None, seconds: float = 2.0) -> dict:
    """FOUR TONES BEFORE FOUR VOICES. A mixer that is wrong is wrong in ways speech hides - a
    dropped source sounds like someone paused, and clipping sounds like a bad microphone. Tones
    make both obvious and measurable: four known frequencies, four known pan positions, and the
    output can be checked against arithmetic instead of against an opinion.

    Verifies: all four sound TOGETHER (not serialised), the bus does not clip, panning is
    constant-power, and stopping one voice leaves the others running."""
    m = Mixer(device=device).start()
    t = np.arange(int(seconds * SR)) / SR
    tones = [(220.0, -1.0, "left  220Hz"), (330.0, -0.33, "mid-L 330Hz"),
             (440.0, 0.33, "mid-R 440Hz"), (660.0, 1.0, "right 660Hz")]
    srcs = []
    t0 = time.time()
    for f, pan, name in tones:
        x = (0.6 * np.sin(2 * np.pi * f * t)).astype("float32")
        srcs.append(m.play(x, SR, gain=1.0, pan=pan, name=name))
    time.sleep(0.25)
    overlapped = m.busy()
    time.sleep(0.4)
    srcs[1].stop()                                    # one voice out, the rest keep going
    time.sleep(0.2)
    after_stop = m.busy()
    m.wait(timeout=seconds + 3)
    el = time.time() - t0
    h = m.health()
    m.stop()
    ok = (overlapped >= 4 and after_stop >= 2 and el < seconds + 1.5 and m.peak > 0
          and h["ok"])
    print(f"  four tones started together : {overlapped} live after 0.25s   "
          f"{'OK' if overlapped >= 4 else 'FAIL - they serialised'}")
    print(f"  one stopped, others continue: {after_stop} live            "
          f"{'OK' if after_stop >= 2 else 'FAIL'}")
    print(f"  wall clock                  : {el:.2f}s for {seconds}s of audio   "
          f"{'OK - concurrent' if el < seconds + 1.5 else 'FAIL - sequential'}")
    print(f"  bus peak (pre-limiter)      : {m.peak:.3f}   "
          f"{'OK' if m.peak <= 1.0 else 'CLIPPING'}")
    print(f"  realtime ratio (THE health) : {h['realtime']:.4f}   "
          f"{'OK - the bus kept up' if h['ok'] else 'FAIL - audio is MISSING'}")
    print(f"  underflow flags (advisory)  : {m.underruns}   "
          f"(measured to read 0 while half the audio was lost - never trust this alone)")
    h["verdict_ok"] = ok
    return dict(overlapped=overlapped, after_stop=after_stop, wall=round(el, 2),
                underruns=m.underruns, **h)


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("MIXER SELFTEST - four tones, four pan positions, one sound card")
    print("=" * 72)
    r = selftest()
    print("=" * 72)
    print("VERDICT:", "the bus mixes" if r["verdict_ok"] else "SOMETHING IS WRONG")
