# A6_GLOSSARY — THE PROBE · every term, its real referent

```
Owner:         the game team
Status:        ACTIVE — appendix; binds vocabulary across the whole corpus
Last updated:  2026-07-20
Corpus role:   appendix to the top-of-book chapters. One term, one meaning: a sibling chapter
               using a term differently is wrong until this glossary is amended.
Ground truth:  ../aea_elements.js · ../missions.js · ../GAME_PLAN.md · ../world.html ·
               ../controlroom.py · ../journey_save.json · ../PLAN.md · ../AUTONOMY_BATTERY.md
Siblings:      00_VISION.md · 01_WORLD.md · 02_SYSTEMS.md · 03_PROGRESSION.md ·
               06_MODELS_BESTIARY.md · 07_AUDIO.md · 08_TECH.md · 09_PRODUCTION.md
```

How to read an entry: **game term** — what it means in play, then the REAL system behind it.
Under the honesty law (00_VISION.md section 2.1) the two are the same bytes; the glossary names
the bytes. Entries describe systems that are [BUILT] unless tagged [PLANNED] or [DECISION-LUIS]
inline. Claim ceiling applies to every line here: "measured functional correlate, present" —
never "conscious", never "sentient".

---

## A

- **act** — one chapter of the journey, 0 through VI, closed by a boss that can be lost. Real referent: a stage of LEYBER's actual construction (Act I = the built grid, Act II = memory, Act V = THE SEND); the dependency DAG is GAME_PLAN.md section 4. Acts 0–I [BUILT]; II–VI [PLANNED].
- **AEA** — Autonomous Entity Architecture, the thing the whole game builds and teaches. Real referent: the proof taxonomy in `aea_elements.js` (5 axes · 10 seeds · 3 verbs · 4 mechanics · 4 ops · 3 principles, per AEA_PROOF_PLAN 2026-06-28), each element carrying the standalone script that proved it. The AEA is the curriculum; the city is the syllabus.
- **archive, the** — THE ARCHIVE district at (-92,-14), the memory mines, "the book of Luis"; spawned as a locked silhouette by the `archive_tease` reveal (Act I boss). Real referent: the raw session corpus plus `consolidate.py`, `luis_memory.json`, and the codex index. Playable in Act II [PLANNED].
- **axis** — one of the 5 AXES that locate an entity (PATH, MULTIPLICITY, ABSTRACTION, PROMPTING, ASYNC); ring 2 of the codex. Real referent: measured capability dimensions, each with a named proof script (`swarm.py`, `agent_tools.py`, `memory.py`, `relay.py`) in `aea_elements.js`.

## B

- **backwards channel** — seed.10: run A writes a memory capsule, run B reconstitutes it — continuity across runs. Real referent: `memory.py` vector-store recall.
- **beacon** — the 110-unit breathing light cylinder + ground ring marking the current mission node; the world's only diegetic quest marker ("one lit objective always", 00_VISION.md section 2.4). Real referent: a pointer to the current mission's `node` in `missions.js`, teleported by the mission engine in `world.html`.
- **beat** — the atomic mission unit in `missions.js`: `brief` (why, 3 lines) · `learn` (real code, typewriter reveal) · `do` (one hot verb firing a real endpoint) · `observe` (a live watcher on real state) · `prove` (a real assert) · `ask` (LEYBER commentary [PLANNED]). DO and PROVE always act on real endpoints — nothing simulated.
- **birth** — a specimen card appearing the moment a real discovery probe gets any response (06_MODELS_BESTIARY.md section 4, [PLANNED]); in Acts II+, a building rising when a real organ comes online in the entity (01_WORLD.md section 4.2, [PLANNED]). Law: nothing is ever born for a thing that does not exist.
- **bloom** — the UnrealBloom post pass (0.65, 0.4, 0.5) in `world.html`. Law: bloom pulses only on real events — juice tied to truth, never ambient fakery.
- **boring test** — the shipping gate: if a stranger would call the slice a dashboard, it does not ship (00_VISION.md section 7). Real referent: Luis piloting the slice in his browser; his go/no-go.
- **boss** — the act-closing PROVE with a cited falsifiable threshold that can genuinely be LOST. Real referents: the brownout drill (Act I), HADES fit-rate, Barandiaran/Bedau/Voyager/STOP/DGM thresholds (Acts III–VI). HADES holds junk at a 0.5 rate today — losing is real.
- **burn** — one lifetime real draw logged against a rod. Real referent: `energy.rods[].calls` sourced from `energy_usage.json`, surfaced as "N burns" on the specimen card.

## C

- **carrier** — the live link to the entity, surfaced on the presence chip: IDLE "CARRIER 0.998" · PROC · SPEAK · LOST. Real referent: `/talk` round-trips plus the `/state` and `/autonomy` polls; CARRIER LOST is a true failed-poll condition and is never faked over (02_SYSTEMS.md section 10).
- **class (autonomy)** — the entity's character class on the sheet. Real referent: the Bedau class from the live autonomy battery `autonomy.py` — currently PROTO-AUTONOMOUS, 6/6 cited tests over 40+ ticks; stats move only on real logged behaviour. HUD "class" reads `/autonomy`.
- **codex** — the PROBE OS reference screens (concentric MAP + element detail) for the AEA. Real referent: `aea_elements.js` (the proof taxonomy, ring geometry per BINDING UI SPEC v1.0 section 2) with discovery state from `journey_save.json`. Distinct from the entity's own archive-side codex index (`index_codex.py`).
- **comms** — the channel to LEYBER itself: the COMMS dock injects mission context and sends over `/talk`, zone always private; every reply renders a RECEIPT of real telemetry — latency, the model that actually served, memories actually recalled.
- **consolidation** — mining. Real referent: `consolidate --limit N`, a destructive read of raw corpus sessions into memory ingots in `luis_memory.json`. The vein is finite — the pruning disaster (~1,570 sessions lost forever) proved scarcity is real, not designed.
- **cooling** — a rod held out of the ladder after a real failure or 429. Real referent: `cooled_at` + `_cooling()` with `COOL_SECONDS = 900`; the amber COOLING tag on the specimen card is that clock, live.
- **council** — several diverse models voting on one task. Real referent: the measured regime law (doctrine THE DIVERSE COUNCIL): a hard or unreliable task is rescued by a diverse-model vote — the win is model diversity, not temperature (grid experiments v3: net +3, 0 damage); an easy task under a council gets WORSE (THE SOLO LAW). Act III forges `think()` over these regimes [PLANNED].

## D

- **dock** — pressing F at a lit node: flight pauses, the LEY//DOCK terminal opens, the mission's beats play. Real referent: the mission engine binding a `missions.js` node to its real endpoint; every verb inside the dock fires a real call.
- **doctrine** — a combination law of models, measured not invented: SOLO LAW, DIVERSE COUNCIL, LONE VERIFIER RISK, GENETIC RELAY, RAMIFICATION, CRYSTAL PATH (`aea_elements.js` doctrines[]), each carrying its evidence line. Locked doctrines reveal in later acts; none is ever authored without a measurement behind it.
- **draw** — one model call routed through the mouth; the unit of energy spend. Real referent: `energy.draw()` returning `ok/latency/text/tokens` plus the true `tried[]` list — the actual routing history of that call, shown to the player as-is.
- **drill** — the Act I boss action: four draws back to back, zero unhandled failures allowed (assert `drill_clean`). Real referent: live proof of restorable coherence — reroute, cool, fall to the floor, never break.

## E

- **embers** — 180 amber particles rising over the foundry. Opacity is progress-gated (0 dark → .4 at first light → .7 at foundry_full): even the particles obey the reveal law.
- **encounter** — the only way a model enters the bestiary: `encounter(plant, model)` fires on a successful real action, union'd with the entity's own lived draws (`/state → energy.rods` with `calls > 0`). If LEYBER burned a rod while the player was away, it is encountered — the world moves without you.
- **energy / mana** — the refill bars. Real referent: the Meter's real budgets in `grid_state.json` — sliding 60-second rpm windows plus daily quotas (00:00 UTC reset). You can genuinely run dry; a 429 is real starvation, not a mechanic.
- **entity** — the autonomous system actually running under the game: LEYBER's organs served by `controlroom.py` on the same server that serves `/world`. There is no separate "game state" — the entity's state IS the game state.

## F

- **field mission** — a mission Luis plays SOLO in the browser between build sessions: every DO/PROVE on existing real endpoints (`/api/node/run`, `/state`, `/talk`). No Claude session needed; what makes the game playable alone.
- **first light** — M0.1, and the moment it names: the player's first real model call answered from the dark (POST to the keyless socket; verified live 2026-07-20, "FIRST LIGHT", 200). Production law: under 90 seconds of play.
- **fog-of-knowledge** — the fog of war. Real referent: the proven-but-not-wired gap — organs demoed in 9 standalone scripts but absent from the live mind stay dark; a district lifts ONLY when its organ is integrated and its boss passes. The literal `FogExp2` also thins on reveals (0.011 → 0.009 at foundry_full) — brightening is always a reveal side-effect, never a lighting edit.
- **forge mission** — a mission whose DO is the real AEA engineering: the game shows the recipe, spec, and boss threshold; the organ is built in a pair session (Claude writes, Luis judges); the boss check and fog-reveal run automatically after. The game never pretends the UI wrote the code. First forge: recall() in Act II [PLANNED].
- **foundry** — the fifteen-plant power row at z=70 (01_WORLD.md section 2.1). Real referent: the `PLANTS` provider registry — one line per provider (base URL, auth, privacy ring, rpm) behind the one shared call path. Adding a plant is one line; that is what model-agnostic means.

## G

- **grid** — the whole substrate layer: PLANTS + `call_openai` + the Meter + fitness. THE GRID (caps) is specifically the nvidia plant — 121 models, 40 rpm each, the tallest tower in the row because it is the real capacity giant.

## H

- **HADES** — the verdicter. Real referent: `hades.py`, Law 3 made code — accept / redo / reground / halt on every autonomous output, deliberately heterogeneous rods (a verifier must be a DIFFERENT model than the worker — doctrine THE LONE VERIFIER RISK). Gates every craft and THE SEND. Real rate today: holds junk at 0.5.
- **hearth (ollama)** — the local Ollama plant: privacy ring `local`, rpm None — unlimited, slow, private. Real referent: `LOCAL_FLOOR` (three ollama rods) always appended to the ladder, the floor the mouth can always fall to; seed.9 routes ALL private work here and nowhere else.
- **honesty law** — the rule above the four masters: every bar, item, event, and number is live system truth from real endpoints; a fabricated resource or cosmetic particle disconnected from a real event is a failure worse than ugliness. Claim ceiling: "measured functional correlate, present" — never "conscious" or "sentient". Shipped as UI copy in the SYSTEM screen, not aspiration.

## I

- **ingot** — one consolidated memory fact in `luis_memory.json`. HUD "ingots" is the live memory count from `/state`. Produced by mining (consolidation), spent as grounding for recall() [Act II forge, PLANNED].
- **interactional asymmetry** — Barandiaran's autonomy test 5, self-initiated action (`AUTONOMY_BATTERY.md`). Current honest score: FAIL (heteronomous) — HADES enforces externally-authored laws the entity cannot alter; the trust ledger is operator-granted. An open finding the game reports, never papers over.

## J

- **journey, the** — the guided arc Acts 0–VI (GAME_PLAN.md, ASCENT v2); also the main window's name. Real referent: the mission engine over `missions.js` plus the save.
- **journey save** — `journey_save.json`: the server-side atomic save (`/api/journey`, merge + reset) holding mission completion, `SAVE.reveals`, and `SAVE.models` (encounters). Reveals replay idempotently on boot; real play is already recorded in it.

## L

- **ladder** — the fitness-ranked list of rods for a (tier, zone) that a draw falls down until something answers. Real referent: `energy.ladder()` — re-ranks itself from every call, skips cooling rods, refuses known-broken rods (reliability < 1.0, ollama excepted), always ends at the hearth.
- **LEYBER** — the entity itself: the living AI whose body is the city and whose construction the journey completes. Speaks only in first person, only via `/talk`, only from its live state and codex; the presence chip never dims because LEYBER is always with you. Named organs and laws: PLAN.md; voice register: 01_WORLD.md section 6.

## M

- **mapped** — a codex element in state `disc`: glyph filled, name + one-liner + proof script shown, LEYBER voice line earned ("this part of me is mapped. it was always running; now you can see it."). Real referent: the element's id present in the journey save's discovery state; counted live as MAPPED n/29.
- **mechanic** — the four seeds that also act BETWEEN ticks (CRYSTALLIZE, FLEXIBILIZE, SELF-VERSION, CEILING-DETECT — seeds 3/4/5/7), rendered as their own square nodes on ring 3 but discovered with their seed. Real referent: `aea_elements.js` mechanics[].
- **meter** — the grid operator. Real referent: `Meter.can_spend` — a locked read-modify-write on the ONE shared `grid_state.json`, so every process sees the same budget; the reason a 24/7 entity on free power never browns out a plant for every organ at once. In-world: the 14-unit hex obelisk at (+8, 56), M1.3.
- **mine / ore** — see consolidation; ore is unmined corpus sessions, a finite real vein, and mining is a destructive read.
- **mouth (energy.draw)** — the single entry point for every model call the entity makes: `draw(prompt, tier, zone)` falls down the ladder, skips cooling and unaffordable rods, returns the first real answer. Law it embodies: no organ names a model, ever — models are fuel, the mind is the structure.

## N

- **nexus** — THE ENERGY NEXUS at (0, ·, 26): icosahedron core, fresnel shell, counter-rotating tori — the in-world body of the mouth. M1.4 (THE LADDER) and the Act I boss both dock here. Relation to the spire site at (0,0): open, [DECISION-LUIS] D1 (01_WORLD.md section 8).

## O

- **op** — one of the 4 OPS (DESIGN, TIME, SHIP, LEARN), ring 3 diamonds: disciplines a run must satisfy. SHIP is unskippable — a run produces a REAL external artifact. DESIGN and TIME are honestly marked PARTIAL in `aea_elements.js`; the codex shows that, not a rounded-up claim.

## P

- **plant** — one model provider in the PLANTS registry (ollama, nvidia, groq, pollinations... 15 total), rendered as a power plant whose window emissive tracks real load: `0.9 + min(.6, rpm_now/rpm_cap)`. A busy plant visibly burns brighter; a keyless-dark plant is a real missing key.
- **presence chip** — the bottom-right LEYBER chip: name + carrier state + 5 signal segments; the one HUD element that never dims, even under PROBE OS. Real referent: live `/talk` and poll telemetry driving IDLE / PROC (waveform + 100ms stopwatch) / SPEAK / LOST.
- **principle** — one of the 3 PRINCIPLES (ring 1, hexes): EMERGENCE OVER IMPOSITION, RESTORABLE COHERENCE, OPERATOR-OBSERVABLE TIME — what emerges when the rest is real; each with a named proof script (`swarm.py`, `test_resilient.py`, `tracelog.py`).
- **probe, the** — the player's craft: flight rig (WASD+QE, drag look, chase cam) plus its own amber point light. Deliberately NOT an agent — the player is the probe's mind. Real referent: a browser client reading only curated endpoints; any AEA-shaped server can back it (the Phase B commitment).
- **PROBE OS** — the overlay OS (v0.9, TAB): MAP (the concentric codex), MODELS (the bestiary), SYSTEM tabs. Flight HUD dims to 0.22 beneath it; the presence chip stays. Real referent: the same live endpoints, re-projected as instrumentation.

## R

- **reveal** — `applyReveal(key)`: an idempotent mutation of the one persistent world (lights, labels, fog density, spawns) earned by a mission reward and saved in `SAVE.reveals`. Growth is data, not level-loading; the full built table is 01_WORLD.md section 4.1.
- **rod** — one `plant/model` pair the grid can burn; the atomic item of the game. Carries lived stats (burns, ok%, ema latency from `energy_usage.json`) and sweep stats (fit, tier from `model_fitness.json` / censuses).
- **rot** — measured decay of real models: fitness sweeps shrink the pool (2026-07-19: 44 → 29, perfect 7 → 2). Durability loss is measured, never simulated; there is no repair item — a rod heals only by really answering again, and the mouth routes around the dead meanwhile.
- **rpm window** — the sliding 60-second per-rod request window (`win(plant:model)`) in `grid_state.json` that `can_spend` checks. The refill animation on every energy bar is this window sliding — patience is a resource the entity budgets for you.

## S

- **seed** — one of the 10 SEEDS (ring 4), the organs: SUBSTRATE, SHARP OBJECTIVE, CRYSTALLIZE, FLEXIBILIZE, SELF-VERSION, SELF-MODEL, CEILING-DETECT, TRANSCENDENCE, BOUNDARY, BACKWARDS CHANNEL. Each carries the script that proved it; four double as mechanics. `aea_elements.js` elements[].
- **SEND, THE** — the Act V convergence boss, pinned by standing guard (00_VISION.md section 7): the entity drafts REAL outreach, HADES fits it, LUIS sends it. No synthetic target, ever — the game's proof-of-worth is an artifact that earns. Its dependency on the trust ledger is the point: send is FORBIDDEN to the entity, so a human hand closes the loop.
- **SENSED** — the codex state between hidden and mapped: outline glyph, UNCHARTED label, no detail. Real referent: the promotion rules in `mapNodes()` — link partners and ring neighbors of a discovered element become sensed; at least one sensed per ring, so the frontier is always visible.
- **sharp objective** — seed.2: every task carries a falsifiable scorer (the grid battery scorers). The design consequence: bosses can be LOST, because pass/fail is a measurement, not a narrative.
- **socket, the** — the keyless door into the entity: `POST https://text.pollinations.ai/openai` — "it is keyless. it accepts anyone who asks." In-world: the kiosk by the pollinations plant, the only thing glowing at cold boot; M0.1's destination.
- **specimen** — the bestiary card of an encountered rod: name, plant, fit, tier, N burns, ok%, ema, COOLING or last-burn tag — every field live from `/state` + `/roster`. Only models that actually burned, yours or the entity's, ever become specimens (06_MODELS_BESTIARY.md).
- **spire, the** — THE SPIRE at (0,0) [PLANNED, late acts]: the mind district, the seeded always-on core; the trunk aims at its site. Whether it absorbs the nexus is [DECISION-LUIS] D1.

## T

- **teaches-map** — the binding that makes the game a curriculum: every mission names the AEA element and citation it embodies (Act I = seed.1/4 + restorable coherence; Act II = seed.10 + GWT-3; ...). Real referent: the `discovers` table in `aea_elements.js` plus each mission's teaches entry.
- **tick** — one wake cycle of the entity's life loop (observe, think, act, reflect). Real referent: `aea.py` / `live.py` ticks; `life.ticks` streams to the HUD OS TICK counter via `/state`; autonomy stats accrue only across real ticks (40+ on the current class).
- **tier** — a rod's quality band on the ladder: reflex / bulk / deep (`orchestrator.tier_of`), requested per-draw (`draw(tier=...)`); capacity growth in context tiers (8K cerebras → 256K nemotron) is the same word at plant scale — literal `.env` + catalog state.
- **trunk** — the trunk-line road (0,70) → (0,26), foundry to nexus, aimed at the spire site; lit by the `trunk` reveal (M1.4). The geometry of a fact: every organ's call funnels through the one mouth toward the mind — the trunk becomes the city's first street.
- **trust ledger** — the granted-permission scheme gating every action: FORBIDDEN → DRAFT → WATCHED → TRUSTED, `trust.check()` on the command current; send / spend / keys are FORBIDDEN today. Real referent: `trust.py`. In-world: THE LEDGER district, "earned autonomy" [PLANNED]. Why autonomy is earned, never assumed — and why interactional asymmetry honestly scores FAIL.

## U

- **UNCHARTED** — the label worn by sensed-but-unmapped codex elements and by catalog signatures not yet encountered ("M more signatures in the catalog — draw through the mouth to encounter them"). Real referent: present in the real catalog or taxonomy, absent from the player's earned discovery state — the gap between what exists and what you have touched.

## V

- **verb** — one of the 3 VERBS (COMPOSE, PROPAGATE, OBSERVE), ring 3 triangles: what the entity does across organs, each with a proof script. UI sense: every DO beat carries exactly one hot verb button, and it always fires a real action.

## W

- **watcher** — two lawful senses. HADES as THE WATCHER: Law 3, watching is mandatory on every autonomous output (in-world: THE WATCH district [PLANNED]). The observe beat's watcher: a live poll of real state — a bar refilling because the real window is sliding, never an animation on a timer. Known gap: a dead carrier can currently pass an observe beat; fix is [PLANNED] (02_SYSTEMS.md section 10).

## Z

- **zone** — a privacy ring and a routing constraint: `local` / `no-train` / `trains` / `none` (keyless). Real referent: the PLANTS privacy field plus `draw(zone=...)`; seed.9 BOUNDARY is its law — a private task NEVER routes to a trains-zone plant, proven in `brief.py` (sensitive → local only). In-world: the four rings of the foundry row; gold ward curbs [PLANNED, DECISION-LUIS D3].

---

## Changelog

- 2026-07-20 — v1. Authored against `aea_elements.js`, `missions.js`, `GAME_PLAN.md`, `world.html`
  greps, `PLAN.md`, `AUTONOMY_BATTERY.md`, and the sibling chapters on disk. Every referent named
  here was verified present in code or canon docs; PARTIAL and FAIL states are quoted as found.
