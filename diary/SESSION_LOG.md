# THE PROBE — SESSION LOG

One entry per work session. **Read the latest entry before starting.** The next session builds
from the `NEXT` block — it does not re-decide what is under `LOCKED`.

---

## 2026-07-22 (later·9) — FIRST LIGHT green, then R37/R39: the city ripped out, the world is the INSTRUMENT

**DID — first light (committed `35c0afd`):** the honest seam `aea/gameapi/` (firewall + read/act) over the
REAL organs: `/game/state`=controlroom.state, `/game/ignite`=bench_core.start_run, `/game/run`=run_status,
mounted into the :7799 control room (same origin, no new port). Client: `core/api.js` (the only server-talker)
+ `bench.js`'s three fetches repointed to `/game/*`. Verified GREEN in-client: compose BRAIN+SCORER -> ignite
-> PASS on ollama/qwen2.5:7b, driven with real keystrokes via CDP. Bugs the verb surfaced + fixed: modules.json
file-paths went stale in the subpackage reorg (the forge-gate refused every part -> `bench_core` now resolves
against the aea/ package dir, 25 paths remapped); the client sent `T-01`!=`t-01`; `normalizeRun` read a
`verdict` the seam never emits (mapped to run_status's real shape: link.state from ok, verdict from pass);
LOCAL_FLOOR `granite4.1:3b` (not installed) -> `qwen2.5:7b` (the one local model that reliably returns
PROBE ONLINE — CPU-only here, the rest hallucinate or return empty).

**DID — R39/R37 world (uncommitted):** ripped the CITY out of `engine.js` (`buildWorld`: foundry buildings,
socket tower, slab, roads — deleted with its helpers). Built THE INSTRUMENT: an amber core, concentric
PRIVACY-ZONE rings (radius=zone, from grid.ZONES: sensitive->private->public), the AEA organ-nodes on their
ring at dependency-depth altitude — LIT amber where really wired (BRAIN/GOVERNOR/MEMORY/LOOP, from live state
signals), cold-blue FOG-wireframe where not (SENSES/HANDS) — and conduits along the real couplings.
Data-driven from a new seam endpoint `/game/schema` (the fog can't lie: `wired` is a live check that flips as
organs get built). Composer relabeled tap->BRAIN, energy->POWER (R39 vocabulary). Verified on a swiftshader
shot: reads as the FIELD_GUIDE cover (the being as a concentric place), not a city.

**NEXT — finish the world slice:** conduit particles (one per real /events draw, count-true, zero decorative);
the fly-to-BRAIN -> dock -> ignite loop (v2 never wired flight-proximity `S.near`); capacity-fill + node labels.
Owed: D13 (the reorg-registry lesson); the `POWER` word disambiguation (header reserve vs brain sources).

---

## 2026-07-22 (later·8) — aea/ SUBFOLDERED: flat 34-file package -> 10 domain subpackages (DONE, verified)

**DID:** dissolved the flat `aea/` package (34 `.py` at one level, bare `import grid` co-location — the
thing Luis hated) into **10 domain subpackages**: `kernel`(grid,pulse,trust,tracelog) · `mind`(orchestrator,
swarm,hades,pathfinder,relay) · `energy`(energy,capacity,+censuses,model_fitness,probe,gauntlet) ·
`memory`(consolidate,index_codex,memory) · `bench`(bench_core) · `io`(speak,listen,agent_tools,notify) ·
`organs`(autonomy,brief,talk,telegram_bridge,reflect) · `loop`(aea,live) · `server`(controlroom) ·
`tooling`(export_city,build_graph). Strict inward-only DAG, no cycles.

**HOW (safe surgery, not a hand-move):** a 5-agent sweep mapped all 45 internal imports + every
move-breaking pattern (zero dynamic imports; traps = mixed stdlib+internal lines, a docstring
`from energy import draw`, bare-filename subprocess spawns). An **AST-guided migration script** then moved
files + rewrote all 45 imports (`import grid` -> `from aea.kernel import grid`) — splitting mixed lines,
leaving docstrings untouched. Non-import fixes: root shim + `controlroom._do` + `live.py` spawns now use
`python -m aea.<pkg>.<mod>` at cwd=repo-root; `build_graph.py` recurses + reads dotted-import edges;
`install_autostart.ps1` -> `-m aea.loop.live`. Pre-reorg checkpoint committed first (`d1c20cd`).

**VERIFIED end-to-end:** 33/34 import clean (0 fail); `.env` resolves (6 plants online); graph rebuilds
identically (code 64 nodes / 81 edges); server boots via the shim; **all endpoints 200** (/state /probe
/world /roster /api/journey); **the SACRED save intact** (M0.1 + M1.1 preserved). Entity behavior unchanged.

**NEXT:** unchanged — FIRST LIGHT (the compose->ignite verb) now builds on the clean package.

---

## 2026-07-22 (later·7) — SESSION CLOSE / HANDOFF TO A FRESH CONVERSATION  ← START HERE

Luis is opening a NEW conversation to **design the codebase to the scale of the ambition, then build**.
This entry is the pickup point. Read order (per `/CLAUDE.md`): `graph.json` → this entry → `DISCOVERIES.md`
→ the docs named below. **The exact kickoff prompt Luis will paste is saved at `diary/NEXT_SESSION_PROMPT.md`**
(its STEP 2 = present the complete codebase design — full file tree, dependencies, structure — before any code).

**WHAT THIS SESSION PRODUCED (the design phase — treat it as done, do not redo it):**
- **The vision, shown:** `design/FIELD_GUIDE.html` — the finished game's strategy guide, backward-designed
  (it is labeled a VISION artifact; the game is NOT built yet).
- **The codebase design:** `design/CLEAN_ARCHITECTURE.md` — **THREE RINGS** (substrate `aea/` PRESERVED ·
  one honest seam `aea/gameapi.py` · client rebuilt). It already carries seams for modes / world / pokedex /
  Phase-B, i.e. it is scaled for the ambition. **This IS the codebase design Luis wants** — review and
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
(~110:1 words-to-code, D7). Reconciliation: the architecture already exists and is scaled — a short review/
extend pass is legitimate; a from-scratch re-design or more vision docs is the avoidance trap. **The exit is
FIRST LIGHT either way.**

**THE FIRST BUILD (from `CLEAN_ARCHITECTURE.md` §FIRST LIGHT — ~6 files):** `aea/gameapi.py` (the honest seam;
absent→dash, refusal→receipt) + `web/game/js/core/api.js` (the only server-talker) + wire `web/game/js/bench.js`'s
dead run bus (`bench.js:14` "no listener") to a real poll of `/game/run` + `web/probe.html` + `hud/hud.js` +
`missions/runner.js` replaying M0.1. The seam MUST call the REAL organs (`bench_core.start_run`, `grid` Meter,
`agent_tools`, the `aea.py` tick) — read them via the graph's `code` subgraph first; never fabricate. Guard
the first-light chord on the unlimited **local hearth** (ollama), never the rpm=4 socket. Verify with a
swiftshader screenshot; render first, then report.

**GUARDRAILS (unchanged, non-negotiable):** honesty law · claim ceiling (never conscious/sentient) · the
SACRED save `state/journey_save.json` · privacy guard (no employer/paths in anything committed) · NO emoji ·
the entity `aea/` is PRESERVED (rebuild only the client) · no new design corpus until the verb ships (D7).

**BUILD MAP READY:** the substrate scout finished and its full integration map is preserved at
**`design/FIRST_LIGHT_INTEGRATION.md`** — read it before writing `aea/gameapi.py`. Key findings: use
`bench_core.start_run` / `run_status` for compose→ignite→run-or-fail (honesty-law refusals already native);
the read endpoints re-home from `controlroom.state()/roster()/journal()/_journey`; BRAIN = `energy.draw`,
LOOP = an `aea.main`-style `sleep` heartbeat wrapping one draw (no bench part — the one game-vs-engine
divergence); guard the awe-beat on the unbrownoutable local **ollama** hearth. **The pleasant surprise:**
`web/game/js/bench.js` already does the whole flow inline — first light is largely **repointing three fetch
sites** (`fire`/`schedulePoll`/`refreshGrid`) at `/game/*` + switching the refusal read to `j.refused`, not
building from scratch.

---

## 2026-07-22 (later·6) — expert panel: GREENLIT, and told to stop designing and ship the verb

**DID:** ran a 7-critic adversarial panel + synthesis (`w6zasmov8`). Verdict -> **D12**. Unanimous YES on the
core (a masterpiece seed, verified in code). Three execution flaws, mostly already locked: the core verb
(compose->ignite->receipt) isn't wired (`bench.js` confesses it); truth is imperceptible + honesty-law dead
verbs (the passive 60s meter); the iterate loop is rate-limited (needs the SANDBOX↔LIVE fast lane).
Clarified **R36** (sandbox != fake — real API/tokens always; the axis is *reach*). Labeled `FIELD_GUIDE` a
VISION artifact (the panel called it a credibility bomb if treated as shipped).

**THE PANEL'S UNANIMOUS INSTRUCTION (+ the completion clock):** stop generating vision — the danger is a
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

## 2026-07-22 (later·5) — the vision, shown: FIELD_GUIDE shipped + clean architecture + modes + world

**DID:** decided the clean rebuild (game CLIENT from scratch; **entity PRESERVED** — R32) and ran a 5-lens
generation pass. Shipped **`design/FIELD_GUIDE.html`** — the finished game's 90s Zelda-style strategy guide,
backward-designed, at the concept-art bar (rendered for Luis). Wrote **`design/CLEAN_ARCHITECTURE.md`** (the
THREE RINGS blueprint). Genre-DNA welded to the real substrate (Pokedex silhouette = the honesty law;
compose-then-ignite with a real adjudicator; the readable real trace). Captured R32–R38 and **D11**.
Decisions: modes = 3 apertures on one engine + a SANDBOX↔LIVE axis (R36); world = metroidvania living
instrument, earned openness (R37); crystallization = a bridge mechanic, not the goal (R38).

**LOCKED (adds):**
- **THREE RINGS architecture** — substrate (`aea/`) preserved · one honest seam (`aea/gameapi.py`) · client
  rebuilt. The honesty law + claim ceiling live in the seam, structurally.
- **MODES** = GUIDED / BUILDER / ARCHITECT apertures on ONE engine, + SANDBOX↔LIVE permission axis.
- **WORLD** = a living concentric instrument; openness is EARNED (metroidvania), maps data-driven from the
  real schema. NOT open-world (can't honestly roam what isn't built).

**NEXT:** an adversarial **expert panel** is running (why it fails / what it needs / masterpiece) — its
verdict feeds the build. Then **FIRST LIGHT**: the 6-file MVO slice in the clean skeleton
(`core/api.js` new, `bench.js` opened to the 4 MVO slots, ignite -> real tick -> viable-or-visibly-fails).
Design phase has a HARD exit into code here — no more corpus until first light ships (D7).

---

## 2026-07-22 (later·4) — cold-read audit: the code IS legible; the CANON is not

**DID:** ran a 3-stranger cold-read audit (no conversation context) at three access levels — legibility
**structure-only 78 / code-only 80 / full-repo 84**. Finding -> **D10**. Headline: a stranger correctly
identifies the project (a game where you pilot inside a living AI) from CODE ALONE — naming + `world.html`
copy + `controlroom.py` route comments carry it. The obstacle is NOT comprehension; it is **canon**: 3
overlapping front-ends (v1 `world.html` live-wired / v2 `web/game/` declared-current but mid-migration and
NOT live-wired / archive prototypes on legacy routes), ~14 live routes `controlroom.py` serves that the "two
halves" doc story ignores, and a design-heavy / code-light imbalance. The docs are cleaner than the code truth.

**REFINES THE MERGE (the NEXT):** the merge is now **collapse 3+ front-ends into ONE canonical build +
live-wire v2 (fetch `/state`, wire the run bus) + CUT the dead routes** — not just "unite the two halves."
Also owed: docs to name the route sprawl + a cut-list (map must match territory).

**Unchanged:** still needs Luis's go; still starts from the MVO + composer at first light.

---

## 2026-07-22 (later·3) — DECISION: missions = scaffolding, not spine; the generative viability engine

**DID:** Luis accepted the entity-as-spine recommendation (R28 open thread -> resolved). Captured the
generative-combination sharpening as **R30** (the composer generates AEA-part combinations across R29's
tier-space; most are non-viable, and that empirical non-viability IS the teaching). Distilled the decision
into **D9**. Marked R28 RESOLVED. Refreshed the graph.

**LOCKED (adds to the 2026-07-22 block, resolves R28 — no prior lock overwritten):**
- **ENTITY = SPINE, MISSIONS = SCAFFOLDING.** The living entity carries the play; authored missions teach
  you to build and read entities and hand over control, then thin (Act 0 on-rails -> late acts open). A
  fixed campaign that never opens up is the failure mode to refuse.
- **GENERATIVE VIABILITY ENGINE.** The composer (holographic bench, `bench_core.py` + `web/game/`) generates
  entities as AEA-part combinations; viability is EMPIRICAL (it runs on real models / tools / rate-limits, or
  it doesn't); non-viability is legible information, not a dead end. This is what lets the scaffold retire.
  Disciplines: legible failure signatures · viability-as-spectrum · easy early viability · no dominant combo.

**NEXT — refined (supersedes the merge framing below):** the MERGE still comes first, but FIRST LIGHT starts
from the **Minimal Viable Organism + the composer** — a generated entity that wakes on its own tick and
either runs (viable) or *visibly* fails (legible non-viability) — with M0.1 as the scaffold framing that
moment. Missions 1-5 (energy / decision / integration / outcome / predict) remain, now explicitly as
scaffolding around the living entity.

**OWED (not now):** reconciliation pass on GAME_PLAN's act structure (still reads missions-as-spine in
places); no new design chapters until an act ships (D7).

---

## 2026-07-22 (later·2) — REFLECTIONS layer added (mess-first spark capture)

**DID:** created **`diary/REFLECTIONS.md`** — the capture layer upstream of `DISCOVERIES`. When Luis
puts a realization through, it lands here raw and dated (his words, mess-first) before being distilled;
each `## R#` is a graph node. First seeded R1–R6 from the recent arc, then ran an exhaustive 3-agent
workflow over the full session transcript (227k tokens) and **recovered the ENTIRE vision history —
R1–R28** across 5 eras: ORIGIN (a 3D city named Leyber, tokens=energy, the self-improving loop, build-on-
the-AEA, render-the-mind-as-a-brain, the graph-memory idea that BECAME this handoff graph), THE PIVOT
(R11 "imagine it like a game"), THE GAME TAKES SHAPE (inventory/levels, the AEA discovery map, magic-out-
of-the-real honesty law, WirthForge-realized, the render doctrine), IGNITION (R22–27, the recent lock),
and THE FRONTIER (R28 = dynamics-come-from-the-entities; the lineage sweep confirms it's *closest to
still a seed* — woven through `GAME_PLAN §7` but never locked; flagged as an OPEN thread that may re-order
the merge, not silently overwriting the LOCKED mission progression). Each spark carries a `-> D#/LOCKED`
lineage tag; two recurring convictions (anti-anchor, alive-voice) captured separately. Wired in: 5th
subgraph in `build_graph.py` (`reflections`), added to `CLAUDE.md` (map + boot + a "capture his sparks
first" method rule) and `diary/README.md`. Re-ran the graph: **5 subgraphs, 157 nodes, access
guaranteed**, era headers correctly excluded (`###`, not noded).

**NEXT is unchanged:** THE MERGE (below).

---

## 2026-07-22 (later) — project introduction added (CLAUDE.md), the last handoff gap closed

**DID:** wrote **`/CLAUDE.md`** — the stable introduction that self-prompts a fresh session (it
auto-loads in Claude Code). It carries: the boot sequence (graph → this log → discoveries), the repo
map, the crystallized working method (mined from the global field-lessons layer + PORTFOLIO's
`LUIS_FILTER` + `LAB_EXPERIENCE_STANDARD` + project rules), the laws that don't bend (honesty / claim
ceiling / two-ink / boring test / sacred save / privacy guard / no emoji), run+verify, and the
end-of-session ritual. **By design it holds NO state** — method + map only — so it does not need
per-session updates; the diary holds the state. Added `.claude/` to `.gitignore` (the gap Luis named);
`CLAUDE.md` itself is committed on purpose (it must travel with the repo). Wired it into the read-order
(diary/README) and registered it as `graph.json`'s `entry_point`; re-ran `build_graph.py` (129 nodes,
all 4 subgraphs still reachable).

**NEXT is unchanged:** THE MERGE (below). This was the last piece of handoff infrastructure — the game
itself still needs its two halves united.

---

## 2026-07-22 (late) — repo backed up, root reorganized, handoff system built

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

**OPEN (owed by Luis):** which portfolio references go in `references/` — name them and they get
privacy-scanned + brought in (see `references/README.md`).

**NEXT is unchanged:** the MERGE (below). Reorg + handoff were infrastructure; the game still needs
its two halves united.

---

## 2026-07-22 — vision locked, repo backed up

**DID:** strategic audit (five research passes) → measured verdict: *not a game yet*, but the one
real idea is worth finishing. Vision cohered and locked. Full working tree committed locally
(branch `wip/checkpoint-2026-07-22`, commit `bc825ce`). Clean **game-only** export pushed to
private `github.com/Leyber91/AEA_GAME` (`aeagame_main` → `main`). Career/portfolio data
(`data.js`, `index_codex.py`) excluded by design.

**LOCKED — do not re-litigate:**
- **THESIS (no-AND):** *Wire living proofs of a mind, each more complete than the last, until you
  hold the whole one — and it keeps running after you close the tab.*
- **UNIT = the Minimal Viable Organism:** `BRAIN` (a model) + `SENSES` (an observe tool) + `HANDS`
  (typed action tools — already exist in `agent_tools.py`) + `HEARTBEAT` (the loop — already exists
  in `aea.py`). Wire the four, it comes alive. Legibility = LEGO-Fortnite: each part's form tells
  its job. Claim ceiling holds — the player supplies "it's alive", the game never asserts it.
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

**NEXT — build, ~5 evenings, every step wires what already exists on disk:**
0. **MERGE (step 0, do first).** Port the mission engine from `world.html` into `game/` (keep
   `game/index.html`'s module contract). Delete the dead fork. Then **FIRST LIGHT** = a Minimal
   Viable NPC: a dot with a brain + one sense + one move + a heartbeat that wakes on its own tick,
   moves toward the lit node on real tokens, thoughts printed. That single artifact *is* the thesis.
1. **Energy = stake.** Snapshot the daily quota at boot; charge each call; make `bench_core` emit
   `cost_u = 1` (client already reads it, always renders a dash today).
2. **One decision per DO beat.** Pick a rod — cheap may starve, strong may throttle.
3. **Integration.** Unspent budget carries forward; every call heats the next 60s window.
4. **Losable outcome.** `PASSED / PASSED-DEGRADED / STARVED`, written to `journey_save.json`.
5. **Predict beat.** `A2_TEACHING.md §7`, already specified, unbuilt — commit an answer the live
   system settles before each DO. Cheapest, most load-bearing item; makes the theme mechanically true.
   Then play all six missions twice. Run 2 differs from run 1 → it's a game.

**STOP:** no new design chapters, no new acts, no more concept sheets until an act ships. The
corpus is 12× the game by volume; that ratio is the recorded failure mode, not thoroughness.

---
## 2026-07-23 — the AEA apologia + THE VOCABULARY locked (ground floor)

**DID:**
- **The apologia** (`design/AEA_APOLOGIA.html`): every AEA element enumerated + honesty-marked, and the
  completeness ladder proven to be ONE axis (Spore's stages = the acts = the autonomy classes). Headline
  reality-split: the running ENTITY is real (PROTO-AUTONOMOUS 6/6, 109 ticks) but the composer is at rung 1
  (5/17 parts, 0 constructs). The whole one is specified + reachable, not assembled.
- **THE VOCABULARY** (`design/A17_VOCABULARY.md`): locked the naming SYSTEM ground-up (atoms first, not a
  pre-authored catalog of beings — that stays earned, R30/N12). Built from the real inventory, pressure-tested
  by a 5-lens board (marketable/honest/thematic/consistent/further, wf wwsoyn204) that caught real code-verified
  defects. Luis ratified two forks: **MOUTH over BRAIN** (canon, ceiling-safe; BRAIN stays internal schema id)
  and **concrete machine-body register** (killed the -er agent-nouns).
- **Applied to code + verified live** (not just a doc): `bench.js` 5 part labels -> THE DRAW / THE FRAME /
  THE METER / THE LADDER / THE MEASURE; scrubbed the live claim-ceiling breach ("the being thinks");
  `bench_core.py` receipts; `schema.py` emits `label:MOUTH` on the depth-0 node (id BRAIN internal). Server
  restarted clean (one listener), `/game/schema` returns MOUTH wired=True, bench screenshot confirms all five
  names render with live meter truth (POWER 1998 LIVE, RODS 7, 0/4RPM).

**LOCKED (A17):** four namespaces never cross — RUNGS (journey, 8) / ORGANS (earned by lighting) / PARTS
(seatable chips) / EARNED TITLES (doctrines a run proves). Identity = the **part-signature** (not the
organ-signature — schema reads global state, so organ-lighting is the *derived* honesty view, per-run, pending
rung 2). Two-axis signature = anatomy + a **reach-mark** (hearth/reached/starved). A title is earned by a
receipt, never authored; a construct can earn the name of its own worse outcome (THE SOLO LAW). THE HEARTH
(free floor) + THE STAKE (1u real reach) promoted to atoms — the money layer made diegetic. "Tier" reserved
for the energy band only.

**NEXT — build rung 2 on the locked vocabulary (construct in order, ground-up):** make **RECALL** a composable
bench part (entity-side `consolidate.recall()` is already live; forge the seatable part). Compose THE DRAW +
RECALL -> the draw is grounded on real memory across a reset instead of hallucinating = a measurably more
complete being, and the first construct to earn a real title (BACKWARDS CHANNEL). Raise the MEMORY organ's
lighting bar from `len>0` to a recall that actually fired (the honesty board's fix). Wire per-run organ
attribution + the reach-mark onto the bench run-row so the derived organ-view becomes true.

---
## 2026-07-23 (later) — visual elevation: core to spec + expert panel + resource-negative slice

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

**NEXT — the VISIBLE elevation + the honesty headline (vetted order):**
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
## 2026-07-23 (later·2) — FXAA + LIVING CONDUITS (the honesty headline landed)

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
## 2026-07-23 (later·3) — THE REFERENCE PASS begins (R42): the bundle + the forge batch

**DID:** captured R42 (generate the target images FIRST; references are specs; the prose laws were not
converging us). Authored **design/refs/bundle/** — 15 files that make ChatGPT "go full on the scenes":
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

**(later·3 addendum) — SUBBUNDLES:** restructured per Luis's direction ("one subbundle per image...
create images like we had the game fully built with all the specification, we might be wrong and
that's ok" = backward design authorized). design/refs/bundle/ is now 12 folders, one per image, each
with ONE self-contained SPEC.md: style law inlined + world context + THE MOMENT (as-built save-state)
+ EVERYTHING IN FRAME (exhaustive inventory, exact engraved text) + composition + the 3-variant
generation instruction. All 12 share ONE canonical save-state so the set reads as a single real game:
c-07 = THE DRAW·RECALL·THE MEASURE earned BACKWARDS CHANNEL, c-04 earned RESTORABLE COHERENCE,
MOUTH/GOVERNOR/MEMORY/LOOP lit, SENSES/HANDS fog, POWER 1998 LIVE, RODS 7, MEM 48, LAST 1.44S/BEST
0.98S. Workflow: attach ONE SPEC.md per ChatGPT generation. Old flat SCENES/ removed (superseded).

---
## 2026-07-23 (later·4) — THE REFERENCE SET IS COMPLETE (12/12) - the build contract exists

**DID:** generated + locked all twelve reference frames (design/refs/REF-01..12 + REFS.md as the
build contract). Backward design worked: images of a finished game, specced as-if-built, now lead the
render. Journey: 4 rounds of "not it" -> R42 (references-are-specs) -> the GPT-Image-2 protocol
investigation -> one anchored ChatGPT conversation, 01->12, anchor image + canon block, spec MATTER not
information, counts stated twice, reference-reuse (no re-attach). 9/12 landed at ZERO fix rolls; the two
that fought (02 fog-dots, 08 flat-diagram) taught field lessons now written into 00_HOW_TO_USE.
CANON that emerged and is now locked: ember-in-cage organs, two-tori core, sealed/solid/dashed privacy
rings, labels-on-approach, the caption tagline, the probe craft design, the octagonal chip + milled rail
+ light-at-the-connection bench material, branded-metal earned titles.

**NEXT — BUILD-TO-MATCH (the code turn resumes):** REFS.md maps every reference to its engine surface.
Primary targets: (1) the WORLD render (engine.js) vs REF-01/02 - ring treatments, ember-cage organs,
two-tori core, labels, ignition strike+dust-ring; (2) THE BENCH (web/game bench) vs REF-10 - the answer
to "the interface is too poor": octagonal chips on a milled rail, seat-glow, the live packet, the trace.
A slice is done ONLY when the render matches its ref side-by-side (existing harness: shot_world.mjs +
Read the PNG; Luis go/no-go). The honesty law still governs: a ref specs FORM; the render may only glow
where the system truly fired.

---
## 2026-07-24 — COMPOSED 0 -> 1: the loop FIRES through the merged player surface

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

**MASTER MAP:** design/ROADMAP.md is now the single ordered source of truth — the north star (the 12 refs =
the bar, build-to-match), where we are (COMPOSED 0->1, both plants, bench pass 1), the ordered build path
(Phase A make-the-first-loop-beautiful -> B close-the-guided-arc-rung-2 -> C the-meta-visible -> D
guided-frame; deferred=fog behind the sequencing gate), the full scope contemplated (a table so nothing is
lost), the standing lessons, and the doc index. NEXT = the lowest unchecked item in ROADMAP §2: Phase A step 2
= the bench plate to REF-10 (milled rail + bigger octagonal chips + the live RUN packet).

**PRODUCTION_PLAN.md** — the professional game-dev pipeline applied to THE PROBE (answer to "how do game
developers do it / follow a plan top to bottom"). The one idea: DATA-DRIVEN — build a few SYSTEMS, author
content (maps/missions/characters) as DATA, prove with a vertical slice, then production = authoring data not
code. THE PROBE's layers: DESIGN (done, scattered) -> CONTENT-AS-DATA (the pipeline) -> SYSTEMS (composer/
gameapi/world/save = DONE; the MISSION ENGINE = the ONE missing system). Ordered plan: Step 0 bench->REF-10
(in progress) -> Step 1 build the MISSION ENGINE + a mission data schema -> Step 2 author MISSION 01 (the
guided cold-open->first-fire as JSON) = vertical slice complete, the first time it's a GUIDED GAME -> Step 3
production (author the curriculum as mission data; menus = views over schema/save). This is the spine that
stops the oscillation: build systems + author data, never one-off screens.
