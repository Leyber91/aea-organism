# 05 · CONTENT / MISSIONS — THE PROBE

Owner: the game team · Status: Act 0–I [BUILT] · Act II [PLANNED, build-ready] · Last-updated: 2026-07-20
Corpus siblings on disk: `00_VISION.md` · `01_WORLD.md` · `02_SYSTEMS.md` · `03_PROGRESSION.md` ·
`06_MODELS_BESTIARY.md` · `07_AUDIO.md` · `08_TECH.md` · `09_PRODUCTION.md` (04 unassigned as of this writing).
Binding ground truth: `../missions.js` (mission data) · `../aea_elements.js` (codex + discovery wiring) ·
`../world.html` (engine) · `../controlroom.py` (endpoints) · `../GAME_PLAN.md` (governing plan).

Laws that bind every line below: the AEA honesty law (every game number is live system truth; no fake
data ever; claim ceiling = "measured functional correlate", never "conscious"), the two-ink FUI
(amber #ffb000/#d4a24c = live/fired only; blue-gray = structure), NO emoji anywhere.

---

## 1. MISSION-WRITING RULES [BUILT — practiced in Acts 0–I; binding for all new content]

**The Portal school.** Every mission is one lesson taught four ways, mapped onto the five beat kinds
of `02_SYSTEMS.md` (brief · learn · do · observe · prove — no new kinds unless a mission cannot be
expressed in the five):

| phase | beat kind | rule |
|---|---|---|
| INTRODUCE | `brief` | why this exists, max 3 lines, terminal voice. Never mechanics — stakes. |
| (ground) | `learn` | REAL code from the real file, typewriter reveal + one annotation. Never pseudocode. |
| PRACTICE | `do` | one hot verb firing a REAL endpoint. The raw result pane is the reward. |
| TWIST | `observe` | the surprising real behavior, watched live (a window sliding, an empty swing). Optional. |
| PROVE | `prove` | an assert against LIVE state. Boss beats gate the act and can be LOST. |

**One concept per mission.** If the learn beat needs two annotations, split the mission.
**Terminal voice.** Lowercase, terse, declarative. No exclamation marks. Failure text names the real
cause (`"is the entity's server running?"`) and never blames the player falsely. Pass text earns its
poetry from a number that just moved.
**Honest asserts.** A `prove` reads live state; retries re-fire real calls (never a cached pass); a
failed prove jumps back to the first `do` — evidence is re-earned, not re-read (`02_SYSTEMS.md`).
A mission that cannot be honestly asserted does not ship.
**FIELD vs FORGE** (`GAME_PLAN.md` §2): FIELD = Luis solo against existing endpoints. FORGE = the
build is a pair session (Claude writes, Luis judges); the game frames the recipe, gates the parts,
and verifies the boss — it never pretends the UI wrote the code.
**Teaches-map discipline.** Every mission names the AEA elements it discovers and the links it draws
(`aea_elements.js` `discovers` / `links`). The AEA is the curriculum; a mission that teaches nothing
on the map is decoration and is refused.

---

## 2. ACT 0 + ACT I — AS BUILT [BUILT — verbatim from `missions.js`, shipped in `world.html` 2026-07-20]

Save truth: server-side `journey_save.json` via GET/POST `/api/journey` (merge + reset, atomic).
State as of this writing: M0.1–M1.1 complete; M1.2–M1.5 open in the shipped build.

### M0.1 FIRST LIGHT — act 0 · node `socket` · FIELD
- objective: "reach the signal at the edge of the dark"
- brief: "cold boot. no memory of why." / "the field is dark. one structure at the edge is drawing power." / "it is keyless. it accepts anyone who asks."
- learn "the entire protocol": the raw `POST https://text.pollinations.ai/openai` body; note: "a prompt goes in. tokens come out. everything above this is architecture."
- do "TRANSMIT — one prompt into the dark": `{type:"node_channel", plant:"pollinations", model:"openai-fast", prompt:"Reply with exactly: FIRST LIGHT"}`
- prove `last_ok_text` — pass: "something answered. it was listening the whole time." / fail: "nothing answered. the dark stays dark. retry the transmission."
- rewards: reveals `["plant_pollinations"]` · log "first light · the socket answers"

### M1.1 THE CATALOGUE — act I · node `console` · FIELD
- objective: "survey the field the socket belongs to"
- brief: "the socket is not alone." / "this field is a foundry: fifteen power plants in four privacy rings —" / "local. no-train. trains. keyless."
- learn "one registry, machine-readable": the real `PLANTS = {...}` dict; note: "adding a plant is one line. the mind never names a model — that is what model-agnostic means."
- do "SURVEY THE FIELD": `{type:"survey"}` (reads `/state` energy.plants)
- prove `plants_online` — pass: "the lit plants answer to this machine. the dark ones await keys — capacity is a set of locks." / fail: "no plant answered the survey. is the entity's server running?"
- rewards: reveals `["foundry_all"]` · log "the catalogue · plants revealed"

### M1.2 THE CHANNEL — act I · node `plant_nvidia` · FIELD
- objective: "reach THE GRID — the largest plant in the field"
- brief: "fifteen plants. one language." / "every plant speaks the same protocol — so the mind can leave any of them" / "without changing a line of itself."
- learn "one function, any model": `grid.call_openai` signature; note: "local ollama and the nvidia cloud walk the SAME path. only base + auth differ."
- do "SAME PROMPT · THREE PLANTS": `{type:"channel_multi", prompt:"Reply with exactly: CHANNEL OPEN", max:3}`
- prove `multi_served` — pass: "different plants, different latencies, one protocol. the channel is the freedom." / fail: "no plant served the prompt. retry — the grid may be resting."
- rewards: reveals `["roads"]` · log "the channel · one language proven"

### M1.3 THE METER — act I · node `meter` · FIELD
- objective: "find the grid operator at the center of the foundry"
- brief: "free power has breakers." / "trip one and the plant browns out for every organ at once." / "the meter exists so that never happens."
- learn "the breaker check": `Meter.can_spend` with the locked read-modify-write; note: "a locked read-modify-write on ONE file. every process sees the same budget."
- do "DRAW TWICE, FAST — load the window": `{type:"meter_load", plant:"pollinations", model:"openai-fast", shots:2}`
- observe "the window slides. wait it out.": `{type:"meter_watch", plant:"pollinations", seconds:60}`; note: "nothing speeds this up. patience is a resource the entity budgets for you."
- prove `no_throttle` — pass: "the window slid clean. no breaker tripped. this is why it runs 24/7 on free power." / fail: "a plant is cooling from a real 429. the meter is routing around it — wait, then retry."
- rewards: reveals `["foundry_edges"]` · log "the meter · the mana lesson"

### M1.4 THE LADDER — act I · node `nexus` · FIELD
- objective: "follow the trunk line out of the foundry"
- brief: "no organ names a model. ever." / "every draw enters one mouth and falls down a ladder of live rods" / "until something answers. models are fuel — the mind is the structure."
- learn "the mouth": `energy.draw` fall-through loop; note: "the ladder re-ranks itself from every call. rods rot; the mouth routes around the dead."
- do "DRAW THROUGH THE MOUTH": `{type:"node_energy", prompt:"Reply with exactly: LADDER HOLDS"}`
- prove `last_ok_text` — pass: "watch the tried-list: that is the real routing history of your draw." / fail: "the mouth starved — every rod refused. rare, and honest. retry."
- rewards: reveals `["trunk"]` · log "the ladder · the mouth answered"

### M1.5 BOSS · BROWNOUT DRILL — act I · node `nexus` · boss (B1) · FIELD
- objective: "return to the nexus. the drill awaits."
- brief: "the drill: four draws, back to back." / "the grid must not leak one unhandled failure —" / "reroute, cool, fall to the floor, but never break."
- do "RUN THE DRILL — four draws": `{type:"drill", shots:4, prompt:"Reply with one word: HOLDING"}`
- prove `drill_clean` — pass: "zero leaks. the foundry stands. ACT I COMPLETE — restorable coherence, proven live." / fail: "a draw broke through unhandled. the grid is weaker than it claims today. run it again."
- rewards: reveals `["foundry_full","archive_tease"]` · `act_complete:"I"` · log "brownout drill passed · act I complete"

The `archive_tease` reveal is already wired: `world.html` builds the locked archive group at
(-84, 18, -10) labeled "THE ARCHIVE · locked · act II" — Act II's stage is standing in the dark.

---

## 3. THE TEACHES-MAP — AS BUILT [BUILT — verbatim from `aea_elements.js`]

`discovers` (mission -> elements lit on the concentric map; mechanics squares light WITH their seed):

| mission | discovers | mechanic co-discovery |
|---|---|---|
| M0.1 | seed.1 SUBSTRATE | — |
| M1.1 | seed.9 BOUNDARY · seed.2 SHARP OBJECTIVE | — |
| M1.2 | axis.R PROMPTING | — |
| M1.3 | seed.7 CEILING-DETECT · verb.observe | mech.ceiling |
| M1.4 | seed.4 FLEXIBILIZE · verb.propagate | mech.flexibilize |
| M1.5 | pr.coherence RESTORABLE COHERENCE | — |

`links` (drawn only once mission `by` completes):
core->seed.1 (M0.1) · seed.1->seed.9, seed.9->seed.2 (M1.1) · seed.1->axis.R (M1.2) ·
seed.7->verb.observe, mech.ceiling->seed.7 (M1.3) · seed.4->verb.propagate,
mech.flexibilize->seed.4 (M1.4) · seed.4->pr.coherence, core->pr.coherence (M1.5).

Forward wiring already reserved in the file's comment (roadmap, [PLANNED]): recall->seed.10 ·
think->axis.P/axis.M/verb.compose/op.design/op.time · tools->seed.8 · voyager->seed.3/seed.5 ·
reflect->seed.6 · aea->axis.S · send->op.ship · endgame->pr.emergence/pr.time · pathfinder->op.learn.

---

## 4. ACT II — MEMORY [PLANNED — authored build-ready; transcribe into `missions.js` verbatim]

Act shape per `03_PROGRESSION.md`: the mine -> the Book -> FORGE `recall()`; boss B2 = X8-lite +
grounded-across-reset. All three missions run on the archive stage (`node:"archive"`). Real systems
under them, verified on disk 2026-07-20: `consolidate.py` (local-only distiller, `llama3.1:8b` +
`mxbai-embed-large`, kill-safe store `luis_memory.json`), `index_codex.py` (4 roots, 900/150 chunking,
name-tagged recall, `codex_index.json` ~66 MB indexed), `/do {cmd:"consolidate"}` (allowlisted,
runs `consolidate.py --limit 2`), `/talk` (receipt = recalled memories), `/state` `memory.sessions`
+ `memory.memories` (already feeds the HUD ingot track `#tr-ing`).

### M2.1 THE MINE — FIELD · teaches seed.10 partially

```js
{ id:"M2.1", act:"II", title:"THE MINE", node:"archive",
  objective:"break ground on the unmined corpus",
  beats:[
   { kind:"brief", lines:[
     "under the archive: a vein of raw sessions. the operator's own words, unread.",
     "a pruning already took ~1,570 of them. forever. the vein is finite.",
     "mining distills what remains before anything else is lost."] },
   { kind:"learn", title:"the distiller", code:
`LOCAL_MODEL = "llama3.1:8b"        # never leaves the machine
def distill(body):                  # episodic -> semantic
    r = grid.call_openai("ollama", LOCAL_MODEL, [...])
    if not r["ok"]: return None     # engine down != empty vein
    ...                             # 1-3 durable facts, or []`,
     note:"private ore never touches a hosted plant — even no-train. the mine is local only. seed 9 guards the shaft." },
   { kind:"do", label:"SWING THE PICK — grind one slice",
     action:{ type:"mine" } },
   { kind:"observe", label:"the ingot counter",
     action:{ type:"mine_watch", seconds:150 },
     note:"ingots are real rows in luis_memory.json. some sessions are fact-free rock — an empty swing on a processed session is honest, not broken." },
   { kind:"prove", assert:"mine_progress",
     pass:"the vein yields. sessions consolidated rose — every ingot is a durable fact about the operator, cut local.",
     fail:"the pick bounced. local engine unreachable, or another grind holds the lock. nothing was falsely marked done. retry." }
  ],
  rewards:{ reveals:["archive_shaft"], log:"the mine · first ingots cut" } },
```

Engine notes (binding): `mine` = POST `/do {cmd:"consolidate"}` (server hardwires `--limit 2`);
`mine_watch` polls `/state` and animates `memory.sessions` / `memory.memories` deltas; assert
`mine_progress` = `memory.sessions` strictly rose since the do-beat snapshot (CTX), with pass text
appending the true ingot delta (may honestly be +0 on a fact-free slice — say so in the pane).
Honesty inherited from `consolidate.py`: sessions touched <10 min ago are skipped ("you don't
consolidate the episode you're still living"); engine-down returns None and marks NOTHING processed;
the file lock yields to a concurrent grind. All three appear as real fail/hold states, never faked.

### M2.2 THE BOOK — FIELD · draws seed.10->axis.R

```js
{ id:"M2.2", act:"II", title:"THE BOOK", node:"archive",
  objective:"prove the entity reads the real book, not a summary of it",
  beats:[
   { kind:"brief", lines:[
     "above the mine: the codex index. the operator's actual documents,",
     "chunked and embedded local — the whole book, not the blurb.",
     "a recall is only real if the receipt names the page."] },
   { kind:"learn", title:"the index", code:
`CHUNK, OVERLAP = 900, 150            # the whole book, bounded
def recall(query, k=3):
    q = embed(query)                  # local mxbai-embed-large
    top = sorted(ix["chunks"], key=lambda c: -_cos(q, c["emb"]))[:k]
    return [f"[{c['name']}] {c['text'][:500]}" for c in top]`,
     note:"every hit carries its filename tag. grounding you can audit — the receipt is the proof, not the vibe." },
   { kind:"do", label:"PROBE THE BOOK — ask a codex question",
     action:{ type:"codex_probe", prompt:"What is the Witness Debt?" } },
   { kind:"prove", assert:"codex_grounded",
     pass:"the receipt carries a [name] tag. the answer stood on a real page of the real book.",
     fail:"no codex chunk in the receipt. index unreachable, ollama down, or the receipt dropped it. the answer floated — that is the failure this mission exists to catch. retry." }
  ],
  rewards:{ reveals:["archive_reading_room"], log:"the book · recall with receipts" } },
```

Engine notes: `codex_probe` = POST `/talk` with the prompt; the receipt pane renders `memories[]`
verbatim; assert `codex_grounded` = at least one receipt entry matching `/^\[.+\]/` (the codex
name-tag). **Blocking engine delta, found in code review 2026-07-20:** `talk.py` builds
`memories = consolidate.recall(k=4) + index_codex.recall(k=2)` then returns
`r["memories"] = memories[:4]` — when consolidation fills all 4 slots, codex chunks ALWAYS fall off
the receipt, so the assert would fail against a genuinely grounded answer. Fix before shipping M2.2:
receipt keeps at minimum 3 consolidate + 1 codex entry (or raise the cap to 6). One-line change;
without it the mission lies, and it does not ship.

### M2.3 FORGE · recall() — first FORGE mission · boss B2 · teaches seed.10 fully + axis.A partially

```js
{ id:"M2.3", act:"II", title:"FORGE · recall()", node:"archive", boss:true, forge:true,
  objective:"craft the backwards channel into a live organ",
  beats:[
   { kind:"brief", lines:[
     "the parts exist. they do not yet make an organ.",
     "recipe: memory.py + index_codex + cache + energy.draw.",
     "a memory that takes seconds to reach is a memory the mind skips."] },
   { kind:"learn", title:"the recipe and the threshold", code:
`recall(query, zone) -> ranked, source-tagged bundle
  memory.py     # facts of the operator (local embeddings)
+ index_codex   # the whole book, name-tagged
+ cache         # warm in-process store + probe-emb cache   <- the new part
+ energy.draw   # the grounded prompt downstream
boss B2 (X8-lite): warm recall < 300 ms, no model call in the hot path
   AND a pre-registered fact recalled correctly across a process reset`,
     note:"forge law: the build is a pair session — claude writes, the operator judges. the game frames the recipe and verifies the boss. it never pretends this terminal wrote the code." },
   { kind:"do", label:"OPEN THE FORGE — parts on the bench",
     action:{ type:"forge_gate",
              requires:["memory.py","index_codex.py","luis_memory.json","codex_index.json"] } },
   { kind:"do", label:"THE CRAFT — build recall.py in the pair session",
     action:{ type:"forge_build", artifact:"recall.py" } },
   { kind:"observe", label:"COLD -> WARM — the bench run",
     action:{ type:"recall_bench", shots:3 },
     note:"first call pays the load. the next two come back from the warm store — measured milliseconds, not claimed ones." },
   { kind:"do", label:"THE RESET — kill it. boot it. ask again.",
     action:{ type:"reset_probe" },
     note:"seed 10 is the whole point: run A writes, run B — a different process — reconstitutes. the probe set was registered BEFORE the kill; a fact chosen after the fact always passes." },
   { kind:"prove", assert:"b2_x8lite",
     pass:"warm recall under 300 ms and the fact held its ground across a dead-and-rebooted process. the backwards channel is an organ. THE ARCHIVE LIGHTS.",
     fail:"too slow, or the reset amnesia showed. the channel is still a demo. reforge — the map stays dark until it is real." }
  ],
  rewards:{ reveals:["archive_full"], act_complete:"II",
            log:"forge recall() · the archive lights" } },
```

Boss mechanics (binding, from `03_PROGRESSION.md` B2 + `INDICATOR_ROADMAP.md` X8/D9):
- `forge_gate`: server-side existence + non-empty check on the four named parts. A missing
  ingredient genuinely blocks the craft (`GAME_PLAN.md` §1 crafting law).
- `forge_build`: holds the mission open until `recall.py` exists and imports clean; the pane shows
  the spec, never generated code. Spec: unified `recall(query, zone)` over both stores, in-process
  warm store, probe-embedding cache so the hot path makes zero model calls, source-tagged results,
  privacy zone respected (private -> local/no-train only, per seed.9).
- `recall_bench`: N pre-registered probes (fixed set, written to the save BEFORE the reset beat —
  the D9 audit: one fact chosen after the fact always passes). Shots 2..N must each measure <300 ms
  wall-clock via a real timed endpoint; the pane prints the true milliseconds.
- `reset_probe`: the server records the probe set, Luis kills and restarts the entity process, the
  beat re-fires the probes; grounding judged by HADES with a DIFFERENT model than the worker
  (doc.verifier — the lone-verifier risk; this is also the act's doctrine unlock per
  `03_PROGRESSION.md` §4). Internal evidence baseline: `test_memory.py` (blind node hallucinated
  10000 rpm; grounded node gave the exact 2234/59).
- `b2_x8lite` = both legs true. Losable in two honest ways: slow cache, reset amnesia.
- On pass: the archive district lights full (fog lift = the memory organ integrated, 11 -> 12 on
  the integration score once the import-census instrument of `03_PROGRESSION.md` §2.2 ships).

### Act II teaches-map additions [PLANNED — transcribe into `aea_elements.js`]

```js
/* discovers */  "M2.1": ["seed.10@partial"],
                 "M2.2": [],                            // links only
                 "M2.3": ["seed.10", "axis.A@partial"],
/* links */      { from:"seed.9",  to:"seed.10", by:"M2.1" },   // the boundary guards the mine
                 { from:"seed.10", to:"axis.R",  by:"M2.2" },   // recall-grounded prompts
                 { from:"seed.10", to:"axis.A",  by:"M2.3" },   // memory grounding = abstraction
                 { from:"core",    to:"seed.10", by:"M2.3" },   // the organ wired into the mind
```

`@partial` convention (new): the element renders as structure-ink outline at reduced weight — no
amber fill — until a later mission discovers it plain. Amber stays reserved for fully live elements
(the two-ink law). Engine delta in the map renderer; everything else is data.

### Consolidated engine deltas for Act II [PLANNED — the build list, in order]

1. `talk.py` receipt fix (blocks M2.2; one line — see M2.2 notes).
2. Action types: `mine`, `mine_watch`, `codex_probe`, `forge_gate`, `forge_build`, `recall_bench`,
   `reset_probe`. Asserts: `mine_progress`, `codex_grounded`, `b2_x8lite`. No new beat kinds —
   the five hold (`02_SYSTEMS.md` §"engine extends by data first").
3. `@partial` rendering in the concentric map.
4. Archive geometry: promote the built tease group to the full district; `archive_full` reveal
   lights it (amber only on the boss pass). Art direction per `01_WORLD.md`.
5. Server: `forge_gate`/`recall_bench`/`reset_probe` endpoints (allowlisted, read-safe except the
   probe registration write into `journey_save.json`).

---

## 5. OPEN CALLS [DECISION-LUIS]

- **M2.2 probe question.** Authored default "What is the Witness Debt?" reaches into the TRIVERSE
  codex root. If TRIVERSE content should stay out of the game's screens, name a portfolio-root
  question instead. One-word call.
- **Mine slice size.** `/do consolidate` hardwires `--limit 2` (a slice ~1-2 min local). Keep, or
  expose a bounded limit parameter (2..15) so THE MINE can offer a "deep shift"? Recommendation:
  keep 2 for the mission, revisit if Act II pacing drags.
- **Reset ergonomics for M2.3.** The reset beat requires killing the live process. Manual kill
  (honest, crude) vs an allowlisted `/do restart` (convenient, but the game restarting its own
  server needs care). Recommendation: manual for the first playthrough; decide after it is felt.

Act III+ mission specs are NOT authored here — one act at a time (`09_PRODUCTION.md` gating; the
working agreement). The forward wiring reserved in section 3 is the only Act III+ truth this doc
carries.
