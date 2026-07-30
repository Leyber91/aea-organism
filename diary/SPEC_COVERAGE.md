# THE SPECIFICATION, AND WHAT IS ACTUALLY LEFT

*2026-07-30. Luis: "we need to make a recap of all the specifications done and what is actually left
for the autonomous entity architecture." Counted from the tree, not remembered.*

---

## 1 - THE SPECIFICATION SURFACE

```
235 documents      677,800 words

  design/      198 docs   572,886 w      70 chapters + concept sheets
  diary/        22 docs    80,117 w      the handoff system
  docs/         11 docs    20,053 w      AEA research + specs (pre-game)
  root           3 docs     4,458 w      CLAUDE.md, README, GAME_PLAN
  references/    1 doc         286 w
```

Against **34,650 lines of code**. That is roughly **twenty words of specification for every line
that exists**. Discovery D7 named a 110:1 words-to-code ratio as this project's standing failure
mode; measured on documents rather than diary alone it is still the dominant fact about the repo.

**The laws are real and they are numerous:** 48 laws in `design/THE_LAWS.md` across seven families
(B, G, H, M, S, U, W), 18 discoveries in `diary/DISCOVERIES.md`, 19 voice crystals. They are quoted
constantly and they are enforced unevenly - which is itself one of the recurring findings.

---

## 2 - CAPABILITY COVERAGE: 32 OF 36 HAVE A BODY

| area | specified | body |
|---|---|---|
| **KERNEL** | metered grid, trust/zone gating, HANDS, tracelog | 4/4 |
| **ENERGY** | the draw, capability census, model fitness | 3/3 |
| **MIND** | orchestrator, swarm, pathfinder, tiers, council, persona | 6/6 |
| **MEMORY** | consolidation, codex index, **reflection** | 2/3 |
| **IO** | speak, listen, mixer, notify | 4/4 |
| **ORGANS** | autonomy, brief, converse, reflect, telegram | 5/5 |
| **LOOP** | heartbeat/tick, live wake | 2/2 |
| **RESEARCH** | **hypothesis**, **research loop**, **findings with sources** | **0/3** |
| **GAME** | the world, the bench, the sacred save | 3/3 |
| **SAFETY** | privacy guard, selfcheck invariants, honesty guards | 3/3 |

*(Two false negatives in my first probe, corrected: `web/world.html` exists at 77KB and was missed
because the probe only searched `aea/*.py`; `THE_LAWS.md` lives in `design/` and was looked for in
`diary/`. Recorded because the instrument being wrong is the most reliable pattern in this project.)*

---

## 3 - WHAT IS ACTUALLY LEFT

**Four capabilities, and they collapse into exactly two things.**

### A · RESEARCH (0 of 3) - the entity has never looked anything up

```
hypothesis stated before searching     NO BODY
a research loop with termination       NO BODY
findings stored with their sources     NO BODY
```

The tools exist - `web_search` and `web_fetch` are built and gated. The PROCESS does not. Two deep
research passes ran this session, 116 agents between them, and both were run from outside by an
assistant. The council argues from what four rods already believe, which is the exact failure it was
built to prevent.

Luis's own specification, which is now written down and not yet built:

> state a falsifiable hypothesis FIRST · research it keeping the sources · summarise AGAINST the
> hypothesis · exactly three outcomes - survives / dies / forks · stop when the purpose is met or
> the budget is spent or two rounds produce no new fork.

### B · REFLECTION (0 of 1) - nothing notices what memories mean together

Storage and retrieval both work: three registers, scored recall, measured reaching back 12 turns.
Nothing performs the operation of noticing that several memories mean something together that none
means alone. It must run over a scored SUBSET, store its answer as a retrievable memory, and keep
pointers to its sources.

### C · THE WIRING - and this is bigger than both

```
130 modules      17 reachable from something that runs      113 only if a person types it
```

`hands.invoke` is called by exactly two files. The entity, running on its own, can call nothing.

---

## 4 - THE HONEST SHAPE OF IT

**The AEA is not under-specified. It is over-specified and under-wired.**

Nearly everything named across 677,800 words has a body. What is missing is small, specific, and
clusters into two organs - research and reflection - both of which are about the entity LEARNING
rather than acting. And in front of both sits the wiring problem, which no amount of further
specification touches.

The order that follows from the numbers, not from preference:

1. **One loop that calls one tool and writes down what happened.** Moves 17 to 18. Everything
   already built is waiting behind this, and adding either organ below before it makes orphan 114.
2. **Research**, wired into that loop - because it is the organ that makes the council worth
   convening, and the council is currently four rods arguing from priors.
3. **Reflection**, which needs research to have produced something worth linking.

Nothing on that list requires a new document.
