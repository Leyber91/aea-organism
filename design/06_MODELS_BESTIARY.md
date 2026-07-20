# 06 — MODELS BESTIARY
### THE PROBE design corpus · specimen system, combination doctrines, rot

| | |
|---|---|
| **Owner** | the game team |
| **Status** | core system BUILT and live in `world.html`; three extensions PLANNED; two decisions open |
| **Last updated** | 2026-07-20 |
| **Ground truth** | `aea_elements.js` · `world.html` (`modelsRender`, `encounter`) · `energy.py` · `model_fitness.py` · `capability_census.py` · `controlroom.py` (`/state`, `/roster`) · `journey_save.json` · `candidates_probe.json` |
| **Siblings** | `03_MISSIONS_AND_ACTS.md` (acts, beat kinds, M-ids) · `04_ENERGY_GRID.md` (plants, meter, the mouth) · `05_CODEX_MAP.md` (the concentric AEA map) |
| **Laws in force** | AEA honesty law: every number on a bestiary screen is live system truth; no fake data ever; claim ceiling = "measured functional correlate", never "conscious". Two-ink FUI: amber `#ffb000`/`#d4a24c` = live/fired only; blue-gray (`rgba(120,155,175,…)`) = structure. NO emoji. IBM Plex Mono. |

The bestiary is the game's item system and its creature catalog at once. A "specimen" is a
**rod**: one `plant/model` pair the grid can burn. Nothing in this system is authored content —
every card is a read of the entity's lived experience, which is why the tab opens with
"reading the entity's lived experience…" and renders nothing it cannot prove.

---

## 1. [BUILT] The specimen system — encounters

Implemented in `world.html` (`modelsRender()`, THE PROBE OS → MODELS tab) over two live
endpoints on `controlroom.py`.

### 1.1 What counts as "encountered"

A specimen exists in the bestiary iff it appears in the **union** of:

1. **The journey's own burns** — `SAVE.models` (persisted server-side in
   `journey_save.json → models[]`, atomic + merged via `POST /api/journey {models:[k]}`).
   `encounter(plant, model)` fires only on a **successful real action**: `node_channel`,
   `channel_multi` (per plant served), `node_energy` / `drill` (the rod `p.plant/p.model`
   that actually answered, read from the mouth's returned `tried[]` routing record).
2. **The entity's lived draws** — `/state → energy.rods` filtered to `calls > 0`
   (`controlroom.py state()`, sourced from `energy_usage.json`). If LEYBER burned a rod in a
   tick while the player was away, it is encountered. The world moves without you.

Consequence (by design): you cannot meet a model by reading about it. Only a real call —
yours or the entity's — creates a card. Current save on disk: 1 encounter
(`pollinations/openai-fast`, from M0.1 FIRST LIGHT).

### 1.2 The specimen card — field spec (all live)

One `crow` per encountered rod, sorted alphabetically, staggered reveal (`.03s * i`):

| field | source | meaning |
|---|---|---|
| name | rod key minus plant, 26 chars | the specimen |
| plant | rod key prefix | which power plant serves it |
| `fit a/b` | `/roster.fitness_top` (top-18 from `model_fitness.json` probes, `correct` count / probe count) | sweep-measured competence |
| `lat` | same row, mean probe latency | how fast when probed |
| `tier` | same row (`orchestrator.tier_of`) | reflex / bulk / deep ladder position |
| `N burns` | `energy.rods[].calls` | lifetime real draws |
| `ok%` | `round(100 * ok / calls)` | lived success rate |
| `ema Ns` | `ema_latency` (0.7 old + 0.3 new per success) | lived speed, recency-weighted |
| tag | `COOLING` (amber `.alert`) if cooling, else last-burn date `MM-DD HH:MM` | current health |

A rod can carry fitness data with zero burns (swept but never drawn), burns with no fitness
row (drawn but outside the top-18), or both. The card shows whichever halves exist — absence
of data renders as absence, never as a placeholder number.

### 1.3 The wild count

Header chip: `N encountered · M signatures in the wild`, where
`M = max(0, catalog_size − N)` and `catalog_size` comes **live** from
`/roster.candidates.catalog_size` = `candidates_probe.json` (currently **119**, probed
2026-07-19). Below the known cards, one masked `sensed` row:
`▮▮▮▮▮▮▮ — M more signatures in the catalog — draw through the mouth to encounter them`.
Empty state: "nothing encountered yet — fire the first light." Endpoint failures degrade to
empty arrays; the screen never invents.

`/roster` also carries `excluded` (the nemotron content-safety family, Luis's directive
2026-07-12) — quarantined signatures, never routed, never probed.

---

## 2. [BUILT] The doctrines — measured combination laws

The bestiary's second panel. Six laws in `aea_elements.js → doctrines[]` — **measured, not
invented**, from the 2026-06 grid experiments (`experiment_v2/v3/v4.py`, the swarm
coordination regime map) and the proven organ scripts. Lines and evidence are verbatim data;
the UI renders them untouched.

| id | name | law | evidence (rendered as-is) | state |
|---|---|---|---|---|
| `doc.solo` | THE SOLO LAW | an easy task wants ONE good model. a council on an easy task HURTS it. | measured · grid experiments v2–v4 (2026-06): council overhead damaged easy-task accuracy | open from start |
| `doc.council` | THE DIVERSE COUNCIL | a hard or unreliable task is rescued by a DIVERSE-model vote — the win is model diversity, not temperature. | measured · v3 net +3 with 0 damage; same-model ensembles did not rescue | open from start |
| `doc.verifier` | THE LONE VERIFIER RISK | a single verifier can be wrong alone. the watcher survives by strict-schema + a DIFFERENT model than the worker. | measured · verifier error analysis; hades.py Law-2 heterogeneity | locked |
| `doc.relay` | THE GENETIC RELAY | models hand a compact state capsule down a chain — the toolkit grows across hands. | proven · relay.py: 5 distinct models, 2/2 handoffs, toolkit reused downstream | locked |
| `doc.swarm` | THE RAMIFICATION | decompose, escalate, depth-cap — a tree of small minds where one big mind would drown. | proven · swarm.py: 8 role-differentiated agents, spawn decisions mid-tree | locked |
| `doc.path` | THE CRYSTAL PATH | search once for the winning model per task-type, then run cheap forever. | proven · pathfinder.py -> paths.json (op.learn live) | locked |

**Unlock rule as built** (`modelsRender`): a doctrine renders iff `!d.locked || actI` where
`actI = missionDone("M1.5")` (BOSS · BROWNOUT DRILL, Act I). So SOLO LAW and DIVERSE COUNCIL
ship visible; the four locked laws all open at the Act I boss. Locked rows render masked
(`▮▮▮▮▮▮ — an undiscovered doctrine — combinations reveal in later acts`); chip = `n/6 known`.
See §5 for the planned refinement — and the collision it creates with this blanket rule.

---

## 3. [BUILT] ROT — durability as measured decay

The extreme test from `GAME_PLAN.md` §1, and it holds: **durability loss is measured, not
simulated**. Models genuinely degrade — providers throttle, retire, and break them — and the
bestiary shows it because the systems underneath record it. Rot runs on two clocks.

### 3.1 The fast clock — live cooling (`energy.py`)

- `_record_use` per draw: success → `ok++`, `consec_fail = 0`, `cooled_at` cleared, EMA
  updated. Failure → `fail++`, `consec_fail++`; at `COOL_AFTER = 3` consecutive failures the
  rod gets `cooled_at` and `_cooling()` holds it out of the ladder for `COOL_SECONDS = 900`
  (15 min), after which it may retry.
- Canon scar (energy.py comment, review 2026-07-10): cooling was originally a **permanent
  tombstone** — nothing could reset `consec_fail` because a cooling rod was never drawn
  again; tiers decayed monotonically to the local floor. The 15-minute retry window is the
  fix. The bestiary surfaces this clock as the amber `COOLING` tag: the one place a specimen
  card goes hot-ink for a bad reason, which is correct — amber = live, and a cooldown is the
  liveliest fact about a rod.

### 3.2 The slow clock — the fitness sweep (`model_fitness.py`)

Fitness, not benchmark. The docstring names the founding failure: `models_report.json` scored
`qwen3-next-80b` a 4/4, then that model **timed out in brief.py and shipped a hole in the
brief**. So the sweep's battery is shaped like the entity's real jobs (`reason_tight`,
`json`, `synth`, `instruct`; 45 s timeout) and classifies failure honestly:
`ok | EMPTY | TIMEOUT | RATE | ERRn` — EMPTY (200-with-no-text) called out as the silent
killer.

**The 2026-07-19 sweep is canon** (`model_fitness.json`, generated 2026-07-19): the general
pool fell **44 → 29** nodes; perfect scorers fell **7 → 2** (only
`nvidia/mistralai/mistral-small-4-119b-2603` and `nvidia/minimaxai/minimax-m3` at 4/4);
18 of 29 are fully fit (reliability 1.0, zero failure modes); the rest carry TIMEOUT,
ERR404/410/400, EMPTY, or RATE scars. That is a third of the armory rusting in one sweep,
with no game code involved. Rot is the world, not a mechanic skinned onto it.

### 3.3 What rot does to play

- `energy.ladder()` **refuses known-broken rods** (reliability < 1.0, ollama excepted) — the
  fitness lesson, in code. A rotted specimen is not "weaker"; the mouth routes around it, and
  the player sees the reroute in the drill's `tried[]` trace (`rerouted ×n`).
- `LOCAL_FLOOR` (three ollama rods) is always appended: the hearth. Unlimited, slow, and the
  reason starvation is rare and honest.
- Card-level: `fit` columns shift on re-sweep, `ok%`/`ema` shift on every burn, the wild
  count shifts when the catalog itself changes. No respawns, no repair item — a rod heals
  only by actually answering again.

---

## 4. [PLANNED] Probe-a-candidate — the discovery mission type

The wild count is currently a locked door with a number on it. This mission type makes it a
frontier. Not built; designed against existing machinery (`candidates_probe.json` shape,
`capability_census.py` battery, `/api/node/run` plumbing).

- **The act**: from the bestiary's UNCHARTED row (or a field mission), the player targets an
  unencountered, unprobed catalog signature and fires a **real probe** — instruction probe
  plus reasoning probe with escalating budgets, exactly the `candidates_probe` recipe.
  Energy cost is real: probes spend meter budget like any draw.
- **The discovery event**: on response — any response — the specimen card is **born** with
  its first measured data, the wild count decrements, feed line + toast fire
  (`new signature answered: <rod>`), and the result merges atomically into
  `candidates_probe.json` and journey `models[]`.
- **Honesty of dead finds**: a probe that times out or 404s is still a discovery — the card
  records the failure outcome as its first fact. No rerolls, no hiding corpses. Discovering
  that `z-ai/glm-5.2` times out at 60 s (real, in `candidates_probe.json` today) is worth as
  much as finding a live one.
- **Boundaries**: excluded families are not probeable and render as quarantined, with the
  directive cited. Zone rules hold — a probe is a trains-zone act and never carries private
  payload (seed.9 is law here too).
- **[DECISION-LUIS]** Probe pricing: flat one-draw cost, or a visible multi-call cost
  (instruction + N reasoning attempts) itemized on the meter? Recommendation: itemized —
  it teaches what a probe actually is.

## 5. [PLANNED] Specimen detail panel + Act III doctrine beats

### 5.1 Specimen detail panel

Click a card → a detail pane (map-detail pattern reused), all live:

- **Census scores** from `capability_census.json`: the 6-probe battery
  (`reason · trap · code · json · instruct · synth`), deterministic score /6, badge
  `FRONTIER >=5 / solid >=4 / weak` — the same thresholds as `capability_census.py rank()`.
- **Failure modes** and per-probe latency; the `synth_sample` rendered as the specimen's
  voice sample (its actual words, 80 chars, quoted).
- **Lived vs sweep split**: burns/ok%/ema (this machine's history) beside fit/score (the
  battery's verdict) — the panel teaches that the two can disagree, which IS the
  model_fitness lesson.
- **Specialist organs** (OCR/vision/embed/rerank/guard, the `NON_CHAT` regex) render as a
  separate bestiary family and are never shown chat stats — the router bug we fixed stays
  fixed in the UI's ontology.
- FUI: structure ink for all labels and frames; amber only for score digits, FRONTIER badge,
  and COOLING. Two inks, no exceptions.

### 5.2 Act III doctrine-unlock beats

Act III (MIND — the council, the regimes, forge `think()`) demonstrates the laws instead of
handing them over. The council field mission runs the regime map **live**:

1. `do` — easy task, one good model. `do` — same task, 3-model council. `prove` — the
   council did not beat the solo run (the measured expectation). **SOLO LAW re-earned.**
2. `do` — hard/trap task where the solo pick fails; `do` — diverse-model council vote on the
   same task; `observe` — the vote rescuing it in real time. **DIVERSE COUNCIL re-earned.**
3. `learn` — HADES Law-2 code reveal (worker/watcher heterogeneity) → **LONE VERIFIER RISK**
   unlocks on a real verdict pair, not on a checkbox.
4. RELAY / RAMIFICATION / CRYSTAL PATH unlock inside their forge missions (relay, swarm,
   pathfinder organs) as each is wired and its boss passes — fog lifts on integration.

**Named collision** (per the vision-fragment protocol): the built rule (§2) opens ALL four
locked doctrines at M1.5, which would leave Act III demonstrating laws the player already
holds. These two truths cannot coexist. Proposed resolution: `aea_elements.js` doctrines gain
an `unlockedBy: <missionId>` field; `modelsRender` checks `missionDone(d.unlockedBy)`; M1.5
keeps only what Act I actually taught (nothing beyond the two open laws — the brownout drill
is a resilience lesson, not a combination lesson). **[DECISION-LUIS]** approve the re-gating,
or keep the Act I blanket unlock and let Act III be confirmation rather than discovery.

**SUPERSEDED (2026-07-20).** The fork above is resolved by `05B_CONTENT_ACT3_4.md` §1: the
two-state READ/EARNED scheme. M1.5 keeps its built blanket unlock, downgraded in meaning to
READ (text unmasked, structure ink); Act III missions EARN (amber tag, evidence line appended
with the live demonstration's real result) — nothing shipped regresses. `doc.verifier`'s earn
point is M3.3 per 05B's earnedBy map; M2.3's reset-probe verdict grants READ context only,
not the earn. The original text stands above as the record of the collision. Luis retains
veto (BOOK.md open-decisions ledger, #4).

— edited 2026-07-20 (completeness audit closure)

**[DECISION-LUIS]** Sweep agency: does the player ever trigger `model_fitness.py` /
`capability_census.py` re-sweeps as a field action (a "survey expedition" that can come back
with bad news), or do sweeps stay operator-side with the game only reading the fallout?
Recommendation: player-triggered, metered — rot you go looking for lands harder than rot in
a changelog.

---

## 6. Phase B note

Everything in §1–§3 reads from files any AEA build produces (`energy_usage.json`,
`model_fitness.json`, `capability_census.json`, `candidates_probe.json`). A Phase B player
building their own assistant gets their own bestiary for free: their rods, their rot, their
sweep dates. No content in this document is Luis-specific except the canon events named as
canon (the 2026-07-19 sweep, the 2026-07-10 cooling review, the 2026-07-12 exclusion
directive) — those are this world's history, and each new world writes its own.
