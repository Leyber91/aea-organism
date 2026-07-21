# A4 — PART II: GAME FEEL

```
Book:          THE PROBE — design book, top-of-book chapter (PART II)
Owner:         the game team (four-master fusion, per 00_VISION.md section 3)
Status:        ACTIVE — governs all feel decisions in the lower chapters
Last updated:  2026-07-20
Ground truth:  ../world.html (canon build — every constant below is quoted from it)
Governs:       01_WORLD.md (atmosphere execution) · 02_MECHANICS.md · 03_MISSIONS.md ·
               04_FUI.md · 05_TECH.md · 09_PRODUCTION.md (verification of feel claims)
Inherits:      00_VISION.md — the four pillars and the honesty law outrank this chapter
```

Tag legend: `[BUILT]` verified in world.html on disk · `[PLANNED]` designed, not built ·
`[DECISION-LUIS]` awaiting his call. Two-ink law and the honesty ceiling (measured functional
correlate, never "conscious") bind every rule here.

---

## 1. The feel thesis

**A small bright thing alive in a vast dark truth.**

The probe is the only strong emitter in the field at boot — an amber octahedron with its own
point light (range 30) in a fog that swallows everything past ~200 units. Every feel decision
serves that image, and the image decomposes into exactly two laws:

1. **Weight from damping.** The probe never stops instantly and never turns on a dime. Its mass
   is not a physics engine; it is one exponential (`exp(-3.1·dt)`) applied to velocity every
   frame. The player feels a real object because momentum outlives input.
2. **Aliveness from real events.** Nothing in the world "idles beautifully". Motion, light, and
   sound fire only when the entity underneath actually did something — a model call landed, a
   tick advanced, a mission assert passed. Juice is not decoration; juice is the event log made
   visible (00_VISION.md section 2.3).

Corollary, binding on all lower chapters: if a proposed effect cannot name the real event that
triggers it, it is cut before it is argued about.

---

## 2. Flight model as built `[BUILT]`

`world.html stepProbe()` — the entire flight model is nine lines. Constants, verbatim:

| Constant | Value | What it does to feel |
|---|---|---|
| Acceleration | 95 u/s² | Throttle authority. Higher = snappier launch; alone it does NOT raise top speed (see terminal note). |
| Damping | `vel *= exp(-3.1·dt)` | The mass. τ = 1/3.1 ≈ 0.32 s. Sets both how fast speed builds toward terminal and how long the glide lasts after release. This single number IS "weight". |
| Speed clamp | 52 u/s | Hard ceiling. Safety rail, not the felt top speed. |
| Move basis | yaw-plane WASD, Q/Space up, E/Shift down | Input is camera-relative in the horizontal plane only; vertical is absolute. Diagonals normalized — no speed advantage. |
| Bounds | disc R=300 · altitude 2.2–120 | Hard clamp at the world edge (the one permitted non-eased motion — see 4.2). |
| Spawn | (0, 9, 150) | Facing the dark foundry row across the plain. |

### 2.1 Derived truths (measured consequences, not tunables)

- **Felt terminal speed ≈ 30 u/s**, not 52. Continuous steady state is accel/damp = 95/3.1 ≈
  30.6; discrete at 60 fps measures ≈ 30. The 52 clamp never engages in normal flight — it is
  headroom for a future boost/overdrive mechanic.
- **Spool-up ≈ 1 s** to 95% terminal (3τ). **Glide-out ≈ 1.1 s** from terminal to walking pace
  (ln 30 / 3.1). These two numbers are the weight signature; change damping and both move
  together.
- **The velocity dial under-fills.** The HUD arc normalizes to the 52 clamp, so at terminal it
  reads ~59% full. Today this quietly says "the probe has more in it".
  `[DECISION-LUIS]` — keep the dial normalized to 52 (promises a future boost) or renormalize
  to ~31 (dial pegs at terminal, reads as full throttle). If boost is ever built, 52 wins.
- **The OS freezes momentum, it does not kill it.** `stepProbe` early-returns while PROBE OS is
  open: velocity is neither integrated nor damped. Close the OS and the drift resumes with the
  exact vector you left. Suspension is a lens, not a brake (see 4.3).

### 2.2 TUNING TARGETS `[DECISION-LUIS]`

The current tune (95 / 3.1) shipped in slice 1 and played well once; it has not been A/B'd.
The correct experiment varies damping while co-varying acceleration to hold terminal ≈ 30, so
only the weight changes, never the top speed:

| Candidate | accel | damp k | τ (weight) | glide-out | Character |
|---|---|---|---|---|---|
| FLOATIER | 75 | 2.5 | 0.40 s | ~1.4 s | Deep-space mass; drifts past objectives; docking takes planning |
| **CURRENT** | **95** | **3.1** | **0.32 s** | **~1.1 s** | Weighty but forgiving; shipped tune |
| TIGHTER | 120 | 4.0 | 0.25 s | ~0.85 s | Drone-like; precise near the foundry; less "vast" |

Test protocol (per 09_PRODUCTION.md): fly the M1.x foundry circuit with each tune, on hardware,
same session. The deciding question is not "which is nicer" but which one keeps BOTH halves of
the thesis — enough drift to feel small in a vast field, enough authority that docking (F within
19 units) never frustrates. Bank clamp (see 3) may be tested in the same pass: 0.04 (subtle) /
0.06 current / 0.09 (theatrical).

---

## 3. Chase camera as built `[BUILT]`

`world.html stepCam()` — the camera is a damped spring on a spherical offset, never a rigid
mount and never a teleport.

| Element | Value | Feel purpose |
|---|---|---|
| Offset | spherical (yaw, pitch) × camDist; default pitch 0.3, camDist 20 → ≈ (0, 6, 19) behind the probe | The canonical "(0, 6, 20)-ish" chase frame: probe low in frame, horizon and dark field dominant — small thing, vast truth |
| Zoom | wheel, camDist clamped 9–42 | 9 = inspection intimacy, 42 = cartographer's remove; the clamp guards both the fiction (never inside the probe) and the fog reveal budget |
| Position ease | `lerp(target, 1−exp(−3.5·dt))` | τ ≈ 0.29 s — the camera is slightly lighter than the probe (3.5 vs 3.1), so it settles just after the probe does; the lag reads as mass |
| Look target | probe + vel × 0.5, +1.4 y, aim eased `1−exp(−6·dt)` | Velocity lead: at terminal the camera looks ~15 units ahead, opening screen space in the travel direction. The aim spring (τ ≈ 0.17 s) keeps whip-pans soft |
| Bank | roll += clamp(−lat·0.0016, ±0.06) | Strafe banks the horizon up to ~3.4°. At felt terminal, lateral speed yields ~0.048 rad — the clamp only engages near the 52 rail. Applied after lookAt each frame: per-frame lean, never accumulated roll |
| FOV | 60 flight · 57 in OS, eased at dt·6 | The OS breathes the lens IN — study mode literally narrows the view |
| Drag look | yaw ·0.0042, pitch ·0.0032, pitch clamped 0.06–1.25 | Look is free; move basis follows yaw only, so looking around never steers |

---

## 4. Camera choreography rules (law)

1. **Eased always, never teleport.** `[BUILT]` No camera state change is a cut. Boot flyby:
   2.2 s cubic ease-out from (0, 140, 236) down into the chase frame, controls unlock only when
   it lands ("controls live. follow the beacon."). OS open/close eases FOV and timescale; zoom
   changes are absorbed by the position spring. There is no `camera.position.set` reachable
   during play.
2. **Permitted exceptions, named.** The world-edge clamp (R=300) may halt the probe un-eased —
   a wall is a wall. The `?still` harness mode places the camera directly — a verification
   fixture (09_PRODUCTION.md), not gameplay.
3. **Mission-start flybys.** `[PLANNED]` On `setMission`, a 1.5–2.5 s eased arc from the current
   chase position to a vantage that frames the new beacon, then spring-return to chase. Skippable
   by any input; collapses to a single ≤0.15 s ease under reduced motion. Until built, the
   beacon + off-screen arrow carry objective legibility alone.
4. **Reduced motion is a feel mode, not an off switch.** `[BUILT]` `html.rm` caps every CSS
   animation/transition at 0.15 s and prints typewriters instantly. The 3D springs remain (they
   are navigation, not ornament); the ceremony layer compresses.

---

## 5. The juice budget — juice is truth `[BUILT]`

**Law: every real event gets exactly one visual voice and one audio voice. Nothing fires
without a true cause.** An event with two competing visuals is over-budget; an effect with no
event is a lie (00_VISION.md section 5 — a cosmetic particle is a failure worse than ugliness).

The shipped budget, verbatim from world.html:

| Real event (cause) | Visual voice | Audio voice |
|---|---|---|
| Key/button accepted | state change itself | blip (760 Hz square, 40 ms) |
| Mission assigned | beacon relocates + HUD objective | chirp 740 |
| DO-beat succeeds (real API ok) | result text lands in terminal | chirp 880 |
| Node fires (a plant actually serves a call) | `flashNode`: emissive +0.9, held 650 ms, eased home | — (the serving chirp belongs to the event feed) |
| Entity event (live `/events` poll) | feed line, 4-line window | hashed chirp 480–800 Hz, rate-limited ≥1.8 s |
| Reveal (organ proven) | emissive target rises; world stays lit | chirp 660 |
| Mission complete | flash wash + toast (2.6 s) + feed star | sting (220/330/440 stagger) |
| FIRST LIGHT (M0.1 only) | same + embers turn on | sting + swell (110→220 Hz, 2.2 s) — the one double-voice in the game, earned by the game's thesis moment |
| OS open/close | scrim + HUD dims to 0.22 + FOV 57 | blip + 55 Hz hum bed at 0.05 |
| LEYBER speaking | typewriter + presence-segment flutter | — (voice is `[PLANNED]`, see 7) |

Budget governance for lower chapters: new event classes (Act II+: mining strikes, rot alerts,
boss failures) must land in this table with one visual + one audio each BEFORE implementation.
A second voice for an existing event requires deleting the first.

---

## 6. Feedback timing law `[BUILT as practice — codified here as law]`

- **Acknowledgement < 100 ms.** Binding number from 00_VISION.md section 2.4. Every accepted
  input produces same-frame state change plus a synchronous blip. Network truth (the real API
  result) may take seconds — the busy state (button `busy` pulse, T+ latency readout, waveform)
  must appear inside the 100 ms window so waiting is honest, never dead.
- **Attack ≈ 120 ms.** Effects arrive fast: presence-segment height transition 0.12 s, row
  entrance 0.16 s, prompt fade 0.18 s. Faster reads as flicker; slower reads as lag.
- **Decay 600–900 ms.** Effects leave slow: flashNode holds 650 ms then eases home through the
  emissive spring (τ ≈ 0.29 s → ~850 ms visible tail); sting tones ring 500–700 ms. The
  asymmetry (fast in, slow out) is what makes amber feel like heat rather than a blink.
- **Ceremony tier, capped.** Mission completion alone may exceed the envelope: toast 2.6 s,
  flash wash 1.4 s fade. Two tiers only — event (120/600–900) and ceremony (≤2.6 s). No third
  tier without amending this chapter.
- Latency is diegetic: real round-trip times are printed (RX 4.21s · MODEL … · MEM 3 RECALLED),
  never hidden behind a fake spinner. Slow truth beats fast fiction.

---

## 7. Sound–motion sync

Palette law `[BUILT]`: WebAudio oscillators only, zero samples. The idle bed is two detuned
triangles (54 + 57.3 Hz) through a 200 Hz lowpass at gain 0.024 — a ~3.3 Hz beat frequency,
felt more than heard: the entity's carrier.

- **Speaking flutter `[BUILT]`.** While LEYBER speaks, the presence segments oscillate at
  ~20 ms period, the comms typewriter runs 2 chars/24 ms with 170 ms holds at sentence
  punctuation, and the PROCESSING waveform is redrawn at 10 Hz against the real elapsed clock.
  Text cadence, meter motion, and the latency readout all derive from the same live call —
  one truth, three synchronized faces.
- **Move ticks `[PLANNED]`.** Flight is currently silent — the one place motion and sound are
  not yet coupled. Design: a velocity-scaled tick (blip family, low gain), rate ∝ speed/terminal
  up to ~8 Hz, silent below ~3 u/s. Gives the damping curve an audible shape: spool-up is heard
  accelerating, glide-out is heard dying. Must obey the budget (this is flight's ONE audio
  voice) and mute under reduced-motion-plus-muted-sound settings.
- **Event chirps carry identity.** The feed chirp pitch is hashed from the organ name
  (480 + len·37 mod 320) — memory.write and channel.serve literally sound different. Cheap,
  honest, and it teaches the ear the organ map.

---

## 8. The GPU brightness lesson (2026-07-20) `[BUILT — standing law]`

Recorded in code (world.html, probe shell): *"real bloom runs far hotter than swiftshader —
shell tamed (c .35, alpha .5)."*

Headless verification renders through swiftshader, which **undersells UnrealBloom**. A scene
tuned to look right in headless screenshots blooms into a smear on real hardware — the probe
shell had to be tamed (fresnel c 0.35, alpha 0.5) after the first on-hardware session. Law:

1. **Tune conservative.** Emissive intensities, fresnel alphas, and bloom-adjacent opacities are
   set to the LOW end of acceptable in headless review.
2. **Hardware is the judge.** No brightness/bloom value is final until seen on a real GPU in
   Luis's browser; the headless pass (09_PRODUCTION.md) verifies layout, state, and honesty —
   never final glow.
3. **The bloom pass itself is locked** at (0.65, 0.4, 0.5) with ACES exposure 1.1. Brightness
   problems are fixed at the emitter (material intensity), never by re-tuning the pass — one
   global bloom, many disciplined emitters (01_WORLD.md one-atmosphere law).

---

## 9. The stillness law `[BUILT]`

**The idle world is near-still. Motion means something happened.**

If the player parks the probe and nothing is occurring in the entity, the frame must be almost
static — so that when a plant flashes or a feed line lands, it is unmissable. The permitted
idle motion inventory is closed:

| Always moving (sub-threshold, the "alive-idle" signature) | Rate |
|---|---|
| Sky amber horizon breath | 0.10–0.18 over ~20 s |
| Beacon pulse (the one lit objective — the single deliberate attention magnet) | ~2.1 s period |
| Dust drift in the camera box | fractions of a unit/s |
| Probe self-rotation + trail | constant, it is the player's body |
| Presence segments idle sine | ~8 s period |

Everything else — emissive flashes, feed lines, chirps, ember bursts, map pips — fires only on
a logged real event. Additions to the idle inventory require amending this table; "ambient
activity" loops, scripted flickers, and fake traffic are banned by name (00_VISION.md
section 5).

Timescale corollary `[BUILT]`: opening the PROBE OS eases world time to **0.12, never 0**
(τ via dt·5). The world must never fully freeze, because the entity underneath never stops —
the beacon still breathes at 12% speed behind the map. Pausing the world would be a lie about
the system; slowing it is the truth about attention.

---

## 10. Governance

This chapter is the source for all motion, timing, camera, and audio decisions below it.
01_WORLD.md executes the atmosphere inside these laws; 02_MECHANICS.md and 03_MISSIONS.md may
add event classes only through the juice budget (section 5); 04_FUI.md styles the voices this
chapter allots; 05_TECH.md implements the springs and clamps quoted here; 09_PRODUCTION.md
verifies feel claims on hardware per section 8. A lower chapter contradicting a constant here
is wrong until this chapter is amended; amendments to sections 2.2, 4.3, and the [DECISION-LUIS]
items are Luis calls.

## Changelog

- 2026-07-20 — v1. Authored top-down from world.html on disk; every constant quoted from code;
  derived quantities (terminal ≈ 30 u/s, τ values, glide times) computed from those constants;
  GPU lesson carried from the in-code comment dated 2026-07-20.
