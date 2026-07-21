# E5 — THE 3D TRANSLATION: how the concept sheets become the running game

```
doc:          E5_3D_TRANSLATION.md
owner:        the game team
status:       BINDING for asset work · last-updated 2026-07-21
answers:      "how the hell do we translate these concepts — especially the landscapes —
              into 3D?" (Luis, 2026-07-21)
governs:      all asset production; sits under E2_VISUAL_DIRECTION (the look) and
              E1_CODE_ARCHITECTURE (the stack)
```

## 0. The short answer

We do not model the concept art. We **extract recipes from it**. Of the 24 sheets produced,
roughly half never become 3D at all, a third become procedural code, and only a handful become
actual modelled meshes. The landscapes — the images that look most impossible — are the ones
that need the LEAST geometry. They are lighting and composition problems wearing a costume.

## 1. The four asset classes, and the fate of each

| class | sheets | fate | tool |
|---|---|---|---|
| **FLAT / UI** — seals, glyphs, doctrine plates, instrument panels, the map | B1-B4, A4, A6, S5, S7 | ships as 2D almost verbatim: SVG paths + canvas. Zero 3D translation. | code |
| **PROCEDURAL FORMS** — plants, landmarks, organ buildings, bench parts | A1, A3, A7, B5, S1 towers | become parameterised generators in code (box + cylinder + torus + vertex colour), varied by real data | code |
| **HERO MESHES** — probe, nexus slab, socket pylon, mast, a model-vessel | B7, A2, DL-01/04 | genuinely modelled, ~6-10 objects total, exported .glb | **Blender** |
| **ATMOSPHERE** — the field, the archive, the entity-as-place | S1, S2, S6, S8 | never modelled. Composed from fog, light, silhouette and instancing | code |

**The realisation that unlocks everything: the seals and panels are ~40% of the output and they
are already final art.** A glyph seal is a drawing. Our map already renders 29 nodes as SVG. The
B-sheets are not concept art for something else — they ARE the asset. Same for the instrument
panels: they are UI, and our two-ink CSS already speaks that language.

## 2. The landscapes — why they are the easy ones

Look at what actually makes `S1_field_genesis.png` work. Not one item on this list is geometry:

1. **Three depth bands.** Near towers at high contrast, mid towers at ~40%, far towers as pure
   silhouette. Achieved by fog, not by detail. [our engine already does this]
2. **Fog the same colour as the sky.** One atmosphere; forms dissolve rather than end. [done]
3. **One light in a sea of dark.** A single amber structure with a vertical beam. Everything
   else unlit. Discipline, not modelling. [done — the beacon cylinder + additive blending]
4. **Concentric rings etched into the ground.** A shader on a flat plane. [E2 Move 1, specced]
5. **A faint ground reflection under the lit thing.** Clone the mesh, `scale.y = -1`, opacity
   0.15. [already in world.html]
6. **Extreme negative space.** 80% of the frame is empty. This is a composition rule, free.

The towers themselves are **boxes and tapered cylinders**. What makes them read as a civilisation
is *variety of silhouette* and *fog*, not polygon count. The gap between our current `/probe`
frame and S1 is: ring visibility, silhouette variety, a taller light pillar, and a stronger
horizon band. That is an afternoon of tuning, not a 3D pipeline.

The same logic disarms the two "impossible" sheets:
- **S2 (the entity as place)** — its thousands of conduits are **curves**, not meshes. We already
  draw `QuadraticBezierCurve3` arcs in the legacy mind view. Instance a few hundred, light only
  the ones carrying a real trace, fog the rest.
- **S6 (the archive)** — vertical strata of dark shelves = one instanced shape repeated down a
  shaft with a vertical fog gradient and a few amber veins. The drama is the LIGHT SHAFT, which
  is one cylinder.

**Rule of the atmosphere class: if a sheet impresses through mood, the answer is never geometry.**

## 3. The three-tier pipeline

**TIER 1 — PROCEDURAL, NOW (no Blender, no new tools).** The atlas sheets are read as *shape
grammars*, not as models. From `A1_bench_parts` we do not model eight parts; we extract the
vocabulary — cylindrical body, ring collar, port studs, mount glyph — and write one generator
that composes those primitives with parameters. Real data drives the parameters, which keeps the
honesty law: a plant's height comes from its real rate limit, its lit windows from its real load.
This is how the current foundry already works. The atlas makes the recipes better, not different.

**TIER 2 — BLENDER, FROM P5 (asset tool, not engine).** Only where a form cannot be composed from
primitives without looking cheap: the probe itself, the nexus slab, the socket pylon, the mast,
one model-vessel, one landmark. Six to ten objects, ever. Workflow: model from the round-3
orthographic turnaround sheets → keep them low-poly (these are silhouette-first designs; they do
not need density) → flat/vertex-colour materials only, no PBR texture sets (the two-ink law makes
texturing nearly free) → export `.glb` → load with three.js `GLTFLoader` → the file sits in
`game/assets/` and the engine treats it exactly like a procedural mesh.
**Blender is additive. It changes nothing about the stack.**

**TIER 3 — NEVER MODELLED.** The field, the sky, the fog, the depth bands, the light pillars,
the reflections, the dust and embers. These stay code forever. No amount of concept fidelity
changes that; they are camera and atmosphere.

## 4. Unity — the honest verdict [DECISION-LUIS, gated post-MVP per E1 §6]

**Recommendation: no, and probably never — but the reason matters more than the verdict.**

The game's defining property is that it lives *inside the entity*: served by the same local
Python process that runs LEYBER, opening instantly in a browser, reading live endpoints with no
build step. That property is not a technical convenience — it is the honesty law made
architectural. A Unity WebGL build is a 20MB+ compiled artifact with a loading bar, produced by a
toolchain that sits between the player and the truth. We would gain: better tooling, a real
editor, physics, and an easier path to a store. We would lose: instant load, the no-build-step
law, the game's residence inside the entity's own server, and months of migration.

Take Unity seriously only if we hit a wall three.js genuinely cannot climb — and after four
rounds of concept art, the wall has not appeared. Blender solves the only real gap (hero meshes),
and it solves it without touching the engine.

## 5. What to extract from each sheet (the working list)

| sheet | extract | into |
|---|---|---|
| S1 field | ring visibility, silhouette variety, light-pillar height, horizon band strength | engine.js tuning + E2 Move 1 |
| S2 entity | conduit curves as the trace language; the ringed core form | trace-wire system, nexus |
| S6 archive | vertical shaft + strata instancing + amber veins | Act II district (P3+) |
| A1/A3/A7 | the shape grammar (bodies, collars, ports, mount glyphs) | procedural generators |
| A2 vessels | the six decay states as material/emissive parameters | bestiary + rot mechanic |
| A4/B1-B4 | final SVG geometry for 29 seals + 6 doctrine plates | the map, verbatim |
| A6 panels | the plate anatomies (run plate, record strip, zone dial, carrier-lost) | bench UI, verbatim |
| B5 constructs | port/wire/packet grammar + the stat-block layout | the bench plate |
| B7 hardware | the probe's true form: octahedral core, ring drive, axial fins | Blender, first model |
| B9 the send | the four-stage ceremony staging | Act V, and the key art |

## 6. Order of work (when asset production begins)

1. Tune the atmosphere to S1 using code only — no new assets. Proves the thesis cheaply.
2. Port the 29 seals + panels from B-sheets to SVG. Pure 2D, high value, zero risk.
3. Upgrade the procedural generators with the atlas shape grammar.
4. Only then: Blender, starting with the probe (B7 PH-01), from the round-3 turnaround.

Nothing here blocks P0. The bench needs none of it.
