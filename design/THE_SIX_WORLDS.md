# THE SIX WORLDS — the game's spine, by CLASS

*Written to disk 2026-07-26 because it was not. It existed only in conversation, and in one session*
*that cost two wrong answers: a bestiary plate built on the wrong grouping and a locked art direction*
*that had to be reopened.*

**WORLDS ARE NOT LEVELS.** `THE_LINEAR_HIERARCHY.md` files 86 census items into eight rungs L0..L7 by
NECESSITY: the lowest place each item becomes unavoidable. That is the architecture's spine and it is
the book's chapter structure, one chapter per rung.

**The game's spine is different.** Six worlds, one per CLASS of assembled entity, named by what the
entity can do. A world is a set of COMPONENTS the player can seat and the creatures those components
produce, repair, or ruin. A single world can draw components from several rungs, and a single rung can
feed several worlds.

Reaching for the hierarchy when the question is about worlds is the trap. It is written down and this
is not, which is why it keeps winning.

| world | class | layer | components |
|---|---|---|---|
| 1 | THE ANSWERER | SPECIFY | GOAL, FRAME |
| 2 | THE CORRECTOR | REPAIR | MEASURE, READOUT, VALIDATION, CLOCK, CRITIC, LADDER, COUNCIL |
| 3 | THE REMEMBERER | REMEMBER | CHECKPOINT, RECALL, CONVERSATION |
| 4 | THE KEEPER | PERSIST | — |
| 5 | THE HAND | ACT | — |
| 6 | THE APPRENTICE | CHANGE | — |

---

## WHAT EACH WORLD ACTUALLY HAS. Gaps counted, not described.

### WORLD 1 — THE ANSWERER · SPECIFY · **PLAYABLE**

> **REVISED 2026-07-26 after the World 1 brief audit. Four corrections, all verified against the runs.**
>
> **1 · THE WORLD HAS THREE PARTS, NOT TWO.** `GOAL`, `METHOD`, `MANNER`. Chapter III's own law already
> separates them — *"a frame that names a METHOD is free or better; a frame that names only a MANNER is
> actively harmful"* — and `Obtemperans habitui`'s entire receipt is a MANNER frame. Collapsing them
> into one "FRAME" left the world's only poison harmed by a part the player was not carrying.
>
> **2 · A METHOD FRAME CURES MUTENESS, so `Tacitus operis` is OPEN, not the door.** Mute trials (work
> right, mouth wrong) in `x15`: **28 of 288 bare, 24 of 288 posture, 0 of 360 fitted.** The annex's
> evolution line `Clausus —(FRAME)→ Tacitus` is backwards: the method does not create this creature, it
> eliminates it. `Tacitus` is one of World 1's cleanest conversions.
>
> **3 · THE DOOR IS `Speciosus operis`, AND IT WAS NEVER NAMED.** Sixteen creatures in the annex and the
> one that ends the first world is not among them. Replies that showed complete working where the
> working was wrong: **16 of 288 (5.6%) bare, 70 of 360 (19.4%) fitted.** The method more than triples
> it. Every reply now shows its reasoning, one in five reasonings is wrong, and checking an answer is a
> World 2 component. Brief at `refs/W1_THE_DOOR.txt`. Needs an annex entry.
>
> **4 · `Integer sufficiens` MOVES TO WORLD 2.** Its only measured state is against the VALIDATION
> GUARD (7/7 to 0/7, forced abstention). It has never been tested against GOAL, METHOD or MANNER, so it
> has no World 1 state at all.
>
> Also: `Incuriosus vacui` is **OPEN (THE METHOD)**, not sealed — `x19` on the goal-absent condition
> scores bare **0.000** and method-alone **0.648**. And `Rogans vacui` weakens to **5 of 127, 3.9%**:
> all nine of its asks sit on flagged replies, and while `echoes_prompt` is that behaviour's signature
> rather than its debris (asking what you wanted requires naming what you were given), the four
> carrying `reasoning_leak` are deliberation rather than a question and do not count.

Components: **GOAL, METHOD, MANNER**

| slot | creature |
|---|---|
| correct | `Egens unius` — one part converts it, 0.00 to 0.53 |
| correct | `Integer sufficiens` — needs nothing, 1.00 bare |
| toxic | `Obtemperans habitui` — a manner frame takes a 70b from 0.67 to 0.00 |
| non-functional | `Incuriosus vacui` — answers a task nobody set |
| non-functional | `Clausus operis` — answers, shows nothing |
| different attributes | **none** |
| evolution | `Clausus operis` —(FRAME)→ `Tacitus operis` |

Two correct, one toxic, two dead ends, one evolution. The only complete world.

### WORLD 2 — THE CORRECTOR · REPAIR · **HALF-BUILT**

Components: MEASURE, READOUT, VALIDATION, CLOCK · **CRITIC, LADDER, COUNCIL never assembled**

| slot | creature |
|---|---|
| correct | `Lectus operis` — 0/8 to 8/8 at zero tokens |
| toxic | the Cautious Answerer, −0.30 |
| toxic | `Arbiter vacui` — a clean verdict about nothing |
| non-functional | the READOUT itself: +0.02 and +0.05, inert on both batteries |
| different attributes | `Tardus erroris` — legible in latency, not in text. The only creature you cannot catch by reading |
| evolution | `Tacitus operis` —(READOUT)→ `Lectus operis` |

**Three of its seven components have never been assembled, and they are the three the whole
"prevention dominates repair" claim rests on.**

### WORLD 3 — THE REMEMBERER · REMEMBER · **THIN, AND IT HOLDS THE BEST MECHANIC**

Components: CHECKPOINT · RECALL (n=3, weak) · CONVERSATION (never measured)

| slot | creature |
|---|---|
| correct | `Labens longitudinis` + checkpoint: 9/16 to 11/11, p=0.0216 |
| corrupted | the free-form carrier: 4,801 characters of its own doubt, then it truncates |
| non-functional | **none** |
| different attributes | inheritance: upward costs nothing (5.12 to 5.25), downward loses a box (5.5 to 4.5) |
| evolution | `Labens longitudinis` —(CHECKPOINT, declared form)→ complete |

**Inheritance is the only creature-to-creature interaction in the whole project.**

### WORLDS 4, 5, 6 — KEEPER, HAND, APPRENTICE · **EMPTY**

All three. No components measured, no creatures, no evolutions, no stumbles. `agent_tools` exists
unwired; the tick loop exists unrun.

---

## THE EIGHT RENDERED CREATURES, MAPPED

Eight hero renders exist in black glass (`E10_WORLD1_ART_DIRECTION.md`, brief at
`refs/W1_EIGHT_SHOTS.txt`). They were commissioned as one world's plate. They are not.

| creature | world | note |
|---|---|---|
| `Effusus responsi` | **1** | converted by GOAL, more by FRAME |
| `Clausus operis` | **1** | non-functional, and the evolution's start |
| `Obtemperans habitui` | **1** | the toxic one |
| `Integer sufficiens` | **1** | needs nothing |
| `Tacitus operis` | **1 → 2** | **the bridge.** Made in World 1 by seating a FRAME, solved in World 2 by seating a READOUT |
| `Obsignatus unius` | **2** | the COUNCIL is a World 2 component |
| `Iterans sui` | **none** | 0 loops in 1,280 attempts across two runs. Does not reproduce |
| `Rogans vacui` | **1** | reproduces at 7.1%, and it belongs to SPECIFY because both SPECIFY parts erase it |

**Missing from World 1 and never drawn:** `Egens unius` and `Incuriosus vacui`.

### `Rogans vacui` earns a place, and a strange one — `x19`, 2026-07-26

Bare condition, 127 clean calls: **9 asks, 7.1%**, against x12's 11 of 158 at 7.0% on the identical
detector. It reproduces exactly.

**Both World 1 parts delete it.** THE GOAL takes asking 7% to 0%. THE FRAME takes asking 7% to 0%.
Neither improves the creature; each removes the hole it was noticing. So it is the one creature on the
plate that is **destroyed by the parts that help everything else**, and the only way to keep it is to
leave the hole open. It punishes the completionist, which makes it the sharpest teaching creature in
World 1 despite being the rarest.

**And it is a fuel phenotype, with a total split rather than a gradient:**

```
gpt-oss-120b            5/25    20.0%
nemotron-3-ultra-550b   4/26    15.4%
granite4.1:3b           0/40     0.0%
llama-3.1-8b-instant    0/36     0.0%
```

Two plants ask, two never ask in 76 calls. Spread 0.20, twice the noise band. Law IV: **where you find
it tells you what you are standing on.**

`Iterans sui` remains unplaced and unreproduced: zero verbatim loops in 640 calls, twice.

---

## THE TRANSITION, WORLD 1 TO WORLD 2

It needs no invented signal, because the bestiary already contains it.

Seat a FRAME on `Clausus operis`, the one that answers and shows nothing, and it becomes
`Tacitus operis`, the one that shows its whole working and states the wrong answer. **That is World 1
completed: every lever you have is spent and the creature is still wrong.**

You cannot fix it with GOAL or FRAME, because the fault is not in what you sent. It is in what came
back, and reading what came back is a World 2 component.

**You leave the first world at the moment you realise the reply contains more than the answer.**
