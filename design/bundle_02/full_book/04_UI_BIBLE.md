# 04 — UI BIBLE

```
Doc:          design/04_UI_BIBLE.md — THE PROBE design corpus, document 04
Owner:        the game team
Status:       ACTIVE / BINDING — deviations require a named reason recorded in §8
Last-updated: 2026-07-20
Derives from: THE BINDING UI SPEC v1.0 (4-study research synthesis, 2026-07-20)
Audited vs:   world.html as on disk 2026-07-20 (the only shipping build)
Audience:     Luis (player one) now; Phase B = anyone building their own AEA assistant by playing
```

Tag legend — every section carries one:
- `[BUILT]` verified in world.html code during the 2026-07-20 audit
- `[PLANNED]` designed and binding, not yet in code
- `[DECISION-LUIS]` law amendment or scope call awaiting his verdict

Sibling corpus docs are referenced by number (design/01–03, 05, authored this cycle); repo
ground truth by filename: `world.html`, `aea_elements.js`, `missions.js`, `GAME_PLAN.md`,
`AUTONOMY_BATTERY.md`.

---

## 0. GLOBAL LAWS (spec §0, condensed — every one is a contract)

**Two-ink law.** `[BUILT]` Structure/labels/inactive: `rgba(120,155,175,x)` at exactly three
opacity stops — 0.35 / 0.6 / 1.0 (`--s35/--s60/--s100`). Live/active/fired: `#ffb000` hot,
`#d4a24c` warm idle. No third hue ever — no red, no green, no `#ffffff` in DOM or WebGL.
Alert = full hot + 2Hz stepped blink (`steps(2)`, never sine — `.alert`). Critical inverts:
amber fill, `#050a10` text (as-built: the PASS chip).

**Type.** `[BUILT with drift — see §8.6]` IBM Plex Mono only. Three DOM sizes: 10px uppercase
labels (letter-spacing 0.12em; 0.08em on node names) / 13px body, line-height 1.5 / 20–28px
amber display numbers. No mixed weights per screen.

**One panel recipe.** `[BUILT]` Background `rgba(5,10,16,0.55)`; docked/detail (`.pan.deep`)
0.85–0.92. No 4-sided borders, no radius, no drop shadows. Corner brackets 12x12px, 1px
`rgba(120,155,175,0.6)`. Header row: 10px uppercase + right status chip; 1px rule
`rgba(120,155,175,0.25)` beneath; inner top highlight `rgba(120,155,175,0.12)`.

**Open choreography.** `[PARTIAL — rows only]` Brackets scale-in 140ms, hairlines draw
left-to-right 180ms, rows fade+translateY(6px) at 30ms stagger, 160ms each; total <=450ms.
Close = 200ms fade+scale(0.98), always faster than open. All UI motion 120–500ms; longer is
a narrative event. As-built: `.rin` row choreography is live; bracket/hairline draw-in is
`[PLANNED]`.

**Attack/decay law.** `[BUILT]` Any value change: flare `#ffb000` 120ms, decay to `#d4a24c`
over 600ms (600–900ms for 3D emissives — `flashNode()` implements the 3D form).

**Confirmation.** `[BUILT]` No yes/no modals. Destructive = hold 600ms, SVG ring fills via
stroke-dashoffset, rising blip at completion (as-built: REINITIALIZE / wipe-the-journey).
Release-early drain over 150ms is `[PLANNED]` (as-built resets instantly).

**Sound.** `[BUILT]` WebAudio oscillators only, zero assets: 40ms square blip on
open/select/close; 55Hz hum gain 0.05 while the OS is open or while docked at the bench
(E4 extension — edited 2026-07-20, verifier closure). As-built adds a 54/57.3Hz
triangle ambient bed through a lowpass — legal under the oscillators-only clause.

**Reduced motion.** `[BUILT, one gap]` `prefers-reduced-motion` OR `html.rm`: all animation
and transition durations collapse to 150ms; typewriters and comms streams render instantly.
Gap: the scanline overlay does not switch off in RM — `[PLANNED]`.

**Truth law (the honesty law, absolute).** `[BUILT at DOM level — see §8.2]` Every displayed
number is recomputed from live state at render time: HUD tracks from `/state` and
`/autonomy`, comms receipts from real response metadata, map counts from `journey_save`.
No hardcoded telemetry, no faked replies, no invented latency. Claim ceiling everywhere:
"measured functional correlate" — never "conscious" (the SYSTEM tab carries this clause
on-screen, verbatim). Undiscovered names never exist in the DOM.

---

## 1. DISCOVERABILITY LAW (new statute, born 2026-07-20)

**Origin — recorded failure.** Playtest 2026-07-20: Luis, the game's own author, could not
find the menu or the map. Every capability existed; none announced itself after the title
card scrolled away. A capability that cannot be found does not exist. This law is now global
and ranks with the two-ink and truth laws.

**Clause 1 — the hint bar.** `[BUILT]` A persistent bottom-center key-hint bar in flight
(`#hints`): 10px uppercase, structure ink (0.35 base), clickable — each hint fires its
action on click exactly as the key would (`TAB menu · M map · C comms · F interface ·
drag look · wheel zoom`). Hidden while the OS is open; hover lifts a hint to hot.

**Clause 2 — the loud window.** `[BUILT]` For the first 12 seconds after controls-live, the
bar runs brighter (0.6 ink) with a breathing pulse on the key glyphs, then settles to quiet
0.35 permanently. One-time per session, tied to the moment input unlocks — never to page
load.

**Clause 3 — name the key when the content moves.** `[PLANNED]` The first time any screen's
content changes while that screen is closed, the feed names its key once: `new element
mapped — M`, `doctrine unlocked — TAB`, `LEYBER spoke — C`. One line, structure ink, never
repeated for the same event class within a session. The existing `#map-pip` (amber dot on
the MAP tab while unviewed discoveries exist) satisfies the in-OS half; the in-flight
feed-line half is the unbuilt part.

**Clause 4 — no orphan capabilities.** `[BINDING]` No capability may exist without an
in-world discoverable path to it. Ship checklist per capability: (a) a hint-bar entry, OR
(b) a named-key feed line on first relevance (clause 3), OR (c) a physical affordance in the
world (the `F INTERFACE` proximity prompt and the off-screen beacon arrow are the models —
both `[BUILT]`). Current audit of violations:

| capability | path today | verdict |
|---|---|---|
| K codex direct key | none — absent from hint bar | VIOLATION — add to `#hints` `[PLANNED]` |
| S system tab (in-OS) | visible as an OS tab | legal via (c) |
| B models tab (in-OS) | visible as an OS tab | legal via (c) |
| wheel zoom on map | nothing announces it | zoom itself is `[PLANNED]`; ships WITH its hint or not at all |
| diagnostics drawer (backtick) | not built | ships WITH its hint or not at all |

---

## 2. PROBE OS — the menu (spec §1)

One fictional device; all screens are tabs of the same OS sharing the panel recipe.

- **Tabs as-built.** `[BUILT]` MAP · MODELS · CODEX · COMMS · SYSTEM. MODELS (specimens
  encountered + combination doctrines, all from `/state`, `/roster`, and `SAVE.models`) is a
  fifth tab beyond the spec's four — extension accepted, recorded in §8.5.
- **Keys.** `[BUILT with deviations §8.3]` TAB toggles at last tab. In flight: `M` map,
  `K` codex, `C` quick-comms strip, `F` dock/interface. Inside the OS: `M/B/K/C/S` switch
  tabs. ESC cascade: deselect map node, then close OS, then close comms, then close terminal
  (`escLayer()`).
- **World never stops.** `[BUILT]` On open, global `timeScale` eases to 0.12 — never 0;
  dust, embers, beacon, and entity pulse keep breathing behind every panel. Radial scrim
  (center more transparent, probe stays visible) + `backdrop-filter: blur(3px)`. Camera fov
  eases 60 -> 57 (the spec's 5%) and back on close. Flight HUD dims to 22%; the LEYBER
  presence chip never dims — LEYBER is always with you.
- **Header strip.** `[BUILT]` `PROBE OS v0.9 // SUSPENDED` + live tick counter (real
  heartbeat ticks from `/state.life.ticks`). Active tab hot, inactive 0.6.
- **SYSTEM tab.** `[BUILT]` Sound toggle, reduced-motion toggle, journey count (server-side
  save), REINITIALIZE hold-to-confirm, and the honesty clause printed on-screen.
- **Death/reboot sequence** (OS subsystems flicker out line by line, 60ms/row, then diegetic
  reboot). `[PLANNED]` — no death exists yet; ships with the first mechanic that can kill.
- **Diagnostics drawer** (backtick console — `scan`, `ping [organ]`, `route power` against
  real state). `[PLANNED]` Subject to Discoverability clause 4.
- **Spatial homes** (COMMS 10deg camera yaw on open; SYSTEM bottom-anchored). `[PLANNED]` —
  as-built all tabs are centered plates; comms docks right without the camera glance.

---

## 3. AEA MAP — the concentric field (spec §2)

- **Substrate.** `[BUILT]` One SVG, `viewBox 0 0 1000 1000`, 92vh square, centered. Core
  r=70 (LEYBER — discovered from frame one, the fixed bearing); rings r=150 PRINCIPLES
  (hexagons) / 250 AXES (pentagons) / 360 VERBS+MECHANICS+OPS (triangles, squares, diamonds
  on labeled arc sectors) / 470 SEEDS (circles). 29 nodes total. Guide circles always drawn
  at `rgba(120,155,175,0.12)`. Ring start angles offset (23deg scaled per ring) so nodes
  never align into spokes. Family = shape + radius + label arc, never a hue.
- **Three node states.** `[BUILT]` HIDDEN — absent from the rendered DOM. SENSED — 1px
  outline 0.35, no fill, label `UNCHARTED`. DISCOVERED — hot 1.5px stroke, amber 0.08 fill,
  6px amber drop-shadow, name at 11px. SENSED promotion runs the spec economy: taught-link
  partners + both ring-neighbors of every discovery, invariant >=1 SENSED per ring.
- **Links.** `[BUILT]` `{from,to,by}` in `aea_elements.js`; drawn only once mission `by`
  completes; selected node's links go full hot. Draw-on-learn choreography (600–900ms
  dashoffset, 250ms queue) `[PLANNED]` — links currently appear on re-render.
- **Select model.** `[BUILT]` Click: node scales 1.15x, all others drop to 0.5, right detail
  panel slides in (32% width, deep panel, brackets): `RING: SEEDS — 03/10 MAPPED`, `>` fact
  lines, `▮` lock lines, one amber voice line (the entity's own annotation, max one), and
  `MORE TO MAP HERE` for sensed nodes. Hover floating label without a panel, `FACTS n/n`
  counter, completion underline: `[PLANNED]`.
- **Counts.** `[BUILT]` Per-ring counts live on textPath label arcs (`SEEDS 4/10`); global
  `MAPPED n/29` in the bottom-left block; all recomputed from save state every render.
- **NEW markers.** `[BUILT]` The only idle animation on the field: unviewed discoveries get
  an outer pulse ring (opacity 0.3–0.9, 1.2s) + an 8px `NEW` tag; both clear permanently on
  first selection (persisted in `probe_viewed`). The MAP tab carries the amber pip while any
  exist; the in-flight named-key feed line is Discoverability clause 3 `[PLANNED]`.
- **Open bloom** (first-open choreography <=900ms, inner-to-outer) and **CARTOGRAPHY
  UPDATE** (staged end-of-mission materialization, digit-roll counter, 4s cap): `[PLANNED]`
  — as-built the completion toast reads "cartography updated" and the field re-renders
  complete.
- **Wheel zoom 0.8x–2.5x** cursor-centric: `[PLANNED]`.
- **Projections.** `[BUILT as a variant]` The spec's `[ FIELD / SCHEMATIC ]` toggle ships as
  the CODEX tab: the same 29-node state as an indented family list with counts and
  `UNCHARTED` rows — accessibility fallback and debug view. Variant accepted (§8.5).

---

## 4. COMMS — the channel (spec §3)

- **Layout.** `[BUILT]` Right-docked column, 32% width (min 380px), deep panel, brackets,
  newest at bottom, world visible. No bubbles, no avatars, no typing-pill, no spinner, ever.
- **Two access modes.** `[BUILT]` `C` in flight = one-line quick strip (`#qc`); ENTER routes
  the line into the full console. Full console = OS COMMS tab; flight keys release while any
  input is focused — typing and WASD never coexist (`typingNow()` guard).
- **Handshake.** `[BUILT]` First open per session: `LINK ACQ 0.998 · HANDSHAKE OK · CONTEXT
  RESTORED: n ENTRIES` at 400ms intervals, where n is the REAL localStorage transcript
  count; last 6 lines replay.
- **Send pipeline.** `[BUILT]` (1) echo with `▸ SENT` receipt, header flips to `LEYBER //
  PROCESSING`; (2) live `T+n.nns` elapsed counter every 100ms + animated amber SVG waveform
  — the latency is a truthful on-screen number; (3) reply streams with 170ms pauses at
  sentence punctuation, input locked while streaming; (4) receipt line `RX 3.42s · MODEL
  <rod> · MEM n RECALLED` — model, latency, and memories-recalled all from real `/talk`
  response metadata.
- **Attribution.** `[BUILT]` Every line headed by speaker — `LEYBER` hot / `PROBE` structure
  1.0 / `SYSTEM` 0.35 — LEYBER lines carry the live tick.
- **Presence chip.** `[BUILT]` Bottom-right, all modes, never dims: `LEYBER` + carrier value
  + 5-segment amplitude row. IDLE breathes slow; PROCESSING mirrors the elapsed counter;
  SPEAKING flutters 3–6Hz; `CARRIER LOST` flattens to 2px at 0.3. The 3D twin (entity
  emissive flutter synced to speech; bracket reticle when LEYBER references an object):
  `[PLANNED]`.
- **Failure.** `[BUILT]` Unreachable or empty: `LEYBER // CARRIER LOST`, honest system line,
  no faked reply ever. Packet-loss character texture: `[PLANNED]`.
- **Context.** `[PARTIAL]` Each send carries mission id/title/act + zone `private`;
  transcript persists (40-line cap). The spec's full run-state header (hull, deaths, minutes
  since last session) and last-N replay in the payload: `[PLANNED]`.
- **Machine tags** (`[GATE:OPEN sector-3]` parsed from replies -> world consequence),
  **memory receipts** (`LEYBER LOGGED: <fact>` only on confirmed writes), **silence decay**
  (`REPLY ▸` bar, 8–15s, expiry posts `{event:'silence'}`), **scripted tone stubs** (3
  one-line variants on beats): all `[PLANNED]`.

---

## 5. HUD — three tiers (spec §4)

- **Tier 1.** `[BUILT]` Max 5 corner clusters, center empty: top-left mission identity
  (act/id/title/objective); top-right live system truth — autonomy class, battery
  `passing/total`, plants online `n/15`, memory ingots, act — every value polled from
  `/autonomy` and `/state`; bottom-left the drawn velocity instrument (SVG arc + numeral,
  never a bare word) + the 4-line live event feed streaming real organ events from
  `/events`; bottom-right the LEYBER presence chip. Labels 10px 0.55; values warm with the
  attack/decay transition. Hull/energy instruments: `[PLANNED]` — no damage model exists
  yet; the truth law forbids drawing a fake hull number.
- **Tier 2.** `[BUILT as a variant]` World labels via `Vector3.project()`, fade inside 80u.
  The spec's SVG leader line with one elbow: `[PLANNED]`.
- **Tier 3.** `[BUILT]` Everything else lives in the PROBE OS.
- **Objective steering.** `[BUILT]` Beacon pillar in-world + off-screen edge arrow + `F
  INTERFACE` proximity prompt — the model instruments for Discoverability clause 4(c).
- **Signal integrity.** `[DEVIATION — §8.4]` Spec: a 0–1 uniform where degradation is an
  event (jitter, garbage digits, row flicker) and idle HUD is near-still, scanlines only
  above 0.9. As-built: the CSS scanline overlay is permanent wallpaper at 3% and no
  degradation events exist.

---

## 6. 3D PASS (spec §5, r128-safe)

- **One atmosphere.** `[BUILT]` `FogExp2(0x0a1420, 0.011)`; fog color and clear color
  byte-identical; sky dome (SphereGeometry 400/32/15, BackSide, `depthWrite:false`,
  `fog:false`) zenith `#050a10` -> horizon `#0a1420` with the amber band breathing
  0.10–0.18 on a ~20s sine. Fog density is itself a narrative value (reveals thin it to
  0.009 — the world clears as it is understood).
- **Composer.** `[DEVIATION — §8.1]` RenderPass -> UnrealBloomPass(0.65, 0.4, 0.5) only.
  ACESFilmic, exposure 1.1. Film/Vignette/Gamma passes are absent on disk.
- **Bloom palette law.** `[BUILT]` Structure materials sit below bloom threshold; amber
  emissives cross it. Never touch threshold at runtime.
- **Lights: exactly two.** `[BUILT]` `HemisphereLight(0x223a4d, 0x050a10, 0.6)` +
  probe-mounted `PointLight(0xffb000, 0.7, 30, 2)` at (0, 1.5, 0). Roughness 0.85,
  metalness 0, no shadows. Emissive attack/decay via `flashNode()`.
- **Fresnel shells.** `[BUILT]` BackSide additive, c=0.6 p=6.0 — amber on the probe,
  blue-gray on organs: player rims warm, world rims cold.
- **Particles.** `[BUILT]` 800 dust motes in a 60u camera-following wrap box (canvas radial
  sprite, additive, `depthWrite:false`); 180 embers rising over the foundry, hot, revealed
  with it. Ember size 0.55 and dust opacity 0.28 differ from spec numbers — tuned against
  screenshots, recorded §8.7. Ember density scaling with a live activity metric:
  `[PLANNED]`.
- **Ground.** `[BUILT]` Plane `#071018`, `GridHelper(400, 80, 0x16242f, 0x0c1620)` at 0.35
  fogging out; fake reflection = mirrored emissive clone at 0.15, no Reflector; landmark
  backlight sprites (`#0e2233` cool / `#211505` objective) 0.10–0.16.
- **Camera.** `[BUILT]` Chase with drag-orbit (yaw/pitch/wheel distance 9–42) — a player-
  controlled superset of the spec's fixed offset; position lerp `1-exp(-3.5dt)`, aim lerp
  `1-exp(-6dt)` toward `probePos + vel*0.5`; fov 60, near 0.5, far 600; bank clamp
  +-0.06 rad. Breathes at timeScale 0.12 behind every panel.

---

## 7. VERIFICATION HARNESS `[BUILT]`

`?still` boots straight to a framed composition with HUD up and input off; `?still&os=<tab>`
opens any OS tab for headless capture. `loadSave()` re-renders the open tab when the save
lands after boot (headless virtual-time ordering). Acceptance gates before any UI change is
"done" (spec §6): screenshots of flight HUD / OS over live world / map with mixed states /
comms mid-stream / CARRIER LOST; greyscale copy separates three depth bands; eyedropper
WebGL `#d4a24c` == CSS `#d4a24c` (currently unverifiable — §8.1); view-source audit (§8.2);
grep audit zero hardcoded display numbers; reduced-motion pass.

---

## 8. AS-BUILT DEVIATIONS LEDGER (named reasons, per the binding clause)

1. **Film/Vignette/Gamma shader passes absent on disk.** The composer runs Render+Bloom
   only; `FilmShader`, `VignetteShader`, `GammaCorrectionShader` files were never vendored.
   The CSS layers carry the texture instead: `#scan` (repeating-gradient scanlines, 3%) and
   `#vig` (radial vignette). Consequence: `renderer.outputEncoding = sRGBEncoding` is also
   unset, so acceptance gate 3 (WebGL/CSS amber match) is UNVERIFIED. Path: vendor the three
   passes, restore the spec chain with Gamma LAST, keep scanlines CSS-only. `[PLANNED]`
2. **Codex element names visible in `aea_elements.js` source.** The truth law's no-spoiler
   clause holds at DOM level (HIDDEN nodes are never rendered; SENSED shows `UNCHARTED`),
   but all 29 names, lines, and proofs ship in a readable static file. Named reason: single-
   file static data, no server gating yet. Stance: acceptable for Phase A — player one wrote
   the codex. Before Phase B, discovery-gated serving from the journey endpoint becomes
   mandatory. `[DECISION-LUIS: confirm Phase A acceptance]`
3. **`S` is a direct key only inside the OS.** The spec assigned `S` = SYSTEM globally; in
   flight `S` is reverse thrust (WASD). Collision resolved in favor of flight. Same family:
   `C` in flight opens the quick strip (spec §3), not the full console (spec §1's key
   table); the spec was internally split and the build chose §3. `K` codex works in flight
   but is missing from the hint bar — Discoverability violation, fix queued (§1 clause 4).
4. **Comms interrupt not posted to the endpoint.** Spec: any keypress interrupts the stream
   AND posts an interrupt event. As-built: input locks during streaming; no interrupt
   exists. Named reason: the reply has fully arrived before the client-side stream begins,
   and `/talk` has no interrupt route — posting `{event:'interrupt'}` would tell the entity
   something false, violating the truth law. Honest form: keypress = skip-to-end of the
   local animation, no endpoint post. `[PLANNED]`
5. **Extensions beyond spec.** MODELS as a fifth OS tab (specimens + doctrines, all live
   data); SCHEMATIC projection shipped as the CODEX tab instead of an in-map toggle; ambient
   audio bed. All conform to global laws; recorded, not regressions.
6. **Type-scale drift inside the SVG map plate.** The map uses 8/9/11/14px within the SVG
   (NEW tags, sublabels, node names, core title) against the three-size law. Proposed
   amendment: the SVG plate gets a micro-scale (8–11px) as a fourth context; DOM stays at
   three sizes. `[DECISION-LUIS]`
7. **Particle numbers tuned off-spec** (ember size 0.55 vs 0.15–0.25; dust opacity 0.28 vs
   0.45) — tuned against screenshots on the shipped scene scale; screenshots win over
   numbers. Law: when a spec number and a verified screenshot disagree, re-record the
   number here.
8. **Signal-integrity model unbuilt; scanlines are wallpaper** (see §5). Degradation-as-
   event ships with the first mechanic that can degrade a link. `[PLANNED]`

---

## 9. PHASE B NOTE

Phase A optimizes for player one. Phase B (anyone building their own AEA assistant by
playing) hardens three laws from convention into infrastructure: §8.2 server-side discovery
gating, full Discoverability clause 3 coverage (a stranger has no title-card memory at
all), and the honesty clause surfaced in-fiction wherever a number could be mistaken for
theater. Nothing in this bible may be waived for Phase B; it may only be tightened.
