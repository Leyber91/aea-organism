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

## D9 · Missions are scaffolding, not spine; viability is empirical and IS the teaching (DECIDED 2026-07-22)
The entity-as-spine question (R28) is **decided**: the living entity is the spine; authored missions are
**scaffolding** — they make the autonomous entity legible and the game shippable, and they are designed to
*thin* as the player gains mastery (Act 0 on-rails -> late acts open sandbox). This resolves the
R28/mission-progression collision without overwriting the ignition thesis or the UNIT — it clarifies their
relationship. The engine that lets the scaffold retire is the **generative composition space** (R29 + R30):
the player generates entities as AEA-part combinations, and **most combinations are not viable — and that is
the point.** Viability is *empirical* (it runs on real models / tools / rate-limits, or it doesn't), so the
player learns the real architecture of a mind by mapping which combinations live and why the rest die
(failure-as-information; the failure modes mirror real agent-architecture failures). **Consequence for the
build:** the MERGE starts from the Minimal Viable Organism + the composer, not from M0.1; M0.1 becomes the
scaffold framing the MVO's first self-directed act. **Disciplines:** legible failure signatures;
viability-as-spectrum not binary; easy early viability; guard against a dominant combination.
**Owed (not now):** GAME_PLAN's act structure still reads missions-as-spine in places — a reconciliation
pass is owed (SESSION_LOG + this discovery govern on conflict; no new chapters until an act ships, D7).

## D10 · Cold-read audit — legible in the parts, ambiguous in the CANON (measured 2026-07-22)
Three strangers (no conversation context) read the repo blind at three access levels; legibility scored
**structure-only 78, code-only 80, full-repo 84** (0-100). Verdict: a stranger CAN tell what this is — all
three independently and correctly identified *"a game (THE PROBE) where you pilot a probe inside a real
running autonomous AI entity (LEYBER), every number live truth."* The code-only reader (forbidden ALL prose
docs) said *"yes, unambiguously, from code alone"* — carried by `world.html`'s own copy ("a journey into a
living entity"), `engine.js` (a real flight rig), `missions.js` (Acts/beats), and `controlroom.py`'s route
comments. Naming was praised as "exceptionally descriptive." So "what is this" is NOT the problem. The REAL
problem, hit independently by all three: **which version is canonical and how much actually runs.** (1) THREE
overlapping front-ends — `world.html` (v1, live-wired) vs `web/game/` (v2, declared "the NEW codebase" but
MID-MIGRATION: `engine.js` hardcodes geometry and never fetches `/state`; `bench.js` says "run:link has NO
listener yet") vs `archive/` prototypes still reachable on legacy routes; (2) `controlroom.py` serves ~14
live routes (`/probe /lab /city /brain /mind /tree /builder /plan /poster /room /workspace /tracker /game
/world`) that the docs' clean "two halves" story does not account for; (3) design-heavy / code-light (~40
chapters + hundreds of PNGs vs ~6 game JS files) makes "is it playable yet" unanswerable from structure.
**Meta-finding:** the docs are CLEANER than the code — they carry intent/spine/how-to-run (the full-repo
reader BOOTED it and verified every claim TRUE, incl. live `/state` + the sacred save) but paper over the
fork/route sprawl. **Consequence — the MERGE is redefined and more urgent:** not merely "unite mission loop +
bench," but **collapse 3+ front-ends into ONE canonical build, live-wire v2 (fetch `/state` + wire the run
bus so the canonical build actually shows the living entity), and CUT the dead routes** — and the docs must
name the sprawl + cut-list so the map matches the territory. The legibility fix is cutting and resolving
canon in code, NOT more docs.

## D11 · The vision crystallized — backward-designed, genre-welded, clean-architected (2026-07-22)
A five-lens generation pass turned the reset (D10) into a concrete, buildable vision.
**(a) Backward-designed as a strategy guide:** `design/FIELD_GUIDE.html` — the finished game's 90s
Zelda-style player's guide, built first so the code has a north star. **(b) Genre-DNA welded to the real
substrate** (not cargo-culted): the Pokemon **silhouette of the un-caught IS the honesty law** (Pokemon
fakes the absence to tease; THE PROBE's is real, so the same desire-engine ends in a receipt); LEGO-Fortnite
= **compose-then-IGNITE with a real adjudicator** (the autonomy battery, not simulated physics); deep-systems
= the **readable REAL trace** as the central object of play (its one edge over Factorio/Zachtronics). Each
lens also produced its refusal list (no gotta-catch-em-all, no invented type chart, no cosmetic parts, no
output-side RNG, no dominant-strategy collapse). **(c) Clean architecture = THREE RINGS** (see
`design/CLEAN_ARCHITECTURE.md`): `aea/` substrate PRESERVED · one honest seam `aea/gameapi.py` where the
honesty law lives structurally · a concern-scoped client REBUILT. The pass also caught that the legacy view
routes serve `"<file>.html missing"` strings TODAY (they `open()` from the pre-reorg path). **(d) Modes
(R36)** = 3 apertures on one engine (GUIDED/BUILDER/ARCHITECT) + a SANDBOX↔LIVE stakes axis — not 3 products.
**(e) World (R37)** = a living concentric instrument with EARNED (metroidvania) openness, data-driven from
the real schema. **NEXT:** an adversarial expert panel is stress-testing the vision (why it fails / what it
needs), then the build is FIRST LIGHT — the 6-file MVO slice in the clean skeleton. Design phase has a hard
exit into code; no more corpus until first light ships (D7).

## D12 · Expert panel — GREENLIT masterpiece seed; three execution flaws; SHIP THE VERB (2026-07-22)
A 7-critic adversarial panel (each played it) + a showrunner synthesis (`w6zasmov8`). **Unanimous: YES, the
core is a masterpiece worth building** — verified in the CODE, not just the copy (`grid.py` meters for real,
`model_fitness.py` classifies real failure, `autonomy.py` caps its own claims). The thesis (refuse to
simulate; expose a real running mind; the win is READING it; a receipt not a claim; a dash for the unknown)
is novel and defensible. **But three flaws would sink it even for its target audience — all execution, not
concept, and mostly already LOCKED:** (1) **the named core verb isn't built** — compose -> IGNITE ->
receipt is not wired (`bench.js:14` confesses "run:link has NO listener yet"); until the verb is the thing
you DO, all else is polish on a promise; (2) **truth is imperceptible + the honesty law is producing DEAD
VERBS** (survey/observe/watch/wait; the passive 60s meter-watch in minute nine is the emblem) — realness is
asserted on an unverifiable receipt and buried where it is most felt; (3) **the iterate loop is rate-limited
by design** — genre-fatal for the systems audience; the fix is the SANDBOX↔LIVE fast lane (local hearth +
replayed real traces), R36, unbuilt. **THE ONE MOVE that unlocks everything:** make the player compose two
real parts and IGNITE, in the flown world, inside the first 10 minutes, with realness demonstrated against
fake ONCE, in their own hands. *"Ship the verb, not more of the vision."* **HOLD THE LINE (deliberate
exclusions to KEEP — the answer to "we don't chase likability"):** the honesty law; the claim ceiling; real
code/jargon in learn-beats (a non-engineer bouncing off code is the CORRECT filter, IF the concept beside it
is scaffolded); latency-as-truth waiting (fix the dead verb, keep the cold truth); LLM non-determinism
(optimize the distribution, never force determinism); losable bosses / honest failure / no rubber-banding;
the two-ink austerity (it WILL repel the spectacle crowd — that is the point); local-only/BYOK for the full
product; **the audience is AI-curious builders, NOT everyone**; the coldness. **THE MIRROR (the panel caught
us):** it independently flagged this session's own pattern — ~110:1 words-to-code (D7), "reviewing the
trailer instead of the tech demo"; `FIELD_GUIDE.html` is a credibility bomb if treated as shipped (now
labeled a vision artifact). **NEXT is not more design — it is FIRST LIGHT (the verb). Stop the corpus.**

## THE SHORTEST PATH FROM INSTRUMENT TO GAME (~5 evenings, all wiring what exists)
0. **Merge** the mission loop (`web/world.html`) + the bench (`aea/bench_core.py` + `web/game/`)
   into one program; first light = a Minimal Viable NPC that wakes on its own tick and moves.
1. Energy = a stake (snapshot the daily quota; charge each call; `bench_core` emits `cost_u`).
2. One decision per DO beat (pick a rod: cheap may starve / strong may throttle).
3. Integration (unspent budget carries; calls heat the next window).
4. A losable outcome (`PASSED / PASSED-DEGRADED / STARVED`).
5. The `predict` beat (`design/A2_TEACHING.md §7`) — commit an answer the live system settles.
Then play all six twice; if run 2 differs from run 1, it's a game.
