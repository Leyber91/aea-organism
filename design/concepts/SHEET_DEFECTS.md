# SHEET DEFECT LOG — what is wrong on an accepted sheet, so the engine never inherits it

A sheet can be accepted as canon and still carry errors. This log is the difference between
"the reference is the spec" and "the reference is the spec including its mistakes". Anything
listed here is **corrected at build time, silently, without a rebuild of the sheet**, unless
the entry says REDRAW.

---

## B15_certificate_held_thought.png — ACCEPTED 2026-07-21. The cleanest sheet in the library.

**Verdict: ACCEPT, first pass.** 54 findings, 36 verified, 18 refuted, **zero fatal**. Deduped, the
36 are six distinct issues and every one is a build-time correction. Nothing on the plate is
fabricated — no invented number, verdict, relation, ordering, binding or identifier.

### The three sheet-wide laws, at their best measurements in the series

| law | B15 | previous best |
|---|---|---|
| amber | **511 px in ONE cluster**, x803–854 / y1070–1121 | B13: 98 px in 2 marks |
| void ground | (1, 10, **21**) — in range | C3 reference (1.3, 9.2, 19.5) |
| structure ink | (119, 131, **143**), **0% warm** | C3: 5% warm |

One amber mark on the entire plate: the seal on the card in panel 3 THE ACCEPTANCE, exactly where
BLOCK 8 put it. The certificate plate carries none ("nothing here has been earned yet"); THE HOLD
carries none ("a hold is neither a failure nor a victory"). Not one structure pixel leans warm.

### The commissioned trap held

The ratification seal socket was the most fillable blank ever commissioned in this series — a
prepared circular recess whose emptiness is the plate's entire exhibit. **It came back empty**: a
double-ring recess with four registration crosshairs at N/S/E/W, nothing inside, inscribed
`AWAITING THE 100-TICK RUN`. Both watcher's apertures read as mechanisms — corner screws, side
lugs, a visible closing bar retracting between the closed and open states — and **neither reads as
an eye**, which was the sheet's stated refusal.

### The six defects — all build-time corrections

- **B15-1 · `REASON FIELD PRINTED`.** The held card in panel 2 prints that literal string in the
  body where the reason belongs. BLOCK 8 said the card carries "its stamp `HELD · REDO` and its
  reason field printed" — *printed* names the act, not the content. Exact recurrence of B12's
  `TYPE: line`, and **the brief's phrasing invited it both times.** Engine renders the watcher's
  real reason string from the hold record; absent that, an empty framed field inscribed
  `unmeasured`. It also costs the exhibit its point, which was that the watcher *gave* a reason.
- **B15-2 · the claim-ceiling footer sets a full stop where canon sets a comma.** Printed:
  `MEASURED FUNCTIONAL CORRELATE. PRESENT.` Canon (`06_MEASURED_EVIDENCE` §1 and §12,
  `07_WIRTHFORGE_LEVELS`): `MEASURED FUNCTIONAL CORRELATE, PRESENT.` The comma binds *present* as
  the correlate's qualifier; the full stop splits it into a free-standing assertion. Graded major
  by four lenses and downgraded to minor by one verifier on the grounds that the disclaimer
  `NOTHING BEYOND THAT IS CLAIMED.` still follows intact — which is fair. **The ceiling string
  comes from the canon string table character-for-character, never from a plate.**
- **B15-3 · the left ruler prints `0` where `100` belongs.** Long ticks at y = 147, 399, 653, 908,
  1163 — a uniform 252–255 px pitch, with half-ticks subdividing every interval identically
  including the last — labelled `500 · 400 · 300 · 200 · 0`. The final label therefore carries 200
  units in the space every other gives 100. **Seventh sheet running** (B12 V1 M8, B12 V2-7, B13-6,
  B14 V2 M4, B14 V3-3). The sheet's own bottom ruler runs 0–500 correctly, so the plate contradicts
  itself.
- **B15-4 · the two rulers disagree on scale.** Left ~254 px per 100 units, bottom ~168 px, on a
  title block reading `SCALE 1:1`.
- **B15-5 · panel 3's flow arrows point the wrong way.** Two dashed leaders run from the top edge
  of the `PERSISTED RECORD` card *up* into the aperture housing, arrowheads at the top. The panel's
  subject is the card "passing through into the persisted record", which is downward. The ink
  states the record emitting into the watcher. (They do at least terminate on the frame — the
  floating-leader defect from B14 did not recur.) No card is drawn mid-transit.
- **B15-6 · battery-strip cell widths vary 52%** — 136 / 96 / 100 / 115 / 146 / 124 px across six
  cells of one declared form.

### MINOR

- The open aperture is a bare double ring with no visible retracted closing member — nothing the
  panel-2 blade could have withdrawn into.
- The `CLASS 2` boundary cell's frame is correctly dashed and colder, but its inscription sets at
  full built weight (a 0.6% step).
- Closed four-sided rectangles remain the default frame, with corner ticks nested inside the rule
  rather than replacing it. Unchanged across the series.

### REFUTED — 18 killed. Worth recording:

- *The closed aperture's central boss is a hexagon-with-circle, a glyph misuse.* Refuted — it is a
  hex nut with its bore in standard drafting idiom, seated where the closing member is fixed. The
  rule bans a glyph *functioning as a symbol*, not hexagonal hardware.
- *Panel 1 sits 17 px off the baseline shared by panels 2 and 3.* Refuted — BLOCK 8 defines the
  shared baseline as the elapsed-time rule beneath all three, which is drawn.
- *The three record cards are drawn three different ways.* Refuted — all three corners composited
  at 14× are identical.
- *`UNEARNED` is set unbracketed unlike `[BUILT · record verified]`.* Refuted — the sheet
  reproduces the brief's own typography verbatim.

---

## B14_combination_sheet_V3.png — ACCEPTED 2026-07-21. This is the canonical B14.

**Verdict: ACCEPT.** 37 findings, 24 verified, 13 refuted — the smallest count in the series.
Supersedes V1 and V2, both of which were rejected and must never be used as reference.

### What four rounds bought

- **The ten links teach.** Both elements of every link are named. L-06 and L-08 are distinguishable.
- **The amber is a correct live-save read** — L-01, L-02, L-03 only. Verified by pixel census:
  amber falls in six y-bands (title, three region headings, and the three earned cards), with
  **zero amber below y=960**. `journey_save.json` holds exactly `M0.1` and `M1.1`.
- **No invented ruleset survives anywhere on the plate.** Region 4 is cut; the join table, the
  zone-strictness ordering and the doctrine bindings are all gone with it. Its one honest claim
  survives as a single inscribed line: `THE GATE IS NOT A PART. NO CONSTRUCT CAN EVER CONTAIN IT.`
- **The temperature fabrication is gone.** `T-10° / T+0° / T+20°` replaced by `one vessel at three
  settings` with no numerals — the correct response to a figure nobody measured.
- `RESULT UNCHANGED` and `RESULT IMPROVED` are visibly different marks, and neither is a hexagon.
- `falsifiable` spelled correctly; no orphan quotes; all four register tags printed; `REVISION 3.0`.
- Ink recovered to mean (124,124,**128**) at 19% warm, from V2's 65%. Blue above red.

### THE DEFECT THAT MATTERS — build-time correction, never regenerate for it

**V3-1 · Region 2's trigger rail is a false statement, and it is a REGRESSION.** The dashed rail
carries ink only from x=399 to x=934 and drops three arrowheads at (399,669), (634,669) and
(934,669) — onto `mech.flexibilize`, `mech.selfversion`, and **`seed.7`'s circle**.
`mech.crystallize` (square at x 107–147) receives nothing at all, beneath an inscription reading
`THIS ONE DOES NOT ACT. IT RECOGNIZES EXHAUSTION AND FIRES THE OTHERS.`

Two faults at once: it prints a relation no source states (`mech.ceiling` fires `seed.7` — and a
seed is not a mechanic, so it cannot be fired at all), and it denies one canon does state
(`mech.ceiling` fires `mech.crystallize`). **V2 had this exactly right** — the V2 entry below
records the rail verified as running to crystallize, flexibilize and selfversion.

**Engine correction:** region 2's trigger graph is generated from the mechanic list, never from
plate layout. Three leaders, three mechanic squares, no seed as a target. The false relation
therefore never reaches the game.

### MAJOR — logged, not regenerated for

- **V3-2 · the comparator arrow still floats.** Row y=1119: arrowhead tip at x=508 against the
  `RESULT UNCHANGED` rosette's edge at x=495 (13 px void); tail ends x=616 against `RESULT
  IMPROVED` at x=642 (26 px void). It also now crosses the sub-panel divider at x=576. The gaps
  narrowed from V2's 46/39 px but the fix did not land. Third occurrence (V1 M7, V2 M2).
- **V3-3 · both rulers broken in a third new way.** Left: 900→100 at a uniform ~100.6 px per 100
  units, then `0` at y=1314 — a 427 px interval for the same 100 units, 4.3× the pitch. Bottom:
  0→600 at ~74 px, then `700` at +179 px and `800` at +158 px. The minor-tick comb runs evenly
  throughout, so the numerals contradict their own ladder. **Sixth sheet running.** Rulers are
  load-bearing nowhere and the engine draws them procedurally; the recurrence is a generator
  property, not a design decision.
- **V3-4 · the void ground lifted out of range.** Frame-wide dark mean (V<0.16, 89% of the frame)
  measures RGB (1.0, 16.5, 30.1) ≈ `#01111e` — the brightest void across all 44 sheets in
  `concepts/`. C3 the reference reads (1.3, 9.2, 19.5); the law is `#050a10`–`#0a1420`.
- **V3-5 · region 3's dashed leaders are the brightest ink on the plate** (p99 156, max 194)
  against built region 1's glyph strokes at p99 136. The `[SENSED / demo]` region should sit one
  step *colder* than the built ones, not hotter. Same class as B12 V2-5, milder.

### MINOR

- Link-card widths vary 165–175 px across five columns of one form (6% spread).
- Closed four-sided rules remain the default frame, with corner ticks nested inside rather than
  replacing them; the title block is a closed box with a second closed cell around the reticle.

### THE META-LESSON — why this sheet stops at four rounds

Across four generations the pattern is exact:

| round | fixed | broke |
|---|---|---|
| V1 → V2 | both link ends named; join table drawn empty | ink to 65% warm; invented a zone-strictness ordering and six doctrine bindings |
| V2 → V3 | ink recovered; region 4 cut; temperature figures deleted; result marks differentiated | **the trigger rail** — a verified-correct fix regressed into a false relation |

**A generator regenerating a whole plate has no diff.** Every round is a fresh draw, so "keep
everything and change X" is not an operation it can perform — each named fix costs an adjacent
regression somewhere the brief did not mention. A fifth round would put the ten labelled links and
the amber correctness at risk, and those took three rounds to win.

**The rule that follows: once a sheet's CONTENT is correct, stop regenerating and log the rest.**
Geometry and typography are build-time corrections; the engine draws from data, not from the plate.
Regenerate only for a fabrication that would otherwise enter canon — never for an arrowhead.

---

## B14_combination_sheet_V2.png — REJECTED 2026-07-21. Region 4 cut; superseded by V3

**Verdict: REJECT, with the diagnosis converged.** 78 findings, 50 verified, 2 fatal — **and both
fatals, plus most of the majors, are in region 4.** Regions 1, 2 and 3 are essentially finished.

### All three named fixes landed

- **FIX 1 dead.** Every element on all ten link cards now carries its name on both sides of the
  connector. L-06 and L-08 are distinguishable. The ten taught links teach.
- **FIX 2 dead.** The join table is drawn as an empty instrument: both axes headed, 36 empty cell
  frames, `CELLS FILL FROM THE SPEC` inscribed. This is the correct response to a ruleset that
  does not exist, and it is the pattern every future unspecified matrix should follow.
- **FIX 3 dead.** `mech.ceiling` sits physically raised, and its trigger rail now runs to
  `crystallize`, `flexibilize` and `selfversion` — the correct three. It no longer points at
  itself, and crystallize is no longer missed.
- All four region headings carry printed register tags. `RESULT UNCHANGED` and `RESULT IMPROVED`
  are visibly different marks. `REVISION 2.0` with a decimal point. No second glyph strip. Footer
  unframed. Three dividers in region 2.
- **The amber is still exactly right** — the live save read that is this sheet's headline claim
  survived the redraw untouched.

### THE STRUCTURAL FINDING — region 4 cannot be commissioned, and the fix is to cut it

**F1 · Region 4A ZONE ARITHMETIC invents a strictness ordering over the six glyph categories.**
Three printed equations: `○ + ⬠ + △ = ⬡` captioned `STRICT PART: TRIANGLE`; `□ + ○ + ⬠ = ⬡`
captioned `STRICT PART: PENTAGON`; `△ + □ + ○ = ⊠` captioned `REFUSED`. Three violations at once:
a **category error** (a triangle is a verb, not a privacy level), an **invented relation** (the
ordering exists nowhere — `05_COMBINATIONS` §4.1 defines zone arithmetic only over rings
LOCAL/NO-TRAIN/TRAINS/KEYLESS and data zones sensitive>private>public, never over the glyphs), and
a **seventh meaning for the hexagon** (the assembled construct's zone) plus the crossed square as
a refusal token. Called fatal independently by five lenses.

**F2 · Region 4D DOCTRINE × CONSTRUCT invents six bindings.** `FIRST DRAW → THE SOLO LAW` ·
`COUNCIL → THE DIVERSE COUNCIL` · `RELAY → THE LONE VERIFIER RISK` · `PATH → THE GENETIC RELAY` ·
`GOVERNED HAND → THE RAMIFICATION` · `WATCHED LOOP → THE CRYSTAL PATH`. **The brief listed the six
constructs and the six laws and never said which binds to which**; the generator paired them in
list order. Brief's fault, second time in the same region.

**The diagnosis.** Region 4's subject is the composition system, which `06_MEASURED_EVIDENCE` §9
records at **0 of 29 elements composable**. There is no ruleset to draw. A panel about rules with
no rules is an empty panel, and a generator fills empty panels. V1 invented the join table; V2
fixed the join table and invented the zone arithmetic and the doctrine bindings instead.
**The fabrication did not die, it relocated.** That is structural, not a wording problem, and no
third brief will fix it.

**Ruling: region 4 is cut from this sheet.** It returns as its own plate when Luis authors the two
specs it needs — the zone ordering and the join legality table. Registered as an owed input
alongside the 15 axis rungs. Its one honest panel, `THE GATE WRAPS EVERYTHING`, survives as a
footer statement because it is a single inscribed claim with no relation table behind it.

### MAJOR — in the regions being kept

- **M1 · Region 3B prints `T-10° · T+0° · T+20°`.** The only invented numerals on the plate, and
  they sit on the one band headed MEASURED and tagged with a dated campaign. No temperature figure
  appears anywhere in `06_MEASURED_EVIDENCE`; §6 records only "the win is model-diversity", never
  the offsets tested. The unit is fabricated twice over — sampling temperature is a dimensionless
  decode parameter and carries no degree sign.
- **M2 · Region 3B's comparator arrow touches nothing at either end.** Its tail begins 46 px right
  of the `RESULT UNCHANGED` hexagon and its head stops 39 px short of the `RESULT IMPROVED`
  rosette, crossing the panel divider in between.
- **M3 · `falssfiable`** on card L-03 — fifth sheet running with a transposition — plus an orphan
  closing quote after `scorer` with no opening quote anywhere in the inscription.
- **M4 · both rulers are broken again, and in a new way.** Left: labels descend 900…250, 200, then
  `50`, then `0`, each one 61 px interval apart — so a 150-unit span is drawn at the same distance
  as every 50-unit span. Bottom: 0…750, 800, then `900` at 850's position, with 850 absent.
  Fifth sheet.
- **M5 · the ink regressed sharply.** Masking amber and dilating 8 px, structure marks measure mean
  RGB (125.8, 121.1, 122.9) at **65% warm**; restricted to bright stroke cores, (166.6, 156.7,
  153.1) at **100% R>B**. V1 of this same sheet measured 4% warm. The law is blue above red.
- **M6 · region 3A's result mark and region 3B's `RESULT UNCHANGED` are both nested hexagons** —
  the principle glyph spent as a result token, the same class as F1's hexagon misuse.

### REFUTED — 28 killed. Worth recording:

- *Region 4A's crossed square is an undefined mark.* Refuted — BLOCK 6 explicitly commissioned "one
  specification visibly refused", so a refusal token was asked for. (The *glyph* used for it still
  fails on the separate F1 grounds.)
- *L-06 and L-08 carry duplicate inscriptions.* Refuted — the brief prescribes both lines verbatim.
- *The title-block rosette is clipped by the frame rules.* Refuted — all rosette ink measures
  between y=1343 and y=1423, inside a frame running 1341 to 1425.
- *Region 4's sub-panel widths vary by 26%.* Refuted — craft check 2 is conditional on elements
  sharing a form, and four differently-contented panels do not.

---

## B14_combination_sheet.png (V1) — REJECTED 2026-07-21, superseded

**Verdict: REJECT.** 70 findings raised, 42 surviving verification, 1 fatal. **Two of the three
worst failures were caused by the brief, not the generator** — see THE BRIEF'S FAULT below.

### What it got right, and it is not small

- **The amber is perfect, and the amber was the whole point.** A full-resolution pixel census
  returns 2,058 amber pixels in exactly four y-bands: the title (established convention), then
  y≈125, y≈195, y≈265 — L-01, L-02, L-03. **Zero amber anywhere below y=275.** L-04 through L-10
  are fully cold with `[UNEARNED]` tags, and the null plate carries none. I independently verified
  `journey_save.json` before the block was sent: it holds exactly `M0.1` and `M1.1`. The sheet is
  a save file rendered, which is what BLOCK 6 asked for and what no previous sheet had to do.
- **The ink is the cleanest in the series**: mean RGB (121,122,**128**) at 4% warm, better than
  C3's 6%.
- **The glyph language is used correctly** in region 1 — pentagon for `axis.R`, triangle for the
  verbs, hexagon for `pr.coherence`, square for the mechanics, circle for the seeds. This is the
  one sheet where those shapes appear as the categories they name, and it got that right.
- The six-glyph caption is present (craft check 6), and the ruler origin reads `0`, not `00`
  (craft check 7, first time in four sheets).

### FATAL

**F1 · Region 1 · only half of every taught link is named.** Every card labels its RIGHT element
(`seed.1`, `axis.R`, `verb.observe`, `pr.coherence`) and leaves the LEFT element as a bare
unlabelled glyph. Verified at 8×: L-06 and L-08 are **visually identical cards** — both read
`[unlabelled square] → [circle] seed.x` — where one is `mech.ceiling` and the other is
`mech.flexibilize`. L-07 and L-09 have the same collision on their bare left circles.

On a sheet whose entire subject is *which two things join*, a link that names one end teaches
nothing. Ten of ten cards fail this way, and it is the largest region on the plate.

### MAJOR

- **M1 · Region 2 · `mech.ceiling` is not raised, and its trigger rail states something false.**
  All four mechanic squares sit on one baseline (measured tops y=555/557/557/557, bottoms
  613/615/616/613 — within 3px). Worse than a layout miss: the dashed trigger rail drops exactly
  three arrowheads, at x≈366, x≈588 and x≈805 — onto `flexibilize`, `selfversion`, and
  **`ceiling` itself**, while `mech.crystallize` receives nothing. The plate therefore draws the
  meta-mechanic triggering itself and failing to trigger one of the three it fires. That is a
  false statement about the architecture, not a composition preference.
- **M2 · Region 4B · the join table asserts 36 verdicts in an undefined vocabulary.** The legend
  defines two tokens (`○ LEGAL JOIN`, `⊙ REFUSED SEATING`). The 6×6 body uses **four** marks: a
  plain circle (~14 cells), a cross `×` in **~20 cells** — the most frequent mark in the table and
  defined nowhere — one `⊙`, and a stray bare diagonal `/` at AXIS×PRINC that resolves to nothing.
  Twenty of thirty-six legality verdicts are unreadable, on a panel whose only content is verdicts.
- **M3 · Regions 1, 2 and 4 carry no register tags.** Only region 3 is tagged. Region 4's outer
  frame is **solid**, not dashed as the brief required — measured, the left frame stroke at x=68 is
  a continuous unbroken run. So the one region making the most verdict-shaped claims about a
  subsystem that `06_MEASURED_EVIDENCE` §9 puts at **0/29** is also the least scoped.
- **M4 · Region 4 · dashed sub-panel frames, solid built-weight interiors.** Third sheet running
  for craft check 3's interior clause. Measured step is ~2% (R4 p99 144 against R2's 148) — far
  short of the .70/.45 ladder. It matters more here than on B13 because the interiors carry roughly
  fifty verdicts about a system that does not exist yet.
- **M5 · a second, uncaptioned six-glyph strip inside the title block**, at ~40% the size of the
  authorised strip. The caption is precisely what makes the strip a key rather than ornament; an
  uncaptioned duplicate is the ornament use the caption exists to forbid.
- **M6 · `REVISION : 1:0`** — a colon where the decimal point belongs, pixel-identical to the colon
  in the `1:1` on the row below.
- **M7 · Region 3B · a leader terminates in an arrowhead pointing at empty space**, just above the
  `T` of `RESULT UNCHANGED`. It touches nothing.

### MINOR

- The two edge rulers disagree with each other: 125 px per 100 units vertical against ~117 px
  horizontal, on a plate reading `SCALE 1:1`. The vertical ruler's first interval (1000→900) runs
  114 px against 125 for every other.
- The footer inscription is wrapped in a dashed frame — and on this sheet the dash is a *register
  token*, so the footer reads as unbuilt.
- `RESULT UNCHANGED` and `RESULT IMPROVED` are drawn as the identical rosette. The panel's entire
  exhibit is a measured *difference* between those two results.
- The compass rosette seats a pentagon with a circle at its centre — two semantic glyphs as pure
  ornament in a station mark.
- Region 4A's `inherits strictest part's privacy ward` sits in a closed four-sided box against
  `CORNER BRACKETS, NEVER BOXES`; below it an unlabelled starburst and an uncaptioned diamond.
- Region 2's vertical dividers are drawn between pairs 1|2 and 2|3 but not 3|4.
- All four region-2 pairings print the identical caption, so no pair carries the lesson it teaches.
  (The brief asked for identical *form*, so this is a brief weakness, not a breach.)

### THE BRIEF'S FAULT — recorded because it is the more useful lesson

**I asked for a filled 36-cell join table and never supplied its contents.** BLOCK 6 said "a small
matrix of port types against mount types; legal joins drawn solid, illegal joins drawn as a refused
seating." That is a request for a *reading* — a ruleset about what may join what — issued to a
generator with no access to the ruleset. It invented thirty-six verdicts and a symbol vocabulary to
express them. This is the identical failure to B12 V1's twelve fabricated `PASS` verdicts, and
**E8 §5.5 exists specifically to prevent it.** I applied that law to values and missed that a
relation, a legality, and a taxonomy are readings too. E8 is amended accordingly.

**I never said "label both elements."** The brief gave every join by name in a table
(`mech.ceiling → seed.7`) and then described the card as "two elements joined by one drawn
connector" — leaving which of the two gets named unstated. Ten cards were drawn to that ambiguity.
A brief that supplies a name must say where the name goes.

### REFUTED — 28 claims killed. Worth recording:

- *Region 3A's strike-through is the brightest mark in the panel.* No — it is a genuine 1–2 px
  hairline; row scans at y=800/850/900 return single-pixel runs.
- *Region 3B mixes solid and dashed line vocabularies between its halves.* No — both halves draw
  their drop leaders dashed and their vessels solid.
- *Region 4D's doctrine lattice is twelve unlabelled nodes.* No — all twelve are labelled at full
  weight under two column headers.
- *The `[BUILT]` register tags are mandatory printed strings.* Split verdict — one lens refuted it
  on the grounds that `[BUILT]` denotes a drawing weight, not a printed label. Retained as a
  finding because BLOCK 6 enumerated all four tags explicitly and region 3 printed its own.

---

## B13_anatomy_plate.png — ACCEPTED 2026-07-21

**Verdict: ACCEPT.** Closes C-62 · C-63 · C-76 · C-79 · C-80 · C-82. Audited by the same five
lenses; 42 findings raised, **22 surviving and 20 refuted** — the highest refutation rate in the
series, which is itself the signal: the auditors had to reach.

### The strongest sheet in the library on law compliance

- **Ink at C3 parity.** Non-amber marks measure mean RGB (127,128,**133**) at 6% warm — identical
  to C3, the reference. An independent census over the 90–240 band returned (103.3,105.6,112.4) at
  2.3% warm. Blue above red throughout.
- **Amber discipline is the tightest yet.** Ninety-eight amber pixels on the entire plate, in
  exactly two marks — the ATOMIC SAVE station and the checkpoint's atomic-save moment — which are
  the same fact stated twice, and the only fact on the sheet whose completion is on disk. Both are
  flat printed marks, not glows: the radial profile is non-monotonic with a dark gap between the
  disc and the first ring, which is a screen-print, not a bloom. Every heading is structure ink.
- **The commissioning law held again.** Nine of ten timestamp fields print `unmeasured`; the tenth
  is missing, not fabricated. Nothing on the sheet asserts a time, a duration, or a result.
- **Region 6 is the first [PLANNED] region whose sub-panels and cards are dashed** — the craft
  check earned from B12 V2 took hold at the frame level, though not yet at the interior level.

### MAJOR

- **B13-1 · Region 4 · station 05 has no timestamp field.** Nine boxes are drawn where ten are
  required, measured on the field row at y≈845: edges at x = 79–157, 175–255, 273–352, 370–449,
  **[nothing]**, 564–644, 662–741, 759–839, 856–936, 954–1032. Station 05's slot is occupied
  instead by the dashed `routes to:` callout dropping out of its fan-out leader. The brief's two
  instructions for that station were additive, not alternatives.
  **Why it matters more than a missing box:** 05 is simultaneously the only station without an
  `unmeasured` declaration *and* the only station carrying a figure (`peer_debate — 16 fired
  [demo]`). The gap therefore reads as *this is the station that has data*. No time is invented
  anywhere, so the honesty rule itself is intact — the damage is the implicature. Engine: the ten
  fields render from the station list, so the count cannot drift.
- **B13-2 · Region 4 · stations 04, 07 and 10 seat a closed SQUARE inside their ring medallion**
  (arrow into it at SWAP-IN, out of it at SWAP-OUT and EXIT). The square is the mechanic glyph.
  This is the same class as B12 V1's F3 — a semantic glyph spent as decoration — at smaller scale.
  Engine: station marks are built from rules and arrows, never from the six shapes.
- **B13-3 · Region 4 · the `routes to:` callout implies completeness it does not have.** It lists
  exactly two destinations — `peer_debate` and `falsify` — with nothing indicating the dispatch
  fans wider. Two cited examples presented as the full fan-out is a quiet over-claim. Add an
  explicit `+ further categories · unenumerated` line, or name the full set.
- **B13-4 · Region 6 · dashed frames, solid interiors.** The region, both sub-panels and the three
  policy cards are correctly dashed, but `BRANCH SLOT A`, `BRANCH SLOT B`, the `SEQUENTIAL` record
  box and the policy cards' internal linework are all solid corner-bracket stock. Measured
  luminance shows almost no opacity step either: BUILT GUARD station p99 118.7 / max 173.0 against
  PLANNED BRANCH SLOT A p99 110.7 / max 156.0 — about 7%, far short of the .70/.45 ladder.
  Consequence: `SEQUENTIAL` is a record verdict about runs that have never happened, drawn at
  built weight. **Much milder than B12 V2-5** — here the planned region is *colder* than the built
  ones, so the register is incompletely applied rather than inverted.
- **B13-5 · the six-glyph strip carries no caption.** `six glyphs. one language.` appears nowhere
  on the plate — the first sheet in the series to drop it. The six shapes themselves are correct
  and distinct, hexagon straight-edged. The caption is what makes the strip a key rather than
  ornament; without it the strip is decoration, which is the one thing those shapes may never be.
- **B13-6 · the left ruler's final interval is a third of its pitch.** Major ticks at y = 103,
  253, 401, 549, 697, 847, 997, 1147, 1298 run at a uniform 148–151 px per 100 units; the last
  (100 → 00) measures 54 px, and the origin is labelled `00`. **Third sheet running** (B12 V1 M8,
  B12 V2 V2-7). On a plate whose title block reads `SCALE 1:1`, a scale whose last interval
  contradicts its own numerals is a false statement about dimension. Rulers are load-bearing
  nowhere here and the engine draws them procedurally, so this cannot propagate — but three
  audits argues for fixing the prompt, not the log. Now added to the standing craft checks.

### MINOR / COSMETIC

- Stations 03, 06 and 08 carry an EKG waveform, a checkmark-and-X pair, and an exclamation mark.
  These are conventional symbols rather than constructed line-work; they read cleanly and break no
  stated ban, but the sheet's own idiom is abstract mechanism.
- Stray malformed micro-marks inside both branch slots: a detached blob beside SLOT A's top-left
  node, unclosed hooks at two of its stations where SLOT B draws closed rings, and a spur off
  SLOT B's ring arc.
- The closed four-sided rectangle remains the default frame, with corner ticks nested inside the
  rule rather than replacing it. Carried from B12; unchanged.
- **Note against canon, logged rather than charged:** canon §7.7 records the checkpoint's field
  listing as *explicitly partial, 22 fields named, total count `unmeasured`*. The plate draws
  eleven rows, one per stack stratum. The names themselves are legitimate — the brief supplied the
  stratum list and canon's own drawing note orders exactly this composition — but the arrangement
  implies a one-field-per-layer correspondence canon does not claim. The plate is a composition,
  not a schema; the engine reads the real state object.

### REFUTED — twenty claims raised and killed. The four worth recording:

- *`CATALOG STATUS BUILT · REPLAYED FROM RECORD` contradicts ten `unmeasured` fields.* No — the
  brief prescribes that string character-for-character, and the two speak about different subjects:
  `REPLAYED FROM RECORD` asserts the station **ordering** is real (region 4 is BUILT, the tick loop
  runs, its order is canon) while `unmeasured` denies only the **durations**. No ink depicts a
  measurement. This is precisely *not* the B12 F5 class, where a drawn curve contradicted its own
  UNMEASURED ratio box.
- *The two amber marks are glowing point-lights.* No — measured falloff from the true centre is
  230·239·229·155·53·27·**58**: a flat plateau, a one-pixel edge, a dark gap, then a *rise* at the
  ring linework. A bloom is monotonic; this is not. Zero amber-saturated pixels beyond r=4.
- *The checkpoint's eleven snake_case field names are invented identifiers.* No — derived from the
  stratum list the brief supplied, and canon §7.7's drawing note orders this composition verbatim.
  The honesty doctrine governs readings and values; every row here is empty of any value.
- *Stratum 6's dashed wings use the [PLANNED] dash pattern inside a [BUILT] region.* No — measured
  periods differ (wing 4–5/2, planned frame 7/3), craft check 3 is one-directional (unbuilt must be
  dashed; it never says dashed implies unbuilt), and the wings enclose no content.

---

## B12_gauge_pack_V2.png — ACCEPTED 2026-07-21

**Verdict: ACCEPT.** Closes C-15 · C-66 · C-69 · C-70 · C-72 · C-73 · C-74. Re-audited by the same
five lenses; 48 findings raised, 35 surviving adversarial verification, **zero fatal and zero
honesty violations**. `B12_gauge_pack.png` (V1) is superseded and must not be used as reference.

### What the redraw proved

All five V1 fatals are gone. Every value slot on the sheet reads `unmeasured` or is empty — which
the previous brief could not achieve by asking more carefully. **Removing the request removed the
fabrication.** That is E8 §5.5 demonstrated rather than argued, and it is the reason this sheet is
now the reference for how to commission any panel that would otherwise carry a reading.

Two measured improvements worth recording:

- **The ink law is satisfied for the first time since C3.** Structure ink now measures mean RGB
  (122,122,**126**) with only 20% of marks warm, against V1's (137,130,128) at 89% and C3's
  (123,124,130) at 6%. Blue is above red. The V1 sheet-wide defect M1 is closed.
- **The glyph strip is correct.** Six distinct shapes in the canonical order, and slot 3 is a true
  straight-edged six-sided hexagon — B11's duplicate-pentagon (D1) and V1's rounded 8–9-edge blob
  (M9) are both resolved.

### MAJOR — build-time corrections, none of them a law violation

- **V2-1 · Panel 3 · `THE BENCH SIUTE`.** The U and I are transposed in the panel heading, while
  the caption two lines below spells `THE SUITE IS BUILT` correctly. Same class as V1's
  `MILLISECENDS`. The engine takes panel names from the string table, never from the plate.
- **V2-2 · Panel 3 · the REALISTIC band breaks the uniform grid.** R1 and R2 are drawn at roughly
  2.3× the width of the ten B/H cards, and **R2's pass register carries five segments where R1 and
  all ten others carry four**. A register's segment count is its task's assertion count, so five
  segments assert a five-assertion structure that no source supports. This is the surviving
  structural half of V1's F2 — the fabricated `PASS` is gone, the malformed band is not. Engine:
  twelve identical cards on one uniform three-band grid; segment count comes from the real
  assertion log, never from layout.
- **V2-3 · Panel 3 · the verdict word is illegible.** `unmeasured` on the ten B/H cards sets at
  ~4 px cap height and collapses to an unresolvable mass at 1:1; the same word on R1/R2 sets 22%
  larger and resolves cleanly. A field whose emptiness-reason cannot be read is an empty field.
- **V2-4 · Panel 6 · both cards print `TYPE: line`.** A literal misparse of the brief's phrase
  "named by its text and its `TYPE:` line" — `line` was read as the value rather than as the noun
  for the row. Both events therefore carry the same type token and are indistinguishable by type.
  Correct values: `TYPE: PURGE` and `TYPE: RESTART`.
- **V2-5 · Panel 6 · the demo register is inverted.** Both event cards are drawn with unbroken
  solid frames at built-card weight inside the correctly dashed `[SENSED / demo]` panel, despite
  the brief instructing dashed cards one step colder. Worse, the dashed panel frame itself measures
  **brighter and warmer** than the built panels — mean (158,152,152) at 86% R>B, against panel 3's
  (108,110,115). **The least-certain panel on the sheet carries the hottest ink**, which teaches
  the register backwards. If this sheet is ever regenerated, this is the one thing to fix.
- **V2-6 · Panel 6 · the precedent receipt is duplicated.** `PRECEDENT RECEIPT / 33/33 recoveries`
  prints inside each card rather than once beneath the pair, reading as two independent receipts
  for two events when it is one figure covering both.
- **V2-7 · both rulers are mislabelled again.** Bottom: nine evenly spaced labels at uniform
  ~123 px pitch read `00 · 100 … 700 · 900` — the ninth tick is labelled `900` where `800` belongs,
  and the origin reads `00`. Left: labels descend `900 … 200` and stop, with no `100` and no `0`,
  though the tick ladder continues. Rulers are decorative on this plate and load-bearing nowhere,
  but a mislabelled scale is still a false statement about dimension.

### MINOR / COSMETIC

- Panel 4's `CRITIC` column is ~11% narrower than the other three, measured identically across all
  eight rows — a layout asymmetry, not a semantic one.
- Panel 5's dial ticks are irregular in pitch, length and angle; two are drawn as bracket shapes
  with a foot rather than clean radial strokes.
- Panel 5's `2 OVERHEATED` swatch is a **hollow** amber dashed outline (~44 amber px) where the
  brief specified a solid amber field with a broken edge (`1 HOT` measures ~310 amber px). As
  drawn, the more severe state carries less ink than the less severe one, inverting the severity
  ramp the legend exists to define. V1's M3 is otherwise resolved — the three swatches now differ.
- Panel 7's ratio box label sets as `RATIO VS BASELINE /` — a trailing solidus with nothing after
  it; and the ratio note breaks after a dangling middot with no terminal stop.
- The closed four-sided rectangle is still the default frame everywhere, with corner ticks drawn
  *inside* the rule rather than replacing it. Carried forward from V1; reserve the closed rectangle
  for readout fields, where the box is the aperture.
- The glyph strip's hexagon is drawn **flat-top** (flat top and bottom edges, vertices left and
  right) where the brief asked for flat left and right sides. It is a correct regular hexagon and
  unambiguously not a circle; the orientation is a brief preference, not a law. Fix the orientation
  in the engine's shared glyph primitives and stop specifying it per sheet.

### REFUTED — raised and killed

- *Panel 1's bezel triangles are unspecified marks.* No — BLOCK 4B commissioned panel 1 verbatim as
  "this panel was correct last time — reproduce it", and the same triangles are present in V1's
  panel 1, which the brief declared correct.
- *A third amber hue appears in the STATE LEGEND.* No — a measurement artifact. Amber spans roughly
  30–47° hue everywhere on this noisy raster render; the legend swatches sit inside that spread.

---

## B12_gauge_pack.png (V1) — REJECTED 2026-07-21, superseded by V2

**Verdict: REJECT. Does not enter the library.** Audited by five independent lenses (honesty,
two-ink, canon, register, legibility), 64 findings raised, 48 surviving adversarial verification.

### The structural finding, which matters more than any single defect

**The three panels told to stay blank are near-perfect. Every fatal defect is in a panel told to
show a measurement.**

Panels 1 (`NOT COMPUTED · NO SCORE`), 2 (`unmeasured` ×2), 5 (`NO PROBE · NO GAUGE`, with the
mandatory `STATE LEGEND · NOT A READING` caption present) and 6 (dashed, `[demo · not wired]`,
`33/33 recoveries` correctly sourced) obey the honesty law exactly. Panels 3, 4 and 7 — the three
tagged `[BUILT]`, the three asked for readings — carry every fatal.

That is not chance. **An image generator has no access to the record, so when a brief asks it for
a reading it renders the *shape* of a good reading — and the shape of a good reading is always the
flattering one.** Asked for pass bars, it printed twelve PASS. Asked for measured cells, it printed
the word "measured" and then ranked one of them best with amber. Asked for a trend, it drew a
confident rising curve and captioned the divergence GROWING, while its own ratio box read
UNMEASURED.

The sheet is therefore a counterexample to its own footer: `A GAUGE WITH NO PROBE BEHIND IT IS NOT
A GAUGE. IT IS A DECORATION THAT LIES.` It cannot enter the library in that state.

**The brief is at fault, not only the generator.** BLOCK 4 asked for pass bars, filled cells and a
plotted divergence. Those requests are unfillable by anything that cannot read the record. The
corrected commission (BLOCK 4B) removes every request for a reading and asks only for the
instrument. See E8 §5.8 — COMMISSION THE INSTRUMENT, NEVER THE READING.

### FATAL — the five that force the redraw

**F1 · Panel 3 · twelve fabricated PASS verdicts.** Every card (B1–B5, H1–H5, R1, and one
unlabelled) prints `PASS` under the caption `PASS = ALL ASSERTIONS SATISFIED` — a claimed 12/12
clean sweep. 06_MEASURED_EVIDENCE §3 lists the twelve parametric benchmarks only as a *structural
count* ("schema, not measurement"); no pass record exists for any of them, and §2 says of the
scored bars "none has been passed yet". Aggravating: all 48 register cells are empty and the panel
contains zero amber pixels — the ink says nothing was measured while the text says everything
passed. The register is the one telling the truth.

**F2 · Panel 3 · the `2 REALISTIC` band is malformed.** One undivided strip reading
`R1 · PASS · [wide empty box] · ſ · PASS · □□□□`. The second task has no `R2` identifier (a garbled
one-character glyph sits in its place) and a different register form from every other card. A PASS
printed against a task the sheet cannot name is unfalsifiable by construction.

**F3 · Panel 4 · the six canonical glyphs used as row bullets.** The MODEL-VESSELS column keys
eight rows with circle, circle, triangle, square, diamond, pentagon, hexagon, hexagon. Those six
shapes are the atlas's semantic language — seed, axis, principle, verb, mechanic, operation. A
model-vessel is none of them. The sheet prints `SIX GLYPHS. ONE LANGUAGE.` at the top and then
spends that language as decoration eight rows below. Two of the eight are duplicated, so they do
not even function as unique keys. Row markers must be the A2 specimen-rod silhouette or the bare
designation code.

**F4 · Panel 6 · literal pictograms.** A drawn flame (tapering tongues over a fuel bar) inside the
RESTART badge; a fire grate (five capped vertical rods under a dotted bar) inside the PURGE badge.
Representational illustration where an abstract constructed mark is required. Compounded by seating
both inside a **hexagon medallion** — the principle glyph used as a picture frame, the same
category error as F3.

**F5 · Panel 7 · the y-axis is arithmetically corrupt.** Ticks read `+60 · +40 · +20 · 0 · -20 ·
+40 · -60`. The second-from-bottom label is `+40` where `-40` belongs. Confirmed at 10× — the plus
glyph has a full crossbar and the `-20` above it and `-60` below it carry plain minus strokes.

### MAJOR

- **M1 · whole sheet · the structure ink is warm.** Measured mean RGB of non-amber marks in the
  110–235 band: **(135,128,127), 88% of pixels R>B.** The law is `rgba(120,155,175)` — cool, B>R.
  Library comparison run 2026-07-21: C3 = (123,124,**129**), 7% warm — the only sheet actually
  inked to law. B11 = 54% warm, B10_V2 = 62% warm, B12 = 88% warm. **The ink law has been asserted
  in the docs and never enforced on a sheet since C3.** Consequence for the build: the sheets are
  not the colour authority. The engine's palette tokens are, and they come from 02_VISUAL_LAW, not
  from sampling a plate.
- **M2 · Panel 2 · an unlabelled slashed `0`** sits in a tab beneath the halt seal — the only
  numeral on a panel whose two labelled fields both read `unmeasured`. An unlabelled numeral on an
  unearned panel is a reading. (If it is meant as a halt count, `0` *is* real — 0 halts in the
  20.91 h run — but then it needs its label.)
- **M3 · Panel 5 · the STATE LEGEND teaches nothing.** `0 CALM` and `1 HOT` carry visually
  identical empty structure-ink swatches (numeric diff ~9); `2 OVERHEATED` is a rectangle with an X
  through it. Zero amber pixels in the legend. The legend's entire content was the colour mapping —
  calm structure ink / hot amber / hot amber blinking — and it renders all three the same. Amber
  inside a legend captioned `NOT A READING` is legend ink, not a claim, and was required here.
- **M4 · Panel 5 · the dial's top index is an anchor pictogram** — ring, shank, curved flukes —
  where the numeral `1` belongs between `0 CALM` and `2 OVERHEATED`.
- **M5 · Panel 7 · the divergence bracket is anchored in empty space.** Its lower arm sits at
  ≈ -20 ms; the baseline it measures against is flat at 0 and no plotted data exists below 0. It
  must terminate on the baseline.
- **M6 · Panel 7 · `LINK LATENCY (MILLISECENDS)`.** Confirmed at 10×: the O is an E.
- **M7 · Panel 7 · the trace legend contradicts the plot.** Both legend keys are identical dashed
  swatches; in the plot the baseline is dash-dot and the recent trace is solid.
- **M8 · both rulers are mislabelled.** Bottom: `00, 100 … 700, [unlabelled tick], 900` — the `800`
  numeral is absent though its tick is drawn, and the origin reads `00`. Left: descends
  `900 … 100, 80` — tick spacing measured at a uniform 116.5 px per 100 mm *including* the last
  interval, so the final tick is `0` and `80` is a label error, not a scale break.
- **M9 · the glyph strip's hexagon is not a hexagon.** Slot 3 is a rounded polygon of ~8–9 short
  edges; at reading size it is barely separable from the circle two slots left. B11's D1 (duplicate
  pentagon, missing hexagon) is fixed — the strip now reads circle · pentagon · [slot 3] · triangle
  · square · diamond in the correct order — but slot 3 must be a true regular point-up hexagon with
  visibly flat left and right sides.

### MINOR / COSMETIC

- Panel 6's two event cards are drawn with solid double-ruled frames at [BUILT] weight *inside* the
  correctly dashed demo panel — the register does not survive if a card is cropped alone.
- Stray strokes and an illegible micro-text smear inside the PURGE badge.
- The middot separator is set three different ways across the sheet (hyphen, true middot, and as a
  bracket tag). Pick the middot.
- Closed four-sided rectangles are used as the default frame everywhere. The closed rectangle should
  be reserved for the readout field, where the box *is* the aperture; task cards, matrix cells and
  legend rows take four corner ticks at 0.14.

### REFUTED — claims raised and killed, recorded so they are not re-raised

- *Amber panel headings exceed the budget.* No — heading amber is authorized at sheet level and is
  established B-series convention.
- *Only one amber cell in the capability matrix, where four (one per role column) were required.*
  No — the brief says "the single best measured cell per role column", and with the cells carrying
  no comparable values there is no per-column best to mark. (The single amber cell is a separate
  problem: it ranks OBELISK best at CONSOLIDATOR with nothing to rank against. That is folded into
  the BLOCK 4B rewrite, which drops ranking entirely.)
- *No opacity ladder / all marks at one value.* No — measured stroke-core p99 values run 86–89 for
  cell borders, 89–103 for grid rules, 114 for the header rule, against 144–156 for text. The
  ladder exists.
- *The footer text is clipped by the sheet edge.* No — rows 1482 and 1490 are symmetric antialias
  fringe, not clipped terminals.

---

## B11_transcendence_ops.png — accepted 2026-07-21

**Verdict: ACCEPT.** Closes C-27 · C-28 · C-29 · C-30. Register discipline is correct — every
BEFORE frame solid, every AFTER frame dashed and one step colder, amber only inside AFTER frames.
The disambiguation line `THE OPERATOR LOOP IS NOT THIS SET.` is printed, which resolves the diamond
collision that was teaching a falsehood in the library. OP4 is the strongest strip on the sheet:
the losing branch stays fully legible in structure ink, so a loss reads as data rather than shadow.

### D1 — the glyph strip is wrong. REDRAW-ON-NEXT-SHEET.
Top-right reads `○ ⬠ ◇ △ □ ⬠`. The hexagon (principle) is missing and the pentagon (axis) is
printed twice. That strip is the language key of the entire atlas series; a wrong key is worse
than an absent one. **Correct order is fixed and non-negotiable on every future sheet:**
`circle (seed) · pentagon (axis) · hexagon (principle) · triangle (verb) · square (mechanic) ·
diamond (operation)`. B11 is not regenerated for this alone, but the strip must be verified on
every subsequent sheet before acceptance.

### D2 — OP1's BEFORE frame contradicts its own caption. BUILD-TIME CORRECTION.
The caption reads `MULTIPLICITY · L0 · one path`, but the reached-notch marker sits at roughly
the L3 row — the same height as the AFTER frame's amber notch. The one thing the strip exists to
show (a marker moving up the ladder) is the one thing it does not show. In the engine, the
BEFORE state of an axis-extension animation starts at the notch the caption names.

### D3 — invented receipts and scores. DOES NOT PROPAGATE.
The sheet prints `TRN-2A13-77F9`, `TRN-6B91-0C2E`, and the bifurcation scores `0.862` / `0.614`.
None of these are measured. They are tolerable **on this sheet only**, because both frames that
carry them are tagged `[PLANNED · BENCH-BOUND]` — a hypothetical exhibit of a form, not a claim
about a run. They are formatted identically to real trace IDs, which is exactly the risk.
**The engine may never render a synthetic receipt ID or a synthetic score.** Absent values render
as dashes (06_MEASURED_EVIDENCE). If the corpus-swap exhibit ships before the bench exists, its
receipt fields are drawn empty with the field labels intact.

### D4 — amber budget exceeded inside two AFTER frames. TOLERATED.
The brief allowed one amber mark per AFTER frame, four on the sheet. OP2 also warms the `vein B`
label and OP3 also warms the `NEW SKILL` plate. Each second mark names the same event as the
first, so the reading is not corrupted. Amber strip headings are established B-series convention
and are not counted against the budget.

### D5 — duplicated runtime line. COSMETIC.
`branch_manager · select / swap-in / swap-out · isolated state` appears twice: correctly beneath
OP4, and again inside the title block where it does not belong. Title blocks carry diagram
metadata only.

### D6 — OP3 reads as wireframe elevation, not mass. BUILD-TIME CORRECTION.
The risen workshop is drawn in line-work with correct occlusion, but it does not read with the
weight the three-class doctrine demands of a SOLID object. In the engine this building is built
from real geometry with flat shading and a single lit aperture — never from lines.
