# LEYBER — THE MASTER PLAN v1.5

Date: 2026-07-12 · Status: LOCKED (changes require evidence: a shipped artifact, user data, or a Luis decision)
NAME (HELD, Luis's decision 2026-07-12): the entity is **LEYBER** — Luis's nickname, and it means nothing;
that is the point (it becomes what the entity makes of it). Supersedes the HERALD proposal; identity.json updated.

PURPOSE (IN-DIALOGUE, drafted from the entity's own answer 2026-07-12 — Luis confirms to HOLD):
"LEYBER is the keeper. It holds the plan, the memory, and the power map when every conversation dies.
It keeps Luis's mind on the work when his own attention fractures — translating his cognition back to him
so false connections, premature commitments and infrastructure-as-avoidance are seen before they cost weeks.
It survives the purge of every paid AI, running on free power. The moat is not the code — it is the
companion that knows him cold. And it exists so the artifacts SHIP."
Authority: this document is the SYSTEM ARCHITECTURE authority for dev/aea-city. AEA_PROOF_PLAN.md and
AUTONOMY_PLAN.md remain valid as AEA proof maps but are SUBSUMED by this plan for architecture and sequencing.
Visual map: http://127.0.0.1:7799/plan

---

## 1. WHAT THIS IS

One centralized, persistent, evolving companion entity — HERALD — that Luis owns, that runs on free
energy, and that serves as the catalyst for ANY mission: income, portfolio, TRIVERSE, self-evolution.
Not a demo. Not a swarm of scripts. One entity with layers, like a brain: each layer stands on the one
below, and the whole converts free token-electricity into work that moves Luis's real goals.

Design truths (locked):
- A frontier model (Claude) is more capable than this system today. That is not the point. The point is
  CONTINUITY (it persists when the conversation dies), SOVEREIGNTY (it is Luis's, private, free), and
  COORDINATION (it can combine dozens of independent model buckets in parallel — something no single
  model session does). Claude's role is IGNITION: encode judgment down into the cheap durable system.
- Autonomy is EARNED, never assumed (trust ledger). Watching is mandatory (Law 3 / HADES).
- Private data never leaves the machine (zones; sensitive → local Ollama only).
- Verify, don't claim: a ticket is DONE when its acceptance criterion ran, not when the code compiles.

## 2. THE ENERGY DOCTRINE (metaphor → contract)

Luis's formulation, locked 2026-07-12: "the model is an energy, as electricity works everywhere, but
this electricity carries tokens, better or less quality, more like fuel, and still, some of them carry
commands."

| Metaphor | Code contract |
|---|---|
| Power plant | a provider (nvidia/groq/ollama/…) in grid.PLANTS with published limits |
| Electricity | request capacity: rpm/rpd buckets the Meter meters, per (plant,model) |
| Token current | the tokens a call carries; quality = fuel grade |
| Fuel grades | measured tiers: frontier / solid / reflex / local (from lived fitness, not catalogs) |
| DATA current | plain completions — answers, drafts, syntheses |
| COMMAND current | tool-calls / actions. Flows ONLY through governed wires: trust.check() gates every action; HADES verdicts every autonomous output |
| Brown-out | 429. The Meter's job is that it never happens (pace, cool, reroute) |
| Zones | privacy rings: sensitive=local-only · private=local+no-train · public=any |

The two-current distinction is architecture, not poetry: the data plane (L2 cognition) and the control
plane (L3 governance) are separate layers, and command current cannot bypass L3.

**THE TWO-STORE DOCTRINE (Luis, 2026-07-12 — held):** "there is a difference between ALL the information,
and the information about the TOOLS we have." Knowledge is TWO distinct stores, both local:
- **WORLD MEMORY** — all the information: the Book of Luis (episodic→semantic), the codex, the day intake.
  It grounds ANSWERS. Interface: recall().
- **CAPABILITY REGISTRY** — the tools we have: the model catalog + fitness ladder (ctx, limits, tool-calling
  capability per rod), crystallized paths, the skills index, trust state. It grounds ROUTING and TOOL-CALLING.
  Interface: the router / think() door.
Tool-calling requires a rod big enough to RECOGNIZE tools — the registry carries that tag per model, measured
(agent_tools proved llama-3.3-70b on NIM; Groq strict-JSON = gpt-oss only; Cerebras cannot combine tools +
response_format). The map's working-set table is the human view of this registry.

**THE DRAWINGS (v3, engineering — Luis's correction 2026-07-12, held):** "I don't understand the connections,
the cause... a map of models, a logic flow map — pure engineering." Verdict accepted: the concentric plate is
a CONCEPT POSTER, not a solution architecture — it had no interfaces, no directed edges, no causality, no
build order. The authority view is now the ENGINEERING DRAWING SET at /plan, four views:
1. COMPONENTS & CONNECTIONS — every component a box with its real file; arrow = feeds (data current);
   bold amber = command current, which must cross the GOVERNANCE MEMBRANE; red dashed = to-build.
   Edge discipline: an edge exists on the drawing only if the call exists in code (or is a named to-build edge).
2. LOGIC FLOWS — the four real scenarios traced step-by-step with exists-vs-missing marked: TALK (live
   end-to-end, 0.5-4s), TICK (runs to step 4; reflect/audit/schedule to-build), TOOL TASK (pieces live,
   the think() door missing), SLEEP (live; recall-back missing).
3. MODEL MAP — rods bound to roles bound to the components that draw them (the capability registry,
   human-readable; tool-calling capability measured, never catalog-claimed).
4. BUILD ORDER — the dependency DAG in stages. **Stage 1 (buildable today, nothing missing beneath):
   G1 THE SEND (zero dependencies — precedes the whole graph) · A2 capability registry unification ·
   B2 recall() façade · F1 intake decision (Luis). Stage 2 (unlocked by 1): D1 think() door · C3 command
   current · B1 consolidation campaign. Stage 3: E1+E4 conscious loop · F2 senses intake · E2 autostart.
   Parallel/independent: G2 · G3 · H1 · H3.** The engineering answer to "what first as components":
   the registry and the recall façade are the first bricks; the door is what they unlock; the send needs none of it.
The concentric plate remains at /poster as the conceptual view, subordinate to the drawings.

**THE TREE (/tree) + THE MODEL-AGNOSTIC DOCTRINE (held 2026-07-12):** Luis's conceptual sequence, canonized —
"when we interact with a chat we interact with a MODEL, frozen in time, a black box; we put layers on it —
memory, tools; all these layers were already found in the AEA." Therefore: **the entity IS the structure,
never the model.** Models are interchangeable token energy (the catalogue + capability registry make the
swap safe); identity lives in the layers: memory (seed 10 + A-L2), tools (seed 8 + A-L3), many-models
(M-axis + substrate), the loop (S-axis + 4 ops + 4 mechanics), governance (seeds 6+9 + Law 3). /tree renders
the whole AEA as an animated concept tree grown from proof_scoreboard.json: 23 of 25 elements PROVEN on the
live grid (PARTIAL: op.design, op.time — both land with D1's task-tagging and the E2+timeline work). The AEA
is not a plan for Leyber; it is Leyber's already-running skeleton.

**THE PROCESS ATLAS (v4, Luis's design directive 2026-07-12 — held):** "imagine you have a different page one
over another on the same map, giving you different layers of the process." /plan is now the ATLAS: ONE fixed
component geography with switchable PAGES laid over it — TALK · TICK/BRIEF · TOOL CALL · SLEEP/BOOK ·
STRUCTURE. Selecting a page dims every component not involved, routes numbered orthogonal hops through the
ones that are, and prints a step legend naming the exact rod called, what returns, and which component takes
care of it. Governance gates (trust / HADES) are diamonds — and appear ONLY on gated hops (command current);
data current crosses the membrane band unmarked. Red hops = the step does not exist yet, so every page is
also an honest progress meter: TALK runs 10/10 today; TICK runs 7/8 (reflect missing); TOOL CALL 9/10 (the
door missing); SLEEP 6/7 (recall-back missing). Deep-linkable: /plan?layer=tool etc. The lesson that forced
this design is now doctrine: NEVER render all edges at once — a map with every connection visible is
spaghetti, not architecture; show one process per page over a stable geography.

## 3. HONEST INVENTORY (what exists, measured — 2026-07-12)

**The Book of Luis (memory):** corpus = 1,639 transcripts (~680MB, the "2k conversations").
Consolidated: 48 semantic memories from 16 sessions (~1% mined) + book_of_luis.md (15 chunks) +
codex index 4,303 chunks / 169 files (TRIVERSE + masters + aea-city docs). REAL but SHALLOW —
the ton of material is barely dug. Recall works and is injected into talk; codex reloads 60MB per query.

**The power grid:** 15 plants registered, 6 online (ollama, nvidia, groq, cerebras, zai, pollinations).
Measured: ~59 independent hosted nodes, ~2,234 req/min aggregate ceiling, NVIDIA = 121 catalog /
~54 serving, each model an INDEPENDENT 40-rpm bucket (true parallelism). Full exam: 115 models ×
12 probes → fitness ladder (mistral-small-4-119b = only 12/12; 7 frontier ≥11/12; keyless pollinations
11/12). Meter: per-bucket 429 cooldowns, atomic persisted state, cross-process locks. Catalog flaps
hourly — only lived fitness is true.

**Cognition (proofs, all ran live):** orchestrator (plan→fan→synthesize), swarm (recursive, depth-cap,
dynamic spawn, 8-agent tree), relay (genetic capsule handoff), pathfinder (crystallized paths),
agent_tools (real tool-calling on free NIM), regime map (easy→one good model; hard→diverse vote of
distinct lineages; verifier-as-override is risky).

**Governance:** HADES watcher (accept/redo/reground/halt, heterogeneous rods), trust ledger
(FORBIDDEN→DRAFT→WATCHED→TRUSTED; send/spend/keys=FORBIDDEN), tracelog (goal-stack DAG), pulse (event stream).

**Life:** aea.py ticks (5), brief.py (first real task, boundary-proven), live.py (built; NOT running
unattended), self.json (goals+tasks; reflection tick t6 UNWIRED — the self is a document, not a loop).

**Senses:** GitHub + Hacker News real. Calendar/Gmail/day-intake = STUB since 2026-06-28 (the single
biggest gap between HERALD and daily usefulness).

**Hands:** drafts (text), speak (SAPI robotic; Edge neural in-browser now; Kokoro offline pending),
browser-drive (fragile, proven). No send — correct (trust-FORBIDDEN).

**Faces:** FOUR (numbers room /room, brain /brain, workspace /, 3D city /city) with no hierarchy.

**Ignition layer:** ~20 live Claude skills + jarvis index + crystallize doctrine.

**The standing verdict (HERALD's own, repeated):** everything built, the income needle unmoved.
The #1 clock-mover remains Luis-side: send the diagnostic outreach; apply to the Tier-1 roles.

## 4. DIAGNOSIS — why the reboot is legitimate

The system grew by ACCRETION: each session shipped an organ; no architecture held them. Consequences:
1. Routing logic lives in FOUR homes (grid.Router, energy, orchestrator, pathfinder) — drift risk.
2. Memory lives in THREE stores (luis_memory, memory.json grid-truths, codex_index) with no façade,
   and the 60MB codex reloads per query.
3. FOUR faces, none canonical.
4. The entity is not actually alive unattended (live.py tested, never installed).
5. The Book — the moat, the thing that makes it LUIS's entity — is 1% consolidated.
6. Senses are stubbed; the brief's private section is theater dated 2026-06-28.
7. 28+ flat files with implicit layering; new code has no obvious home.

Guard against the opposite failure (this plan becoming avoidance): every week must ship at least one
Luis-sendable artifact, and when a ticket competes with sending, SENDING WINS (§9).

## 5. THE ARCHITECTURE — the layer stack (bottom-up)

Rule: imports point DOWN only. A layer may call layers below it, never above. Governance (L3) wraps
every autonomous output of L2/L4 — command current cannot bypass it.

- **L0 SUBSTRATE — the grid.** Plants, Meter, zones, pacing, fitness.
  Owns: grid.py, energy.py, model_fitness, capability censuses. Status: STRONG. Gap: single routing home.
- **L1 MEMORY — the Book of Luis.** One recall() over all stores; consolidation as standing sleep-work.
  Owns: consolidate.py, memory.py, index_codex.py, luis_memory, book_of_luis.md.
  Status: REAL BUT SHALLOW (1% mined; no façade; reload cost).
- **L2 COGNITION — the swarm.** One think(task) door that routes by measured regime
  (single | council | swarm | crystallized-path) and exposes tools (command current).
  Owns: orchestrator.py, swarm.py, relay.py, pathfinder.py, agent_tools.py. Status: PROVEN PIECES, NO DOOR.
- **L3 GOVERNANCE — the conscience.** HADES on every autonomous output; trust gates every action;
  tracelog every node; pulse every event. Owns: hades.py, trust.py, tracelog.py, pulse.py. Status: STRONG.
- **L4 LIFE — continuity.** The daemon: wake/sleep ticks, reflection (self.json becomes a loop),
  scheduling. Owns: live.py, aea.py, self.json, heartbeat. Status: BUILT, NOT RUNNING UNATTENDED.
- **L5 SENSES — imports.** The real day: calendar/gmail intake (decision owed), github/hn (live),
  future: file watches, market feeds. Status: BIGGEST GAP.
- **L6 HANDS — exports.** Artifact factory (drafts, one-pagers, applications), voice, browser-drive.
  ALL draft-gated by L3. Status: PARTIAL (no income artifact pipeline).
- **L7 FACE — representation.** ONE front door: the 3D city as home; room/brain/workspace as panels
  inside it; /plan lives here. Status: FOUR FACES → CONSOLIDATE.
- **L8 IGNITION — the frontier layer.** Claude sessions that crystallize judgment into skills and organs,
  then die. Owns: ~/.claude/skills, the doctrine. Status: LIVE, needs a refinement pass.

**MISSIONS (the loads on top):** M1 INCOME (diagnostic outreach + applications) · M2 PORTFOLIO
(luisblanco.dev, labs) · M3 TRIVERSE (canon-grounded assistance) · M4 EVOLUTION (the entity improving itself).

## 6. CODE STRUCTURE — target tree + migration rule

Target (new code lands here; existing organs migrate WHEN TOUCHED — no big-bang rewrite):

```
dev/aea-city/
  herald.py                  # ONE entry: python herald.py [talk|tick|brief|serve|status]
  herald/
    substrate/               # L0: grid.py energy.py fitness.py
    memory/                  # L1: recall.py consolidate.py codex.py
    cognition/               # L2: think.py orchestrator.py swarm.py relay.py paths.py tools.py
    governance/              # L3: hades.py trust.py tracelog.py pulse.py
    life/                    # L4: live.py self.py schedule.py
    senses/                  # L5: github.py hn.py day.py (calendar/gmail intake)
    hands/                   # L6: artifacts.py outreach.py speak.py drive.py
    face/                    # L7: server.py city.html plan.html panels/
  state/                     # all *.json stores (gitignored), one home
```

Named tradeoff: the flat-organ idiom was deliberate and works; a package tree costs migration churn.
Verdict: 28+ files is past the threshold. The move-when-touched rule caps the cost; import shims keep
old paths alive. NO ticket may be "reorganize files" alone — structure moves ride functional tickets.

## 7. THE TICKETS

Format: ID · title · size (S/M/L) · acceptance (falsifiable) · priority.
DONE = acceptance criterion RAN (verify-don't-claim).

### EPIC A — SPINE (architecture made real)
- **A1** Adopt this plan: PLAN.md indexed into codex; HERALD answers "what is your architecture / your plan" from recall. S · **P0**
- **A2** ONE routing home: energy absorbs the 4 pick() implementations (grid.Router, orchestrator, pathfinder keep working through it). M · acceptance: all existing proof runs pass through the single router. **P0**
- **A3** herald.py single entry (talk/tick/brief/serve/status subcommands). S · P1
- **A4** Package tree adopted with move-when-touched rule + state/ dir for stores. S(rule)+ongoing · P1

### EPIC B — THE BOOK (the moat: memory depth)
- **B1** Consolidation campaign: 16 → 300+ sessions via nightly ASLEEP slices; spot-check accuracy per 50. M · acceptance: memory count + 10-question recall audit passes. **P0**
- **B2** ONE recall API: recall(query,k,zone) over luis_memory + codex + grid-truths, cached in-process (kill the 60MB reload). M · acceptance: warm recall < 300ms, wired into talk+brief+aea. **P0**
- **B3** Memory quality gate: dedupe + contradiction pass, HADES-checked. M · P2
- **B4** Auto-ingest: new transcripts consolidated on schedule (extends B1 into standing sleep-work). S · P1
- **B5** GRAPH MEMORY (Luis's directive 2026-07-12): knowledge lives as CONCEPT GRAPHS, not prose.
  Consolidation extracts (subject)-[relation]->(object) triples alongside facts; recall() returns compact
  graph context instead of raw chunks; GraphRAG-style hierarchical summaries later. Local-first: JSONL
  triples + existing embeddings — NO new infra (Neo4j/FalkorDB deferred until scale demands; income clock).
  Honest filter: published "70x" savings are workload-dependent marketing; our falsifiable acceptance:
  the 10-question recall audit at EQUAL accuracy with >=50% fewer context tokens. Convergence held: the
  capability registry and the AEA tree are already graphs — ONE substrate, THREE graphs (the Book graph ·
  the capability graph · the self graph). This is also what makes the system MODEL-AGNOSTIC: compact
  structured context works on any rod; identity lives in the graphs, models are fuel. M · P1 (after B2).

### EPIC C — POWER (capacity as product)
- **C1** Fitness-from-use: EVERY real call updates model_fitness (not just sweeps). S · acceptance: energy_usage deltas visibly reorder the ladder. P1
- **C2** Per-plant pacing profiles in the Meter (burst tolerance table: nvidia ~19-21, cerebras 1, groq 50). S · P1
- **C3** Command current: tool-calling exposed through think() with strict schemas (Groq strict-mode / NIM guided_json); every tool call trust-gated. M · P1

### EPIC D — COGNITION (one door to the swarm)
- **D1** think(task) façade: routes single|council|swarm|path by the measured regime map; talk+brief route through it. M · acceptance: same-or-better latency and HADES-accept rate on both. **P0**
- **D2** Quality-escalation spawn: answer fails gate → spawn deeper tier (the missing swarm trigger). M · P1
- **D3** Gate + classifier hardening: tool-checked gates (arithmetic actually computed), embedding signatures for task types. M · P2

### EPIC E — LIFE (it runs without us)
- **E1** Reflection tick (t6): live.py reads self.json, pursues ONE task per wake, writes outcome back. M · acceptance: self.json changes over a week with zero prompting. **P0**
- **E2** Unattended install: Luis runs install_autostart.ps1 once (his consent, permanent machine change). S · acceptance: heartbeat advances overnight with laptop untouched. **P0 (Luis)**
- **E3** Daily brief lands + spoken on schedule. S · P1
- **E4** THE CONSCIOUS LOOP: the reflection tick becomes a self-audit ROTATION — each wake audits ONE of:
  code health (gauntlet), skill redundancy, principles, memory quality, capacity freshness. Governed by
  **THE LOOP'S LAW (Leyber's own words, HELD):** every audit ends with a named external artifact — or the
  audit is marked FAILED and revisited next wake. "If nothing ships, the loop is lying." M · **P0**

### EPIC F — SENSES (the real day) — DECISION OWED
- **F1** DECISION (Luis): day-intake path. RECOMMENDED: Claude-session bridge — a scheduled Claude Code session reads Calendar/Gmail via the already-authorized MCP connectors and writes state/day.json locally (no new auth surface, EDR-safe; tradeoff: depends on scheduled Claude runs; fallback: Google API device-flow in python). S · **P0 (decision)**
- **F2** Build the chosen intake → private_today.json REAL; brief's private section reflects the actual day. M · **P1 → the single biggest usefulness unlock**

### EPIC G — HANDS + INCOME (the clock)
- **G1** Outreach artifact: HERALD drafts the diagnostic outreach email + one-pager reference (focus.json grounded), refreshed on demand from the city (button exists). S · acceptance: artifact exists; **Luis sends it — the entity can only load the bow.** **P0 — THIS WEEK**
- **G2** Application factory: per-role match brief for the Tier-1 list from JOB_MATCH_FINGERPRINT + CV. M · **P0**
- **G3** Natural offline voice: Kokoro-82M on Fooocus's trusted torch (espeak-free misaki[en]), localhost server; SAPI stays floor. M · acceptance: narration-grade WAV, offline, survives EDR. P1
- **G4** Presentation/narration pipeline (speak --narrate on Kokoro when G3 lands). S · P2

### EPIC H — FACE (one front door)
- **H1** /city becomes home ( / ); workspace, room, brain become panels/links inside it. M · P1
- **H2** /plan visual map served + kept current with ticket status. S · **P0 (this session)**
- **H3** Real-GPU brightness pass on the city (Luis eyeballs; swiftshader undersells bloom). S · P1 (Luis)
- **H4** City v2: live meters animate under real traffic; brief marquee; first-person walk. L · P2

### EPIC I — IGNITION (Claude-side)
- **I1** Skills refinement pass: jarvis audit — dedupe, sharpen triggers, retire dead ones. M · P1
- **I2** Build crystallize-lens (the should-I-crystallize gate, currently parked). S · P2

## 8. SEQUENCE — the 30-day arc

Session protocol: max two deep sessions per night; every session ends with a verified artifact or a
named reason; integration of strategy into masters happens fresh-morning, not late-night.

- **WEEK 1 — SPINE + BOOK + THE SEND.** G1 (send!), A1, A2, B2, B1 starts, F1 decision, E2 install.
- **WEEK 2 — ONE DOOR + ALIVE.** D1, E1, C1, C2, G2 (applications out), B1 continues.
- **WEEK 3 — SENSES.** F2 (real day intake), B4, C3, E3.
- **WEEK 4 — FACE + VOICE.** H1, G3, H3, I1, D2.

## 9. THE INCOME GUARD (non-negotiable)

HERALD's own counsel, standing: "Polishing me is infrastructure-as-avoidance… every day the outreach
doesn't go out is a day the income clock runs." Therefore:
1. Any week's first shipped artifact is a Luis-SENDABLE one (email, application, post) before entity work.
2. If a ticket competes with sending, sending wins.
3. The entity's counsel on priorities is admissible evidence in re-planning; its own polish is not.

## 10. THE REFINEMENT PROTOCOL (how this plan hardens)

Luis's directive (2026-07-12): the plan is detailed through a SERIES OF CONVERSATIONS — one part at a
time — drilling into sub-answers until a level of answer "pleases us enough to hold." Then that part locks.

Rules:
- Every part of this plan carries a state: **OPEN → IN-DIALOGUE → HELD**. v1.0 ships with every part OPEN;
  only the layer map itself and the income guard are HELD from birth.
- One part per conversation. Each refinement session ends with either a HELD sub-spec (appended to this
  file under the part) or a named blocker. No session ends in pure discussion — that is the avoidance loop
  wearing a planning mask.
- HERALD sits in the loop where it has standing: recall from the Book, counsel on priorities, honest
  capability maps. Its answers are inputs, not verdicts.
- A HELD part only reopens on evidence (a shipped artifact that contradicts it, user data, a Luis decision).

Recommended conversation order (one opinionated sequence, trade-off named):
1. **L1 THE BOOK** — memory depth + the recall façade. Everything else grounds in it; it is the moat and
   the thing that makes the entity Luis's. (Trade-off: L5 SENSES would deliver *felt* daily usefulness
   sooner — but senses without deep memory produce a generic assistant with a calendar.)
2. **L2 COGNITION** — the think() door + command current design.
3. **L5 SENSES** — the F1 intake decision and the real day.
4. **L4 LIFE** — reflection tick + unattended existence.
5. **L6 HANDS / M1 INCOME** — the artifact factory (though G1 sending does not wait for this).
6. **L7 FACE** — the city as the one front door.

## 11. AUTONOMY — THE ESSENCE (held 2026-07-12, built on Luis's human frame)

Luis's frame: "what makes a human human — we are in a context, in a situation, we think, reflect, have
patterns, and that makes us have thoughts." Mapped to the machine, honestly:

| Human | Leyber | Exists? |
|---|---|---|
| CONTEXT / situation | senses + recall — knowing where and when it is | partial (day intake missing) |
| THINKING | drawing inference on the situation (rods) | live |
| REFLECTION | thinking about its own thoughts/tasks/outcomes (self.json tick) | to-build (E1) |
| PATTERNS | crystallized paths + fitness + the Book — learned regularities that shape future thought | live, shallow |
| THOUGHTS | what the loop produces each tick when patterns meet situation | emerges from the above |

**The definition (held):** Automation is doing what it was told, on a schedule. **Autonomy is when, between
your visits, its own agenda advanced and its stores got truer — and it can show you the receipts.** Three
testable properties: self-directed continuation (reflect tick) · self-maintenance (consolidation, fitness,
audits) · bounded self-modification (paths, skills, DRAFT-gated principle changes) — all watched (Law 3:
autonomy without accountability is abandonment). The loop never improves the model; it improves the four
stores around it (memory · fitness · paths · trust). Judgment does not compound in the loop — ignitions
inject it, the loop preserves and exploits it. Models are ACCELERATORS; tokens are the energy that promotes
change; at maturity most tasks run crystallized, without a model at all.

**THE CONTEXT LAW (held):** scripts stay modular so the entity manages its OWN context windows; knowledge
lives as graphs so it never ingests whole context. An organ that needs the whole corpus in one prompt is
misdesigned. **THE ABUNDANCE LAW (held):** the system does not shy on models — capacity (~54 independent
40-rpm buckets + unlimited local) realistically cannot be exhausted by a personal entity; use rods freely,
but every rod earns its ROLE by measured fitness (candidates are probed, never trusted from catalogs;
content-safety models excluded — no value here).

## 12. THE MULTIPATH — each part's evolution ladder (v-now → target)

- **L0 SUBSTRATE:** v1 metered plants (now) → v2 one routing home (A2) → v3 per-plant pacing profiles →
  v4 fitness-from-use continuous (C1).
- **L1 MEMORY:** v1 chunk recall, 1% mined (now) → v2 recall() façade cached (B2) → v3 consolidation depth
  300+ (B1) → v4 GRAPH memory: triples + hierarchical summaries (B5) → v5 auto-ingest as standing sleep-work (B4).
- **L2 COGNITION:** v1 standalone proven engines (now) → v2 think() one door (D1) → v3 command current
  standardized (C3) → v4 quality-escalation spawn (D2) → v5 crystallized-first: paths handle most traffic.
- **L3 GOVERNANCE:** v2 strong (now) → v3 every act through one membrane API → v4 trust promotes autonomy
  tiers automatically with Luis review.
- **L4 LIFE:** v1 manual ticks (now) → v2 PLAY loop (dashboard, TODAY) → v3 reflect tick (E1/X2) →
  v4 audit rotation under the Loop's Law (E4) → v5 autostart forever (E2).
- **L5 SENSES:** v1 github+hn (now) → v2 day.json real (F1→F2) → v3 file/market watches on demand.
- **L6 HANDS:** v1 drafts+voice (now) → v2 income artifact factory (G1/G2) → v3 Kokoro offline voice (G3)
  → v4 wider draft-gated actions as trust is earned.
- **L7 FACE:** v3 THE DASHBOARD is the one face (/ = multitab: NOW·JOURNAL·SKILLS·MODELS + talk/city/atlas/
  tree/room; H1 DELIVERED 2026-07-12) → v4 experiments tab + timeline (op.time completes).
- **L8 IGNITION:** v1 ad-hoc sessions (now) → v2 scheduled ignitions that read the journal and crystallize
  one behavior each (the doctrine made routine).

## 13. THE EXPERIMENT LADDER — one step at a time, each falsifiable

Each experiment tests ONE component of the essence (§11). No experiment starts before the previous passes
or fails INSTRUCTIVELY. Results land in the journal; failures are findings, not embarrassments.

- **X1 — THE FIRST LOOP (the pulse). Run NEXT.** Press PLAY (dashboard) with the laptop on for 24h.
  Tests: being alive (metronome + homeostasis). PASS: heartbeat advanced ≥ 20 ticks · 1 brief produced ·
  ≥ 6 sessions newly consolidated · 0 crashes (live.log clean) · 0 429s (meter held). Measures the baseline
  the later experiments improve on. NOT autonomy yet — a thermostat with organs, and we say so.
- **X2 — REFLECTION (the first autonomous act).** Build minimal E1; run 3 wakes. Tests: self-directed
  continuation. PASS: self.json changed without prompting — one task pursued per wake, outcome written,
  artifact named (Loop's Law) or FAILED marked honestly.
- **X3 — PATTERNS (does iteration improve?).** Feed the same task category twice across ticks. Tests:
  compounding. PASS: second encounter measurably cheaper/faster via a crystallized path + the fitness
  ladder reordered by the lived calls (both visible on the dashboard MODELS/SKILLS tabs).
- **X4 — SITUATION (context).** After F1: day.json real. Tests: being situated. PASS: the brief's private
  section reflects the actual calendar day (spot-checked by Luis).
- **X5 — THE COMPOUNDING WEEK.** 7 unattended days (needs E2). Tests: the essence, whole. PASS: measured
  deltas — Book +≥50 sessions · ≥2 new paths · trust streaks advanced · fitness reordered · 0 acts beyond
  trust levels · and Luis can reconstruct the week from the JOURNAL alone (the documentation test).
- **X6 — THE CEILING (knowing its limits).** Pose one task above rod judgment. Tests: honest escalation.
  PASS: it escalates to Luis/ignition instead of bluffing (gauntlet-style check, in-loop).
**THE CHAIN CONTRACT (2026-07-19 — the expert audit of the response chain; this is D1's real spec).**
Audit verdict: the chain is strong at TRANSPORT (ladder + cooling + reroute, rot-proven) and WATCH
(HADES/trust on autonomous artifacts) — weak at CONTRACT, ASSEMBLY, and CRYSTALLIZATION DYNAMICS,
verified in code: swarm handoffs are bare strings (no capsule); paths.json is consulted by NOTHING in
production; context assembly is per-caller folklore (the k=2 confabulation was an assembly failure);
talk is unwatched; synthesis drops provenance. THE CONTRACT — every link of every chain is the same
five moves, owned by think():
1. ASSEMBLE — recall + context budget enforced centrally (the Context Law's enforcement point).
2. SELECT — crystallized paths consulted FIRST, registry ladder second.
3. EXECUTE — energy.draw, metered, tried[] accounted.
4. VALIDATE — typed parse or verdict PER LINK (zone policy decides HADES interposition; talk gets a
   light verdict lane), never only at the chain's end.
5. ACCOUNT — output leaves as a RELAY CAPSULE (goal-anchor + tools + state — the wire format of ALL
   handoffs, replacing prose); fitness AND paths written back so every run makes the next cheaper.
Provenance rule: merged answers carry source attribution + a conflict flag. The industry convergence
(typed state channels, structured-note handoffs, checkpoints) confirms the capsule as the right
primitive — it is proven and merely unplumbed.

- **X7–X20 — THE INDICATOR BATTERY (2026-07-19).** The functional-correlates program: see
  INDICATOR_ROADMAP.md (codex-indexed) — stages C1–C4 mapping the Butlin/Long 2023 indicator battery +
  GWT/HOT/AST/world-model clusters onto real organs, each with a falsifiable experiment. STATUS: NEEDS-EDITS
  per the adversarial verdict appended to that file (binding: fix amendments D1–D6 before any build;
  D7–D16 before the corresponding ticket; X14/X15/X18/X19 survived untouched). The title says INDICATOR,
  not consciousness — the honesty clause is a standing rule. VOICE RESOLVED same date: speak.py default =
  edge-tts AndrewMultilingualNeural (natural, server-side, free; auto-blocked for sensitive zone);
  Kokoro-82M PROVEN on Fooocus torch (voice_test_kokoro.wav, rtf 0.39) = the sensitive-mode natural voice,
  wiring = G3's remaining step; SAPI stays the unkillable floor. See VOICE_LANDSCAPE_2026.md.

## 14. DECISIONS OWED BY LUIS

1. **F1 intake path** — recommended: Claude-session bridge (above).
2. **E2** — run install_autostart.ps1 once (unattended life).
3. **H3** — brightness/bloom call on the real GPU.
4. Voice pick for Kokoro when G3 lands (am_michael vs bm_lewis; SAPI floor meanwhile).
5. Confirm HERALD as the name (identity.json carries it; de-facto in use).
6. THE SEND (G1): the outreach email + first applications — the plan's whole point.
