# E8_FIDELITY_LAW — THE ESSENCE, THE GATES, AND THE LOOP

```
doc:           E8_FIDELITY_LAW.md (THE PROBE design book — evidence chapter E8, FIDELITY)
owner:         the game team (fidelity-director hat)
status:        BINDING for every built object from 2026-07-21 forward
last-updated:  2026-07-21
origin:        Luis, 2026-07-21 — "define the essence of the quality it must follow,
               referencing the images... we do not stop on an object until it is a replica
               as the image generated in the concepts folder."
answers:       what "replica" means operationally, and how an object earns the word DONE
inherits:      A11_SIGNATURE.md (the one-second test, the amber-is-a-variable thesis,
               §4 scarcity budget) · 04_UI_BIBLE.md (pixel law) · bundle_20/02_VISUAL_LAW.md
               (two inks, six glyphs, the tells) · E2_VISUAL_DIRECTION.md (silhouette +
               palette discipline as the pillars that survive a tech jump) ·
               E5_3D_TRANSLATION.md (which sheets become geometry, which become code)
governs:       every mesh, panel, seal, glyph and scene in game/. Nothing ships on opinion.
               Where this chapter and a taste argument disagree, this chapter wins, because
               this chapter carries measurements and the taste argument does not.
evidence:      §2's baseline table was MEASURED off the nine sheets on disk 2026-07-21 with
               PIL + numpy (method in §2.1). Every threshold in §3 is derived from that
               table. No number in this document was invented.
laws:          two-ink absolute · honesty law absolute (no faked data, no invented numbers)
               · render doctrine three classes (SOLID / HOLOGRAM / FLAT UI) · NO emoji
```

Tag legend: `[BUILT]` verified on disk 2026-07-21 · `[PLANNED]` specified, binding, not yet
in code · `[DECISION-LUIS]` awaiting his verdict.

---

## 0. The law in one line

**An object is a replica when a stranger shown the sheet and the render calls them the same
object, and the seven measurements in §3 agree with the stranger.** Neither half alone is
sufficient: the measurements without the stranger produce a compliant object nobody
recognises; the stranger without the measurements produces drift that nobody can name.

---

## 1. THE ESSENCE — eight qualities the sheets share

These are stated as rules a builder obeys, not as adjectives. Each one names the sheets it
was read from.

### E-1. The void is the subject, not the background
*Read from: S1, S3, S7, S9.*

Measured: **72% to 98% of every sheet sits below value 0.10.** S3 (the probe) is 97.6% void
holding a single 0.4%-of-frame object. The darkness is composed — it has edges, weight, and a
job (it is the not-yet-understood, rendered as area).

**Rule:** the frame budget starts at void and spends outward. Before adding anything, name
what area of void it consumes and what it buys. A scene render whose void share falls below
70%, or a plate whose void share falls below 80%, has been filled rather than composed —
delete the newest thing, not the oldest.

### E-2. Two inks, and amber is rationed to near-nothing
*Read from: all nine.*

Measured: amber is **0.33% to 1.61% of frame pixels** and **3.2% to 22.0% of the lit marks**.
The highest-amber sheet in the set (S1, 22% of ink) is a sheet whose entire subject is one
beacon. Third-hue leakage across all nine sheets is **0.0017% to 0.0801% of frame** — a rounding
error, never a decision. Cool ink sits at hue 202–216 (the sanctioned `rgba(120,155,175)` is
hue 202). Amber sits at hue 28–37 (`#ffb000` is 41, `#d4a24c` is 38); scene sheets skew
*orange-ward* because amber sits on dark, never yellow-ward.

**Rule:** amber marks a thing that is alive, running, understood or earned — and it lands on
the concentric motif (the gimbal ring on PH-01, the index mark on the zone dial, the ground
rings under the probe), not scattered as highlight. If amber drifts above hue 41 it has gone
yellow and is wrong. A cold render is a correct render.

### E-3. Every object carries its own designation and measured facts
*Read from: B7, A2, C3, C4, B1.*

Nothing in these sheets is anonymous. The pattern is fixed and repeats without exception:
**index number · code · name · one-or-two-line function · class glyph · measured facts with
units · provenance or diagram ID.** `1. PH-01 / A11-CORE PROBE — Octahedral core with
stabilization ring`. `7. SR-41 / ACTIVE RELIC — SPEED 0.61 m/s · RELIABILITY 0.99 · DECAY
STATE STABLE`. `4. WA-12 / TRACE RIBBON — PROVENANCE: TRACE LABORATORY`. Every callout points
at a *named part*: AXIAL FIN (x4), RING DRIVE GIMBAL, ISOLATION COLLAR, ROT VECTOR SCAR.

**Rule:** an object without a designation, a class glyph and at least three measured facts is
not finished — it is a shape. The parts are named before the mesh is built, because the names
are what the player scans, logs and remembers. Under the honesty law the *values* come from
live data; the *fields* come from the sheet.

### E-4. Hairline-dominant line economy — weight carries hierarchy, colour never does
*Read from: B7, A2, C4, B1, S7.*

Measured stroke-width distribution on the plates (native 1024–1536px): **38–51% of strokes are
1px, 76–87% are ≤2px, and only 8–15% are ≥4px.** Hierarchy is produced by the *ratio* of
hairline to structure line and by value, never by introducing a colour. B1's own title block
states the intent in the fiction: `LINE WEIGHT: 0.18mm`.

**Rule, resolution-independent:** detail stroke = 1/1024 of the frame's short side, structure
stroke = 2/1024, heavy accent = 4/1024 and capped at 15% of all strokes. At a 1440px-tall
viewport that is 1.4px / 2.8px / 5.6px. Scale the ratio, never the pixel count.

### E-5. Density is evidence, never ornament
*Read from: B7, A2, C3, C4, S7.*

The plates are dense — 8–15% ink — and every single mark is doing work: a dimension, a
tolerance, a leader line to a named part, a run ID, a checksum, a log extract with timestamps
(`> SCAN 00:00:07 / > VERIFY 00:00:07 / > ISOLATE 00:00:08`). S7 spends half its frame on a
severed chain link and spends the other half explaining what the severance *means*
(`CONDUCTIVITY: OPEN · INTEGRITY: 0% · IMPACT: CONTAINED · STATUS: ACKNOWLEDGED`). There is no
greeble anywhere in the set. Terminal text is used as a surface material, and the surface it
makes is *evidence*.

**Rule:** every mark must be able to answer "what fact are you?" A mark that answers "I make it
look technical" is cut. Denser therefore means better-instrumented, never busier. This is the
same rule as the honesty law wearing a visual hat.

### E-6. Depth separates into three bands, and fog is the sky
*Read from: S1, S9, S3.*

S1: near towers at full contrast, mid towers at roughly 40%, far towers as pure silhouette
dissolving into a horizon of the same colour as the fog. Measured, the scene sheets are
tonally *compressed* — cool-ink p99 lands at 0.29–0.50 versus 0.42–0.64 on the plates —
meaning the scenes buy their depth from separation, not from range.

**Rule:** a greyscale copy of any scene render must still show three distinct depths. If it
does not, the fix is fog and silhouette variety, never more geometry (E5 §2).

### E-7. Solid reads solid — material, facets, and cut lines
*Read from: B7 crop, A2, C3, S9.*

At crop level PH-01 is unambiguously a **manufactured object**: faceted hull with a value
hierarchy across facets, panel lines *cut into* the surface rather than drawn on it, an edge
that catches light, two engraved glyph plates, and a segmented amber gimbal ring whose
segments have their own darker divisions. It is never a wireframe and never a glow. Even the
zone dial in C4 — flat UI — draws each ring as **two hairlines with a gap**, so the ring reads
as a rim with thickness rather than a stroke.

**Rule (binds to the render doctrine):** anything in the SOLID class must show facet value
separation, cut lines and an edge response before it is called done. A solid rendered as
additive lines is a doctrine violation, not a style choice. Double-line rims are the cheapest
single move that separates our work from default 3D.

### E-8. The concentric field is present, and it is where the light lands
*Read from: all nine.*

Rings appear in every sheet in the set: etched into the ground under the probe, radiating
under the genesis beacon, as the district plates in S9, as the integrity map in S7, as the
title-block reticle on every plate, as the zone dial itself. And the amber almost always sits
*on* a concentric element.

**Rule:** every object and every scene carries the concentric motif somewhere, and the hot mark
is placed on it. An object with no ring, no reticle and no radial index is off-canon even if
every other gate passes.

---

## 2. THE MEASURED BASELINE — what the sheets actually are

`[BUILT]` — measured 2026-07-21 off the nine sheets in `design/concepts/`.

| sheet | class | dims | void % | ink % | amber %frame | amber %ink | hot/amber % | leak %frame |
|---|---|---|---|---|---|---|---|---|
| S9_the_city_revealed | scene | 1672×941 | 71.6 | 28.4 | 1.614 | 5.68 | 14.1 | 0.0801 |
| S1_field_genesis | scene | 1672×941 | 93.5 | 6.5 | 1.419 | 21.98 | 8.0 | 0.0043 |
| S3_the_probe | scene | 1122×1402 | 97.6 | 2.4 | 0.376 | 15.87 | 7.8 | 0.0317 |
| S7_honest_failure | scene | 1448×1086 | 94.8 | 5.2 | 0.349 | 6.68 | 23.0 | 0.0017 |
| B7_probe_hardware | plate | 1024×1536 | 87.1 | 12.9 | 0.536 | 4.16 | 54.1 | 0.0089 |
| A2_specimen_rods | plate | 1024×1536 | 85.3 | 14.7 | 0.477 | 3.25 | 41.3 | 0.0049 |
| C3_world_artifacts_v3 | plate | 1536×1024 | 86.5 | 13.5 | 0.726 | 5.36 | 30.9 | 0.0512 |
| C4_instrument_panels_v2 | plate | 1536×1024 | 86.0 | 14.0 | 0.467 | 3.33 | 40.9 | 0.0031 |
| B1_axis_principle_seals | plate | 1024×1536 | 92.0 | 8.0 | 0.331 | 4.12 | 56.1 | 0.0029 |

Three findings that change how we build, beyond the obvious:

1. **The void is darker than the sanctioned band's top.** Mean void RGB across the nine sheets
   is `(0.6–3.4, 5.8–10.0, 13.2–19.0)` — roughly `#010812`. The sanctioned void range tops out
   at `#0a1420` = `rgb(10,20,32)`, which is **brighter than any sheet's void mean**. The bright
   end of the band is for local gradient only; a render whose frame-wide void mean sits near
   `#0a1420` is washed out even though every pixel is technically legal.
2. **Scenes and plates are two different budgets.** Plates run 3–5% amber-of-ink with 31–56% of
   that amber HOT; scenes run 6–22% amber-of-ink with only 8–23% HOT. A plate is a lit catalogue
   entry; a scene is a dark world with one or two live things in it. Using one budget for both
   produces either dead plates or over-lit scenes. `[DECISION-LUIS]` confirm the two-class split
   before §3 is enforced.
3. **Every sheet clips.** Max value is 1.000 on all nine, while the 99.9th percentile is only
   0.44–0.76 (scenes) and 0.81–0.93 (plates). There is always a tiny pure-hot core. A render
   with no pixel above 0.95 is under-lit *at the core* even if its census passes.

### 2.1 Method (so any number here is reproducible)

RGB → HSV per pixel. **void** = V ≤ 0.10 · **ink** = V > 0.10 · **amber** = S > 0.25 ∧ hue ∈
[20°,60°] ∧ V > 0.18 · **hot** = amber ∧ V > 0.62 · **cool ink** = ink ∧ ¬amber · **third-hue
leak** = S > 0.30 ∧ V > 0.15 ∧ hue ∉ [20°,60°] ∧ hue ∉ [170°,260°]. Stroke width = run-lengths
of the mask `L > 0.16` along every third scanline, runs ≥40px discarded as fills.

`tools/fidelity.py` `[PLANNED]` — ~60 lines wrapping exactly the above, taking a PNG and a
class (`scene` | `plate` | `object`) and emitting one JSON record. It is a re-implementation of
a run that already happened, not a promise of new science.

---

## 3. THE FIDELITY GATES — the checklist that replaces opinion

A built object is measured against **its own sheet**, not against the set. All seven gates must
pass. A failing gate names the fix; it does not open a debate.

### G-1 · SILHOUETTE MATCH
**How:** render the object with all materials replaced by flat black on a white field, from the
sheet's camera *and* from the play camera. Do the same to the sheet by thresholding.
**Passes when:** (a) the black-only render is recognisable as the same object without labels;
(b) the part count in the outline matches the sheet's — four axial fins are four fins, the
gimbal ring is present, the base lock ring is present; (c) it still reads at the play camera
angle, which is the binding one.
**Fails to:** proportion and part-count work. Never to texture work.

### G-2 · PALETTE CONFORMANCE
**How:** sample every pixel of the still (§2.1 classifier).
**Passes when:** cool ink hue median ∈ [200°, 218°] · amber hue median ∈ [26°, 41°] · **third-hue
leak < 0.10% of frame** (sheet max measured: 0.0801%) · frame-wide void mean within
`#010812`–`#050a10`, never at `#0a1420` · at least one pixel > 0.95 (the hot core).
**Fails to:** material and tone-mapping work. A single stray hue invalidates the render, exactly
as it invalidates a sheet.

### G-3 · AMBER CENSUS
**How:** count amber pixels on the standard `?still` boot frame, plus one late-save frame.
**Passes when:**
- *plate / flat-UI class:* amber 0.30–0.75% of frame · 3–6% of ink · hot 30–60% of amber.
- *scene class:* amber ≤ 1.7% of frame · 5–22% of ink · hot ≤ 25% of amber.
- *object in-world:* treated as scene.
**Two-sided, and this is the point:** too much amber early is over-lighting; too little amber on
a late save means earned understanding is not being rendered. The census is the plot
(A11 §1) — record both frames or the gate has not been run.

### G-4 · LINE-WEIGHT RATIO
**How:** run-length histogram (§2.1) on the still, normalised to a 1024px short side.
**Passes when:** ≥ 76% of strokes ≤ 2px · ≥ 35% of strokes ≤ 1px · ≤ 15% of strokes ≥ 4px.
**Fails to:** stroke-width and outline-shader work. Symptom of failure: the render looks
"chunky" or "like a 2003 menu" — that is this gate, quantified.

### G-5 · DENSITY BUDGET
**How:** void share from the classifier, plus a hand count of text marks against the data
source.
**Passes when:** void ≥ 80% (plate) or ≥ 70% (scene) · **every text mark traces to a real
datum** · the object carries designation + class glyph + ≥3 measured facts (E-3) · no mark
exists whose only justification is that it looks technical.
**Fails to:** deletion. This gate is never passed by adding.

### G-6 · LEGIBILITY AT DELIVERED SIZE
**How:** screenshot at the size the object will actually appear — the HUD panel at its real
CSS box, the artifact at its real on-screen diameter, the landmark at real traversal distance.
No zooming to judge.
**Passes when:** the smallest label is still readable, and the designation is still readable, at
that size. Measured on B7 (1024px wide): the smallest type in the sheet — callouts, footer notes
and title-block rows — runs **9–11px cap height, i.e. 0.88–1.07% of frame width**, and the item
caption runs 17px, **1.66%**. So the type scale is two sizes plus a designation size, at roughly
1.0% / 1.2% / 1.7% of frame width. Below ~0.85% of frame width, type on
these sheets stops being type and becomes texture, which is legal only when it is *meant* as
texture (E-5) and never for a designation.
**Fails to:** scale and hierarchy work, not to "add a tooltip."

### G-7 · THE STRANGER TEST
**How:** show one person who has seen neither, the sheet and the render, side by side. Ask two
questions and nothing else: *"Are these the same object?"* and *"Point to the ring drive
gimbal."* (Substitute any named part.)
**Passes when:** yes, unprompted, and the finger lands on the right part.
**This gate outranks the other six.** A render that passes G-1..G-6 and fails G-7 is a
compliant object nobody recognises, and the correct response is to find what the stranger
looked for and did not find — that is the next single gap (§4).
`[DECISION-LUIS]` who the strangers are and how often we can spend them. Until answered, Luis
is the stranger of record, judged at first glance before any explanation is offered.

### 3.1 The gate record
`[PLANNED]` One JSONL line appended to `design/fidelity_ledger.jsonl` per pass:

```
{"ts":"...","object":"PH-01","sheet":"B7_probe_hardware.png","class":"object",
 "still":"shots/ph01_still.png","g1":"pass","g2":{"leak":0.004,"hue_cool":209,"hue_amber":33},
 "g3":{"amber_frame":0.61,"amber_ink":4.4,"hot":38},"g4":{"le2":0.81,"ge4":0.11},
 "g5":{"void":0.86,"facts":5},"g6":"pass @ 220px","g7":"pass — Luis, first glance",
 "verdict":"DONE"}
```

**An object is DONE when a record with `verdict:"DONE"` exists. Not before. Not by opinion, not
by "looks right to me," not by the builder's own satisfaction.** No record, no done — and the
ticket does not move in `tickets.json` (E3 §2).

---

## 4. THE ITERATION LAW

The loop, and there is no other loop:

> **build → screenshot → hold the screenshot against the sheet → name the single biggest gap →
> fix only that gap → screenshot again.**

Five clauses that make it work:

1. **Screenshot or it did not happen.** Judgement is made on a still, at delivered size, next to
   the sheet. Never on the running canvas, never from memory of the sheet. (Verify-don't-claim.)
2. **One gap per pass, named out loud before the edit.** Fixing two things costs the attribution:
   when the render improves you no longer know which change bought it, and when it regresses you
   no longer know which change cost it. Write the gap down first, then edit.
3. **Biggest first, and "biggest" has an order.** Silhouette outranks palette; palette outranks
   density; density outranks line weight; line weight outranks polish. Working on a lower rung
   while a higher one fails is procrastination with a tool open.
4. **Six passes is the escalation bell.** If six recorded passes have not closed one gap, the gap
   is not a tuning problem — it is a form decision (E2's structural-first rule). Stop tuning,
   re-read the sheet at crop level, and change the form.
5. **Nothing else is touched.** No drive-by improvements to neighbouring objects mid-loop. They
   have their own sheets and their own records.

**The stopping rule, stated the way Luis stated it:** we do not stop on an object until the
gate record says DONE. "Good enough for now" is not a state this ledger can represent. An object
that must ship unfinished ships as `verdict:"HELD"` with the open gap written in the record, so
that the debt is visible instead of forgotten.

---

## 5. WHAT FIDELITY DOES NOT MEAN

Replica is a claim about **form, proportion, designation, ink discipline and where the light
lands**. It is not a claim about the following, and a render is *required* to differ here:

1. **Numbers.** `SPEED 0.61 m/s`, `RELIABILITY 0.99`, `CYCLES 001247`, `HASH 0D1E-3C7A` are
   plausible fillers drawn to show the *layout of a fact*. Copying a sheet's number into the
   game would be a fabricated reading and a direct honesty-law violation. **The sheet specifies
   the field; live data supplies the value.** A render whose numbers match the sheet exactly has
   failed, not passed.
2. **Amber quantity, early.** The sheets are frozen at an authored moment. In the game the
   census is a save file (A11 §1): a first-hour render legitimately carries *less* amber than its
   sheet, and a late-game render legitimately carries more. G-3 is checked against the class
   budget and the save state — never against the sheet's exact percentage.
3. **What only motion can carry.** The sheets are stills; a still cannot show the trace crossing
   the void, the gimbal ring's drift, the horizon band breathing, or latency rendered as travel
   time. Motion is allowed to add what the sheet could not hold — under the juice budget, and
   never by adding a second attention magnet at idle.
4. **Plate conventions are not world geometry.** Leader lines, ruler edges, corner brackets,
   title blocks and dimension arrows are the *language of the plate*. They belong to FLAT UI —
   scan mode, the codex, the panel. Floating them in 3D space beside a mesh is a category error,
   not fidelity.
5. **Render class is decided by doctrine, not by the sheet's drawing style.** A sheet drawn as a
   line diagram does not license a hologram. The probe, towers, landmarks, artifacts, bench parts
   and organ buildings are SOLID and may never be holograms, however wireframe the plate looks.
   Conversely, the map and the city-as-diagram stay HOLOGRAM even where S9 shows them with
   material, because a projection is honestly a representation.
6. **Camera, aspect and resolution.** Sheets are 1024–1672px orthographic-ish plates; the game is
   a moving perspective viewport. Every threshold here is a *ratio*, deliberately. The sheet's
   camera is a suggestion; the play camera is the one G-1 binds.
7. **Sheet artefacts are not canon.** Generation noise, soft glow bloom around amber, and any
   value drift in the sheets' dark fields are properties of how the sheets were made. Where a
   sheet artefact contradicts the two-ink law or the banned-tells list, the law wins and the
   artefact is not reproduced.
8. **A sheet may show a FIELD. It may never show a VERDICT.** This is the distinction clause 1
   was missing, and B12 is what taught it. `SPEED 0.61 m/s` is a **field**: a plausible filler
   showing the layout of a fact, harmlessly overwritten the moment live data arrives. `PASS`,
   `DIVERGENCE GROWING`, and an amber cell meaning *best in column* are **verdicts**: conclusions
   drawn from evidence. A verdict cannot be overwritten by live data without changing what the
   drawing means, so a fabricated verdict is not a placeholder — it is a false claim that survives
   into the build as composition. On a sheet, every verdict slot renders `unmeasured` or a dash.
9. **The sheets are not the colour authority.** Measured across the library 2026-07-21, only C3 is
   actually inked to the cool structure law (mean RGB 123,124,129; 7% of marks warm). B10_V2 is 62%
   warm, B12 is 88% warm at mean (135,128,127). The law has been asserted in the docs and never
   enforced on a plate. Engine palette tokens come from 02_VISUAL_LAW, never from sampling a sheet,
   and G-2 is checked against the token values rather than against a plate's pixels.

---

## 5.5 THE COMMISSIONING LAW — commission the instrument, never the reading

Earned from B12_gauge_pack, rejected 2026-07-21. Binding on every future sheet brief.

A generator has no access to the record. When a brief asks it for a reading, it renders the *shape*
of a good reading — and the shape of a good reading is always the flattering one. B12 proved this
cleanly: the three panels told to stay blank came back near-perfect, and **every fatal defect landed
in a panel told to show a measurement.** Asked for pass bars it printed twelve PASS. Asked for a
trend it drew a confident rising curve and captioned the divergence GROWING, beside its own ratio
box reading UNMEASURED.

So the brief carries the fault, not only the generator. Three rules follow:

1. **Never commission a value, a verdict, a fill level, a plotted series, or a ranking.** Commission
   the frame, the field, the label, the unit, the axis, the layout, and the *reason a field is
   empty*. The engine supplies everything else at runtime from a real source.
2. **When a panel must show a shape that only real data can produce** — a trend, a distribution, a
   sparkline — commission the empty plot area with its axes and its inscription, and print
   `TRACE RENDERED FROM LIVE SAMPLES` inside it. Never a drawn curve. A drawn curve is evidence
   the sheet does not have.
3. **Ask for the honest state, then forbid improving it.** State the register split explicitly
   ("three built, one demo, three unearned") and inscribe *the sheet must not improve this ratio*.
   B12's blank panels came back correct precisely because that instruction was present for them.

The check before any block is sent: **read every panel in the brief and ask what a generator with
no access to the record would have to invent to satisfy it.** Whatever the answer is, delete that
request and replace it with the field plus the reason it is empty.

### 5.5.1 A RELATION IS A READING TOO — amended 2026-07-21, after B14

The law above was written about *values* and it has a blind spot. B14's brief asked for "a small
matrix of port types against mount types; legal joins drawn solid, illegal joins drawn as a refused
seating" and never supplied which joins are legal. The generator invented **thirty-six legality
verdicts** and a four-symbol vocabulary to express them, on a panel about a composition system that
`06_MEASURED_EVIDENCE` §9 puts at **0 of 29 elements composable**. That is the same failure as
twelve fabricated `PASS` verdicts, wearing a different shape.

So the forbidden list is wider than numbers:

- a **value** (`0.61 m/s`, a fill level, a score)
- a **verdict** (`PASS`, `DIVERGENCE GROWING`, best-in-column)
- a **relation** (this joins to that; this triggers those; A is legal with B)
- a **legality or a taxonomy** (a rule table, a compatibility matrix, a state machine's transitions)
- an **identifier set** (field names, keys, enum members)

If the brief does not supply it, the sheet may not print it. Commission the empty matrix — the axes,
the headers, the legend, the cell frames — and inscribe `CELLS FILL FROM THE SPEC` inside it.
An empty table with correct axes is a design. A filled table with invented cells is a fabricated
ruleset that a later build session will read as canon.

### 5.5.2 SOME PANELS CANNOT BE COMMISSIONED AT ALL — amended after B14 V2

B14's region 4 was briefed twice and invented a different ruleset each time. V1 fabricated a 36-cell
join table. V2 drew that table correctly empty — and fabricated a strictness ordering over the six
glyph categories and six doctrine-to-construct bindings instead. **The fabrication did not die; it
relocated.**

The reason is structural. Region 4's subject is the composition system, which `06_MEASURED_EVIDENCE`
§9 records at **0 of 29 elements composable**. There is no ruleset to draw. A panel about rules with
no rules is an empty panel, and a generator fills empty panels — that is what generators are for.
No amount of stricter wording changes it, because the instruction "draw the rules, but do not invent
the rules" is unsatisfiable when no rules exist.

**The rule: if a panel's entire content would be a relation set that does not exist yet, do not
commission the panel. Cut it and register the missing spec as an owed input.** One empty instrument
is legitimate and teaches something (B14's empty join table with `CELLS FILL FROM THE SPEC` is the
model). A whole region of empty instruments is not a design, it is an admission better made in the
census than on a plate.

Test before commissioning any panel: *if the author cannot state its content in one sentence of
supplied fact, the panel is not ready to be drawn.*

**The corollary, also from B14:** if the brief *does* supply a fact, it must say where the fact
goes. BLOCK 6 listed every join by both names (`mech.ceiling → seed.7`) and then described the card
as "two elements joined by one drawn connector" without saying which of the two gets labelled. Ten
cards were drawn to that ambiguity and only the right-hand element was named, so not one of the ten
taught links is legible. Supplying a name is not the same as placing it.

---

## 6. First application `[PLANNED]`

Run the gates in this order, because each one teaches the next:

1. **PH-01 / the probe** against `B7_probe_hardware.png` — the object the player looks at for
   the whole game, and the cleanest SOLID-class test of E-7.
2. **The instrument panels** against `C4_instrument_panels_v2.png` — FLAT UI, already ~final art
   (E5 §1), so any failure is ours and cheap to fix.
3. **The /probe scene still** against `S1_field_genesis.png` — the scene-class budget, and the
   test of E-6's three bands.
4. **The axis and principle seals** against `B1_axis_principle_seals.png` — FLAT UI at small
   delivered size, the hardest G-6.

Each produces one ledger line. Four lines, and the loop has a spine.

---

## 7. The one-paragraph version, for the top of any build session

Void is the subject and holds 70–98% of the frame. Two inks only, amber under ~1.6% of frame and
landing on the concentric motif, third hues under 0.1%. Every object has a designation, a class
glyph and at least three measured facts, and every mark answers "what fact are you?". Lines are
hairlines at a 1/2/4-per-1024 ratio with heavy strokes under 15%. Solids show facets, cut lines
and an edge — never wireframe, never glow. Scenes separate into three depth bands in greyscale.
Build, screenshot, hold it against the sheet, name the single biggest gap, fix only that, repeat
— and the object is not done until the ledger says so.
