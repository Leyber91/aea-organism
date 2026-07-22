/* aea_elements.js — THE PROBE · the AEA codex + combination doctrines (data only)
   The concentric map + codex screens read this. Discovery state lives in journey_save
   (missions' `discovers` lists + models encountered via real tried[] logs).
   Taxonomy = the proof taxonomy (AEA_PROOF_PLAN / proof_scoreboard, 2026-06-28):
   5 axes · 10 seeds · 3 verbs · 4 mechanics (=seeds 3/4/5/7 between ticks) · 4 ops · 3 principles.
   `proof` = the standalone demo that proved it (honest: demo-proven is not live-wired). */
"use strict";
window.AEA = {

/* ring geometry per BINDING UI SPEC v1.0 §2 (viewBox 1000: core r70; rings 150/250/360/470).
   ring3 (r360) holds three arc families: verbs (triangles) + mechanics (squares) + ops (diamonds).
   mechanics render as their own nodes but discover WITH their seed (3/4/5/7). */
rings: [
 { id:"principles", label:"PRINCIPLES", sub:"what emerges",       r:150, shape:"hex" },
 { id:"axes",       label:"AXES",       sub:"locate the entity",  r:250, shape:"pent" },
 { id:"mid",        label:"VERBS · MECHANICS · OPS", sub:"the rails", r:360, shape:"mixed" },
 { id:"seeds",      label:"SEEDS",      sub:"the organs",         r:470, shape:"circle" },
],
/* mechanics nodes (ring 3, squares) — each mirrors a seed; discovered when its seed is */
mechanics: [
 { id:"mech.crystallize", seed:"seed.3", name:"CRYSTALLIZE" },
 { id:"mech.flexibilize", seed:"seed.4", name:"FLEXIBILIZE" },
 { id:"mech.selfversion", seed:"seed.5", name:"SELF-VERSION" },
 { id:"mech.ceiling",     seed:"seed.7", name:"CEILING-DETECT" },
],
/* taught links {from,to,by} — drawn only once mission `by` completes (spec §2 links) */
links: [
 { from:"core",    to:"seed.1",         by:"M0.1" },
 { from:"seed.1",  to:"seed.9",         by:"M1.1" },
 { from:"seed.9",  to:"seed.2",         by:"M1.1" },
 { from:"seed.1",  to:"axis.R",         by:"M1.2" },
 { from:"seed.7",  to:"verb.observe",   by:"M1.3" },
 { from:"mech.ceiling", to:"seed.7",    by:"M1.3" },
 { from:"seed.4",  to:"verb.propagate", by:"M1.4" },
 { from:"mech.flexibilize", to:"seed.4",by:"M1.4" },
 { from:"seed.4",  to:"pr.coherence",   by:"M1.5" },
 { from:"core",    to:"pr.coherence",   by:"M1.5" },
],

elements: [
 /* ---- AXES (5) ---- */
 { id:"axis.P", ring:"axes", name:"PATH",         line:"control flow — the entity defines its own next step, not a fixed graph", proof:"swarm.py · spawned 4 sub-agents mid-tree" },
 { id:"axis.M", ring:"axes", name:"MULTIPLICITY", line:"how many role-differentiated nodes run and synthesize in parallel",      proof:"swarm.py · 8 roles coordinated" },
 { id:"axis.A", ring:"axes", name:"ABSTRACTION",  line:"memory grounding, tool use, writing new skills",                         proof:"agent_tools.py · live GitHub call" },
 { id:"axis.R", ring:"axes", name:"PROMPTING",    line:"a frontier-encoded scaffold makes a cheap node beat its raw self",       proof:"memory.py · recall-grounded prompts" },
 { id:"axis.S", ring:"axes", name:"ASYNC",        line:"temporal independence — scheduled, unattended, parallel",                proof:"relay.py · 5-model genetic handoff" },
 /* ---- SEEDS (10) ---- */
 { id:"seed.1",  ring:"seeds", name:"SUBSTRATE",        line:"the model grid answers — plants, generators, free energy",         proof:"test_capacity.py · 59 nodes live" },
 { id:"seed.2",  ring:"seeds", name:"SHARP OBJECTIVE",  line:"every task carries a falsifiable scorer",                          proof:"grid battery scorers" },
 { id:"seed.3",  ring:"seeds", name:"CRYSTALLIZE",      line:"freeze a repeated behaviour into a reusable tool",                 proof:"relay.py toolkit growth", mechanic:true },
 { id:"seed.4",  ring:"seeds", name:"FLEXIBILIZE",      line:"kill a node mid-run — the route falls, the task completes",        proof:"test_resilient.py · 15/15 under fire", mechanic:true },
 { id:"seed.5",  ring:"seeds", name:"SELF-VERSION",     line:"a run writes a NEW skill; a later run uses it",                    proof:"relay.py · downstream reuse", mechanic:true },
 { id:"seed.6",  ring:"seeds", name:"SELF-MODEL",       line:"the entity reports what it is made of; judges its own work",       proof:"hades.py · Law-3 verdicts" },
 { id:"seed.7",  ring:"seeds", name:"CEILING-DETECT",   line:"a quality gate flags the ceiling — escalate deeper",               proof:"pathfinder.py · reflex→bulk→deep", mechanic:true },
 { id:"seed.8",  ring:"seeds", name:"TRANSCENDENCE",    line:"the toolset — real external tools invoked by the mind",            proof:"agent_tools.py · web_fetch/json_get/calc" },
 { id:"seed.9",  ring:"seeds", name:"BOUNDARY",         line:"a private task NEVER routes to a trains-zone plant",               proof:"brief.py · sensitive→local only" },
 { id:"seed.10", ring:"seeds", name:"BACKWARDS CHANNEL",line:"run A writes a memory capsule; run B reconstitutes it",            proof:"memory.py · vector store recall" },
 /* ---- VERBS (3) ---- */
 { id:"verb.compose",   ring:"verbs", name:"COMPOSE",   line:"assemble subtask results into one coherent whole",                 proof:"swarm.py synth step" },
 { id:"verb.propagate", ring:"verbs", name:"PROPAGATE", line:"the honesty node — live trace of task→node→output",                proof:"swarm.py silent-wrong-work flag" },
 { id:"verb.observe",   ring:"verbs", name:"OBSERVE",   line:"meter telemetry + trace — the state is visible",                   proof:"tracelog.py · goal-stack ledger" },
 /* ---- OPS (4) ---- */
 { id:"op.design", ring:"ops", name:"DESIGN", line:"tag a task with the axis-levels it needs before running",                    proof:"PARTIAL — lands with think() (D1)" },
 { id:"op.time",   ring:"ops", name:"TIME",   line:"every tick timestamped and observable",                                     proof:"PARTIAL — per-tick stamps owed" },
 { id:"op.ship",   ring:"ops", name:"SHIP",   line:"unskippable — a run produces a REAL external artifact",                     proof:"brief.py · HADES-accepted brief" },
 { id:"op.learn",  ring:"ops", name:"LEARN",  line:"a run's result measurably improves the next",                               proof:"pathfinder.py · paths.json" },
 /* ---- PRINCIPLES (3) ---- */
 { id:"pr.emergence", ring:"principles", name:"EMERGENCE OVER IMPOSITION", line:"the entity defines its own steps — no central controller", proof:"swarm.py spawn decisions" },
 { id:"pr.coherence", ring:"principles", name:"RESTORABLE COHERENCE",      line:"a failure reroutes; the system still completes",           proof:"test_resilient.py · 429s rerouted" },
 { id:"pr.time",      ring:"principles", name:"OPERATOR-OBSERVABLE TIME",  line:"full goal-stack, append-only timeline",                    proof:"tracelog.py DAG" },
],

/* which missions reveal which elements (the discovery wiring) */
discovers: {
 "M0.1": ["seed.1"],
 "M1.1": ["seed.9", "seed.2"],
 "M1.2": ["axis.R"],
 "M1.3": ["seed.7", "verb.observe"],
 "M1.4": ["seed.4", "verb.propagate"],
 "M1.5": ["pr.coherence"],
 /* Act II+ (authored later): recall->seed.10, think->axis.P/axis.M/verb.compose/op.design/op.time,
    tools->seed.8, voyager->seed.3/seed.5, reflect already live->seed.6, aea->axis.S, send->op.ship,
    endgame->pr.emergence/pr.time, op.learn->pathfinder mission */
},

/* ---- COMBINATION DOCTRINES — measured, not invented (grid experiments 2026-06, regime map) ---- */
doctrines: [
 { id:"doc.solo",    name:"THE SOLO LAW",        locked:false,
   line:"an easy task wants ONE good model. a council on an easy task HURTS it.",
   evidence:"measured · grid experiments v2–v4 (2026-06): council overhead damaged easy-task accuracy" },
 { id:"doc.council", name:"THE DIVERSE COUNCIL", locked:false,
   line:"a hard or unreliable task is rescued by a DIVERSE-model vote — the win is model diversity, not temperature.",
   evidence:"measured · v3 net +3 with 0 damage; same-model ensembles did not rescue" },
 { id:"doc.verifier",name:"THE LONE VERIFIER RISK", locked:true,
   line:"a single verifier can be wrong alone. the watcher survives by strict-schema + a DIFFERENT model than the worker.",
   evidence:"measured · verifier error analysis; hades.py Law-2 heterogeneity" },
 { id:"doc.relay",   name:"THE GENETIC RELAY",   locked:true,
   line:"models hand a compact state capsule down a chain — the toolkit grows across hands.",
   evidence:"proven · relay.py: 5 distinct models, 2/2 handoffs, toolkit reused downstream" },
 { id:"doc.swarm",   name:"THE RAMIFICATION",    locked:true,
   line:"decompose, escalate, depth-cap — a tree of small minds where one big mind would drown.",
   evidence:"proven · swarm.py: 8 role-differentiated agents, spawn decisions mid-tree" },
 { id:"doc.path",    name:"THE CRYSTAL PATH",    locked:true,
   line:"search once for the winning model per task-type, then run cheap forever.",
   evidence:"proven · pathfinder.py -> paths.json (op.learn live)" },
],
};
