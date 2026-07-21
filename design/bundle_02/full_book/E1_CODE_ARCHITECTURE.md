# E1_CODE_ARCHITECTURE — THE CODE DOCTRINE

```
doc:          E1_CODE_ARCHITECTURE.md (THE PROBE design book — engineering layer)
owner:        the game team (principal-engineer hat)
status:       ACTIVE — the doctrine every P0+ code session builds under
last-updated: 2026-07-20
ground truth: world.html (1,143 lines, wc-measured this date) · controlroom.py (641 lines,
              re-measured at closure — the file grew the /api/tickets + /tracker routes after
              this doc's first read) · missions.js · aea_elements.js · grid.py · energy.py ·
              08_TECH.md (stack law) · P0_PROTOTYPES.md incl. the P0 SPEC ADDENDUM (binding) ·
              A14_MODULE_REGISTRY.md
laws:         honesty law absolute — every number below was read from the files, not
              remembered. Citations anchor on SYMBOL NAMES (_journey, CURATED, do_GET);
              line numbers are the 2026-07-20 snapshot, courtesy only, re-verified (grep
              the symbol) at the start of any session that uses them. Two-ink FUI
              (amber #ffb000/#d4a24c live · blue-gray structure). NO emoji. Claim ceiling
              holds in code comments too.
governing:    Luis's law — THE TECH-STACK CHOICE HAPPENS ONCE THE MVP WORKS. P0–P3 build
              on the current stack. This chapter hardens that stack; section 6 is the
              gated decision, and nothing above section 6 depends on it.
marks:        [BUILT] verified in code on disk · [PLANNED] designed, not built ·
              [DECISION-LUIS] awaiting his call
```

---

## 0. What this chapter is

Not a rewrite plan. The recorded failure of this workspace is brilliant strategy, zero
artifacts — a rewrite proposal before the MVP would be that failure wearing an
engineering hat. This chapter does three things only: states honestly what the code is
today, sets the rules that keep it strong through P0–P3 on the CURRENT stack, and parks
the stack decision behind the MVP gate where Luis's law put it.

---

## 1. THE HONEST AUDIT (2026-07-20, from disk)

### 1.1 What is strong — keep, and imitate

- **Durable-state discipline [BUILT]** — grid.py's three helpers are the best code in the
  project: `atomic_save_json` (write-temp then `os.replace`, a kill mid-write can never
  truncate a store), `load_json` (corrupt file quarantined LOUDLY, never silently
  cemented), `file_lock` (cross-process msvcrt lock that degrades rather than deadlocks).
  The Meter is stateless-over-file: every operation a locked read-modify-write, any
  number of instances share one truth (grid.py:225–330). `_journey` in controlroom.py
  already saves through this idiom (controlroom.py:500–523). This is the house style for
  ALL state, forever.
- **No build step [BUILT]** — one HTML file plus flat scripts, served by the entity's own
  stdlib server, runs from a plain browser. Zero toolchain rot, zero dependency surface,
  the whole game greppable. This is a real asset, not a naivety (see section 6 before
  disagreeing).
- **Allowlist serving [BUILT]** — `_static_path` (controlroom.py:273–279): flat basenames
  only, extension allowlist only, so `luis_memory.json`, `*.md`, `*.py` are unreachable
  over the socket by construction. Bound to 127.0.0.1 as a literal, not a config.
- **Honesty plumbing [BUILT]** — `window.onerror` paints into `#err`; the composer is
  built in try/catch and the game survives bloom death; energy.draw returns `tried[]`
  (the real routing history) instead of pretending; empty text counts as failure.
- **Data/engine split already begun [BUILT]** — missions.js and aea_elements.js are pure
  data files ("data only: the engine lives in world.html"). The module plan below
  extends an existing idiom, it does not invent one.

### 1.2 What will rot at P3 scale — named, with line numbers

The client is 1,143 lines today and healthy. P3 adds seven action types, three missions,
archive geometry, coach-marks; P0 adds the bench. At ~2,500+ lines the single inline
script becomes the place where every session pays a reading tax and every regression
hides. The specific rot vectors, each named against today's code:

1. **The monolith itself.** One inline `<script>` owns scene, input, missions engine,
   OS, map, comms, HUD, audio, boot. Every new feature edits the same file; two
   parallel sessions on it will collide; nothing is testable in isolation.
2. **Geometry/material/texture dispose on reveal-rebuilds.** Today reveals mostly toggle
   emissive intensity (cheap, safe). But: `makePlant` clones a CanvasTexture per plant
   (world.html:434); the socket reflection clones every material of a whole group
   (world.html:494–495); `buildArchiveTease` allocates three boxes plus a backlight
   sprite (world.html:504–509). P3 "promotes archive geometry from the built tease" —
   the FIRST real rebuild. Without the section 3 checklist, the tease's geometries,
   materials, and the sprite stay resident in the GPU pool forever. The LUMEN lesson
   (never churn the context pool) is already memory-tier law; this is its r128 form.
3. **Event-listener accumulation on OS re-renders.** Current code is mostly safe by
   accident: it assigns `el.onclick=` on freshly rebuilt nodes (sysRender, mapRender),
   and property assignment cannot stack. The rot arrives when a module attaches
   `addEventListener` to `window`/`document`/`renderer.domElement` in a render path
   instead of an init path — the drag/key/wheel handlers (world.html:542–559) are
   boot-time today, but bench.js and coach-marks will be tempted. Law in section 3.
4. **The trail/dust/ember buffers.** Three permanent Float32Array-backed
   BufferGeometries (trail world.html:523–528, dust :398–404, embers :406–412), mutated
   per frame with `needsUpdate`. Fine as built. The named risk: any future "rebuild the
   field" path that re-runs this setup allocates NEW GPU buffers while the old attach to
   nothing — the census test (section 3.2) exists to catch exactly this.
5. **setTimeout chains in typeInto / observe pollers / flashNode.** `typeInto`
   self-reschedules and stores its handle in the single shared `typing` var
   (world.html:614–617) — a second typer overwrites the handle, and the orphaned chain
   does NOT run quietly to completion: the next `runBeat`'s `body.innerHTML=''` detaches
   its span, so the orphan throws on `el.parentNode.scrollTop` (world.html:616) and dies
   into `#err` — the test asserts THAT symptom. `runObserve`'s meter_watch poll
   (world.html:740–750) self-reschedules with NO handle at all: close the dock
   mid-observe and it keeps hitting `/state` for up to 60s — and the worst case is not a
   dead-footer repaint: if the player re-docks, the stale `doneFn`'s `foot()`
   (world.html:611) replaces the ACTIVE beat's buttons with a stale continue whose
   `next()` mutates the GLOBAL `BI` (world.html:622) and can `completeMission()` the
   stale closure's mission — mission-state corruption, not cosmetics. `flashNode`
   (world.html:760–761) is the same class: an un-owned 650ms setTimeout capturing
   `keep` — two flashes on the same node within 650ms restore `tgt` to the ELEVATED
   value, a node stuck bright with no live cause (an honesty-law display bug); fix is a
   per-node timer handle + restore to a recorded base level. A bug factory at P3 when
   `mine_watch` joins.
6. **Fetch loops without abort.** `api()` (world.html:591) has no timeout and no
   AbortController. `pollEvents`/`pollTracks` (world.html:1035–1051) recurse forever
   with silent `catch(e){}` — on a hung (not dead) server a fetch can stall a loop
   indefinitely. Worst case is `cSend` (world.html:994–1026): if `/talk` hangs, the
   waitTimer spins forever and `cBusy` never releases — comms permanently locked for
   the session. The bench run-poller (P0) must not inherit this.
7. **WebGL context loss unhandled.** No `webglcontextlost`/`webglcontextrestored`
   listeners anywhere. A GPU reset (driver update, sleep/wake, another tab's churn)
   currently kills the scene silently with the HUD still lit — a live-truth game
   showing a frozen world is an honesty-law violation. One listener pair + the CARRIER
   LOST treatment (A10) fixes it. [PLANNED — small, rides P0]
8. **DOM growth without pruning.** `#c-feed` appends message divs unbounded in-session
   (world.html:980; the localStorage transcript is capped at 40 but the DOM is not).
   `#feed` prunes to 4 — correct; imitate it.
9. **Duplication drift, client vs server.** `MODEL_FOR` (world.html:685–687) hand-copies
   controlroom.py's `CURATED` table (:469–473) — and the drift HAS ALREADY HAPPENED:
   MODEL_FOR carries `openrouter`, CURATED does not; latent only because no mission and
   no channel_multi order names openrouter today. The server refuses non-curated pairs,
   so the drift surfaces as user-visible failures the day anything names that plant.
   One source: server echoes the curated table (ride /state or a tiny endpoint — the P0
   session records which transport won in its 09 ledger line) and the client reads it.
   [PLANNED — rides P0, NON-OPTIONAL]
10. **controlroom.py's elif ladder.** `do_GET` is ~150 lines of repeated
    open-file/encode/elif (controlroom.py:281–433). Every new page is copy-paste — the
    ladder already grew `/api/tickets` (:352) and `/tracker` (:358) the same day this
    doc was first authored, confirming the prediction — and P4 adds `/api/manifest`.
    It needs a routes table, not a framework (section 2.3).

None of these blocks P0 from starting. Items 2, 3, 5, 6, 7 become the standing
discipline (section 3) and the two small tickets (7, 9) ride P0.

---

## 2. THE MODULE PLAN — inside the current stack

No bundler, no ES modules, no import maps (08_TECH stack law — r128 global build).
The split is flat-served plain scripts, exactly like missions.js today. The allowlist
already serves `.js`; zero server work.

### 2.1 The client split [PLANNED — extraction schedule below]

Load order extends the law as it exists ON DISK (world.html:312–321: three.min.js, then
the data files missions.js / aea_elements.js, then the six-file bloom chain, then the
inline boot script) — modules load after the bloom chain, before boot:

| file | owns | extracted at |
|---|---|---|
| `engine.js` | scene, sky, ground, particles, probe, beacon, fresnel/dot helpers, the animate loop, resize, context-loss | P3 (with the archive rebuild — the first session that must touch scene lifecycle anyway) |
| `os.js` | PROBE OS shell, tabs, map/codex/models/system renderers, comms | P3 |
| `bench.js` | THE BENCH: construct spec load, run poller, trace-wire pane, record readout | **P0 — born as a module, never lives in world.html** |
| `missions-engine.js` | beats, dock terminal, runAction/runObserve/runAssert, reveals | P3 (it gains seven action types there; extract before adding) |
| `hud.js` | corner HUDs, feed, labels, arrow, prompt, hints, presence | P3 or first session that edits it, whichever first |
| `world.html` | markup, CSS, boot sequence, the GAME object + bus (below) | remains the spine |

Module birth ritual (written so a stranger can do it): the script tag goes after
UnrealBloomPass.js and before the inline boot script; the boot sequence calls each
module's `init(GAME)` in table order, after GAME is constructed; `dispose()` is wired at
birth even while nothing calls it; screenshot before the session's real work starts.

Per-frame seam — named now, built at the P3 engine.js extraction: engine.js exposes a
frame-hook registry, `GAME.onFrame(fn)`, registered in a module's `init()` and released
in its `dispose()`. hud.js and missions-engine.js are its two immediate callers (the
animate loop as built executes their ownership every frame, world.html:1087–1138), so
the abstraction is born with its second caller already existing — never per-frame bus
traffic, never cross-module reaching.

Extraction discipline: NEVER a big-bang refactor session. A module is extracted in the
same session that must materially edit that region, as its first step — cut, paste,
serve flat, verify a screenshot, then do the session's real work. P0 creates only
bench.js. If P3 runs long, missions-engine.js is the priority extraction and the rest
wait. An extraction session with no feature attached is scope inflation, named.

### 2.2 THE ONE BOUNDARY RULE [PLANNED — born at P0] (binding from P0)

**Modules communicate through a single game-state object plus one event bus. No other
cross-module globals — none.**

- `window.GAME` is the ONLY global the game adds (data files keep `window.MISSIONS` /
  `window.AEA` — freezing them is [PLANNED — two lines, rides P0]; no Object.freeze
  exists on disk today). `GAME.state` holds what is now scattered — SAVE, CTX, OS,
  NODES, LABELS, flags — at P0 by REFERENCE, not relocation: `GAME.state.save = SAVE`,
  `GAME.state.nodes = NODES`, and so on. Aliasing, never a wholesale move; physical
  ownership migrates per module at that module's extraction rung (2.1). bench.js codes
  against `GAME.state` from birth; world.html churn at P0 is ~10 lines. `GAME.bus` is
  a ~15-line emit/on/off pub/sub.
- The interregnum, ruled: world.html's inline script is grandfathered as ONE implicit
  module until its regions extract. Its existing globals are legal until each region's
  extraction session moves them into `GAME.state`; any NEW cross-surface state added
  from P0 onward goes in `GAME.state`, even when written inside world.html.
- A module reads `GAME.state`, emits events (`mission:complete`, `reveal:applied`,
  `os:open`, `run:link`, `carrier:lost` — a vocabulary, not a to-do list: an event gets
  its emit plumbed on its FIRST real listener, never before; at P0 only `run:link` has
  a producer-consumer pair, and speculative emits into world.html are the §1.2-audit
  defect class), and listens for the ones it renders from. It NEVER calls another
  module's internals by name. If two modules need a function, it lives on GAME or the
  caller owns a copy — no reaching.
- Each module exposes exactly `init(GAME)` and `dispose()`. `init` attaches listeners
  (DOM and bus) and records every handle it takes; `dispose` releases all of them.
  P0 gives dispose its first real caller: bench.js `dispose()` wires to the bench
  undock/pane-close path, so the 3.1.7 AbortController release runs through it — the
  seam is real from birth, not ceremonial. The discipline exists so the leak tests
  (3.2) have a seam to test against and so P10's bench relocation is a move, not a
  rebuild.
- Server truth stays server truth: modules never cache `/state` beyond one poll cycle.

### 2.3 The server split [PLANNED — at P4, when /api/manifest lands]

Stdlib stays stdlib — no Flask, no FastAPI, no pip (grid.py's own law).

- `controlroom.py` — bootstrap only: main(), ThreadingHTTPServer, telegram thread,
  the Handler shell.
- `routes.py` — a declarative table: `(method, prefix) -> handler fn`, plus the
  static-allowlist logic verbatim. do_GET/do_POST shrink to a lookup and a
  serve-bytes tail. The PAGE string moves to a served file like every other page —
  MINUS a ten-line minimal inline fallback that stays: PAGE is what serves when
  dashboard.html AND interface.html are both unreadable (controlroom.py:415–428), and
  the split must not delete that degrade-never-die property (the same idiom grid.py's
  file_lock docstring canonizes).
- `handlers.py` — state()/journal()/skills()/roster() + the game handlers
  (_journey, _run_node, _talk, _do) as plain functions taking (req) -> dict.
  All file access stays on grid.load_json / atomic_save_json / file_lock.
- Timing: P4 already deletes ORGANS_DOC and adds /api/manifest — that session touches
  every seam this split needs; doing it earlier is a refactor without a feature.

---

## 3. MEMORY DISCIPLINE

### 3.1 The r128 dispose checklist (binding on every scene-object teardown)

r128 has no automatic resource reclamation: removing from scene frees NOTHING on the
GPU. Any code path that removes or replaces scene content walks this list:

1. `scene.remove(root)` (or detach from parent group).
2. `root.traverse(o => ...)` and for every mesh/points/sprite/line:
   - `o.geometry.dispose()`
   - materials: handle BOTH forms — `Array.isArray(o.material)` (the plant boxes use
     6-slot arrays) and single. For each material: dispose every texture slot in use
     (`map`, `emissiveMap` — the window textures are clones, each clone is its own GPU
     texture) via `tex.dispose()`, then `material.dispose()`.
3. Null the JS refs (`archiveTease=null`, NODES/LABELS entries, `userData` closures) so
   the heap side can collect.
4. DOM labels: remove the `.wlab` element AND its LABELS entry together — a label
   without a node is a detached-DOM leak.
5. Shared resources are exempt and REGISTERED as such: DOT and the WIN masters — and
   ONLY those. Every `fresnelMat()` call returns a PER-INSTANCE material
   (world.html:414–420); the holder owns it and disposes it with the object — do not
   skip it as "shared". A module never disposes what it does not own; a `SHARED`
   comment marks each genuinely shared resource (comment law, section 5).
6. Timers and listeners are resources too: every self-rescheduling `setTimeout` chain
   stores its handle and has a named owner that clears it (the runObserve defect,
   1.2.5, is the counterexample); every `addEventListener` outside boot/init has a
   matching removal in `dispose()`.
7. Fetch: any poller that can outlive its surface takes an AbortController; `api()`
   grows an optional timeout. The bench run-poller ships with abort from day one.
8. Context loss [PLANNED, rides P0]: `webglcontextlost` -> preventDefault, freeze the
   loop, CARRIER LOST treatment; `webglcontextrestored` -> reinit renderer-side state.
   Never rebuild the whole scene reactively (the LUMEN no-teardown law).

### 3.2 The three leak tests — run at EVERY rung's exit, results in the 09 ledger line

1. **Heap snapshot ritual.** DevTools Memory. Snapshot A at a settled field. Exercise:
   open/close OS x10, dock/undock x10, one full mission, comms send x3 (P0+: one bench
   run). Force GC, snapshot B. Repeat the exercise, snapshot C; repeat once more,
   snapshot D. LAW, per class — falsifiable, no "~flat" judgment calls: Detached
   elements delta B->C must be EXACTLY 0. For JSArrayBufferData and Texture-related
   retained size (the always-on pollers land fetch buffers there nondeterministically),
   leak = MONOTONIC growth across B->C->D in the same class; single-step jitter under
   100KB is noise. A->B growth is allowed (caches warm once). The three numbers are
   recorded in the 09 ledger line; a monotonic class blocks the rung.
2. **Scene census.** In console before/after the exercise:
   `scene.children.length`, `renderer.info.memory.geometries`,
   `renderer.info.memory.textures`, `renderer.info.programs.length`.
   All four return to baseline plus EXPLAINED additions (a reveal legitimately adds; the
   addition is named in the ledger line). Unexplained monotonic growth blocks the rung.
3. **Listener count.** In console: `getEventListeners(window)`, `(document)`,
   `(renderer.domElement)` — total counts stable across the exercise. (This API is
   DevTools-console-only; it cannot be scripted into the page — do not try to automate
   this census.) Any growth means a render path is attaching what only init may attach.
   Timer discipline spot-check, falsifiable: the network panel can never go fully quiet
   (pollEvents hits /events every 1.6s and pollTracks every 6s for the app's whole
   life, world.html:1035–1051) — so FILTER the panel to `/state`; baseline = one
   request per ~6s (pollTracks). Close the dock mid-observe: after one in-flight cycle
   (~3–4s), NO additional 3s-cadence /state requests may appear. Extra cadence = the
   orphan runObserve poller = fail.

The ritual costs ~10 minutes. It is the boring test's memory twin: a rung that leaks
did not ship.

---

## 4. STATE RULES

1. **Server-side saves ONLY, always through the grid.py idiom.** Every durable write =
   `file_lock` + `load_json` + mutate + `atomic_save_json` — exactly what `_journey`
   does today [BUILT]. No handler ever `open(...,"w")`s a store directly. New stores
   (bench records at P1, modules.json at P2) inherit the idiom on birth, including the
   append-only law for records (records are never rewritten — pr.time's bench law).
2. **Client state is ephemeral by definition.** localStorage may hold VIEW state only —
   things whose total loss costs nothing true: `probe_viewed` pips, the comms transcript
   cache, sound/motion prefs [BUILT — already true]. If a value would be missed after a
   cache clear, it belongs in a server store. The comms transcript rides the line
   deliberately: it is a courtesy replay, and the honest record is talk_state.json,
   server-side. Nothing gameplay-gating ever lives client-side.
3. **The run-tag law (P0 SPEC ADDENDUM, binding).** Every bench event carries its
   `run_id`; the trace pane polls BY run_id. The entity's own concurrent draws are on
   the same wires — untagged events would misattribute them to the bench, which is a
   fabricated number, which is the honesty law broken at the protocol layer. Per-link
   milliseconds come from the harness's own perf_counter, never energy.draw's rounded
   latency.
4. **One truth per fact.** No client-side copy of a server table (the MODEL_FOR defect,
   1.2.9). No second registry beside modules.json once it exists (A14). When the game
   and the entity disagree, the entity's files win and the game re-renders.

---

## 5. CODE STANDARDS

- **Naming — every clause greppable.** Python: stdlib style, organs are lowercase
  single words (grid, energy, pulse), constants UPPER. JS: functions lowerCamelCase in
  the house voice — short, verb-first (`osOpen`, `feedLine`, `runBeat`); NEW module
  files lowercase-with-dashes (aea_elements.js and city.data.js grandfathered by
  name); bus events `noun:verb` lowercase. UI ids stay terse (`#c-feed`). Every name says what the thing
  IS in the game's own vocabulary (rod, plant, draw, reveal) — never generic
  (`manager`, `helper`, `utils`).
- **Comment law: constraints only.** A comment records a LAW, a LESSON, or a WHY —
  never narrates code. The codebase already does this well ("GPU lesson 2026-07-20:
  real bloom runs far hotter than swiftshader", "review 2026-07-10: cooling was a
  PERMANENT tombstone"). Dated lessons keep their dates. A comment that restates the
  line below it is deleted on sight. `SHARED` marks non-owned resources (3.1.5).
- **The no-dead-code rule.** Delete, never comment out. Superseded organs get a drift
  tombstone in the manifest (A14), not a corpse in the file. Data files may carry
  forward-references in comments (aea_elements.js's Act II+ block) because they are
  authored content plans, not dead code. `git`-less today; the file history is the
  entity's own stores, so a deleted block is GONE — that is the point.
- **Error surfaces, enumerated.** Client: `window.onerror` -> `#err` strip [BUILT];
  module init failures must reach it too, not vanish in a promise. Server: handlers
  return `{ok:false, error:"..."}` with the reason truncated, never a 500 page, never
  a stack trace over the socket [BUILT — keep]. Empty `catch(e){}` is legal ONLY on
  fire-and-forget telemetry (pulse writes, chain_write) and must stay illegal on
  anything a player waits for — a swallowed error on a waited path becomes a lie on
  screen (the cSend lockup, 1.2.6, is what it looks like).
- **Failure text is honest and in-world.** "starved", "CARRIER LOST", "the meter holds
  pollinations: rpm" — real states, named plainly, two inks. Never "Oops".

---

## 6. THE TECH-STACK DECISION [DECISION-LUIS — gated POST-MVP, not before]

Recorded now so the MVP gate has an honest table waiting; decided NEVER before the MVP
works (Luis's law, the chapter's governing line). "MVP works" = the P7 exit at minimum
— the income rung shipped on the current stack.

| | A. Stay vanilla + r128 | B. TypeScript + Vite + modern three | C. Hybrid: keep stdlib server, modernize client only |
|---|---|---|---|
| Phase B distribution (anyone installs) | weakest: "run this python file" is fine for player one, rough for strangers; but Phase B is GATED and unpriced | strongest client story (bundle, versions, npm) — server still needs an answer anyway | matches reality: the server IS the entity and cannot be npm-ified; only the client travels |
| r128 API ceiling | real but distant: no WebGPU, aging examples-js addons, snippets from modern docs silently break (08_TECH law) | ceiling removed; every current three.js feature and doc applies | ceiling removed on the client |
| The no-build-step law's value | fully kept: greppable, zero toolchain rot, file:// debuggable, the entity serves its own game | lost: node_modules, config, version churn — a second machine to feed | lost on the client, kept on the server |
| Migration cost (sessions) | 0 | 6–10: full client port + r128->modern three API delta (color management, addons, materials) + re-verification of every screenshot recipe | 4–7: same client port, server untouched |
| Leak/perf tooling | manual (section 3 rituals) | typed dispose patterns, better tooling, same GPU rules | same as B on the client |
| Risk to the honesty law | none — running truth stays running | a port is weeks of a broken game between two working ones | same, smaller |

**Recommendation (one, with the trade-off named):** stay on A through ALL of Phase A —
the module plan and memory discipline above remove the monolith pain, which is the only
pain that is actually bleeding; 4–10 sessions of migration is 2–5 rungs of the ladder,
and the income clock prices that as unaffordable. Re-open this table ONLY when Phase B
gets its explicit call (BOOK ledger #17), and then choose C, not B — the stdlib server
is the entity's own body and modernizing it buys nothing, while a distributed client is
the one thing Phase B genuinely cannot ship without. The named trade-off: choosing A
means living with the r128 ceiling and manual leak rituals for months, and paying the
client port later at possibly higher line count. That is the correct side of the trade
while sessions are the scarce currency.

---

## 7. THE P0 ENGINEERING CHECKLIST (distilled from the P0 SPEC ADDENDUM, binding)

Build order inside the rung; each line is checkable.

0. `window.GAME` `{state, bus}` created in the boot section (~15 lines): `state`
   ALIASES the existing globals (2.2 — references, no relocation), `bus` is the
   ~15-line pub/sub. Expose exactly the seams bench.js needs — the state keys its pane
   reads plus `run:link` / `carrier:lost`. Nothing else migrates at P0.
1. `bench.js` born as a flat-served module under the section 2.2 boundary rule; docks
   as the DOCK TERMINAL pattern at the nexus — no new OS tab.
2. Construct spec v0.1.0 hand-authored: `parts / wiring / rods / policies / zone`;
   `zone` REQUIRED — harness refuses a spec without it, naming the clause; bench UI
   defaults zone=private; the run pane prints the zone word.
   [DECISION-LUIS — freeze v0.1.0]
3. TAP = thin wrapper over `energy.draw` [BUILT underneath] with
   `{tier, zone, prompt_source}` -> `{text, latency_ms, tried[], plant, model}`.
4. SCORER = new server-side function, tens of lines: receipt-measured fields ONLY
   (`pass, axes:{latency_ms, tokens, ok, zone}`) — no model-judged quality number at P0.
5. Bench task v0: `{id, prompt, expect:{contains|exact}, tier_floor}`; ONE curated task;
   `tier_floor` pinned local/keyless.
6. Run contract: `POST /api/construct/run` -> `run_id` immediately, executes in its own
   thread; `GET /api/construct/run?id=` for live status; the trace pane polls by run_id
   WITH AbortController (sections 3.1.7, 4.3). Run status/trace rows persist through
   `grid.file_lock` + `load_json` + `atomic_save_json` (a per-run file or runs.json,
   append-only per §4.1's record law): the run thread writes the file, the GET handler
   reads the file; any in-memory copy is a cache, never the truth.
7. Per-link ms from the harness's own perf_counter around each fire.
8. Run-tagged events on every record — the entity's concurrent draws can never
   misattribute to the bench.
9. Trust law live at fire time: manifest binding evaluated per part — allowed -> fire ·
   draft_only -> artifact only, nothing leaves · else refuse, naming the level.
10. The honest kill for the falsification screenshot: zone=sensitive with local ollama
    down (true starvation); a plant-kill on a healthy grid renders as reroute marks —
    resilience working, and labeled so.
11. modules.json v0 rows name the real entry point each part wraps (TAP->energy.draw ·
    GOVERNOR->grid.METER.can_spend · LADDER->energy.ladder · SCAFFOLD->prompt scaffold ·
    SCORER->receipt scorer).
12. Riders: COMMS wait pattern (`T+x.xxs` + destination) on mission do-beats; one-line
    `last run / best run ms` readout on the bench pane; M0.1 pane lifts answer+latency
    above the raw JSON (JSON intact below); EMISSIVE-TUNE first, verified on BOTH
    pipelines per R2; controlroom PAGE's hardcoded corpus denominator fixed.
13. Engineering riders from THIS chapter: context-loss listener pair (1.2.7);
    MODEL_FOR/CURATED single-sourced (1.2.9 — drift already live; the transport chosen,
    /state vs tiny endpoint, is recorded in the 09 ledger line); runObserve poller
    gains a handle and an owner (1.2.5); `api()` gains timeout support and cSend
    releases `cBusy` on it (1.2.6).
14. Exit protocol: pre-playtest survey check (>=3 plants online) + the three leak tests
    (3.2) run and recorded in the 09 ledger line + the two ADDENDUM screenshots and the
    kill.

---

## Changelog

- 2026-07-20 — v1. Authored from a full read of world.html, controlroom.py, missions.js,
  aea_elements.js, grid.py, energy.py on this date. Audit findings 1.2.1–1.2.10 carry
  line numbers from that read. Module plan honors the no-build-step law and the r128
  stack law (08_TECH); extraction schedule bound to rungs, never to refactor-only
  sessions. Tech-stack decision recorded as a gated table per Luis's law — decided
  post-MVP, recommendation stay-vanilla-then-hybrid-at-Phase-B. P0 checklist distilled
  from the binding P0 SPEC ADDENDUM plus this chapter's four engineering riders.
- 2026-07-20 — nine-critic closure (Greybeard, Reliability Engineer, Maintainer-in-a-Year).
  Ground truth re-measured: controlroom.py 641 lines; _journey :500–523, CURATED
  :469–473, do_GET :281–433; /api/tickets + /tracker added to 1.2.10; symbol-anchoring
  law added to the header. §2.2 marked [PLANNED — born at P0] and gains
  aliasing-not-relocation, the interregnum clause, grow-on-first-listener events, the
  bench dispose() caller, and Object.freeze marked [PLANNED]. §2.1 load-order law
  restated to disk; module birth ritual and the engine.js frame-hook seam named. §2.3
  keeps the PAGE minimal fallback. §3.1.5 fresnel ownership corrected (only DOT + WIN
  masters are shared). Leak tests 1 and 3 respecified falsifiably. §1.2.5 gains
  flashNode plus the corrected typeInto/runObserve failure narratives; 1.2.9 upgraded
  to drift-has-happened, single-sourcing non-optional. Naming law made
  grep-enforceable. P0 checklist gains item 0 (GAME birth) and the 7.6 run-status
  file-idiom line.
