# E6 — THE ART PIPELINE: how the concept sheets become the running city

```
doc:          E6_ART_PIPELINE.md (THE PROBE design book — engineering/art seam)
owner:        the game team (technical-director hat)
status:       BINDING for all asset and world-geometry work · last-updated 2026-07-21
answers:      "we have 35 concept sheets and a stack that cannot load them — what is the
              actual pipeline?" — and specifically: S9_the_city_revealed is now the world
              target. How is it built, and how much of it is real?
governs:      every geometry, material and asset decision from here forward
sits under:   E5_3D_TRANSLATION (the four asset classes) · E2_VISUAL_DIRECTION (the look,
              the 12 moves, the tell lists) · E1_CODE_ARCHITECTURE (stack law, dispose
              checklist, module boundary) · A11_SIGNATURE (two-ink law, amber census)
supersedes:   E5 §3 TIER 2 (Blender as asset pipeline) — see §5. Collision named, not hidden.
marks:        [BUILT] verified on disk this date · [PLANNED] designed, binding, not in code ·
              [DECISION-LUIS] a law amendment awaiting his verdict
```

**Verification note (honesty law).** Claims marked *(verified)* were read off this machine on
2026-07-21: `three.min.js` REVISION `"128"`; `LatheGeometry`, `InstancedMesh`, `instanceColor`,
`setColorAt`, `TubeGeometry`, `CatmullRomCurve3`, `EdgesGeometry`, `MeshToonMaterial`,
`ShapeGeometry`, `ExtrudeGeometry`, `WebGLRenderTarget`, `DataTexture`, `isWebGL2` all present;
`BufferGeometryUtils` **absent** (its three occurrences are deprecation *warning strings*);
**zero loader files of any kind on disk** — GLTFLoader and SVGLoader would both be new vendored
dependencies. Role-view claims not re-verified locally are marked *(reported)*.

## 0. THE RULING, IN ONE PARAGRAPH

We adopt a **shader-and-instancing trick stack**, not an asset pipeline. Nothing is imported. The
city is built from eleven named generators and utilities (§4), all of which we write, all taking
their parameters from `/state` and `city.data.js`. The single largest visual jump available costs
**zero draw calls and zero geometry** — a procedural window-light field in the fragment shader,
bound to `rpm_now/rpm_cap`. Blender is demoted from asset tool to measuring instrument, killed by
two silent-failure blockers on the only two channels we use. Image-to-3D is rejected on
architecture, not quality. S9 is reached with roughly **10–15% real geometry**, the rest instanced
massing, points and one-time impostor cards baked from our own generated meshes — legal under a
clause written explicitly in §3.4 so it is never re-litigated.

## 1. WHAT WE ADOPT — the trick stack, ordered by leverage

Leverage = visible jump toward the sheets per keystroke. S = under half a session · M = about
one session · L = its own ticket.

| # | move | serves | effort | draw calls added |
|---|---|---|---|---|
| 1 | Procedural window field in the fragment shader | S9, S1, A3 | S–M | **0** |
| 2 | `LatheGeometry` profile vocabulary | A7 (all 7 DL forms), S9 spire | S | 0 (merged) |
| 3 | Ground shader extended to concentric plots + radial hairlines | S9, S5 | M | 0 (existing mesh) |
| 4 | `InstancedMesh` district massing + per-instance emissive | S9 | M | 1 total |
| 5 | Our own `mergeInto()` (40 lines) | everything | S | negative |
| 6 | CGA-lite shape grammar (Subdiv / Repeat / Taper) | A7, A3, A1 | M | 0 (merged) |
| 7 | Merged conduit tubes + arclength flow shader | S9, S2 | M | 1 total |
| 8 | Merged hairline edge buffer with distance-faded alpha | S9, A7 | M | 1 total |
| 9 | Far-district window lights as one `Points` cloud | S9 | S | 1 total |
| 10 | Runtime-baked 8-azimuth impostor cards | S9 far ring | M–L | 1 total |
| 11 | Analytic vertex-baked AO (INSIDE method) | S9, S1 ground contact | M | 0 |
| 12 | Palette guard in the existing final pass | every frame | S | 0 (pass exists) |

**1.1 The window field [PLANNED].** `engine.js:216` hand-places five window quads from a literal
coordinate array *(verified)* — authored, not generated, and it cannot scale to a city. Replace
with a term injected into the mass material via `onBeforeCompile`, the pattern `buildGround()`
already uses *(verified, engine.js:119)*: cell = `floor(vec2(facadeU, vWpos.y) * vec2(COLS,ROWS))`,
`lit = step(hash(cell + seed), uLoad)`, written **only** into `totalEmissiveRadiance` with
`INK.warm`/`INK.hot`. ~35 lines of GLSL, ~20 ALU per fragment on surfaces already shaded. Cheapest
*and* most honest: the lit count becomes a pure function of a live value and the amber census
stays auditable. Prior art: US Patent 10,380,790 *(reported)*.

**1.2 Lathe profiles [PLANNED].** Every one of A7's seven landmarks is a stepped plinth, tapered
shaft, ring collars and needle cap — surfaces of revolution at 6–12 facets; the S9 spire is a
fluted lathe of ~14 profile points × 12 segments ≈ 168 verts. Our engine builds everything from
`BoxGeometry` today *(verified)*, which is exactly why it reads as blocks while the sheets read as
a drafted civilisation. `lathe(profile, segments)` ~15 lines, `profileFromData(plant)` ~40.
Highest sheet-fidelity per line in this chapter.

**1.3 Ground as the city [PLANNED].** Most of what makes S9 read as a city is on the floor:
survey circles, radial hairlines, plot boundaries, plate seams. `buildGround()` already does the
ring trick (`mod(length(vWpos.xz - uNexus), 22.0)`) *(verified)*; generalising to N district
anchors costs an array uniform and no new geometry. Do it before a single tower.

**1.4 Instanced massing [PLANNED].** `unitMassGeometry()` is `BoxGeometry(1,1,1,1,4,1)` = 48 verts
/ 36 tris *(verified by counting the segment planes)*; 2,000 instances = 72k tris in one draw call.
**Two gotchas, named now:** (a) `instanceColor` multiplies the **diffuse** term only, never
emissive — per-instance lit windows need an `InstancedBufferAttribute` plus `onBeforeCompile`
(~30 lines; do **not** vendor Troika for it); (b) an `InstancedMesh` is frustum-culled as one
object by its bounding sphere, so a city-spanning instance mesh is never culled — at 72k tris that
is correct, do not add per-instance culling.

**1.5 Our own merger + 1.6 CGA-lite [PLANNED].** `BufferGeometryUtils` is not in the build
*(verified)* and vendoring a ninth file to concatenate `Float32Array`s is not a trade worth making
here: `mergeInto(geoms, matrices)` over position/normal/color/index is ~40 lines, written once,
used for landmarks, conduits, rims and eventually the probe. On top of it, A7's shape grammar —
three operators from Müller et al., *Procedural Modeling of Buildings*, SIGGRAPH 2006 (`Subdiv`,
`Repeat`, `Taper`) plus a terminal emitter over a scope object, ~150 lines. **Each landmark's
grammar output is baked into ONE merged geometry at build time**, or the grammar reintroduces the
draw-call problem it exists to solve.

**1.7–1.9 Conduits, edges, points [PLANNED].** Conduits: `TubeGeometry` over
`QuadraticBezierCurve3`, 32×5 segments ≈ 320 tris each, forty merged into one mesh, `uv.x` read as
arclength for the flow term. Edges: one merged buffer of `EdgesGeometry` with per-vertex alpha
driven by camera distance — Sable's exact trick, and what makes impostor and LOD swaps invisible,
so it ships **before** the impostors. Points: one `Points` object holding every far-district lit
window, per-point colour from live `rpm_now` — at distance a lit city reads as a field of bright
points against dark mass, the cheapest large win here and literally a data visualisation.

**1.10 Impostors [PLANNED, constrained].** Bake each far district's real mesh into an 8-cell
azimuth strip in one shared 2048px `WebGLRenderTarget` at world-generation. Full octahedral atlases
(Brucks/Epic) are overkill at a broadly fixed elevation; the documented browser failure mode is
*continuous per-frame re-baking*, while a one-time bake is a few extra `render()` calls at load
*(reported)*. The §3.4 constraints are binding.

**1.11 Analytic vertex AO [PLANNED].** INSIDE's method (GDC 2016), not a DCC bake: accumulate
per-vertex darkening from *analytic* occluders (plate proximity, neighbour volumes) at generation
time into the colour attribute, free at render. ~40 lines, and the fix for the "boxes floating on
a plane" read.

**1.12 The palette guard [PLANNED] + the tone-map question [DECISION-LUIS].** The Technical
Artist's diagnosis is correct: ACES desaturates amber toward cream-white in every bloom core —
degrading the "amber = alive" signal exactly where it matters most — and lifts the toe on the
near-black void. His prescription, delete `ACESFilmicToneMapping`, is **overruled as a unilateral
change** on evidence: `engine.js` deliberately inlines the ACES curve inside the sky
`ShaderMaterial` so sky and fogged ground pass the *same* curve *(verified, engine.js:68–80)* —
removing the renderer's tone map without the sky seams the horizon, and E2 §6 makes hardware the
judge of brightness moves. **Adopted now:** two terms in the *existing* `FinalShader` (already
LinearToSRGB + sub-1/255 dither, *verified*) that (a) reassert amber chroma in clipped highlights
and (b) re-seat the void floor — corrections to a camera-curve artifact, not a new look, so both
sit in the colour-management class the sRGB tail already occupies (A11 §4.5). **To Luis:** full
ACES removal as an on-hardware A/B pair with the sky-shader edit costed in. A three-stop LUT remap
of the frame is *rejected*: it authors the look in post and makes material colour unfalsifiable.

## 2. WHAT WE REJECT — named, with the reason

**2.1–2.2 Image-to-3D generation — Meshy 6, Tripo 3.x, Rodin/Hyper3D, CSM Cube, TRELLIS.2, and
the AI-remesh layer sold beside them. REJECT.**
Architecture first: a GLB is a frozen artifact. It cannot grow a district, fire a plant, or answer
an endpoint. It breaks the honesty law at import time, before quality is discussed. The quality
kill is second and counter-intuitive: the only vendor-independent evaluation, **3D Arena (arXiv
2506.18787; 123,243 votes, 8,096 users, 19 models)**, finds textured models carry a **+144.1 ELO**
advantage and splats +16.6 over meshes, with the authors stating that voting "systematically
favours visual impact through vibrant rendering and aesthetic appeal over downstream utility"
*(reported)*. We would pay for the category's strongest output (texture) in order to delete it,
and keep its documented weakest output (hard-surface topology) as our only deliverable. Third: our
subjects are octahedra, cylinders, concentric plates and stepped plinths — **there is nothing to
reconstruct.** For hard-surface low-poly on a two-ink flat-shaded budget, image-to-3D is not worth
it. Say it plainly and stop revisiting it. **AI quad-remesh / auto-retopology goes with it** — a
fix for dense irregular meshes, and our geometry is born at the polycount we typed.

**2.3 AI texture / material generation. REJECT.** Every channel it produces (normal, roughness,
metallic, detailed albedo) is discarded by a flat matte vertex-coloured look; we may not even have
UVs. **One correction to the ban:** "no textures" must not become "no texture samplers." Two
texture objects are code-generated and therefore legal — a 1D ramp `DataTexture` for a hard toon
step, and later an MSDF atlas if instrument type goes into 3D. We already generate `CanvasTexture`
ramps for the road strips *(verified, engine.js:175–182)*.

**2.4 SVGLoader + vtracer for the seals. REJECT — overruling the Tooling Scout**, who called this
"the single highest-value external artefact in the scan." It is already built, and better:
`seals.js` is 634 lines generating all 29 element seals plus the three map-glyph states from the
six-shape grammar, deterministically (FNV-1a over the element id seeds an LCG; no `Math.random` in
the file), captioned with the real proof string read from `window.AEA` *(verified)*. Tracing a
raster of a generated image to recover vector paths we already own as code is a lossy round trip
that also loses the live binding. Zero new vendored files. Closed.

**2.5 Blender Geometry Nodes → glTF. REJECT outright.** Self-defeating: the exporter cannot read a
Geometry Nodes modifier without `Realize Instances`, which collapses the proceduralism into a
baked mesh — precisely the artifact the law forbids (glTF-Blender-IO #1537, #2474) *(reported)*.

**2.6 CC0 asset libraries — Kenney, Quaternius, Poly Haven. REJECT on aesthetics.** Licensing is
flawless and beside the point: Kenney/Quaternius are warm saturated toy low-poly, Poly Haven is
photoreal PBR/HDRI — the exact category E2 bans. The one thing worth stealing is not an asset but
the **single global snap-grid and consistent unit scale** that makes a kit read as a designed
city. Adopted in §3.2 as the plot module.

**2.7 Inverted-hull outlines and `OutlinePass`. REJECT.** Inverted hull doubles draw calls for a
*silhouette* outline; our `EdgesGeometry` gives *structural* edges, which is what a blueprint is.
`OutlinePass` is a selection-highlight tool, not a scene stylisation tool.

**2.8 L-system / Parish-Müller street routing. REJECT.** It invents a plausible network; our
conduits must **be** the real topology (§4.4).

**2.9 gltfpack / meshopt / Draco. NOT REJECTED — BANKED.** r128's `GLTFLoader` does support
`EXT_meshopt_compression`, Draco and `KHR_mesh_quantization` *(reported)* — recorded because it
removes an excuse. We are not shipping meshes, so it is banked, not scheduled.

## 3. THE DISTRICT LAYOUT DECISION — S9 as the world target

### 3.1 What S9 actually is
One lit spire on a stepped concentric plinth. Around it ~10 district plots on circular stepped
platforms at varying radii; amber conduits spire-to-district and district-to-district, thinning as
they go, with bright junction nodes; a sunken ring pit (the archive, S6); a wheel/mirror (DL-13);
a far horizon band of pure silhouette plus points. And — the detail that makes the image honest —
**empty plots: surveyed rings with nothing standing on them.**

### 3.2 The binding: plots are plants, emptiness is truth [PLANNED]
`city.data.js` holds 15 plants with `zone` (residential 7 / industrial 6 / outskirts 2), `privacy`,
`online`, `rpm`, `rpd`, `models`; `/state.energy.plants[]` lists **only online plants**
(`controlroom.py:92`, `if not online: continue`) *(both verified)*.

- **Ring radius ← `zone`.** Residential inner, industrial mid, outskirts outer. Not invented: the
  zone field is the privacy geography the game already teaches.
- **A plot exists for every plant in the registry; it is *built* only if its plant appears in
  `/state.energy.plants[]`.** Offline plant = survey rings, plate seams, rim, nothing else. The
  empty plots in S9 are therefore not composition — they are the literal set of organs that are
  proven-not-wired, which is the game's named antagonist (A12: the antagonist is FOG).
- **Snap-grid law (Kenney's discipline, §2.6):** one plot module unit; every plate, rim and
  conduit elbow snaps to it, elbows to 45-degree increments. This is what makes concentric plots
  read as a designed city rather than scattered boxes.

### 3.3 The ring budget — how much is modelled
Firewatch's principle makes this invisible: distant objects collapse to flat colour with clean
silhouettes under a distance-driven ramp, at which point a card and a mesh are
pixel-indistinguishable; Sable fades outline opacity with distance for the same reason. Our fog
already band-separates *(E2 §4.1, BUILT)*.

| ring | contents | treatment | share |
|---|---|---|---|
| 0 | occupied district + the spire | real geometry, real edges, live window field | ~10–15% |
| 1 | 2–3 adjacent districts | instanced massing, no interior detail, merged edges | ~25% |
| 2 | remaining 6–7 districts | 8-azimuth impostor card + `Points` window cloud | ~45% |
| 3 | horizon band, far city | shader sky + one generated silhouette band, no geometry | ~15% |

### 3.4 THE IMPOSTOR CLAUSE — written into law now [PLANNED, binding]
A baked card is **not** a fake: it is a render of geometry this engine generated from live data.
The honesty law forbids *invented* content; it does not require every pixel to be re-rasterised
from triangles each frame. That distinction holds only under three hard constraints:

1. **An impostor carries structure ink only** — mass and silhouette. **Amber is never baked.**
   Far-district lights are the live `Points` cloud (§1.9) on the `refreshPlantLights` poll. A
   stale card showing lit windows for a plant that went offline is a lie; this makes that state
   unreachable by construction.
2. **A card is invalidated by its district's data changing** — online/offline, throttle state,
   model count. Invalidated means re-baked or dropped to the unlit mesh, never left standing.
3. **Every impostor is registered in the resource registry `R`** (E1 §3.1) — render target,
   material and geometry owned and disposed. A bake path that leaks GPU textures is the LUMEN
   lesson repeating in r128.

### 3.5 The S9 collision — persistent amber conduits are currently illegal [DECISION-LUIS]
S9's dominant read is **amber conduits everywhere, at rest**. A11 §4.1's closed list of legal
idle amber contains: probe · beacon · windows-tracking-load · discovered nodes · presence chip ·
HUD values · sky band. **It does not contain roads or conduits**, and E2 Move 7 ruled explicitly
that idle wires are structure ink only, amber appearing solely under a real trace and its
600–900ms decay. **Therefore S9 as drawn cannot ship under current law.** This is named, not
worked around. Two honest paths:

- **(a) Ship as ruled.** Conduits idle in structure ink; the S9 amber network appears only as
  traffic flows through it. The city is dark and lights up when the entity works. Defensible,
  arguably *better* — it makes the sheet's beauty a reward rather than wallpaper.
- **(b) Amend A11 §4.1** to add conduits to the closed list, with the intensity bound to a named
  real value: per-link cumulative routed calls from `events.jsonl` / the tracelog, log-scaled and
  capped. Then S9 is legal and still true.

The §4.4 generator is written so both are one uniform apart. Luis rules; nothing is built against
(b) until he does.

## 4. THE ALGORITHM SET — every generator, and the live value it reads

**No generator may take a parameter that is not a real field.** E2 Move 3's recorded failure — a
fabricated `tier` field — is the pattern prevented; every field below was read from
`controlroom.py:77–129` and `city.data.js` *(verified)*. Determinism follows `seals.js`: FNV-1a
over the plant id seeds an LCG, no `Math.random` in any generator.

| # | generator | parameters ← live source | fallback when the value is absent |
|---|---|---|---|
| 1 | `plotRing(plant)` — the district plinth (lathe, 3–4 steps, 64 seg) | outer radius ← `zone` band + `models` count · step count ← `privacy` rank (local/no-train/trains/none) | registry-only plant → rim + survey rings, no plinth |
| 2 | `massing(plant, seed)` — CGA-lite towers | tower count ← `models` · tower height ← `rpm_cap` · footprint ← `rpd_cap` · setback ← `privacy` | `rpm_cap` null (uncapped, e.g. ollama) → height from the plant's own `rods[].calls` share, **labelled uncapped in the panel, never a fake ceiling** |
| 3 | `windowField(instance)` — fragment-shader lights | lit fraction ← `rpm_now / rpm_cap` | uncapped plant → **literal count**: one window per request in the last 60s, no denominator invented |
| 4 | `conduits(graph)` — MST + merged tubes | topology ← the real provider/zone graph · per-link brightness ← routed calls from `events.jsonl` · live pulse ← an in-flight trace | no traffic → structure ink only (§3.5 path (a)) |
| 5 | `spire(state)` — the centre (fluted lathe) | height ← REGISTERED rows in `modules.json` vs total · flute count lit ← `/state.trust[*].level > 0` · beam ← `life.alive_since` uptime | pre-registry → the shaft, unlit |
| 6 | `emptyPlot(plant)` — the unbuilt organ | presence ← in registry, absent from `/state.energy.plants[]` | — (this **is** the fallback state) |
| 7 | `lightPoints(plants)` — far window cloud | per-point colour/count ← `rpm_now` per district | offline → points absent, not dimmed |
| 8 | `impostorBake(district)` — 8-azimuth strip | geometry ← the generated district mesh, structure ink only | invalidated on data change (§3.4) |
| 9 | `edgeBuffer(meshes)` — merged hairlines | per-vertex alpha ← camera distance | — |
| 10 | `mergeInto(geoms, matrices)` — our merger | — (pure geometry utility) | — |
| 11 | `vertexAO(mesh, occluders)` — analytic AO | — (pure geometry utility, INSIDE method) | — |

**4.4 conduit routing.** Radial minimum spanning tree (Prim's, ~30 lines) over the district
centres of the **real** provider/zone graph, elbows snapped to 45 degrees for the sheet's
orthogonal-diagonal ductwork. Strictly better than a generative street grammar: cheaper,
deterministic, and a new provider coming online visibly **rewires the city**.

**4.12 The panel obligation.** Every generator reading a live value owes a readout: the district's
instrument panel prints the number the geometry was built from. A tower whose height cannot be
traced back to a printed number is decoration — the thing this chapter exists to refuse.

## 5. BLENDER'S EXACT ROLE — and why E5 §3 TIER 2 is amended

**Collision named.** E5 §3 ruled: Blender for 6–10 hero meshes, exported `.glb`, loaded with
`GLTFLoader`. **This chapter overrules that**, on two blockers unknown when E5 was written — both
*silent* failures, on the only two channels our art direction uses:

1. **r128's `GLTFLoader` has zero support for `KHR_materials_emissive_strength`** — the extension
   was ratified after r128 shipped (2021-04-23), and unknown extensions are silently ignored
   *(reported: grep of the r128 source returns 0 hits)*. Any Blender-authored emission above 1.0
   arrives **dead**, clamped to 1.0, while our whole aesthetic hangs on amber overdriving
   `UnrealBloomPass`. The glow must be re-set as `material.emissiveIntensity` in JS anyway — at
   which point the authoring round trip bought nothing.
2. **Blender 4.1+ silently stops exporting vertex colours (`COLOR_0`)** unless they are wired
   into the material node tree (Blender #123925, #118563) *(reported)*. Vertex colours **are** our
   material model *(verified: `unitMassGeometry()` authors them by hand, engine.js:162–173)*.
   Geometry arrives; colour is just gone.

Two silent colour failures on our only two channels, in a workflow judged by screenshots in short
sessions. That retires "author the look in Blender."

**The precedent is on disk.** The probe — E5's named *first* Blender model (B7 PH-01) — was built
as primitives instead, and the code says why: *"the design language was extracted straight into
geometry… a drawing between concept and code buys nothing when the modeller is us"* *(verified,
engine.js:263–268)*. It shipped. The lathe + grammar work in §1 is what E5 reached for when it
wrote "genuinely modelled."

**Blender's role, ruled [PLANNED]: a measuring instrument, not a pipeline.** Block out a landmark
or the spire, read off real proportions, angles, setbacks and step ratios, type those numbers into
`profileFromData`, delete the `.blend`. No export, no loader, no ninth vendored file, no `.glb` in
`game/assets/`. If a form ever defeats the grammar the decision reopens here, blockers priced in.

## 6. THE ORDER OF WORK — numbered, each fitting one session

Each step ends screenshot-verified (E2 §6: hardware judges brightness, headless gates composition)
**with `renderer.info.render.calls` recorded in the 09 ledger line.**

1. **Instrument first. S.** `renderer.info.render.{calls,triangles}` into the debug readout and
   the `?still` output. No step below ships without its number.
2. **`mergeInto()` + `lathe()` + the profile library. S.** Pure utilities, no visual change,
   unlocks everything after them.
3. **The ground becomes the city. M.** Extend the `buildGround` injection to N district anchors:
   plots, radial hairlines, plate seams, snap-grid. Towers wait — this is the composition.
4. **Instanced massing + CGA-lite grammar. M.** One `InstancedMesh`, seeded per plant from real
   fields (§4 rows 1–2).
5. **The window field. S–M.** Lights bound to `rpm_now/rpm_cap`; delete the hand-placed quad
   array in the same session. Zero draw calls, biggest single jump toward S9.
6. **The edge buffer with distance fade. M.** Ships *before* the impostors — it hides their swap.
7. **Conduits. M.** MST over the real graph, merged tubes, arclength flow, structure-ink idle
   (§3.5 path (a) until Luis rules).
8. **Far ring: the `Points` cloud, then the impostor bake. M–L.** Split if the bake harness runs
   long; the points alone are a legitimate stopping point.
9. **The spire. M.** Lathe + trust-bound flutes + uptime beam. The frame's subject.
10. **The palette guard. S.** Plus the ACES A/B pair prepared for Luis.
11. **Analytic vertex AO. M.** The ground-contact weight that stops primitives floating.
12. **The archive pit and the mirror. M.** S6 and DL-13, both lathe composites.

Steps 1–5 alone reach most of the S9 read. Nothing here blocks P0; the ladder starts when
world-geometry work starts and interleaves with E2's move list rather than replacing it.

## 7. THE PERFORMANCE BUDGET — binding

Published browser budgets converge on under 100 draw calls for desktop 60fps; a call costs
~50–200µs of CPU, so 100 calls can consume 20ms and blow a 16.6ms frame before a shader runs
*(reported)*. Our frame today is **~45–55 geometry draw calls by inspection** of
`buildWorld`/`buildProbe` *(read from the file, not yet instrumented — that is step 1)*.

| bucket | budget | notes |
|---|---|---|
| sky dome | 1 | built |
| ground (plots, rings, hairlines, seams) | 1 | all in the existing shader |
| district massing (rings 0–1) | 1 | `InstancedMesh`, ≤ 2,500 instances |
| merged hairline edges | 1 | one buffer, per-vertex alpha |
| merged conduits | 1 | ≤ 40 runs |
| merged plot rims | 1 | lathes |
| landmark composites | ≤ 7 | one merged geometry each, ring 0 only |
| impostor batch (ring 2) | 1 | shared 2048px atlas |
| far window `Points` | 1 | ≤ 6,000 points |
| dust / embers / trail / stars | 4 | built: 800 / 180 / 90 / 1,200 |
| probe | ≤ 10 now, 3 after merge | built |
| **geometry total** | **≤ 30 warn · 40 hard ceiling** | a step that crosses 40 does not ship |
| post chain | fixed | RenderPass + bloom mip chain + FXAA/final — already paid, bloom locked |
| triangles | ≤ 250k | 2,000 instances × 36 = 72k; landmarks ≤ 40k; the rest is fog |
| instances | ≤ 2,500 masses | one bucket |
| points | ≤ 8,300 across 5 clouds | far windows ≤ 6,000 |
| textures / render targets | ≤ 12 / 1 | all code-generated; the impostor RT registered in `R` |
| **target** | **60fps at 1440×900 on Luis's hardware** | swiftshader/headless is never the judge (A4 §8) |

**Instrumentation law.** The draw-call count is printed behind the debug key and recorded per
step. If the number is not in the ledger line, the step did not ship.

## 8. GOVERNANCE

This chapter owns the pipeline; E2 owns the look; E1 owns the stack; A11 owns identity. On
conflict, resolve upward. Two-ink and honesty laws are absolute here as everywhere: no generator
invents a parameter, no impostor bakes amber, no asset is imported.

**Open `[DECISION-LUIS]`, both blocked until he rules:**
1. **§3.5 — conduit idle amber.** Ship dark-until-traffic (path a), or amend A11 §4.1 with a named
   per-link binding (path b). S9 as drawn requires (b).
2. **§1.12 — the ACES question.** Keep the tone curve plus the narrow palette guard, or remove
   ACES and re-tune the sky shader with it. Needs an on-hardware A/B pair per A4 §8.2.

**Amendment recorded:** E5 §3 TIER 2 (Blender → `.glb` → `GLTFLoader`) is superseded by §5. E5's
asset-class table stands otherwise; only the tool for the hero-mesh class changed, and it changed
toward code — the direction every other class already runs.

## Changelog

- 2026-07-21 — v1. Technical-director synthesis of three role-view research passes (technical
  artist / procedural engineer / tooling scout), checked against a read of `three.min.js` (r128
  confirmed), `game/js/engine.js`, `game/js/seals.js`, `game/index.html`, `city.data.js`,
  `controlroom.py:77–129` and `modules.json` this date. Role-views overturned: ACES removal
  demoted to `[DECISION-LUIS]` with the narrow palette guard adopted instead; SVGLoader + vtracer
  rejected because `seals.js` already generates all 29 seals deterministically and live-bound.
  Chapter overturned: E5 §3 TIER 2 — Blender demoted to a measuring instrument on two silent glTF
  blockers. New law: the impostor clause (§3.4) and the S9 amber-conduit collision (§3.5).
