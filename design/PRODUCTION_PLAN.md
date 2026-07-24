# HOW THE PROBE GETS BUILT — the production pipeline (top to bottom, the way studios do it)

*The methodology that makes ROADMAP.md executable and stops the oscillation. ROADMAP = what/when.
This = HOW: the layers, the data pipeline, the systems that sustain the design. Read with ROADMAP.md.*

## 1 · HOW GAME DEVELOPERS ACTUALLY DO IT

The professional pipeline, in order:
1. **Concept / pillars** — the fantasy, the one line, the 3–4 pillars everything is tested against.
2. **GDD (Game Design Document)** — the design bible: the core loop, systems, progression, content
   categories (maps, missions, characters), economy, UX/menus, narrative.
3. **TDD (Technical Design) / architecture** — the systems that SUSTAIN the design: the state model, the
   content pipeline, save, backend/API, rendering.
4. **THE ONE IDEA THAT CHANGES EVERYTHING — data-driven content.** Studios do NOT hand-code each map,
   mission, or character. They build a small number of **engine SYSTEMS** (a map system, a mission system,
   an entity system, a progression system, a dialogue system) that **load and run CONTENT authored as DATA**
   (JSON/config). A designer authors *missions* as data; the mission system runs them. You build the system
   ONCE, then scale the game by **authoring more data, not more code.**
5. **Vertical slice** — build ONE complete strip end-to-end (one map + one mission + one character) that
   exercises every system. Prove the pipeline, not the content.
6. **Production** — author the content (the maps, the missions, the characters) as data through the proven
   systems. The design layer feeds data down; the systems layer runs it.

**The spine, in one sentence:** *design becomes DATA; a few SYSTEMS run that data; the vertical slice proves
the systems; production is authoring data.* That is the "structure to sustain all that."

## 2 · THE PROBE IN THAT STRUCTURE (the three layers, top to bottom)

### LAYER A — THE DESIGN (the top: what the game is) — DONE, just scattered
Pillars: the thesis + honesty law + the AEA. GDD: `GAME_INVENTORY.md` (the BOM) · `THE_FIELD_GUIDE.md` (the
scenario) · `A17_VOCABULARY.md` (names) · `refs/REFS.md` (the visual bar). The three content categories:
- **MAPS** = the world (the concentric instrument, the 8 rungs, the privacy zones, the fog).
- **MISSIONS** = the guided curriculum beats (`brief · learn · do · observe · prove · ask`).
- **CHARACTERS** = the constructs/beings you compose · LEYBER (the guide voice) · the antagonists (runaway
  constructs — deferred).

### LAYER B — THE CONTENT AS DATA (the pipeline — the connective tissue)
Each content type = a **data schema** + the **system** that runs it. This is the layer we've under-built:

| content | the DATA | the SYSTEM that runs it | state |
|---|---|---|---|
| **MAP** | `/game/schema` (organs, zones, edges, fog) + rung/district data | the WORLD render (`engine.js`) | **EXISTS** |
| **MISSION** | mission JSON: beats `brief\|learn\|do\|observe\|prove\|ask`, the beacon, the gate | the **MISSION ENGINE** | **MISSING in web/game/** (world.html had one) |
| **CHARACTER / construct** | the part-signature + receipt + earned title (on disk: `r-01`) | the COMPOSER (`bench_core`) | **EXISTS, fires real** |
| **VOICE (LEYBER)** | line data keyed to beats/events | the mission engine surfaces it | data to author |
| **PROGRESSION** | the sacred save + the reveal ledger (what's de-fogged) | the SAVE system (`journey_save`) | **EXISTS** |
| **ANTAGONIST** | runaway-construct data (needs a running construct) | the GOVERNOR/METER (already the defense) | **FOG** (sequencing-gated) |

### LAYER C — THE SYSTEMS / ARCHITECTURE (the bottom: what sustains it)
The three rings: substrate `aea/` → the honesty seam `aea/gameapi/` → the client `web/game/`. The systems
inventory and its truth: composer **✓** · gameapi seam **✓** · world/schema **✓** · save **✓** · flight+dock+
bench merge **✓ (verified)** · render pipeline **✓** · **MISSION ENGINE ✗ (the one missing system)** · reveal
ledger (fog-lift) **partial** · the menu-views-over-data (map/codex/being-sheet/stats) **to build in Phase C**.

## 3 · THE MISSING PIECE (why it feels unfinished)

Everything the *bench* needs exists and works — the composer fires real constructs. What's missing is the
**MISSION ENGINE**: the data-driven system that turns "the loop can fire" into "a guided game with a
curriculum." It places the lit beacon, speaks LEYBER's line, waits for the real DO (fly / compose / ignite),
gates on the real PROVE (a real assert), fires the EARN/REVEAL, and advances to the next beat — **all read
from mission DATA**, not hand-coded. `world.html` shipped a mission loop (SLICE 1); it was never ported into
the merged `web/game/`. **That port + a data schema for missions is the connective tissue between the map, the
missions, and the characters.** Build it once; then every guided beat, every rung, is authored as data.

## 4 · THE ORDERED PLAN (top to bottom — follow this, do not jump)

**STEP 0 — vertical slice, systems (in progress).** The composer fires (✓). The bench renders to REF-10 (pass
2 done; finish it). This proves the CHARACTER system.

**STEP 1 — build the MISSION ENGINE (the missing system) + a mission data schema.** A small runner that reads
one mission JSON (`beats[]`, `beacon`, `gate`, `leyber[]`) and drives beats over the existing flight/dock/
bench/composer, gating on real events. This is the connective tissue — build it ONCE.

**STEP 2 — author MISSION 01 as data (the vertical slice's content).** The guided cold-open → fly to beacon →
LEARN → SEAT → IGNITE → READ → PROVE. One mission, authored as JSON, running through STEP 1. Now maps +
missions + characters are one playable strip, data-driven.

**STEP 3 — PRODUCTION: author the guided curriculum as data.** Missions 02…N (rungs 0–2) = more mission JSON,
NOT more code. The map de-fogs from the reveal ledger (data). The menus (map/codex/being-sheet/stats) = views
over the schema + save (data). Everything from here is authoring content the systems already run.

**STEP 4+ — the deferred layers** (BUILDER/ARCHITECT, the antagonist ecology, the other apertures) are new
SYSTEMS, built later — each proven by its own vertical slice, then scaled by data. Named as fog now.

## 5 · THE DISCIPLINE (why this ends the oscillation)

- **We build SYSTEMS and author DATA — never one-off screens.** A "menu" is a view over data (schema/save/
  missions). A "mission" is data. A "map" is data. A "character" is a real construct. The structure sustains
  the design because **the design IS data the systems read.**
- **The reference set grows with the build, not ahead of it.** 12 refs = the guided phase's bar. Each new
  surface gets its ref when its system is next (just-in-time). The whole game is captured at north-star level
  (the vision posters + the field guide); detailed refs arrive per phase.
- **Top to bottom is always:** design (a data spec) → the system that runs it → author the data → the game is
  the sum. When unsure what to do next, find the lowest-layer missing SYSTEM (right now: the mission engine)
  and build it, then author its data.

**The immediate next move under this plan:** finish the bench to REF-10 (Step 0), then **build the MISSION
ENGINE + author MISSION 01** (Steps 1–2) — that is the vertical slice completed, and the first time THE PROBE
is a *guided game*, not a bench that fires. Everything after is production: authoring data through systems
that already run.
