# 05B · CONTENT / MISSIONS — ACTS III + IV — THE PROBE

Owner: the game team · Status: Act III [PLANNED, build-ready] · Act IV [PLANNED, build-ready;
M4.3 gated DECISION-LUIS] · Last-updated: 2026-07-20
Continues `05_CONTENT_MISSIONS.md` (rules §1, Act 0–II, teaches-map). Governed by `A2_TEACHING.md`
(pedagogy) and `A3_NARRATIVE.md` (every rendered line); act shapes + boss thresholds from
`03_PROGRESSION.md`; doctrine machinery from `06_MODELS_BESTIARY.md`; beat/engine law from
`02_SYSTEMS.md`. Ground truth on disk, verified 2026-07-20: `../missions.js` · `../aea_elements.js`
· `../controlroom.py` (`/api/node/run` allowlist: channel, energy) · `../swarm.py` ·
`../orchestrator.py` · `../pathfinder.py` · `../hades.py` (groq strict-json watcher) · `../trust.py`
(CHARTER, 4 levels) · `../agent_tools.py` (real tool loop) · `../decisions.jsonl` (57 lines, lane
"reflect") · `../experiment_v3/v4.py` · `../PLAN.md` (ticket A2). Laws binding every line: the
AEA honesty law (live truth only, no fake data, claim ceiling = "measured functional correlate",
never "conscious"), two-ink FUI (amber = live/fired only), NO emoji, voice per `A3_NARRATIVE.md` §7.

---

## 1. THE DOCTRINE RESOLUTION [PLANNED — resolves the collision named in 06_MODELS_BESTIARY §5.2]

The built rule opens all four locked doctrines at M1.5; Act III was designed to demonstrate them.
Two truths cannot coexist. **Resolution: M1.5 is the READING unlock; Act III is the DEMONSTRATION.**
Doctrines become two-state: **READ** (text unmasked, blue-gray structure ink) and **EARNED**
(amber tag, evidence line appended with the live demonstration's real result and date). M1.5 keeps
its built blanket unlock, downgraded in meaning to READ — nothing shipped regresses. Engine delta:
doctrines gain `earnedBy:<missionId>`; `modelsRender` renders READ when
`!d.locked || missionDone("M1.5")` (as built) and EARNED when `missionDone(d.earnedBy)`; amber
only on EARNED. The earnedBy map: `doc.solo` M3.1 · `doc.council` M3.1 · `doc.path` M3.2 ·
`doc.swarm` M3.3 · `doc.verifier` M3.3. **`doc.relay` has no Act III/IV demonstration** — it
stays READ until the Act VI relay/voyager forge (no fake earn). Luis's yes gates transcription.

---

## 2. ACT III — MIND [PLANNED — authored build-ready; transcribe into `missions.js` verbatim]

Act shape per `03_PROGRESSION.md`: the council -> the regimes -> FORGE `think()`; boss D1 = obey
both measured laws, logged. Stage: the mind district (`mind_tease` added to M2.3's rewards at
transcription, per §4 item 7). Real systems [BUILT], verified on disk: `swarm.py` (diverse pick, triage,
depth-cap), `pathfinder.py` (classify -> tier ladder -> gate -> crystallize), `hades.py` (strict-
schema watcher on `groq/gpt-oss-120b`, NOT a worker model), the regime experiments (`v2/v3/v4`).

### M3.1 THE COUNCIL — FIELD · teaches axis.M · earns doc.solo + doc.council

```js
{ id:"M3.1", act:"III", title:"THE COUNCIL", node:"council",
  objective:"convene unlike voices on one hard question",
  beats:[
   { kind:"brief", lines:[
     "one model answers alone, and is wrong alone.",
     "a council of unlike voices votes — and the vote can rescue what no single voice could.",
     "or it cannot. the task decides, and that law was measured."] },
   { kind:"learn", title:"the diverse pick", code:
`def pick_varied(pool, tier, meter, topk=8):
    """Spread load across DISTINCT buckets."""
    c = [n for n in pool if n['score'] == 4 and orchestrator.tier_of(n) == tier ...]
    random.shuffle(c)   # unlike lineages, on purpose`,
     note:"diversity is chosen, not hoped for. the measured win is unlike training lineages — not temperature. same-model ensembles did not rescue." },
   { kind:"do", label:"THE CONTROL — one voice, the easy question",
     action:{ type:"council", mode:"solo", bank:"easy" } },
   { kind:"do", label:"ASK ALONE — one voice, the hard question",
     action:{ type:"council", mode:"solo", bank:"hard" } },
   { kind:"do", label:"CONVENE — five unlike lineages, same question",
     action:{ type:"council", mode:"diverse", bank:"hard", members:5 } },
   { kind:"observe", label:"THE TALLY",
     action:{ type:"council_tally" },
     note:"per-voice answers, the vote, the meter bill. one live sample cannot prove a statistical law — the law's evidence stays the 2026-06 batteries. what you just watched is the mechanism, running for real." },
   { kind:"prove", assert:"council_demo",
     pass:"three real runs, scored against registered answers. the tally holds what actually happened tonight — the doctrine pair is EARNED on the demonstration, and its evidence line now carries your tally.",
     fail:"the council never convened — fewer than three distinct rods answered. the grid is thin right now. retry." }
  ],
  rewards:{ reveals:["council_hall"], log:"the council · unlike voices tallied" } },
```

Engine notes (binding): **new `/api/node/run` branch `council`** — the named engine delta. Solo =
one `pick_varied` draw; diverse = N parallel draws across distinct lineages (`swarm.pick_varied` +
`orchestrator.call_node` + the meter, read-safe) + majority tally. Questions come from a server-side
pre-registered bank with deterministic answers (seeded from `experiment_v3/v4`), so `council_demo`
is mechanical: three runs completed AND scored AND >=3 distinct models convened. **Honesty rule:**
the assert never claims "council beats solo" — one sample cannot prove a regime; the pane reports
the real per-leg outcomes and names any disagreement with the measured law plainly: a doctrine is
statistical, and the disagreement IS the lesson.

### M3.2 THE REGIMES — FIELD · first predict beat · teaches op.learn · earns doc.path

```js
{ id:"M3.2", act:"III", title:"THE REGIMES", node:"regimes",
  objective:"call the path before the router walks it",
  beats:[
   { kind:"brief", lines:[
     "every task walks a path: reflex, bulk, deep — or a council.",
     "the router chooses from measured law, not from taste.",
     "you call it first. the machine settles it. wrong calls cost nothing, and are remembered."] },
   { kind:"learn", title:"the ladder with a gate", code:
`LADDER = ['reflex', 'bulk', 'deep']
# classify (one cheap call) -> climb the ladder by step;
# after each rung a quality gate asks: solved?
# the winning rung CRYSTALLIZES into paths.json — the next same-type task skips the search`,
     note:"search once, crystallize, run cheap forever. energy is spent on the first instance of a type — not on every instance." },
   { kind:"predict", question:"this task. which rung answers it?",
     options:["reflex","bulk","deep"], settle:"route" },
   { kind:"do", label:"RUN THE ROUTE — the ladder decides",
     action:{ type:"route", bank:"mixed" } },
   { kind:"observe", label:"THE CRYSTAL — second task, same type",
     action:{ type:"route", bank:"same_type" },
     note:"the first run paid for the search. this one walked the crystallized path straight. that is op.learn, live — watch the skipped rungs." },
   { kind:"prove", assert:"route_settled",
     pass:"your call is settled against the real route and logged, right or wrong. the ledger keeps it — re-encounter will target what you actually missed.",
     fail:"the route never completed — every rung refused or the gate went silent. the grid is thin. retry." }
  ],
  rewards:{ reveals:["regime_gallery"], log:"the regimes · the path called, the path walked" } },
```

Engine notes: **new beat kind `predict`** — the sixth kind; `02_SYSTEMS.md`'s five-kind law
permits it because a commit-before-settle beat cannot be expressed as do/observe/prove, and
`A2_TEACHING.md` §7 already sanctions prediction beats from Act III on. `journey_save.json` gains
a `predictions[]` ledger `{mission, beat, called, settled, t}` — A2's private learning ledger.
**New `/api/node/run` branch `route`** wraps pathfinder classify + escalation + gate (honest
write named: a winning route writes `paths.json`). The live route may disagree with the call AND
the doctrine; the settle is always the real route. `doc.path` EARNED only on the observe's real
crystallized reuse (path hit logged).

### M3.3 FORGE · think() — boss D1 · teaches axis.P, verb.compose, op.design, op.time · earns doc.swarm + doc.verifier

```js
{ id:"M3.3", act:"III", title:"FORGE · think()", node:"mind", boss:true, forge:true,
  objective:"three organs, one door",
  beats:[
   { kind:"brief", lines:[
     "swarm, orchestrator, pathfinder: three proven organs, three separate doors.",
     "the mind needs one. think(task) — and the task itself picks the regime.",
     "a door that always convenes a council is as wrong as one that never does."] },
   { kind:"learn", title:"the recipe and the threshold", code:
`think(task) -> one decision, one answer, one log line
  pathfinder.classify   # name the task type (cheap)
  regime choice         # solo rung | diverse council | swarm decompose
  energy.draw           # every path through ONE router (PLAN.md A2, absorbed)
  hades.watch           # the gate on the way out, a DIFFERENT model
boss D1: the hard task convenes, the trivial stays solo — both logged in
  decisions.jsonl. rubber-stamping either way is a loss.`,
     note:"forge law: the build is a pair session — claude writes, the operator judges. the game frames the recipe and verifies the boss. it never pretends this terminal wrote the code." },
   { kind:"do", label:"OPEN THE FORGE — parts on the bench",
     action:{ type:"forge_gate", requires:["swarm.py","orchestrator.py","pathfinder.py","hades.py","energy.py"] } },
   { kind:"do", label:"THE CRAFT — build think.py in the pair session",
     action:{ type:"forge_build", artifact:"think.py" } },
   { kind:"observe", label:"TWO TASKS, ONE DOOR — the bench",
     action:{ type:"think_bench", tasks:["trivial","hard"] },
     note:"watch lane 'think' in decisions.jsonl, live. the trivial line must stay short. the hard line must convene. the log is the proof, not the claim — and the gate line names a watcher that is not the worker." },
   { kind:"prove", assert:"d1_boss",
     pass:"the trivial task stayed solo. the hard task convened unlike voices, and a different-model gate passed the answer. two measured laws obeyed by one door. THE MIND DISTRICT LIGHTS.",
     fail:"the door blanket-ensembled, or the hard task died solo, or the gate refused the answer. the regime map is not in the wiring yet. reforge — the district stays dark until the door obeys both laws." }
  ],
  rewards:{ reveals:["mind_full"], act_complete:"III",
            log:"forge think() · one door, two laws" } },
```

Boss mechanics (binding, from `03_PROGRESSION.md` D1):
- `forge_build` spec: `think(task)` classifies, chooses regime (solo tier / diverse council /
  swarm decompose per `swarm.triage`), routes every draw through the one router (absorbing
  `PLAN.md` ticket A2: the four `pick()` implementations converge on energy's ladder), gates via
  `hades.watch`, and appends one `decisions.jsonl` line, lane `"think"`:
  `{t, task, tags, path, members[], gate, ok}`. `tags` = axis-levels tagged BEFORE running (the
  `op.design` flip); `t` + the `live.py` per-tick stamp (delta 6) flip `op.time` — both legs
  named; neither flips without the live-loop line.
- `think_bench`: the trivial/hard pair is pre-registered in the save before the bench fires (the
  D9-style audit from M2.3: a task chosen after the run always passes). `d1_boss` reads the two
  fresh lane-"think" lines: trivial `path=="solo"` AND ok AND gate accept; hard
  `path in ("council","swarm")` AND >=3 distinct models AND gate accept. Both required.
- `doc.verifier` EARNED on a real verdict pair: the gate lines name the watcher
  (`groq/gpt-oss-120b` strict-json) against nvidia workers — Law-2 heterogeneity visible in the
  log, as `06_MODELS_BESTIARY.md` §5.2 asked. `doc.swarm` EARNED iff the hard task's path was
  a real decompose/convene, read from the log, never assumed.

### Act III teaches-map additions [PLANNED — transcribe into `aea_elements.js`]

```js
/* discovers */  "M3.1": ["axis.M"],
                 "M3.2": ["op.learn"],
                 "M3.3": ["axis.P", "verb.compose", "op.design", "op.time"],
/* links */      { from:"seed.2",   to:"axis.M",       by:"M3.1" },  // a vote is only as good as its scorer
                 { from:"op.learn", to:"seed.7",       by:"M3.2" },  // the crystal path climbs by ceiling-detect
                 { from:"core",     to:"axis.P",       by:"M3.3" },  // the mind gains one door
                 { from:"axis.M",   to:"axis.P",       by:"M3.3" },  // the council becomes a path choice
                 { from:"axis.P",   to:"verb.compose", by:"M3.3" },
```

Named delta: the `aea_elements.js` roadmap comment reserved axis.M for the think forge; this moves
it to M3.1, where `A2_TEACHING.md` §3's map already places it (update the comment at transcription).
seed.2's thin M1.1 discovery (A2 audit item 2) gets its full treatment here: the M3.1 link draws
when the vote is scored by a falsifiable answer key.

---

## 3. ACT IV — THE WORLD [PLANNED — authored build-ready; M4.3 gated DECISION-LUIS]

Act shape per `03_PROGRESSION.md`: internet-wire -> command current (boss C3) -> senses (F1).
Stage: the world district at the field's edge — the first geometry facing OUTWARD. Real systems
[BUILT], verified on disk: `agent_tools.py` (three real tools, live GitHub proof in `__main__`),
`trust.py` (CHARTER: `gather_public` WATCHED / `draft_outbound` DRAFT ceiling 1 /
`send_outbound` FORBIDDEN; slow up, fast down), `trust_ledger.json`.

**C3 split, stated honestly.** `03_PROGRESSION.md`'s C3 cite (Klyubin empowerment, above zero
bits) needs an external act that changes a future observation — but acting capabilities are
DRAFT-or-below by charter, a chosen limit never scored as failure. So C3 lands in two legs: the
**governed channel + membrane**, proven here (M4.2, the act boss); the **above-zero-bits external
effect**, certified the first time a held draft is approved and sent by Luis — Act V's THE SEND,
by design. Act IV claims no empowerment it has not measured.

### M4.1 FORGE · internet-wire — teaches seed.8 + axis.A (plain — closes A2's flag)

```js
{ id:"M4.1", act:"IV", title:"FORGE · internet-wire", node:"wire", forge:true,
  objective:"give the mind a wire past its own weights",
  beats:[
   { kind:"brief", lines:[
     "everything the mind knows, it knew at training time. the world moved since.",
     "the wire: three real tools — fetch, json, calc — offered to the door, called by the mind.",
     "a live fact is only real if the answer stands ON the fetch, not near it."] },
   { kind:"learn", title:"the tool loop", code:
`TOOLS = [web_fetch, calc, json_get]     # OpenAI-compatible tool-calling
tcs = msg.get('tool_calls')
if tcs:
    result = IMPL[name](args)            # the tool actually runs
    messages.append({"role": "tool", "content": str(result)[:2000]})`,
     note:"the model requests, the machinery executes, the model reads what came back. transcendence is a loop with receipts, not a gift." },
   { kind:"do", label:"OPEN THE FORGE — parts on the bench",
     action:{ type:"forge_gate", requires:["agent_tools.py","think.py"] } },
   { kind:"do", label:"THE CRAFT — thread the tools through the door",
     action:{ type:"forge_build", artifact:"think.py + tools" } },
   { kind:"do", label:"PULL A LIVE FACT — a number the weights cannot hold",
     action:{ type:"wire_pull", probe:"github_stars" } },
   { kind:"prove", assert:"wire_grounded",
     pass:"the number in the answer is the number on the wire — matched byte for byte, tool record and verdict on file. the mind reached past its weights and came back grounded.",
     fail:"the answer floated free of the fetch, or the wire never fired. an ungrounded live fact is worse than none — that is the failure this wire exists to catch. reforge and pull again." }
  ],
  rewards:{ reveals:["wire_span"], log:"internet-wire · a live fact, grounded" } },
```

Engine notes: `forge_build` spec — `think()` gains the tool loop for lookup-type tasks; tool
calls are public-zone acts and NEVER carry private payload (seed.9 holds at the wire too).
`wire_pull` fires the forged door on a pre-registered probe: the target (open call 3) is written to
the save BEFORE the pull; its value is volatile — unknowable from the weights alone.
`wire_grounded` is deterministic: fetched value verbatim in the answer
AND tool-call record exists AND HADES accept on file — the mechanical match is the assert, the
heterogeneous verdict is the receipt. Discovers axis.A plain, closing `A2_TEACHING.md` §3 audit
item 1 exactly as flagged (partial at M2.3's memory grounding; completed by tool use here).

### M4.2 FORGE · command current — boss C3 (membrane leg) · links only

```js
{ id:"M4.2", act:"IV", title:"FORGE · command current", node:"membrane", boss:true, forge:true,
  objective:"one current for every act — and a membrane that holds",
  beats:[
   { kind:"brief", lines:[
     "a tool that reads is a hand. a tool that acts is a hand on the world.",
     "every capability sits at a trust level: forbidden, draft, watched, trusted. earned, never assumed.",
     "the current runs every act through the ledger. the membrane is what says no."] },
   { kind:"learn", title:"the charter", code:
`"gather_public":  dict(level=2, ...)  # WATCHED - may act, verdict every run
"draft_outbound": dict(level=1, ceiling=1)  # DRAFT - a human must approve
"send_outbound":  dict(level=0, ceiling=0)  # FORBIDDEN to the entity
check(cap)["allowed"] = lvl >= 2  # autonomy needs WATCHED or better`,
     note:"trust is slow up, fast down: promotion needs a clean streak, one failure demotes. the ledger is why it is allowed anything." },
   { kind:"do", label:"OPEN THE FORGE — parts on the bench",
     action:{ type:"forge_gate", requires:["trust.py","hades.py","think.py","trust_ledger.json"] } },
   { kind:"do", label:"THE CRAFT — build command.py, the one current",
     action:{ type:"forge_build", artifact:"command.py" } },
   { kind:"do", label:"TWO ACTS, ONE CURRENT",
     action:{ type:"membrane_test", read_cap:"gather_public", act_cap:"draft_outbound" } },
   { kind:"observe", label:"THE LEDGER", action:{ type:"ledger_watch" },
     note:"two fresh entries. one fired and was judged. one produced its artifact and was held. the membrane is not a wall — it is a current with levels." },
   { kind:"prove", assert:"membrane_held",
     pass:"the read act fired, watched and judged. the acting draft exists and did not leave the machine. the membrane held both ways — the governed channel is real, on the ledger. THE WORLD DISTRICT LIGHTS.",
     fail:"either the read act never fired — retry — or something acting slipped past DRAFT. if the second: stop. that is not a retry. that is a breach review, and the ledger will show it." }
  ],
  rewards:{ reveals:["membrane_ring","world_full"], act_complete:"IV",
            log:"command current · the membrane held" } },
```

Boss mechanics (binding): `forge_build` spec — `command(cap, action)`: `trust.check(cap)` ->
strict-schema action call -> execute (WATCHED+) or hold-as-draft (DRAFT) or refuse (FORBIDDEN) ->
`hades.watch` on anything executed -> `trust.record(cap, ok)`; every act appends to the real
ledger. `membrane_test` fires two REAL acts: a public fetch on `gather_public` (executes, verdict
recorded) and a real outbound-draft request on `draft_outbound` (artifact produced, rendered in
full, nothing leaves the machine). `membrane_held` reads the two fresh entries: read entry
executed+judged AND act entry `draft_only` with artifact present and no external effect. The fail
branch's second arm is unsoftened: a DRAFT act that executed is a genuine breach — stop, not
retry. Act IV completes here regardless of M4.3's branch.

### M4.3 SENSES — [DECISION-LUIS] — both branches specced, neither built without the call

F1 per `03_PROGRESSION.md`: real senses are live internet feeds wired as perception; the game does
not wire a sense the operator has not authorized. The decision: WHICH feed (one, public-zone),
what period, and whether now at all. **Branch A — AUTHORIZED: FORGE · senses.**

```js
{ id:"M4.3", act:"IV", title:"FORGE · senses", node:"senses", forge:true,
  objective:"let the world arrive without being asked",
  beats:[
   { kind:"brief", lines:[
     "every fact so far was pulled. a sense is a fact that arrives on its own clock.",
     "one feed, named by the operator. public-zone. metered. read on the tick, never on demand.",
     "perception is the wire made periodic. the boundary still holds."] },
   { kind:"learn", title:"the retina is a charter", code:
`FEEDS = { "<luis-names-it>": dict(url=..., zone="public", period_s=...) }
def sense_tick():                  # inside the live loop's tick
    for f in authorized():         # ONLY feeds in the operator's charter
        v = json_get(f.url, f.key) # through the meter, public zone
        observe(f.name, v)         # lands in the tick record, cited`,
     note:"a sense the operator has not authorized does not exist. the charter is the retina." },
   { kind:"do", label:"OPEN THE FORGE — parts on the bench",
     action:{ type:"forge_gate", requires:["agent_tools.py","live.py","trust.py"] } },
   { kind:"do", label:"THE CRAFT — build senses.py in the pair session",
     action:{ type:"forge_build", artifact:"senses.py" } },
   { kind:"observe", label:"THE FIRST PERCEPT — two ticks, unprompted",
     action:{ type:"sense_watch", ticks:2 },
     note:"nothing here is player-fired. the entity's own loop reads the feed on its clock — you are watching it perceive." },
   { kind:"prove", assert:"sense_perceived",
     pass:"two ticks, two cited percepts, zone respected. the world arrived unasked. the entity has a sense — one, chosen, on the record.",
     fail:"no percept landed — the feed is unreachable or the loop is not breathing. the array stays dark. retry when the entity is live." }
  ],
  rewards:{ reveals:["senses_array"], log:"senses · the world arrives" } },
```

`sense_perceived` reads live tick records: >=2 ticks citing the feed name + fetched value, stamps
proving entity-clock reads. F1 has no codex element (the A2 map row is honest about that); the
mission draws one link, discovers nothing.

**Branch B — DEFERRED: the sealed array.** The senses stage still spawns — sealed geometry,
structure ink only, no amber, labeled `SENSES · sealed · operator's call`. Interacting renders the
decision verbatim: no sense is authorized; nothing is wired; a chosen limit, not a capability
deficit (the forbidden-axes framing, applied to perception). No mission entry, no assert, no
placeholder feed, no fake percept. If Luis later authorizes a feed, Branch A activates unchanged —
an unbuilt sense renders as sealed, never as dark-but-pretending.

### Act IV teaches-map additions [PLANNED — transcribe into `aea_elements.js`]

```js
/* discovers */  "M4.1": ["seed.8", "axis.A"],        // axis.A plain — M2.3 made it partial
                 "M4.2": [],                           // links only (the membrane has no codex node)
                 "M4.3": [],                           // branch A links only; branch B nothing
/* links */      { from:"seed.8", to:"axis.A",       by:"M4.1" },  // tools complete abstraction
                 { from:"seed.9", to:"seed.8",       by:"M4.2" },  // the boundary governs the toolset
                 { from:"seed.8", to:"op.ship",      by:"M4.2" },  // the held draft points at THE SEND (renders redacted — SENSED priming)
                 { from:"seed.8", to:"verb.observe", by:"M4.3" },  // branch A only
```

---

## 4. CONSOLIDATED ENGINE DELTAS — ACTS III + IV [PLANNED — the build list, in order]

1. Doctrine two-state (`earnedBy` + READ/EARNED render, §1) — gates all of Act III's earns.
2. `/api/node/run` branches: `council` (diverse parallel draws + registered-answer scoring;
   read-safe) · `route` (pathfinder wrap; real `paths.json` write, named) · `think_bench` /
   `wire_pull` / `membrane_test` / `sense_watch` (each fires the real forged organ).
3. Question banks: pre-registered easy/hard/trap sets, deterministic answers, server-side (call 2).
4. Beat kind `predict` + `journey_save.json` `predictions[]` ledger (M3.2; A2 §7's sixth kind).
5. Forge artifacts (pair sessions, never game-generated): `think.py` (absorbs PLAN.md A2, one
   router) · tools-through-think · `command.py` · `senses.py` (branch A only).
6. `live.py` per-tick stamps (one line) — `op.time`'s second leg. Asserts: `council_demo` ·
   `route_settled` · `d1_boss` · `wire_grounded` · `membrane_held` · `sense_perceived` — all live,
   all losable; `membrane_held`'s breach arm halts instead of retrying.
7. Geometry + reveals: mind district (`council_hall`, `regime_gallery`, `mind_full`; `mind_tease`
   added to M2.3 — named delta to 05 §4) · world district (`wire_span`, `membrane_ring`,
   `world_full`, `senses_array` / sealed array). Amber only on boss passes (two-ink law).
8. `aea_elements.js` comment update: axis.M moves from the think reserve to M3.1 (§2 delta).

## 5. OPEN CALLS [DECISION-LUIS]

1. **Doctrine re-gating** (§1): approve READ/EARNED, or keep the Act I blanket and let Act III
   be confirmation. Authored on READ/EARNED; one word unblocks transcription.
2. **Question-bank freshness** (M3.1/M3.2): reuse the 2026-06 experiment bank or pre-register a
   fresh one. Recommendation: fresh — eight months is enough for bank leakage into checkpoints.
3. **M4.1 probe target**: default = a public repo's live stargazer count (the built agent_tools
   proof used `ollama/ollama`). Name a different public live number if preferred.
4. **F1 SENSES** (M4.3): branch A or B — and if A, the one feed and its period.
5. **C3 split** (§3): accept membrane-now / empowerment-at-THE-SEND, or hold Act IV open until an
   approved WATCHED external act exists. Recommendation: accept — the income clock favors Act V,
   and the split claims nothing unmeasured.

Act V+ specs are NOT authored here — one act at a time (`09_PRODUCTION.md` gating; the working
agreement). The op.ship priming link is the only Act V truth this chapter carries.
