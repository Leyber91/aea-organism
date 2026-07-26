# E10 — WORLD 1 ART DIRECTION. LOCKED.

*THE CORE, the first region. Locked 2026-07-26 after three generation rounds and one evidence audit.*
*Supersedes nothing. Sits under `E2_VISUAL_DIRECTION.md` and `E8_FIDELITY_LAW.md`, which still govern.*

---

## THE LOCK

**BLACK GLASS.** Bodies of polished dark obsidian and smoked glass, fluid and heavy, on a plain of
marbled black and white stone. Cold light, high mist. Amber filament under the surface of the OPEN
creatures only. Cold blue-white, running inward, on the ADVERSE ones. Nothing at all on the SEALED
ones.

Two candidates were beaten and the reasons are recorded so this is not re-litigated:

| | why it lost |
|---|---|
| SOOT AND SPARK | spends amber everywhere as ambient sparkle, so the fired state stops being a signal. Eight volumetric particle bodies is also the most expensive of the three to run at 60fps |
| FOLDED RECORD | warm cream and gold leaf across every surface. The gold is decoration, not an earned state, which breaks the two-ink law directly. Per-facet printed text also dissolves at any real draw distance |

**BLACK GLASS wins on the project's own law.** Void field, structure grey, amber as the fired state
only. It is the one candidate where a player reads a creature's diagnosis from colour before shape,
because it is the one candidate where most of the frame is dark.

**Named trade-off, and it is real.** FOLDED RECORD produced the better *level*: stacked platforms,
staircases, verticality, places to fly a probe. BLACK GLASS produced a plain, and a plain is not a
level. **The architecture is owed separately**: black-glass material, folded-record verticality.
That is a build task, not another generation round.

---

## THE EIGHT, AS DRAWN AND AS CORRECTED

Sizes are **design constants chosen for silhouette legibility**, never described as measured. No
experiment in this project produces metres.

| # | creature | m | state | receipt |
|---|---|---|---|---|
| 1 | `Effusus responsi` | 4.0 / 12 across | OPEN (THE GOAL) | most-flagged behaviour, on a flag that conflates four and has never been split |
| 2 | `Clausus operis` | 0.4 | OPEN (THE METHOD FRAME) | 29 of 153 replies contained any working; one rod 0 of 48 |
| 3 | `Tacitus operis` | 1.8 + 6 cascade | OPEN (THE READOUT) | **3 of 153.** See the correction below |
| 4 | `Obtemperans habitui` | 0.9 | ADVERSE (THE MANNER FRAME) | 8/12 to 0/6 on one rod, 69% to 9% on another. Best-measured effect in the set |
| 5 | `Iterans sui` | 1.6 across | **UNMEASURED** | three verbatim loops in the project, and **0 in 1,280 attempts** across two x19 runs. Does not reproduce |
| 6 | `Integer sufficiens` | 1.2 | **ADVERSE (THE VALIDATION GUARD)** | see the correction below |
| 7 | `Rogans vacui` | 0.5 | **ADVERSE (THE GOAL, THE FRAME)** | reproduces at 9 of 127 bare, 7.1%. **Both World 1 parts take asking to 0%** — they erase the behaviour rather than improve the creature. Fuel-split: 20% and 15% on two plants, 0% on two others in 76 calls |
| 8 | `Obsignatus unius` | 1.4 | SEALED (THE COUNCIL) | 8 calls, 1 distinct reply. Only the council was tried |

**Three colour states became four.** `UNMEASURED` renders dark like SEALED but with its seating
points visibly present and visibly **empty**: open sockets catching no light. A creature we have not
tested may not be painted as a creature we have.

---

## THREE CORRECTIONS THAT LAND IN THE ART

### 1 · `Tacitus operis` is demoted, not retracted

The famous receipt is wrong, and wrong in the direction that inverts the creature.

```
'...They want only the plant name. The line includes "plant=cerebras".
 So answer: "cerebras". No extra text.cerebras'
```

**The stored reply is 256 characters and ends with the answer.** All clean `extract` trials for that
rod end in `cerebras`. It scored as a failure because of a length gate:

```python
"check": lambda t: "cerebras" in (t or "").lower() and len(t.strip()) < 60
                                                      ^^^^^^^^^^^^^^^^^^^^
aea/lab/x12_L0_goal_presence.py:66
```

The creature "reasons correctly and cannot say the answer" was sourced from a reply that says the
answer twice. **That is the third false finding produced by our own instrument**, after the 320-token
cap that created `Auratus gravis` and the prompt echo that created the 52% mute rate.

What survives is `x13`: `mute = 3` of 153 clean trials, work right and mouth wrong, recovered by the
readout at zero tokens. The behaviour is real. It is **2 percent, not 100**, and the art does not
change: a rare creature is still a creature. Its billing changes. It is not the striking one.

### 2 · `Integer sufficiens` is ADVERSE, not SEALED

SEALED means nothing reaches it. Something reaches it and takes it to zero. On `nemotron-550b`:

```
frame                     7/7  ->  frame|validation            0/7   all 7 declined
frame|readout             7/7  ->  frame|readout|validation    0/8   all 8 declined
frame|goal                4/4  ->  frame|goal|validation       0/4   all 4 declined
```

Every loss is a forced abstention. The guard that makes other creatures honest makes this one refuse
to answer at all. **It is the sharpest game mechanic in the set** and we had it labelled inert: a
player who seats their best part into the one creature that was already correct destroys it.

Drop the wings. A winged body was invented to encode "its difficulty lies elsewhere", and the
measurement says its difficulty is that **our tools point at it and break it**. Coiled, closed,
balanced on one point of contact, cold blue-white light running inward under the coil.

### 3 · `median reply length 3 to 320` never existed

Invented in the first image brief and carried through three of them. There is no such measurement.
The real medians over clean trials are 8 characters with a goal present, 1617 with it absent. The
`320` is the max-tokens cap that produced the retracted `Auratus gravis`; reusing it would make it
the source of a fourth false finding. **Never quote it again.**

Surviving figure for the same idea: replies showing working go from **41 percent to 100 percent**
under a frame that names a method, and the median reply goes from **71 output tokens to 167**. That
was measured on counting tasks and `x18` did not confirm it generalises, so anything resting on it
renders **provisional**: amber at the seams as unfilled outline rather than solid fill.

---

## WORLD 1 IS SHOT. THE REFERENCE MANIFEST, 2026-07-26

Nine creatures and four scenes, all in BLACK GLASS, all obeying the light law. Briefs at
`refs/bundle/W1_THE_ANSWERER/WORLD_1_THE_ANSWERER.txt`, `refs/bundle/W1_THE_ANSWERER/W1_EIGHT_SHOTS.txt` and `refs/bundle/W1_THE_ANSWERER/W1_THE_DOOR.txt`.

| # | creature | state | render |
|---|---|---|---|
| 1 | `Effusus responsi` | OPEN (GOAL, METHOD) | beached leviathan, amber apron running forward, human tiny at left |
| 2 | `Clausus operis` | OPEN (METHOD) | leaning egg-body, one aimed spur, amber only at the ground seam |
| 3 | `Tacitus operis` | OPEN (METHOD) | head hung low, sealed mouthless face, ribbon of ranked plates |
| 4 | `Egens unius` | OPEN (METHOD) | lean quadruped, topline channel milled open and lit, empty |
| 5 | `Incuriosus vacui` | OPEN (METHOD) | heavy grazing ox, open mouth at bare ground, **no eyes**, fully dark |
| 6 | `Obtemperans habitui` | ADVERSE (MANNER) | armless column, half the human's height, cold blue-white inward |
| 7 | `Rogans vacui` | ADVERSE (GOAL, METHOD) *provisional, 3.9%* | small seated animal, amber eyes, empty sockets on the flank |
| 8 | `Integer sufficiens` | **moved to World 2** | coiled animal on one point, cold blue-white under the curl |
| 9 | `Speciosus operis` | **SEALED. THE DOOR.** | head high, longest fullest ribbon, every seam lit, no socket left |

| scene | render |
|---|---|
| THE ARRIVAL | bare marbled plain, close fog wall, hanging filaments, `Effusus` glowing mid-left, `Incuriosus` grazing in the mist, `Rogans` watching, probe as one amber point with a ribbon |
| THE SEATING | `Egens`'s topline channel lit amber, a component descending into it, half seated |
| THE TERRAIN | `Tacitus` on concentric amber-seamed terraces, its ribbon merging into the steps |
| THE EDGE | built ground stopping at a clean curved line, bare plain beyond running into fog |

**The recognition pair is the world's last lesson.** `Tacitus` and `Speciosus` share a body and invert
a posture: bowed and mouthless against upright and complete. One is cured by the method. The other is
*made* by it.

## THE PRODUCTION ORDER

One image per turn. Six-in-one-turn is why the first three rounds drifted: six independent samplings
with no shared conditioning, and one wrong detail forces regenerating all six.

1. **Silhouette strip.** Eight solid black shapes plus a hairline grey human, plain white, one ground
   line, 4:1. No material, no light, no text. This is the test, not an illustration.
2. **Silhouette fix.** One change per turn until the ladder reads.
3. **`Tacitus` alone**, black glass, three-quarter, the sealed face turned to camera.
4. **`Obtemperans` alone.** It must not resolve as a small human.
5. **The plate**, attaching the approved strip: *reproduce these shapes and sizes exactly, change
   only the material*.
6. **The detail sheet**, the five creatures under 1.5 m.
7. **The world**, attaching the approved plate.

Plate and detail sheet are built **once, in black glass only**. The other two materials are dead.

---

## THE UPSTREAM PATCH, DONE 2026-07-26

The annex was the source of the bad numbers and it is now corrected in place, every edit signed and
dated, nothing deleted. Seven sites across four files:

| file | was | now |
|---|---|---|
| `ANNEX_G` `Tacitus` | 100% / 88% / 52%, quote truncated before the answer | the full 256-char reply, the `len < 60` gate named, `3 of 153` |
| `ANNEX_G` `Effusus` | *"Asked how many vowels are in `unconventionality`"* | no question was asked, `prompt_chars: 17` |
| `ANNEX_G` `Iterans` | *"28 instances, all on the trap battery under a fitted frame"* | 28 detector artifacts, **three real loops in the whole project** |
| `ANNEX_G` ladder | `Auratus gravis [REGRESSION]`, *"up to 57 points"* | the validation guard, 7/7 to 0/7, three times |
| `ANNEX_G` `Arbiter` | contrast case was a retracted creature | `Obtemperans habitui`, best-measured effect in the book |
| `00_INDEX` | the front page still asserted `Auratus gravis` and 57 points | `Integer sufficiens`, forced abstention |
| `03_CHAPTER_II` | *"Chapter I ended holding 52%"*, and `Auratus` as a live example | the retraction, and `3 of 153` |
| `DISCOVERIES` D-entry 2 | *"a fitted frame harms a rod that does not need it, up to 57 points"* | retracted, with what survives |

`04_CHAPTER_III_OPENING_LOCKED.md` is untouched **on purpose**. It is the sealed prediction document,
its predictions were wrong, and the losses are the point. Editing it would destroy the only mechanism in
this project that catches us.

## THE MEASUREMENTS NOW RUNNING

- **`x07b`** — 5 rods, chain lengths 10 and 50, n=12, three probes each. Settles whether *"0 of 12"* holds
  at power, and whether comparative self-knowledge exists where absolute self-knowledge does not.
- **`x19`** — the two unmeasured creatures. 4 shape conditions, 4 rods, 2 tasks, n=20, 640 calls. Read
  components are excluded by design: they act after the reply exists and cannot change a word of it.
  Baseline is clean: x12's asks are spread evenly across both tasks (10/157, 6/147), both conditions and
  both temperatures, so this is comparable rather than a new instrument.

**The prior x19 is testing is already visible in x12 and it would change the creature.** Asking is not
distributed: `cerebras/gpt-oss-120b` asks 12 of 44 times, every other rod 0 or 1. If that holds,
`Rogans vacui` is not the region's rare conscience but **one plant's**, which is Law IV again and a better
lesson than rarity: where you find it tells you what you are standing on.

`x19` also ships a replacement loop detector, verified before a call was spent: it catches all three real
loops, clears four structural texts, and clears **all 28 of the known false positives**.

## STILL OPEN, NAMED

- **The plate teaches diagnosis, not conversion, until x19 lands.** Distribution after correction is
  3 OPEN, 2 ADVERSE, 1 SEALED, 2 UNMEASURED, and all three OPEN states are provisional after `x18` moved
  goal and frame outside the noise band. One solid conversion survives: `Clausus` by the method frame,
  0.00 to 1.00.
- The name collision: `Clausus operis`, "the closed one", is labelled OPEN. Gloss it "the shut one" or
  drop the English glosses from the plate labels.
