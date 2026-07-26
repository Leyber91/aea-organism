# E11 — HOW TO BRIEF A GENERATIVE MODEL FOR THIS GAME

*The craft, earned across three failed rounds and one that worked. Companion to `aea/lab/METHOD.md`,*
*which does the same job for experiments. Read this before writing any image brief; the World 1 brief*
*at the bottom is the worked example.*

Style is locked in `E10_WORLD1_ART_DIRECTION.md`. This file is about **getting what you asked for.**

---

## 1 · THE NINE FAILURES, IN THE ORDER WE HIT THEM

### F1 · "Digital entity" resolves as anything except a creature

Round 1 asked for "living entities made of information" and got, three times out of three, an object:
a machine cutaway, a natural-history phenomenon, a specimen board. Not one had a body.

**Fix.** Say **ANIMAL**, and forbid the alternatives *by name*: not a machine, not a diagram, not a
specimen, not a mineral formation, not weather. Then add the falsifier: *if it could be mistaken for an
object, it is wrong.*

### F2 · Adjective sizes compress to a uniform mid-size

"Knee high" and "the size of a held object" both came back at human torso scale. Six of eight creatures
landed between 1 and 2 metres. A grid layout wants equal cells and the model will serve the layout.

**Fix.** Three redundant encodings of the same size, all binding at once: **metres**, **percentage of
frame height**, and **a body landmark on a human reference** ("level with the human's knee"). Then a
household object per creature ("a beach ball", "a golf bag standing up") — that one does more work than
the numbers, because it is what the model has actually seen.

### F3 · Unassigned body plans default to a dog

Four creatures with no stated body plan came back as sitting dogs and cats, indistinguishable in
silhouette. The eye then reads the size differences as errors rather than as information, which is what
"the proportions are off" actually means.

**Fix.** Assign all eight explicitly and **make the model count**: *four legs appears exactly once, two
legs exactly once, five of the eight have no walking legs. Count the legs before finishing.*

### F4 · Negations summon what they ban

"No robes, no crown, no staff, no mark of office" produced a robed hierarch with a crown, three times.
Four consecutive negations is a description of a wizard.

**Fix.** Write the positive that leaves no room: *one uninterrupted smooth surface from crown to feet, a
single material, proportioned like a turned wooden peg, nothing projecting from it at any point.*

### F5 · Absences are the hardest thing to generate

"It has no mouth" never once rendered. The model draws a face; a face has a mouth.

**Fix.** Describe the absence as a **positive surface**, with real-world referents: *the front of the
face is one continuous plate of the same material as the skull, like a fencing mask with no grille, like
the blunt seamless toe of a boot. Two eyes sit high on it. Below the eyes the surface runs unbroken to
the end of the muzzle.* Then force the camera to see it, or it will be hidden by the pose.

### F6 · Every hero subject gets rim light

Three creatures were specified as completely dark. All three came back with lit veins, because lighting
a subject is what rendering *is*.

**Fix.** State darkness as a **material property plus a placement**: *a flat, matte, light-absorbing
mass, the darkest value in the picture, no point on it brighter than the ground behind it. Its form is
read only from its outline against a pale background, and that is sufficient. No rim light, no edge
light, no separation glow, no specular. Place it against the palest part of the background.*

### F7 · Six images in one turn drift

Six images in one reply is six independent samplings with no shared conditioning. Body plans, sizes and
materials all move between frames, and one wrong detail forces regenerating all six.

**Fix.** One image per turn, and **attach the approved previous image** with *"reproduce the shapes,
order and relative sizes in the attached exactly; change only the material."*

### F8 · Spend the hard problems on cheap frames

True scale and eight distinct silhouettes are the two hardest asks. Solving them inside a fully rendered
plate means every retry is expensive.

**Fix.** **The silhouette strip is turn 1**: eight solid black shapes on white, one ground line, no
material, no light, no text. Retries are free and the test is unambiguous. Nothing renders until the
strip is approved.

### F9 · Text bakes into the frame

Asking for labels inside the image produces garbled pseudo-Latin on every surface. Asking for prose
commentary inside an image turn makes the model spend the turn on prose.

**Fix.** **No text of any kind in any image.** Mark state with a plain coloured dot on the ground beneath
each creature and leave a clean empty band across the bottom. Names are typeset afterwards, outside the
generator. Ask for all written commentary once, text-only, before turn 1.

---

## 2 · THE TWO RULES THAT ARE OURS, NOT THE MODEL'S

**Colour must carry a diagnosis, not a mood.** A player reads state before shape. If every creature is
lit, the plate is decoration. This is the two-ink law doing real work: amber is the fired state only, so
the frame has to stay dark enough for it to mean something.

**A state names a part.** `OPEN` alone is a claim about a creature. `OPEN (THE METHOD FRAME)` is a
measurement. Anything we have not tested renders `UNMEASURED`: dark, with its seating points visibly
present and visibly **empty**. Painting an untested creature as an open one is a honesty-law violation
that happens to look good, which is the most dangerous kind.

---

## 3 · THE NUMBERS THAT MAY BE QUOTED, AND THE ONES THAT MAY NOT

Verified against the run files 2026-07-26. **Never quote a figure that is not on this list.**

| claim | figure | source |
|---|---|---|
| no goal and no procedure | **0 of 158** clean, plus 0 of 146 vague | `x12` |
| of those 304 | 16 asked, 2 refused, 286 answered | `x12` |
| working, method frame | **41% to 100%**, on clean trials | `x15` `working_by_frame` |
| median reply | **71 to 167** output tokens | `x15`, all trials |
| any working at all | 29 of 153; one rod 0 of 48 | `x13` |
| mute, work right mouth wrong | **3 of 153** | `x13` |
| manner frame harm | 8 of 12 to 0 of 6; 69% to 9% | `x15` |
| validation on a rod that needs nothing | 7/7 to 0/7, 7/7 to 0/8, 4/4 to 0/4, all abstention | `x17` |
| council on a frozen rod | 8 calls, 1 distinct; 3 of them, 24 answers, truth 0 times | `x11` |
| asking, bare condition | **9 of 127, 7.1%** (x12: 11 of 158, 7.0%) | `x19` |
| asking, by plant | 20% and 15% on two plants; **0% on two others in 76 calls** | `x19`, bare only |
| both World 1 parts vs asking | goal 7% to 0%, frame 7% to 0%. Each erases it | `x19` |
| verbatim loops | three in the project, **0 in 1,280 attempts** | `x19` x2 |
| false confidence | **0 YES across 21 cells they went on to fail** | `x07b` |
| false doubt | 16 NO across 39 cells they would have passed | `x07b` |
| cannot host the meta-question | 2 of 5 rods; one did it 12 times of 12 | `x07b` |

**Banned outright:**

- `median 3 characters to 320` — never existed. Invented in the first brief, carried through three.
- `52%` / `100%` / `88%` mute — retracted; the population was 100% prompt-echo.
- `up to 57 points` and `Auratus gravis` — retracted; the harm was a 320-token cap.
- `28 loop instances` — detector artifacts on markdown tables.
- Any figure in **metres**. No experiment here produces metres. Sizes are design constants, and the brief
  must say so in its own opening paragraph.

---

## 4 · THE TURN STRUCTURE

Every turn opens and closes with the same hard-constraint block, verbatim. Repetition at both ends
survives the model skimming the middle.

| turn | deliverable |
|---|---|
| 0 | text only: three sentences on what the material says about information. No image. |
| 1 | **silhouette strip.** Eight black shapes plus a hairline grey human, plain white, one ground line, 4:1. |
| 2 | **silhouette fix.** Attach turn 1. One change per turn. Repeat until the ladder reads. |
| 3 | **`Tacitus` alone**, full frame, the sealed face turned to camera. The hardest single instruction. |
| 4 | **`Obtemperans` alone.** It must not resolve as a small human. |
| 5 | **the plate.** Attach the approved strip: *change only the material.* |
| 6 | **the detail sheet**, the five creatures under 1.5 m. |
| 7 | **the world.** Attach the approved plate. |

---

## 5 · THE WORLD 1 BRIEF, AS FIRED

The verbatim text is at `design/refs/W1_CORE_BRIEF.txt`. It is the worked example of everything above:
committed to one material, four states each naming a part, sizes triple-encoded, eight assigned body
plans with a leg count, absences written as positive surfaces, and a silhouette strip before anything is
rendered.

---

## F10 · A MECHANISM'S SHAPE OVERRULES ITS STATED FUNCTION — added 2026-07-26, World 2

World 2's first style candidate asked for an **external observer**: apertures hanging from above that
*read* a creature without warming it. It came back as **pendant lamps.** A showroom.

The brief was not ignored. It was obeyed, and the obedience is the problem: **a narrow cone of light
falling from a fixture overhead means ILLUMINATION.** That is what the shape says, and no amount of
"this light only reads, it does not warm" survives it. The image said *these creatures are being lit*
when the fiction needed *these creatures are being examined*.

**The rule.** When you specify a mechanism, you are specifying its **meaning**, not just its geometry.
Before writing one down, ask what that form already means to a viewer who has never read the brief.
If the existing meaning fights the intended one, the existing meaning wins every time.

**Two ways out, and prefer the first.**

1. **Specify the FUNCTION and its EFFECT, and let the model find the form.** "A second thing observes
   the first, and the information travels inward" produced a passenger riding a creature's back —
   better than anything I would have specified.
2. **Choose a form that already means the right thing.** A parasite on a host already means *this thing
   is being read by something that is not it*. A lamp does not.

**The tell.** If a mechanism needs a sentence explaining what it is *not* ("this is not lighting"),
the form is wrong. Redesign it rather than annotating it.
