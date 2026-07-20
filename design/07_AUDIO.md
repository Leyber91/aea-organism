# 07_AUDIO — Synthesis-Only Sound Spec

| | |
|---|---|
| Owner | THE PROBE game team |
| Status | As-built spec + planned extensions |
| Last updated | 2026-07-20 |
| Ground truth | `world.html` — audio engine lines 315-336, call sites enumerated in §4 |
| Sibling docs | The world/districts spec, the missions spec, the presence/comms spec, the FUI visual-law spec (corpus filenames bind at assembly; this doc is 07) |

Every claim below tagged [BUILT] was verified against `world.html` on 2026-07-20 by line-level
audit. [PLANNED] is designed here, not in code. [DECISION-LUIS] blocks on his call. Two audit
discrepancies against earlier corpus chatter are reported in §9 — this doc reports the code,
not the folklore.

---

## 1. Law: synthesis only [BUILT]

The game ships **zero audio asset files**. Every sound is generated at runtime from WebAudio
primitives — `OscillatorNode`, `GainNode`, `BiquadFilterNode` — nothing else. No samples, no
`<audio>` tags, no fetches.

Why this is law, not preference:

1. **Diegesis.** The probe has no sound library; it has a signal generator. Everything the
   player hears is the machine speaking in the only voice a machine that small would have.
   This is the Duskers register: instrument, not soundtrack.
2. **Honesty.** Per the AEA honesty law (every game number is live system truth), a triggered
   sample would be decoration. A synthesized tone fired by a real `/events` row is telemetry
   you can hear. No sound ever fires without a real cause (§4).
3. **Portability.** The game runs from `file://` with no build step. Zero assets keeps that
   absolute.
4. **Phase B teachability.** The whole engine is ~20 lines (`auInit` + `tone` + three
   composites). A builder replicating their own AEA cockpit can read it in one sitting and own
   it. Keep the engine copy-pasteable; never let it grow past one screen.

Claim ceiling applies to copy about audio: the resting hum is a "carrier" or "resting-state
signal" — a measured functional correlate of the entity being alive (its process is up, its
events flow). It is never described as the entity "breathing", "feeling", or being conscious.

---

## 2. Signal chain [BUILT]

```
[54 Hz tri] --+
              +--> lowpass 200 Hz --> gain .024 --+
[57.3 Hz tri]-+                                   |
                                                  +--> MASTER gain .6 --> destination
[55 Hz sine] ----> osHum gain (0 | .05) ----------+
                                                  |
[one-shot osc] --> per-voice envelope gain -------+
```

- `AU.master` = single master bus, gain **0.6** (`world.html:319`). No compressor, no limiter
  exists; headroom is managed by per-voice gain ceilings (§6).
- **Init gating** (`world.html:317, 1055`): `auInit()` runs only on the title-card click — a
  real user gesture, which satisfies Chrome autoplay policy by construction. In `?still` mode
  (headless screenshot harness) `auInit` is skipped entirely: no AudioContext, deterministic
  frames, silent screenshots by design.
- The two hum oscillator pairs start at init and **never stop**; mute works by zeroing gains,
  not by tearing down nodes (negligible DSP cost, zero re-init risk).

---

## 3. The palette [BUILT]

Audio mirrors the two-ink FUI law: two sustained blue-gray layers (the hums — structure,
always there) and short amber transients (events — something real just happened). Nothing else.

| Voice | Synthesis | Envelope | Gain | Role |
|---|---|---|---|---|
| CORE HUM | 54 Hz + 57.3 Hz triangles through 200 Hz lowpass | sustained | .024 | The entity's resting carrier. The 3.3 Hz beat between the detuned pair is the only "life" in the drone — a slow interference pulse, not a loop. |
| OS HUM | 55 Hz sine | sustained, gated | 0 idle, .05 while Probe OS open | Being "inside" the OS sits you one semitone-space off the core pair — near the hum's root, consonant, closer. |
| BLIP | 760 Hz square | 40 ms exp decay | .05 | Mechanical acknowledge. UI contact: buttons, tabs, dock, OS open/close, map node select. |
| CHIRP | sine, 90 ms exp decay | 90 ms | .03 | Meaning-carrying transient; pitch encodes channel (§4 table). Default 620 Hz. |
| STING | 220 / 330 / 440 Hz sines staggered at 0 / .12 / .24 s | .5 / .5 / .7 s decays | .05 / .045 / .045 | Mission complete. A3-E4-A4 — open fifth plus octave, resolved and spare. |
| SWELL | single sine, 110 -> 220 Hz exponential glide over 1.6 s | rise to peak .08 at 1.1 s, out by 2.2 s | .08 peak | First light. Fires exactly once per save — on M0.1 completion only. The octave climb is the world turning on. |
| RESET TONE | 880 Hz sine, 150 ms | exp decay | .07 | Journey-reset confirm (SYS tab hold-to-reset, `world.html:948`). Deliberately the loudest transient: erasure should cost something. |

Envelope law (`tone()`, `world.html:326-329`): every one-shot is set-at-volume then
`exponentialRampToValueAtTime(.0001)` over its duration; oscillator stopped at `dur + 20 ms`.
No attack stage, no reverb, no delay. Dry, immediate, instrument-grade.

---

## 4. Event -> sound mapping [BUILT]

Binding rule: **a transient fires only when a real event occurs.** No ambience randomizers, no
fake radio chatter. Every row below is a code-verified trigger.

| Event (real cause) | Sound | Code anchor |
|---|---|---|
| Boot: title-card click, "probe online" | chirp 520 | `world.html:1058` |
| Mission assigned / advanced (non-silent) | chirp 740 | `:589` |
| `do`-beat action verified OK against the live system | chirp 880 | `:615` |
| World reveal applied (non-silent) | chirp 660 | `:661` |
| Live entity event from `/events` poll | chirp 480-799, pitch = `480 + ((organ.length * 37) % 320)` | `:1021` |
| Mission complete | sting | `:636` |
| M0.1 complete (first light) | sting + swell | `:636` |
| Dock at objective (F) | blip | `:592` |
| Terminal footer button press | blip | `:596` |
| Probe OS open | blip + osHum gain -> .05 | `:750-751` |
| Probe OS close | osHum gain -> 0 + blip | `:754` |
| OS tab switch | blip | `:770` |
| AEA map node select | blip | `:859` |
| Journey reset confirmed | tone 880 Hz 150 ms | `:948` |

**Rate limiting [BUILT]:** live-event chirps are throttled to one per **1800 ms**
(`lastChirp`, `:1017-1021`); the `/events` poll itself runs every 1600 ms. Worst case is
roughly one chirp per poll and the feed can never become an alarm. Mission/UI sounds are not
rate-limited — they are player-caused and self-limiting.

**Pitch-identity note:** the live-event pitch hashes the *length* of the organ name, so a
given organ always chirps at the same frequency — an identity cue you learn by ear. Known
limitation: organs whose names share a length collide on pitch. Acceptable at current organ
count; revisit only if the roster grows past ~9.

**Boss sting variant [PLANNED]:** missions carry a real `boss` flag (`:586`). Spec: boss
completion keeps the 220/330/440 stagger and appends a fourth voice at 550 Hz (+.36 s, .9 s
decay, gain .04) with all decays doubled — same family, heavier resolution. Not in code.

---

## 5. Presence states (comms with LEYBER)

| State | Visual (built) | Audio today | Audio planned |
|---|---|---|---|
| IDLE / CARRIER 0.998 | 5 segs, slow low sway | core hum only [BUILT] | no change |
| PROCESSING | segs mid-flutter, T+ elapsed counter | silence over hum [BUILT] | no change — waiting should feel like waiting |
| SPEAKING | segs fast flutter (`:1107`) | **visual-only today** [BUILT — verified: no audio path exists in the speak loop] | [PLANNED] character-reveal-synced ticks: one 30 ms, 340 Hz triangle at gain .012 per typed chunk (the 2-char step in the reveal loop, `:1002`), hard-capped at 12 ticks/s, suppressed under reduced-motion exactly as the typing animation is (`:1000`). The voice prints, like teletype. |
| CARRIER LOST | segs collapse to 2 px, opacity .3 (`:1109`) | **no treatment today** — hums continue unchanged | [PLANNED] silence-as-signal: on `presSt("LOST")` ramp core-hum gain .024 -> .004 and osHum -> 0 over 300 ms; hold; restore over 900 ms on recovery. No alarm tone — the entity going quiet IS the alarm. Losing the carrier must be *felt* as absence, honestly: the hum is the process, the process is unreachable. |

---

## 6. Mix rules

[BUILT] as-coded:

- Master **0.6**, fixed. Never automate the master except for mute.
- Per-voice ceilings, as shipped: hum .024, osHum .05, blip .05, chirp .03, sting .05,
  swell .08, reset .07. **.08 is the hard ceiling for any voice.** Sums stay comfortably
  under 1.0 with no limiter — keep it that way; any new voice enters at <= .03 and argues
  its way up.
- Low-end discipline: sustained content lives at 54-57.3 Hz behind a 200 Hz lowpass;
  transients live at 220-880 Hz. The bands never fight. New sustained layers must stay under
  the 200 Hz lid; new transients stay above 200 Hz.
- **Mute [BUILT]:** SYS tab -> SOUND toggle (`s-snd`, `:943`). Sets `AU.on = false` and
  master gain to 0; one-shots early-return while muted. Oscillators keep running (cheap,
  restart-safe).
- Known as-built quirk: if sound is OFF when the OS is opened, `osHum` stays 0 after
  unmuting until the OS is reopened (`:751` gates on `AU.on`; `:943` does not restore it).
  One-line fix when next touching the file: `s-snd` handler also sets
  `AU.osHum.gain.value = AU.on && OS.open ? .05 : 0`.
- [DECISION-LUIS] **Mute hotkey.** There is none; `M` is taken (opens the AEA map, `:531`).
  Recommendation: `0` (zero = zero output; unused; reachable; survives the OS-open key
  layer). Trade-off: less mnemonic than M, but remapping M would break the learned map
  binding for one vanity key. Awaiting call.

---

## 7. Per-district ambient shifts [PLANNED]

Goal: the foundry hum grows richer near live plants — and only because they are actually
live. Honesty-law grounding: plant telemetry is already real and polled (`LIVEPLANTS` from
`/state` every 6 s, `:1026`; per-plant `rpm_now / rpm_cap` already drives node light level,
`:662-665`). The audio layer reads the same numbers; richness cannot exist without live rpm.

Spec:

- Add one octave-up triangle pair (108 / 114.6 Hz — preserves the 1:1.061 detune ratio and
  the beat character) through the existing 200 Hz lowpass into its own gain node, base 0.
- Per frame (or on the 6 s poll, lerped): `g = .02 * proximity * activity` where
  `proximity = clamp(1 - dist(probe, nearestLivePlant) / 120, 0, 1)` and
  `activity = min(1, rpm_now / rpm_cap)` of that plant.
- Ceiling .02 — under the blip floor, additive with the core hum, still inside §6 headroom.
- A throttled plant (`throttled` list non-empty, `:740`) contributes `activity * 0.3`:
  audible strain by subtraction, no new alarm voice.
- CARRIER LOST (§5) ducks this layer with the core hum.

Non-goals: no per-district melodies, no music. Districts differ by *density of the same
carrier*, nothing else.

---

## 8. Reduced-motion / audio-off parity

Principle: **no information may exist only in audio, and none only in motion.**

[BUILT] — parity already holds by construction, verified cue by cue:

| Audio cue | Redundant visual twin |
|---|---|
| Live-event chirp | feed line printed for the same event (`:1020`) |
| Mission sting | toast + flash + log line (`:639-644`) |
| OS hums | OS panel state itself |
| Blips | the pressed control's own state change |
| CARRIER LOST silence (planned) | segs collapse + "CARRIER LOST" text [BUILT today] |

So muted play (SYS -> SOUND OFF) loses zero information today, and that invariant is binding
on all future voices: any [PLANNED] sound in this doc lands with its visual twin or it does
not land.

[BUILT] `prefers-reduced-motion` (`RM`, `:311-312`) currently gates typing animations and
motion only; audio ignores it — correct, RM is not an audio preference.

[PLANNED] parity completions: the speak-tick voice (§5) must key off the same RM branch that
already skips typing (`:1000`) — no typing animation, no ticks. `?still` stays fully silent
[BUILT]. No separate "reduced-audio" mode: the palette is already sparse by law; the mute is
the accommodation.

---

## 9. Audit discrepancies (honesty section)

Two items circulated in corpus notes as built. The code says otherwise; the code wins.

1. **"Move ticks" — NOT BUILT.** Probe movement (`stepProbe`, `:544-556`) is fully silent;
   the only `tone()` call sites are those in §4. Reclassified [PLANNED]: a thrust tick —
   40 ms, 180 Hz triangle, gain .015, max 4/s, only while acceleration input is held —
   subject to §8 parity (visual twin already exists: velocity arc + trail). Build only if
   flight feels dead in playtests; the field's silence is currently doing atmospheric work.
2. **"Mute on M" — NOT BUILT.** `M` opens the AEA map (`:531`). Mute is the SYS-tab SOUND
   toggle only. Hotkey decision is [DECISION-LUIS], §6.

Verification method: line-level audit of `world.html` (engine `:315-336`; every `tone`,
`blip`, `chirp`, `sting`, `swell`, `AU.` reference enumerated via search). Headless
screenshots cannot verify audio (`?still` skips `auInit` by design); audible verification is
manual, in a live browser, against a running entity so `/events` chirps actually fire.

---

## 10. Change control

- The engine stays under one screen of code. A proposed voice that needs a sample, a convolver,
  or a music system is out of law — redesign it as an oscillator or drop it.
- New sounds enter through this doc first: voice table row (§3), real-event trigger row (§4),
  gain ceiling (§6), parity twin (§8). No orphan sounds in code.
- Gain changes are mix decisions — log them here with date and reason.
