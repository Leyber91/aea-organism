# LEYBER — READINESS RUBRIC (are we there yet?)

The gate for "an assistant at Claude's level, combined with Luis's thoughts." Scored 0-5 per dimension
against the REAL code (2026-07-19), verified live where possible. This is a standing gate: Leyber is not
"ready" until the load-bearing rows clear 3. Honest headline first, then the interrogation.

## HEADLINE VERDICT
**NOT READY. ~40% — a superbly governed, observable, self-healing SUBSTRATE with the COGNITION and REACH
organs still hollow.** It is not at a frozen rod's ceiling, let alone Claude's; and "combined with Luis's
thoughts" is currently ~48 memories deep. STRONG: governance, observability, orchestration-plumbing,
memory-mechanics, ops, voice. ABSENT/WEAK: agentic loop in conversation, self-tool-making, action, senses,
knowledge-graph, reflection tick, remote reach. The plumbing is world-class; the cognition and hands are not built.

## LUIS'S THREE QUESTIONS, ANSWERED STRAIGHT
- **Is it ready?** No. It reflects and talks (shallowly); it cannot browse, act, or make its own tools (tested live).
- **Is it agentic / does it actually develop scripts?** The main surface (talk) is SINGLE-SHOT, not agentic —
  no plan→act→observe loop, no goal stack across turns. The swarm/orchestrator ARE agentic but are not wired
  into conversation. It does NOT develop/persist/reuse its own scripts — "no write path" (its own words, live).
  The self-tool-making pattern (Voyager/smolagents CodeAgent) is the single biggest missing organ.
- **LangGraph or knowledge graph — are we context-efficient?** NEITHER. Orchestration is a custom
  swarm/orchestrator (not LangGraph — no state-graph checkpointing, no human-in-loop interrupts, no streaming
  graph). Memory is vector RAG-by-chunks (top-k inject), NOT a knowledge graph. On tokens: we retrieve k
  (good, not dump-everything) BUT we do NOT compress via a graph (the thing that truly minimizes context),
  and we have NO hierarchical summary layer (GraphRAG-style). B5 (graph memory) is specced, unbuilt.
  LangGraph adopt-vs-keep is an open build decision the running pressure-test fleet is scoring.

## THE INTERROGATION (the "thousand questions", load-bearing set)

### 1 · REASONING & AGENCY — score 2/5
Does the primary surface run a plan→act→observe loop, or single-shot? (single-shot) · Can it decompose a goal
and execute the parts? (swarm yes, unwired to talk) · Does it choose tools autonomously mid-task? (proven once,
unwired) · Can it re-plan after a failed step? (HADES redo for briefs only) · Does it hold a goal across turns?
(no goal stack in talk) · Does it know when it's stuck and escalate? (partially).
GAP: wire the agentic loop (think() = D1) into conversation; a per-task goal stack.

### 2 · TOOLS & ACTION — score 1/5 (the hollowest, and what "capable of anything" needs most)
Can it WRITE a tool, SAVE it, REUSE it next session? (NO — tested live) · Execute code safely in a sandbox?
(only calc/safe-eval) · Act on the world — email/calendar/files/commands? (NO, trust-FORBIDDEN + no integration) ·
Is there a dynamic tool registry it can grow? (no — paths.json is model-routes, not tools) · Does it dedup tools?
(n/a). GAP: the self-tool library (write→register→reuse) + an allowlisted action layer over trust.py.

### 3 · MEMORY & KNOWLEDGE — score 2.5/5
Graph or raw RAG? (raw vector RAG) · Context-efficient or re-stuff every turn? (top-k retrieve = ok; no graph
compression; no summary hierarchy) · Episodic→semantic consolidation? (YES — real strength) · Does memory
provably compound? (proven; but shallow — 48 memories after the pruning loss) · Source-tagged provenance?
(partial) · Contradiction/dedup pass? (no — B3 unbuilt) · Working vs long-term separation? (yes: talk_state vs
luis_memory). GAP: B5 knowledge-graph triples + GraphRAG hierarchical summaries; B1 depth; B3 quality gate.

### 4 · ORCHESTRATION — score 3.5/5 (a genuine strength, with a gap)
LangGraph or custom? (custom — proven but no checkpoint/interrupt/stream state-graph) · Deterministic vs
model-driven control? (mixed) · Is the chain observable end-to-end? (YES — tracelog + pulse + chains.jsonl +
the console; strong) · Cross-model rate/concurrency management? (YES — meter + per-plant pacing; strong) ·
One entry door? (NO — think()/D1 missing; routing lives in 4 homes). GAP: consolidate to one router (A2) +
the think() door (D1); score the LangGraph adopt honestly.

### 5 · SENSES / LUIS'S WORLD — score 1.5/5
Does it perceive Luis's real day (calendar/inbox/files)? (NO — stub since 2026-06-28) · Does it hold Luis's
goals/projects/preferences? (partial — book_of_luis, thin post-pruning) · Live internet awareness in
conversation? (NO). GAP: day intake (F1/F2 — the Google MCP connectors are the adopt path); real web (adopt a
keyless reader + search).

### 6 · LEARNING / SELF-IMPROVEMENT — score 2.5/5
Improves routing from use? (YES — fitness-from-use; strength) · Crystallizes repeated procedures into reusable
code? (partial — pathfinder crystallizes MODEL-routes, not skills) · Self-directed agenda / reflection tick?
(NO — E1 unwired; the autonomy gap) · Writes new skills for itself? (no — self-tooling again). GAP: E1 reflect
tick + the self-tool library close most of this at once.

### 7 · GOVERNANCE / SAFETY / TRUST — score 4.5/5 (the crown jewel)
Every autonomous output watched? (YES — chain surveillance + HADES verdicts, live) · Earned-autonomy ladder?
(YES — trust.py) · Privacy boundary code-enforced? (YES — sensitive→local, verified) · Conservative on
irreversible acts? (YES — send/spend/keys/self-modify FORBIDDEN). This is where Leyber genuinely leads. The
action layer (row 2) must be built THROUGH this, never around it.

### 8 · INTERFACE / EMBODIMENT — score 3/5
Reachable anywhere or localhost-only? (localhost only — a gap for "always with me") · Natural voice in+out?
(YES — edge-tts + browser STT) · Always-on/persistent? (YES now — X1 running). GAP: remote/secure reach
(a tunnel or a phone surface) if Leyber is to be a companion beyond the desk.

### 9 · RELIABILITY / OPS — score 4/5
Survives crashes/restarts? (YES — heartbeat + atomic state) · Handles model rot? (YES — self-healed today) ·
Corpus durability? (JUST FIXED — pruning was silently eating it; cleanupPeriodDays=3650 + widened corpus).
Strong, now that the silent data-loss hole is closed.

## THE SCORE
Governance 4.5 · Ops 4 · Orchestration 3.5 · Interface 3 · Memory 2.5 · Learning 2.5 · Reasoning 2 · Senses 1.5
· Tools/Action 1. **Weighted verdict: a rare, trustworthy substrate; a hollow cognition and hand.** The three
lowest rows (Action, Senses, Reasoning-loop) are exactly the three organs the pressure-test names next — and
each is an ADOPT (existing free tool), not an invent. "Ready" = those three clear 3, on the governance the
project already has. None of it outranks the income clock: the outreach still ships first.
