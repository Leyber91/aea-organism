# 00 · HOW TO USE — the GPT-Image-2 protocol (v3, refined after REF-01)

ChatGPT Images 2.0 (gpt-image-2, Apr 2026) runs a REASONING PASS over the prompt before drawing:
it plans composition, counts objects, and checks constraints. That changes how we drive it. This
protocol replaces v2. Folders stay in generation order 01 → 12; REF-01 (the accepted
`01_THE_INSTRUMENT_AT_REST` image) is now the canon anchor for everything.

## What changed and why (the investigation, distilled)

1. **Paste, don't rely on attachments.** The documented path is the PROMPT itself. Each SPEC now
   contains a paste-ready structured prompt (scene → subject → key details → constraints — the
   model's preferred order). Attach nothing except reference IMAGES.
2. **Anchor with the reference image, not chat memory.** Style consistency is strongest when you
   ATTACH the locked REF-01 image to each new generation and say what it is by index:
   "Image 1 is the canon style reference — do not redesign the world." Chat-memory canon drifts;
   re-specify the critical invariants every turn (the CANON BLOCK below).
3. **One image per message.** Batch "3 variants" produces near-duplicates (we measured it:
   Image_1 vs Image_4 were the same frame). Generate ONE, then refine with SMALL SINGLE-CHANGE
   follow-ups ("brighten only the pulse; keep everything else the same"). If you want a true
   alternative, name the axis: "second take — vary ONLY the camera height."
4. **Constraint budget is real (~7–8 hard constraints).** The SPEC prompts now carry a SHORT
   hard-constraint list; everything else rides as scene description, which the reasoning pass
   handles well.
5. **Text rules:** every literal string in "quotes", typography stated as a constraint, "render
   each string once, verbatim, no extra characters"; spell risky words letter-by-letter if they
   misrender. Dense-text frames (10–12) want quality high.
6. **Size explicitly:** "landscape 1536×1024" (or 2K 2560×1440) for wide frames; "portrait
   1024×1536" for 05_THE_STAKE.


## FIELD LESSONS (measured across REF-01..03 — these override the general guidance above)

1. **Fresh generations beat surgical edits.** Text and small elements come out CLEAN on a fresh
   roll (REF-03: five HUD strings + empty fog cages, zero errors, first try) and get WORSE under
   edit chains (REF-02: MEMORY->NEMORY->fixed->HANDS·POG; fog dots survived two dedicated fixes).
   When a take has more than ~2 flaws, fold ALL corrections into one REGENERATE-with-changes
   instead of chaining micro-edits.
2. **Cap repair rolls at 2 per flaw.** If it persists and the engine corrects it by code anyway
   (fog vertex dots, missing ring labels), rule it non-binding in REFS.md, lock, move on.
3. **Scale constraints under-obey on the first pass.** "4% of frame width" produced 12%. Fix with
   RELATIVE language — "three times smaller" — and always add "keep its exact design" so the
   shrink doesn't redesign the subject.
4. **Preempt known model tics in the BASE prompt.** Fog cages: say "hollow and dark inside, no
   bright vertex points" up front — asking later bounces off.
5. **Avoid edit rolls on text-heavy frames.** Every edit roll can wobble untouched text. Get the
   base right; if text breaks, fix THAT string by quoting it, nothing else.
6. **The anchor chain works.** REF-01 attached + the CANON BLOCK held style perfectly across
   three frames. Never generate without both.
7. **Adopt-back rule.** When the model invents something better than the spec, it becomes canon
   and flows back into the SPECs: ember-in-cage organs (01), the ember-dust shockwave ring (02),
   the curved horizon limb at altitude + the probe's craft design (03).
8. **Spec MATTER, not information (the 08 lesson).** A spec that describes a diagram gets a
   flat diagram. Every frame must be staged as a PHOTOGRAPH of physical matter in a place —
   plate, void, ring — with a camera, perspective, depth of field, and material texture; the
   information rides ON the matter (debossed labels, light in milled grooves, mounted modules).
   The set's premium feel IS material physics; "diagram-class" frames were a category error.
9. **Reference-reuse (the no-re-attach rule).** WITHIN one continuous conversation the model
   keeps every image it already rendered in context — so stop re-attaching. Only attach a
   reference the FIRST time it is needed in a conversation (REF-01 at frame 01; REF-07 at frame
   07 for the bench material). After that, reference by MEMORY IN WORDS: "match the exact
   style/material/palette of the images you generated earlier in this conversation — the world
   plate and the bench plate." Re-attach ONLY when (a) starting a fresh conversation, or (b)
   drift appears (then re-attach the one that drifted and say "match this"). Fewer attachments,
   same anchor — the words carry the canon the model already holds.

## THE CANON BLOCK — paste with EVERY generation from 02 onward

> Image 1 attached is the canon style reference (REF-01). Apply its exact style: near-black
> void, thin engraved steel grey-blue hairlines, amber only as light emitted from within, vast
> negative space, matte materials. Do not redesign the world: the core is a faceted amber
> icosahedron wrapped in exactly two thin tilted tori with a hair-thin vertical beam; organs are
> identical thin wireframe octahedral cages — an earned organ has a bright amber ember inside,
> a fog organ is COMPLETELY empty; the three rings are drawn sealed-double (inner), solid
> (middle), finely-dashed (outer). No people, no watermark, no extra text, no new elements.

## The per-frame ritual

1. Same conversation as REF-01 (or a fresh one — the attached reference makes either safe).
2. Attach the REF-01 image. Paste: the CANON BLOCK + the SPEC's PROMPT section. Send.
3. Judge against the SPEC's inventory. Fix with one single-change message per flaw:
   "Change only X. Keep everything else the same." Repeat the preservation list each time.
4. When right, save as `<folder>_<take>.png`, declare "this is REF-<nn>, canon for this frame",
   and move to the next folder.
5. If a frame needs a true alternative: "second take — vary only <axis>".

## Generation order (unchanged)

01 world anchor → 02 ignition → 03 flight → 04 fog frontier → 05 stake (portrait) →
06 whole one → 07 seat → 08 fall-through → 09 earned title → 10 bench plate → 11 run trace →
12 flight HUD. Interfaces last so they inherit the full material + type language.

## The shared save-state (all specs agree — the set is ONE game)

Mid-game, rung 2. `c-04` = THE DRAW · THE LADDER · THE MEASURE earned RESTORABLE COHERENCE;
`c-07` = THE DRAW · RECALL · THE MEASURE earned BACKWARDS CHANNEL. Organs lit: MOUTH, GOVERNOR,
MEMORY, LOOP. Fog: SENSES, HANDS. `POWER 1998 LIVE` · `RODS 7` · `MEM 48` · `LAST 1.44S ·
BEST 0.98S` · zone `PRIVATE`.

Masters `01_STYLE_LAW.md` / `02_WORLD_BRIEF.md` stay the law's source of truth. REF-01 additions
now canon: ember-in-cage organs · two-tori core · per-zone ring treatments (sealed/solid/dashed)
· engraved labels-on-approach · the caption line "EVERY LIGHT IS SOMETHING THAT REALLY HAPPENED"
as the game's standing tagline surface.
