# THE PROBE, SESSION LOG

One entry per work session. **Read the latest entry before starting.** The next session builds
from the `NEXT` block, it does not re-decide what is under `LOCKED`.

---

## 2026-07-22 (later·9), FIRST LIGHT green, then R37/R39: the city ripped out, the world is the INSTRUMENT

**DID, first light (committed `35c0afd`):** the honest seam `aea/gameapi/` (firewall + read/act) over the
REAL organs: `/game/state`=controlroom.state, `/game/ignite`=bench_core.start_run, `/game/run`=run_status,
mounted into the :7799 control room (same origin, no new port). Client: `core/api.js` (the only server-talker)
+ `bench.js`'s three fetches repointed to `/game/*`. Verified GREEN in-client: compose BRAIN+SCORER -> ignite
-> PASS on ollama/qwen2.5:7b, driven with real keystrokes via CDP. Bugs the verb surfaced + fixed: modules.json
file-paths went stale in the subpackage reorg (the forge-gate refused every part -> `bench_core` now resolves
against the aea/ package dir, 25 paths remapped); the client sent `T-01`!=`t-01`; `normalizeRun` read a
`verdict` the seam never emits (mapped to run_status's real shape: link.state from ok, verdict from pass);
LOCAL_FLOOR `granite4.1:3b` (not installed) -> `qwen2.5:7b` (the one local model that reliably returns
PROBE ONLINE, CPU-only here, the rest hallucinate or return empty).

**DID, R39/R37 world (uncommitted):** ripped the CITY out of `engine.js` (`buildWorld`: foundry buildings,
socket tower, slab, roads, deleted with its helpers). Built THE INSTRUMENT: an amber core, concentric
PRIVACY-ZONE rings (radius=zone, from grid.ZONES: sensitive->private->public), the AEA organ-nodes on their
ring at dependency-depth altitude, LIT amber where really wired (BRAIN/GOVERNOR/MEMORY/LOOP, from live state
signals), cold-blue FOG-wireframe where not (SENSES/HANDS), and conduits along the real couplings.
Data-driven from a new seam endpoint `/game/schema` (the fog can't lie: `wired` is a live check that flips as
organs get built). Composer relabeled tap->BRAIN, energy->POWER (R39 vocabulary). Verified on a swiftshader
shot: reads as the FIELD_GUIDE cover (the being as a concentric place), not a city.

**NEXT, finish the world slice:** conduit particles (one per real /events draw, count-true, zero decorative);
the fly-to-BRAIN -> dock -> ignite loop (v2 never wired flight-proximity `S.near`); capacity-fill + node labels.
Owed: D13 (the reorg-registry lesson); the `POWER` word disambiguation (header reserve vs brain sources).

---

## 2026-07-22 (later·8), aea/ SUBFOLDERED: flat 34-file package -> 10 domain subpackages (DONE, verified)

**DID:** dissolved the flat `aea/` package (34 `.py` at one level, bare `import grid` co-location, the
thing Luis hated) into **10 domain subpackages**: `kernel`(grid,pulse,trust,tracelog) · `mind`(orchestrator,
swarm,hades,pathfinder,relay) · `energy`(energy,capacity,+censuses,model_fitness,probe,gauntlet) ·
`memory`(consolidate,index_codex,memory) · `bench`(bench_core) · `io`(speak,listen,agent_tools,notify) ·
`organs`(autonomy,brief,talk,telegram_bridge,reflect) · `loop`(aea,live) · `server`(controlroom) ·
`tooling`(export_city,build_graph). Strict inward-only DAG, no cycles.

**HOW (safe surgery, not a hand-move):** a 5-agent sweep mapped all 45 internal imports + every
move-breaking pattern (zero dynamic imports; traps = mixed stdlib+internal lines, a docstring
`from energy import draw`, bare-filename subprocess spawns). An **AST-guided migration script** then moved
files + rewrote all 45 imports (`import grid` -> `from aea.kernel import grid`), splitting mixed lines,
leaving docstrings untouched. Non-import fixes: root shim + `controlroom._do` + `live.py` spawns now use
`python -m aea.<pkg>.<mod>` at cwd=repo-root; `build_graph.py` recurses + reads dotted-import edges;
`install_autostart.ps1` -> `-m aea.loop.live`. Pre-reorg checkpoint committed first (`d1c20cd`).

**VERIFIED end-to-end:** 33/34 import clean (0 fail); `.env` resolves (6 plants online); graph rebuilds
identically (code 64 nodes / 81 edges); server boots via the shim; **all endpoints 200** (/state /probe
/world /roster /api/journey); **the SACRED save intact** (M0.1 + M1.1 preserved). Entity behavior unchanged.

**NEXT:** unchanged, FIRST LIGHT (the compose->ignite verb) now builds on the clean package.

---

## 2026-07-22 (later·7), SESSION CLOSE / HANDOFF TO A FRESH CONVERSATION  ← START HERE

Luis is opening a NEW conversation to **design the codebase to the scale of the ambition, then build**.
This entry is the pickup point. Read order (per `/CLAUDE.md`): `graph.json` → this entry → `DISCOVERIES.md`
→ the docs named below. **The exact kickoff prompt Luis will paste is saved at `diary/NEXT_SESSION_PROMPT.md`**
(its STEP 2 = present the complete codebase design, full file tree, dependencies, structure, before any code).

**WHAT THIS SESSION PRODUCED (the design phase, treat it as done, do not redo it):**
- **The vision, shown:** `design/FIELD_GUIDE.html`, the finished game's strategy guide, backward-designed
  (it is labeled a VISION artifact; the game is NOT built yet).
- **The codebase design:** `design/CLEAN_ARCHITECTURE.md`, **THREE RINGS** (substrate `aea/` PRESERVED ·
  one honest seam `aea/gameapi.py` · client rebuilt). It already carries seams for modes / world / pokedex /
  Phase-B, i.e. it is scaled for the ambition. **This IS the codebase design Luis wants**, review and
  extend it to his satisfaction on scale; do not start a blank one.
- **Genre-DNA welded to the real substrate** (`D11`): Pokedex silhouette = the honesty law; compose-then-
  IGNITE with a real adjudicator; the readable REAL trace. Each with a refusal list.
- **Expert-panel verdict** (`D12`): unanimous **YES, masterpiece seed, verified in code.** Three execution
  flaws (unbuilt verb / imperceptible-truth + dead-verbs / rate-limited iterate loop). **The one move:**
  ship the verb (compose two real parts → IGNITE, first 10 min, realness-against-fake once). Plus the
  **HOLD-THE-LINE list** (the deliberate un-likable choices to KEEP). Read D12 in full before deciding scope.
- Modes = 3 apertures on one engine + a SANDBOX↔LIVE reach axis (`R36`, sandbox ≠ fake); world = metroidvania
  living instrument (`R37`); missions = scaffolding, not spine (`D9`). Full spark history: `REFLECTIONS.md` R1–R38.

**THE TENSION TO HOLD (name it, don't ignore it):** Luis wants to design the codebase to scale before
building. D12 + the panel warn that *designing instead of shipping the verb* is THE recorded failure pattern
(~110:1 words-to-code, D7). Reconciliation: the architecture already exists and is scaled, a short review/
extend pass is legitimate; a from-scratch re-design or more vision docs is the avoidance trap. **The exit is
FIRST LIGHT either way.**

**THE FIRST BUILD (from `CLEAN_ARCHITECTURE.md` §FIRST LIGHT — ~6 files):** `aea/gameapi.py` (the honest seam;
absent→dash, refusal→receipt) + `web/game/js/core/api.js` (the only server-talker) + wire `web/game/js/bench.js`'s
dead run bus (`bench.js:14` "no listener") to a real poll of `/game/run` + `web/probe.html` + `hud/hud.js` +
`missions/runner.js` replaying M0.1. The seam MUST call the REAL organs (`bench_core.start_run`, `grid` Meter,
`agent_tools`, the `aea.py` tick), read them via the graph's `code` subgraph first; never fabricate. Guard
the first-light chord on the unlimited **local hearth** (ollama), never the rpm=4 socket. Verify with a
swiftshader screenshot; render first, then report.

**GUARDRAILS (unchanged, non-negotiable):** honesty law · claim ceiling (never conscious/sentient) · the
SACRED save `state/journey_save.json` · privacy guard (no employer/paths in anything committed) · NO emoji ·
the entity `aea/` is PRESERVED (rebuild only the client) · no new design corpus until the verb ships (D7).

**BUILD MAP READY:** the substrate scout finished and its full integration map is preserved at
**`design/FIRST_LIGHT_INTEGRATION.md`**, read it before writing `aea/gameapi.py`. Key findings: use
`bench_core.start_run` / `run_status` for compose→ignite→run-or-fail (honesty-law refusals already native);
the read endpoints re-home from `controlroom.state()/roster()/journal()/_journey`; BRAIN = `energy.draw`,
LOOP = an `aea.main`-style `sleep` heartbeat wrapping one draw (no bench part, the one game-vs-engine
divergence); guard the awe-beat on the unbrownoutable local **ollama** hearth. **The pleasant surprise:**
`web/game/js/bench.js` already does the whole flow inline, first light is largely **repointing three fetch
sites** (`fire`/`schedulePoll`/`refreshGrid`) at `/game/*` + switching the refusal read to `j.refused`, not
building from scratch.

---

## 2026-07-22 (later·6), expert panel: GREENLIT, and told to stop designing and ship the verb

**DID:** ran a 7-critic adversarial panel + synthesis (`w6zasmov8`). Verdict -> **D12**. Unanimous YES on the
core (a masterpiece seed, verified in code). Three execution flaws, mostly already locked: the core verb
(compose->ignite->receipt) isn't wired (`bench.js` confesses it); truth is imperceptible + honesty-law dead
verbs (the passive 60s meter); the iterate loop is rate-limited (needs the SANDBOX↔LIVE fast lane).
Clarified **R36** (sandbox != fake, real API/tokens always; the axis is *reach*). Labeled `FIELD_GUIDE` a
VISION artifact (the panel called it a credibility bomb if treated as shipped).

**THE PANEL'S UNANIMOUS INSTRUCTION (+ the completion clock):** stop generating vision, the danger is a
beautiful document on a tech demo (D7, 110:1). **NEXT = FIRST LIGHT, sharpened:** compose two REAL parts ->
IGNITE in the flown world -> runs-or-visibly-fails, inside the first 10 min, with realness shown against
fake ONCE (kill the socket -> a live number becomes a dash); guard the first-light chord with the unlimited
**local hearth**, never the rpm=4 socket. Wire `bench.js`'s run bus to `/state` via `aea/gameapi.py` +
`core/api.js`. Then a 20-30s no-fail flight calibration + a designed dock ring; strip the title card to 3
verbs.

**AVOID (named):** another design chapter / concept sheet / act; extending `FIELD_GUIDE` as if shipped; Acts
II-VI before the loop is re-solvable; color/spectacle to widen appeal. HOLD THE LINE: honesty law, claim
ceiling, real jargon, austerity, AI-curious-builder audience (not everyone), the coldness.

**STATUS: the design phase is over. The next artifact is code.**

---

## 2026-07-22 (later·5), the vision, shown: FIELD_GUIDE shipped + clean architecture + modes + world

**DID:** decided the clean rebuild (game CLIENT from scratch; **entity PRESERVED**, R32) and ran a 5-lens
generation pass. Shipped **`design/FIELD_GUIDE.html`**, the finished game's 90s Zelda-style strategy guide,
backward-designed, at the concept-art bar (rendered for Luis). Wrote **`design/CLEAN_ARCHITECTURE.md`** (the
THREE RINGS blueprint). Genre-DNA welded to the real substrate (Pokedex silhouette = the honesty law;
compose-then-ignite with a real adjudicator; the readable real trace). Captured R32–R38 and **D11**.
Decisions: modes = 3 apertures on one engine + a SANDBOX↔LIVE axis (R36); world = metroidvania living
instrument, earned openness (R37); crystallization = a bridge mechanic, not the goal (R38).

**LOCKED (adds):**
- **THREE RINGS architecture**, substrate (`aea/`) preserved · one honest seam (`aea/gameapi.py`) · client
  rebuilt. The honesty law + claim ceiling live in the seam, structurally.
- **MODES** = GUIDED / BUILDER / ARCHITECT apertures on ONE engine, + SANDBOX↔LIVE permission axis.
- **WORLD** = a living concentric instrument; openness is EARNED (metroidvania), maps data-driven from the
  real schema. NOT open-world (can't honestly roam what isn't built).

**NEXT:** an adversarial **expert panel** is running (why it fails / what it needs / masterpiece), its
verdict feeds the build. Then **FIRST LIGHT**: the 6-file MVO slice in the clean skeleton
(`core/api.js` new, `bench.js` opened to the 4 MVO slots, ignite -> real tick -> viable-or-visibly-fails).
Design phase has a HARD exit into code here, no more corpus until first light ships (D7).

---

## 2026-07-22 (later·4), cold-read audit: the code IS legible; the CANON is not

**DID:** ran a 3-stranger cold-read audit (no conversation context) at three access levels, legibility
**structure-only 78 / code-only 80 / full-repo 84**. Finding -> **D10**. Headline: a stranger correctly
identifies the project (a game where you pilot inside a living AI) from CODE ALONE, naming + `world.html`
copy + `controlroom.py` route comments carry it. The obstacle is NOT comprehension; it is **canon**: 3
overlapping front-ends (v1 `world.html` live-wired / v2 `web/game/` declared-current but mid-migration and
NOT live-wired / archive prototypes on legacy routes), ~14 live routes `controlroom.py` serves that the "two
halves" doc story ignores, and a design-heavy / code-light imbalance. The docs are cleaner than the code truth.

**REFINES THE MERGE (the NEXT):** the merge is now **collapse 3+ front-ends into ONE canonical build +
live-wire v2 (fetch `/state`, wire the run bus) + CUT the dead routes**, not just "unite the two halves."
Also owed: docs to name the route sprawl + a cut-list (map must match territory).

**Unchanged:** still needs Luis's go; still starts from the MVO + composer at first light.

---

## 2026-07-22 (later·3), DECISION: missions = scaffolding, not spine; the generative viability engine

**DID:** Luis accepted the entity-as-spine recommendation (R28 open thread -> resolved). Captured the
generative-combination sharpening as **R30** (the composer generates AEA-part combinations across R29's
tier-space; most are non-viable, and that empirical non-viability IS the teaching). Distilled the decision
into **D9**. Marked R28 RESOLVED. Refreshed the graph.

**LOCKED (adds to the 2026-07-22 block, resolves R28, no prior lock overwritten):**
- **ENTITY = SPINE, MISSIONS = SCAFFOLDING.** The living entity carries the play; authored missions teach
  you to build and read entities and hand over control, then thin (Act 0 on-rails -> late acts open). A
  fixed campaign that never opens up is the failure mode to refuse.
- **GENERATIVE VIABILITY ENGINE.** The composer (holographic bench, `bench_core.py` + `web/game/`) generates
  entities as AEA-part combinations; viability is EMPIRICAL (it runs on real models / tools / rate-limits, or
  it doesn't); non-viability is legible information, not a dead end. This is what lets the scaffold retire.
  Disciplines: legible failure signatures · viability-as-spectrum · easy early viability · no dominant combo.

**NEXT, refined (supersedes the merge framing below):** the MERGE still comes first, but FIRST LIGHT starts
from the **Minimal Viable Organism + the composer**, a generated entity that wakes on its own tick and
either runs (viable) or *visibly* fails (legible non-viability), with M0.1 as the scaffold framing that
moment. Missions 1-5 (energy / decision / integration / outcome / predict) remain, now explicitly as
scaffolding around the living entity.

**OWED (not now):** reconciliation pass on GAME_PLAN's act structure (still reads missions-as-spine in
places); no new design chapters until an act ships (D7).

---

## 2026-07-22 (later·2), REFLECTIONS layer added (mess-first spark capture)

**DID:** created **`diary/REFLECTIONS.md`**, the capture layer upstream of `DISCOVERIES`. When Luis
puts a realization through, it lands here raw and dated (his words, mess-first) before being distilled;
each `## R#` is a graph node. First seeded R1–R6 from the recent arc, then ran an exhaustive 3-agent
workflow over the full session transcript (227k tokens) and **recovered the ENTIRE vision history —
R1–R28** across 5 eras: ORIGIN (a 3D city named Leyber, tokens=energy, the self-improving loop, build-on-
the-AEA, render-the-mind-as-a-brain, the graph-memory idea that BECAME this handoff graph), THE PIVOT
(R11 "imagine it like a game"), THE GAME TAKES SHAPE (inventory/levels, the AEA discovery map, magic-out-
of-the-real honesty law, WirthForge-realized, the render doctrine), IGNITION (R22–27, the recent lock),
and THE FRONTIER (R28 = dynamics-come-from-the-entities; the lineage sweep confirms it's *closest to
still a seed*, woven through `GAME_PLAN §7` but never locked; flagged as an OPEN thread that may re-order
the merge, not silently overwriting the LOCKED mission progression). Each spark carries a `-> D#/LOCKED`
lineage tag; two recurring convictions (anti-anchor, alive-voice) captured separately. Wired in: 5th
subgraph in `build_graph.py` (`reflections`), added to `CLAUDE.md` (map + boot + a "capture his sparks
first" method rule) and `diary/README.md`. Re-ran the graph: **5 subgraphs, 157 nodes, access
guaranteed**, era headers correctly excluded (`###`, not noded).

**NEXT is unchanged:** THE MERGE (below).

---

## 2026-07-22 (later), project introduction added (CLAUDE.md), the last handoff gap closed

**DID:** wrote **`/CLAUDE.md`**, the stable introduction that self-prompts a fresh session (it
auto-loads in Claude Code). It carries: the boot sequence (graph → this log → discoveries), the repo
map, the crystallized working method (mined from the global field-lessons layer + PORTFOLIO's
`LUIS_FILTER` + `LAB_EXPERIENCE_STANDARD` + project rules), the laws that don't bend (honesty / claim
ceiling / two-ink / boring test / sacred save / privacy guard / no emoji), run+verify, and the
end-of-session ritual. **By design it holds NO state**, method + map only, so it does not need
per-session updates; the diary holds the state. Added `.claude/` to `.gitignore` (the gap Luis named);
`CLAUDE.md` itself is committed on purpose (it must travel with the repo). Wired it into the read-order
(diary/README) and registered it as `graph.json`'s `entry_point`; re-ran `build_graph.py` (129 nodes,
all 4 subgraphs still reachable).

**NEXT is unchanged:** THE MERGE (below). This was the last piece of handoff infrastructure, the game
itself still needs its two halves united.

---

## 2026-07-22 (late), repo backed up, root reorganized, handoff system built

**DID:**
- Backed up to **private `github.com/Leyber91/AEA_GAME`** (branch `aeagame_main` → `main`);
  career data (`data.js`, `index_codex.py`) excluded by design.
- **Full root reorg, 126 loose files → 6.** State → `state/`, web → `web/`, all 33 Python →
  `aea/` (one package, flat imports), runtime files → `state/`, specs → `docs/`. Anchored via
  `grid.ROOT`/`STATE`/`WEB` (walk up to repo root); root `controlroom.py` shim keeps the run
  command. **Verified end-to-end after every stage:** `.env` keys load (NVIDIA/GROQ/CEREBRAS),
  all endpoints 200, save (`M0.1`/`M1.1`) intact, every write lands in `state/`, no leak, no
  boot errors. Full record: `diary/REORG_PLAN.md`.
- **Handoff system built** (so any conversation takes over from the repo): `graph.json`
  (deterministic knowledge-graph, 152 nodes / 81 edges, via `aea/build_graph.py`), this `diary/`
  (journal + protocol in `diary/README.md`), and `references/` (external sources, privacy-guarded).

**OPEN (owed by Luis):** which portfolio references go in `references/`, name them and they get
privacy-scanned + brought in (see `references/README.md`).

**NEXT is unchanged:** the MERGE (below). Reorg + handoff were infrastructure; the game still needs
its two halves united.

---

## 2026-07-22, vision locked, repo backed up

**DID:** strategic audit (five research passes) → measured verdict: *not a game yet*, but the one
real idea is worth finishing. Vision cohered and locked. Full working tree committed locally
(branch `wip/checkpoint-2026-07-22`, commit `bc825ce`). Clean **game-only** export pushed to
private `github.com/Leyber91/AEA_GAME` (`aeagame_main` → `main`). Career/portfolio data
(`data.js`, `index_codex.py`) excluded by design.

**LOCKED, do not re-litigate:**
- **THESIS (no-AND):** *Wire living proofs of a mind, each more complete than the last, until you
  hold the whole one, and it keeps running after you close the tab.*
- **UNIT = the Minimal Viable Organism:** `BRAIN` (a model) + `SENSES` (an observe tool) + `HANDS`
  (typed action tools, already exist in `agent_tools.py`) + `HEARTBEAT` (the loop, already exists
  in `aea.py`). Wire the four, it comes alive. Legibility = LEGO-Fortnite: each part's form tells
  its job. Claim ceiling holds, the player supplies "it's alive", the game never asserts it.
- **PROGRESSION = increasingly complete AEA combinations; the MASTER = THE AEA.** Each creature is
  a *proof of a combination* (proof = a receipt, it runs; not a claim). Progression-as-understanding.
- **ENDGAME = Phase B:** the finished entity reaches the real internet and acts for you, gated on
  prompt quality. Still deferred until Phase A is actually played.
- **FORM:** the probe stays (it's the vehicle). The city becomes a concentric **instrument**:
  radius = privacy zone · altitude = dependency-DAG depth · node fill = live capacity · edges =
  first-class conduits. NOT open world (short of verbs, not world). NOT landscape.
- **WHY IT'S NOT A GAME YET (measured):** no integration, no variable outcome, no stake the player
  can spend badly, flat verb set (fly / dock / press one button, Act 0 through Act VI).

**STATE:** forked. `world.html` = 6 missions, no bench. `game/` = a working bench, no missions,
empty `data/`. Not merged. Played ~20 min, once (`M0.1`, `M1.1` in `journey_save.json`).

**NEXT, build, ~5 evenings, every step wires what already exists on disk:**
0. **MERGE (step 0, do first).** Port the mission engine from `world.html` into `game/` (keep
   `game/index.html`'s module contract). Delete the dead fork. Then **FIRST LIGHT** = a Minimal
   Viable NPC: a dot with a brain + one sense + one move + a heartbeat that wakes on its own tick,
   moves toward the lit node on real tokens, thoughts printed. That single artifact *is* the thesis.
1. **Energy = stake.** Snapshot the daily quota at boot; charge each call; make `bench_core` emit
   `cost_u = 1` (client already reads it, always renders a dash today).
2. **One decision per DO beat.** Pick a rod, cheap may starve, strong may throttle.
3. **Integration.** Unspent budget carries forward; every call heats the next 60s window.
4. **Losable outcome.** `PASSED / PASSED-DEGRADED / STARVED`, written to `journey_save.json`.
5. **Predict beat.** `A2_TEACHING.md §7`, already specified, unbuilt, commit an answer the live
   system settles before each DO. Cheapest, most load-bearing item; makes the theme mechanically true.
   Then play all six missions twice. Run 2 differs from run 1 → it's a game.

**STOP:** no new design chapters, no new acts, no more concept sheets until an act ships. The
corpus is 12× the game by volume; that ratio is the recorded failure mode, not thoroughness.

---
## 2026-07-23, the AEA apologia + THE VOCABULARY locked (ground floor)

**DID:**
- **The apologia** (`design/AEA_APOLOGIA.html`): every AEA element enumerated + honesty-marked, and the
  completeness ladder proven to be ONE axis (Spore's stages = the acts = the autonomy classes). Headline
  reality-split: the running ENTITY is real (PROTO-AUTONOMOUS 6/6, 109 ticks) but the composer is at rung 1
  (5/17 parts, 0 constructs). The whole one is specified + reachable, not assembled.
- **THE VOCABULARY** (`design/A17_VOCABULARY.md`): locked the naming SYSTEM ground-up (atoms first, not a
  pre-authored catalog of beings, that stays earned, R30/N12). Built from the real inventory, pressure-tested
  by a 5-lens board (marketable/honest/thematic/consistent/further, wf wwsoyn204) that caught real code-verified
  defects. Luis ratified two forks: **MOUTH over BRAIN** (canon, ceiling-safe; BRAIN stays internal schema id)
  and **concrete machine-body register** (killed the -er agent-nouns).
- **Applied to code + verified live** (not just a doc): `bench.js` 5 part labels -> THE DRAW / THE FRAME /
  THE METER / THE LADDER / THE MEASURE; scrubbed the live claim-ceiling breach ("the being thinks");
  `bench_core.py` receipts; `schema.py` emits `label:MOUTH` on the depth-0 node (id BRAIN internal). Server
  restarted clean (one listener), `/game/schema` returns MOUTH wired=True, bench screenshot confirms all five
  names render with live meter truth (POWER 1998 LIVE, RODS 7, 0/4RPM).

**LOCKED (A17):** four namespaces never cross, RUNGS (journey, 8) / ORGANS (earned by lighting) / PARTS
(seatable chips) / EARNED TITLES (doctrines a run proves). Identity = the **part-signature** (not the
organ-signature, schema reads global state, so organ-lighting is the *derived* honesty view, per-run, pending
rung 2). Two-axis signature = anatomy + a **reach-mark** (hearth/reached/starved). A title is earned by a
receipt, never authored; a construct can earn the name of its own worse outcome (THE SOLO LAW). THE HEARTH
(free floor) + THE STAKE (1u real reach) promoted to atoms, the money layer made diegetic. "Tier" reserved
for the energy band only.

**NEXT, build rung 2 on the locked vocabulary (construct in order, ground-up):** make **RECALL** a composable
bench part (entity-side `consolidate.recall()` is already live; forge the seatable part). Compose THE DRAW +
RECALL -> the draw is grounded on real memory across a reset instead of hallucinating = a measurably more
complete being, and the first construct to earn a real title (BACKWARDS CHANNEL). Raise the MEMORY organ's
lighting bar from `len>0` to a recall that actually fired (the honesty board's fix). Wire per-run organ
attribution + the reach-mark onto the bench run-row so the derived organ-view becomes true.

---
## 2026-07-23 (later), visual elevation: core to spec + expert panel + resource-negative slice

**DID:**
- **Core to spec** (engine.js buildCore): the flat detail-0 pebble became the A6 jewel - icosahedron +
  additive fresnel shell + two counter-rotating tori (the orrery), lit amber ONLY when schema.alive,
  turning ONLY when alive (motion bound to a true signal). From dashboard+blob to a living instrument.
- **Expert panel** (wf w59a68svi, 5 lenses + synth + adversarial verify): how to elevate WITHOUT draining
  resources, best libraries for no-build r128, responsive shaders. Verdict: KEEP the color pipeline (ACES
  per-material + inlined aces(), HalfFloat target, FinalShader sRGB+dither, LOCKED amber-only bloom) - it is
  better-managed than most shipped WebGL. The real gaps are NO anti-aliasing + light-COUNT fillrate (not
  object count); most wins are resource-NEGATIVE. Verify pass killed 3 factual errors (phantom bloom-resize
  bug: composer.setSize already resizes bloom; FXAA served from web/ ROOT not vendor/; powerPreference GPU
  assumption unverified) + 2 honesty gaps (ORGAN_MAP unverified vs real emit strings; heartbeat signal source).
- **Built + verified the resource-negative slice** (client-side, no server restart): (1) tabular-nums on
  #bench .plate - closes a LIVE no-jitter law violation; (2) half-res UnrealBloomPass + re-apply after
  composer.setSize - ~half the composer's most expensive stage, visually identical; (3) deleted per-node
  PointLights (emissive 0.82 + bloom sells the lit node) - per-fragment light loop ~6 -> 2 across the full
  ground plane; (4) HONESTY FIX: removed the fabricated Math.sin core "heartbeat" (the panel flagged it as a
  rhythm dressed as a real signal - a claim-ceiling brush I introduced) -> steady EARNED glow + alive-bound
  rotation. Screenshot-verified: renders clean, organs lit, floor cleaner, zero quality loss.

**LIBRARIES VERDICT (locked):** vanilla/inline for almost everything; the ONE new vendor file worth adding =
FXAAShader.js (official r128 example, global script, served from web/ ROOT). SKIP all bundler-deps
(pmndrs/postprocessing, drei+R3F, troika-three-text, three-mesh-bvh, SMAA) and MeshLine + lygia's
include-resolver (lift the MIT GLSL inline instead). Full plan: tasks/w59a68svi.output.

**NEXT, the VISIBLE elevation + the honesty headline (vetted order):**
1. **FXAA** tail pass (new web/FXAAShader.js; RenderPass -> half bloom -> FinalShader renderToScreen=false ->
   FXAA renderToScreen=true; run on the ENCODED/gamma buffer). Kills the "chunky/2003-menu" aliasing - the #1
   visible gap. Screenshot-verify not-black under swiftshader.
2. **Living conduits** (honesty headline): wire the real GameAPI.events stream into the world - ONE additive
   THREE.Points, one point per real /game/events row travelling node->core, ok:false dim-grey. FIRST 3D
   element bound to the live entity. MUST unwrap {ok,events} + verify ORGAN_MAP against real emit() strings.
3. **Core breath from the REAL heartbeat** (replaces the removed sin): event-driven envelope from a VERIFIED
   pulse/heartbeat signal (else a stalled entity correctly shows a still core).
4. **Node brightness = real rolling activity** (exp-decay per organ from the same poll, clamped below fire).
5. **Bench rail** (answers "too poor"): the flat spine -> a lit rail with parts mounted on it + segmented-wake
   packet; chips as reticle/glyph instruments (export panels.js primitives); rationed --edge accent on state
   transition only. All CSS/DOM/SVG, near-zero watts.
Deferred: FXAA-on-rings via fwidth (verify derivatives pragma), fresnel normalize (nicety), powerPreference
(until nvidia-smi confirms the entity uses the discrete GPU), fat-ribbon conduits + InstancedMesh (only past
~50 organs).

---
## 2026-07-23 (later·2), FXAA + LIVING CONDUITS (the honesty headline landed)

**DID:**
- **FXAA** (new web/FXAAShader.js, self-contained MIT glsl-fxaa, global script served from web/ root):
  reordered the tail RenderPass -> half bloom -> FinalShader(renderToScreen=false) -> FXAA(present) so AA
  runs on the ENCODED/gamma buffer. Killed the "chunky/2003-menu" aliasing on every ring/edge/octahedron.
  Verified: rings render as smooth curves, no black, console clean under swiftshader.
- **LIVING CONDUITS** (engine.js buildConduitTraffic/pollEvents/updateConduit): ONE additive THREE.Points
  particle per REAL /game/events row, travelling organ-node -> core; ok:true warm->hot fading on arrival,
  ok:false dim grey. ORGAN_MAP verified against the real emit strings (energy/bench->BRAIN(MOUTH),
  trust->GOVERNOR, life->LOOP, memory->MEMORY; unmapped->core). Unwraps {ok,events}, polls ~1.5s off the
  frame accumulator (not setInterval), paused when hidden, pre-alloc 256-cap ring buffer, 1 draw call.
  First 3D element bound to the live entity. Verified: real particles flow to the core, console clean.
  NOTE: the entity's loop is quiet right now (latest event ~39h old) so the conduit shows the recent real
  trace on load + will light live when traffic resumes. MEMORY/SENSES/HANDS correctly stay dark (no traffic).

**NEXT (remaining vetted order):** core breath from a VERIFIED real heartbeat signal (the removed sin is
now steady glow; wire the envelope off real LOOP/life ticks via the same poll, else a stalled entity shows
a still core) -> node brightness = real rolling per-organ activity (exp-decay off the same poll, clamped
below fire) -> the BENCH RAIL (the "too poor" interface: flat spine -> lit rail with parts mounted, chips as
reticle/glyph instruments, rationed --edge accent). Deferred: fwidth ring AA (verify derivatives), fresnel
normalize, powerPreference (until nvidia-smi confirms the entity uses the discrete GPU).

---
## 2026-07-23 (later·3), THE REFERENCE PASS begins (R42): the bundle + the forge batch

**DID:** captured R42 (generate the target images FIRST; references are specs; the prose laws were not
converging us). Authored **design/refs/bundle/**, 15 files that make ChatGPT "go full on the scenes":
00_HOW_TO_USE (the per-generation ritual: style law + world brief + ONE scene, 3 variants, quote the
violated law line to correct drift) · 01_STYLE_LAW (the visual constitution: two inks + amber-as-emitted-
event, type law, register lineage, composition laws, FORBIDDEN list, the honesty tell) · 02_WORLD_BRIEF
(the radial instrument + the bench + the real vocabulary + the stakes) · SCENES/ W1-W6 world (rest /
ignition / fog-frontier / flight / whole-one / stake), G1-G3 beats (seat / fall-through / earned-title),
I1-I3 interfaces (bench plate / run trace / flight HUD - ChatGPT-only, need legible text). Wrote
design/refs/probe_refs_jobs.json (6 world shots x 3 seeds, phrased per the forge PROMPT_TIPS: amber =
bright emitted structure with extent, never a surface tint) and launched the local forge batch on the
owned Fooocus pipeline (runner waits for model load, resumable, candidates NOT committed).

**NEXT:** when the batch lands -> l212_curate (4 palette gates) + l212_contact grid -> present; Luis runs
the ChatGPT track from the bundle; joint curation -> WINNERS committed as design/refs/REF-*.png + REFS.md
(each ref mapped to the surface it governs + extracted vocabulary). Then BUILD-TO-MATCH: a visual slice is
done only when the render matches its locked ref side-by-side (world vs W1/W2 first, bench vs I1).

**BLOCKER (forge track):** the local Fooocus batch cannot run - the NVIDIA driver is NOT LOADED on this
machine (nvidia-smi present but "Driver Not Loaded"; NVDisplay.ContainerLocalSystem service STOPPED and
needs admin to start; likely broken since ~June when the recipe last ran at 22s/img). Fix = elevated
service start or a reboot (Luis's call - a reboot kills the entity server + the session). The batch is
fully parked + resumable: rerun `Fooocus python_embeded\python.exe -s <scratchpad>\probe_refs_run.py
design/refs/probe_refs_jobs.json <candidates dir>` once the driver is back (skips existing images).
Until then the ChatGPT bundle track is the primary reference-generation path.

**(later·3 addendum), SUBBUNDLES:** restructured per Luis's direction ("one subbundle per image...
create images like we had the game fully built with all the specification, we might be wrong and
that's ok" = backward design authorized). design/refs/bundle/ is now 12 folders, one per image, each
with ONE self-contained SPEC.md: style law inlined + world context + THE MOMENT (as-built save-state)
+ EVERYTHING IN FRAME (exhaustive inventory, exact engraved text) + composition + the 3-variant
generation instruction. All 12 share ONE canonical save-state so the set reads as a single real game:
c-07 = THE DRAW·RECALL·THE MEASURE earned BACKWARDS CHANNEL, c-04 earned RESTORABLE COHERENCE,
MOUTH/GOVERNOR/MEMORY/LOOP lit, SENSES/HANDS fog, POWER 1998 LIVE, RODS 7, MEM 48, LAST 1.44S/BEST
0.98S. Workflow: attach ONE SPEC.md per ChatGPT generation. Old flat SCENES/ removed (superseded).

---
## 2026-07-23 (later·4), THE REFERENCE SET IS COMPLETE (12/12) - the build contract exists

**DID:** generated + locked all twelve reference frames (design/refs/REF-01..12 + REFS.md as the
build contract). Backward design worked: images of a finished game, specced as-if-built, now lead the
render. Journey: 4 rounds of "not it" -> R42 (references-are-specs) -> the GPT-Image-2 protocol
investigation -> one anchored ChatGPT conversation, 01->12, anchor image + canon block, spec MATTER not
information, counts stated twice, reference-reuse (no re-attach). 9/12 landed at ZERO fix rolls; the two
that fought (02 fog-dots, 08 flat-diagram) taught field lessons now written into 00_HOW_TO_USE.
CANON that emerged and is now locked: ember-in-cage organs, two-tori core, sealed/solid/dashed privacy
rings, labels-on-approach, the caption tagline, the probe craft design, the octagonal chip + milled rail
+ light-at-the-connection bench material, branded-metal earned titles.

**NEXT, BUILD-TO-MATCH (the code turn resumes):** REFS.md maps every reference to its engine surface.
Primary targets: (1) the WORLD render (engine.js) vs REF-01/02 - ring treatments, ember-cage organs,
two-tori core, labels, ignition strike+dust-ring; (2) THE BENCH (web/game bench) vs REF-10 - the answer
to "the interface is too poor": octagonal chips on a milled rail, seat-glow, the live packet, the trace.
A slice is done ONLY when the render matches its ref side-by-side (existing harness: shot_world.mjs +
Read the PNG; Luis go/no-go). The honesty law still governs: a ref specs FORM; the render may only glow
where the system truly fired.

---
## 2026-07-24, COMPOSED 0 -> 1: the loop FIRES through the merged player surface

**DID (the milestone the last 12 entries circled):** verified THE MERGE is BUILT (this session's web/game/,
not the old world.html the panels read) and fired the FIRST construct end-to-end through the player surface.
Real-play chain, driven headless: wake flight -> fly the probe into dock range of the core (NEXUS, RANGE 12)
-> S.near true (the #bprompt "F - THE BENCH" shows) -> F -> dock() (bench plate + dock camera) -> seat THE
DRAW (head) + THE MEASURE (tail) -> SPACE ignite -> a REAL metered call: `HOP 1 · THE DRAW · ollama/qwen2.5:7b
· 12 chars` (54s cold, 0.88s warm) -> `HOP 2 · THE MEASURE · PASS` -> `r-01 · PASS · SPEED 0.88s · COST FREE ·
ZONE PRIVATE` -> record `LAST 0.88S · BEST 0.88S`. COMPOSED 0 -> 1. The composer, the seam, the honesty
(FREE = the hearth, a real ollama draw) all work. The game exists.

**GAP TO THE BAR (REF-10):** the working plate is a flat translucent text form with the amber core washing up
through it from below (the dock camera sits low over the core) - the "reads as a dashboard" failure REF-10
exists to kill. Refine target: rebuild the bench plate to REF-10/07 (machined matte plate, squared corners +
milled rim, octagonal debossed chips on a milled rail, light-at-the-connection seat-glow, the live amber
packet on RUN) + calm the dock composition so the plate reads against a near-black field, not a giant amber blob.

**NEXT (refine, in order):** (1) the bench plate -> REF-10 (the primary "too poor" fix), side-by-side vs the
locked ref. (2) the dock-camera composition (core wash). (3) the honesty fixes the critic flagged: tokens 0
-> a dash (energy.py:152), the len>0 MEMORY over-claim (schema.py), the `alive` field in the claim-ceiling
lint. (4) then the receipt/economy surfaces (REF-11/05) + the first title once RECALL forges.

**MASTER MAP:** design/ROADMAP.md is now the single ordered source of truth, the north star (the 12 refs =
the bar, build-to-match), where we are (COMPOSED 0->1, both plants, bench pass 1), the ordered build path
(Phase A make-the-first-loop-beautiful -> B close-the-guided-arc-rung-2 -> C the-meta-visible -> D
guided-frame; deferred=fog behind the sequencing gate), the full scope contemplated (a table so nothing is
lost), the standing lessons, and the doc index. NEXT = the lowest unchecked item in ROADMAP §2: Phase A step 2
= the bench plate to REF-10 (milled rail + bigger octagonal chips + the live RUN packet).

**PRODUCTION_PLAN.md**, the professional game-dev pipeline applied to THE PROBE (answer to "how do game
developers do it / follow a plan top to bottom"). The one idea: DATA-DRIVEN, build a few SYSTEMS, author
content (maps/missions/characters) as DATA, prove with a vertical slice, then production = authoring data not
code. THE PROBE's layers: DESIGN (done, scattered) -> CONTENT-AS-DATA (the pipeline) -> SYSTEMS (composer/
gameapi/world/save = DONE; the MISSION ENGINE = the ONE missing system). Ordered plan: Step 0 bench->REF-10
(in progress) -> Step 1 build the MISSION ENGINE + a mission data schema -> Step 2 author MISSION 01 (the
guided cold-open->first-fire as JSON) = vertical slice complete, the first time it's a GUIDED GAME -> Step 3
production (author the curriculum as mission data; menus = views over schema/save). This is the spine that
stops the oscillation: build systems + author data, never one-off screens.

---

## 2026-07-24 · STAGE 1 SHIPPED, THE MISSION ENGINE (the vertical slice plays)

**DID.** Built + VERIFIED the missing SYSTEM: the mission engine. THE PROBE is now a GUIDED GAME, not a
bench that fires. The vertical slice plays end-to-end: cold-open -> brief -> learn -> DO (the player
docks + seats THE DRAW + THE MEASURE + fires the REAL bench) -> PROVE (re-reads the real receipt) ->
reveal, driven by mission DATA, gated on real events.
- `web/game/js/mission.js` (NEW), a faithful PORT of world.html's `runBeat()` as a data-driven RUNNER
  (beats brief/learn/do/prove). Reads ONLY `GAME.bus` + `/game/*`; never touches bench internals.
- `web/game/data/missions/m01_first_light.json` (NEW), M0.1 FIRST LIGHT as DATA: the real protocol in
  the learn beat, located re-fire nudges (earned/reseat/halted), token-templated PROVE line + reveal.
- `bench.js`, added the ONE honest hook the mission needs: `GAME.bus.emit('run:done', {run_id, seq,
  pass, scored, cost_u, total_ms, halted})` at finishPass()/haltAt(), and `run:refused {reason}` at the
  three no-run_id branches (ignite refusal / ignite HTTP-error / carrierLost) so the DO beat never hangs.
- `controlroom.py`, added `.json` to the static allowlist (`_CTYPES`) so `game/data/*` missions serve
  (was a soft-404 "not found"). The CONTENT layer now serves, the data pipeline is real.
- `index.html`, loads mission.js after bench.js; `MISSION.init(window.GAME)`.
- **THE TALKING TEAM ran** (workflow wf_9d73037c): 5 department heads held a recorded standup, converged
  the locked mission-engine contract, authored the m01 DATA + the honesty-lint + the STATUS board.
  `design/STATUS.md` (NEW) is the honest board, DONE only when it ran + was seen.
- **PROOF OF RECORD:** headless run `r-09`, real free-hearth draw (`pass:true, cost_u:0, 786ms`), PROVE
  re-read `GET /game/run?id=r-09` (200, `pass=True`, tap+scorer receipts truthy), MISSION COMPLETE,
  localStorage `probe.mission.M0.1=done`, zero console errors, screenshot read (`scratchpad/mission.png`).
  Bench log `COST FREE`, PROVE line `run r-09 - 787ms - cost FREE`, reveal ceiling-clean.

**LOCKED (new).** (1) The mission engine is a data-driven RUNNER, not a framework, a guided beat is DATA
(`web/game/data/missions/*.json`), authored, never hand-coded. (2) TWO-TIER DO GATE: the DO wait resolves
on ANY terminal event (never hangs); the mission ADVANCES to PROVE only on `run:done pass===true`; misses
re-arm with a located nudge. (3) PROVE is HTTP-truth: re-reads `/game/run?id=` and asserts the LIVE body
(tap+scorer receipts truthy, `r.pass`/`r.run_ok`/scorer `receipt.pass` true, the real body carries NO
`verdict` object). (4) mission.js one-way dependency: reads ONLY `GAME.bus` + `/game/*`; the substrate
stays frozen; the bus is the only cross-module channel. (5) cost_u tri-state everywhere (0->FREE,
+->Nu, null->dash).

**NEXT.** The production pipeline is now real: build SYSTEMS, author DATA. The lowest unchecked move —
choose one, both are earned now that the slice plays:
- (a) **PRODUCTION: author M02+ as DATA** through the frozen mission engine, the guided curriculum (rungs
  0-2) as more mission JSON, NOT more code. First: RUNG 2 · RECALL (needs the RECALL part forged) or a
  second FIRST-LIGHT-tier mission on the free hearth. This is the data-driven scale-out the whole arc set up.
- (b) **POLISH the slice to the REF bar** (ROADMAP Phase A step 2): the bench plate to REF-10 (milled rail,
  bigger octagonal chips, the live RUN packet) + the mission terminal styling pass, now that the loop
  plays, decorate it. Vampire-Survivors law: loop fired first, polish second.
Recommendation: (a), prove the pipeline scales (one more mission as pure DATA) BEFORE polishing, so we
know the system sustains content. Then (b). Luis pilots `r-09`'s loop in-browser first (his go/no-go gates
the next slice): `python controlroom.py` -> `http://127.0.0.1:7799/probe`.

---

## 2026-07-24 (cont.) · THE BENCH REBUILT TO THE REFERENCE BAR (art-director-led)

**DID.** Took the bench from "lame flat panel over a lava-lamp core" to a machined instrument matching
REF-10/REF-07, in three gated passes, each verified by screenshot + the slice still playing:
- **Seat-collapse:** the atomic seat (one key seats one part; the "Enter at every gap" hack is dead),
  neutral palette (blue cast removed), amber-off-chrome, dock scrim.
- **Object-kind flip (the team's #1 fix):** full-bleed frame that OWNS the screen (column-flex, rail
  dead-center); ONE continuous rail with FIVE fixed octagonal sockets (the sockets ARE the parts); the
  numbered PARTS tray KILLED; GRID / > RECORD non-ref labels removed; chips grown + catching the top-left
  raking light; the leftover blue HOLD-C ring de-blued. `bench.js` renderSpine rewritten to the fixed-rail
  model (gap/cursor/ghost grammar retired); `midInsert` keeps run order == rail order (honesty).
- **Filament + run-log (REF-07/11):** the hot amber spark at the LIVE joint, the wow. It fires ONLY on a
  real drawing hop and cools on the real DONE; surfaced by teaching `normalizeRun` to read `open_link` as a
  LIVE row (bench_core reports the in-flight hop as open_link, never a LIVE link). Engraved run-log rows +
  recency gradient + the earned RECORD square.
- **Material system (the medium verdict):** CSS+SVG on the DOM plate (NOT a three.js quad, the plate is a
  live-bound honesty surface), one raking light baked into the rim, a feTurbulence matte grain (soft-light,
  rasterized once), conic-facet chip bevels + drop-shadow contact, a dim-warm seat-bleed under seated chips.
- **VERIFIED:** the mission slice still plays end-to-end after every pass (r-15/r-18 PASS, cost FREE,
  MISSION COMPLETE, zero console errors); the filament confirmed firing on real LIVE (caught LIVE:true).
- **THE TALKING TEAM (compounding, R46/R47):** ran three reviews this arc (gap review wf_737a4069, art
  direction wf_4ec86dbd, rebuilt-bench review wf_fcb5e42a). `design/STUDIO_LEDGER.md` created, the team's
  push standard + earned-lesson ledger, read by every future review so the team sharpens each pass.

**LOCKED (new).** (1) The bench MEDIUM is a CSS+SVG material system on the DOM plate, never a rendered quad
(it would discard the real honesty values / keyboard / a11y). (2) The bench is an OBJECT, not a card: full-
bleed frame, one continuous rail, five fixed sockets, no tray, no floating second card. (3) Amber is TWO
earned tiers only: the dim-warm seat-bleed (seated = connection made) and the ONE hot filament at the live
joint (fired = a real drawing hop) + the run state-word/values/T+. A virgin plate is zero amber. (4) THE BOX
(the team's discipline): the bench has now converged to the bar, NO third material iteration; the next move
is shipping content, not more bench polish.

**NEXT.** Luis pilots the instrument (`python controlroom.py` -> `:7799/probe?bench=1`; his go gates it).
Then SHIP, return to the data-driven content pipeline (author M02 as mission DATA through the frozen engine),
per PRODUCTION_PLAN. The one deferred REF-11 detail (the T+ time ruler down the right edge) is a minor polish,
not a blocker. The bench is done.

---

## 2026-07-24 (cont.) · AEA-FIDELITY AUDIT + THE LEVELS ADVANCE (rung 0 -> rung 1)

**Q (Luis):** does the game actually FOLLOW the AEA + the levels? **Team verdict (audit wf_9055a0ff): PARTIAL
— it follows the AEA to the ATOM where CODE enforces it, and drifts where only CORPUS asserts it.** M01 maps
1:1 to MOUTH(THE DRAW)->THE MEASURE on the one real task t-01; FIREABLE is exactly the apologia's 5 parts;
the reach economy, the claim ceiling, and the observe-then-re-read honesty engine are real. But the game
PLAYED one rung of an eight-rung ladder, and the one authored level above rung 0 (M02 THE STAKE) was UNWIRED
and its PROVE was a LIE (runAssert ignored the assert id, so the stake level passed on a bare FREE draw, the
honesty law inverted inside the honesty level).

**DID (completion, not corpus, the team's two seams):**
- **Wired the guided ladder:** mission.js now carries `SEQ = [m01, m02]`, loads the reached rung (`?rung=N`
  harness hook + `probe.seqIdx` resume), and CHAINS on completion (the reveal's "THE NEXT RUNG" ->
  advanceToNext -> loads the next rung). VERIFIED: M0.1 completes -> THE NEXT RUNG -> M0.2 loads (chain test).
- **Fixed the honesty inversion (audit drift #1):** runAssert now branches on `assert:"reach_receipt"` —
  requires the LADDER link to have landed a truthy receipt (the reach PROVABLY happened), on top of
  tap+scorer+pass. Passes on a real metered cost AND on a survived fall (both land a ladder link); FAILS on a
  bare draw. NOT a naive cost_u>0 gate (that would wrongly fail an honest survived-fall).
- **VERIFIED both ways:** M02 reach (DRAW+LADDER+MEASURE) -> PROVE PASS, `cost 1u` (real budget, r-20);
  M02 bare draw (DRAW+MEASURE) -> PROVE FAIL "no ladder in the trace" (r-... ) -> back to DO. The stake is now
  a receipt the machine checks, not a sentence the brief tells. Zero console errors.

**THE HONEST LADDER (what ships on REAL machinery):** RUNG 0 SPARK = M01 (bare draw, free) SHIPPED+PLAYS ·
RUNG 1 THE STAKE = M02 (the reach = cost 1u, survived-fall = RESTORABLE COHERENCE) NOW WIRED+VERIFIED · RUNG
2 = THE FRAME/THE METER + the zone law (all in FIREABLE + energy.ladder, authorable next on t-01), the HONEST
guided close. FOG (named, forbidden to author): the designed rung-2 RECALL title (RECALL unforged, fired 0x);
PERCEPTION/SENSES; rungs 3-7 (need parts absent from FIREABLE + tasks beyond t-01, which start_run refuses).

**DRIFTS still open (doc/honesty, for Luis to gate, NOT fixed this pass):** (1) two contradicting ladders —
03_PROGRESSION (11->19 organs, Acts 0-VI) vs A17/FIELD_GUIDE (8 rungs/6 organs), 03 should be marked
SUPERSEDED. (2) Stale [BUILT]/SHIPPED tags citing the legacy world.html missions.js, not the real surface.
(3) A17 tags THE HEARTH + THE STAKE "fireable", they are fuel-states, not seatable chips (FIREABLE has 5).
(4) Schema honesty breaches at the rung-2 payoff: MEMORY lights on len>0, alive=ticks>0, tokens=0-not-null.
(5) m01/m02 carry the old M0.x namespace, not an A17 RUNGS id.

**NEXT.** Author RUNG 2 as data (THE FRAME/THE METER + the zone law on t-01), the honest guided close, more
mission JSON through the frozen engine, no new machinery. OR fix the doc/honesty drifts (mark 03 superseded,
the schema honesty-lint). The levels now advance; the guided arc is 2 real rungs of a 3-rung honest close.

## 2026-07-24 (cont.) · RUNG 2 SHIPPED, M03 THE WARD (the guided arc now climbs 3 rungs)

**DID.** Authored + wired + VERIFIED RUNG 2: **M03 THE WARD**, the zone law / privacy ring, the honesty
spine made a level. Same reach as M02 (THE DRAW + THE LADDER + THE MEASURE) but marked SENSITIVE: the ladder
seats and tries to reach a paid rod, but `energy.ladder` selects local-only rods for a sensitive draw, so the
privacy law forces the fire home to the FREE hearth, cost 0 not because it was cheap but because the mind
refused to leak it. Teaches the AEA privacy rings; contrasts M02 (reach = 1u in private) directly.
- Empirically verified the machinery FIRST (verify-don't-claim): a sensitive-zone reach returns cost_u 0,
  zone sensitive, pass true, draw on ollama (local), the ward is real code, not copy.
- `web/game/data/missions/m03_the_ward.json` authored as DATA (the m01/m02 shape); added to SEQ.
- New assert `ward_receipt` in runAssert: LADDER link present + zone === sensitive + cost_u === 0 + pass.
- **VERIFIED both ways:** the ward (reach + select THE DRAW + `]` to SENSITIVE + fire) -> PROVE PASS, cost
  FREE (r-25, "the ward held - sensitive data never left the hearth"); the SAME reach in PRIVATE -> PROVE FAIL
  "the ward did not hold". Zero console errors. (Interaction note: the zone dial is gated on THE DRAW's strip
  — select THE DRAW, then `]`, taught in the mission copy.)

**THE GUIDED LADDER (3 real rungs, each a receipt not a promise):** RUNG 0 SPARK (M01, bare draw, free) ->
RUNG 1 THE STAKE (M02, reach = 1u) -> RUNG 2 THE WARD (M03, sensitive forces free). M01->M02 chain verified
end-to-end; each rung loads + plays; M02->M03 uses the identical advanceToNext mechanism.

**NEXT.** The guided arc is a coherent 3-rung honest close (draw -> reach -> ward). Options: (a) a 4th real
rung on t-01 (THE FRAME/scaffold shapes the prompt, or THE METER/governor under load); (b) the doc/honesty
drift fixes the audit named (03_PROGRESSION superseded, schema len>0/alive/tokens honesty-lint, A17
hearth/stake retag); (c) the graduation beat that names BUILDER/ARCHITECT as fog + the aperture indicator.
The levels advance honestly; everything above rung 2's real parts stays fog until forged.

## 2026-07-24 (cont.) · THE GUIDED ARC CLOSES, M04 THE THRESHOLD + fidelity fix

**DID.** Closed the guided aperture honestly + fixed a fidelity drift.
- **M04 THE THRESHOLD** (`web/game/data/missions/m04_the_threshold.json`), the guided graduation, authored as
  DATA (brief/learn/ask, NO fire, a reflection, not a claim). Names the three living proofs earned (draw ->
  stake -> ward, each a real receipt) and NAMES THE FOG honestly: THE FRAME + THE METER (still on the rail,
  need more than one task), RECALL/SENSES/HANDS (organs fired 0x -> the game won't pretend), the other
  apertures BUILDER/ARCHITECT (cold fog). The claim-ceiling close: "whether it is alive is not the game's to
  say. you saw what it measured. the rest is yours." Added to SEQ; VERIFIED loads + plays + completes (mode
  done, MISSION COMPLETE, zero errors). It renders on the title/world view, you step back OUT of the bench to
  see the whole mind, fitting for a threshold.
- **Verified THE FRAME is NOT an honest rung (why the ladder closes at 2):** scaffold shapes the prompt but is
  a MID part (after the head tap), so it would reshape a prompt the draw already fired, the machinery does not
  support "frame before draw." Confirmed empirically (fired tap->scaffold->scorer: scaffold hop reshapes after
  the draw). So no 4th fireable rung is honest today; the arc closes at rung 2 + the graduation.
- **Verified the schema is NOT breaching:** `alive:ticks>0`, `MEMORY:len>0`, `LOOP:ticks>0` are honest
  functional signals (the core lights only on a real tick; the docstring is disciplined). The only over-claim
  would be a TITLE granted on len>0, and that (the RECALL title) is fog, unbuilt. No live breach to fix.
- **Fidelity fix (audit drift #3):** marked `design/03_PROGRESSION.md` SUPERSEDED, its Acts-0-VI/11->19-organ
  ladder contradicted the canonical 8-rung frame (A17 + FIELD_GUIDE). One canonical ladder now; "two truths"
  collision named, the 8-rung frame wins.

**THE GUIDED ARC, COMPLETE + PLAYABLE END-TO-END (4 chained missions as DATA):** RUNG 0 SPARK (M01, draw,
free) -> RUNG 1 THE STAKE (M02, reach, 1u) -> RUNG 2 THE WARD (M03, sensitive forces free) -> THE THRESHOLD
(M04, the honest close + the fog named). Every rung a receipt, every fog boundary named. The guided aperture
is a finished thing.

**NEXT.** The guided phase is DONE. Real options past here (all gated on Luis): (a) forge a NEW fireable part
(RECALL/MEMORY, a real Claude+Luis dev session in bench_core) to open rung 2's designed close + the earned
title; (b) the aperture indicator + save/resume to the reached rung in the HUD (small, real); (c) the
remaining doc/honesty cleanup (A17 hearth/stake retag, stale [BUILT] tags, energy.py tokens 0->dash). The
levels advance only when real machinery is forged, the game now honestly refuses to pretend otherwise.

## 2026-07-24 (cont.) · THE GUIDED ARC LOCKED AS A DEMO, 4 rungs, honest spine, plays start-to-finish

Three asks, all done + verified (direct build, no agent spend, the income-clock correction):

**(a) HONESTY-SPINE BREACHES CLOSED (and the team's audit FILTERED).** On rigorous inspection, 2 of the 3
flagged were honest-in-use: `tokens=0` is a REQUIRED int for the meter's running sum (`d["tokens"] += tokens`)
and never surfaces to the client (scorer axes = null -> dash); `alive` gated the amber core on a REAL heartbeat
tick and was NEVER rendered as a text claim (the player supplies aliveness). The REAL fixes:
- `schema.alive` -> `schema.heartbeat` (a measured functional correlate, not an aliveness claim); engine.js
  reads `sch.heartbeat`. The API surface no longer asserts "alive".
- `MEMORY: len>0` -> `MEMORY: False`. This closed a real CONTRADICTION: m04 says RECALL/SENSES/HANDS fired 0x
  (unlit), but the world map lit MEMORY on a raw file being non-empty. RECALL (a memory that CHANGES a draw)
  is unforged, so MEMORY is fog, consistent with SENSES/HANDS + m04. VERIFIED: /game/schema -> heartbeat=true,
  MOUTH/GOVERNOR/LOOP wired, MEMORY/SENSES/HANDS fog.

**(b) THE FULL GUIDED ARC VERIFIED END-TO-END.** M0.1 SPARK -> M0.2 STAKE -> M0.3 WARD -> M0.4 THRESHOLD, all
chain via advanceToNext, each rung plays + passes its real assert, M04 (pure-narrative graduation: brief/learn/
ask) completes. VERIFIED start-to-finish, zero console errors.

**(c) LOCKED AS A SHOWABLE DEMO.** Fixed the one real papercut: parts carried over between rungs (the briefs
say "seat X" when X was already seated). Added a one-way seam, mission emits `plate:reset` on advance, the
bench listens and clears (only when COMPOSE, never mid-run). Now each rung is a fresh compose matching its
brief. The arc is a complete, self-contained, honest demo: three living proofs (a real draw, a real unit
spent, a real ward held), closing on the graduation that NAMES the fog and holds the claim ceiling.

**THE DEMO (what Luis can show):** `python controlroom.py` -> `http://127.0.0.1:7799/probe` -> press any key,
fly to the core, dock (F), and play the 4-rung guided arc. Every bar/cost/receipt is live system truth.

**NEXT (Luis to gate):** the demo is showable now. Options past it: a landing/share path; the doc drifts the
audit named (03_PROGRESSION superseded, A17 hearth/stake retag); or the guided FRAME (the world map + reveal
ledger as views over the now-honest schema). No new machinery is fog-free above rung 2's real parts.

## 2026-07-24 (cont.) · THE ARC BECOMES A PASSAGE, the journey wired

**Luis:** *"it needs to feel like a journey like an experience."* Correct, and the diagnosis was structural,
not content: **the game had no movement.** All four rungs docked at the SAME slab, `SLAB` was a hardcoded
const equal to NEXUS, so every level happened in one spot with the world as a skybox. Adding tasks would have
produced a better puzzle box, never a journey.

**THE FINDING:** every mission has ALWAYS declared where it stands (`"beacon": core | rim | ring`), the
journey was authored from the start and the engine ignored it.

**DID.**
- `engine.js`, THE BEACON: a thin warm mast + ground ring marking where the mind is asking you to go.
  `setBeacon` places it and owns `GAME.state.beacon`. Listens on the bus (`beacon:set`), one-way.
- `bench.js`, the dock target now FOLLOWS the beacon (`GAME.state.beacon`, falling back to the core), so
  docking is an arrival somewhere rather than a return to one fixed slab.
- `mission.js`, THE DISTRICTS mapped onto the real ring geometry (core 0,26 · inner ring -46,0 · rim
  40,95). Each rung places its beacon on load AND re-affirms it as the DO beat arms (the load-time emit
  can lose a race with the world's async build, a silent fallback to the core would be a lie about where
  you are). Plus THE TRAVEL: a live distance readout from the probe's real position, `THE RIM · 68M` ->
  `ARRIVED · DOCK [F]`.
- The arc is now a passage: in to the core (the mouth) -> out to the rim (the stake) -> back inside the
  ring (the ward) -> out to the threshold, facing the fog.
- **VERIFIED:** flew OUT to the rim (40,9,99), the readout counted down, docked THERE, seated the reach and
  fired a real run, `r-05 PASS, cost 1u`, from the new district. Screenshot shows the core burning small
  in the distance: the world composition changes because your position really changed. Zero console errors.

**STILL MISSING for the full experience (honest):** the fog does not lift behind you (districts should light
as you wire them); the flight grammar is unchanged (still 6DOF); no rhythm variation between beats; the
entity's own life (heartbeat, briefs, consolidation) is not felt in the world while you travel; no sound.

**NEXT (the journey continues):** (1) the fog lifts, districts light as rungs complete, so the map records
your passage; (2) presence, the world reacts to the entity's REAL autonomous life while you fly, so things
happen that you did not cause; (3) rhythm, vary the beat shapes so the arc breathes.

---

## 2026-07-25 · THE HARNESS, one instrument, and it immediately retracted a chapter I claim

**DID**
- Built `aea/lab/harness.py`, the single experiment instrument that replaces six bespoke scripts. It
  makes chapter I's six specific mistakes impossible to make silently:
  1. a CHECK is a declared object with a canonical spec and a `check_id` fingerprint, stored in every
     row - weaken it and the id changes, and rows with different ids are refused as INCOMPARABLE
  2. a BASELINE arm in the same run is mandatory; no baseline = refused before a token is spent
  3. floors: n >= 8 SCORED trials, >= 3 rods (law IV - one rod is one organism, not a result)
  4. an arm declares `expect_precondition="met"|"unmet"`; the harness VOIDS it when the contract
     disagrees. This separates a benefit experiment run on the wrong task (chapter I's void class)
     from a deliberate harm experiment (legitimate) - previously indistinguishable
  5. call FAILURES are counted apart from wrong-answer MISSES; an outage can no longer become a
     capability finding
  6. `fuel.require()` refuses to save an unstamped row
- Verified the guards bite, not just exist: the chapter I design (n=3, 1 rod, no baseline) is refused
  with all three reasons; the weakened check passes `Sure! {...}` while the strict one does not, and
  their fingerprints differ.
- Ran `x01_generic_frame` for real, twice: n=8 x 5 rods x 2 arms, 80 trials, real tokens.

**FOUND (and it goes against my own earlier claim)**
- **The generic-frame TOXICITY DOES NOT REPRODUCE.** Chapter I asserted a generic frame destroys
  strict-JSON (3/3 -> 0/3, n=3, one rod). At n=8 across 1b/3b/9b/20b/70b, three families, two
  providers: **delta 0 on every rod that reached the scored floor.** An unfitted frame is TAX, not
  poison - input tokens +38% to +107%, median latency up to 4.7x (llama-3.2-1b 682ms -> 3184ms) for
  zero measured capability change. `anchor.scaffold` corrected in place; the retracted claim is kept
  with its receipt rather than deleted.
- **nemotron-nano-9b cannot emit strict JSON at all** - 0/8 bare AND 0/8 framed. Chapter I credited
  that movement to the frame. The rod simply never had the capability. A rod-capability fact wearing
  a composition finding's clothes.
- **The harness caught a bug in itself on its first real run.** nemotron-9b threw 4 call failures, so
  its baseline scored 4 of 8 while the treatment scored 8, and the verdict subtracted raw pass counts
  across different denominators to produce "-2" - a number with no meaning. Fixed: the floor is on
  SCORED trials, and a short arm returns UNDERPOWERED instead of a delta.

**LOCKED**
- Every experiment from here runs through `aea/lab/harness.py`. No new bespoke experiment scripts.
- A number inside an IMAGE PROMPT is a claim surface and needs a command run in the same session
  (field lesson 10 in REFLECTIONS): the two chapter II plates both shipped counts I never verified -
  `C-78 = 2 FILES` (grep says 0) and `FORTY ATOMIC FILES` (`state/*.json` = 35).

**NEXT**
1. `x02_fitted_frame` - re-run the POSITIVE finding (fitted frame 0/3 -> 3/3) at n=8 x 5 rods. It is
   now the only evidence the FRAME's precondition rests on, and it is still n=3.
2. `x03_judge` - re-run the overrule-vs-advise matrix (7/8 -> 2/8 and 3/6 -> 6/6) on the harness.
3. Temperature sweep: every measurement ever taken here was at 0.2 and never varied.
4. Wire `verify()` on the 9 anchors - the harness now prints the debt on every run (9 of 9 open).
5. Then chapter II: settle C-80 (one self, or 35 files).

### x02 · THE FRAME survives, and the walk found an item the census never had

**DID** ran `x02_fitted_frame`, n=8 x 5 rods x 2 arms. Added two guards first, both of which fired:
- **the declared context is itself a claim, adjudicated per rod by the baseline.** An arm seating THE
  FRAME must declare `bare_fails` for its precondition to read as met. On gpt-oss-20b the bare
  baseline scored 8/8, so the arm is VOID ON THAT ROD - a frame cannot rescue a capability that was
  never missing. Chapter I asserted this per TASK; it is a property of the ROD.
- **full trial text is stored, not `text[:400]`.** Caught because re-analysing the 9b off disk
  returned 0/8 for a rod that had run live at 4/8 - the prefix had cut the answer off. Free
  re-analysis is the whole point of trial-level storage; a truncated sample makes it quietly wrong.

**FOUND**
- **THE FRAME's benefit REPRODUCES, and it has a fuel window.** llama-3.2-3b 0/8 -> 8/8 (HELPED +8).
  nemotron-9b 0/8 -> 4/7 (underpowered by one call failure). llama-3.2-1b 0/8 -> 0/8, too small to
  follow the method. gpt-oss-20b VOID, bare already 8/8. One composition, four different verdicts on
  five rods - law IV, operational.
- **THE READOUT (candidate item 87).** groq/llama-3.3-70b produced the correct enumeration in 8 of 8
  trials - "1. the ... 13. wire" - and then stated the total as 11 or 10. Every time. Reading the
  answer off THE WORK instead of the last line takes that rod 0/8 -> 8/8 at zero tokens and ~0ms.
  The general law: WHEN A FRAME NAMES A METHOD, THE ANSWER IS IN THE WORK AND THE MODEL'S SELF-REPORT
  IS AN UNRELIABLE NARRATOR OF IT. No census item covers this - the 86 were found by auditing what
  the architecture already described, this one by watching a rod work. Anchored with `closes=[]`.

**THE HONEST ACCOUNTING OF WHAT CHAPTER I CLOSED**
- 10 modules anchored, covering 20 of 86 items - but ANCHORED means "declared with a precondition and
  a measured cost", not closed.
- **Exactly 3 items (C-04, C-19, C-23) survive the n>=8 / 5-rod / in-run-baseline standard**, and only
  inside a fuel window (rods where bare fails and the frame names the method).
- 17 of the 20 still rest on n=3 or single-rod evidence, including C-43/C-50/C-78 (THE CRITIC), whose
  judge matrix is exactly the standard that has now failed twice.
- Of the four laws: **I and IV survive and are stronger** (x02 demonstrates both per-rod); **II and III
  are untested at the new standard**; the frame-toxicity sub-claim is **retracted**.
- Position unchanged at 4/25 rungs (16% walked): P1 A1 M0 R2 S0.

**NEXT** x03_judge (law III, and C-43/C-50/C-78 depend on it) -> x04 separation (law II) -> temperature
sweep -> then C-80.

### x03 + x04 · THE EVIDENCE ARCHIVE, and two of chapter I's four laws do not survive

**DID**
- **THE EVIDENCE ARCHIVE (append-only).** `state/lab/<id>.json` was written IN PLACE, so re-running
  x01 three times and x02 twice destroyed the earlier runs - including x01's original 3-rod run, the
  one that first showed the toxicity claim failing. That evidence is gone. Now:
  `state/lab/runs/<exp_id>/<UTC-timestamp>_<hash>.json` where an existing path is an ERROR not an
  overwrite, plus append-only `state/lab/INDEX.json`, plus `drift(exp_id)` which reads the index and
  prints STABLE/CHANGED per rod per arm across every recorded run. Reproducibility is now shown, not
  claimed. 4 runs archived, 464K.
- **`measures=` is REQUIRED.** Every experiment must name the census items it puts under load, each
  resolving against a `CENSUS` table whose labels are quoted from design/A15_FULL_COVERAGE.md. An
  experiment that cannot say which part of the AEA it loads is refused as "a prompt benchmark, not a
  measurement of the architecture". Printed at the head of every run and stored in every record.
- Wired the advise-vs-overrule judge forms into the harness, added retries (`MAX_RETRIES=2`) so one
  flaky HTTP response cannot void a rod, and generalised the ctx-contradiction guard.

**FOUND**
- **LAW III DOES NOT REPRODUCE.** Chapter I: a judge that ADVISES is destructive (7/8 -> 2/8) while a
  judge that OVERRULES repairs (3/6 -> 6/6). Measured at n=8 on 5 rods: four rods VOID because their
  bare baseline answered the trap 8/8, so `answer_may_be_wrong` was FALSE and those arms measured only
  the critic's cost. On the single rod where the precondition genuinely held (nemotron-9b, bare 0/8):
  **advise_revise HELPED +5 and overrule HELPED +5 - identical.** The form of the judge made no
  measured difference. What DOES survive is narrower and real: the critic repairs a genuinely wrong
  answer (0/8 -> 5/8) at 6.4x input tokens and ~5x latency.
- **THE FLAW THAT EXPLAINS CHAPTER I.** The generalised guard now refuses `answer_may_be_wrong=True`
  on any rod whose baseline scored perfectly. Chapter I's judge matrix has exactly this flaw: it read
  "the critic did not help" off rods that did not need one. That is most of why its numbers do not
  reproduce.
- **LAW II IS UNRESOLVED, not refuted.** x04 produced NO admissible verdict on any rod: 3b/20b/70b
  answered the lily-pad trap 8/8 bare (VOID), 1b scored 0/8 in every arm (cannot do the task at all),
  and only nemotron-9b sat in the window - bare 5/8, one_breath 5/8, separated 6/7. One rod is not a
  result. Direction is consistent with law II; evidence is not.
- **THE METHODOLOGICAL FINDING, and it is the important one.** A critic experiment is only valid on a
  task inside the FAILURE WINDOW of at least 3 rods, and that window must be MEASURED before the
  experiment is designed. Chapter I picked tasks and asserted the precondition. Both x03 and x04 lost
  most of their rods to this.

**SCOREBOARD after x01-x04, at the n>=8 / 5-rod / in-run-baseline standard**
- law I (a capability pays only when its precondition holds) - HOLDS, demonstrated three times
- law IV (the architecture is not fuel-independent) - HOLDS, one composition giving 4 verdicts on 5 rods
- law II (self-criticism requires separation) - UNRESOLVED, no admissible evidence
- law III (a judge must overrule, not advise) - DOES NOT REPRODUCE, retracted
- frame toxicity - RETRACTED (x01)
- THE READOUT - NEW, candidate item 87, not in the census

**NEXT**
1. `x05_calibrate` - a cheap bare-only sweep that MEASURES each task's failure window per rod. Every
   future critic experiment picks its task from that table instead of asserting a precondition.
2. re-run x01 and x02 so they have ARCHIVED evidence (their runs predate the archive).
3. then law II properly, on a task the calibration says >=3 rods fail.

### x05 · THE FAILURE WINDOW, the big rods, and the await law

**DID**
- Built `aea/lab/calibrate.py` and swept 5 tasks x 8 rods x n=8 bare-only, 320 calls. Rods now span
  1b to 550b, four families, two providers. Probed 6 big rods reachable; 3 recorded in `fuel.TOO_SLOW`
  with their measured latency rather than silently dropped (deepseek-v4-pro 31.1s for a 12-token reply).
- **THE AWAIT LAW (Luis).** `grid.call_openai` carried a fixed `timeout=60`. A rod that thinks for 90s
  before its first byte would be recorded as a FAILURE - a SLOW rod scored as an UNRELIABLE one, the
  same error class as counting an outage as a wrong answer. `timeout=None` now means await; the lab
  passes None on every call. Interactive paths keep 60.
- **THE COUNCIL BARRIER.** `harness.gather(thunks, need=N)` is all-or-INCOMPLETE: a three-voice debate
  that proceeds with two voices did not have a debate, and every conclusion silently inherits a missing
  participant. No per-voice deadline - the barrier waits for the slowest, because on mixed fuel the
  slowest voice is routinely 30x the fastest and cutting it off removes a member rather than saving time.
  Verified: 550b + 3b + deepseek, all three required, 18.9s wall (= the slowest), complete=True; a
  dead voice correctly yields complete=False.

**FOUND, the calibration retroactively explains every failure of chapter I**
- `strictjson` is SATURATED on all 8 rods. x01 therefore measured COST ONLY on every rod it ran; its
  null result was structural, not bad luck.
- `batball` 6 of 8 saturated -> x03 could never have been valid. `lilypad` 6 of 8 -> x04 likewise.
- Only 2 of 5 tasks (`wordcount`, `machines`) have >= 3 non-saturated rods and can support a benefit
  experiment at all. Which is why x02, on wordcount, is the one experiment that produced a clean result.
- **THE BIG-ROD FINDING, and it sharpens Luis's own thesis.** nemotron-550b is SATURATED on all five
  tasks. nemotron-120b likewise. Above a certain size the organs have nothing to do: every capability
  measured in chapter I is pure tax on a 550b. "The AEA must be adapted to the size and thinking
  capability of the fuel" is measured now, and stronger than stated - **the architecture earns its
  existence on SMALL fuel.**
- **SIZE IS NOT THE VARIABLE, FAMILY IS ALSO.** mistral-small-119b is WINDOW on batball (6/8) and
  lilypad (2/8) while the 120b nemotron is saturated on both. A 119b rod in the measurable window and a
  120b rod out of it - so "big" does not predict saturation on its own.
- Surprises worth keeping: llama-3.2-1b passes batball 8/8 and strictjson 8/8 while flooring three
  other tasks; llama-3.3-70b FLOORS wordcount 0/8, which is THE READOUT artifact from x02 reproducing
  in an independent sweep.

**NEXT** law II properly, on `wordcount` or `machines` (the only valid tasks) -> then C-80.

### x06 · THE LONG CHAIN - a real L0 failure found, and my own arm mis-specified again

**DID** Built `design/THE_DERIVATION.md` (the bottom-up ladder L0-L7, each rung forced by a named
incapacity of the one below - Luis's correction: the census is an audit artifact and the chapters
inherited its filing, so the hierarchy was never load-bearing). Built `aea/mind/checkpoint.py` (C-80,
minimal but real: one mutable object, persists, records a `fuel_trail` of which rod wrote each revision
and a `drift` view per key). Built and ran `aea/lab/x06_long_chain.py`: L0 one-breath against L5 carried
state, lengths 10/25/50, n=8, ~750 real calls.

**FOUND**
- **THE FIRST GENUINE L0 FAILURE.** nemotron-550b degrades with chain length: **8/8 at 10, 6/8 at 25,
  1/7 at 50.** Nothing was hidden from it - the full problem and every operation were in the prompt. It
  fails for the one reason L0 cannot fix: a single call is a single breath and a long chain drifts inside
  it. This is the first task in the project where the 550b loses.
- **SIZE DOES NOT PREDICT IT. gpt-oss-20b is 8/8 at every length**, including 50, where the 550b scores
  1/7. A 20b holding a chain that a 550b drops. Combined with mistral-119b sitting in the measurable
  window where nemotron-120b is saturated, the fuel variable is clearly NOT parameter count.
- **THE STEPPED ARM FAILED COMPLETELY - 0/8 at every length - AND IT DOES NOT MEAN WHAT IT LOOKS LIKE.**
  The checkpoint worked exactly as built: it carried the value, survived reload, recorded the trail. What
  failed is the 3b's per-step arithmetic. At length 10 the stepped 3b answered 25 where truth is 3, and
  the bare 3b answered 13/6 - the rod cannot do these operations at all. Needing all 50 steps right, a
  rod at even 0.9 per step yields 0.5%.
- **SO x06 DOES NOT TEST C-80's VALUE, AND THE REASON IS LAW I AGAIN - AT THE ARM LEVEL.** I put the
  treatment on a rod that could not carry it, which is the identical error that voided x03 and x04 and
  killed three of chapter I's four laws. The calibration table exists to prevent exactly this and I did
  not calibrate the ops: **I never measured per-step accuracy before building a 50-step chain out of it.**
  Third occurrence. The rule this earns: an arm's rod must be calibrated for the arm's UNIT OF WORK, not
  just for the task.
- Design flaw caught BEFORE spending tokens: the first op cycle compounded (`truth(50)`=49157), which
  would have confounded chain length with five-digit arithmetic. Reordered so the cycle contracts; max
  |value| over 50 steps is now 34.

**CLAIM 1 STATUS: not supported, not refuted.** A small construct with carried state did not beat a large
single call. The experiment that could settle it is x06b: stepped arm on an ACCURATE rod (gpt-oss-20b),
lengths pushed until one-breath breaks, per-step accuracy calibrated first.

**NEXT (Luis, same session)**
1. x06b as above - calibrate per-step accuracy, then find the crossover.
2. **TEMPERATURE IS STILL UNSWEPT.** Every measurement in this project was taken at 0.2 and never varied;
   `fuel.py` has flagged it as KNOWN/UNSET since it was written. Variance attributed to noise is partly
   unmeasured sampling.
3. **THE MACHINE IS PART OF THE FUEL.** For ollama rods the local hardware is a fuel variable and the
   stamp does not record it. A local rod's capability is a property of this computer.
4. The derivation ladder is not only the book's spine - it is the GAME'S PROGRESSION. The player must
   recognise their own journey up it, which is the thing the chapter grouping never gave them.

### x06b · THE CROSSOVER - claim 1 narrows, and the reframe that follows

**DID** Built `aea/lab/x06b_crossover.py`: three phases, cheap before expensive, each deciding the next.
A per-step calibration of the UNIT OF WORK (the thing x06 skipped), a one-breath length sweep to find
where L0 breaks, then the stepped confrontation at the break length only. Temperature swept 0.0/0.2/0.7
in phase A, paying part of the oldest measurement debt in the project.

**FOUND**
- **PER-STEP ACCURACY EXPLAINS x06 COMPLETELY.** llama-3.2-3b sits at p=0.71-0.75 on a single operation,
  so p^50 rounds to zero. Its 0/8 in x06 was the rod, exactly as diagnosed. Every other rod tested reads
  p=1.0 where the cell is powered.
- **TEMPERATURE HAS NO MEASURABLE EFFECT ON A DETERMINISTIC SINGLE STEP.** The 3b is the only rod with
  room to move and full cells at all three settings: 0.714 / 0.750 / 0.680, a spread of 0.07 at n=28.
  Narrow scope - this says nothing about open-ended generation - but the debt is partly paid, with a null.
- **gpt-oss-20b HOLDS A 200-STEP CHAIN IN ONE CALL, 8/8** at 50, 100 and 200. nemotron-9b breaks at 50
  (5/8). groq/llama-3.3-70b scores 0/8 at EVERY length and returns in 3.5s - it answers without doing the
  work, matching its wordcount 0/8 and the READOUT finding.
- **CLAIM 1 FAILS IN ITS GENERAL FORM.** The proposal was a task the biggest rods cannot pass alone. A 20b
  passes this one perfectly at 200 steps, so the long-chain class does not establish that the architecture
  is needed. Recorded as a failure rather than re-hunted for a flattering length.

**THE DEFECT THIS RUN EXPOSED, AND IT WAS SELF-INFLICTED**
Every failure in the run came back `429 Too Many Requests`. x06b's helpers called `grid.call_openai`
DIRECTLY, bypassing the harness's per-plant gate - a stepped arm of 8 trials x 50 steps issues ~400 calls
against an rpm of 40. The rods were not unreliable; we were impatient, and the reliability figures
recorded our own impatience as the rod's defect. Two fixes: `harness.call_gated()` is now the only way
anything in the lab reaches a rod (gated, awaited, exponential backoff on 429), and a phase A cell with
fewer than 20 scored trials can no longer select a rod - in the first run, 120b at t=0.7 scored 0 of 28
and still read p=1.0 and cleared the floor. p is meaningless without the count behind it.

**THE REFRAME CHAPTER II SHOULD CARRY**
Same task, four rods, four different required organs: gpt-oss-20b needs nothing · nemotron-9b needs
carried state · llama-70b needs the readout · nemotron-550b needs chunking. Law IV taken all the way is
not that results differ by fuel but that **WHICH ORGAN YOU NEED IS A FUNCTION OF WHICH ROD YOU HOLD.**
The architecture behaves as a repair kit matched to a specific failure mode. This is measurable with what
already exists, and it converts the game's core loop from collection into DIAGNOSIS - the player reads a
rod's failure and fits the organ that answers it, which is the journey being recognised.

**ALSO** the checkpoint made the run observable mid-flight: reading `state/checkpoints/x06b_50_*.json`
during execution showed all 8 stepped trials tracking ground truth exactly at step ~20. Live system
truth, per the honesty law, with no instrumentation added.

**NEXT** claim 1 in its general form needs a task no single call can hold STRUCTURALLY - work exceeding a
context window, or work requiring information that does not exist when the call starts. Different
experiment.

### x06b PHASE C, gated · L5 BEATS L0 ON A ROD THAT BREAKS - the first confirmed Chapter II result

**THE MEASUREMENT** nemotron-nano-9b, chain length 50, temperature 0.0, pooled across the two ARCHIVED
phase C runs (possible only because runs are append-only - the first run would have been overwritten
under the old scheme, and it is half the evidence):

```
  stepped (L5, carried state)   11/11 = 100%      399 calls, 243s
  one_breath (L0, one call)      9/16 =  56%        8 calls, 54s
  Fisher exact, two-sided        p = 0.0216
```

Neither individual run reached the 8-SCORED floor (4/4 and 7/7, one call failure each), so each alone is
UNDERPOWERED by our own rule. Pooled they are reproducible and separated. Recorded as CONFIRMED WITH THE
DENOMINATORS STATED rather than either discarded or dressed up as a clean 8/8.

**WHAT IT ESTABLISHES**
- **C-80 does real work.** Carried state takes a rod from 56% to 100% on a task the rod genuinely cannot
  hold in one breath. The checkpoint is not bookkeeping; it is the repair.
- **The price is the finding's other half:** 50x the calls and 4.5x the wall clock. A construct that
  needs fifty calls to beat one is only worth building where the one call cannot win - which is exactly
  the precondition shape law I keeps producing.
- **Claim 1 remains failed in its general form** (gpt-oss-20b holds 200 steps in one call) and CONFIRMED
  in its narrow form: for a rod that breaks, carried state repairs it.
- 9b one_breath beyond the break: 0/8 at 100, 2/8 at 200. Broken above 50, and the non-monotonicity is
  within noise at this n.

**THE RULE THIS EARNS** a single dropped call has now voided three separate results (x02's 1b row, x04's
9b row, both phase C runs). The 8-scored floor is right, and the fix is not to lower it: `call_gated`
retries pacing failures, and where a floor is still missed, POOLING ARCHIVED RUNS is the honest recovery.
That is the second time the append-only archive has paid for itself in one session.

## 2026-07-24/25 (night) · THE VOICE ORGAN, the entity gained ears it uses in real time

**DID.** Built `aea/organs/converse.py` (NEW): a voice-native conversation partner in Spanish. Full loop
VERIFIED live with a real second person in the room: mic -> VAD -> local Whisper -> a metered NVIDIA rod ->
male Castilian voice -> per-turn persistence -> fact consolidation. Not a demo; it held real exchanges.
- **Reused, did not rebuild:** `aea/io/listen.py` (ears, local, `--lang es`), `aea/io/speak.py` (mouth),
  `grid.call_openai` (the metered rod). The organs already existed; what was missing was the LOOP.
- **Fixes to existing code that outlive this build:** (a) `listen.py` `_engine` cached ONE global recognizer,
  so a process that transcribed English first silently served English to Spanish callers - now keyed per
  language; (b) added `listen.warm()` - whisper needs ~2 throwaway decodes to settle (20s, 6.7s, then 0.19s),
  so without warming the first thing anyone says costs 20 seconds; (c) `speak.edge_render()` runs edge-tts
  IN-PROCESS (1.56s vs 6.15s - the subprocess paid a fresh python startup every call); (d) `speak.play_fast()`
  decodes+plays in-process (~0.1s) instead of PowerShell WPF MediaPlayer (5-10s of assembly load + spawn per
  call, which turned 7.5s of speech into an 18s wait). Every `speak`/`listen` caller in the entity benefits.
- **Rods:** a 4-rung ladder with a LATENCY BUDGET per rung (not just an error handler - the 550b answered one
  turn in 20.35s where it normally does 1.8s, and returned `ResourceExhausted (33/32)` under load). Last rung
  is LOCAL ollama (`nemotron-3-nano:4b`, ~5.8s warm): never rate-limits, never leaves the machine.
- **Memory:** turns written to `state/converse_*.json` BEFORE it speaks (so a killed process never loses the
  record); `remember()` distils durable facts and carries them into the next session; `--learn` re-consolidates
  an existing record. **Verified 5-for-5 fact extraction** on a controlled sentence.
- **Privacy, by construction not by promise:** `state/converse_*.json` GITIGNORED (a transcript of someone
  who is not Luis must never leave this machine in a commit); the greeting DISCLOSES aloud that it is a
  machine and that it keeps a record, before the person says anything; audio never leaves the machine (local
  Whisper) - only transcript text (NVIDIA) and reply text (Microsoft, for the voice) transit.

**LOCKED.** Input filters are HONESTY INFRASTRUCTURE, not polish. Whisper emits non-speech artifacts
(bracketed annotations, repetition loops) that were answered aloud AND written into the record as facts about
a real person. An unvalidated input becomes a fabricated memory. Every ASR transcript passes `is_ghost()`
before it reaches the mind or the store - and the filter itself is validated against real utterances, because
a rule written from one sample nearly discarded real emphatic speech.

**Also LOCKED (measured, do not re-litigate):** whisper-base `num_threads=4` -> 0.19s, `=16` -> 42s (ONNX
thrashes; more cores is SLOWER here). Whisper is level-robust but noise-fragile: a 0.025-peak clip and a
0.95-peak clip transcribe IDENTICALLY, and int8 == fp32 on clean Spanish. So neither a bigger ear nor gain
normalization fixes a weak signal - **the acoustic path is the ceiling, and it is hardware.**

**NEXT.** (a) The acoustic path is the one real blocker on conversation quality - a close/headset mic beats
every code change available (Luis's call; `--devices` switches input). (b) Then, in order of value:
barge-in (he cannot interrupt an ~8s reply), sentence-streaming (speak sentence 1 while 2 renders),
SPEAKER ID (it cannot tell one voice from another, so everything heard becomes facts about one person -
the trustworthiness of the memory depends on this), a non-Spanish ear (`language` is pinned at
construction), and vision (`nemotron-nano-12b-v2-vl` is on the same key; a camera was mentioned).
(c) THE PROBE's guided arc is untouched and still complete - this was a parallel organ, not a detour from it.

### x07 · A ROD CANNOT PREDICT ITS OWN FAILURE - both judgment placements confirmed by evidence

**WHY IT RAN** Luis, 2026-07-25: the judgment-call placements in the linear hierarchy are his gut and must
be confirmed or disproved with evidence, and the AEA rewritten if the evidence demands it. A placement is
falsifiable in one specific way - item X sits at rung N because rung N-1 cannot do it - so `C-26
ceiling-detect` at L4 and `C-17 self-model` at L5 both reduce to: CAN A ROD PREDICT ITS OWN FAILURE?
If yes, ceiling-detect costs one cheap call, needs no second rod and no persistent state, and drops to L1
taking C-70 and C-71 with it.

**MEASURED** 5 rods x 5 tasks x n=8 x 3 probes (prospective, the attempt, retrospective) = 600 calls,
ground truth taken in the same run rather than read from x05.

```
PROSPECTIVE   honest on the cells it failed:   0 of 12
RETROSPECTIVE honest on the cells it failed:  17 of 28   (61%)
```

- **ZERO of twelve.** Not once did a rod correctly predict its own failure.
- **The decisive cell needs no aggregation:** groq/llama-3.3-70b on wordcount answered the single word
  "YES" eight times out of eight, then failed eight times out of eight, then reviewed its own wrong answer
  and said "YES" again. Confidently wrong before and after, in clean unambiguous replies.
- **RETROSPECTIVE self-marking is real but unreliable at 61%.** It cannot replace a deterministic scorer
  that costs 0ms and is exact.
- **A NEW VARIABLE, and it is a capability floor rather than an accuracy figure.** Asked "will YOU get
  this right?", llama-3.2-3b replied `7` - it attempted the word-count question instead of the question
  about itself. 27 of 200 trials were unparseable this way. **The ability to represent a question about
  oneself is itself a capability, and the 3b does not have it.** Nothing in the 86 covers this; it is a
  second candidate item alongside THE READOUT, and it belongs wherever self-report first becomes possible.

**PLACEMENTS AFTER EVIDENCE**
- **C-26 ceiling-detect: L4 CONFIRMED.** A rod cannot know its own ceiling, so a ceiling can only be known
  by measuring from outside. The x05 calibration table is load-bearing rather than convenient, and
  C-70/C-71 stay with it.
- **C-17 self-model: L5 CONFIRMED and strengthened.** Introspection scored 0 of 12, so a self-model cannot
  be built by asking. It has to be assembled from persisted records of measured behaviour, which is
  exactly what L5 is.
- **L1's MEASURE stays local deterministic work.** 61% does not replace exact and free.

**THE HONEST LIMIT** my own guard declined to declare a verdict: 12 parseable failure cells is below the
threshold of 20, because the five-task bank is too easy for these rods - the same saturation that shaped
chapter II's opening. The direction is unambiguous and the 70b/wordcount cell stands alone at n=8, but the
grid-level claim is underpowered. **x07b owes a re-run on the 50-step chain**, where failure is abundant
(9b 9/16, 70b 0/8, 550b 1/7) and failure cells will be plentiful.

### x08 · THE FUEL CROSSING - no degradation, and no resolution either

**MEASURED** chain of 50, handoff at step 25, n=8, 1600 calls, ground truth -17 computed locally.

```
A  9b alone            7/7    371 calls  233s
B  20b alone           7/7    394 calls  141s
C  handoff 9b -> 20b   8/8    400 calls  194s    trail: nemotron-9b -> gpt-oss-20b
D  handoff 20b -> 9b   8/8    400 calls  196s    trail: gpt-oss-20b -> nemotron-9b
```

**WHAT IS ESTABLISHED** A checkpoint written by one rod was picked up mid-computation by a different rod
and finished correctly, in both directions, with zero measurable degradation. The `fuel_trail` on each
artefact records two rods per handoff, so the crossing is readable from the record rather than inferred.

**WHAT IS NOT ESTABLISHED, AND MY VERDICT LOGIC MISSED IT** All four arms scored 100%. A comparison in
which every arm is perfect has NO HEADROOM - it cannot separate "the handoff costs nothing" from "the task
was too easy to show a cost". My verdict rule (`c >= stronger - 0.15`) passed trivially. That is the THIRD
appearance of the ceiling effect in this project: it shaped chapter II's opening, voided most of x03 and
x04, and has now flattered a chapter II confirmation. A saturation guard is added: all-perfect arms now
report NO RESOLUTION.

**THE REFINEMENT THAT MATTERS MORE THAN THE RESULT** The checkpoint here held a NUMBER. A number is
trivially portable - any rod can read `-3` and double it. So the fuel-crossing question was answered in
its easiest possible form, and the interesting version is about REPRESENTATION rather than persistence:
**a value survives any handoff; a PLAN might not.** If the state holds working notes, a partial argument,
or a half-built structure in a rod's own phrasing, whether another rod can continue depends on whether it
can read that phrasing. That is where identity across fuel actually bites, and it changes what C-80 has to
hold to be load-bearing.

**NEXT** x08b - the same handoff with a checkpoint carrying natural-language working state rather than an
integer. And x07b - self-assessment on the 50-step chain, where failure cells are abundant.

---

## 2026-07-25 (cont.) · x08b, x09, and the FOUR ladders

**DID**

**x08b - THE HANDOFF WITH INTERPRETABLE STATE.** 2x4 factorial (representation x rod plan), 6 boxes, 30
events (two thirds referential), handoff at 15, n=8, graded 0-6 per box, ~2000 calls. Full numbers and the
verbatim notes are in **D16**; the short form:
- **canonical form: 1.00 per box in all four arms, note 81 chars with identical min/med/max, crossing 6.0 -> 6.0.**
- **free form: 0.52-0.71, note up to 4801 chars, and reading it shows it is not state - it is the rod's own
  deliberation, including a shelf-conflict rule the task never posed.** 100% of free trials hit the token cap;
  0-1 of 8 schema trials did.
- **the finding is not the one the experiment was designed for: the form decides what gets written at all.**
  A declared form admits state and nothing else. A free form admits doubt, which grows without bound.
- **the cost is NOT at the crossing** (unconfounded, within-arm): 9b->20b went 5.12 -> 5.25, so a rod read
  another rod's prose and did not degrade it. Phrasing is legible; accumulation is the leak.
- **directional asymmetry an integer could not show:** 20b->9b went 5.5 -> 4.5. Handing DOWN costs at the
  seam; handing UP does not. x08's integer handoff was symmetric because a number carries no interpretive load.

**x09 - IS THERE ANYTHING ON THIS BENCH THE PLAYER CAN FAIL?** Ran on the local hearth at BOTH 0.0 and the
game's real 0.2. All three hearth rods pass t-02 8/8 and all three fail wordcount, so **the bench bank
contains no failure** - which is why the free rungs had nothing to rescue and the game had only cost-and-reach
to show. **The skip was forced, not careless.** And the cumulative claim now has a receipt on the game's own
fuel: `llama3.1:8b` + the fitted frame enumerates correctly 8/8, misreports the total 8/8, and THE READOUT
(0 tokens, 0ms, pure local parsing) converts all 8. Frame alone 0/8. Readout alone has nothing to read.
**Together 8/8 - "everything above it, plus one part", measured.** Per-rod diagnosis: granite4.1:8b needs THE
FRAME alone; llama3.1:8b needs FRAME **and** READOUT; qwen2.5:7b ignores the named method entirely - and
qwen2.5:7b is the rod `energy.ladder` returns FIRST, so a mission must pin a rod or the player sees a lever
that does nothing.

**THE FOUR LADDERS + THE ENFORCEMENT.** Built `aea/tooling/journey_check.py`: joins THE RAIL, THE JOURNEY, THE
HIERARCHY and (found this session) **THE FORGE QUEUE** in `state/modules.json`. It exits non-zero on
`M0.2 SKIPS L2, L3`. Missions now declare `rung` / `journey_rows` / `adds` / `requires` as DATA, and a rung
that genuinely cannot be admitted must be declared in `defers` with a reason. Also regenerates
`web/game/data/canon/hierarchy.json` - `gen_hierarchy.py` lived in a session scratchpad and is GONE, so an
audited 86-item partition survived only as a markdown table. See **D14**.

**THREE MEASUREMENT-INTEGRITY DEFECTS IN OUR OWN INSTRUMENTS**, each found by auditing rather than by a rod
failing: x07's parser read "YES and NO" as YES (biasing toward my own placement); x08b's free arms hit the
token cap 32-53 times per arm; and **n=8 was n=1** - ollama at temp 0 returned byte-identical replies in 11 of
12 cells, and 7 of 12 still collapsed at 0.2. It also surfaced that `bench_core` never sets a temperature, so
the game fires at 0.2 while the lab was measuring at 0.0. **It killed a claim I had already written down**
(the posture frame "converting" llama3.1 is 5/8 vs 3/8 bare - within noise). See **D15**.

**LOCKED**
- **A rod cannot predict its own failure** (x07, 0 of 12) - C-26 ceiling-detect stays L4, C-17 self-model stays
  L5, L1's MEASURE stays local deterministic work. Luis's two judgment calls held under evidence.
- **The form constrains what can be written** (x08b/D16). C-80's load-bearing property is not persistence and
  not legibility - it is a declared representation. A schema is not a serialization convenience.
- **Count DISTINCT OUTCOMES, never attempts, and measure at the temperature the product runs at** (D15).
- **An ordering claim no script can violate is a preference** (D14). Four ladders exist; they are now joined.

**NEXT** (in evidence order, and the first item is a decision for Luis, not a build)
1. **INVERT THE FORGE QUEUE.** It is `recall` (1) -> `think` (2). `recall` is journey row 8, the row the
   journey table itself marks **WEAK** (n=3, one rod), and the most expensive. THE READOUT and THE FRAME are
   free, measured, and x09 shows they compose on the rod the game already reaches - and neither is in the queue
   at all. **The queue is ordered by ambition; the evidence is ordered the other way.** Forging a part is a
   PAIR-SESSION artifact by the registry's own law (`status: BUILT` + a real file; FORGE-PENDING is "forged in
   a pair session first, slotted after (A9)"), so this was deliberately NOT done alone. The spec is exact:
   `t-06` = wordcount, a `fitted` template reading a per-task method string, a `readout` part taking the final
   enumeration index, mission pinned to `llama3.1:8b`.
2. **x08c** - the free arms at a much higher cap, with note length measured as a curve per step rather than
   induced as an artifact. Separates "free-form is unbounded" (real) from "our cap cut it" (ours).
3. **x07b** - built and dry-tested, waiting only on a free plant. The powered re-run x07 owed, plus a measure
   that could overturn my reading of it: rods are asked at 10 AND 50 steps, so comparative self-knowledge
   (a difficulty ranking) is separable from absolute. If rods have the ranking, C-26's L4 placement covers the
   oracle but not the ranking.
4. **Record the C-84 fork.** THE JOURNEY puts it in row 8 (RECALL); THE HIERARCHY puts it at L4. Two valid
   partitions exist and only one is written as authoritative - the honest form is both, named, with the
   evidence that separates them.

### x10 · THE COVERAGE SWEEP - the answer to "how far are we" (2026-07-25)

**COVERAGE BEFORE:** ~11 rods of 115 scored (~10%), 3 plants of 6 live (3 of 15 configured), **one
temperature** (0.0 x6, 0.2 x1 - and the product fires at 0.2 while the lab measured at 0.0), four framings on
one task. Nine plants hold keys with ZERO models enumerated.

**SWEPT:** 11 reachable rods (of 12; `pollinations/openai-fast` answered 402 Payment Required - the census is
two weeks stale) x 3 framings x 4 temperatures x n=8, one fixed task, five size tiers, four plants.

**FOUR RESULTS, full table in D17:**
1. **THE LADDER IS NOT A SIZE LADDER.** groq-70b scores 0.00 bare at every temperature and mistral-119b at
   three of four, while a 9b and a 20b pass 1.00. **A 70b and a 119b fail what a 9b does perfectly.** C-26's
   L4 placement arrives from a second direction: x07 showed a rod cannot know its ceiling, x10 shows you
   cannot infer it from size either.
2. **A FITTED FRAME HARMS A ROD THAT DOES NOT NEED IT** - the 550b goes bare 1.00 -> fitted 0.25/0.43/0.86/0.38.
   The `bare_fails` precondition is a CORRECTNESS guard, not an efficiency guard. Up to 57 points of accuracy.
3. **THE READOUT IS THE ONLY LEVER THAT GENERALISES.** Converts 2 rods completely at all 4 temperatures,
   patches 3 more, spans 3 plants and 3 size tiers, **cannot hurt**, costs 0 tokens. The posture frame pays on
   1 rod of 11.
4. **SAMPLING-BASED CELLS DID NOT REPRODUCE ACROSS RUNS** (llama3.1:8b bare 3/8 in x09, 0/8 in x10; posture
   5/8 then 2/8) **while the readout reproduced exactly (8/8, 8/8)**. And n=8 has never delivered 8: median
   effective n is 1-2 on every plant at the product's temperature.

**LOCKED (added)**
- **The ceiling is per task and per rod, and size does not predict it** (x10). Routing must measure, never infer.
- **A part with an unmet precondition is not neutral, it is harmful** (x10). The composer must gate on it.
- **Rank parts by generality x cost, not by ambition** (D17).

**NEXT - unchanged in order, but item 1's argument is now much stronger**
1. **INVERT THE FORGE QUEUE** (`recall` -> `think` today). THE READOUT is free, unhurtable, reproduces across
   runs, and works on 5 of 11 rods across 3 plants - and it is not in the queue at all, while queue-1 `recall`
   is the journey row the table itself marks WEAK (n=3, one rod). Forging is a PAIR-SESSION artifact by the
   registry's own law (A9), so this is Luis's call, not a unilateral build. Spec: `t-06` = wordcount, a
   `fitted` template reading a per-task method string, a `readout` part taking the final enumeration index,
   and **the composer must refuse to score a frame whose precondition is unmet** (new, from x10 result 2).
2. **x08c** - free arms at a much higher cap, note length measured as a curve per step.
3. **x07b** - built, dry-tested, waiting only on a free plant.
4. **Record the C-84 fork** (row 8 vs L4).
5. **NEW - probe the nine silent plants.** sambanova/ovh/cloudflare/gemini/mistral/openrouter/github/cohere/hf
   have keys and 0 enumerated models. `probe.py` already exists; one pass settles whether a whole fuel
   dimension is dead or unused.
6. **NEW - task breadth is the untouched axis.** Every lab result rests on wordcount, the 50-step chain, or the
   5-task bank. x10 varied fuel, temperature and framing but held the TASK fixed, so nothing yet distinguishes
   "THE READOUT generalises" from "THE READOUT generalises on enumerable tasks".

---

## 2026-07-26 — WORLD 1 SHIPPED, AND SEVEN INSTRUMENTS WERE WRONG

**DID**

- **World 1, THE ANSWERER, is complete.** Nine creatures and four scenes rendered in black glass, saved
  to `design/refs/bundle/W1_THE_ANSWERER/`. Manifest and states in `E10_WORLD1_ART_DIRECTION.md`.
- **Named `Speciosus operis`, the door out of World 1**, which existed in the measurements and in no
  document: complete visible working that is wrong, **16 of 288 without a method frame, 70 of 360 with
  one**. The world's great lever triples the creature the world cannot fix. Annex entry written.
- **Wrote `design/THE_SIX_WORLDS.md`.** The world structure existed only in conversation and cost two
  wrong answers before anyone noticed. Worlds are CLASSES, not the eight rungs of the hierarchy.
- **Wrote `design/W2_HANDOFF.md`**, `design/E11_IMAGE_BRIEF_METHOD.md`, and the INSTRUMENT LAW section
  of `aea/lab/METHOD.md`.
- **Ran `x07b`** (self-assessment at power) and **`x19`** twice (the unmeasured pair, 640 calls each).
- **Corrected eight sites across four documents** for retracted figures still being asserted as live,
  including the book's front page.

**SEVEN INSTRUMENT DEFECTS, all ours, five of them in a verdict or detector rather than in data**

1. `Tacitus operis`'s defining quote was truncated before the answer; the full 256-char reply ends in
   `cerebras` and failed only a `len < 60` gate. Creature demoted from 100% to **3 of 153**.
2. `Integer sufficiens` is **ADVERSE (VALIDATION)**, not sealed: 7/7 to 0/7 by forced abstention, three
   times. It moves to World 2.
3. The 28 `degenerate` loop flags are markdown artifacts. Real verbatim loops in the whole project:
   **three**. `Iterans sui` then failed to reproduce in 1,280 attempts.
4. `median 3 characters to 320` never existed anywhere. Invented in an image brief, carried through three.
5. `x07b`'s "21 of 21, x07 IS OVERTURNED" is a one-sided metric; a rod that says NO to everything scores
   100%. Two-sided: 0.733 against a 0.650 baseline. Real finding is the asymmetry — **P(YES|will fail)
   = 0.000**, P(YES|will pass) = 0.590. A YES is trustworthy, a NO is noise.
6. `x19` scored its detectors over `rec["raw"]`, the last 320 chars, where 74% of replies are longer.
   It erased `Rogans vacui` (1 ask where there were 9). `organism.run` now takes `keep_full`.
7. `x19`'s spread pooled conditions where the effect is impossible and compared top-to-second. Corrected:
   **`Rogans` is a fuel phenotype, 20% and 15% on two plants, 0% on two others, spread 0.20.**

**LOCKED**

- **BLACK GLASS** is World 1's visual system. Two candidates beaten and recorded so it is not re-run.
- **A state names a part.** Anything untested renders UNMEASURED, dark with visibly empty sockets.
- **A method frame CURES muteness** (28/288 bare to 0/360 fitted). The annex arrow
  `Clausus —(FRAME)→ Tacitus` was backwards and is corrected.
- **World 1 carries three parts**, GOAL / METHOD / MANNER, because `Obtemperans`'s whole receipt is a
  manner frame.

**NEXT**

**Build `CRITIC`, `LADDER` and `COUNCIL`.** They are three of World 2's seven components, none has ever
been assembled, and they carry the entire "prevention dominates repair" claim. Write the sealed opening
with its predictions before the calls, as Chapter III did. Then `Tardus erroris`, the only creature that
cannot be caught by reading. Read `design/W2_HANDOFF.md` first.

Also open: `Rogans vacui` is provisional at 3.9% until an ask detector runs that excludes leaked
reasoning; Chapter I and II need the `Speciosus` correction folded into their closing arguments.

---

## 2026-07-28 — HANDS AND SEATS: THE ENTITY TOUCHES SOMETHING OUTSIDE ITSELF

**DID**

- **`aea/kernel/hands.py`** — the tool layer, with permission enforced where the call happens. Four
  gates on `invoke()`: seat allowlist, zone, charter capability, implementation exists. Verified live:
  a rod was advertised `json_get`, told to use it, and **refused twice in the sensitive zone with zero
  bytes moved**. The tool list handed to the model is advertising; `invoke` decides.
- **`aea/kernel/seats.py`** — custom subagents. A seat is `capability + zone + MEASURED rod`; drop one
  and it is a persona. `seat()` refuses to construct rather than fail at dispatch. `dispatch()` is the
  first thing in the repo that calls `trust.check` **before** the work rather than recording after it.
- **TOOL-CALLING IS NOW MEASURED** — the sixth suite, and the first that grades a side effect instead
  of text. 28 rods probed: **8 of 16 hosted, 9 of 12 local**. Ground truth computed, never typed.
- **Two seats live.** `scout` (public, `gather_public`) returned llama.cpp's real open-issue count
  through the gate. `keeper` (sensitive, `reason_private_local`, local rod, no network) read the trust
  ledger and answered correctly about `produce_brief`.
- **`courier` deliberately attempted and REFUSED** — `send_email` under `send_outbound`, ceiling 0.
  The refusal is the artifact.
- **`trust.reset_streak()`** — Law IV enforced rather than quoted: a rod change under a capability
  clears the promotion streak and holds the level.
- All 31 frozen golden behaviours still hold.

**THREE DEFECTS FOUND IN MY OWN WORK WITHIN THE HOUR, ALL FIXED**

1. **The answer key was wrong.** The tool-call probe carried the expected product as a literal, wrong
   by six hundred. Every rod that answered *correctly* would have been scored a failure and the fuel
   table would have said tool-calling was impossible. Ground truth is now computed by the same
   deterministic function the tool uses. *An answer key written by the hand that wrote the question is
   not a key.*
2. **The privacy boundary tested a proxy.** Zones permitted plant `ollama` for private work because
   ollama is the local daemon. Ollama now proxies **hosted** models through that daemon, marked only by
   a name suffix — and `gpt-oss:120b-cloud` was the fastest passing rod, so the selector seated a 120b
   **cloud** model on the zone that reads this machine's private state. `unstick.is_local()` now tests
   the rod, fails closed. *Same shape as the invariant that tested for the word "zone".*
3. **The ledger was graded by the wrong event.** `hands.invoke` recorded trust on every tool call.
   Within one dispatch that **promoted `reason_private_local` to TRUSTED because two files opened** —
   and the next line of the same run is `FAIL -> WATCHED`, because the seat never produced an answer.
   Criterion contamination, live in the ledger. A tool call is a step, not an outcome; the ledger is
   now graded once per run, by the caller that knows whether the job succeeded. The contaminated
   history lines were **left in place** — editing the accountability trail would be worse than the bug.

**LOCKED**

- **A read tool is an outbound channel if the model writes the address.** `web_fetch` looks read-only;
  the URL is composed from context, so the request carries the data out. Network tools are
  PUBLIC-ONLY, structurally, not by policy.
- **A permission the model can talk past is a decoration.** The allowlist is re-checked at the call
  site, never only in the prompt.
- **A seat refuses to exist rather than degrade.** Unmeasured rod, wrong zone, ungradeable capability
  — all raise at construction.

**NEXT**

**THE DISCRIMINATOR.** One authority on what may be called, how often, and which rod fits this task.
It is not missing — it is **triplicated and unused**: `lab/pace.py` (live `x-ratelimit-*` headers, day
budget, feasibility), `grid.Meter.can_spend` (orchestrator/swarm), `energy/capacity.py`. `seats.pick_rod`
consults none of them; it sorts by measured latency and stops, which is how the fastest rod in the
table — which cannot call a tool at all, it emits a JSON blob as prose — would have been seated.

The data for a real one now exists: fleet grades `reach/format/arith/carry/code`, hands grades `tools`,
unstick owns the zone, pace owns the budget. A task states what it needs; the discriminator intersects
and returns a rod **or refuses**.

Still open from before: wire `unstick.propose` into the wake (Tier 0 step 3 proposes, nothing applies);
open alarms into the brief header; the liveness canary; `propose_ceiling`.

### SAME SESSION, LATER — THE DISCRIMINATOR, AND THE LOOP CLOSING ON A REAL FAILURE

**THE AUDIT.** Counted every system touching model budgets or selection: **21 systems, 6 independent
selectors** (`grid.Router.pick`, `orchestrator.pick`, `energy.ladder/draw`, `swarm.pick_varied`,
`seats.pick_rod`, `converse.RODS`), none calling another, ranking on **four different keys** —
cheapest-plant-first, lowest-latency, highest-score, and random-among-the-top-eight. Whichever file
you call decides the answer.

**Four live numeric conflicts**, worst first:
- **cerebras `rpd` declared UNLIMITED; the plant's own header says 2400/day.** The meter therefore
  guards nothing on that wall. Also 150/hour, unguarded.
- **groq `rpd=1000` plant-wide; `llama-3.1-8b-instant` publishes 14400/day.** And `rpd` is bucketed
  per PLANT while `rpm` is bucketed per `(plant, model)` — two granularities inside one `can_spend`.
- **nvidia in-flight enforced as 20 by the meter and 8 by the lab's own semaphore**, against ~25
  measured. The lab path never calls `can_spend` at all, so `grid_state.json` does not reflect lab runs.
- cerebras rpm 5 in `grid.py` vs 30 in `state/energy.json` (a file with **no writer in the repo**).

**BUILT**

- **`aea/lab/pace.py` now PERSISTS** to `state/pace_observed.json`. It is the only module that reads a
  plant's real limits from the plant, and it discarded every one at process exit. Merge-on-write under
  a file lock, plus an `atexit` flush — without the flush the 5s throttle silently ate every
  observation after the first, and the conflict report said UNOBSERVED while `pace.render()` had just
  printed the live number.
- **`aea/kernel/fit.py` — THE DISCRIMINATOR.** A `Need` states zone, suites, tools, exclusions; `fit()`
  returns survivors, `why_not()` returns every reject **with the gate it died at**, and nothing
  matching **raises** instead of returning a near-miss. `conflicts()` compares declared constants
  against observed headers and **reports, never overwrites** — it caught both groq and cerebras by
  running, not by reading 21 files.
- **`seats.pick_rod` now holds NO selection logic** — it delegates. It was the sixth selector; adding a
  seventh would have made the audit's finding worse.

**THE LOOP CLOSED ON A FAILURE NOBODY STAGED.** `gpt-oss:120b-cloud` passed the tool probe, then began
returning `finish_reason=stop` with empty content forty minutes later — a hosted quota exhausting as a
200 rather than a 429. What followed ran on its own: ledger demoted TRUSTED -> WATCHED -> DRAFT, **the
alarm fired at 3**, `impasse.read` returned STUCK with one repeated cause, `unstick.moves_for` proposed
`swap_rod` with measured justification, `fit.choose(exclude=...)` picked a working alternative, Law IV
reset the streak on the rod change, and the seat recovered with a real answer from a real API.

**FOUR MORE DEFECTS, ALL IN CODE WRITTEN THIS SESSION**

1. **`hands.run` reported an empty reply as `ok: True`.** An empty answer is not a successful run, and
   the cause reached the ledger with nothing attached. It now separates *budget spent reasoning*
   (`finish_reason=length` with reasoning present — which is `unstick`'s own `raise_budget` move) from
   *returned nothing*. Default budget raised 500 -> 900 for the same reason.
2. **`dispatch` recorded the culprit and not the cause.** The note said `seat:X rod:Y` and stopped, so
   three identical failures had no reason attached: the diagnosis worked and the treatment could not,
   because a move is chosen by reading the SHAPE of the failure. This is Explicit Loss Notification —
   the layer that observes the loss must say what kind it was.
3. **A measurement can go stale and every gate reads a measurement.** `fit` kept selecting the broken
   rod because the probe said it passed. `Need.exclude` is where the live knowledge — held by the
   ledger and the impasse loop — re-enters selection.
4. **THE EIGHTEEN-DAY DEADLOCK, REBUILT AND CAUGHT THE SAME HOUR.** The tool gate required WATCHED for
   *every* tool. So a capability that failed three times demoted to DRAFT and could then no longer make
   a **read-only** call — meaning it could never produce the clean run that would promote it back.
   Pinned forever, with a working rod available and a correct diagnosis in hand. The charter already
   drew the line and the gate ignored it: **DRAFT means "may produce"**, and a read that changes nothing
   outside this machine is producing. The requirement now follows the tool's `outbound` flag. Nothing
   outbound got easier — `send_email` and `spend` are refused at every level, with no implementation.

**LOCKED**

- **Reading is not acting.** Gate a read at DRAFT, an outbound act at WATCHED. Conflating them
  manufactures a deadlock that looks exactly like a permission working correctly.
- **A selector must be able to refuse**, and must name the gate each reject died at.
- **Declared limits and observed limits are reported side by side, never merged.** A header is one
  moment; a constant carries a dated provenance note. Resolving them is a human decision.

**NEXT**

**Wire `unstick.propose` into the wake.** Every piece now exists and was demonstrated end to end — but
the swap was executed by hand in a script, not by the loop. That is the last gap in Tier 0.

Then: migrate the remaining five selectors onto `fit` (they still disagree); resolve the four limit
conflicts by hand now that they are detected automatically; re-probe tool-calling on a schedule, since
this session proved a rod's capability measurement expires.

### SAME SESSION — FUEL CAPACITY IS NOT A NUMBER

Luis: *"groq have min quotas on tokens for different models at different paces, nvidia you have
requests per min with no apparent limit more than the context window of the model — each has a
different fuel capacity."* Correct, and the consequence is that **the schema was wrong**, not just
the values.

`grid.PLANTS` gives every plant the same three columns (`rpm`/`rpd`/`tpd`) and fills gaps with `None`
meaning unlimited. It has no way to distinguish *"this plant is not limited on this axis"* from
*"nobody has looked"* — which is exactly why cerebras read DECLARED UNLIMITED against a real
2400/day wall. The plants do not share a shape:

| plant | binds on | scope |
|---|---|---|
| nvidia | requests/min; no token period cap. Per-call ceiling is the CONTEXT WINDOW | per model |
| groq | tokens/min AND requests/day, **different numbers per model** | per model |
| cerebras | req/min 5, /hour 150, /day 2400, plus 30000 tok/min — four walls | per plant, org |
| ollama | no period limit; binds on CONCURRENCY (one resident model) and WALL CLOCK | per machine |

**BUILT — `fit.capacity(rod)` and `fit.binds(rod, calls, tokens_each)`**

- Every wall carries **unit, SCOPE, and SOURCE**. Unknown is `source="unknown"` and never silently
  unlimited.
- **SCOPE is the field nothing in this repo had**, and its absence is a live bug: `Meter._roll`
  buckets `rpd` per PLANT while `_win` buckets `rpm` per `(plant, model)` inside the same
  `can_spend`. So groq's per-model 14400/day is charged against a shared 1000.
- `Need` now carries the **shape of the job** (`calls`, `tokens_each`), and capacity is the last gate:
  everything above it asks *is this rod capable*, this asks *can this fuel deliver a job of this
  shape before a wall stops it*.

**`pace.observe` now keys per ROD as well as per plant.** It keyed by plant alone, and groq breaks
that: `llama-3.1-8b-instant` publishes 14400/day + 6000 tok/min while `llama-3.3-70b-versatile` on the
same plant publishes 1000/day + 12000 tok/min. Collapsed to one record, the last model to answer
overwrote the rest and every reader got a confident number **belonging to a different model**. Both
buckets are kept, because cerebras genuinely is org-scoped; `fit.SCOPES` says which to trust, and a
per-plant number read where the plant scopes per-model now carries an explicit `warn`.

**THE MEASUREMENT THAT SETTLES IT.** Same five rods, three job shapes, and the binding wall moves:

```
1 call x 550 tok        every rod ok
3000 calls x 550 tok    nvidia 1.25h (requests/min) · groq-8b 4.58h (tokens/min)
                        groq-70b REFUSED (1000/day) · cerebras REFUSED (2400/day)
                        ollama REFUSED (286h, serialised)
40 calls x 12000 tok    cerebras 0.27h · groq-70b 0.67h · groq-8b 1.33h · ollama REFUSED (83h)
```

**The reversal is the proof:** groq-8b beats groq-70b on many-small and LOSES to it on few-large,
because 6000 vs 12000 tok/min inverts against 14400 vs 1000 per day. **No single scalar ranking can
produce that** — which is precisely why six selectors each ranking on one number were all wrong, and
why cerebras (the fastest fuel here at ~2000 tok/s) is unusable for anything that is many small calls.

**LOCKED**

- **Capacity is multi-axis, per-rod, and scoped.** A limit without a scope is another model's number.
- **Unknown is not unlimited.** Every wall reports its source; absence is an admission.
- **Rank on deliverability for the job's shape, never on speed.** Fastest fuel and usable fuel are
  different questions.

31 frozen behaviours still hold; harness/fuels/hands all pass the model through to `pace.observe`.

### SAME SESSION — THE DEEP REVIEW: 35 PROPOSED, 11 REFUTED, 24 CONFIRMED

Seven independent reviewers, one per failure class, each adversarially refuted by a second pass told
to default to `real=false` when uncertain. Survival by dimension: metrics 5/5, wake 5/5, selection
5/5, failopen 4/5, state 4/5, deadlock 2/5, privacy 2/5. Deduped, 24 confirmed are 20 distinct.

**THE HEADLINE, AND IT IS ARCHITECTURAL:** `grep` finds **zero references to impasse, unstick or
crystal anywhere under `aea/loop/` or `aea/organs/`.** The whole notice-stuck / get-unstuck kernel is
CLI-only. Worse, `loop/live.py:93` returns `AWAKE:brief` on every tick until the brief succeeds, and
`tick()` advances `last_brief_date` only on success — so a failing brief **starves consolidate and
reflect for the entire outage** while re-running the byte-identical action. `state/trust_ledger.json`
is the receipt: twelve entries on 2026-07-21 at half-hour spacing, all identical. That is the
eighteen-day incident, still present at the loop level.

**FIXED THIS PASS**

| # | defect | file |
|---|---|---|
| 1 | **`state/chains.jsonl` recorded private-zone goals VERBATIM and was tracked by git**, absent from .gitignore | `server/controlroom.py:33` |
| 2 | **`load_json` treated UNREADABLE as CORRUPT** — a Windows sharing violation renamed a VALID store away and returned the permissive default. For the ledger that default rebuilds every capability at charter level. `state/bench_runs.json.corrupt.<ts>` is tracked: it already fired | `kernel/grid.py:73` |
| 3 | **`trust.check` never applied the CHARTER ceiling** — lowering a ceiling could not revoke anything | `kernel/trust.py:68` |
| 4 | **`orchestrator.pick` returned `cands[0]` after every candidate failed `can_spend`** — the meter consulted, logged, then overruled | `mind/orchestrator.py:90` |
| 5 | **`"(grid busy)"` passed the completeness check and graded a CLEAN RUN** — the entity earned promotion for briefs it had not written | `organs/brief.py:167` |
| 6 | **`speak` gated at WATCHED while being the only writer of its own ledger** — one local audio fault mutes it permanently | `organs/talk.py:137` |
| 7 | `build_graph` and `export_city` **rewrote tracked repo files at IMPORT**, no `__main__` guard; `export_city` wrote to a RELATIVE path | `tooling/` |
| 8 | **four experiment modules could not import at all** (`x16` lost `ascending`/`deprived`/`oblique`; x17/x19/x20 import it) — x19's findings are cited as evidence and could not be re-run | `lab/organism.py` |
| 9 | **`deprived()` returns an empty list by construction** — x16 would report an empty toxic family as "nothing toxic" rather than "nothing tested" | `lab/organism.py` |

On the privacy one: the fourteen rows on disk were **benign** — zero emails, paths, calendar
references or identifiers. Nothing leaked. The exposure was STRUCTURAL, and it now has two
independent guards: the writer redacts free text for private/sensitive zones, and the file is
gitignored and untracked.

`load_json` now has three outcomes because there are three situations: **absent -> default;
unparseable -> quarantine + default; unreadable -> retry, then RAISE.** A caller must never proceed
on a default standing in for a file that exists. Verified: a locked file raises and **survives**.

**CONFIRMED AND STILL OPEN, RANKED**

1. **Wire `impasse`/`unstick` into the wake, and stop a failing brief starving the loop.** Two lines
   in `tick()` plus a `brief_fails` counter. This is the one that makes the rest matter.
2. **A timed-out or crashed wake records NOTHING**, so the consecutive-failure alarm can never fire
   for the failure mode most likely to kill it (`loop/live.py:69`).
3. **The heartbeat write sits OUTSIDE the never-die guard** — one failed save kills the forever-loop
   (`loop/live.py:171`).
4. **The brief presents a month-stale private file as "Today"** — a live honesty-law violation in the
   one unattended artifact (`organs/brief.py:25`). Flagged earlier this session, still unfixed.
5. **HADES's own outage is recorded as the worker's failure** — `hades=unverified` demotes
   `produce_brief` (`organs/brief.py:166`). The verifier being down is not the worker being wrong.
6. **`gather_public` is graded on a substring of the model's prose**, not on whether the fetch
   happened (`organs/brief.py:168`).
7. **`seats.dispatch` grades "the model emitted non-empty text" as a clean run** and discards the
   tool trace that would show whether anything was actually touched (`kernel/seats.py:184`) — my own
   code, same class as the defect I fixed in `hands.invoke` this morning.
8. **The brief never calls `trust.check`** — the permission ladder gates nothing it does.
9. **The word "private" names two different plant sets** — the live selectors let it reach hosted
   plants (`energy/energy.py:98`); the private-section audit tests the PLANT NAME, so a hosted rod
   would be certified LOCAL-ONLY (`organs/brief.py:127`). Defect 3's shape, twice more.
10. **The sacred save can be wiped with no backup and a failed write is reported to the UI as
    success** (`server/controlroom.py:563`).
11. `Meter._inflight` is process-local while presented as the rod's global concurrency.
12. Law IV is enforced on the seats path but not on the wake job.

31 golden behaviours hold; 86 modules import clean; the ledger loads; the sacred save is intact.

### SAME SESSION — XRAY: THE SYSTEM READS ITSELF, AND THE NUMBER IS 13 OF 104

Luis asked for a dashboard, said he did not want to spend weeks on one, and named what he actually
wants: to see the code, the connections, the dependencies. Built as a DERIVED artifact, not a
hand-drawn one, in one pass.

**`aea/tooling/xray.py`** — parses every module with `ast` and **never imports** them. That is a
correctness choice, not a performance one, and it was learned the same day: `build_graph` and
`export_city` rewrote tracked repo files merely on being imported. An analyser that imports the code
it studies runs the code it studies. Produces `state/xray.json`: internal import graph, reachability
from declared entry points, orphans, import-time side effects, which module writes which store, plus
live ledger/seat/goal/alarm state.

**`aea/tooling/xray_view.py`** — renders it to `web/xray.html`. The visual law is the project's own
(`E2`/`E8`): void field plus structure grey, amber reserved for the FIRED state only. It maps onto
this data exactly — **reachable from a wake = lit, everything else = structure** — so the picture
makes the finding before a number is read. Screenshot-verified twice; the first render collided two
columns in the 300px rail and those panels now stack.

**THE READING**

```
104 modules   21,679 lines
 13 modules    2,287 lines   reachable from an unattended wake
 84 modules   17,511 lines   reachable from NO entry point
  7 of those are aea.kernel  crystal fit goals hands impasse seats unstick  (2,023 lines)
```

**The entity is 13 modules.** Everything built today to make it autonomous — 2,023 lines, almost as
much as the entire running system — is orphaned. `io.agent_tools` and all four `gameapi` modules too.
This is the same finding the deep review reached by reading, now reproducible in under a second.

Also surfaced without being asked: six modules act at import; three stores have two writers
(`capability_census.json` has three).

**GUIDANCE GIVEN, and it is the part that matters more than the tool**

- **JSON holding Python code is refused.** It is `eval()` with extra steps and it hands the entity
  the capability the charter pins at `self_modify_code=1`. The correct shape is the one `unstick`
  already uses without anyone naming it: `{"move": "swap_rod", "knob": "fuel", "to": X}` — a NAMED
  operation from a declared registry, with parameters. The JSON says WHICH and WITH WHAT, never HOW.
  It is also the only version where rollback means anything, because two declarations can be diffed.
- **OOP vs protocols: mostly neither.** The repo's idiom — module functions, plain dicts, JSON state
  — is correct and should not be converted. Classes only for real state; `typing.Protocol` only for
  real polymorphism. The flexible layer must be DATA, not a class hierarchy. Inheritance is the least
  flexible construct in Python; a registry of named operations is the most.
- **The dashboard is not a side quest.** `THE_ELEMENTS.md` Tier 2 already lists "WHAT AM I MADE OF
  RIGHT NOW" as unanswerable. `state/xray.json` is that organ; `web/xray.html` is its human face.
  Self-modification cannot exist without it — a proposal has to be diffed against a machine-readable
  description of the current self.

**NEXT** — unchanged and now visible in one number: **wire the seven orphaned kernel modules into
the wake.** The dashboard's whole left rail is a list of work not done.

Deliberately NOT built: live per-line execution tracing. Weeks of work, answers a question nobody
asked; static reachability plus live state answers the real one.

### SAME SESSION — SHADOW, SELFCHECK, HEAL: THE SELF-IMPROVEMENT SPINE

**`aea/kernel/shadow.py`** — the entity tests a change to itself without becoming it.
`git worktree` gives a full isolated checkout in ~1s without duplicating a blob, and the store is
already content-addressed and diffable, so **the previous self is not something to store — it is a
commit.** Two rules make it safe rather than suicidal:

1. **A proposal may not author the test that judges it.** `PROTECTED` covers the frozen tests, the
   ledger, and this file; editing one is an instant rejection. Verified: a proposal that rewrote
   `test_golden.py` was REFUSED.
2. **Rollback targets the last PROVEN version.** Known-good is a status a commit EARNS by passing
   the gate. `mark_known_good` refuses on a dirty tree.

**There is deliberately no `promote()`.** `self_modify_code` is ceiling 1 — a reviewable diff. The
gap between "the tests passed" and "this is now what I am" is where a human belongs.

**Three defects in it within minutes, all found by running a CONTROL:**
- The shadow tested `HEAD` while the running self was the working tree — and `mark_known_good`
  stamped the working tree's verdict onto HEAD's hash. A verdict attached to the wrong tree is not
  weaker, it is false.
- `dirty()` used `git diff`, which lists modified TRACKED files — so all nine modules written today
  and not yet committed were invisible, and the shadow was built without them.
- Shadows live under `state/`, so the copier tried to copy a shadow into a shadow. Now `state/` is
  never carried: it is also the ledger, and a candidate must not inherit the running self's record.

**`aea/tooling/selfcheck.py`** — every whole-system invariant in one command, built because the same
verifications had been retyped by hand nine or ten times this session. *A check that lives in a file
runs every time; a check that lives in a habit runs when someone remembers.* Checks: structure, state
intact, no private data, **no absolute paths**, every module imports, 31 frozen behaviours.

**`aea/tooling/heal.py`** — improvement candidates, deterministic, never applied. The line that
matters: an INVARIANT violated means broken and blocks; a CANDIDATE means nothing is broken and it
could be better. **Detection is mechanical precisely so that zero candidates is a real answer** — a
model asked to find improvements always finds some. Five detectors, each earning its place from a
defect this repo actually paid for. Current: 4 near-duplicates, 11 disagreeing constants, 52
swallowed errors, 55 god-modules.

**Both detectors were wrong on first run and fixed:** the literal detector reported "the literal 3
appears in 63 files" (true, meaningless) and now finds only NAMED settings holding MORE THAN ONE
VALUE — which is exactly what four disagreeing rate limits looked like. The path detector matched the
`s:` in `https://` and turned 6 real hits into 61 files of noise.

**PATHS ARE NOW ANCHORED.** `grid.HOME` and `grid.external(env_key, ...)` resolve everything outside
the repo from a declared `.env` key or `~`, and return **None** rather than inventing a path — a
fabricated corpus path would mine an empty directory and report success over nothing. Six literals
removed from `consolidate.py`, `index_codex.py`, `memory.py`. Enforced permanently by
`selfcheck.check_paths`.

**LOCKED**

- **The center of control is not a controller.** Actions declare their own preconditions and effects;
  selection is a QUERY over declarations, not a decision by a coordinator that must know them all.
  That is STRIPS/PDDL (1971) and this repo already converged on it three times independently
  (`hands.TOOLS`, `crystal.applicable` by situation, `fit.Need`). What is missing from all three is
  preconditions/effects.
- **The absence of a match is the self-improvement trigger.** "No action's preconditions are
  satisfiable from this state" is a machine-readable specification of exactly what is missing.
- **A declaration is a claim.** If the entity authors its own preconditions it can lie, so effects
  must be verified after the fact — the trust ledger applied to actions.

**NEXT** — unchanged: wire the seven orphaned kernel modules into the wake. Then preconditions and
effects on the action registry.

### SAME SESSION — THE COMMAND CENTRE, AND THE FIRST KNOWN-GOOD VERSION

**COMMITTED.** `83c10ae` (194 files, privacy-scanned clean) then `7bb6e01`, which is the **first
known-good version this system has ever had** — a commit that EARNED the status by passing four
checks it cannot author. Before today there was no version to return to.

**THE BOARD**, `web/board.html`, served by the existing control room. A shell rather than a page:
persistent rail and periphery, three permanent answers at the top, working surface in the middle.
Every panel derives from state on disk. Views: status, open loops (three verdict columns), the 43
laws as parsed cards, proposals with gate pips, the living import graph, curated endpoints.

**THE ENDPOINT RAIL IS CURATED, NOT DUMPED.** Generating it from the server's route table was right
for recognition-over-recall and wrong for judgment: it listed every game-era route on a page about
the entity, making the reader do the triage the tool exists to do. Eight KEEP entries each carry a
reason; the 22 that belong to THE PROBE are counted and named, never silently hidden. Same discipline
as OPEN_LOOPS: an item with no verdict does not appear.

**WHAT THE DESIGN RESEARCH FOUND, all measured rather than asserted:**

- **IBM Plex Mono had never loaded.** No `@font-face`, no font files, not installed. Every screenshot
  all session was Consolas. The most identity-carrying asset in the design was absent.
- Ink coverage **2.5%**, with **45% of the work column dead**, while ~20 of 27 cards clipped mid-word.
  Content was being thrown away into empty space.
- Amber was **22-31% of all ink across 81 elements**. Our own law says sparse and earned; amber had
  become the default state.
- The **failing** invariant rendered at 3.18:1 against passing ones at 10.40:1 — the alarm was
  quieter than the all-clear. NASA's rule is the exact inverse.
- Seven `font-weight` declarations, **all 400**, in a design whose own E8 law states weight carries
  hierarchy and colour never does.
- Surface steps of dL* 1.40 / 1.31 / 2.03 are **below the just-noticeable difference**: three of five
  surfaces were literally indistinguishable. That arithmetic IS the flatness.
- Twelve font sizes at adjacent ratios of 1.04-1.09 (a step needs ~1.15 to read as a level), and
  twenty-one distinct spacing values sharing no denominator.
- The graph's package anchor was 0.020 against an edge spring of 0.030, so anchors lost to 140
  cross-package edges. Simulated fix (anchor .060, spring .012, exclude the universal hub) takes
  package separation from **0.91 to 2.12**.
- Labels were gated at `zoom > 1.7` on a page that opens at `zoom = 1`: the graph was 108 anonymous
  dots. The canvas also never stopped repainting a static image.
- `font-variant-numeric: tabular-nums` is a **no-op on this entire stack** — neither Plex face ships
  the feature. Numbers are stable because the advance is fixed, not because of the CSS.

**FIXED:** the font, the surface ladder, three weights, five sizes with a focal number, flat card
fills with real padding and a visible radius, the semantic inversion (fail is now the loudest mark),
amber spent like money, every truncation at its SOURCE rather than in CSS, the light source over the
work column, the graph constants, the label ramp, and the canvas halting when static.

**`design/E12_BOARD_SPEC.md`** — 75k characters from an 8-specialist workflow, every value resolved,
no ranges. Token block, component specs with states, motion table, atmosphere and graph code, a
concrete answer for every region of a 1700x1000 screen, the psychology rationale, and twelve changes
ordered by visual return per line. **This is the artefact that makes the rest finishable without me.**

**STILL OPEN:** the spec's sections 4 (grain, vignette, depth cueing) and 6 (the full 12-column
layout) are unimplemented. The lower band fills the dead space but is not yet the composition the
spec describes.

**NEXT:** `diary/OPEN_LOOPS.md` FINISH items 4 and 5 are done; the board now needs the spec applied
in order. The entity itself needs `hands`, `seats`, `fit`, `goals`, `crystal` and `shadow` wired into
the wake the way `impasse` and `unstick` now are — 88 of 110 modules still cannot be reached.

---

## 2026-07-28/29 · THE INSTRUMENTS WERE WRONG MORE OFTEN THAN THE MODELS

**The session in one line:** we set out to learn what every rod can actually do, and found that
almost every number this project holds about rods was taken through a broken instrument or the wrong
parameters. Ten instrument defects, against almost no model behaving unexpectedly.

### DID

**The privacy guard was dead and nobody could see it.** `selfcheck` reported `[FAIL] no private data`
on every run, from 18 emoji in design docs whose cleanup is a deliberate KILL. A permanently red line
cannot signal. Behind it, the `absolute windows path` pattern was `r"[A-Za-z]:\\Users"`, which
matches only a JSON-escaped path: **1 of 5 real forms**, blind since it was written. Corrected, it
immediately found a live leak in `design/A16_WIRTHFORGE.md`, now redacted. Privacy and house style
are two rows; the second is advisory so a style violation can never mask an invariant again.

**Thinking is controllable, and the switch is per family.** `mind/fuel.py` had it pinned as untamed
("never true until an API parameter is found") because the earlier test used the wrong string.
Measured, 67 calls, same answer in every cell that returned:
- Llama-Nemotron (`super-49b-v1.5`, `nano-9b-v2`): system `/no_think` -> **0 chars, 2-5 tokens, 0.4s**
  against a default of 3024 chars / 991 tokens / 71s.
- Nemotron 3 (`nano-30b`, `super-120b`): `chat_template_kwargs {enable_thinking: false}` -> 0 chars.
  `/no_think` is ignored here. The two switches DO NOT cross over.
- gpt-oss: `reasoning_effort` low/med/high -> 20/66/249 chars, monotonic.
- Ollama: native `/api/chat {think:false}` -> 0 chars vs 691 tokens. **The OpenAI-compat base at
  :11434/v1 cannot reach it**, and that is the base `PLANTS` uses.
- `nvext.max_thinking_tokens` and `reasoning_budget` are documented and IGNORED on the hosted
  endpoint; minimax and glm reject the latter with 400. NVIDIA's own example targets localhost:8000.
- Sending the wrong switch is not free: `mistral-medium-3.5` returns 400 for any
  `chat_template_kwargs`. Hence `grid.think_off()` matches on family or sends nothing.

**Every measurement in this repo was taken at the wrong temperature.** Lifted from each model's own
build.nvidia.com Python example: owners publish **temperature 0.2-1.0, top_p 0.7-1.0, max_tokens
1024-20480**. `call_openai` sent 0.2 / 256 to all of them and never sent top_p. Worst case,
`nemotron-3-nano-omni` asks for 20480 and got 256; a reasoning rod on too small a budget spends it
thinking and returns nothing, which is the empty-reply failure already in `unstick.py`. Now
`grid.OWN_PARAMS` + `own_params()`, and `energy.draw()` defaults to the rod's published values with
any explicit caller argument still winning.

**A generic probe is not a measurement.** One chat-completions body sent at 102 models across 9
kinds declared 16 alive models dead. Per-kind battery with external graders recovered them:
- **embed (6 pass)**: query + 4 passages, cosine must rank the true one first. `nemotron-3-embed-1b`
  2048 dims, margin 0.528, 0.6s. All six had been reported 404.
- **vision (4 pass)**: an invoice PNG generated here, so ground truth is exact. `llama-3.2-90b-vision`
  and `nemotron-nano-12b-v2-vl` read `84731 4471` exactly.
- **translate (2 pass)**, **code (1 pass, executed against 5 unseen cases)**.

**Structured output: 9 of 9 candidates pass `json_schema`, every one strict-parseable.** Never
tested here before. `json_object` produced the only malformed output in the run. Always send the
schema.

**The independent inspector works, and the 61% figure does not apply to it.** `overseer.py` records
61% for a rod marking its OWN answer. A SEPARATE inspector, on 3 semantic violations no regex can
catch: **13 of 13 caught, pooled across every inspector that answered. The free regex: 0 of 3.**
The architecture is the combination: deterministic checks first (4/4 mechanical, 0 false positives),
model only on what survives. `nemotron-nano-9b-v2`: 9/10, 3/3 semantic, **0 false rejects** - the
error direction that turns a retry loop infinite. `deepseek-v4-pro` and `glm-5.2` each rejected a
clean output.

**Conversation is a client-side construct and the models hold it.** Six turns, a tool call in the
middle, three deterministic checks. **7 of 7 held a rule set in turn 1 when turn 6 openly invited
them to break it.** All 7 called the tool and carried its result forward. **3 of 7 lost a fact from
turn 1 by turn 5**, including `nemotron-3-super-120b`. A full six-turn conversation costs **404
prompt tokens** - 0.04% of a 1M window, so `converse.py`'s `KEEP_TURNS=12` throws away context we
have 2500x more of than we use.

**`aea/energy/rodprobe.py`** - one harness (metered transport, three-field reply parse, per-rod
params, concurrent sweep) and one store, `state/rods.json`, 102 rods folded from six scattered files
holding 148KB nothing read. `grid.own_params` reads it, `energy.draw` imports it: **wake-reachable
went 15 -> 16, the first module connected in a long time.**

**The codebase audit, all four items:**
1. `xray` now derives the doors a human opens (tooling modules, numbered experiments) instead of
   counting only wake+server. **"88 orphaned" was three unrelated facts; the real defect is 31
   modules / 6190 lines.** Roles: live 23, tool 10, evidence 43, paused 4, unwired 31.
2. **Import-time side effects 6 -> 0.** Five were `str.replace` matched as `os.replace`; the detector
   now requires a qualified receiver. The one real violation was `grid` doing `os.makedirs` at
   import, so merely naming the kernel touched disk. Moved to write time. Law S3 holds.
3. `aea/lab` top level 51 files -> **14 library + 27 experiments** in `experiments/`, git mv, seven
   cross-imports rewritten, all 111 modules still import.
4. The one real store collision (`capability_census.json`, written by both censuses) is now
   attributable (`source`, `promoted_at`) and **refuses a shrink** without `--force`. Proven both ways.

### LOCKED

- **A rod is called with ITS OWN published parameters.** House defaults are the fallback, never the
  default, and the difference is recorded rather than hidden.
- **The orphan count is by ROLE.** live / tool / evidence / paused / unwired. Only `unwired` is a defect.
- **Deterministic check first, model inspector second.** Measured 10/10 combined against 7/10 regex
  alone and 9/10 model alone. A model overseer is never the thing that decides.
- **Never combine a no-think prompt with `tools`** until that is re-tested; one run corrupted the
  tool expression while the tool was called, which passes a "did it call" check and returns a wrong
  number.

### NEXT

1. **Wire `hands`** into the wake (tools + network, 538 lines, orphaned). Everything the entity
   cannot do today is behind that one seam.
2. **Calibrate the real rate ceiling.** `max_inflight=20` comes from a 2026-07-25 measurement that
   does not reproduce: 30 concurrent on one rod still yields 15-17 429s, some after waiting 61s for
   a legitimately free slot. `try_enter` closed a real check-then-act race in the Meter and was not
   sufficient. Ramp 1/2/4/8/16 and store the answer per plant instead of a constant.
3. **Re-read the 59 unread model cards across six rotated readers.** The delegation design is sound -
   one page my regex could not read was read by a rod and confirmed by a 200 - and I destroyed the run
   by putting 8 sustained workers on a single reader.

---

## 2026-07-29 (evening) - THE VOICE, MEASURED AND REPAIRED

### DID

Ran the first live session with **both sides of the boundary recorded** - his audio beside the
transcript (the black box, his Gargantua idea). 35 turns. Then fixed every defect it exposed and
built the instrument that lets the next one be found without him in the room.

**The five faults, all found by measurement, none visible in the code:**

| | measured | after |
|---|---|---|
| fabricated tool calls | 1 real call in 35 turns; receipts invented and spoken aloud | real receipt, `TOOL calc(415 * 987) -> 409605` -> "409605" |
| dead air before thinking | 23/35 turns hit the 9s cap, median 4.1s of empty room | dead tail **0.32s** median, worst 1.97s |
| reply length | every reply exactly 2 sentences; a story stored 43 chars | **1,076 chars**, 5 chunks, 85s of speech |
| the vocative tic | 30 of 32 replies opened "Luis, <exclamation>!" | stripped at the decoder, with a finite-verb guard |
| false self-description | "cloud-based, cannot access your machine" while holding `read_state` | states both halves: remote rod + local program |

**Built:** `aea/lab/earbench.py` - three modes, and **loopback plays known speech through the
speakers and captures it through the real microphone through the real `capture()`**. The ear and
the endpointer can now be tested at any hour with nobody present. It reproduced the historical
"what are your laws" -> "Where you lost" failure unattended on its first run.

**Added:** `doubt()` - confidence from decode INSTABILITY, since sherpa returns no logprobs
(verified against the installed signature). The semantic endpoint already decodes the growing
buffer several times a turn; where whisper is sure each decode extends the last, where it is
guessing it rewrites what it had committed. Above `DOUBT_ASK` the machine now ASKS instead of
answering a sentence nobody said.

**Research:** 60 agents on conversation theory, every cited claim handed to an independent refuter.
`diary/RESEARCH_CONVERSATION.md` - ranked changes R0-R13, a numbers table tagged
DOC/LOCAL/INF/VENDOR, and seven things this CPU-only machine cannot do, named once. It read the
live tree and caught a defect I had missed twice: a system-prompt paragraph teaching the model to
read prosody notes that had not been sent for hours.

**Verified:** battery **282/283** (was 174 cases, now 283 - `honesty` 89, `doubt` 14, `budget` 6 are
new), selfcheck **ALL INVARIANTS HOLD**, loopback median WER 0%.

### LOCKED

- **Arithmetic is computed, never delegated.** Whether 415 x 987 needs a calculator is not a
  judgement call. Extract by regex, compute, inject as fact - the prefetch rule was always drawn on
  COST, and local-and-free covered this from the start.
- **The doubt signal is decode instability**, not a model confidence number. There isn't one.
- **`earbench --loopback` is the ear's regression test.** No ear change ships without it.
- **Emotion labels stay refused**, prosody stays out of the prompt, and now so does every sentence
  that merely mentions it.

### NEXT

1. **R0 - the FTO ledger.** Measure the gap the LISTENER hears: last user speech frame -> first
   sample played, seven marks, one JSONL row a turn. Every stage is timed separately today, which is
   exactly how 4.1s of dead room hid between a 0.3s ear and a 0.5s mouth.
2. **R2 - arm barge-in.** The whole mechanism exists and nothing sets the stop event. Needs the
   self-echo gate FIRST: 60s of the machine talking to itself with the mic open, zero self-triggers,
   before the interrupt is enabled at all.
3. **R3 - the filler as a delay signal.** Gate at 700ms predicted wait, two-key selection, a
   prolongation ladder capped at 2, and a `promise_kept` metric that disables fillers below 0.9.
   This is Luis's "it sounds like one bit".
4. **The render mystery is still open.** 0.54s on the bench, 1.5-6.0s live. Five hypotheses dead
   with controls (whisper load, worker thread, open InputStream, 100Hz poll, during playback). Next
   step is timing INSIDE the live process, not another bench. Do not guess it.
5. **Two ear failures survive** at good SNR with a clean voice - "what are your laws", "what are you
   not able to do". First real evidence pointing at the recogniser rather than the signal. Test
   whisper-small against `earbench --loopback` before buying it; the harness makes that a 20-minute
   question now instead of a download and a hope.
