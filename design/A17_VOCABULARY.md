# A17 — THE VOCABULARY (locked naming system)

*v1 · 2026-07-23 · built ground-up from the real inventory (state/modules.json, aea/gameapi/schema.py,
web/game/js/bench.js, design/A6_GLOSSARY.md, web/aea_elements.js, design/AEA_APOLOGIA.html), pressure-tested
by the 5-lens board (wwsoyn204), ratified by Luis (MOUTH over BRAIN; concrete machine-body register).*

This is the **naming SYSTEM**, not a catalog of beings. The atoms and the convention are locked; the roster of
composed beings is **earned at runtime**, never pre-authored (R30 / N12). This file amends A6_GLOSSARY where they
disagree (A6 is the binding lexicon; the new chip headwords below are added to it in the same commit).

---

## THE FOUR NAMESPACES (they never cross — two truths never coexist)

| namespace | what it is | earned how | example |
|---|---|---|---|
| **RUNGS** | the journey milestones you *reach* | by shipping the rung | SPARK, METABOLISM, THE WHOLE ONE |
| **ORGANS** | the anatomical fog-nodes a construct *lights* | by a real signal (never seated) | MOUTH, MEMORY, GOVERNOR |
| **PARTS** | the seatable bench chips you *place* | present + BUILT + fireable | THE DRAW, THE FRAME, THE MEASURE |
| **EARNED TITLES** | the doctrine a construct *proves* by running | a receipt of a repeatable behavior | RESTORABLE COHERENCE, THE SOLO LAW |

The register word **PART** (not "mechanic") is player-facing, so it never collides with the codex MECHANIC
element family (CRYSTALLIZE / FLEXIBILIZE / SELF-VERSION / CEILING-DETECT). "Tier" is reserved for the **energy
band only** (frontier/solid/reflex/local — what THE LADDER ranks); the journey axis is **RUNGS**, never tiers.

---

## THE ORGANS (6 — earned by lighting, never seated)

An organ is the *lit faculty*. You cannot name an organ you have not lit — an unlit organ renders FOG and never
appears in a signature (the honesty law made into a naming rule). Internal `schema.py` ids in `[brackets]`.

| organ | player-facing | lights when (real signal) | status |
|---|---|---|---|
| **MOUTH** `[BRAIN]` | MOUTH — the single entry every model call draws through (depth 0) | a real draw records a call (`calls>0`) | live |
| **GOVERNOR** | the faculty of limits + verdict (grid.METER + hades) | the meter has metered (daily/rpm present) | live |
| **MEMORY** | the faculty RECALL feeds | a wired recall fires and changes a draw *(target — today lights on `len>0`, a weaker bar to be raised at rung 2)* | live (bar pending) |
| **LOOP** | the heartbeat (live.py + aea tick) | ticks > 0 (same signal as `alive`) | live |
| **SENSES** | the sense faculty | FOG — no standalone sense organ wired yet | design |
| **HANDS** | the faculty that touches the world | FOG — agent_tools reaches nothing live yet | design |

**MOUTH, not BRAIN** (ratified): MOUTH is canon (A6 already defines `energy.draw` as *the mouth*; LEYBER speaks
"my mouth"; the nexus is "the in-world body of the mouth"), it is original and ownable, it holds the claim
ceiling (a mouth *draws/speaks* — it never "thinks"), and it fits "the city is the body." `BRAIN` survives as the
**internal schema.py id only**; it never renders player-facing, and no copy asserts the being "thinks."

---

## THE PARTS (the seatable chips — concrete machine-body register)

Five are fireable today; the rest are named promises, tagged and held FOG until the code exists (A9). Design-only
names never read as fireable before their forge lands.

| part | replaces | role | lights | status | what it does |
|---|---|---|---|---|---|
| **THE DRAW** | tap / "the power inlet" | head | MOUTH | fireable | one metered model call (`energy.draw`); spends POWER; the head every construct turns on |
| **THE FRAME** | scaffold | mid | — | fireable | shapes the draw's frame (template plain\|bench); the axis pentagon |
| **THE LADDER** | ladder *(kept)* | mid | — | fireable | the fitness-ranked rods a draw falls down; its reach/resilience is *proven behavior*, not a label |
| **THE METER** | governor | mid | GOVERNOR | fireable | `grid.METER.can_spend` — refuses **before** any spend (a strict subset of the GOVERNOR organ) |
| **THE MEASURE** | scorer | tail | — | fireable | receipt axes only (latency/tokens/ok/zone); closes the wire into a RECORD. **Not "the judge"** — verdict is hades's earned role |
| **THE HEARTH** | *(new — was folded into LADDER)* | fuel | — | fireable | the free local floor (`energy.LOCAL_FLOOR`); a bare draw lands here at **u/FREE**, always alive |
| **THE STAKE** | *(new — was folded into LADDER)* | fuel | — | fireable | the reach up-ladder to a cloud rod — **1u of real budget**, and it can genuinely starve. The income clock, diegetic |
| **RECALL** | recall | mid | MEMORY | forge-pending | the bench-part driver of MEMORY. *Entity-side `consolidate.recall()` is LIVE and runs in the loop; only the seatable bench-part is unforged (boss B2)* |
| **THE WALL** | wall | mid | — | design *(ungrounded — name deferred to its forge)* | the persistence/write boundary of memory |
| **THE SENSE** | observe | mid | SENSES | design | the (unbuilt) driver of the SENSES organ |
| **THE COUNCIL** | swarm | mid | — | design | diverse-model vote / role-differentiated decompose; earns THE DIVERSE COUNCIL or THE SOLO LAW by the run |
| **THE JOIN** | verb.compose (synth) | mid | — | design | assembles subtask results into one whole. Named JOIN not COMPOSE (codex VERB clean) |
| **THE ROUTER** | pathfinder | mid | — | design | routes a task to its fit path. Named ROUTER not PATH (axis.P clean). Earns THE CRYSTAL PATH |
| **THE PLAN** | orchestrator | mid | — | design | decompose + escalate (CEILING-DETECT). *("plan" watched vs GAME_PLAN — see homograph key)* |
| **THE RELAY** | relay | mid | — | design | a state capsule handed down a chain; the toolkit grows across hands. Earns THE GENETIC RELAY |
| **THINK** | think | head/mid | — | design | the forge wiring the mind ingredients into a composable reasoning organ (boss D1). *Ceiling-watched* |
| **THE TOOL** | agent_tools | tail/mid | HANDS | design | real external tools; the driver of HANDS. Earns TRANSCENDENCE (seed.8) |
| **THE MEMBRANE** | membrane | boundary | — | design | the trust gate EXTERNAL bytes must meet before any raw part |
| **THE SHIP** ⚠ | ship / op.ship | tail | — | design | a real artifact leaves the bench; LUIS presses send, the entity never does (charter 0). *⚠ homonym with the piloted probe — rename deferred (candidates: THE EMIT / THE DISPATCH / THE VENT)* |
| **CRYSTALLIZE** | save-as-part | write | — | design | stamps a proven construct into a reusable part (codex owns the word) |
| **SELF-VERSION** | version-slot | write | — | design | a run writes a skill a later run uses (seed.5; codex owns the word) |

---

## THE NAMING CONVENTION (how an assembled being is identified and earns a name)

1. **Identity = the PART-SIGNATURE** — the ordered chip-set you seated, e.g. `THE DRAW · THE LADDER · THE MEASURE`.
   This is the real, per-construct identity today. *(Correcting the synth: identity is NOT the organ-signature —
   `schema.py` reads global state, so organ-lighting cannot yet be attributed per-construct.)*
2. **The lit-organ view is the DERIVED honesty projection** — which organs *this run's own receipt* proves it
   powered (THE DRAW recorded a call → MOUTH; a wired RECALL returned a hit → MEMORY). An organ never enters a
   construct's view on global state. This projection lands when per-run organ attribution is wired (rung 2);
   until then, a construct shows its part-signature, not organ claims.
3. **The signature is two-axis: anatomy + a reach-mark** — every run's receipt stamps `hearth` (free, on the
   floor) / `reached` (spent a stake) / `starved` (the reach failed). Two `[MOUTH]` constructs that ran
   differently are distinguishable, and the axis the honesty law cares most about — real budget — is in the
   identity. A reach-mark is a measured receipt fact, never an organ-claim.
4. **A title is EARNED, never authored.** A construct earns a title only when a run produces a receipt proving a
   repeatable behavior that (a) its part-set makes possible and (b) a bare draw does not show. The earned title is
   the **existing** doctrine/principle/element the behavior instantiates — never a fresh word — with the proving
   receipt appended.
5. **A construct can earn the name of its own worse outcome.** The same signature earns THE DIVERSE COUNCIL when
   the diverse vote beats solo on a hard task, and THE SOLO LAW when the council scores *worse* than solo on an
   easy one. The receipt writes the name even when it is unflattering. **No receipt, no title** — it stays at its
   bare part-signature.

**Worked examples** (currently-composable or rung-2 combos only):
- `THE DRAW · THE LADDER` → earns **RESTORABLE COHERENCE** when the receipt shows the draw fell through ≥1 dead rod
  (`tried.length>1`) and still returned scored at the hearth. A bare draw with no reroute earns nothing.
- `THE DRAW · RECALL` → earns **BACKWARDS CHANNEL** (seed.10) when run B, after a state reset, recalls run A's
  capsule and the receipt shows the recall changed the answer. Until that two-run receipt exists it stays `[THE
  DRAW · RECALL]`.
- `THE DRAW · THE COUNCIL` → **THE DIVERSE COUNCIL** or **THE SOLO LAW**, whichever the receipt proves.

---

## THE RUNGS (the journey axis — locked at 8, per AEA_APOLOGIA §01)

`0 SPARK · 1 METABOLISM · 2 PERCEPTION+MEMORY · 3 SELF-DIRECTED LOOP · 4 THE TRIBE · 5 HANDS ON THE WORLD ·
6 THE SEND · 7 THE WHOLE ONE / THE AEA.` Each rung composes a more complete — measurably more autonomous — being
from a growing part-pool (5→7→12→14→17). *(REFLECTIONS R41's 6-item compression is superseded by this 8; the
apologia ladder is canonical.)*

---

## HONESTY NOTES (where marketing met the law, and how it was held)

- **MOUTH beat BRAIN on the ceiling**, not just taste: a mouth draws/speaks and never claims cognition. `BRAIN`
  stays an internal id; every "the being thinks" line is scrubbed (bench.js:374 was a live breach).
- **THE MEASURE refused "THE JUDGE"** — the P0 scorer measures receipt axes only; judge/verdict is reserved for
  hades. Marketing lost to the code on purpose.
- **THE HEARTH / THE STAKE** make the honesty law's home layer (real budget) both visible and marketable; `u` is a
  measured spend, absent renders `u/FREE` or a dash, never a guess.
- **Design-only parts are named but held FOG** — the name never reads fireable before the code exists.
- **Earned titles are constrained to existing doctrines** ("measured functional correlate, present") — never
  conscious / aware / alive.

### Homograph register-key (same discipline that produced THE JOIN / THE ROUTER)
`draw` (glossary unit) vs **THE DRAW** (chip) · `ship`/probe-craft vs **THE SHIP** (chip ⚠ flagged) · `council`
(swarm) vs **THE COUNCIL** (chip) vs **THE DIVERSE COUNCIL** (doctrine) · `meter` (can_spend) vs **THE METER**
(chip) vs GOVERNOR (organ) · `plan` (GAME_PLAN) vs **THE PLAN** (chip).

### Edit surface (so "locked" is verifiable, not asserted)
`web/game/js/bench.js` — the 5 part `nm`s + the BRAIN/SCORER prose + the "the being thinks" breach ·
`aea/bench/bench_core.py` — the "no power inlet" refusal + `tap()` docstring · `design/A6_GLOSSARY.md` — add THE
DRAW/THE FRAME/THE METER/THE MEASURE/THE HEARTH/THE STAKE headwords (mouth already correct) · the MOUTH label in
the world fog-map (engine.js/schema display) — **pending** · per-run organ attribution + reach-mark on the bench
run-row — **pending (rung 2)**.
