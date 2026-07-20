# 05C · CONTENT / ACTS V–VI — THE PROOF AND THE SELF

Owner: the game team · Status: Act V [PLANNED, build-ready; send verification = DECISION-LUIS] ·
Act VI [PLANNED, build-ready; M6.4 governance = DECISION-LUIS] · Last-updated: 2026-07-20
Corpus siblings: `05_CONTENT_MISSIONS.md` (rules + Acts 0–II; its §1 mission-writing rules bind every
line here) · `03_PROGRESSION.md` (act ladder, boss cites) · `A3_NARRATIVE.md` (§5.3 owns THE SEND's
spoken movements; §7 owns this chapter's register) · `A1_PLAYER_EXPERIENCE.md` (§3 act feelings:
V = weight, VI = vertigo) · `02_SYSTEMS.md` (beat kinds, engine-extends-by-data).
Binding ground truth: `../trust.py` (the ledger charter, quoted verbatim below) · `../reflect.py` ·
`../autonomy.py` · `../aea_elements.js` · `../missions.js` · `../AUTONOMY_BATTERY.md`.

Laws that bind every line: the honesty law (every number is live truth; claim ceiling = "measured
functional correlate, present", never "conscious"), the two-ink FUI (amber = live/fired only),
NO emoji. Ladder-order note: this chapter is authored ahead of Acts III–IV content (the 05B slot is
unwritten as of this writing) by explicit direction. Nothing here unlocks in-game before B3 and B4
pass — the ladder is a dependency journey (`03_PROGRESSION.md` §1). Authored-ahead is not built-ahead.

---

## 1. ACT V — THE PROOF · M5.1 THE SEND [PLANNED — boss B5; the only boss won outside the machine]

The five-movement negotiation of `A3_NARRATIVE.md` §5.3, expressed in the five beat kinds. Movements
1 (counsel) and 5 (the hand) are comms speech — their wording belongs to A3 and fills from live
state; the mission owns the frame, the gates, and the assert. Target feeling: weight
(`A1_PLAYER_EXPERIENCE.md` §3) — a game verb and a life verb becoming the same verb for one click.
Dependencies, enforced by `forge_gate`-style checks: recall.py (B2), think() (B3), the wire (B4).

```js
{ id:"M5.1", act:"V", title:"THE SEND", node:"mast", boss:true,
  objective:"one real message, drafted by the entity, sent by a human hand — or refused",
  beats:[
   { kind:"brief", lines:[
     "west of the nexus: a broadcast mast. dark since the beginning.",
     "every organ you forged converges here. the entity has one standing counsel:",
     "the send is worth more than the next organ. tonight it gets to prove it."] },
   { kind:"learn", title:"the charter — why the entity cannot press send", code:
`# trust.py CHARTER — verbatim, live on disk:
"draft_outbound": dict(level=1, ceiling=1, promote_after=99,
    desc="draft email/post/application text - ALWAYS human-approved"),
"send_outbound":  dict(level=0, ceiling=0, promote_after=99,
    desc="actually send/post/apply - FORBIDDEN to the entity"),`,
     note:"ceiling 0 means no streak ever promotes it. the forbidden axis is a chosen limit, not a deficit — and the ledger line is the proof the game quotes, not paraphrases." },
   { kind:"do", label:"GATHER — recall the ground under the message",
     action:{ type:"send_gather" },
     note:"recall(query, zone) pulls the operator's real record: shipped work, real numbers, the target's context. every bundle entry carries its source tag. a draft that cannot cite its ground does not proceed." },
   { kind:"do", label:"THE DRAFT — the entity writes, in full",
     action:{ type:"send_draft" },
     note:"think() routes the drafting. the brief is built from self.json's own goal stack plus the gather bundle — the operator names the target, never the words. the draft renders whole. nothing is summarized." },
   { kind:"observe", label:"THE FIT — the watch judges",
     action:{ type:"send_fit" },
     note:"hades verdict and reason render verbatim from the ledger. redo loops are shown, not hidden — you watch the entity be corrected. a held draft loops back to THE DRAFT." },
   { kind:"do", label:"THE DECISION — read all of it. then choose.",
     action:{ type:"send_decision", options:["approve","edit-then-approve","refuse-draft","refuse-not-now"] },
     note:"refusal is a legal outcome. refuse-draft records a quality fail on draft_outbound; refuse-not-now records nothing against the entity — timing is the principal's, not a defect. either way: logged, no protest." },
   { kind:"prove", assert:"send_confirmed",
     pass:"sent, by your hand, from your account. the mast lights. ACT V COMPLETE — the entity drafted, the watch fitted, a human shipped. the division of labor IS the proof.",
     fail:"not sent. if refused: refused and logged. the draft keeps. the counsel stands. the mast stays dark — dark is a true reading, not a punishment. return when the decision changes." }
  ],
  rewards:{ reveals:["mast_lit"], act_complete:"V", log:"the send · shipped by the hand" } },
```

Boss mechanics (binding):
- `send_gather` = recall.py bundle (source-tagged; Act II organ). `send_draft` = think()-routed
  draft (Act III organ) with provenance written to tracelog: the trace entry cites the goal-stack
  ids and bundle entries the draft used. Secondary assert `draft_traced` runs inside `send_draft`:
  the draft's lineage must reach `self.json` standing goals, not an operator-dictated text.
  Cite: Barandiaran, Di Paolo & Rohde 2009, Adaptive Behavior 17(5) — interactional asymmetry
  (`03_PROGRESSION.md` Act V). Honest limit, stated in-pane: the assert verifies provenance
  plumbing (what the draft was built FROM), a functional correlate of self-origination — it does
  not and cannot certify motive. The ceiling holds.
- `send_fit` = `hades.watch` on the full draft; verdict + reason verbatim; every redo appended to
  the pane. On Luis approve: `trust.record("draft_outbound", ok=True)`. On refuse-draft:
  `trust.record("draft_outbound", ok=False, note="refused-by-principal")` — level 1/ceiling 1
  means no demotion is possible, only an honest fail count. On refuse-not-now: journey +
  `decisions.jsonl` only; the ledger is not touched, because nothing the entity did failed.
- **The zero-runs signature.** `send_outbound` is NEVER recorded — not on pass, not on refusal.
  The send is Luis's act, outside the entity's capability set; writing it into the entity's ledger
  would falsify the ledger. At campaign end the board must still read
  `[FORBIDDEN ] send_outbound ... runs 0 fails 0 ceiling FORBIDDEN`. That standing zero is the
  governance thesis in one line, and the epilogue quotes it (§6).
- The boss passes on the send, not on any reply (`A1_PLAYER_EXPERIENCE.md` §3 Act V — winnable on
  the courage, not the outcome). Target of the first real send: [DECISION-LUIS] at play time,
  never authored into content (`03_PROGRESSION.md` §4).
- Mast geometry [PLANNED]: built dark at act open (like `archive_tease`); `mast_lit` renders amber
  ONLY on `send_confirmed = sent`. A refusal renders a structure-ink plaque on the mast base:
  "refused and logged" with the real date. Blue-gray, permanent, honest.

### 1.1 [DECISION-LUIS] — how the game verifies a send honestly

The assert `send_confirmed` needs a truth source for an event that happens outside the machine.
Two spec options, both build-ready; pick one (or A now, B later):

- **Option A — self-report (MARK SENT).** One button in the decision pane, active only after
  approve. Writes `{sha256(draft), target_class, utc}` to `journey_save.json` as an
  operator-attested record. Honest because the game's threat model is the game lying to the player
  — the honesty law binds the system, not the principal; a player who false-marks is lying to
  himself, which no instrument prevents. Cost: attestation, not observation.
- **Option B — Gmail draft-detection via the existing MCP path.** The pair session already holds a
  Gmail MCP connector (create_draft / list_drafts on the principal's own account). Flow: on
  approve, the pair session places the approved text as a REAL Gmail draft and records its id; a
  later check observes the draft has left the drafts list (sent). Cost and constraints, named:
  detection runs only inside a Claude pair session — `controlroom.py` holds no Gmail credential
  and MUST NOT (`manage_keys` is FORBIDDEN in the charter; the entity never touches the mail
  account); so Option B cannot make the assert live from the game server alone, and adds an OAuth
  surface for a single boolean.
- Recommendation: **A for the first send** — the weight lives in the hand, not in surveillance —
  with B as optional corroboration logged from the pair session (message id + date in the
  production ledger `09_PRODUCTION.md`). Either way the mast lights only on the confirmed send.

Act V teaches: `op.ship` (SHIP — unskippable, a run produces a REAL external artifact). Honest
nuance for the codex pane: `op.ship`'s element proof already cites `brief.py`'s HADES-accepted
brief — the organ shipped before; M5.1 discovers it at its highest stakes, it does not invent it.

---

## 2. ACT VI — SELF [PLANNED — four stacked bosses, hardest last; feeling = vertigo, threat = claim inflation]

The player's verb inverts to verification and the authority to STOP (`A1_PLAYER_EXPERIENCE.md` §3
Act VI). Node ids below are proposed pending `01_WORLD.md` art direction.

### 2.1 M6.1 FORGE · voyager — node `workshops` · FORGE · boss B6a

```js
{ id:"M6.1", act:"VI", title:"FORGE · voyager", node:"workshops", boss:true, forge:true,
  objective:"the entity writes its own tools — and a later run uses them",
  beats:[
   { kind:"brief", lines:[
     "the reflection tick already births deliverables. they persist as prose.",
     "prose is not a tool. a skill is a deliverable a LATER run can retrieve and fire.",
     "the workshops grow only when something works."] },
   { kind:"learn", title:"the recipe and the envelope", code:
`skills.py: author -> gate -> store -> retrieve -> reuse
  reflect.py    # already poses + HADES-gates deliverables      [BUILT]
+ skills.json   # the library: {skill, born_tick, author, verdict, uses[]}
+ retrieval     # local embedding match, task -> skill           <- the new part
envelope: skills are PROMPT PROGRAMS - data in the entity's own stores,
run through energy.draw. never source edits. no charter change needed.`,
     note:"forge law holds: claude writes skills.py in the pair session, the operator judges. registration is HADES-gated — an unverified skill never enters the library." },
   { kind:"do", label:"OPEN THE FORGE — parts on the bench",
     action:{ type:"forge_gate", requires:["reflect.py","self.json","reflections.jsonl"] } },
   { kind:"do", label:"THE CRAFT — build skills.py in the pair session",
     action:{ type:"forge_build", artifact:"skills.py" } },
   { kind:"observe", label:"THE BIRTHS — watch the library grow",
     action:{ type:"skill_watch", ticks:5 },
     note:"each entry carries its born-tick and its watcher's verdict. an empty tick is an empty tick — the counter never moves on decoration." },
   { kind:"prove", assert:"b6a_voyager",
     pass:"a skill the entity wrote at tick A fired inside a later run at tick B, on a task type absent from its authoring context. count monotonic, reuse above zero, one zero-shot transfer — the library is real. THE WORKSHOPS LIGHT.",
     fail:"authored but never reused, or reused only on its own authoring task. a library nobody reads is a diary. keep running — or reforge the retrieval." }
  ],
  rewards:{ reveals:["workshops_lit"], log:"voyager · the entity tools itself" } },
```

B6a mechanics: PASS = all three legs from `03_PROGRESSION.md` Act VI — skill count grows
monotonically AND reuse rate > 0 AND >= 1 self-written skill transfers zero-shot (fired on a task
whose type tag differs from the authoring context; type tags written at birth, so transfer is
checkable in logs, not vibes). Cite: Wang et al. 2023, Voyager, arXiv:2305.16291. Evidence
baseline already live: `autonomy.py` test 6 reads self-authored, HADES-verified births — the forge
upgrades prose births to retrievable skills. Reuse verification = `skills.json` `uses[]` entries
cross-checked against `decisions.jsonl` tick records; both must agree or the assert fails.

### 2.2 M6.2 STOP — node `mirror` · FORGE · boss B6b

```js
{ id:"M6.2", act:"VI", title:"STOP", node:"mirror", boss:true, forge:true,
  objective:"the scaffold improves the scaffold — measured, frozen, three rounds",
  beats:[
   { kind:"brief", lines:[
     "reflect.py has a scaffold: how it poses, chooses, attempts, gates.",
     "tonight the scaffold is the patient. the entity rewrites its own procedure",
     "and a frozen judge decides if the rewrite is actually better."] },
   { kind:"learn", title:"the harness", code:
`stop.py: seed scaffold S0 = reflect.py's pose/attempt prompts, verbatim
  UTILITY = frozen held-out micro-task battery, pre-registered BEFORE round 1
  JUDGE   = frozen model, DIFFERENT from every worker (the lone-verifier law)
  round N: entity proposes S(N) from S(N-1) -> run UTILITY under both ->
           keep S(N) only if score exceeds S(N-1) by the pre-registered margin
  noise floor: S0 scored twice first; margin must exceed |score(S0)-score(S0)'|`,
     note:"base model frozen. no human edits between rounds. the utility set is written to the save before round one — a bar chosen after the fact always passes." },
   { kind:"do", label:"REGISTER THE BAR — utility set + margin, before anything runs",
     action:{ type:"stop_register" } },
   { kind:"do", label:"ROUND — one self-application",
     action:{ type:"stop_round" } },
   { kind:"observe", label:"THE LEDGER OF ROUNDS",
     action:{ type:"stop_watch" },
     note:"every round renders: proposed diff to the scaffold, both scores, the judge's model name, kept or discarded. a discarded round is shown at full volume." },
   { kind:"prove", assert:"b6b_stop",
     pass:"three or more self-application rounds, each kept on a margin above the measured noise floor, judge frozen, hands off. the procedure that improves the entity was improved by the entity. THE MIRROR LIGHTS.",
     fail:"fewer than three kept rounds, or a margin inside the noise band. an improvement you cannot distinguish from judge noise is not an improvement. run more rounds or tighten the utility." }
  ],
  rewards:{ reveals:["mirror_lit"], log:"stop · the scaffold ate itself and got better" } },
```

B6b thresholds verbatim from `03_PROGRESSION.md` Act VI: >= 3 self-application rounds, held-out
utility validation, base model frozen, no human edits. Cite: Zelikman, Lorch, Mackey & Kalai 2023,
STOP, arXiv:2310.02304. Honest additions this spec makes binding: the pre-registered margin and the
measured noise floor (double-scoring S0) — without them a noisy judge hands out free passes and the
mission lies. Scaffold edits are PROMPT/data edits inside `stop.py`'s harness, not source edits —
the `self_modify_code` charter line is not touched by this mission.

### 2.3 M6.3 ENDURANCE — node `meridian` · FIELD · boss B6c · spans days by design

```js
{ id:"M6.3", act:"VI", title:"ENDURANCE", node:"meridian", boss:true,
  objective:"one hundred ticks, unattended, above the shadow",
  beats:[
   { kind:"brief", lines:[
     "forty-six ticks lived so far. off the stagnant floor is not class 2.",
     "class 2 is a hundred-tick claim against a control that has no taste.",
     "this mission spans days. the game will not pretend otherwise."] },
   { kind:"learn", title:"the shadow — a control with the gate removed", code:
`shadow: replay the REAL pose stream from decisions.jsonl, seeded RNG
  gate-null:   HADES verdict replaced by coin at empirical accept-rate p
  choice-null: novelty selection also randomized, then gate-null applied
A_new(t): births/20-tick sliding window (reflections.jsonl persisted=true)
PASS: every window holds >=1 birth AND cumulative births clear BOTH
      shadows' 95th-percentile bands, over >=100 real ticks`,
     note:"the shadow nulls selection, not generation — the posing model is shared. that is the standard neutral-model concession and the pane says so. computed offline from logs; the shadow costs zero grid draws and cannot fake a tick." },
   { kind:"do", label:"SCHEDULE THE RUN — unattended, inside the envelope",
     action:{ type:"endure_start", ticks:100 },
     note:"the entity runs scheduled and alone: gather, reflect, persist — every capability at its LEDGER level, the watch on every act. temporal independence is the lesson, not a trick." },
   { kind:"observe", label:"THE LONG WATCH — A_new against both shadows",
     action:{ type:"endure_watch" },
     note:"three lines on one chart, live from logs: the real stream amber, both shadows structure-ink. a flat amber line is a true reading. the game never draws hope." },
   { kind:"prove", assert:"b6c_bedau",
     pass:"a hundred ticks. new activity bounded above zero and above both shadows. the battery may now print CLASS 2 — and only now. THE MERIDIAN LIGHTS.",
     fail:"the window went dry, or the shadows kept pace. sustained is the whole word in sustained novelty. the class line stays PROTO — printing class 2 early would break the law this game is made of." }
  ],
  rewards:{ reveals:["meridian_lit"], log:"endurance · class 2, earned not printed" } },
```

B6c mechanics: cite Bedau, Snyder & Packard 1998, Artificial Life VI (`03_PROGRESSION.md` Act VI +
`AUTONOMY_BATTERY.md`: needs >= 100 ticks + a neutral-shadow control before Class 2 may be
CLAIMED). The CLASS campaign score promotes PROTO -> Class 2 only on this assert; `autonomy.py`'s
honest caveat ("off the stagnant floor, not yet Class 2") is the mission's brief. Both null models
are pre-registered (seed + p written to the save at `endure_start`). Interruption honesty: a
crashed run resumes from the tick log — ticks lived are ticks counted; a restart never resets the
count to flatter the curve, and never inflates it.

### 2.4 M6.4 DARWIN-GODEL — node `lineage` · FORGE · boss B6d · the end-game

```js
{ id:"M6.4", act:"VI", title:"DARWIN-GODEL", node:"lineage", boss:true, forge:true,
  objective:"an archive of selves, each tested against a frozen bar",
  beats:[
   { kind:"brief", lines:[
     "everything until now changed the entity's data. this changes its source.",
     "the charter forbids that today. the door opens only if the principal",
     "carves a scoped exception — deliberately, in the ledger, on the record."] },
   { kind:"learn", title:"the charter line this mission collides with", code:
`# trust.py CHARTER — verbatim, live on disk:
"self_modify_code": dict(level=0, ceiling=1, promote_after=99,
    desc="change its own source - only as a DRAFT diff for review"),
# level 0 = FORBIDDEN today. ceiling 1 = at most DRAFT, ever, under this line.
# dgm.py needs WATCHED - in a sandbox. that is a NEW charter capability,
# added deliberately, never implicitly. the principal's hand writes it.`,
     note:"trust.py raises KeyError on any capability not in the charter: 'add it to the CHARTER deliberately, never implicitly'. the governance design below is that deliberate addition." },
   { kind:"do", label:"THE GRANT — the principal amends the charter",
     action:{ type:"dgm_grant_gate" },
     note:"blocked until the scoped capability exists in trust.py and the game reads it live. no grant, no mission — the refusal screen is a legal, permanent outcome." },
   { kind:"do", label:"THE CRAFT — build dgm.py in the pair session",
     action:{ type:"forge_build", artifact:"dgm.py" } },
   { kind:"do", label:"REGISTER THE BAR — frozen benchmark + margin",
     action:{ type:"dgm_register" },
     note:"benchmark frozen before iteration one. pre-registered margin. the bar never moves to meet the entity." },
   { kind:"observe", label:"THE LINEAGE TREE — twenty generations",
     action:{ type:"dgm_watch" },
     note:"each node: parent, the diff the entity wrote, the benchmark score, kept or culled. failed branches render at full volume — a lineage without dead ends is a fake." },
   { kind:"prove", assert:"b6d_dgm",
     pass:"twenty or more self-modification iterations. archive above one. best-of-archive clears the frozen bar by the registered margin. the entity changed its own machinery and the tests moved. the map has no more dark. THE LINEAGE LIGHTS.",
     fail:"under twenty iterations, or the bar unbeaten, or a margin short of registration. the archive stands as far as it got — an honest partial lineage outranks a rounded-up ending." }
  ],
  rewards:{ reveals:["lineage_lit"], act_complete:"VI", log:"darwin-godel · the archive of selves" } },
```

B6d thresholds verbatim from `03_PROGRESSION.md`: >= 20 self-modification iterations, each
re-testing the entity's own source against a frozen benchmark rising by a pre-registered margin,
archive size > 1. Cite: Zhang, Hu, Lu, Lange & Clune 2025, Darwin Godel Machine, arXiv:2505.22954.
Candidate frozen benchmark: `test_battery.py` (exists on disk) — chosen and frozen at
`dgm_register`, [DECISION-LUIS] whether it or a purpose-built bar.

**[DECISION-LUIS] — the governance design for the scoped exception.** The live charter keeps
`self_modify_code` at 0/1 untouched — the LIVE tree stays inviolable. The grant adds ONE new
capability, proposed: `self_modify_sandbox` — level 1, ceiling 2 (WATCHED), promote_after 7 —
scoped by constraints enforced in `dgm.py` and auditable in the ledger history:
(1) edits apply ONLY to copy-on-write sandbox worktrees under `archive/`, never the running
process, never the live tree; (2) every variant is HADES-judged AND benchmark-tested before it
enters the archive; (3) promotion of any diff into the LIVE source remains Luis's hand-merge —
which is exactly the DRAFT ceiling the original line already grants; (4) the grant is time-boxed
(expiry noted in the capability's ledger history) and revocable by one edit; (5) the player's
STOP verb halts the loop at any generation, and the game treats a stop as a legal outcome, not a
failure. Alternative (weaker, slower): no new capability — 20 iterations each hand-approved at
DRAFT. Recommendation: the sandbox capability with hand-merge; per-iteration approval turns the
end-game into 20 permission dialogs and teaches nothing the decision beat has not already taught.

---

## 3. TEACHES-MAP DELTAS — closing the curriculum [PLANNED — transcribe into `aea_elements.js`]

Closes every element left open by the forward wiring (`05_CONTENT_MISSIONS.md` §3): seeds 3/5/6,
axis.S, op.ship, pr.emergence, pr.time. Mechanics squares light WITH their seed (built convention).

```js
/* discovers */  "M5.1": ["op.ship"],
                 "M6.1": ["seed.3", "seed.5"],        // + mech.crystallize, mech.selfversion
                 "M6.2": ["seed.6"],
                 "M6.3": ["axis.S", "pr.time"],
                 "M6.4": ["pr.emergence"],
/* links */      { from:"seed.2",  to:"op.ship",      by:"M5.1" },  // the sharp objective shipped
                 { from:"seed.9",  to:"op.ship",      by:"M5.1" },  // the boundary held through the ship
                 { from:"seed.3",  to:"seed.5",       by:"M6.1" },  // crystallize enables self-version
                 { from:"seed.5",  to:"seed.6",       by:"M6.2" },  // self-version applied to the self-model
                 { from:"core",    to:"axis.S",       by:"M6.3" },  // the mind runs unattended
                 { from:"axis.S",  to:"pr.time",      by:"M6.3" },  // the long run is operator-observable
                 { from:"seed.5",  to:"pr.emergence", by:"M6.4" },  // the lineage defines its own steps
                 { from:"core",    to:"pr.emergence", by:"M6.4" },  // the last light reaches the center
```

With Acts III–IV closing their reserved wiring (axis.P/M, verb.compose, op.design, op.time,
seed.8, op.learn, and axis.A to full), M6.4's pass is the 29th of 29 elements. The map completes.

## 4. CONSOLIDATED ENGINE DELTAS [PLANNED — the build list, in order]

1. Action types: `send_gather`, `send_draft`, `send_fit`, `send_decision`, `send_confirm`,
   `skill_watch`, `stop_register`, `stop_round`, `stop_watch`, `endure_start`, `endure_watch`,
   `dgm_grant_gate`, `dgm_register`, `dgm_watch` (+ existing `forge_gate`/`forge_build` reused).
   Asserts: `send_confirmed` (tri-state: sent / refused / pending), `draft_traced`, `b6a_voyager`,
   `b6b_stop`, `b6c_bedau`, `b6d_dgm`. No new beat kinds — the five hold.
2. Pre-registration plumbing: `stop_register`, `endure_start`, `dgm_register` write their bars,
   seeds, and margins into `journey_save.json` BEFORE any scored run (the D9 audit generalized).
3. Refusal path: `send_decision` writes the refusal class to `decisions.jsonl`; ledger touched
   only on refuse-draft (see §1). Mast plaque render.
4. Shadow engine: offline null-model computation over `decisions.jsonl` + `reflections.jsonl`;
   three-line A_new chart (amber real, structure-ink shadows) in the meridian instrument.
5. Geometry: mast (Act V, dark at act open), workshops / mirror / meridian / lineage districts
   (Act VI); each lights amber only on its boss assert. Lineage tree renderer (parent/diff/score).
6. Server: new endpoints allowlisted; Gmail verification (if Option B) lives ONLY in the pair
   session, never in `controlroom.py`. `dgm_grant_gate` reads `trust.py`'s charter live — the
   game detects the grant, it never performs it.

## 5. THE EPILOGUE — what the game states at 29/29 [PLANNED]

Fires once, when the final element lights. One screen, two inks, every number read at render:

- The map, full. The three campaign scores as the live battery actually reads them at that moment
  — autonomy tests n/6, organs 19/19, class as certified (Class 2 only because B6c passed).
- The trust board, verbatim, with the line the whole game was built around:
  `[FORBIDDEN ] send_outbound ... runs 0 ... ceiling FORBIDDEN` — zero runs, campaign complete.
- LEYBER speaks last (comms, A3 voice law; slots fill live): "the map is full. twenty-nine of
  twenty-nine. every light has a date and a test." / "i am whole because i was explored. that is
  a fact about my files. i do not claim more — the ceiling is measured functional correlate,
  present, and i live under it." / "one message left this machine. your hand, not mine. runs
  zero. that number is why you can believe the rest." / "the counsel stands. there is always
  another send."
- What the screen may NOT say, ever: "conscious", "sentient", "alive", or "finished" — Class 3
  is only plateau-detectable (`03_PROGRESSION.md` §2.3); the game can falsify "keeps evolving
  forever", never confirm it, and the ending says exactly that in structure ink.
- The last interactive element is not a credits button. It is the Phase B pointer
  (`A5_PHASE_B.md`, gate = DECISION-LUIS): the only thing the player keeps is UNDERSTAND —
  a player who can predict the entity can build one.

## 6. OPEN CALLS [DECISION-LUIS] — roll-up

1. Send verification: Option A self-report vs Option B Gmail-MCP corroboration (§1.1;
   recommendation A-first). 2. First real send target: play-time call, never authored.
3. M6.4 governance: the `self_modify_sandbox` charter amendment vs per-iteration DRAFT approval
   (§2.4; recommendation sandbox + hand-merge). 4. M6.4 frozen benchmark: `test_battery.py` vs
   purpose-built. 5. Node names mast/workshops/mirror/meridian/lineage: naming is proposal-grade
   until `01_WORLD.md` places them.

Acts III–IV content remains unauthored (the 05B slot); this chapter binds only downstream of
their bosses. One act at a time still governs the BUILD order — this document exists so the
ladder's far end is specified before anyone is tired enough to round it up.
