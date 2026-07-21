# THE JOURNEY — the big plan (ASCENT v2)

> The governing design for the game that gets us to the Autonomous Entity Architecture.
> Supersedes the static ladder of 2026-07-20 (kept at /game as scaffolding until replaced).
> Verdict on v1, accepted: a checklist wearing a graph — nothing regenerates, nothing is
> scarce, nothing is discovered, nothing is taught. v2 fixes all four with mechanics that are
> REAL, not skinned.

## 1. What it is

A guided journey from a bare socket to a living AEA, played mission by mission, with LEYBER
itself as the guide. Three mechanics carry it, and every one is grounded in a real system —
the honesty test (pushed to the extreme, does the mapping hold?) is applied to each:

| game mechanic | the real thing under it | extreme test — does it hold? |
|---|---|---|
| Energy / mana bars that refill | Meter rpm windows (60s, sliding) + daily quotas (00:00 UTC reset) in `grid_state.json` | Can you run dry? YES — 429s and rpd exhaustion are real starvation; local Ollama = the hearth: unlimited but slow. HOLDS |
| Items / tools with stats + durability | Models: reliability, ema latency, size, ctx, privacy zone from `model_fitness.json` + censuses. They ROT (2026-07-19 sweep: pool 44→29, perfect 7→2) | Durability loss is measured, not simulated. Discovery = `candidates_probe` on unprobed catalog models. HOLDS |
| Ore / mining | Unmined corpus sessions → `consolidate --limit N` → memory ingots in `luis_memory.json` | Finite vein (the pruning disaster proved it: ~1,570 sessions lost forever). Mining is destructive-read of a real resource. HOLDS |
| Crafting recipes | Organs built from named parts (recall = memory.py + index_codex + cache + energy.draw). The recipe DAG = the AEA schema | A recipe with a missing ingredient genuinely cannot be built (think() without recall() grounds in nothing). HOLDS |
| Fog of war | The proven-but-not-wired gap (swarm/orchestrator/pathfinder/agent_tools/relay demoed in 9 scripts, absent from the live mind) | Fog lifts ONLY when the organ is wired and its boss passes — integration, not decoration. HOLDS |
| Character sheet / XP / class | The live autonomy battery: 6 cited stats + Bedau class (`autonomy.py`, currently PROTO-AUTONOMOUS 6/6, 40 ticks) | Stats move only on real logged behaviour. HOLDS |
| Boss fights | Cited falsifiable thresholds (Barandiaran, Bedau, Voyager, STOP, DGM...) | A boss can be LOST (HADES holds junk at 0.5 rate today). HOLDS |
| Capacity growth | Keys unlock plants; probes add generators; context tiers (8K cerebras → 256K nemotron) | "Token limits increase" is literal `.env` + catalog state. HOLDS |

Honesty clause carries over: no mission ever licenses "conscious/sentient" — ceiling stays
"measured functional correlate, present."

## 2. Two mission types (the honest split)

- **FIELD missions** — Luis plays them SOLO in the UI, fully real, via existing endpoints:
  fire a call (`/api/node/run`), mine a corpus slice (`/do consolidate`), run a tick
  (`/do tick`), probe a candidate, watch a mana bar refill, interrogate the entity (`/talk`).
  No Claude session needed. This is what makes the game playable between our sessions.
- **FORGE missions** — we build a NEW organ together (recall, think, C3...). The game frames
  the craft: shows the recipe, the spec, the boss threshold; the build itself is a pair
  session (Claude writes, Luis judges); the boss check and the fog-reveal are automatic after.
  The game never pretends the UI wrote the code. It drives and verifies the work.

## 3. The guide — the customized assistant

LEYBER narrates its own construction. Every mission beat has authored core text (reliable,
learning-ordered) plus an ASK LEYBER button: the beat's context is injected into `/talk` and
the entity comments live from its real state and codex. The thing being built teaches you the
thing being built — that is the meta-thesis made playable (understand it from inside out).

## 4. The acts — the journey and the relationships between levels

Dependency journey; each act has field missions, ends in a boss; forge missions from Act II.

```
ACT 0  THE DARK ROOM      one socket, one keyless call — what a model call IS
ACT I  POWER              the grid: catalogue -> channel -> meter -> ladder    [all built: pure field]
ACT II MEMORY             the mine -> the Book -> CRAFT recall() (B2)          [first forge]
ACT III MIND              the council -> the regimes -> CRAFT think() (D1+A2)
ACT IV THE WORLD          CRAFT internet-wire -> CRAFT command current (C3) -> F1 senses (Luis decision)
ACT V  THE PROOF          THE SEND — convergence boss: draft real outreach, HADES-fit, LUIS sends
ACT VI SELF               Voyager self-tool -> STOP (>=3 rounds) -> ENDURANCE (100-tick A_new,
                          Bedau Class 2) -> DARWIN-GODEL archive (end-game)
```

Tech tree (recipe DAG — the master schema WITH progression semantics; this is the fog map):

```
 corpus ──mine──> ingots ──┐
 codex ────────────────────┼──> recall(B2) ──┐
 energy.draw ──────────────┘                 │
 swarm ┐                                     ├──> think(D1, absorbs A2) ──┬──> internet-wire ──┐
 orch  ├──(proven, fogged)───────────────────┘                            │                    ├──> THE SEND
 path  ┘                                              trust ──────────────┴──> C3 governed ────┘
 reflect(live) ──> voyager ──> STOP ──> ENDURANCE(Class 2) ──> DGM
 hades(live) ─────────────────────────── gates every craft and THE SEND
```

Teaches-map: every mission names the AEA element + citation it embodies (Act I = seed.1/4 +
restorable coherence; Act II = seed.10 + GWT-3; Act III = axes P/M + GWT-2/4; Act IV = seed.8
+ the governance membrane; Act VI = seeds 3/5 + open-endedness). The AEA is the curriculum.

## 5. Mission anatomy — data-driven script (missions.json)

Missions are DATA, the engine replays them. Adding content = writing JSON, not UI.

```json
{"id":"M1.3","act":"I","title":"THE METER — why it never browns out","type":"field",
 "requires":["M1.2"],
 "teaches":[{"code":"seed.4","cite":"restorable coherence; engine review 2026-07-10"}],
 "beats":[
  {"kind":"brief","text":"Free energy has breakers. 40 req/min per NVIDIA model. Trip one and the plant browns out. The Meter is the grid operator."},
  {"kind":"learn","code_reveal":{"file":"grid.py","fn":"Meter.can_spend"},"annot":"a locked read-modify-write on ONE shared file — every process sees the same budget"},
  {"kind":"do","text":"Fire 3 calls, watch the rpm window fill","action":{"endpoint":"/api/node/run","payload":{"node":"channel"},"repeat":3}},
  {"kind":"observe","text":"Now watch the bar refill as the 60s window slides","watch":{"endpoint":"/state","field":"energy.meter","seconds":60}},
  {"kind":"prove","check":{"endpoint":"/state","assert":"no plant over cap"},"boss":false}],
 "rewards":{"reveals":["meter-mastery"],"lore":"the mana lesson"}}
```

Beat kinds: `brief` (why, 3 lines) · `learn` (real code, typewriter reveal + annotation — the
builder.html mechanic, reused where it belongs) · `do` (a REAL endpoint action Luis clicks) ·
`observe` (a live watcher on real state — bars moving, events streaming) · `prove` (a real
assert; boss beats gate the act) · `ask` (LEYBER commentary, optional on every beat).
Progression persists in `journey_save.json` (server-side, atomic — same durability rules).

## 6. The windows (multiwindow, locked FUI skin)

Minecraft mechanics, Expanse skin — the locked plate language (two inks, amber=live only,
brackets, mono, void) applies to every window. No cartoon, no emoji, ever.

- **THE JOURNEY** (main): mission player (beats advance with real actions) + the world map
  with fog (evolved from game.html board + schema.json — reuse, don't rebuild).
- **INVENTORY** (pop-out `/inv`): live energy bars per plant (REAL refill animation from
  grid_state windows), item cards (models w/ true stats + rot warnings), ingot count
  (memories), keys held/missing, crafted organs.
- **CHARACTER** (`/autonomy` reskinned): the 6 stats + class tier as the sheet.
- **EVENTS**: the live world feed (`/events`) — the entity acting in real time under the game.
Each is a route on the same server; open as many windows as wanted.

## 7. Why it is dynamic now (the anti-static list)

Mana refills animating from real sliding windows · live ticks streaming as world events ·
item-rot alerts from fitness deltas ("mistral-large is degrading") · discovery events from
probes · fog reveals on integration · the guide talks from live state · count-ups only on
real value changes. The world moves because the entity is actually alive underneath it.

## 8. Build order — SUPERSEDED by the approved plan (2026-07-20)

Both forks were put to Luis and LOCKED: **form = PILOT THE ENTITY** (a real three.js game —
fly a probe inside the living machine; Duskers/Observation lineage) and **opening = ACT 0
GENESIS**. The governing build plan (operating prompt, production values, slices) lives in
the approved plan; canon summary:

- **SLICE 1 (SHIPPED 2026-07-20)**: `world.html` at `/world` — genesis dark world on the
  city.html district geography, probe flight rig (WASD+QE, drag look, chase cam), beacon +
  off-screen arrow, dock terminal, mission engine over `missions.js` (Acts 0–I: FIRST LIGHT,
  CATALOGUE, CHANNEL, METER, LADDER, BROWNOUT boss — every DO/PROVE on real endpoints),
  WebAudio synth, HUD tracks (class/tests/plants/ingots from live state), `/api/journey`
  server-side save (merge + reset, atomic), THE PROBE tab (new window). Verified: genesis +
  revealed screenshots, M0.1's real call ("FIRST LIGHT", 200), save roundtrip.
- **SLICE 2**: Act II MEMORY (the mine -> the Book -> FORGE recall()/B2) + `/inv` pop-out +
  revealed-state art pass. Gate: Luis pilots slice 1 and calls go.
- **SLICE 3+**: Acts III–VI as reached. THE SEND pinned at Act V. F1 = Luis decision.

Guards unchanged: forge missions ARE the real AEA engineering; polish that does not serve
the current act is refused; the boring test gates every slice.
