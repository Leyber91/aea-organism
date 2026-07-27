# THE AEA'S OWN LAYERS, MAPPED ONTO THE SIX WORLDS

*2026-07-27. Read from `THE_WALK.md`, `00_VISION.md`, `A8_AEA_ALIGNMENT.md` and `state/modules.json`,*
*not from memory. Where a name collides with a world component the collision is stated.*

---

## TWO DIFFERENT THINGS THAT ARE EASY TO CONFLATE

**THE AEA HAS FIVE AXES.** `aea/mind/axes.py:29` — `AXES = ("P", "A", "M", "R", "S")`, each running
L0–L5, and the walk is scored as `sum(levels) / (TOP * len(AXES))`. Position currently reads **1 of
25**. This is the AEA's own coordinate system, in running code.

**THE GAME HAS FOUR DESIGN PILLARS.** `00_VISION.md §2` — tests every design decision is measured
against, the first being *diegetic truth*: the interface IS the fiction, the same bytes. They sit
alongside the honesty law and the claim ceiling, and **a law does not live in a world, it governs all
of them.**

*An earlier version of this file corrected "five pillars" to "four" and was answering about the wrong
document. Five was right — for the axes.*

---

## THE FIVE AXES ARE THE WORLD PROGRESSION

This is the strongest convergence in the map, and it was not designed in: the six worlds were derived
from CLASS names, the five axes from canon's coordinate system, and they land on each other.

| axis | canon's own definition | world |
|---|---|---|
| **R** · prompting | bare → framed | **1 · THE ANSWERER.** THE FRAME |
| **P** · path | L0 single call → L3 multi-step plan **+ critique** | **2 · THE WITNESS.** THE CRITIC |
| **M** · multiplicity | L0 one path → L3 **a council of N** | **2 · THE WITNESS.** THE COUNCIL |
| **A** · abstraction | the task with a **real recalled memory** injected | **3 · THE REMEMBERER.** RECALL |
| **S** · async | L0 synchronous → **a receipt timestamped while nobody was watching** | **4 · THE KEEPER** |

**S lands exactly on World 4's faculty** — *it runs while nobody is watching* — which was derived
independently from the class name. Two decompositions, arrived at separately, agreeing.

**And the two worlds with no axis are the two with no evidence.** World 5 (THE HAND, `act-external`)
and World 6 (THE APPRENTICE, the ops and the innovation layer) have no growth axis in canon, because
they are not movement along a coordinate — they are **capabilities the entity acquires** and **things
that happen TO the map.** The axes measure growth; those two change what is growing.

---

## THE LAYERS, AND WHERE EACH LANDS

`THE_WALK.md` decomposes the AEA into ten layers. The six worlds decompose it by CLASS. They are
different cuts of the same body, and this is how they intersect.

| AEA layer | census | world | state |
|---|---|---|---|
| **LAYER 1 · THE AXES** (C-11, C-06 R/A/P/M/S) | 5 ladders | **none — cross-cutting** | The axes are the coordinate system growth is measured ON. They are not components to seat. `axes.py` exists, position reads 1/25 |
| **LAYER 2 · THE FLOOR SEEDS** (C-12..C-17) | 6 | **Worlds 1 and 2, almost entirely** | see below |
| **LAYER 2 · THE STAIRCASE SEEDS** (C-18..C-22) | 5 | **Worlds 2–3** | C-21 `hypothesize` is *the census's headline hole*, unbuilt |
| **LAYER 3 · THE MECHANICS** (C-23..C-26) | 4 | **World 2 and World 3/4** | split below |
| **LAYER 4 · THE TRANSCENDENCE OPS** (C-27..C-30) | 4 | **World 6 · THE APPRENTICE** | canon's cleanest finding: *ops are things that HAPPEN TO the map, not nodes on it* |
| **LAYER 5 · THE INNOVATION LAYER** (C-31..C-58) | 28 | **World 6** | *"the deepest stratum, 28 items, **absent**"* |
| **LAYERS 6–9 · PRINCIPLES + ENGINEERING** (C-59..C-75) | 17 | **World 2 and World 4** | recovery, capability matrix, `pick_for_role`, resource monitors |
| **LAYER 10 · THE RECEIPT** | — | **all six** | a law, like the pillars |

### The six floor seeds, one by one

| seed | census | world | measured? |
|---|---|---|---|
| goal-presence | C-12 | **1 · ANSWERER** | **yes.** 0 of 158 clean trials with no objective |
| perception | C-13 | **2 · WITNESS** | compressed, not isolated |
| coordination (plan-act-critique) | C-14 | **2 · WITNESS** | **yes.** THE CRITIC, x20 |
| coherence | C-15 | **2 · WITNESS** | **yes.** THE MEASURE, a gauge, fooled 0 of 153 |
| substrate-variation | C-16 | **cross-cutting** | **yes, and it is Law IV.** Not a world component — it is the *fuel* axis every world runs on |
| self-model | C-17 | **2 · WITNESS** | **yes.** `Caecus interioris` — 2 of 5 rods cannot host a question about themselves |

**Five of six floor seeds land in Worlds 1 and 2.** That is not an accident of where we spent effort —
**the AEA's floor IS the first two worlds**, and it is the only part of the architecture with
measurements because it is the only part that is built.

### The four mechanics

| mechanic | census | world | note |
|---|---|---|---|
| flexibilize | C-20/C-24 | **2 · WITNESS** | *"every draw at any time falls through the ladder"* — this is World 2's `LADDER`, and it is `[BUILT live]` |
| ceiling-detect | C-26 | **2 · WITNESS** | meta: it *triggers other mechanics by recognising exhaustion* rather than acting |
| crystallize | C-19/C-23 | **3 · REMEMBERER** | *"the toolkit grows while no mission is running"* — `[PLANNED live]` |
| self-version | C-25 | **4 · KEEPER** | *"skills persist and compound across runs without ceremony"* — `[PLANNED live]` |

---

## WHEN CAN IT CALL EXTERNAL TOOLS

**World 5 · THE HAND · ACT.** The capability is `act-external` and it is already in the entity's closed
vocabulary. Two modules carry it today:

| module | file | status | unlock |
|---|---|---|---|
| `agent_tools` | `io/agent_tools.py` | **INGREDIENT** — not built | **Act IV** |
| `telegram_bridge` | `organs/telegram_bridge.py` | BUILT | Act IV |

`agent_tools` is `web_fetch`, `json_get` and `calc` — *"the one eval in the organ population,
regex-fenced, scrubbed builtins"*, gated behind trust `gather_public` at `min_level: WATCHED`, and it
**benches after the wire forge**.

**MCP appears nowhere in this repo.** Adding it would be a new `act-external` module under the same
trust gate and the same unlock — it is not a new capability class, it is a second transport for one
the architecture already names.

**And the warning is already on record**, from the innovation layer's own receipt: **16.8% of emitted
actions invent a tool name.** Any protocol layer needs a validator that catches every one, and canon
says we must reproduce that catch before trusting it.

---

## THE STRUCTURAL FACT THIS MAP MAKES VISIBLE

Worlds 1 and 2 hold the AEA's **floor** — six seeds, the mechanics that fire every tick, the
principles. Built, and measurable, which is why they have evidence.

Worlds 4, 5 and 6 hold the **ops and the innovation layer**: 32 census items, described in canon as
*absent* and *the deepest stratum*. `agent_tools` is an INGREDIENT. `hypothesize` is the headline hole.

**So the thinness of the later worlds is not a research failure — it is the architecture's own shape.**
The AEA is built at the bottom and declared at the top, and the game inherits that exactly. World 6
cannot be measured before the thing it describes exists.
