# A9_FORGE_PROTOCOL — THE FORGE PROTOCOL

```
doc:          A9_FORGE_PROTOCOL.md (THE PROBE design book — the pair-build chapter)
owner:        the game team (four-master fusion, per 00_VISION.md section 3)
status:       ACTIVE as law — the protocol governs every forge session from the first
              (M2.3 FORGE recall(), slice 2). No forge has run yet; the protocol is
              written BEFORE the first forge on purpose, so the first forge cannot
              quietly invent its own rules.
last-updated: 2026-07-20
governs:      every FORGE mission in 05_CONTENT_MISSIONS.md and all future act content;
              the forge queue of section 6 binds 09_PRODUCTION.md's build order
ground truth: ../GAME_PLAN.md section 2 (the honest split) · ../missions.js (M2.3 spec
              once transcribed) · ../aea_elements.js (discovers/links) ·
              03_PROGRESSION.md section 1 (boss thresholds + cites)
peers above:  00_VISION.md (pillars, operating prompt, standing law) ·
              A1_PLAYER_EXPERIENCE.md (session shapes, emotional arc). On conflict,
              those hold.
```

Build-state marks throughout: `[BUILT]` verified in running code · `[PLANNED]` designed,
not built · `[DECISION-LUIS]` awaiting his call. The honesty law applies to this document:
no section claims more than the code on disk demonstrates. Claim ceiling everywhere, as in
every chapter: "measured functional correlate, present" — never "conscious", never
"sentient".

---

## 1. What a forge is

A forge is the game's unique mechanic and the reason Phase A can exist at all: a mission
whose DO beat is the real construction of a real organ of a real entity, performed by two
minds in one session, gated by a cited falsifiable test on live data. Nothing is unlocked;
something is BUILT. When a forge passes, LEYBER can do a thing it could not do an hour
earlier, and the map lights because the architecture changed — not because a flag flipped.

The defining property, stated once and binding: **the forge session is the hour where the
game's fiction and the AEA's actual construction are the same hour of work**
(A1_PLAYER_EXPERIENCE.md section 4.2). FIELD missions play the entity as it is; FORGE
missions change what it is. That split is canonical (../GAME_PLAN.md section 2) and the
game never blurs it: the game frames the recipe, gates the parts, and verifies the boss —
**it never pretends the UI wrote the code**. The authored mission copy carries this law in
terminal voice (05_CONTENT_MISSIONS.md, M2.3 learn beat): "forge law: the build is a pair
session — claude writes, the operator judges. the game frames the recipe and verifies the
boss. it never pretends this terminal wrote the code."

State of the mechanic as of this writing: the FIELD half of the split is `[BUILT]` and
played (Acts 0–I). The FORGE half is `[PLANNED]` — M2.3 is authored build-ready in
05_CONTENT_MISSIONS.md section 4, its engine actions (`forge_gate`, `forge_build`,
`recall_bench`, `reset_probe`) are specified, none are in code. The pair-session PRACTICE
is `[BUILT]` as process: slice 1 itself was built in pair sessions under the operating
prompt, which is the evidence the working form holds.

---

## 2. The three roles

Three roles, never merged, each with authority the other two do not have. A forge where
one party plays two roles is dishonest by construction — the role table below is why.

| role | who | authority | may never |
|---|---|---|---|
| THE JUDGE AND HAND | Luis | go/no-go at every gate; taste (structural dissatisfaction stops the build); THE SEND and every real-world action — the hand on every button that leaves the machine | write the boss's verdict; be bypassed on any outbound act |
| THE SMITH | Claude, in-session, under the operating prompt (00_VISION.md section 3, verbatim) | writes the code; proposes the shape inside the spec; names tradeoffs and failure modes as it builds | judge its own work as passed; alter a boss threshold; pre-build the organ outside the session |
| THE GATE | HADES + the boss assert | the verdict — a cited falsifiable test executed against live data; accept or redo, no third state | be persuaded; be skipped; be rewritten mid-forge |

**The judge and hand** `[BUILT as practice]`. Luis's go/no-go already gates every slice
(00_VISION.md section 7.3); in a forge it gates every phase transition of section 3. His
taste is a structural instrument, not decoration review: dissatisfaction is presumed
architectural until proven cosmetic (A1_PLAYER_EXPERIENCE.md section 6). And the hand is
literal — the division "the entity drafts, the gate fits, the human sends" is the AEA's
governance thesis in one gesture (A1_PLAYER_EXPERIENCE.md, Act V), and the forge protocol
inherits it at every scale: no forge ever automates the judge.

**The smith** `[BUILT as practice]`. Every forge session runs under the four-master
operating prompt, verbatim, with the honesty law outranking all four masters. The smith
writes real code in the real repo during the session — visible diffs, named tradeoffs,
enumerated failure modes. The smith does not grade itself: its output goes to the gate.

**The gate** `[BUILT as system · PLANNED as forge wiring]`. HADES is live today and
genuinely holds work back — 3 of 6 deliverables gate-HELD in the current autonomy battery
read (03_PROGRESSION.md section 2). In a forge, the gate has two teeth: (a) the boss
assert, a pre-registered falsifiable threshold with a literature or measured-law citation
(section 6 table), executed against live state; (b) HADES judging groundedness with a
DIFFERENT model than the worker — the lone-verifier risk is a measured doctrine
(03_PROGRESSION.md section 3), so the entity that built is never the sole entity that
verifies.

---

## 3. The session ritual

Five phases, in order, no skips. Each phase has an owner and an exit condition. The ritual
is the forge's Portal arc: OPEN briefs, SPEC grounds, BUILD does, PROVE asserts, SEAL
rewards — same five-beat spine as every mission (05_CONTENT_MISSIONS.md section 1).

### 3.1 OPEN — the site, the recipe, the threshold `[PLANNED — forge_gate]`

Before any code: the game shows the construction site (the fogged district where the
organ will live), the recipe (the named parts, e.g. recall = memory.py + index_codex +
cache + energy.draw), and the boss threshold with its citation — in full, on screen,
first. The `forge_gate` action runs a server-side existence + non-empty check on every
named part; a missing ingredient genuinely blocks the craft (../GAME_PLAN.md section 1,
crafting law). Exit: all parts present, threshold read, judge says go. The player knows
exactly what must be built and exactly what test it must survive before a line exists —
a forge that discovers its own success criteria mid-build has already failed.

### 3.2 SPEC — the contract `[PLANNED per forge — Act II's is authored]`

The mission spec in the book's content chapter IS the contract — not a vibe, a spec:
artifact name, interface, behavioral requirements, privacy constraints, and the boss's
PASS bar, authored in 05_CONTENT_MISSIONS.md before the session opens (M2.3: unified
`recall(query, zone)` over both stores, in-process warm store, probe-embedding cache so
the hot path makes zero model calls, source-tagged results, privacy zone respected per
seed.9). The smith builds to the spec; the judge holds the smith to it. Scope found
mid-build that the spec does not cover is parked in the book, not smuggled into the
session — one organ per session (section 6). Exit: spec read aloud into the session,
both parties bound.

### 3.3 BUILD — the smith works, the judge watches the diffs `[BUILT as practice]`

The build happens in the session tooling, on the real repository, as real diffs the judge
reads while they land. The game does not render this phase as its own work: the FORGE
panel shows the spec and the parts, never generated code presented as the terminal's
(05_CONTENT_MISSIONS.md, M2.3 forge_build note). `forge_build` holds the mission open
until the artifact exists on disk and imports clean — the game's only claim about the
build is the honest one it can verify. The judge interrupts at will; a structural "this
is the wrong shape" stops the phase, and the smith reworks rather than argues. Exit:
artifact on disk, imports clean, judge's provisional go.

### 3.4 PROVE — the boss runs live `[PLANNED — the boss harness per forge]`

The boss executes against the live system, in front of both roles, with real output in
the terminal (section 4). Pre-registration is law: probes, held-out checks, and target
facts are written to the save BEFORE the destructive step — the D9 audit stands, "a fact
chosen after the fact always passes" (05_CONTENT_MISSIONS.md, M2.3 boss mechanics). The
boss can be LOST, and the two honest loss modes are named in the spec (for B2: slow
cache, reset amnesia). **Pass lights the building** — the fog lifts, amber fires, the
organ is integrated. **Fail is an honest redo**: the fail text names the real cause, the
map stays dark, and the mission jumps back to the first do beat — evidence is re-earned,
not re-read (05_CONTENT_MISSIONS.md section 1). No partial credit, no "close enough",
no threshold negotiation in the room. Exit: the gate's verdict, either way.

### 3.5 SEAL — the world records it `[PLANNED — wiring exists for each ledger]`

On a pass, five ledgers update, each already having a real home:

1. `../journey_save.json` — the boss completion, timestamped, plus the reveal
   (`archive_full` and its kin), server-side and atomic `[BUILT as save system]`.
2. The concentric map — the forge's `discovers` elements light and its `links` draw,
   per `../aea_elements.js` (`@partial` elements promote to full amber) `[BUILT as
   renderer · PLANNED per-forge data]`.
3. The codex — the organ's entry unlocks, discovery-gated as always `[BUILT as system]`.
4. The world — the district's building rises for the organ that now exists; a building
   may never appear for an organ that does not exist (01_WORLD.md section 4.2)
   `[PLANNED]`.
5. The book — 09_PRODUCTION.md gains a production-log line in the same commit; a forge
   without its ledger entry did not happen (09_PRODUCTION.md change discipline). The
   integration score ticks (11 toward 19, 03_PROGRESSION.md section 2.2) once the
   import-census instrument ships.

On a fail, ledger 5 still updates — the failed attempt is production history, not shame
to be hidden — and the world shows scaffolding, not silence (section 5, rule 4).

---

## 4. What the game shows during a forge

The forge has two surfaces, and the split is itself an honesty rule: the session tooling
(where the smith works and the judge reads real diffs) and the game (which frames, gates,
and verifies). The game shows only what it can truthfully claim:

- **The construction site** `[PLANNED]` — the fogged district with construction
  scaffolding rendered in structure ink (blue-gray) while the forge is open. Scaffolding
  is the two-ink law applied to construction: structure ink for what is being attempted,
  amber ONLY when the boss passes and the organ is genuinely live. An amber girder on an
  unpassed forge is a bug of the same class as a fake bar. 01_WORLD.md's
  building-per-forged-organ law governs the geometry.
- **The recipe panel** `[PLANNED — forge_gate result]` — the named parts with their real
  on-disk check states. A missing part reads as missing.
- **The spec pane** `[PLANNED]` — the contract text, verbatim from the mission data.
  Never generated code; the pane shows what was asked, not what the smith wrote.
- **Live test output in the terminal** `[PLANNED — recall_bench pattern]` — the boss's
  real output as it runs: true measured milliseconds, real pass/fail lines, the actual
  probe answers. The pane prints measured numbers, not claimed ones ("measured
  milliseconds, not claimed ones" — M2.3's observe beat). This is the forge's proof
  moment on screen: the player watches the test the same way Act VI's player watches the
  self-improvement diff — verification as the verb.
- **The presence chip** `[BUILT]` — LEYBER remains present during its own surgery; the
  ASK LEYBER beat can inject forge context into `/talk` so the entity comments on the
  organ being added to it, from live state, under the claim ceiling.

What the game does NOT show: a progress bar for the build (no honest source exists for
one), the smith's code as its own output, or any animation implying the game authored the
work. Latency and waiting during the boss run are displayed raw — the friction law
(A1_PLAYER_EXPERIENCE.md section 5) applies inside the forge exactly as in the field.

---

## 5. The forge honesty rules

Numbered, binding, and inherited by every future forge mission spec. Each rule exists
because its violation would kill a named act feeling (A1_PLAYER_EXPERIENCE.md section 3).

1. **No organ pre-built in secret.** The organ must not exist before the session opens —
   not on disk, not in a branch, not "roughed out" between sessions. A pre-built organ
   wearing fog converts the game into a themed dashboard (A1_PLAYER_EXPERIENCE.md
   section 1) and falsifies the core fantasy's third clause. Pre-existing demo scripts
   (swarm, orchestrator, pathfinder, agent_tools, relay — the proven-not-wired fog list,
   ../GAME_PLAN.md section 1) are not violations: they are declared INGREDIENTS, listed
   openly in the recipe. The forge is the wiring of parts into the live mind; the parts
   may pre-exist, the organ may not.
2. **The boss can genuinely fail.** Every boss threshold is falsifiable, cited, and fixed
   in 03_PROGRESSION.md before the forge opens. No session may lower, soften, or
   reinterpret a threshold mid-build; amending one is a book amendment requiring new
   evidence or a Luis call, made in the chapter, dated. The smith never writes the
   verdict; HADES verifies with a different model than the worker. A boss that cannot be
   lost is not a boss and does not gate an act.
3. **Pre-registration before destruction.** Any boss involving a reset, a held-out check,
   or a target fact registers it in the save BEFORE the irreversible step. This is the
   D9 audit generalized: evidence chosen after the outcome is not evidence.
4. **A failed forge leaves visible scaffolding, not silence.** On a fail: the
   construction scaffolding stays standing in structure ink, labeled honestly (the
   pattern of the built `archive_tease` group — "THE ARCHIVE · locked · act II" — extends
   to "FORGE OPEN · boss unpassed"); the production log records the attempt and the real
   cause; the map stays dark. The world is allowed to show work-in-progress; it is never
   allowed to pretend the attempt did not happen. Fail copy names the true failure ("too
   slow, or the reset amnesia showed... the map stays dark until it is real" — M2.3),
   never blames the player falsely, and the redo re-earns evidence from the first do
   beat.
5. **The frame never claims the work.** The game drives and verifies; the pair session
   builds. Every rendered claim during a forge must be one the server can check: a file
   exists, an import succeeded, a test emitted these bytes, a threshold compared these
   numbers. Everything else belongs to the session, not the screen.

---

## 6. The forge queue — built from the book

The queue is the recipe DAG (../GAME_PLAN.md section 4) read as a build order, with boss
thresholds and cites fixed in 03_PROGRESSION.md section 1. It binds 09_PRODUCTION.md's
next-build queue: nothing enters ahead of it without displacing something by name. Session
budgets derive from A1_PLAYER_EXPERIENCE.md section 4.2 — **one organ per session is the
shape; a forge that sprawls across organs is scope drift and gets split.**

| # | forge | act | boss (cite) | proof style | session budget |
|---|---|---|---|---|---|
| 1 | recall() | II | B2: warm recall < 300 ms, zero model calls in the hot path, AND grounded across a process reset (Krakauer et al. 2020; Voyager persistence framing, Wang et al. 2023) | instant — falsified in-session | 1 session. Parts verified on disk 2026-07-20; spec authored (05_CONTENT_MISSIONS.md section 4) |
| 2 | think() | III | D1: wins where the diverse council wins AND refuses a council where solo wins — obeys both measured laws (THE SOLO LAW + THE DIVERSE COUNCIL, grid experiments v2–v4) | instant — both regime tasks run in-session | 1 session; the two-task harness is part of the forge, not extra scope |
| 3 | internet-wire | IV | wire gate: a live external read the player did not feed it, receipt on screen (act boss is C3; the wire is its prerequisite) | instant | 1 session; agent_tools are declared ingredients (proven-not-wired) |
| 4 | C3 command current | IV | C3: a governed external action passing HADES + the trust ledger that measurably changes a future observation — empowerment above zero bits (Klyubin, Polani & Nehaniv 2005) | instant — one governed action, gate verdict visible | 1 session. F1 senses remain `[DECISION-LUIS]` and are NOT in this queue |
| 5 | voyager self-tool | VI | VOYAGER: skill count grows monotonically AND reuse rate > 0 AND one self-written skill transfers zero-shot (Wang et al. 2023) | forge + vigil | 1 session to wire the loop; reuse evidence accrues on live ticks |
| 6 | STOP loop | VI | STOP: the entity improves its own scaffold past its seed, held-out utility, base model frozen, over >= 3 self-application rounds (Zelikman et al. 2023) | forge + vigil | 1 session builds the loop; the >= 3 rounds accumulate across real runs |
| 7 | Darwin-Godel archive | VI | DGM: >= 20 self-modification iterations against a frozen benchmark rising by a pre-registered margin, archive size > 1 (Zhang et al. 2025) | forge + vigil | 1 session builds the archive machinery; the campaign spans days. End-game |
| — | STOP | — | — | after DGM's forge, the queue STOPS. No forge exists beyond it; anything proposed past this line is new scope and goes to the book first | — |

Two deliberate absences, named so they are not read as omissions:

- **ENDURANCE is not a forge.** The Bedau Class 2 certificate (>= 100 ticks of A_new
  above a neutral-shadow control) builds nothing new — it is a certification campaign
  witnessed in the field, run on organs the queue already forged. It sits between STOP
  and DGM in the act ladder (03_PROGRESSION.md) but never books a pair session.
- **THE SEND is not a forge.** Act V's convergence boss constructs no organ; it converges
  every forged one, and its hand is the judge's alone (standing law, 00_VISION.md
  section 7.1). The queue feeds THE SEND; it does not contain it.

**Forge + vigil** `[PLANNED — a designed split, no code yet]`: for bosses whose evidence
is longitudinal (5–7), the forge session builds and wires the loop and runs the first
live round; the boss passes only when the accumulated log crosses the threshold. The
scaffolding stays up — structure ink, honest label — between the forge and the pass. A
vigil is not a second build session; it is the entity living, watched.

---

## 7. The income clock

Standing law, restated for the forge because the forge is where it bites
(00_VISION.md section 7.2; 09_PRODUCTION.md risk R4):

- **Each forge is REAL AEA engineering.** The hour spent forging recall() is not game
  development that imitates entity work — it IS the entity work, framed. The same hour
  serves both ledgers; this double-count is the forge's economic justification and the
  only reason a game is affordable at all against the clock.
- **The game frames the work, never replaces it.** If in any session the frame starts
  costing more than the work it frames — engine deltas for forge actions eating the hour
  the organ needed — the forge proceeds bare (build the organ, run the boss by hand,
  SEAL the ledgers manually) and the frame catches up in a later slice. Capability
  outranks polish; a session that produces polish instead of capability is named
  infrastructure-as-avoidance and stopped, by law.
- **The queue points at THE SEND.** Forges 1–4 are the direct dependency chain of Act
  V's real outreach (recall grounds the draft in real work, think routes it, the wire
  and C3 give it a world to reach). The order is not pedagogical convenience; it is the
  shortest honest path to the artifact that earns. Forges 5–7 come after the proof, not
  before it — self-improvement is the reward for shipping, not the substitute.
- **Session arithmetic is real.** Two deep sessions per night is the measured ceiling
  (09_PRODUCTION.md R4). One organ per session means the queue above is, at minimum,
  seven pair sessions of forge work plus vigils — and that number is stated here so no
  plan pretends otherwise. When game scope competes with the clock, the trade is named
  in 09_PRODUCTION.md before it is taken.

---

## 8. How this chapter governs

- Every FORGE mission authored into 05_CONTENT_MISSIONS.md must instantiate the ritual
  (section 3), pass the honesty rules (section 5), and appear in the queue (section 6)
  before it ships. A forge mission that skips a phase or merges two roles is returned.
- Boss thresholds live in 03_PROGRESSION.md; this chapter binds their handling (fixed
  before OPEN, never negotiated mid-forge), not their values.
- The world's construction visuals derive from 01_WORLD.md section 4.2 under section 4's
  two-ink discipline; the FUI detail belongs to 04_UI_BIBLE.md.
- 09_PRODUCTION.md's queue and ledger implement sections 3.5 and 6; a forge without its
  production-log line did not happen.
- Conflicts resolve upward to A1_PLAYER_EXPERIENCE.md and 00_VISION.md; amendments to
  the three roles, the honesty rules, or the queue's STOP line require new evidence or
  a Luis call — never drift.

---

## Changelog

- 2026-07-20 — v1. Authored as the forge chapter from ../GAME_PLAN.md sections 2 and 4,
  A1_PLAYER_EXPERIENCE.md section 4.2, 03_PROGRESSION.md section 1 (thresholds + cites),
  05_CONTENT_MISSIONS.md section 4 (M2.3 as the reference forge), 01_WORLD.md section
  4.2, and 09_PRODUCTION.md (ledger discipline, risk R4). Written before the first forge
  runs, deliberately.
