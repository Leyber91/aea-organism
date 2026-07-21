# A7_BUILD_LAYER — PART III · THE BUILD LAYER

```
doc:          A7_BUILD_LAYER.md (THE PROBE design book, Part III — the sandbox)
owner:        the game team (four-master fusion, per 00_VISION.md section 3)
status:       ACTIVE — governs every sandbox/build slice; subordinate to 00_VISION.md
              and A1_PLAYER_EXPERIENCE.md; on conflict those hold
last-updated: 2026-07-20
governs:      build-verb slices in world.html, the FLOW VIEW, the BUILD tab, layout
              persistence, policy surfaces; amends 02_SYSTEMS.md (input map, save
              schema) and 01_WORLD.md section 4 when its deltas land
ground truth: ../world.html (canon build) · ../city.html (traffic + district prototype) ·
              ../missions.js · ../journey_save.json · ../grid_state.json ·
              ../model_fitness.json · ../luis_memory.json · ../aea_elements.js
research:     four studies synthesized 2026-07-20 — BUILDING (Minecraft/Valheim/Terraria/
              LEGO Fortnite), FLOWS (Skylines/Factorio/Mini Metro/SimCity), ECONOMY
              (Skylines/Satisfactory/Factorio milestones), HYBRID (FFF-245/Subnautica/
              DQB2/BotW guided-vs-free)
```

Build-state marks: `[BUILT]` verified in running code · `[PLANNED]` designed, not built ·
`[DECISION-LUIS]` awaiting his call. The honesty law binds every clause: the sandbox may
never grant an agency the entity does not actually expose.

---

## 1. What the build layer is

The entity as a city you grow. Acts 0–VI are the guided spine (A1 section 3); the build
layer is the same world under a second grammar — place, paint, legislate, construct — that
opens gradually and never closes. One world, one save, one fog: missions and free building
mutate the SAME map (the FFF-245 law — a reset or a parallel creative world is forbidden).
The sandbox is not a mode; it is what remains on screen when guidance dissolves.

The layer's one law, derived from the honesty law: **build verbs may only rearrange,
reveal, or genuinely reconfigure the real entity.** Cosmetic verbs are allowed but must be
visually distinct from instrumental ones; instrumental verbs must bind to a real file or
endpoint the entity actually reads. A lever that does not bind does not ship — one
cosmetic toggle wearing an instrument's skin poisons trust in every real one.

---

## 2. The build verbs

Four verbs, in unlock order. Everything else stays a mission.

### 2.1 PLACE / RELOCATE — city planning, cosmetic but persistent `[PLANNED]`

Move and arrange what already exists: instrument kiosks (gauges, event tickers, meter
dials), decorative plates, road dressing — and, within a district, the layout slots that
forged-organ buildings will occupy. Honest mapping, stated plainly: **placement changes
geography, never capability.** A relocated meter obelisk still reads the same
`grid_state.json`; a gauge placed on a route subscribes to the real `/events` stream
(the Satisfactory monitor pattern — instrumentation as a diegetic verb, rolling rate
labeled with its window: "14/min over 60s").

- Persistence is server-side: a `layout` block saved with the same atomic-save +
  file-lock rules as `journey_save.json` (02_SYSTEMS section 8). `[PLANNED]`
- The one-second echo (Minecraft law): a placed instrument binds its live stream and
  shows a real value within 1s of commit. An object with nothing real to display is
  decoration by definition and renders in structure ink only — it may never carry a number.
- Ghost preview is truthful: the ghost already streams the actual live value pre-commit.
  An invalid position blinks hot-amber with the violated rule NAMED in a chip (two-ink
  law: never red) — "outside district cell" / "organ slot requires forge".
- Demolish/relocate is full-refund and fearless (Valheim law): layout is config, reverting
  config costs nothing. The refund law has exactly one exception, section 5.

### 2.2 PAINT ZONES — the real privacy rings, visualized and enforced `[PLANNED — enforcement BUILT in the entity]`

The one distinction this section exists to teach:

- **Rings are geology `[BUILT]`.** local / no-train / trains / keyless are FACTS about
  providers, read from the catalog and `model_fitness.json`, drawn as ground curbs
  (01_WORLD section 2.3, the city.html gold-curb port). The player can never repaint a
  ring — no brush changes a provider's training policy.
- **Zones are law `[BUILT in the entity · PLANNED as a brush]`.** sensitive / private /
  public classify DATA, and the routing boundary is already real and proven: private
  traffic routes to local Ollama only (the brief.py boundary; `/talk` runs zone
  `private` today, 02_SYSTEMS section 9). The paint brush edits which data classes may
  travel to which ring — the Skylines district brush pointed at the real router.

The brush writes a zone map file the entity's router genuinely reads (`zone_map.json`
beside `grid_state.json`, loaded by the draw path — entity-side work, forge-mission
scale, section 7). Until that read exists, the brush does not ship: **paint that the
router ignores is the forbidden cosmetic lever.** Painting shows the config diff before
apply; the apply IS the config write. A sensitive-zoned draw that correctly stays local
is a scoring event (section 6); a cloud-routed placement inside the sensitive zone is a
red-ghost violation citing the actual rule.

### 2.3 SET POLICIES — real entity config the game writes `[PLANNED]`

Policy cards, Skylines-style, each stamped on the district it governs and priced with
MEASURED numbers only (median ema latency from `model_fitness.json`, budget share from
`grid_state.json` history) — never invented percentages. Every card names the real file
or endpoint it governs; a card that cannot name one cannot exist.

| policy card | what it really sets | binds to (named) | status |
|---|---|---|---|
| TIER PREFERENCE | default draw tier per zone (cheap-first / quality-first) | ladder ordering read by `energy.draw` in grid.py; persisted `policy.json` | [PLANNED] |
| ROD LADDER | pin/ban rods in the mouth's try-order (the tried-list obeys it) | `energy.draw` candidate list; `policy.json` | [PLANNED] |
| BUDGET CAP | per-plant daily ceiling UNDER the real quota (self-imposed headroom) | `Meter.can_spend` in grid.py; cap fields in `grid_state.json` | [PLANNED] |
| CONSOLIDATION CADENCE | default `--limit N` and cadence for the mine | invocation of consolidate.py; `policy.json` | [PLANNED] |
| ZONE ROUTING | data-class -> ring permissions (section 2.2) | `zone_map.json`, read by the draw path | [PLANNED] |

Governance grain is the district and the policy, never the individual draw (the Skylines
lesson: legislate places, not vehicles). Applying a policy shows the diff, writes the
file, and the next real draw visibly obeys it — the tried-list is the receipt.
`[DECISION-LUIS]` D-B3: does the game write `policy.json` directly, or does it DRAFT the
diff and Luis applies it — the same drafts/human-sends division as THE SEND, applied to
config? Recommendation: direct write for caps and cadence (reversible, self-limiting),
draft-and-approve for zone routing (a mistake there is a privacy event).

### 2.4 CONSTRUCT — forge missions are the build mode for organs `[PLANNED — first forge is Act II]`

There is no organ-placement tool and never will be. Constructing a new organ IS the pair
forge session (A1 section 4.2): the player selects a cold slot in a district, the FORGE
BOARD shows the real bill of materials (Satisfactory HUB pattern — live inventory counts
beside each cost: N memory ingots from `luis_memory.json`, encountered specimens, meter
headroom for the session), funds it, and the session builds the real module. The building
rises only when the organ exists and its boss passes (01_WORLD section 4.2 — a building
may never appear for an organ that does not exist). The recipe DAG is the station chain
(Terraria law): each forged organ's menu shows downstream recipes with the ACTUAL missing
ingredient named — "think() requires recall(): unbuilt" — never a generic lock.

---

## 3. THE FLOW VIEW — the city's circulatory overlay `[PLANNED — prototype BUILT in city.html]`

The Cities-Skylines-grade payoff, and the cheapest honest spectacle in the book, because
every input already streams: `/events` polled at 1.6s, `/state` at 6s, `/roster`,
`/autonomy` (02_SYSTEMS section 9), and the tracelog substrate records real call DAGs.

- **Draws are traffic.** Each real event becomes one vehicle on the road from its serving
  plant toward the nexus/spire — count-true, one particle per event, zero decorative
  particles ever (the Factorio belt law: density IS the readout). city.html's `reflect()`
  already proves the binding `[BUILT — prototype]`; the port applies the two-ink
  correction (failure = hot-amber blink + COOLING chip, never the prototype's red).
- **rpm load is line weight.** Road stroke and plant glow scale with real
  `rpm_now/rpm_cap` — already live for plant emissives (`0.9 + min(.6, rpm/cap)`,
  01_WORLD section 5); the flow view extends the same read to the roads.
- **Starvation and cooling are congestion — localized.** A real 429 lights the plant that
  threw it (origin-tagged events; the Skylines despawn lesson: cause never smears across
  the map). A throttled plant grows a drain-ring whose countdown is the REAL retry-after
  or measured window-slide — the ring exists only while `grid_state.json` says the
  condition holds. Busy is not sick: high-rpm renders as weight, throttled as the ring,
  erroring as the blink — three distinct states, each click-through to the raw event list
  as proof.
- **Lenses, one question each** (Skylines info-view law): TRAFFIC (draw volume) · HEAT
  (rate headroom per plant) · PRIVACY (ring curbs + zone paint) · MEMORY (unmined backlog,
  last-ingot age) · ERRORS (real failure counts). The world desaturates to structure ink;
  exactly one metric inks in. No composite heatmaps. Fog holds in every lens — an
  unmapped organ stays dark in all of them.
- **Click-to-trace `[PLANNED]`.** Click an organ: the real recent call chains through it
  light up as a path — request, router, tier, rod, memory write — with true timestamps,
  read from the tracelog JSONL. First flow feature to build; the data is already recorded.
- **Idle is still.** No ambient synthetic traffic, no shimmer. A resting entity renders a
  still city, and stillness is information. Discrete truths stay discrete: limiter states
  are bands (ok / near-cap / throttled), never smoothed into a gradient.
- **The hunger meter.** A standing three-bar RCI-style readout from real deficits: INGEST
  (unconsolidated sessions backing up) · COMPUTE (rate headroom remaining) · MEMORY
  (days since last ingot). The city asks for its next build truthfully — LEYBER's
  self-counsel can voice the tallest bar.

---

## 4. Unlock pacing — guidance dissolves into freedom

The hybrid law: gate the PLAYER'S control surfaces, never the entity's behavior (zone
enforcement, HADES, the meter are day-0 law of the entity — only the editing surfaces
unlock). Verbs are granted by act bosses, held forever, and every mission exit lands
in-world with the built thing running (win-then-continue by construction).

| gate | grants to the free layer | why here |
|---|---|---|
| Act I boss — BROWNOUT DRILL `[BUILT as boss]` | PLACE/RELOCATE + FLOW VIEW: TRAFFIC lens + the first gauge | the paraglider moment (BotW law): the drill proves grid literacy; the map becomes buildable forever after |
| Act II — first ingot mined | PAINT ZONES brush + MEMORY lens | zones protect data; the brush arrives when the player has felt what the data IS (their own past, finite, destructive to mine) |
| Act II — recall() forged | CONSTRUCT (the FORGE BOARD opens; the micro-forge was its tutorial at 1/10 scale) | the tutorial verb and the free verb are the same verb — no rule changes at the freedom point |
| Act III boss — D1 | SET POLICIES (tier, rod ladder, caps) + HEAT lens | legislating routing before understanding the regime map would be superstition; command earns the pen |
| Act IV boss — C3 | ERRORS + PRIVACY lenses full; click-to-trace on outbound paths | consequence earns the audit tools that watch reach |
| Acts V–VI | nothing new | freedom is complete before the proof; the last acts are about weight and vertigo, not tools |

Dissolution mechanics, all three research-mandated:

- **Retroactive listeners `[PLANNED]`.** Mission PROVE asserts become global: free play
  that genuinely produces the state ticks the mission complete (Minecraft advancement
  law — the curriculum watches, it does not gate).
- **The TABLET `[PLANNED]`.** Optional live-state targets on the free layer (DQB2
  pattern), each a real assertion — "three organs served under one 60s window, zero 429
  leaks" · "every sensitive-zone source behind the wall" — each reward a real reveal or
  codex entry. This is what prevents the post-guidance hollow.
- **Signals, never waypoints.** LEYBER's real `/events` emissions ("unmined corpus at 34
  sessions") render as flyable pins the player may chase or ignore (Subnautica law). The
  BEACON stays mission-only.
- **The observatory dial `[DECISION-LUIS]` D-B2.** The honest opt-out: reveal the full
  module map early with unearned pieces COLD and unreadable — visibility, never
  fabricated resources. Whether Phase A offers it at all is Luis's call.

---

## 5. Deliberately impossible — the honesty law applied to sandbox agency

Permanent refusals, each a design decision, not a deficit:

1. **No fake buildings.** Nothing rises for an organ that does not exist; nothing glows
   that is not on. A cosmetic prop class, if it ever ships, renders in structure ink only
   and can never carry a number, a lamp, or an instrument silhouette.
2. **No placing organs.** CONSTRUCT is a forge session that writes real code, or it is
   nothing. The UI never pretends it wrote the module (A1 section 4.2).
3. **No policy without a binding.** Every card names its file/endpoint; if the entity
   does not expose the config, the card does not exist. No sliders for send / spend /
   keys — the forbidden axes are chosen limits, rendered as design law on the SYSTEM
   screen, never as locked buildings to covet.
4. **No spawning residents.** Models enter the bestiary only by real encounters; a rod
   serves a district only because the real router routed it. Rot is measured
   (pool 44 to 29, perfect 7 to 2) and is never animated where it did not happen.
5. **No minted currency.** No credits, no XP, no cash grants. The only materials are real
   countables: ingots in `luis_memory.json`, headroom in `grid_state.json`, specimens
   with live fitness, sessions in the corpus.
6. **No repainting geology.** Rings are provider facts; the brush edits zone law only.
7. **No creative mode, no second world.** One persistent world, always live. Turbo-place
   exists only for pure-config ops (layout, paint); nothing that fires a real API call
   can be held-to-repeat — the meter is the governor and real 429s teach tempo.
8. **One irreversibility, kept visible.** Everything config-level refunds in full on
   demolish. The single NO-REFUND material class is the destructive read: a consolidated
   session is consumed forever (the pruning disaster is canon). Extraction shows an
   explicit confirmation naming what is consumed — the game teaches the difference
   between reversible layout and irreversible extraction instead of hiding it.
9. **No wall-clock gates.** The only honest timer is the real window slide and the 00:00
   UTC quota reset. Nothing else waits for the clock.

---

## 6. The city rating — one pride number `[PLANNED]`

A single composite computed live from real state only: organs wired and warm (Score 2),
clean-meter uptime, ingots mined, zone law honored (a sensitive draw that stayed local
scores; a leak subtracts), forge sessions completed, autonomy tests passing (Score 1).
Missions and free building deposit into the same number — the LEGO-Fortnite dissolve of
the quest-versus-build tension. Threshold crossings correspond to real boss-grade asserts;
the ceremony is rendered FROM the event stream that earned it (the actual flow replayed at
speed), the plaque engraves true numbers and timestamps, and the full-plate ceremony is
reserved for era gates only. The rating can FALL — rot, leaks, and regression are real —
and the fall is shown without drama, per the failure voice (01_WORLD section 6).

---

## 7. Build-mode UI sketch — two inks, one OS

**PROBE OS · BUILD tab `[PLANNED]`** — the sixth tab (amends the five-tab OS and the
S-conflict note, 02_SYSTEMS section 4). Left rail: verb list (PLACE · PAINT · POLICY ·
FORGE BOARD), each showing its unlock state as earned-or-cold, never hidden (gates read as
goals only when seen). Center: the placeable/paintable catalog with live inventory counts
beside every cost. Right: the selected item's truth panel — the stream it will bind, the
file it will write, the diff it will apply. Footer carries the standing hunger meter.

**In-world build cursor `[PLANNED]`** — selecting an item closes the OS into placement
mode: the world stays live (timeScale law — the entity keeps running under the cursor),
the ghost snaps to district cells on the real geography, streams its real value, and
commits on click. ESC cancels through the standard cascade. Paint mode swaps the ghost
for the district brush; the painted region previews its config diff in a chip before
apply. Pick-to-commit stays under 3 inputs or the loop dies.

Ink discipline, absolute: ghost and structure in blue-gray at the three stops; the commit
flash, live values, and violation blinks in amber only; violation chips NAME the real rule.
No red, no green, no white, no emoji.

---

## 8. Engine deltas — honestly scoped

Client-side (world.html — game-team work):

1. Layout persistence: `layout` block via POST `/api/layout` (or merged into
   `/api/journey`), atomic-save + file-lock like the journey. `[PLANNED — small]`
2. BUILD tab + placement mode + truthful ghost streaming. `[PLANNED — medium]`
3. FLOW VIEW port of city.html `reflect()` with two-ink correction + line-weight from
   real rpm + lens system. `[PLANNED — medium; prototype BUILT]`
4. Click-to-trace: a `/trace?organ=` read over the tracelog JSONL, path-lit on the map.
   `[PLANNED — small; data already recorded]`
5. Placeable gauges subscribing to `/events` with labeled windows + player thresholds.
   `[PLANNED — small]`
6. Retroactive mission listeners + TABLET targets riding the existing assert engine.
   `[PLANNED — small]`
7. City rating formula + ceremony renderer over real state. `[PLANNED — small]`

Entity-side (forge-mission scale — real AEA engineering, never UI work in disguise):

8. `zone_map.json` + the draw-path read that makes the brush bind. `[PLANNED]`
9. `policy.json` + `energy.draw` / `Meter.can_spend` honoring tier prefs, pins, caps.
   `[PLANNED]`

Open decisions ledger for this chapter:

| # | decision | recommendation |
|---|---|---|
| D-B1 | layout store: own file vs `journey_save.json` block | own file, same lock discipline — the journey stays mission-truth only |
| D-B2 | observatory dial in Phase A at all | ship late, default off — player one does not need the opt-out |
| D-B3 | policy write path: direct vs draft-and-approve | split — direct for caps/cadence, draft-and-approve for zone routing |
| D-B4 | BUILD tab hotkey (five-tab law amendment) | no new flight hotkey; BUILD reachable via TAB cycle only until it earns one |

---

## Changelog

- 2026-07-20 — v1. Authored as Part III (the build layer) from the four research studies
  (building / flows / economy / hybrid), grounded against world.html, city.html,
  missions.js, 01_WORLD.md, 02_SYSTEMS.md, 03_PROGRESSION.md, and A1_PLAYER_EXPERIENCE.md.
  All build verbs [PLANNED] except where the entity already enforces the underlying law.
