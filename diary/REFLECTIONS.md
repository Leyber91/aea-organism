# REFLECTIONS — Luis's realizations, captured raw (mess-first)

This is the **capture layer**, upstream of everything else. When a realization lands — a vision-shift,
a design idea, "wait, this could be huge" — it goes HERE first, in his words, the moment it happens.
Mess-first (his own methodology): capture the spark raw; filtering, reconciliation, and redesign happen
later, rested, in a separate pass. Typos are fine — parse intent, not spelling. Nothing gets
re-interpreted on the way in.

**The flow:** REFLECTIONS (raw spark) -> `DISCOVERIES.md` (distilled finding) -> `GAME_PLAN.md` /
`design/` (the plan) -> the build. When a spark graduates it is tagged `-> D#` / `-> LOCKED`, but the
original stays here — the reflection is the origin, the discovery is the distillation. Each `## R#` is a
node in `graph.json`'s `reflections` subgraph; numbers are stable (they are node ids). Append new ones
at the end with the next `R#`.

**For Claude (the capture rule):** when Luis *puts a comment through*, write it here first, dated, in his
words, BEFORE rushing to act on it. Losing the spark to fast execution is the failure this file prevents.

**How this file was built:** the recent sparks were captured live; the earlier ones (R1–R21) were
recovered by an exhaustive sweep of the full session transcript (2026-07-22), so the vision's whole
arc — from "a 3D city" to "it's a game" to "ignition" — is preserved, not just the latest chapter.

> **CURRENT FRONTIER:** the vision is now a thing you can look at — `design/FIELD_GUIDE.html` (the
> backward-designed strategy guide) + the three-rings clean architecture. Live edges: R36 (three mode
> apertures on ONE engine — GUIDED / BUILDER / ARCHITECT — plus an orthogonal SANDBOX↔LIVE stakes axis),
> R37 (the world = a living concentric instrument with EARNED / metroidvania openness, data-driven maps),
> R38 (crystallization = the bridge mechanic, not the destination). Built on R28–R35.

---
### ERA 1 · ORIGIN — before it was a game (~project opening)
The instinct was already there: a living, self-improving system you can see and manipulate. The word
"game" had not been said yet.

## R1 · A playable 3D city, and a voice that sounds alive
**Spark:** *"it doesn't look like a city, I want like a 3D city, like Cities Skylines or SimCity. It's
useless right now, and the voice is not natural in any sense."*
**Realized:** the interface should be a playable 3D place whose components you manipulate, and the
entity's voice must sound genuinely non-robotic. *(Form later evolved: city -> concentric instrument,
D6. The natural-voice want recurs across the session and is still open.)*

## R2 · Call it Leyber; tokens are energy; run a conscious self-improving loop
**Spark:** *"a concentric map, circular. We will call it Leyber... The sources of tokens are my sources
of energy... a conscious loop to check every part of the system to look for code improvements, skills
that are redundant, improvement of the principles."*
**Realized:** a concentric architecture named Leyber, powered by tokens-as-energy, running a loop that
continuously inspects and improves its own parts. *(-> LOCKED concentric form, D6; the self-inspecting
loop is the entity's own drive.)*

## R3 · Build ON the AEA, not from scratch
**Spark:** *"we need not to start from scratch, the autonomous entity architecture provides us plenty of
room. The model is frozen in time, a black box; we put layers like memory, like tools. All these have
already been found on the AEA."*
**Realized:** the entity is a frozen-model black box wrapped in the memory/tool layers the AEA already
defines — the game implements the AEA rather than reinventing it. *(Foundational premise.)*

## R4 · Autonomy = press play; a scheduled loop that checks its own systems
**Spark:** *"we click play, let it run a loop that uses tokens to check each of its systems, like being
alive constantly on a scheduled iteration? Does the iteration with time improve? That is the piece I'm
struggling with."*
**Realized:** autonomy is a token-spending loop the entity runs on its own schedule to inspect itself;
the open question is whether it improves over iterations. *(-> the HEARTBEAT, `aea.py`; the "does it
improve" question is answered by crystallization, R5.)*

## R5 · Tokens are energy, models are accelerators — crystallize
**Spark:** *"we never expect a model to improve, we expect the structure to respond better to more
evolved models. Crystallization is key, at one point we won't need even models for most tasks; models
are accelerators, tokens are energy. I want a multi-tab dashboard to see every element of what it's
doing."*
**Realized:** a model-agnostic structure where tokens = energy, models = accelerators, behaviours
crystallize until models are rarely needed, all watched through a global dashboard. *(-> LOCKED energy =
real quota; the crystallize doctrine.)*

## R6 · Show the mind as one navigable 3D brain
**Spark:** *"a global workspace, a self-model, metacognition, agency, temporal continuity, drives, a
world-model... show it as one unified 3D model I can navigate, like seeing a naked brain. Swarms of
models, batch processing equal to how our brain manages bits of the same info on different parts."*
**Realized:** render the entity's cognition as one navigable 3D brain, with model swarms doing
brain-like parallel processing. *(Seed — visualization ambition.)*

## R7 · A Claude-level entity fused with my thinking — and a knowledge graph so it doesn't burn context
**Spark:** *"an assistant that is at the same level as yourself, combined with my thoughts... Are we
using LangGraph or a knowledge graph, so as not to consume the context window on every turn?"*
**Realized:** the entity is a top-tier agentic assistant carrying Luis's thinking, using graph memory to
avoid re-reading everything each turn. *(-> graduated into the handoff **knowledge-graph itself**,
`graph.json` / `build_graph.py`.)*

## R8 · A real battery of tests to prove autonomy
**Spark:** *"a battery of tests to prove an entity is an autonomous entity itself... can it keep
evolving? There must be tests online, theories and principles we can test."*
**Realized:** validate autonomy against real theories, not assertion. *(-> the autonomy battery,
`docs/AUTONOMY_BATTERY.md`.)*

## R9 · A self-building timeline of every bifurcation and tool call
**Spark:** *"a dynamic timeline map of all the bifurcations the models called, so I see the path the
entity takes on the use of tools."*
**Realized:** the entity should draw its own decision/tool-call path as a live timeline. *(-> the trace
substrate.)*

## R10 · A building tab — watch it assembled like a puzzle
**Spark:** *"the building tab. I want this to be a puzzle... see the code written slowly, like putting
together pieces, not like n8n. A robot assembled from parts... On the right, the elements of the AEA
pending implementation."*
**Realized:** assembling the entity is itself the show — piece by piece, with the pending AEA parts as a
checklist. *(-> the bench, `aea/bench_core.py` + `web/game/`.)*

---
### ERA 2 · THE PIVOT — "imagine it like a game"
The single reframing everything downstream flows from.

## R11 · Reframe the whole thing as a GAME
**Spark:** *"Imagine it like a game. We need to accomplish the autonomous entity architecture step by
step. I need you to design the game but start playing it, level by level, test it level by level along
with me."*
**Realized:** the project IS a game whose objective is to build the AEA, level by level, played and
tested collaboratively. *(The defining vision-shift; every reflection after this is downstream of it.)*

---
### ERA 3 · THE GAME TAKES SHAPE
Levels, inventory, the map, the look, the positioning.

## R12 · A guided level journey with an inventory — token limits are resources you grow
**Spark:** *"a journey that gets us to the AEA... multiwindow, you will have your inventory, think of
Minecraft, Fortnite Lego, where you slowly get resources, for some you get token limits and increase
capacity. What we have is boring as fuck, too static."*
**Realized:** a guided, level-based journey with a multiwindow inventory and real resource progression
(token limits as capacity you earn). *(-> LOCKED progression + inventory.)*

## R13 · A discovery map of the AEA as a concentric field
**Spark:** *"menus where I see the map of the AEA, the parts I discovered, like a multi-circular
concentric field."*
**Realized:** a map that tracks the AEA parts the player has unlocked. *(-> the AEA census / teaches-map,
`design/A15_FULL_COVERAGE.md`.)*

## R14 · A game is not one markdown
**Spark:** *"the plan cannot be just one document, do you think Fortnite would be one markdown?"*
**Realized:** a game of this ambition needs a full multi-document design system — menus, maps, a corpus.
*(-> the design corpus + this handoff system.)*

## R15 · The core loop: assemble AEA combinations that act on the world
**Spark:** *"build different combinations of the AEA, but instead it will be able to interact with the
world. We have to think outside the box."*
**Realized:** the loop is assembling AEA combinations from an inventory; the combinations act on and
interact with the world. *(-> LOCKED core loop.)*

## R16 · Every AEA part becomes a journey — and the assistant can run in the wild
**Spark:** *"Every single part of the AEA needs to be transformed into a game, a journey. It needs its
own signature, a narrative, a story... the assistant we build, we will be able to make it run in the
wild."*
**Realized:** each AEA concept is its own journey with a signature and story, and the built assistant can
ultimately be released to run for real. *(-> narrative requirement + Phase B bridge.)*

## R17 · Magic out of the real — a pop-culture game that demystifies AI
**Spark:** *"a game never seen before. People will take it as a reference to understand AI... we are not
mystifying AI, we are back to the principle of making magic out of the real. Each player's assistant is
their character to show. We will make it open-ended and a learning reference on AI."*
**Realized:** the founding creative law — nothing simulated, the wonder comes from the real shown
honestly — plus positioning (demystify AI) and a social layer (your entity is your character to show).
*(-> LOCKED honesty law; the "your character" half is also the organic spread mechanism.)*

## R18 · This is the WirthForge we needed, finally realized
**Spark:** *"We are building the game that can make AI mainstream, understandable. Do you remember
WirthForge? We are making the version we needed."*
**Realized:** this game is the concrete realization of the earlier WirthForge manifesto. *(Connects the
manifesto to the build.)*

## R19 · Define the world through concept art
**Spark:** *"give me a few prompts and I run them on ChatGPT to better define what our world, entity, and
parts should look like... conceptual sketches."* Later: *"the images now finally have what we were
looking for... we will need at the end Unity or Blender or both."*
**Realized:** define the visual world by generating concept art as sketch-assets; the concepts hit the
target, and a production build may later need Unity/Blender. *(-> the concept-sheet phase.)*

## R20 · Spread on quality, not marketing
**Spark:** *"What would make our AI game successful, besides marketing? We won't sell shit to fall fast.
Something that spreads for its quality and engagability and awesome design."*
**Realized:** win on quality, engagement, and design; each player's entity-as-character is the organic
reach. *(-> D4 spread factors.)*

## R21 · Premium low-resource 3D — and the render doctrine (solid = what it IS, hologram = what it SHOWS)
**Spark:** *"i dont mean we have shitty graphics, i mean we have good ones but resources done well"* /
*"holograms with the pictograms is ok... BUT HELL NO with the probe hardware, THESE CANNOT BE HOLOGRAMS."*
**Realized:** high perceived quality at low GPU cost via curated stylization (not realism, not
2000s-looking); and a hard render split — physical objects (probe/hardware) are SOLID because they are
what the entity IS, holographic displays are what it SHOWS, flat UI is apart. *(-> E8 fidelity law /
two-ink visual law.)*

---
### ERA 4 · IGNITION & THE LIVING UNIT (the recent lock, 2026-07-22)
The idea sharpens to its coinable core.

## R22 · Ignite independent organisms that run on tokens
**Spark (2026-07-22):** *"we ignite a character, a mechanism, independent, that keeps doing queries on a
loop for directions, we give a live organism... imagination is powerful, but igniting the path. We
should coin this sentence."*
**Realized:** the core act is *igniting* something that then runs by itself on tokens — the game makes
AI's energy cost visceral. *(-> D3 IGNITION / LOCKED thesis: "...keeps running after you close the tab.")*

## R23 · Assemble brains from Lego pieces — readable or they quit at step one
**Spark (2026-07-22):** *"like in fortnite lego... here the pieces would be types of brain, models or
combinations of models, loops. It needs to be easy to understand so people don't abandon in the first
step."*
**Realized:** building an entity is Fortnite-Lego assembly with brain-pieces; each piece's form must tell
its job, because the first step is the drop-off cliff. *(-> LOCKED legibility law + D4: legibility is the
bottleneck, never depth.)*

## R24 · Minimal Viable Organism — aliveness = how often it queries on its own
**Spark (2026-07-22):** *"how often does it query the model on its own?... we need minimal viable NPCs,
minimal viable machines, minimal viable organism... a holographic display where you wire the cables...
tool use, or we develop our own MCP behaviour."*
**Realized:** the smallest alive unit, defined by self-directed query frequency, wired on a holographic
cable bench, acting through tool-use or a custom MCP. *(-> D3 the unit = BRAIN + SENSES + HANDS
(`agent_tools.py`) + HEARTBEAT (`aea.py`); hands and heartbeat already run.)*

## R25 · Entities are proofs of AEA combinations; the masters ARE the AEA
**Spark (2026-07-22):** *"the characters, machines and organisms will be proofs of different combinations
of the AEA. Eventually there will be masters that will be THE AEA... we will guide users to get to the
AEA."*
**Realized:** every creature is a proof (a receipt that runs, never a claim) of an AEA combination;
progression is understanding; the master is the whole AEA; the game guides players there. *(-> LOCKED
progression.)*

## R26 · Missions -> an open world where your entity acts on the real internet
**Spark (2026-07-22):** *"missions and steps towards the final goals, and once you go there, the world is
open. It can contact the internet, do things for you, but only if the chosen prompts are good. Prompting
given as templates, but you could give your own. This game can actually be huge, I'm realizing it."*
**Realized:** progression runs from missions into an open world where the built entity acts online, gated
by prompt quality — making prompt-craft the mastery axis. *(-> Phase B endgame + D5; the reach is the
point.)*

## R27 · Continuity lives in files — any conversation can take over from the repo
**Spark (2026-07-22):** *"each session makes a report of what it did so the next session can pick up...
any conversation can take over the development."*
**Realized:** no one session builds it all, so continuity must be engineered into the repo — dev diary,
discoveries, an intro/methodology file, graph knowledge — not held in one chat. *(-> D8 + this whole
handoff system: `CLAUDE.md`, `graph.json`, `diary/`.)*

---
### ERA 5 · THE FRONTIER
Not yet locked. The next thing to reconcile.

## R28 · The game's dynamics come from the ENTITIES, not from authored content
**Spark (2026-07-22):** the realization that the *dynamics* — what makes it play differently each time —
are produced by the entities themselves being alive: autonomous organisms querying, deciding, and
integrating on their own loops generate the game, rather than hand-scripted mission content driving it.
**Realized / the frontier:** emergent play from living systems (rhymes with D2 "depth as decision, not
content" and D6 "the city is an instrument"; Dwarf Fortress / Rimworld sit here — build the system, not
the plot). The lineage sweep confirms it is woven through `GAME_PLAN §7` ("the world moves because the
entity is actually alive underneath it") but never crystallized into its own LOCKED bullet — **closest
to still a seed.**
**RESOLVED (2026-07-22):** Luis accepted the entity-as-spine reading — **the living entity is the spine;
missions are scaffolding** that makes the autonomous entity legible and the game shippable, designed to
*thin* as the player gains mastery (Act 0 on-rails -> late acts open). The merge now starts from the
Minimal Viable Organism, not from M0.1. Distilled into **D9**. No prior lock was overwritten — this
clarifies the relationship between the entity and the missions.

## R29 · Entities are typed by which AEA parts they embody -> a combinatorial tier-space
**Spark (2026-07-22):** *"the entities along the path will be classified into types based on what parts
of the AEA they embody — that would give us a huge number of combinations, tiers."*
**Realized:** progression is not a single ladder but a **taxonomy**. Each entity's type is its AEA-part
signature (which axes / organs / verbs / ops it embodies), so the space of buildable entities is
combinatorial and naturally tiered by completeness — the master (all parts) = THE AEA is the top tier.
This is the concrete structure under R25 ("proofs of combinations") and the depth engine under R28: typed
entities are what make an emergent sandbox *legible and deep* — you read the living world by type.
**Discipline it needs (or it is fake depth):** per the honesty law, a "type" is real only if it *behaves
measurably differently when it runs* — distinct live latency / verbs / consequence, never a cosmetic
label (the No Man's Sky "18 quintillion -> samey" trap, D4). And the type-space must be revealed
progressively through the discovery map (R13), never dumped at once (R23 onboarding cliff). This is
honestly enforceable here because every part is a real organ with real behavior.
**-> Extends R25 / D3 progression** (the taxonomy IS "increasingly complete AEA combinations"); a frontier
alongside R28. Open thread: the type-space is also the depth argument FOR the entity-as-spine reading of
R28 — see the missions-scaffolding note carried into the next design pass.

## R30 · The game GENERATES AEA-combination entities — and non-viability is the point
**Spark (2026-07-22):** *"we need to be able to generate creatures, entities or machines that are part of
the AEA — there is a whole bunch of combinations this gives us. Not all of them will be viable, but that's
the point: people know."*
**Realized:** the composer (the holographic bench, R24) lets the player GENERATE entities from AEA-part
pieces across R29's huge combination space — and crucially, **most combinations are not viable, and that
non-viability is the teaching.** People learn the real architecture of a mind by discovering which
combinations run and which fail, and why.
**Why it's honest here (not arbitrary):** viability is empirical, not designer-decreed — a combination is
viable iff it *actually runs* on real models / tool-use / rate-limits. The reasons combinations fail ARE
the reasons real agent architectures fail: senses but no hands (observes, can't act); a loop with no
memory (never integrates); a brain too slow to close its loop inside the rate window (starves); no
governor (runaway cost). Failure-as-information (Zachtronics / Factorio / Baba Is You), made real by the
honesty law — R17's "magic out of the real" applied to failure.
**Discipline it needs (or "that's the point" becomes "that's broken"):** (1) every non-viable result
needs a LEGIBLE failure signature — the player SEES why (starves / spins / throttles), else it reads as a
bug, not information (D4 invisible-systems). (2) Viability is a spectrum (viable / degraded / expensive /
fragile), not binary — that spectrum is the depth (D2). (3) Early viability must be EASY — the scaffold
hands you known-viable seeds first; the non-viable wilds are a mid/late pleasure, not a first-step wall
(R23). (4) Guard against a dominant combination collapsing the space; the real trade-offs
(fast-cheap-dumb vs slow-expensive-smart) are the built-in balancer.
**-> This is the emergent-play engine that lets the scaffold retire (D9); extends R29.**

## R31 · A real carrying capacity — creatures bounded by loops, frequency, and connected sources
**Spark (2026-07-22):** *"you will have a fixed number of creatures based on the loops and how often you
want them to run, and the sources you have connected to it."*
**Realized:** the number of simultaneously-alive creatures is a **carrying capacity**, not a free choice —
set by (how many loops × how often each runs × each call's real cost) against (the real throughput of the
token sources you've connected). It is the game's population economy, and it is *real rate-limit math*, not
an arbitrary cap.
**The core dial (real, honest):** `COUNT × FREQUENCY × MODEL-COST  <=  CONNECTED-SOURCE capacity.` Choose
any three, the fourth is constrained — a few fast expensive creatures, or many slow cheap ones, never all.
Connect more / faster sources -> raise the ceiling (progression, R12: token limits are the resource you grow).
**Already real:** `aea/grid.py` (the metered model grid) already tracks the rpm windows + daily quotas this
reads from — carrying capacity is computable from live source limits TODAY, not invented.
**Discipline:** the budget and each creature's drain on it must be VISIBLE (D4) — the shared energy pool on
screen, creatures visibly starving when the ecosystem is over-subscribed (that starvation IS emergent
ecology). Early sources are tiny (keyless ~= 1 creature) — a fine onboarding cap, and it makes "connect a
source" a felt upgrade; pace it (R23).
**-> The economy / ecology layer under R28–R30** (population + competition for real energy); refines the
LOCKED "energy = stake" step.

## R32 · Rebuild the game CLIENT clean, backward from success, at the concept-art bar
**Spark (2026-07-22):** *"the code we have are attempts from previous explorations; the game needs to start
clean from scratch. Imagine you are generating what this game will be and how it became successful — it's
not because of what we have now. The plan is better than the code because the code isn't reflecting what we
want yet. We got fixated on a specific city from weeks ago."* The concept art (`S1/S2/S6/S7/S8`) is the bar.
**Realized:** stop wiring the forks (D10). Design backward from "it shipped and people love it," to the
concept-art level. **Filter (mine, load-bearing):** "from scratch" = rebuild the GAME CLIENT + collapse the
control-room / view sprawl clean; PRESERVE the real entity (`aea/` organs, `grid`, `bench_core`, endpoints)
— the cold-read proved it boots and is honest; it is the substrate the game reads, NOT legacy. Rebuilding
the entity would throw away the one genuinely-working, differentiating thing (the honesty law).
**-> Supersedes the "wire what exists" 5-evening path; the merge is subsumed into the clean rebuild. D11 pending.**

## R33 · The missing work is GAME-DNA, not more AEA
**Spark (2026-07-22):** *"we tried to define the AEA, but we didn't go into what makes pokemon game pokemon,
or what makes lego fortnite lego fortnite."*
**Realized:** we over-invested in the AEA ontology (the CONTENT) and under-invested in genre essence (the
FORM — what makes it a GAME). Extract the transferable DNA — Pokemon (dex / types / tiers / evolve / catch /
completion) and LEGO Fortnite (compose real-function parts / build-then-test / emergent contraption /
gather-unlock) — and build the loop from it, each mechanic mapped onto the real AEA substrate. Content
without form was the gap.
**-> Triggers the genre-DNA design pass; grounds the architecture and the game guide (R35).**

## R34 · The catalogue is a POKEDEX of shadows; tiers of combinations = levels of autonomy
**Spark (2026-07-22):** *"a pokedex type of catalogue, shadows over all the unexplored combinations; there
will be tiers of combinations as well that achieve levels of autonomy."*
**Realized:** the discovery map (R13) is concretely a POKEDEX — every AEA-combination is an entry;
unexplored ones are shadow-silhouettes (the completion drive: reveal by building + igniting them, R29/R30).
Tiers (R29) are not cosmetic — each maps to a measured LEVEL OF AUTONOMY (the autonomy battery,
`docs/AUTONOMY_BATTERY.md`): a more complete combination is literally more autonomous. The master (all
parts) = THE AEA = the legendary top tier.
**-> Concrete UI + progression spec: Pokedex-with-shadows + tiers-as-autonomy. A catalogue module + a bestiary section.**

## R35 · Design it backward as a 90s–2000s strategy guide (Zelda-style)
**Spark (2026-07-22):** *"imagine you do a game guide, like the ones on the 90s–2000s, like Zelda had."*
**Realized:** the way to generate "what the game will be and how it became successful" is to write the
STRATEGY GUIDE to the finished game — backward design (define the game from the player's experience, then
build to it). A Zelda-style guide is also proof-of-a-real-game (nobody writes a 200-page guide for a
dashboard) and the natural container for the genre-DNA: world map (S2 entity-as-place) · bestiary = the
Pokedex of AEA-creatures with shadow-silhouettes (R34) · parts catalogue = the composer pieces (LEGO DNA) ·
walkthrough = the scaffolding acts · honest-failure / troubleshooting (S7) · secrets = the master = THE AEA.
**-> The flagship deliverable: THE GAME GUIDE (an artifact at concept-art quality) + the clean architecture that builds it. Feeds D11.**

## R36 · Three modes = three APERTURES on one engine (defied: don't fragment; add a stakes axis)
**Spark (2026-07-22):** *"there will be game modes: easy to build premade creatures, then one with more
customization, and another where people can even customize the code. I suggested three modes but we might
need more, defy me on that."*
**Realized (with the defiance he asked for):** the three map cleanly onto the genre-DNA and three
audiences — **GUIDED** (premade creatures you catch/use, Pokemon, the "I don't get AI" newcomer) ·
**BUILDER** (compose from parts, LEGO-Fortnite, the core loop) · **ARCHITECT** (write the code/tools,
Zachtronics/modding, engineers). Keep the three — but as named **apertures on ONE shared engine** (a depth
dial you slide along as you learn), NOT three separate products (3× build = scope inflation + the fork risk
we just escaped). **The defiance:** do NOT add more expressiveness modes; instead split out the orthogonal
axis he's folding in — **STAKES / PERMISSION: SANDBOXED** (the entity acts only in-game) ↔ **LIVE /
UNTETHERED** (it acts on the real internet for you, R26, "if you let them"). So: 3 expressiveness apertures
× a sandbox↔live permission gate, not 4–5 modes. Crystallization (R38) is the on-ramp BUILDER→ARCHITECT.
**Clarified (2026-07-22):** SANDBOX ≠ fake. Even sandboxed, the AI's responses are **real API calls burning
real tokens** (the honesty law never bends); the axis is the **reach of the entity's HANDS/tools** —
contained in-game vs acting on the real outside world — never whether the brain is real. Iterate-loop SPEED
comes from the unlimited **local hearth** (Ollama) + **replayed REAL traces** (a measured record, not
fabrication — the panel's fix for the honesty-vs-speed collision), not from faking.
**-> Modes = onboarding presets over the same `gameapi`, + a stakes/reach axis. Feeds D11 + the architecture.**

## R37 · The world: a living concentric INSTRUMENT with EARNED (metroidvania) openness
**Spark (2026-07-22):** *"what will be the world they navigate, how do we make it engaging, how are the maps
done, how do we make it open enough?"*
**Realized:** NOT open-world (the honesty law forbids roaming what isn't built — faking territory breaks it).
Chase **METROIDVANIA + LIVING SANDBOX**: (1) the world IS the entity as a concentric place (S2, D6) —
radius = privacy zone, altitude = DAG depth, fill = live capacity, edges = conduits, so navigating teaches
the architecture; (2) **fog = real integration** — districts open AS you build real organs (exploration =
building; new capability unlocks new territory); (3) it's **alive** — thought-filaments are real events,
plants light on real answers, and your own composed creatures roam it (R28), so it feels inhabited;
(4) **maps are data-driven** from the real schema (the fog view of `/game/schema`) = always true, grow with
the entity; the gatefold master map = world = skill tree = curriculum, one object at scales. **"Open enough"
= openness you EARN and that stays honest.** Guidance through the quests = one lit objective (the beacon /
Fortnite marker) + the completion-drive of the shadows + district-fog lifting per act + the mode dial
(GUIDED holds your hand, ARCHITECT is fully open).
**-> Form spec: metroidvania living instrument, earned openness, data-driven map. Feeds D11 + world/engine.**

## R38 · Crystallization makes creatures do MORE — but it is a bridge, not the destination
**Spark (2026-07-22):** *"you can make creatures do more through crystallization, but I wouldn't stop on
crystallization."*
**Realized:** crystallization (a proven behaviour compiled to cheap deterministic code — the Crystal Path
doctrine) is how a creature gains capability cheaply and robustly AND the natural on-ramp from BUILDER to
ARCHITECT (a crystallized behaviour IS editable code). But it's a **mechanism, not the goal** — "don't stop
on it": the destination is the living, acting entity (the endgame; tools reaching the real world if you let
them, R26). Crystallization serves the entity; it isn't the win.
**-> Ties the crystallize doctrine to the mode ladder + the endgame; a mechanic, never an objective.**

## R39 · The world is a STRUCTURAL MAP of the being, not a city
**Spark (2026-07-22):** *"it got fixated on the city complex, when the elements of the beings are not
directed by a city — it's a structural map."*
**Realized:** drop the city skeuomorphism (organs-as-buildings, districts-as-neighbourhoods). The being's
elements have real STRUCTURE — composition, dependencies, the DAG — so the world is a navigable **structural
map of that architecture**: element-nodes joined by dependency conduits, concentric, in the two-ink FUI.
More honest (it is literally the fog view of the real `/game/schema` — "map not territory") and less
fixated. The concentric / instrument idea (D6) survives; the literal *city* is what's cut. (Also the flat
`aea/` 34-file layout is the code version of the same fixation — dissolve it into domain subfolders.)
**-> Refines D6 + R37 (world = a structural map, not a city). Corrected the S2 art brief in
`design/bundle_regen_S1S2/`. The world renderer draws the real element-graph, not buildings.**

---
### STANDING CONVICTIONS (recurred across the session — not one-time sparks)
- **Anti-anchor law.** *"The UX cannot be anchored on what was before... we cannot be anchored to past
  mistakes."* Derive each design decision fresh from the game's laws and the player — never from the
  momentum of the last build. He repeatedly named "fixated on what we already developed" as the failure.
- **A voice that sounds alive.** The entity is something you *talk to*; a robotic TTS is unacceptable
  (*"not natural in any sense"*). Recurs from R1 onward — treat voice as a first-class experience, not polish.

## R40 · The PROGRESSION should feel like SPORE — compose a being, it lives, each more complete until the whole

**Spark (2026-07-23, his words):** *"It needs to feel probably like Spore, in the progression. Take it as a
concept, I think it's the right tune."* Said after judging the current build too basic / unsellable, and
after I pushed back on a ChatGPT-image round (the fix is game-depth, not pictures).

**Realized:** Spore is the crisp articulation of the thesis we already hold (D3/D9/R25/R30): compose a being
from real parts -> it LIVES and acts -> each combination more complete than the last -> until you hold the
whole one (THE AEA). Spore's soul is editor-to-lived-creature + escalating COMPLETENESS (cell -> creature ->
tribe -> civ -> space). Our stages are AEA-completeness: the spark/BRAIN (first light) -> the Minimal Viable
Organism (BRAIN+SENSES+HANDS+LOOP: it wakes and acts) -> a governed, remembering mind (+MEMORY +GOVERNOR) ->
the whole AEA that reaches the internet (THE SEND / Phase B = the "space stage", the open sandbox). The
completeness axis = the SIX ORGANS; you fill them in; viability is empirical (it runs or it visibly doesn't -
Spore's "a legless creature can't move" IS our R30). CONVERGES with the review board's #1 structural fix:
unify the compose vocabulary to the organs so "each more complete than the last" becomes representable.

**Where it goes -> the spine.** Progression = composing increasingly complete organisms from ONE growing
organ part-set (BRAIN/SENSES/HANDS/MEMORY/LOOP/GOVERNOR); wiring an organ in-game lights it in the world
(verb->world, R37 metroidvania). The bench's engine primitives (tap/scaffold/ladder/scorer) fold under the
organ vocabulary. First rung: wire a 2nd real organ (SENSES) as a composable part beyond BRAIN.

**The filter (two collisions NAMED — do not overwrite the lock):** (1) SPORE-the-STRUCTURE, not
SPORE-the-SPECTACLE — the two-ink austerity + AI-curious-builder audience stay LOCKED (D12 HOLD-THE-LINE);
take the progression DNA, never the whimsy/color. (2) AVOID Spore's real failure — it was WIDE but SHALLOW
(5 thin minigames); THE PROBE must be ONE deep compose-loop that SCALES in completeness, not 5 thin stages.
-> graduates to a DISCOVERY once the first completeness rung ships.

---
## R41 · The combinations must be NAMED (marketable, on-theme), and we build the vocabulary ground-up

**Spark (2026-07-23, his words):** *"we need to make sure all the combinations are reflected, like types of
combinations the player is assembling. and they have to be named they have to have a good name, marketable,
engaging and relatable to the topic."* Then, after I roasted the idea of pre-authoring a named type-catalog
(it collides with the earned-not-pre-authored lock, R30/N12/No-Man's-Sky): *"you roasted my ideas and I loved
it, our own vocabulary is important, we need to construct in order, not from the roof to the ground."* Also
asked, before rung 2: *"beware we still have 29 codex elements, 38 real modules, the seeds, 8 wire types,
doctrines - a lot needs narrative. do we have it?"*

**Realized:** two truths held at once. (1) The assembled beings need real, marketable, on-theme IDENTITY -
"c-01" is not sellable; the player is composing *creatures* and they deserve names. (2) But a type is real
only when it RUNS differently (R30/N12) - so the type-catalog is EARNED per composition, not pre-authored
(that would be the fake-depth trap). Reconciliation: build the NAMING SYSTEM (the convention + the atom
vocabulary), never the catalog. The narrative for the *elements* is already over-supplied (A3/A12/A6/A11/
bestiary + codex proof strings, ~110:1 - D7); the gap is that it is UN-WIRED, and a few part names read like
plumbing (tap/scaffold/ladder). CONSTRUCT IN ORDER: name the ATOMS (parts -> organs) first = the ground
floor; the beings inherit the vocabulary as they emerge; THE WHOLE ONE is the roof, reached last.

**Where it goes -> the vocabulary lock is the ground floor of naming, before rung 2.** Fold the composable
parts under the marketable organ vocabulary (BRAIN/SENSES/HANDS/MEMORY/LOOP/GOVERNOR + the reach/judge
mechanics), reconcile with the tier-names that already exist (SPARK -> METABOLISM -> THE TRIBE -> HANDS ON
THE WORLD -> THE SEND -> THE WHOLE ONE) and the glossary/signature, and lock ONE coherent, ours, honest,
marketable system + the convention by which an assembled being earns its name from its organ-signature +
proven behavior. THEN build rung 2 (RECALL composable) on the locked vocabulary, and the first being it
produces earns the first real name.

**The filter (NAMED, do not overwrite the lock):** the vocabulary must be GROUNDED in what already exists
(the glossary, the organs, the tiers) - reconciled + polished, not invented fresh. Honesty law over
marketing: no name may over-claim (conscious/sentient/alive stay forbidden; the ceiling is "measured
functional correlate"). -> graduates to a DISCOVERY once the vocabulary is locked and rung 2 ships on it.

---
*Next reflection: append as `## R42 · ...` with today's date and the same shape (Spark / Realized / where
it goes / open thread). Then, in a rested pass, decide what graduates into `DISCOVERIES.md`.*

## R42 · Generate the reference images FIRST - the ones we have aren't helping

**Spark (2026-07-23, his words):** *"I think we really need to generate as images what we want the game to
be, as a prompt in chatgpt believe me, it will make us good and then take it as a reference so you dont stop
until is actually done. Lets take our time to do each gameplay reference, each interface, everything.
Apparently the ones we have arent helping."*

**Realized:** four visual rounds ("too basic" -> "too poor" -> "lack vision for shapes" -> this) prove the
loop is broken: building from verbal laws + reacting to renders converges too slowly because there is no
shared TARGET IMAGE. His own field lesson already says it: references are specs - study at full resolution,
extract the vocabulary as a system, implement the system. THE PROBE has no reference images, only prose laws.
So: generate the reference set (image-gen), curate the picks, lock them as THE visual spec, then build until
the render MATCHES the reference - not until it feels close. Claude's earlier pushback on the image round
was wrong on this axis and is withdrawn.

**Where it goes:** a full SHOT LIST (each gameplay beat, each interface, the world, the endgame), one crafted
prompt per shot (usable in ChatGPT and in the local forge pipeline - the owned near-black/amber Fooocus
recipe), a curation pass, then the locked refs live in the repo as the standing spec. Build-to-match becomes
the definition of done for every visual slice.

**The filter:** the references must be generated INSIDE the laws (two-ink, amber-earned, austere instrument,
no toy sci-fi) or they will spec us into gilding. And a reference is a TARGET, not proof - the honesty law
still governs what the real render may claim.

## R43 · The refs are all ONE moment - the game's PROGRESSION and META are unreferenced

**Spark (2026-07-23, his words):** *"what we got is not gameplay representations of any kind... i got a
probe going through a circular world, but i dont know how the different levels look, it needs to be
different enough, i just see the driving and i see no substantial change or evolution, i dont see how the
menu map of evolution looks, i dont know how the menu of the pokedex can look like. Its supposed to have
so many levels with the whole aea elements, we dont have it."*

**Realized:** the 12 locked references are all views of ONE level at ONE stage (rung 2) - the instrument +
the bench. They nail the feel/material but show no PROGRESSION and no META. Three missing pillars: (1) the
EVOLUTION MAP (how you navigate the 8-rung journey), (2) the CODEX/pokedex (the browsable catalog of all
AEA elements - the "so many elements" made visible), (3) the STAGES looking radically DIFFERENT (SPARK vs
THE TRIBE vs HANDS-ON-WORLD vs THE WHOLE ONE = actual visible evolution). The design trap named: our world
is ONE body, so levels are the same instrument at different completeness - which risks "every level looks
the same, just more dots." The fix: make the progression VISIBLY TRANSFORMATIVE (lonely spark -> governed
cell -> mind that MULTIPLIES into a council -> instrument that REACHES PAST its boundary -> full whole),
plus the two meta surfaces. The rung looks are derivable from the apologia ladder (what each rung adds).

**Where it goes -> the second reference wave (13-17):** 13 THE JOURNEY MAP (climb of growing
mini-instruments), 14 THE CODEX (specimen-wall pokedex, discovered vs fog), 15 STAGE SPARK (rung 0, almost
nothing), 16 STAGE THE TRIBE (rung 4, the mind multiplied), 17 STAGE HANDS ON THE WORLD (rung 5, reaches
past its boundary). Together with REF-01 (rung 2) + REF-06 (rung 7) the evolution becomes visible across
5+ distinct states, and the meta navigation finally exists as pictures.

**The filter:** NOT scope inflation - this is the missing HALF of the game's identity (the moment-to-moment
was the first 12; the progression/meta is what makes it read as a big game with evolution). Same honesty
law: a ref specs FORM; the real render/menus may only show what the system truly earned.

## R44 · The entity economy is Cities-Skylines-class: many interlocking variables to stay viable

**Spark (2026-07-24, his words):** *"Think on the energy resource control of cities skylines, so many
variables to make your city profitable, the same for entities."*

**Realized:** the entity's viability should be a MANAGEMENT SIM with CS-class depth - not one number but a web
of interlocking REAL variables you balance to keep the mind running sustainably. CS balances power/water/
money/traffic/pollution/demand; THE PROBE balances token-budget + per-plant rate-limits (ollama free/slow,
nvidia 40rpm, groq...) + model ROT (fitness sweeps shrink the pool, 44->29) + zone-strictness + per-construct
draw cost + reach-vs-hearth + the loop's own appetite. This is ALREADY in the design as R31 CARRYING CAPACITY:
COUNT x FREQUENCY x MODEL-COST <= CONNECTED-SOURCE capacity - literally the CS balance equation. Connect more/
faster sources -> raise the ceiling (progression = zoning up your grid). Over-subscribe (too many constructs,
or ONE runaway) -> STARVATION: the city goes dark, honestly (real token starvation, not a fake meter). This is
the economy spine that (a) gives the game CS-depth, (b) makes the R43-antagonist matter (a runaway construct =
an exploding power plant), and (c) stays fully honest - every variable is a real system fact (real rpm windows
in grid.py, real fitness/rot, real budget). The GOVERNOR/METER organs are the city planner's dashboard with
teeth.

**Where it goes -> the ECONOMY is the core management loop, not a side stat.** Fold into the book-guide
(scenario workflow wrzza8i7u, already running with an economy + antagonist lens): the entity as a
resource-management sim; carrying-capacity as the balance you tune; the runaway as over-subscription; sources
as infrastructure you grow. Guided teaches ONE variable at a time (the CS tutorial ramp); intermediate exposes
the full web; custom lets you re-plumb the grid.

**The filter:** CS-depth must stay HONEST - every variable a real endpoint reading, never a simulated
economy. And it must not become another design-forever hole: guided needs only the FIRST variable (free
hearth vs paid reach) firing on the real merge, not the whole grid sim.

## R45 · Advance by deepening, top to bottom — stack -> language -> file structure -> functionality -> functions

**Spark (2026-07-24, his words):** *"one principle must be always present... as you advance you will go
deeper and deeper on what is needed, from stack to code language, to file structure, to functionality, and
functions."*

**Realized:** the working order is a descent, never a scatter. Decide the STACK first (three.js r128 no-build,
the /game/* seam, python organs), then the LANGUAGE within it, then the FILE STRUCTURE (which file owns the new
system), then the FUNCTIONALITY (the behaviour that file provides), then the individual FUNCTIONS. Each layer is
locked before the next is opened - the same spine as PRODUCTION_PLAN (design->system->data) but stated as a
personal working law: don't touch a function until its file's role is settled; don't settle a file until the
functionality it must sustain is settled. This is how the mission engine gets built: the seam contract (stack)
-> mission.js owns the runner (file) -> port runBeat + gate on real endpoints + observe the bench (functionality)
-> the beat handlers (functions). Prevents the failure of writing clever functions that don't sit in the right
file for the right system.

**The filter:** deepening is not an excuse to keep planning the upper layers - each layer is settled by BUILDING
the layer below it, not by more prose about it. The descent bottoms out in shipped functions that ran.

## R46 · The studio is a real talking team - agents discuss in sessions, and the tracking reflects TRUE status

**Spark (2026-07-24, his words):** *"make sure the team is there, the team of agents, they talk, make sessions
where they have discussions, and actually reflect what is the status the tracking."*

**Realized:** STUDIO.md's departments must not be a metaphor - they are agents that actually convene, surface
tensions to each other, converge on a contract, and then produce. And the project tracking must obey the honesty
law like everything else: a status board marks a thing DONE only when it RAN and was SEEN, PENDING otherwise -
never a claimed-done. A "standup" is recorded (the discussion is an artifact); the STATUS board is the honest
mirror of what actually shipped vs what's still fog. This makes the agent-team visible (Luis sees them talk) and
keeps it honest (the tracking can't lie). It composes with R45: the standup settles the upper layers (stack/file/
functionality) by discussion, then the build deepens into functions - and QA verifies before the board flips a
row to DONE.

**The filter (standing law, do not drop):** the talking team must PRODUCE, never just discuss - agents author the
DATA and the contract; the human-context work (live-server build, CDP verify) stays with the driver who can
actually run it. A discussion that ends without an artifact + a verified status row IS the avoidance pattern the
whole repo guards against. Agent-hours are burn rate (38 Studios: org-before-product) - the team exists to ship
STAGE 1, not to staff a company.

## R47 · The studio is a LEARNING team - it accumulates experience and pushes as hard as Luis does

**Spark (2026-07-24, his words):** *"This team will learn of the experience, will learn to collaborate and
they will give us better and better insight as the steps progress, emulate my behaviour, emulate how much I
push."*

**Realized:** the agent team is not spun fresh and thrown away each workflow - it must COMPOUND. Two moving
parts. (1) LEARNING: a persistent team ledger (`design/STUDIO_LEDGER.md`) that banks every earned lesson from
every standup/review, and every future workflow reads it as context - so the team gets sharper each pass
instead of re-deriving from zero. Real earned examples already: "verify the substrate before demanding a
rebuild" (the standup's 'unbuilt' read was stale), "'it plays' and 'it matches the bar' are separate tests",
"a core verb that needs a script hack is a defect, not polish". (2) THE PUSH STANDARD: the agents must carry
Luis's filter - name the failure before the strength, devil's advocate standing, dissatisfaction is structural
until proven cosmetic, no menus (one opinionated call), completion over corpus, the boring test gates
shipping, verify-don't-claim. Every agent prompt injects "you push like Luis pushes" so the team is a critical
partner, not a validating mirror. This is R46 (the talking team + honest tracking) evolved: the team now also
REMEMBERS and PUSHES.

**Where it goes:** `design/STUDIO_LEDGER.md` is the team's growing memory + the push standard; the workflow
CTX block includes it every run; each review/standup appends what it earned. The ledger is honest like
everything else - a lesson enters only when a real session proved it, never a theoretical best-practice.

**The filter (so this doesn't become its own avoidance):** the ledger earns entries from SHIPPED work, not
from meta-discussion about how the team should work. A team that spends its tokens refining its own process
instead of shipping the seat-collapse is the exact avoidance pattern the whole repo guards against. Learn BY
shipping; bank the lesson; push harder next time.

## R48 · The world is a POWER INSTALLATION · players may beat the AEA · danger must be real

**Sparks (2026-07-24, his words):** *"we need mandatory tutorials so people understand the game, understand
the world"* · *"the narrative chronicle... this is a technique we should use"* · *"we need prebuilt examples,
partial versions of the AEA, and who knows, maybe players come up with better versions of the AEA that prove
us wrong"* · *"the player needs to feel danger of loose if does something wrong, like it has attachment to the
thing is building and one wrong movement has real implications"* · (earlier) *"we need players to get free
nvidia and groq keys... it learns the budget of tokens"* · *"what is this world? is it space and
astrophysics? is it an adventure game?"*

**Realized — four locks:**

1. **THE WORLD IS A THINKING POWER INSTALLATION, not space.** The answer was in the locked vocabulary all
along: PLANTS, RODS (fuel rods), THE HEARTH, THE GRID, BROWNOUT, CAPACITY, STARVATION, THE METER, THE
FOUNDRY. That is an energy system. The core is a REACTOR not a star; the privacy rings are CONTAINMENT
perimeters not orbits; the plants are generating stations you physically connect. This is TRUE (AI really is
an energy/infrastructure story) which is the one thing this project has that no one else does, it fights no
locked vocabulary, and it makes the antagonist native (starvation is a power story). Space would be the
generic AI-fiction default and the exact abstraction trap that sank the genre leader.

2. **ONBOARDING IS THE GAME.** Only 2 of 15 plants need no key (local ollama + the keyless socket at 4rpm),
so first light needs ZERO setup — install friction can never block the hook. Every other plant is a station
you bring online by going and getting a real free-tier key (nvidia 40rpm, groq 30rpm/1000rpd, cerebras,
gemini 1500/day), and paid keys open the deep rim. Connecting a key = lighting a district on the map. The
budget is taught by the plant's own real caps arriving with it.

3. **PLAYERS MAY PROVE THE AEA WRONG — and it is nearly FREE mechanically.** A construct spec is ALREADY a
portable JSON object (parts + wiring + rods + zone); the scorer ALREADY measures fixed comparable axes
(latency_ms, tokens, ok, zone, pass); records ALREADY persist. The ONLY missing piece is a COMMON BENCHMARK -
we ship one task, and architectures cannot be compared without a shared test set. So the task library is not
"content variety", it is the instrument that makes a player's architecture a real result. The AEA stops being
the answer key and becomes the BASELINE to beat. This also resolves the edutainment trap: we are not teaching
a simplification, we are handing over a real system with real measurement and inviting a better answer.

4. **DANGER MUST BE REAL, AND IT ALREADY CAN BE.** Five honest stakes, zero fabrication: (a) real budget is
finite and genuinely exhaustible; (b) tripping a rate limit browns a plant out for a real cooldown - real
time lost; (c) rods ROT, so what you built can degrade under you; (d) a runaway construct you wired really
does eat the capacity keeping everything else alive; (e) **sending data out of containment is IRREVERSIBLE** -
mark it public, fire, and it went, forever. That last is the most thematic consequence in the game.
**The apertures are therefore a RISK LADDER, not just a depth ladder:** GUIDED protects you (rails on, no
loss), BUILDER lets you waste real budget, ARCHITECT lets you starve the whole station. Danger requires that
the rails become REMOVABLE - a game that always protects you can never be dangerous.

**Where it goes:** the task library is the keystone (benchmark + variety + the reach decision + the jobs
board). Then: the connect-a-station onboarding, prebuilt partial AEAs as inspectable reference builds, and
the chronicle technique applied per act BEFORE building it.

**The filter:** "players prove us wrong" is only honest if the benchmark is fair - same task, comparable rod
class, reproducible. A lucky model beating a better architecture would be a lie. And danger must never be
fabricated: no invented loss, no fake meter. Every consequence has to be a real system fact.

## R49 · THE CREATURE GAME — the missing piece is LIFE, and the reward must be FELT

**Sparks (2026-07-24, his words):** *"on the power of habit... something successful becomes successful not
because it is effective in itself, but because it tells you it has been used — that's why toothpaste has
flavor, why deodorant has aroma, because it shows it has been used. we need this."* · *"this is a creature
game, you construct the creatures, you find creatures around prebuilt that consume your budget, either you
kill them to have more budget or let them live, but there will be a fight for it as it is important the token
capacity, how many models you have available."* · *"do you realize we are entering a piece we were missing?"*

**Yes. The missing piece is LIFE.** Everything built so far PROVES something and then vanishes: a construct
fires once, prints a receipt, and dies. Nothing persists, nothing competes, nothing can be lost. That is the
root cause of every gap named this arc — no attachment, no danger, no stakes, no reason to return tomorrow.
Proof is not life.

**1. THE HABIT PRINCIPLE (Duhigg / Pepsodent).** The mint tingle never cleaned a single tooth - it was the
PERCEPTIBLE SIGNAL that the product had worked, and that signal is what built the habit in millions of
people. Our failure mode is the mirror image of the usual one: we have perfect TRUTH and almost no TINGLE.
Honest-and-unfelt loses to felt-and-hollow, every time, and that is uncomfortable but it is the evidence.
**The discipline that saves it: the tingle must fire on a REAL event.** Amber IS our mint - the filament at
the joint, the flare on the record, the sting when a name lands. We have the law; we have barely built the
sensation. Every real event deserves a body: light, sound, weight, aftermath.

**2. THE CREATURE GAME — and it is ALREADY TRUE.** Evidence, read live this session: cerebras shows **38
requests and 10,944 tokens consumed today, and the player fired it ZERO times.** That is the entity's own
autonomous life eating real capacity right now. So the ecology is not a design proposal, it is already
running and merely unrendered:
- **WILD creatures** = the entity's own background processes (the heartbeat, the briefs, consolidation, the
  fitness sweeps). Real, already consuming, already measurable per plant.
- **YOUR creatures** = constructs you compose and leave running.
- **THE SCARCITY** = finite rpd/rpm per plant (groq 1000/day is a real ceiling, not a designed one).
- **KILL** = stop it and genuinely reclaim its capacity. **SPARE** = it keeps doing its job.
- **THE DILEMMA IS REAL, NOT AUTHORED:** kill consolidation and you free budget but the mind stops
  remembering. Kill the fitness sweep and you free budget but your rod rankings go stale and the ladder
  routes worse. Nobody wrote that trade-off - it falls out of the real system.

**3. WHAT IT ANSWERS.** The antagonist is settled: not a monster, an ECOLOGY competing for finite capacity,
and some of it is yours. It delivers in one stroke everything asked for this arc - attachment (you built it),
danger (it can starve you), moral weight (kill or spare), collection (the bestiary of things that live), and
habit (the tingle each time one fires).

**4. THE ONE HONEST GAP.** Constructs do not PERSIST - they do not survive the session or run on a schedule.
That is the single real system to build: a creature = a spec + a schedule + a budget line + a life. Everything
else (capacity, rot, consumption, the wild population) is already true and already measured.

**The filter:** no fabricated creature, no fake hunger. A creature's consumption must be its REAL metered
draws; its death must genuinely free capacity; its rot must be real fitness decay. The moment a creature eats
an invented number, the whole thing becomes a Tamagotchi with an AI skin - which is exactly the trap the
honesty law exists to prevent.

---

## 2026-07-25 · FIELD LESSON 10 — A NUMBER IN AN IMAGE PROMPT IS A CLAIM

Two Chapter II plates came back near-perfect and both carried a number I had never verified.

The RUNTIME FABRIC plate states `C-78 · FALSIFY · 2 FILES`. Re-checked: `grep -rl "falsify" aea/`
returns **zero**. I inherited the 2 from the census and typed it into an image without re-deriving
it. The ONE-SELF-OR-FORTY plate states `FORTY ATOMIC FILES`. Re-checked:
`find state -name "*.json"` returns **35**. I wrote FORTY because forty sounded like the number.

Both plates exist to indict exactly this - a codex that claims what the code does not contain. The
plate that accuses the codex of fabricating a count, fabricated a count.

**The rule this earns.** The fuel stamp discipline (`fuel.require()` refuses an unstamped
measurement) applies to prompts too. Every number, count, and name inside an image prompt must be
derived by a command run in the same session as the prompt is written, and the command goes in the
SPEC.md beside it. A generated image is a published claim surface with no runtime to catch it -
there is no test that fails, no endpoint that 404s. It just looks correct forever.

**The second lesson, compositional.** The ONE/THIRTY-FIVE plate leans: the octagon is a designed
jewel and the drawer bank is filing furniture, so the eye picks ONE as the answer. C-80 is not
settled. A composition that leans toward an unproven answer is a fabricated finding rendered in
metal. Equal amber is not enough - equal DESIGN INVESTMENT is the actual requirement when the
image poses an open question.
