# DISCOVERIES — what we learned, as findings (not code)

The plan is not only the codebase. It is also the things we *found out*. This file captures the
load-bearing discoveries so a takeover agent inherits the reasoning, not just the result. Each is a
node in `graph.json`'s `discoveries` subgraph. Newest insight wins on conflict.

## D1 · THE PROBE is not yet a game (measured, not opinion)
Against the canonical frameworks (Juul's six features, Salen & Zimmerman's *meaningful play*,
Costikyan, Crawford's toy/game line) it currently fails on: **no integration** (mission N doesn't
change N+1), **no variable outcome** (`02_SYSTEMS.md §6`: "missions block, they never punish"),
**no stake the player can spend badly**, and a **flat verb set** (fly/dock/press-one-button in
Act 0 and Act VI alike). It is an honest *instrument*, not yet a game. Gap ≈ 4 elements, ~5 evenings.

## D2 · The elements a game is made of (reconciled)
One idea statable without "and" · a documented **refusal list** (what's deliberately absent) ·
**perceivable consequence** (Church) · **depth as decision, not content** (tight coupling: one state
variable read many ways) · coherence found by **cutting**, not designed top-down · a peak + an
ending. NOT required: a thesis, or coherence, for canonisation (Tetris #1 declines its own meaning;
BioShock #12 is the founding ludonarrative-dissonance example).

## D3 · The one idea → IGNITION (the thesis)
> **Wire living proofs of a mind, each more complete than the last, until you hold the whole one —
> and it keeps running after you close the tab.**
Scarcity is demoted to *mechanism* (how the lit thing can die); ignition is the idea. Unit = the
**Minimal Viable Organism**: `BRAIN` (a model) + `SENSES` (an observe tool) + `HANDS` (typed
action tools = `aea/agent_tools.py`) + `HEARTBEAT` (the loop = `aea/aea.py`). Both hands and
heartbeat **already run**. Progression = increasingly complete AEA combinations; the **master = THE
AEA**. A "proof" is a receipt (it runs), never a claim — stratum 10, *claim becomes receipt*.

## D4 · What makes a game spread with no marketing
Every near-zero-spend breakout traces to **one ignition event, a named person and a date**
(SplatterCat → Vampire Survivors, 6 Jan 2022). Wordle spread on a **share artifact** (the emoji
grid), not the puzzle. Alien: Isolation (Švelch, *Game Studies* 20(2)) — a genuinely sophisticated
AI was widely believed to *cheat* because the game never gave players a frame; **invisible systems
do not self-evidence**. Dwarf Fortress: 16 years at ~$15k/mo → ~$7.2M the month it added a UI —
**legibility is the bottleneck, never depth**. Make an invisible truth felt by letting it *cost*
the player something they didn't author (Noita), or be the **verb** (Teardown). Never claim
magnitude (No Man's Sky's 18 quintillion → "samey"). Design the **share artifact** (a run receipt)
before the game.

## D5 · Reachability is the structural blocker
The honesty pillar binds the game to Luis's server, keys, corpus, live entity — "runs from a URL"
is true for exactly one person on earth. Every discoverability finding is downstream of a link a
friend can open. That link does not exist yet; the architecture must earn it (Phase B).

## D6 · Form ruling — the city is an instrument, not decoration
Keep the probe (the vehicle; every DO beat is literally an HTTP call to localhost). Bend the city
into a concentric **instrument**: radius = privacy zone · altitude = dependency-DAG depth · node
fill = live capacity · edges = first-class conduits. NOT open world (short of verbs, not world).
NOT landscape (it encodes zero system facts). The docs had already drifted here (`E6 §3`, `E9`
binds ring radius to `zone`).

## D7 · The corpus was the risk
At the audit: ~398k design words vs ~4.9k lines of game code (~110:1). The recorded failure mode
("brilliant strategy, zero artifacts"). Rule adopted: no new design chapter until an act ships;
the next real progress is code, not words.

## D8 · Reorg lesson — continuity lives in the files
Relocating a running entity's state is surgery, not a move: state resolves through a path model
(`grid.ROOT`/`STATE`/`WEB`), and a missed write-site silently splits or resets state (incl. the
save). Scan BOTH quote styles; test read AND write; verify `.env` still authenticates. Everything
is recoverable via git only because it was committed first.

## THE SHORTEST PATH FROM INSTRUMENT TO GAME (~5 evenings, all wiring what exists)
0. **Merge** the mission loop (`web/world.html`) + the bench (`aea/bench_core.py` + `web/game/`)
   into one program; first light = a Minimal Viable NPC that wakes on its own tick and moves.
1. Energy = a stake (snapshot the daily quota; charge each call; `bench_core` emits `cost_u`).
2. One decision per DO beat (pick a rod: cheap may starve / strong may throttle).
3. Integration (unspent budget carries; calls heat the next window).
4. A losable outcome (`PASSED / PASSED-DEGRADED / STARVED`).
5. The `predict` beat (`design/A2_TEACHING.md §7`) — commit an answer the live system settles.
Then play all six twice; if run 2 differs from run 1, it's a game.
