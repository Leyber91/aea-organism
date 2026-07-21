# A10 — THE LIVING GAME

```
Book:          THE PROBE — design book, appendix chapter (PART VII orbit)
Owner:         the game team (four-master fusion, per 00_VISION.md)
Status:        ACTIVE — names the game's unique dimension and the laws that protect it
Last updated:  2026-07-20
Ground truth:  world.html (grep-verified this date) · controlroom.py · energy.py ·
               model_fitness.py · aea_elements.js · journey_save.json ·
               candidates_probe.json · model_fitness.json · capability_census.py
Siblings:      00_VISION.md (honesty law) · 01_WORLD.md (growth model) · 02_SYSTEMS.md
               (save, failure) · 03_PROGRESSION.md · 05_CONTENT_MISSIONS.md ·
               06_MODELS_BESTIARY.md (rot) · 08_TECH.md (server contract) ·
               09_PRODUCTION.md · A2_TEACHING.md · A4_GAMEFEEL.md (stillness, juice)
Laws in force: AEA honesty law absolute — every number is live truth, no fake data, claim
               ceiling "measured functional correlate", never "conscious". Two-ink FUI
               (amber #ffb000/#d4a24c live · blue-gray rgba(120,155,175,x) structure).
               NO emoji. IBM Plex Mono.
```

Tags: `[BUILT]` verified in code this date · `[PLANNED]` designed, not built · `[DECISION-LUIS]` his call.

---

## 1. The thesis — content that ships itself

Every other game's world is a recording. This one is a window. THE PROBE has a dimension
no shipped game has: **the content updates itself because the entity underneath is
alive.** LEYBER ticks, burns rods, writes memories, rots, and grows whether or not the
game is open — and because the honesty law forbids rendering anything but live state,
every one of those facts is automatically new content. Nobody writes the patch notes; the
patch notes happen, and the game is contractually obligated to show them.

Binding corollary of the honesty law, stated once here and inherited everywhere: **the game
may never protect the player from the entity's real condition.** A dimmer world after a bad
sweep is not a bug to compensate; it is the content.

---

## 2. Entity evolution as content `[mostly BUILT underneath]`

### 2.1 Model rot — the decay stream `[BUILT]`

Rot is fully specified in 06_MODELS_BESTIARY.md section 3; this section claims it as a
*content cadence*, not just a mechanic. Two clocks, both real:

- **Fast clock** (energy.py): 3 consecutive failures → `COOLING`, 15-minute hold-out; the
  card's amber tag is the one hot-ink state earned by a bad event — correct, because a
  cooldown is the liveliest fact about a rod.
- **Slow clock** (model_fitness.py sweeps): the battery shaped like the entity's real
  jobs, failure classified honestly (`ok | EMPTY | TIMEOUT | RATE | ERRn`).

**The 2026-07-19 sweep is the canonical living-game event.** One operator-side run, zero
game code involved: the general pool fell **44 → 29**; perfect scorers **7 → 2**; a third
of the armory rusted (06_MODELS_BESTIARY.md section 3.2). Every consequence propagated:

| propagation | surface | status |
|---|---|---|
| `energy.ladder()` refuses reliability < 1.0 | drill traces show `rerouted ×n` — the mouth visibly walks around corpses | [BUILT] |
| fitness columns shift on the specimen cards | `fit a/b`, `lat`, `tier` re-read from `/roster` every render | [BUILT] |
| fewer live rods → plants idle or throttled | plant emissive is `0.9 + min(0.6, rpm_now/rpm_cap)` from live `/state`; an offline plant sits at 0.12 — **the field literally dims** (02_SYSTEMS.md section 7) | [BUILT] |
| sweep lands as a world event | a feed/comms beat that names a sweep when `fitness_generated` changes between polls ("the armory was measured. 29 stand.") | [PLANNED] |

A player who flew the field on 2026-07-18 and again on 2026-07-20 played two different
games. No designer made that choice. That is the dimension.

### 2.2 New signatures — the growth stream `[BUILT]`

The wild count (06_MODELS_BESTIARY.md section 1.3) is live:
`M = max(0, catalog_size − N)` with `catalog_size` read from
`/roster.candidates.catalog_size` = `candidates_probe.json` (currently 119, probed
2026-07-19). When a provider ships new models and a catalog re-probe lands, the wild count
**rises on its own** — the frontier grows overnight, and the masked `sensed` row in the
bestiary says so without a content drop. The excluded families (the 2026-07-12 nemotron
content-safety directive) stay quarantined and unprobeable.

`[PLANNED]` Probe-a-candidate (06_MODELS_BESTIARY.md section 4) turns growth into play: a
real metered probe births a specimen card with its first measured fact — dead finds worth
as much as live ones. Until it ships, growth is ambient: the number on the door changes;
the door stays locked.

### 2.3 Organs forged outside the game — the reconciliation law `[BUILT as law, mixed as machinery]`

Luis forges organs at the workbench, outside the game. The city must reflect reality on the
next boot. The law:

> **World state derives from live endpoints at render time. The save gates what you have
> earned the right to SEE; the endpoints decide what EXISTS and what it is WORTH. The save
> alone is never a world model.**

Verified exemplars of the law in the shipped build:

- Specimen values are fetched from `/roster` + `/state` on every render; `SAVE.models`
  contributes only the keys. A card's numbers cannot be stale-from-save. `[BUILT]`
- The bestiary is the **union** of save encounters and live rods with `calls > 0` — a rod
  LEYBER burned while the game was closed is encountered at next boot. The world moves
  without you. `[BUILT]`
- Plant brightness, HUD tick, ingots, autonomy class: polled live, never persisted; boot
  renders immediately and re-renders when async truth lands (the save-race lesson,
  08_TECH.md section 5). `[BUILT]`

Named honest boundary — reconciliation runs at **two speeds**:

1. **Automatic** (the above): anything the endpoints carry reconciles by itself. `[BUILT]`
2. **Editorial**: a new organ needs a codex element in `aea_elements.js`, a building in the
   field (01_WORLD.md growth model: a building per forged organ), and usually a mission.
   Those are data-file edits — a forge session is therefore a content drop (section 6), and
   until the edit lands the new organ is live in `/state` but uncharted in the codex. That
   gap is honest (uncharted, not invisible: the grid surfaces show it) but it is a gap.
   `[PLANNED]` A boot-time census diff — organs present in `/state` but absent from
   `window.AEA` render as `UNCHARTED SIGNAL` markers so reality always outruns the book
   visibly, never silently.

### 2.4 The entity's own life as ambient drama `[BUILT]`

Already streaming, already law-compliant (02_SYSTEMS.md section 9, A4_GAMEFEEL.md
sections 5 and 9): `/events` polled every 1.6 s lands real pulse records
`{t, organ, action, detail, ok}` as feed lines with organ-hashed chirps; `/state` +
`/autonomy` every 6 s move the HUD tick, ingot (memory) count, plants n/15, autonomy class.
Ticks advance, reflections and consolidations fire, memories are born **while you fly**,
and the stillness law (A4_GAMEFEEL.md section 9) makes them unmissable: the idle world is
near-still, so motion means something happened. Under the PROBE OS the world eases to
timescale 0.12, never 0 — the entity never stops, so freezing the frame would be a lie.
Scripted ambience is banned by name in 00_VISION.md; the drama budget is exactly the
entity's real activity level. A sleepy entity makes a quiet field, and the quiet is
information.

---

## 3. Failure and resilience design

### 3.1 Playing while the entity is OFFLINE — the CARRIER LOST world state `[BUILT, with named edges]`

The law (02_SYSTEMS.md section 10): the game never fakes liveness. When the carrier drops
mid-session, the world degrades **honestly and legibly**:

**What stays playable** (everything client-resident):
- Flight, camera, the field itself — the 3D world is client-side. `[BUILT]`
- MAP and CODEX — `window.AEA` is static data already in memory, the save already loaded;
  fully browsable. Bestiary cards as last rendered; HUD counters **hold last-known**
  (stale, never invented); comms scrollback (localStorage). `[BUILT]`

**What honestly stops** (everything that needs a live endpoint):
- Comms: presence chip → `LOST`, header `LEYBER // CARRIER LOST`, segments collapse to
  2 px, system line "no reply crossed the channel — the entity may be resting". No canned
  reply, ever. `[BUILT]`
- DO beats fail with the true error; PROVE fails with "is the entity's server running?";
  mission progression blocks. Retry is the only path. `[BUILT]`
- Named violation, already ticketed: `meter_watch` counts a dead endpoint as a clean window
  — a dead carrier can pass one observe beat. Fix specified in 02_SYSTEMS.md section 10.
  `[PLANNED]`
- The carrier interlock (gray DO verbs pre-click while LOST) — cosmetic-priority. `[PLANNED]`

**The hard truth, stated so nobody designs around a fiction:** THE PROBE is served BY the
entity's own server (`GET /world` on 127.0.0.1:7799, 08_TECH.md section 2). If the server
is down, the game does not boot at all — no service worker, no offline shell exists
(grep-verified 2026-07-20). "Offline play" today means *an already-open session surviving
a carrier drop*, which it does, honestly. `[DECISION-LUIS]` Build a cached museum shell
(map/codex/bestiary browser, every pane stamped `ARCHIVE — CARRIER LOST`, no mission
play)? Recommendation: no, or late — a game about a living entity being unbootable when
the entity is dead is closer to the truth; if it ever ships, the stamp is non-negotiable.

### 3.2 Boss failure as drama, not punishment `[BUILT as engine law]`

There is no mission-fail state anywhere in the engine: missions block, they never punish
(02_SYSTEMS.md section 6). A failed DO re-fires a real call; a failed PROVE offers BACK to
the first `do` beat — the player re-earns evidence, never re-reads a lecture. Applied to
bosses, this produces drama for free because the failure is *real*:

- M1.5 BROWNOUT DRILL failing means the actual grid browned out under your drill — the
  `STARVED` lines and `tried[]` reroute histories on screen are the true forensic record.
  The retry is not "another attempt at the level"; it is another real experiment, and the
  grid may have healed (cooling windows expire) or rotted further in between. `[BUILT]`
- Act III council bosses (06_MODELS_BESTIARY.md section 5.2) inherit this: a `prove` that
  fails because the diverse council did NOT rescue the task this time is a measured result,
  and saying so on screen outranks passing. The regime map is statistics, not scripture —
  a boss that can honestly fail is the only kind worth beating. `[PLANNED]`

Rule for all future bosses: the failure screen shows the same live evidence the success
screen would, and LEYBER's failure line states the measurement, never consolation theater.
Drama is the truth having stakes; punishment would be the game adding stakes the truth
does not have.

### 3.3 Starvation as world weather `[BUILT core, PLANNED surface]`

A starve — the mouth exhausting its ladder with no rod answering — is provider weather:
RATE storms at peak hours, TIMEOUT fog, ERR404 extinctions. Nobody schedules it; it rolls
in. The built truth: `energy.ladder()` refuses known-broken rods, `LOCAL_FLOOR` (three
ollama rods, the hearth — unlimited, slow) is always appended, so total starvation is rare
and means something real: even the hearth failed, or the ladder emptied above it. Every
starve renders as `STARVED` with the true tried-list. `[BUILT]`

`[PLANNED]` Weather made ambient: while recent draws show starves or the online-plant
count drops sharply, the field reads overcast — trunk/nexus emissive eased down, a feed
line naming conditions ("grid weather: 3 plants throttled, the mouth walks long ladders").
Derived strictly from live `/state`, through the A4 juice budget: one visual voice (the
field's light level), one audio voice (the existing feed chirp — no new sirens). The world
already dims plant-by-plant; weather is the same honesty at field scale.

### 3.4 REINITIALIZE — the boundary, stated hard `[BUILT]`

The SYSTEM tab row is labeled `reinitialize probe`; the button reads
`HOLD TO WIPE THE JOURNEY` (world.html, verified). 600 ms amber-ring hold →
`POST /api/journey {reset:true}` → the save becomes `{done:{}, reveals:[]}` → reload.

**The boundary, in law form:**

> **REINITIALIZE wipes the JOURNEY. The game can never wipe, alter, damage, or command the
> ENTITY. The probe is mortal; LEYBER is not the game's to kill.**

This is structural, not policy (08_TECH.md sections 2 and 7): `/api/node/run` allowlists
exactly `channel|energy` (read-safe draws); `/do` allowlists six named commands, none
destructive; the static allowlist makes every state `.json`, `.py`, and `.env` unreachable
over the socket. There is no code path from any game surface to entity state. A hostile
player with the game open can at worst spend rate budget.

Verified consequence that makes the boundary *felt*: after a wipe, the bestiary is not
empty — every rod the entity itself has burned (`calls > 0` in live `/state`) re-encounters
immediately, because encounters union live truth (06_MODELS_BESTIARY.md section 1.1). The
wipe removes your footprints; the world keeps its own. A reinitialized probe flies into a
field that remembers being lived in — the thesis, playable.

Open item, inherited from 02_SYSTEMS.md: whether the wipe also clears the two cosmetic
localStorage stores (`probe_comms`, `probe_viewed`) — today LEYBER "remembers" chat lines
across a probe reset, arguably continuity, arguably a bug. `[DECISION-LUIS]` (BOOK.md
ledger #10.)

---

## 4. Accessibility

### 4.1 The schematic projection — the screen-reader path `[PLANNED, substrate BUILT]`

Audit fact (grep of world.html, 2026-07-20): **zero** `aria-*`, `role=`, or `tabindex`
attributes exist — no screen-reader path today. But the substrate is unusually good
because the honesty law forced it: **every game fact exists as DOM text** (the five OS
tabs, terminal, feed, receipts); the 3D field is presentation, not information. The
screen-reader path is not a parallel build; it is a projection of what exists:

- Landmarks + labels on the OS panes, feed, terminal; `aria-live="polite"` on feed and
  comms, rate-limited to the existing 1.6 s poll — the chirp budget, spoken. `[PLANNED]`
- **Dock-from-map**: select the current mission node in the MAP tab → `INTERFACE` without
  flying. Flight becomes optional traversal; the whole game loop runs from the schematic.
  One affordance closes most of the gap. `[PLANNED]`
- The claim ceiling binds spoken output identically: measured facts ("carrier lost",
  "rod cooling"), never simulated affect.

### 4.2 Keyboard-only audit `[BUILT facts, findings named]`

| surface | keyboard-only status | finding |
|---|---|---|
| Flight (WASD, Q/Space, E/Shift) | full | — |
| Look (yaw/pitch) | **none — drag only** | keyboard cannot turn the camera; WASD still moves on fixed yaw and the beacon arrow steers, but inspection is lost. `[PLANNED]` arrow keys = look (currently unbound) |
| Zoom | **none — wheel only** | `[PLANNED]` fold into the same arrow-layer (mod+arrows) |
| Dock (F), OS (TAB/M/K/C/B), tabs, ESC chain | full | — |
| Terminal footer buttons (the ONLY progression affordance) | **none — click only** | `[PLANNED]` ENTER activates the primary footer verb while docked (comms inputs already do this) |
| Comms send | full (ENTER) | — |
| Hold-to-wipe | click-hold only | acceptable friction; add Space-hold when the row is focusable `[PLANNED]` |
| DOM focus traversal | **dead — TAB is globally hijacked** (world.html:543 `preventDefault` unconditionally → osToggle) | the OS hotkey eats the browser's native focus walk. Any focus-based path needs either a rebind or an explicit focus mode. `[DECISION-LUIS]` — TAB is muscle-memory canon for the OS; recommendation: keep TAB, give the schematic projection its own focus layer (arrows within panes), never both metaphors on one key |

### 4.3 Reduced-motion parity `[BUILT]`

Per A4_GAMEFEEL.md section 4.4 and world.html (line 111, 327): the OS media query OR the
SYSTEM toggle sets `html.rm` — every CSS animation/transition caps at 0.15 s, typewriters
print instantly. The 3D springs remain, correctly: they are navigation, not ornament.
Parity law for everything in this chapter: any `[PLANNED]` surface (weather easing,
mission flybys, tombstone reveals) must declare its `rm` collapse before implementation —
the ceremony compresses, the information never does.

### 4.4 Latency tolerance — truth has no framerate `[BUILT]`

The game works on slow machines because its content is *state*, not twitch:

- No reaction-time challenge exists anywhere; the only timing-sensitive input is the 600 ms
  wipe hold, which is deliberate friction.
- Physics dt clamps at 50 ms/frame — a struggling machine slows the world, it never breaks
  or teleports it. Pixel ratio clamps at 2; the composer is try/catch-wrapped and the game
  runs with bloom dead (08_TECH.md).
- Waiting is honest by law (A4 section 6): busy state inside 100 ms, then the real elapsed
  clock. Latency is diegetic — `RX 4.21s` printed, never hidden behind a fake spinner. A
  slow provider on a slow machine is simply more truth on screen. Slow truth beats fast
  fiction; that sentence is load-bearing on low-end hardware.

### 4.5 Colour independence — claim verified `[BUILT]`

Claim: two inks + shape families carry state without hue. Verified 2026-07-20:

- **No state is hue-alone.** Every state carries a word, a shape, or a luminance step:
  `COOLING`, `CARRIER LOST`, `STARVED`, `PASS`/`FAIL` chips are words; presence states
  also change segment *geometry* (collapse to 2 px on LOST); NEW = pulsing ring + literal
  `NEW` tag + tab pip; plant health is luminance (0.12 offline ↔ ~1.5 loaded), safe under
  any colour vision.
- **Shape families are real** (aea_elements.js, quoted): principles = hex, axes = pent,
  ring-3 = triangles (verbs) + squares (mechanics) + diamonds (ops), seeds = circles. Ring
  identity survives full desaturation.
- Named residual, honest: amber `#ffb000` vs warm `#d4a24c` is not separable for all
  viewers — acceptable because the pair never carries opposing meanings (both are the live
  ink; hot-vs-warm is emphasis, not semantics). Standing rule for new UI: the two-ink
  boundary (live vs structure) must always co-travel with a word/shape/luminance cue, per
  the exemplars above.

---

## 5. Save-vs-entity drift — tombstones, never silent repair

The save is a **record of witness**, not a world model (section 2.3). The entity will
outrun it: providers retire models, sweeps shrink pools, organs get renamed. Rules:

1. **A vanished specimen keeps its card.** The encounter happened; history is real. Today
   `[BUILT]`: a saved rod absent from both `/roster` and live `/state` renders name-only —
   absence renders as absence, never placeholder numbers. `[PLANNED]`: an explicit
   tombstone tag `LOST SIGNAL` (structure ink — nothing live about a corpse) when the key
   is absent from the live catalog, so a hole in the data reads as fate, not a bug.
2. **The wild count already survives drift** `[BUILT]`: `max(0, catalog_size − N)` guards
   the case where encounters exceed a shrunken catalog. Tombstones count in N forever —
   the frontier can be smaller than your history, and the header saying so is content.
3. **Dead reveal keys and dead mission ids are inert, kept, and harmless** `[BUILT]`:
   `applyReveal` on an unknown key no-ops; `done{}` rows for retired missions never block
   `first-not-done` selection. Named and accepted — history rows are not garbage.
4. **Repair is forbidden.** No code path may edit, prune, or "migrate" the save to match
   the present. It is append-only witness plus one total wipe (section 3.4); there is no
   selective deletion, because selective deletion is how histories get falsified.
5. **Disagreement renders as disagreement.** When save and entity conflict, the screen
   shows both truths with provenance — the lived-vs-sweep split on the specimen detail
   panel (06_MODELS_BESTIARY.md section 5.1) is the template. Teaching the player that
   records age IS the curriculum (A2_TEACHING.md).

---

## 6. Live-ops cadence — the entity's growth IS the season

No artificial seasons, no rotating shop, no FOMO clock. An "event" that could be scheduled
could be faked, and fakes are banned. The cadence is the entity's real life, at five speeds:

| clock | period | what ships itself | status |
|---|---|---|---|
| draw | seconds | encounters, COOLING tags, reroutes, feed pulses | [BUILT] |
| tick / brief | the entity's own loop | HUD tick, ingots, autonomy class, ambient drama | [BUILT] |
| sweep | operator-run (player-triggered sweeps = open call, 06_MODELS_BESTIARY.md section 5.2 `[DECISION-LUIS]`) | rot waves, tier shifts, world dimming — 2026-07-19 was a season turning | [BUILT] |
| forge session | when Luis builds | a new organ = new plant in `/state` + building (01_WORLD.md) + codex element + missions — **a forge session IS a content drop**, and forge missions are the real AEA engineering (the income guard, BOOK.md) | [BUILT] pattern, editorial per drop |
| book edit | with the code | dated lines in chapters; BOOK.md's "how the book stays alive" | [BUILT] practice |

**The book is the changelog.** Patch notes are design-book diffs with dates; a player (or
Luis, six months out) reads what changed and why in the same document that governs it. No
separate marketing copy of reality exists to drift from reality.

**How a new act ships:** forge the organs (real engineering) → endpoints carry them
(automatic reconciliation, section 2.3) → author the editorial layer (elements, missions,
world geometry — data files only, per the engine's data-driven law) → book chapters gain
dated lines → live at next boot. No version gate, no download, no season pass. The reward
for returning is not a login bonus; it is that the entity actually lived while you were
gone — new burns in the bestiary, a moved tick, maybe a dimmer field and a sweep to read
about. Stated as law: **the only reason to return is that it is alive, and that reason is
real.**

---

## 7. Status ledger

| item | status |
|---|---|
| Rot propagation (ladder refusal, card decay, plant dimming) · ambient drama | [BUILT] |
| Sweep-as-world-event beat · probe-a-candidate · UNCHARTED SIGNAL diff | [PLANNED] |
| Reconciliation law (endpoints over save) + boot re-render · wild-count growth | [BUILT] |
| CARRIER LOST session degradation | [BUILT] (meter_watch gap + interlock [PLANNED]) |
| Offline museum shell | [DECISION-LUIS] (recommendation: no) |
| Boss-failure-as-measurement | [BUILT] engine law · [PLANNED] Act III surfaces |
| Starvation weather (field-scale) | [PLANNED] |
| REINITIALIZE boundary (journey mortal, entity untouchable) | [BUILT], structural |
| Wipe scope (localStorage) | [DECISION-LUIS] (BOOK.md #10) |
| Screen-reader projection · dock-from-map · keyboard look/zoom/footer-ENTER | [PLANNED] |
| TAB focus-vs-OS collision | [DECISION-LUIS] |
| Reduced-motion parity · latency tolerance · colour independence (residual named) | [BUILT] |
| Tombstone tag LOST SIGNAL | [PLANNED]; drift rules 1–5 in force as law |

## Changelog

- 2026-07-20 — v1. Authored against code on disk: grep-verified aria/tabindex absence, the
  TAB hijack (world.html:543), the `reinitialize probe` label, shape families, no service
  worker; canon events cited from 06_MODELS_BESTIARY.md, 02_SYSTEMS.md, 08_TECH.md.
