# 01_WORLD — THE PROBE world bible

owner: the game team
status: living document — sections tagged per truth level
last-updated: 2026-07-20
ground truth: `world.html` (canon build) · `city.html` (district prototype, coordinate donor) · `missions.js` (acts 0–I data)
siblings: 00_VISION.md (why the game exists) · 04_UI_BIBLE.md (the binding two-ink FUI spec, "BINDING UI SPEC v1.0") · 05_CONTENT_MISSIONS.md + 05B_CONTENT_ACT3_4.md + 05C_CONTENT_ACT5_6.md (acts, beats, assertions) · 02_SYSTEMS.md + 06_MODELS_BESTIARY.md (LEYBER's organs, honesty law)  <!-- ghosts fixed 2026-07-20 (audit closure) -->

Tag legend: [BUILT] verified in code on disk · [PLANNED] designed, not yet in world.html · [DECISION-LUIS] awaiting his call.

---

## 1. The field — genesis darkness [BUILT]

The world is a dark plain inside a living entity. The player wakes with nothing: "cold boot. no
memory of why." (missions.js M0.1). Everything visible before act I is silhouette.

One-atmosphere law (world.html "SCENE — one atmosphere"):
- One fog: `THREE.FogExp2(0x0a1420, 0.011)`. Never a second fog, never a fog color change.
- Exactly two lights: a hemisphere light (`0x223a4d` sky / `0x050a10` ground, 0.6) plus the
  probe's own point light (`#ffb000`, 0.7, range 30). No sun, no spotlights. Anything that glows
  is emissive — a thing that is ON.
- Sky dome (r=400, camera-locked): zenith `#050a10` to horizon `#0a1420`, with a breathing amber
  horizon band — `skyU.k` oscillates 0.10–0.18 on a ~20s sine. The entity's field respires.
- Ground: 1600x1600 plane at `#071018`; a 400-unit grid (`0x16242f`/`0x0c1620`, opacity .35)
  that fogs out. 1200 dim stars above the fog ceiling.
- Air: 800 dust motes in a 60-unit wrap box that follows the camera; 180 amber embers rising over
  the foundry — ember opacity starts at 0 and only turns on when the first plant lights (M0.1
  reveal). Even the particles obey progress.
- Post: Render pass + UnrealBloom(0.65, 0.4, 0.5). Film/vignette/gamma passes are absent on disk;
  CSS scanlines (`#scan`) and radial vignette (`#vig`) carry the texture — a named deviation,
  kept (world.html line ~359).

The dark is not a skybox choice; it is the fiction. The field is fully built and running — the
player's cartography is what is missing. Light = knowledge earned. The fog itself thins with
progress: the `foundry_full` reveal (act I boss) drops density 0.011 -> 0.009. World brightening
is always a reveal side-effect, never a lighting-rig edit.

## 2. Geography as built [BUILT]

Coordinate frame: origin at field center; +z toward the probe spawn `(0, 9, 150)`; playable disc
radius 300; altitude clamp 2.2–120. All numbers below are quoted from world.html.

### 2.1 The foundry row
`FOUND = {cx:0, cz:70, w:250}` — fifteen power plants in one row along z=70, evenly spaced from
x=-113 to x=+113 (gap = 226/14 ≈ 16.14). Each plant: window-lit hall (windows emissive-mapped in
warm `#d4a24c`), dark cooling tower, top ring, base rim. Emissives start at 0 — dark until
revealed, then driven by live load (§5).

Order and privacy ring (the `PLANTS` array, world.html):

| x (approx) | id | ring |
|---|---|---|
| -113.0 | ollama | local |
| -96.9 | ovh | no-train |
| -80.7 | cloudflare | no-train |
| -64.6 | cerebras | no-train |
| -48.4 | sambanova | no-train |
| -32.3 | nvidia | no-train |
| -16.1 | groq | no-train |
| 0.0 | gemini | trains |
| +16.1 | mistral | trains |
| +32.3 | openrouter | trains |
| +48.4 | zai | trains |
| +64.6 | github | trains |
| +80.7 | cohere | trains |
| +96.9 | pollinations | none (keyless) |
| +113.0 | hf | none (keyless) |

nvidia alone gets scale 1 (tallest — THE GRID, 121 models); all others cycle .45/.63/.81. The
row reads as a skyline whose one giant is the real capacity giant.

### 2.2 Landmarks
- THE SOCKET — kiosk at `(pollinations.x+9, ·, pollinations.z+8)` ≈ `(+105.9, 78)`, interaction
  pos `(x, 4, z)`. The keyless door into the entity; pre-lit at target 0.55 before any mission —
  the only thing glowing at cold boot. M0.1's destination.
- FOUNDRY CONSOLE — kiosk at `(-6, ·, 88)`, pos `(-6, 5, 88)`. M1.1 survey terminal.
- THE METER — 14-unit hex obelisk at `(+8, ·, 56)`, pos `(8, 10, 56)`. The grid operator; M1.3.
- THE ENERGY NEXUS — icosahedron core + fresnel shell + two counter-rotating tori at `(0, ·, 26)`,
  pos `(0, 6, 26)`. The mouth of the ladder; M1.4 and the act I boss both dock here.
- ROADS — foundry row road `(-113,70)->(+113,70)` w2.4; trunk line `(0,70)->(0,26)` w3 on its own
  material. Both dark until earned: row emissive 0 -> .35 (`roads` reveal) -> .45 (`foundry_full`);
  trunk 0 -> .4 (`trunk`) -> .55. The trunk aims at the origin — the spire site (§3).
- ARCHIVE TEASE — three dark boxes near `(-92..-68, -14..-6)`, label
  "THE ARCHIVE · locked · act II" at `(-84, 18, -10)`, plus a cold blue backlight. Spawned only by
  the `archive_tease` reveal (act I boss reward). The next act is physically visible before it is
  playable.
- Backlight sprites (fake volumetrics): warm `0x211505` behind the socket; cold `0x0e2233` at
  `(0,14,8)` (the spire site) and `(-60,12,60)`.
- THE BEACON — mission marker: 110-unit breathing light cylinder + ground ring, teleports to the
  current mission's node. The only diegetic "quest marker" in the world.

### 2.3 Privacy ring geometry [PLANNED]
city.html's `makePlant(scale, priv)` draws a thin gold curb (torus r=6) around every local and
no-train plot — a private-ward marker. world.html's plants do not yet carry the curb (every plant
has the same base rim). Port the curb so the four rings are readable on the ground, not only in
the CODEX. Depends on [DECISION-LUIS] D3 (§8).

## 3. The planned districts — acts II+ [PLANNED]

city.html is the built prototype of the full city; its `DISTRICTS` table (city.html ~line 366) is
the canonical land registry for later acts. Coordinates are reused as-is:

| key | cx, cz | w x d | label | fiction | act |
|---|---|---|---|---|---|
| spire | 0, 0 | landmark | THE SPIRE | the mind — the seeded always-on core | late |
| archive | -92, -14 | 70x66 | THE ARCHIVE | memory mines — "the book of Luis" | II |
| workshops | 0, -80 | 120x52 | THE WORKSHOPS | skills, a growing population | III+ |
| ports | 92, -14 | 70x76 | THE PORTS | imports/exports — connected services | III+ |
| watch | 96, -78 | 44x40 | THE WATCH | HADES gate — law 3, the verdicter | III+ |
| ledger | 92, 56 | 64x36 | THE LEDGER | earned autonomy | III+ |
| broadcast | -92, 56 | 64x44 | THE BROADCAST MAST | voice — signal out | III+ |

District contents come from city.html's live data blocks: `ORGANS.archive` (consolidate / vector
store / codex index), `ORGANS.watch` (hades), `ORGANS.broadcast` (speak / browserdrive /
interface), `ORGANS.ledger` (trust), `MIND` (the six mind organs ringed around the spire, R=20),
`SKILLS` (23 workshop buildings), `SERVICES` (9 port buildings, Gmail flagged as the gated
OUTREACH door).

Act V–VI mission docking [PLANNED] — registry extension for the nodes `05C_CONTENT_ACT5_6.md`
docks missions at. Not in city.html; names are proposal-grade per 05C §6 call 5 until this
chapter places them, and placement rides the BOOK.md open-decisions ledger (#11, act ordering
/ later districts) — [DECISION-LUIS]:

| key | cx, cz | w x d | label | fiction | act |
|---|---|---|---|---|---|
| mast | = broadcast | — | THE BROADCAST MAST | alias of `broadcast` — M5.1 THE SEND docks here; built dark at act open, lights amber ONLY on a confirmed real send (`mast_lit`); a refusal renders a structure-ink plaque, never amber | V |
| mirror | [DECISION-LUIS] | — | THE MIRROR | M6.2 STOP — the scaffold improves the scaffold; lights on `b6b_stop` | VI |
| meridian | [DECISION-LUIS] | — | THE MERIDIAN | M6.3 ENDURANCE — 100 ticks against the shadow; lights on `b6c_bedau` | VI |
| lineage | [DECISION-LUIS] | — | THE LINEAGE | M6.4 DARWIN-GODEL — the archive of selves; lights on `b6d_dgm` | VI |

M6.1 (voyager) docks at `workshops`, already registered above.

Named coordinate deviations (world.html is canon where both exist):
- Foundry: prototype `cz:82, w:230` vs built `cz:70, w:250`. Built wins; the prototype foundry
  row is superseded.
- The spire site vs the nexus: the built nexus sits at `(0, 26)` on the trunk that points at the
  origin. Intent: the nexus is the foundry-side terminus; the spire rises at `(0,0)` in a later
  act, and the trunk becomes the first street of the city. Not yet locked — [DECISION-LUIS] D1.
- Act ordering beyond II: only the archive is committed in code ("locked · act II"). The order of
  workshops/ports/watch/ledger/broadcast is open — [DECISION-LUIS] D2.

— edited 2026-07-20 (completeness audit closure)

## 4. How the world grows

### 4.1 The reveal system [BUILT]
Growth is data, not level-loading. `applyReveal(key)` mutates the one persistent world; keys are
earned by missions, saved server-side (`/api/journey`, `SAVE.reveals`), and replayed idempotently
on boot. The full built table:

| reveal | granted by | what changes |
|---|---|---|
| plant_pollinations | M0.1 | socket + pollinations light to 1.0; labels on; embers ignite (.4) |
| foundry_all | M1.1 | all 15 plant labels; console lights .9; plant lights go live-driven |
| roads | M1.2 | row road emissive .35 |
| foundry_edges | M1.3 | meter obelisk lights; label on |
| trunk | M1.4 | trunk line .4; nexus lights; label on |
| foundry_full | M1.5 boss | roads .45 / trunk .55; fog 0.011 -> 0.009; embers .7 |
| archive_tease | M1.5 boss | archive silhouette + locked label spawn |

### 4.2 A building per forged organ [PLANNED]
Acts II+ extend the same law from lighting to construction: when a real organ comes online in the
entity, its building rises in its district. The prototype already proves the binding — city.html
drives building height and glow from live status (`organ status live -> level 1.15 vs 0.32`,
skills `live -> 1.0 vs 0.2`, services `auth ok -> 1.0`). The world.html port keeps reveals for
first-discovery and adds construction events for organ birth. A building may never appear for an
organ that does not exist — that is the honesty law applied to architecture.

## 5. World-events-are-real law [BUILT]

Binding: every light, number, and motion in the field is a read of the running entity. No
ambient-fakery pass exists and none may be added.

Built wiring (world.html):
- `/events?since=` polled every 1.6s — each real organ event becomes a HUD feed line
  (`organ.action detail`) and a pitch-mapped chirp. The feed is the entity's nervous system
  scrolling by.
- `/state` polled every 6s — plants-online count (HUD "plants n/15"), `life.ticks` (the OS TICK
  counter), memory count (HUD "ingots"). Plant emissive intensity tracks real load:
  `0.9 + min(.6, rpm_now/rpm_cap)`. A busy plant visibly burns brighter.
- `/autonomy` — HUD "class" and "tests passing" are the entity's live self-test results.
- Every mission DO beat calls a real endpoint (`/api/node/run`, `/state`) and `flashNode`s the
  plant that actually served — the flash IS the receipt. PROVE beats assert against live state
  (`runAssert`: last_ok_text / plants_online / multi_served / no_throttle / drill_clean). A
  mission can genuinely FAIL because the real grid is throttled; the fail text says so honestly.
- COMMS is the actual entity: `/talk` with the mission context prefixed, receipts show real
  latency, the real serving model, and real memories recalled. "no reply crossed the channel —
  the entity may be resting" is a true condition, not flavor.
- Model "specimens" (PROBE OS MODELS tab) are only models the player has actually caused to burn
  (`encounter()` on real ok calls) plus rods with real call history from `/state`.

Prototype wiring to port [PLANNED]: city.html's `reflect()` turns each event into a vehicle
driving the road from its source district to the spire, flashes the target organ building, and
pulses the spire on mind/life ticks — ticks light streets, draws move as traffic, HADES verdicts
flash the watch. Port for acts II+ with one correction: city.html used a red-ish bad color
(`0xff7a66`); under the two-ink law failure states are hot-amber blink + COOLING chips, never red.

The claim ceiling, quoted from the built SYSTEM screen (world.html `sysRender`): "every number on
these screens is live system truth. claim ceiling: measured functional correlate — never
'conscious'." That sentence is shipped UI, not aspiration; it governs all future world content.

## 6. Narrative voice [BUILT — law]

Terminal lowercase. Terse. Never purple. All world text (mission beats, feed lines, map detail,
comms) follows the register set in missions.js and world.html:

- Declaratives, short, full stops: "cold boot. no memory of why." / "the field is dark. one
  structure at the edge is drawing power."
- Mechanism as fiction, with the real mechanism shown in the same breath — every LEARN beat pairs
  a lore line with the actual code ("a prompt goes in. tokens come out. everything above this is
  architecture.").
- The entity speaks in first person about its own organs. Built example (map detail voice line):
  "— this part of me is mapped. it was always running; now you can see it." LEYBER never
  describes itself in third person; the probe and the SYSTEM voice never use "I".
- Failure text is honest and unglamorous: "the mouth starved — every rod refused. rare, and
  honest. retry." No blame, no drama, no fake stakes.
- Caps are reserved for names and states (THE GRID, FIRST LIGHT, PASS, COOLING) — the FUI layer,
  not the prose layer.
- No exclamation marks, no metaphors that outrun the mechanism, no emoji ever.

## 7. Palette and material law [BUILT — law]

Two inks (world.html `:root`, quoted): live amber `#ffb000` (hot) / `#d4a24c` (warm); structure
`rgba(120,155,175)` at exactly .35/.6/1. Background `#050a10`, fog `#0a1420`. No red, no green,
no white. 3D obeys the same inks: WARM windows/rings/roads, HOT probe core/beacon/embers,
structure-blue fresnel shells and backlights. Named deviation to resolve on port: city.html's
plant windows and some buildings glow white (`0xffffff` emissive) — world.html's warm-window
recipe is canon.

## 8. Open decisions [DECISION-LUIS]

- D1 — spire vs nexus: does the spire at `(0,0)` absorb the nexus (nexus becomes its foundry-side
  gate), or do both stand? Affects act II+ trunk extension.
- D2 — act ordering beyond II: recommended order archive (II, committed) -> watch (III — HADES
  before autonomy is fitting) -> broadcast/ports (IV) -> workshops/ledger (V). Awaiting call.
- D3 — privacy curbs in world.html: port city.html's gold-curb ward markers now (act I polish) or
  land them with act II construction?
- D4 — vehicles: port the event-traffic system as-is at act II, or hold until more than one
  district is lit so traffic has legible origins?

Phase note: this bible serves Luis as player one. Phase B (anyone building their own AEA by
playing) inherits every law above unchanged — the world can only ever show a stranger's entity as
truthfully as it shows LEYBER.
