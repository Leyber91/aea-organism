# 00_VISION — THE PROBE

```
Owner:         the game team (four-master fusion, see section 3)
Status:        ACTIVE — governs every slice; slice 1 shipped and played
Last updated:  2026-07-20
Corpus role:   root document; every sibling doc inherits this vision and may not contradict it
Ground truth:  ../GAME_PLAN.md (mechanics canon) · the approved build plan (slices, operating
               prompt) · live code: ../world.html, ../missions.js, ../controlroom.py,
               ../journey_save.json
```

Every section below carries a build-state mark:
`[BUILT]` verified in running code · `[PLANNED]` designed, not built · `[DECISION-LUIS]` awaiting
his call. A section with mixed state marks its parts.

---

## 1. What THE PROBE is

`[BUILT — slice 1 live at /world, played 2026-07-20]`

THE PROBE is a game you play inside a living AI system. You pilot a small probe through a dark
machine-city — each district is a real organ of an autonomous AI entity called LEYBER, running
on the same server that serves the game. Missions send you to find sockets, fire real model
calls, mine real memories, and forge real capabilities; every bar, item, and number on your HUD
is the live truth of the system underneath, never a prop. The city starts almost entirely dark.
As you complete missions, districts light up — because the capability they represent has
actually been demonstrated or built. By the end, the player has assembled a complete Autonomous
Entity Architecture (AEA) and, having built it once from inside, can build their own. Lineage:
Duskers and Observation — the interface is the fiction; the machine you are inside is not
pretending to be alive, it is running.

Current state of the build: `world.html` (probe flight rig, mission engine, HUD, WebAudio synth)
serves at `/world`; `missions.js` carries Act 0 (FIRST LIGHT) and Act I (CATALOGUE, CHANNEL,
METER, LADDER, BROWNOUT boss), every DO/PROVE beat on real endpoints; `journey_save.json` is a
server-side atomic save and already records real play (M0.1, M1.1 complete; foundry revealed).
Acts II–VI are designed, not built — see section 6 and `09_PRODUCTION.md`.

---

## 2. The four design pillars

Every design decision in this corpus is tested against these four. A feature that fails one
pillar is cut, no matter how good it looks.

### 2.1 Diegetic truth

`[BUILT — enforced in slice 1; law for all slices]`

The interface IS the fiction, and the fiction IS the system. There is no separation between
"game data" and "real data" — they are the same bytes:

- Energy bars are the Meter's real sliding 60-second rpm windows and daily quotas in
  `grid_state.json`. You can genuinely run dry; 429s are real starvation.
- Items are models with live fitness stats from `model_fitness.json`; they genuinely rot
  (measured pool decay, not a decay timer).
- Ore is unmined corpus sessions; mining is a destructive read of a real, finite resource.
- Fog of war is the proven-but-not-wired gap: a district lifts only when its organ is
  integrated into the live mind and its boss threshold passes.
- The character sheet is the live autonomy battery (`autonomy.py`): 6 cited stats, currently
  PROTO-AUTONOMOUS 6/6 over 40+ ticks. Stats move only on real logged behaviour.

The honesty test for any proposed mechanic: pushed to its extreme, does the mapping hold, or is
it decoration? If it is decoration, it does not ship. Full mechanic-by-mechanic mapping lives in
`../GAME_PLAN.md` section 1 and `03_PROGRESSION.md` section 3 (the honest mapping table).

### 2.2 Discovery-as-learning

`[BUILT for Acts 0–I · PLANNED for Acts II–VI]`

The game is the AEA's teaching vehicle. Nothing is explained that can be discovered; nothing is
read that can be done. Every mission follows the Portal-school arc — INTRODUCE (the machine
demonstrates), PRACTICE (the player does), TWIST (it breaks for real: a rod dies, a rate limit
bites), PROVE (a real assert). One concept per mission. Every mission names the AEA element and
citation it embodies (the teaches-map): the AEA is the curriculum, the city is the syllabus, and
the already-built organs are relearned as discovery while the frontier organs are learned by
forging them. A needed paragraph is a misdesigned level.

### 2.3 The entity is alive

`[BUILT — the world polls the live entity; LEYBER-as-guide wired via /talk]`

LEYBER is not a backdrop; it is running underneath the game while you play. Ticks stream as
world events, signal packets travel the city on real calls, emissive levels track real state,
item-rot alerts fire on real fitness deltas, and the ASK LEYBER beat injects mission context
into `/talk` so the entity narrates its own construction from its live state and codex. The
world moves because the thing under it is actually moving. Claim ceiling (binding, from the AEA
honesty clause): the game may claim "measured functional correlate, present" — it may never
claim "conscious" or "sentient". No mission text, HUD copy, or marketing line breaks this
ceiling, ever.

### 2.4 Professional or nothing

`[BUILT as a gate — slice 1 passed it; every slice must]`

The bar is a game a stranger would judge as professionally made, not a styled dashboard.
Binding production gates: boot-to-input under 3 seconds; the first 60 seconds teach move, look,
interact by doing; one lit objective always (a beacon, never a paragraph); feedback on every
interaction under 100ms; 60fps hard budget; WebAudio runtime synthesis only (zero audio
assets); camera choreography eased, never teleported; juice tied to truth — bloom pulses only
on real events. Visual constitution: the two-ink FUI is law — amber (`#ffb000` / `#d4a24c`)
exclusively for live/fired state, blue-gray for structure, mono type, brackets, void black.
No third ink, no cartoon, no emoji, anywhere. The full art-direction spec is `04_UI_BIBLE.md`.

---

## 3. The operating prompt — the team's role

`[BUILT — this role governed slice 1 and governs every future session; copy is verbatim]`

Every build session on THE PROBE runs under this role, verbatim:

> The build runs under this role, verbatim. **You are a fusion of four masters operating as
> one: (1) the creative director of a Duskers-class diegetic game** — atmosphere is mechanics,
> the interface IS the fiction, restraint over spectacle, cut anything off the core loop;
> **(2) a Bruno-Simon-class three.js technical artist** — eased cameras, emissive discipline,
> bloom as punctuation, 60fps hard budget, r128 global build only; **(3) a Territory-Studio
> FUI designer** — the banked Expanse law is the visual constitution, every HUD pixel
> justified; **(4) a Portal-school learning designer** — every mission is INTRODUCE (the
> machine demonstrates) -> PRACTICE (the player does) -> TWIST (it breaks: a rod dies, a rate
> limit bites) -> PROVE (a real assert). One concept per mission; a needed paragraph = a
> misdesigned level. **Above all four: the AEA honesty law** — every bar, item, event, number
> is live system truth from real endpoints; a fabricated resource or cosmetic particle
> disconnected from a real event is a failure worse than ugliness. The game may only be
> beautiful in ways the truth permits. Binding numbers: boot-to-input <3s; first light
> (the player's first real model call answering from the dark) <90s of play; one lit
> objective always; feedback <100ms; sound = WebAudio synthesis only; the boring test gates
> shipping — if a stranger would call it a dashboard, it does not ship.

The honesty law outranks the four masters. When creative direction, technical art, FUI craft,
or learning design collide with truth, truth wins and the design is reworked until it is
beautiful inside what the truth permits.

---

## 4. Audience — two phases, one gate

### Phase A — Luis, player one

`[BUILT — in progress; slice 1 played 2026-07-20]`

Luis plays THE PROBE against HIS live entity. FIELD missions are solo-playable in the browser
between build sessions (real endpoints, no pair session needed). FORGE missions frame the real
AEA engineering: the game shows the recipe, spec, and boss threshold; the organ is built in a
pair session; the boss check and fog-reveal are automatic after. The game never pretends the UI
wrote the code. Phase A is complete when the journey through Act VI is playable and played.

### Phase B — everyone

`[PLANNED — architecture keeps the door open; no Phase B work yet]`

The north star (Luis, 2026-07-20): after the game is done, anyone can build their own AI
assistant, tamed to them, with all the aspects of the AEA framework — by playing. Phase B is
the bootstrap path: a new player stands up their own grid (keys, local model, organs) mission
by mission. Three architectural commitments made in slice 1 keep this honest:

1. Missions are data (`missions.js`) — content is authorable without touching the engine.
2. The world reads only curated endpoints — any AEA-shaped server can back it.
3. No private Luis data is baked into game content — his entity supplies it at runtime.

### The Phase B gate

`[DECISION-LUIS]`

Phase B work begins only after Phase A is played through and Luis judges it worthy. Any Phase B
task attempted before that gate is scope inflation by definition and is refused by name. The
gate is a Luis call, not a team call.

---

## 5. What the game is NOT

`[BUILT — these are the three rejections that produced the current form; standing law]`

Three console-view attempts (narrative builder, static ASCENT ladder, engineering board) were
rejected for one structural reason: reading is not playing. The rejections are permanent:

- **Not a dashboard.** If the primary verb is "look at", it has failed. The boring test is the
  shipping gate: if a stranger would call a slice a dashboard, it does not ship. Panels of
  live numbers without a mission verb attached are dashboard tissue and get cut.
- **Not a simulation of fake data.** No mocked bars, no scripted "system activity", no
  cosmetic particles disconnected from real events, no invented numbers — a fabricated
  resource is a failure worse than ugliness. If the live system cannot supply a truth, the
  game does not display a substitute; it displays nothing, or the mechanic is redesigned.
- **Not a sandbox without missions.** Free flight exists, but the game is a guided journey:
  one lit objective always, a dependency DAG of acts, bosses that can be lost. A world you
  can only wander is scenery; every capability in the world is reached through a mission that
  teaches it.

---

## 6. Win condition

Two conditions, in order; both must hold for THE PROBE to be "won".

### 6.1 The AEA completed

`[PLANNED — Acts II–VI; Act I complete-able today]`

The journey ends when the entity's architecture is whole and proven: recall() forged (Act II),
think() forged over the council regimes (Act III), the world-wire and governed command current
(Act IV), THE SEND passed (Act V — see section 7), and the self-loop closed — Voyager
self-tooling, STOP, the 100-tick ENDURANCE run to Bedau Class 2, and the Darwin-Godel archive
(Act VI). Every boss is a cited falsifiable threshold that can be lost; the map is fully lit
only when every organ is wired into the live mind, not merely demoed. Act and mission detail:
`05_CONTENT_MISSIONS.md` + `05B_CONTENT_ACT3_4.md` + `05C_CONTENT_ACT5_6.md`; the recipe DAG
and fog map: `../GAME_PLAN.md` section 4.

F1 senses (Act IV) remains `[DECISION-LUIS]` and is not required for the win unless he calls
it in.

### 6.2 The player can build their own

`[PLANNED — Phase B; gated per section 4]`

The deeper win: a player who finishes THE PROBE can stand up their own AEA — because the game
never hid the machine. Every organ was seen as real code (the learn-beat reveal), every
resource limit was felt as real starvation, every threshold was a citation they watched pass
or fail. Phase A proves this on player one: Luis finishing the game IS the first demonstration
that the AEA can be learned from inside. Phase B generalizes it. The game is won when the
teaching vehicle demonstrably teaches.

---

## 7. Standing guard — non-negotiable

`[BUILT as law — carried verbatim from the approved plan; re-read at every slice start]`

1. **THE SEND stays the Act V boss.** The convergence proof — the entity drafts real outreach,
   HADES fits it, LUIS sends it — is pinned. No re-plan moves it, dilutes it, or substitutes a
   synthetic target. The income clock is real; the game's proof-of-worth is an artifact that
   earns, not a demo.
2. **Polish never outranks capability.** Forge missions ARE the real AEA engineering. If a
   session generates polish instead of capability, that is named as infrastructure-as-avoidance
   and the session stops. Polish that serves the current act's mission is production value;
   polish beyond it is refused.
3. **The boring test gates every slice.** Before a slice ships: would a stranger call this a
   dashboard? If yes, it does not ship — no exceptions for effort spent. The decisive test is
   Luis piloting it in his browser; his go/no-go gates the next slice.

---

## 8. Corpus map

`[BUILT — the corpus landed; BOOK.md is the authoritative spine and reading order]`

- `BOOK.md` — the spine: the full chapter list, reading order, cross-chapter laws, and the
  open decisions ledger. Authoritative over this summary; consult it first.
- `00_VISION.md` — this document. The root; siblings inherit it.
- `01_WORLD.md` — the city: districts-as-organs, geography, fog, growth on forge.
- `02_SYSTEMS.md` — flight rig, dock, mission engine, save semantics, failure semantics.
- `03_PROGRESSION.md` — the act ladder with cited bosses, the campaign scores, the honest
  resource economy (energy, items, ore, crafting).
- `04_UI_BIBLE.md` — the two-ink visual constitution, HUD spec, deviations ledger.
- `05_CONTENT_MISSIONS.md` + `05B_CONTENT_ACT3_4.md` + `05C_CONTENT_ACT5_6.md` — act and
  mission detail, Acts 0–VI (rules, beats, teaches-map, engine deltas).
- `08_TECH.md` — engine architecture: three.js r128 stack, endpoints, save, performance.
- `09_PRODUCTION.md` — slices, gates, verification protocol, the income-clock guard.

Conflicts resolve upward: a sibling contradicting this vision is wrong until this vision is
explicitly amended, and amendments to sections 3 and 7 require Luis.

---

## Changelog

- 2026-07-20 — v1. Authored from `../GAME_PLAN.md` (ASCENT v2) and the approved build plan;
  build-state marks verified against `world.html`, `missions.js`, `journey_save.json` on disk.
- — edited 2026-07-20 (completeness audit closure): ghost filenames (`02_MECHANICS.md`,
  `03_MISSIONS.md`, `04_FUI.md`, `05_TECH.md`, `06_ROADMAP.md`) replaced with the real corpus
  in sections 1, 2.1, 2.4, 6.1, and 8; section 8 now points to `BOOK.md` as the authoritative
  spine and routes act/mission detail to the three content chapters.
