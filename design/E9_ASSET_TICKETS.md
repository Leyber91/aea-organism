# E9 — THE ASSET TICKET REGISTRY: one ticket per buildable thing

```
doc:          E9_ASSET_TICKETS.md (THE PROBE design book — production chapter E9, ASSETS)
owner:        the game team (asset-producer hat)
status:       BINDING for all asset work · last-updated 2026-07-21
origin:       Luis, 2026-07-21 — "a considerable amount of well detailed tickets, where the
              style reference is defined, where the techniques to be used to represent with
              full fidelity what we want to achieve, each object at once, won't stop until
              it is a replica."
answers:      what, exactly, is left to build — as a list a builder can work down without
              asking a question, with the sheet, the technique, the binding and the gate
              named per object.
sits under:   E8_FIDELITY_LAW (the gates G-1..G-7 and the DONE definition — this chapter
              authors no gate, it only names which clause each object is judged on) ·
              E6_ART_PIPELINE (the trick stack and the generator set — this chapter authors
              no technique that E6 has not sanctioned) · E2_VISUAL_DIRECTION (the look, the
              twelve moves) · E1_CODE_ARCHITECTURE (module law, dispose checklist) ·
              A11_SIGNATURE (two-ink identity, the amber census)
governs:      nothing above itself. On conflict the cited chapter wins.
registry:     ids A-001..A-107. Engine deltas live in INDEX §3 / tickets.json as T-001..T-082
              and are NOT duplicated here; where an asset needs an engine delta it DEPENDS ON
              the T-id. A-ids and T-ids never collide and never merge.
laws:         two-ink absolute (void #050a10-#0a1420 · structure rgba(120,155,175) at exactly
              .70/.45/.28/.14/.08 · amber #ffb000 hot / #d4a24c warm, only where alive) ·
              honesty law absolute (no faked data, no invented numbers) · render doctrine
              three classes (SOLID / HOLOGRAM / FLAT-UI) · NO emoji ·
              marks [BUILT] / [PLANNED] / [DECISION-LUIS]
```

---

## 0. HOW TO READ A TICKET

Every ticket carries exactly ten fields. Nine are on the page; the tenth (**NAME**) is the
header.

| field | meaning |
|---|---|
| **ID** | `A-nnn`. Stable forever. Never reused, never renumbered. |
| **NAME** | the object's designation + plain name, as the sheet presses it (`PH-01 / A11-CORE PROBE`). |
| **CLASS** | `SOLID` \| `HOLOGRAM` \| `FLAT-UI` \| `EFFECT` \| `INTERACTION`. Decided by the render doctrine, never by the sheet's drawing style (E8 §5.5). |
| **STYLE REFERENCE** | the exact sheet filename in `design/concepts/` **and which panel of it**. Where a pixel cut exists in `game/ref/` it is named too — that cut, never a memory of the sheet, is the target the replica is judged beside in `lab.html`. |
| **AEA CONCEPT SERVED** | the element or law from `aea_elements.js` this object embodies, by id. An object that serves no element is decoration and does not get a ticket. |
| **TECHNIQUE** | the concrete r128 / DOM / SVG method: geometry primitives, material, shader trick, blending mode. Nothing here may exceed E6's sanctioned trick stack. |
| **LIVE DATA BINDING** | the real endpoint or state field that drives it — or `NONE` **with a reason**. The honesty law: an object with no live value must say so out loud, and may then carry no number that pretends to be one. |
| **FIDELITY GATE** | the specific pass condition for THIS object, stated against E8 §3's checklist (G-1 silhouette · G-2 palette · G-3 amber census · G-4 line weight · G-5 density · G-6 legibility at delivered size · G-7 the stranger test). All seven always apply; the ticket names the one or two that will actually fail and what "pass" means here. |
| **SIZE** | `S` under half a session · `M` about one session · `L` multi-session (INDEX §3.0 convention, unchanged). |
| **DEPENDS ON** | A-ids and T-ids. Empty means buildable now. |

**Conventions inherited from INDEX §3.0 and E8.** A ticket closes only against code on disk
plus a `verdict:"DONE"` line in `design/fidelity_ledger.jsonl` — no ledger line, no done. An
object that must ship unfinished ships `HELD` with the open gap written down. Marks are
`[BUILT]` (verified on disk 2026-07-21), `[PLANNED]`, `[DECISION-LUIS]`.

**Sanctioned technique vocabulary** (E6 §1, and nothing outside it): `BoxGeometry` ·
`CylinderGeometry` · `TorusGeometry` · `LatheGeometry` · `ExtrudeGeometry` · `ShapeGeometry` ·
`IcosahedronGeometry` · `OctahedronGeometry` · `TubeGeometry` over `QuadraticBezierCurve3` /
`CatmullRomCurve3` · `EdgesGeometry` + `LineSegments` · `InstancedMesh` + `InstancedBufferAttribute`
· `Points` · `CanvasTexture` (`NearestFilter`, `RepeatWrapping`) · `DataTexture` ·
`WebGLRenderTarget` (impostor bake only, §3.4 clause) · vertex colours · `onBeforeCompile`
injection · `MeshStandardMaterial` / `MeshBasicMaterial` / `MeshToonMaterial` ·
`AdditiveBlending` (hologram and light-transport only, never on a SOLID surface) · our own
`mergeInto()` · `lathe()` · `vertexAO()`. **No loaders, no `.glb`, no imported asset, ever**
(E6 §5 supersedes E5 §3 TIER 2).

---

## 1. THE BUILD ORDER — why the registry runs in this sequence

Ordered by **build value = fidelity gained per session, gated by what unblocks what**.

1. **SOLID first**, because E8's hardest clause is E-7 (solid reads solid) and every scene
   ticket downstream is composed of solids. Inside SOLID: the probe (the object the player
   looks at for the whole game, E8 §6.1), then the bench parts (P0's subject), then the things
   the player collects, then the things the player flies past.
2. **HOLOGRAM second**, because it is small, it is three objects, and it is the class most
   likely to be violated by accident — a hologram that creeps onto a solid is a doctrine
   failure, not a taste one.
3. **FLAT-UI third**, because ~40% of the output is already final art (E5 §1) and most of it is
   `[BUILT]`: these tickets are largely fidelity closeouts against C4 / B1 / B2 / B3, which is
   cheap work with a high pass rate and it teaches the gate loop before the loop is spent on
   geometry.
4. **EFFECT fourth**, because effects are meaningless until there is something to light, and
   because the amber laws (A-087, A-088) constrain every ticket above them — they are written
   fourth and obeyed first.
5. **INTERACTION last**, because an interaction is the seam between an asset and a mechanic;
   it cannot be gated until both exist.

**Where a whole class is blocked** the registry says so in the ticket rather than reordering
around it.

---

## 2. CLASS: SOLID — what the entity IS

Doctrine: these have weight and material. They may **never** be holograms, however wireframe
the plate looks (E8 §5.5). E-7 is the binding essence clause for every ticket in this section:
facet value separation, cut lines, an edge that responds — never a wireframe, never a glow.

### 2.1 THE PROBE AND ITS HARDWARE — A-001 … A-007

The player's own body. Judged hardest, first (E8 §6.1). `B7_probe_hardware.png` is a 7-cell
atlas, cells numbered 1..7 with codes PH-01..PH-07, each with named callouts and a mount glyph
beneath. The mount glyph vocabulary is printed on the sheet: triangle = primary · diamond =
secondary · circle = ring · square = interface · pentagon = support · hexagon = link.

---

**A-001 · PH-01 / A11-CORE PROBE** — `SOLID` · `L` · `[BUILT]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 1 (PH-01, three-quarter view; callouts
  AXIAL FIN (x4), POWER NODE, RING DRIVE GIMBAL, CORE INTERFACE, ALIGNMENT MARK; mount glyph =
  ring) · `R3_01_probe_turnaround.png` (front/side/top ortho + dimension marks) ·
  `S3_the_probe.png` (the in-world read: 97.6% void, one 0.4%-of-frame object).
- **AEA CONCEPT SERVED** — the operator's presence inside the entity; `verb.observe` (the state
  is visible because something is there to see it). The ring drive is the concentric motif
  worn as a body (E8 E-8).
- **TECHNIQUE** — `OctahedronGeometry(r, 0)` hull, detail 0 so the eight faces stay flat and
  faceted; per-face vertex colours authored as a vertical value ramp (E2 Move 2) so facets
  separate without a light. Four axial fins = thin `BoxGeometry` wedges merged into the hull
  via `mergeInto()`. Ring drive = `TorusGeometry(R, 0.02, 6, 48)` segmented into 12 arc blocks
  with darker divisions between them (the sheet's segmented ring), material
  `MeshStandardMaterial` with `emissive` = `INK.warm`, `emissiveIntensity` on the `EMISSIVE`
  tier table (idle 0.35 / fired 1.0). Cut lines = `EdgesGeometry` on the hull merged into the
  shared hairline buffer, **not** a second wireframe object. Two engraved glyph plates =
  shallow inset boxes carrying the six-glyph grammar. Target ≤ 3 draw calls after merge
  (E6 §7 probe bucket).
- **LIVE DATA BINDING** — ring-drive emissive tier ← the probe's own live state (idle vs a run
  in flight from `/api/construct/run`); hull carries no number. **Reason it binds so little:**
  the probe is the player, and the player is not a measurement.
- **FIDELITY GATE** — **G-1 is the binding gate**: flat-black silhouette against
  `game/ref/`-cut of B7 cell 1 must show four fins, the gimbal ring and the base alignment
  mark, at the play camera (20 m behind / 6 m above / 60° FOV), not only at the sheet camera.
  **G-7** substitution question is literally E8's example: "point to the ring drive gimbal."
  **G-2**: the one pixel > 0.95 in the whole frame is allowed to be the gimbal's hot segment.
- **DEPENDS ON** — T-066 (EMISSIVE-TUNE; the core currently blooms to a white blob on real GPU).

---

**A-002 · PH-02 / SCAN LENS** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 2 (LENS ARRAY TIER-02, SENSOR RING
  CONCENTRIC, MOUNT POINT triangle; the face is a concentric target with four radial index
  ticks).
- **AEA CONCEPT SERVED** — `verb.observe` · `seed.7` CEILING-DETECT (a scan is how the probe
  learns it has hit an edge).
- **TECHNIQUE** — stacked `CylinderGeometry` barrels (3 steps, 12 radial segments) inside an
  octagonal `LatheGeometry` shroud; the lens face is a flat disc carrying the concentric field
  as **double-line rims** (two hairlines with a gap — E8 E-7's named cheapest move), drawn into
  a 256px `CanvasTexture` with `NearestFilter`, never as geometry. One amber index tick on the
  outermost ring, `emissiveIntensity` at idle tier.
- **LIVE DATA BINDING** — the lens is dark unless a scan is running; while running, the amber
  index tick sweeps to the bearing of the scanned object (A-089). No readout on the module
  itself — the numbers land in the HUD (A-079).
- **FIDELITY GATE** — **G-4**: the concentric face must hold ≥76% of its strokes at ≤2px
  normalised to a 1024 short side; a lens drawn with fat rings is the "2003 menu" failure
  quantified. **G-6**: at the module's delivered size (a ~40px mount on the probe at play
  distance) the rings must still separate — if they merge, cut rings, do not thin them further.
- **DEPENDS ON** — A-001, A-089.

---

**A-003 · PH-03 / ARCHIVE LINK** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 3 (DOCK COUPLER HEX INTERFACE, TRACE
  CONDUIT + SOCKET, DATA TETHER CHANNEL; mount glyph = link/hex).
- **AEA CONCEPT SERVED** — `seed.10` BACKWARDS CHANNEL (run A writes a capsule, run B
  reconstitutes it) · `axis.A` ABSTRACTION.
- **TECHNIQUE** — a chamfered `BoxGeometry` body with an inset hexagonal coupler (`ExtrudeGeometry`
  from a 6-gon `Shape`, bevel 0.004) and a recessed circular socket bored as a short inverted
  cylinder. The tether channel is a **cut line**, not a drawn line: two parallel inset boxes
  0.006 deep so the edge catches. Vertex-colour ramp darkens the recess floor.
- **LIVE DATA BINDING** — coupler seats warm only while a real recall is in flight
  (`memory.py` recall through `/talk` or `/api/node/run`); otherwise structure ink.
  **The socket is never lit "ready"** — readiness is not a measurement.
- **FIDELITY GATE** — **G-7**: "point to the dock coupler." If a stranger points at the socket
  instead, the hex is not reading and the fix is the coupler's proportion, not its shading.
- **DEPENDS ON** — A-001.

---

**A-004 · PH-04 / TRACE RECORDER** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 4 (TRACE INLET PORT triangle, RIBBON SPOOL
  CAPACITY 01, TRACE WINDOW, INDEX MARK diamond).
- **AEA CONCEPT SERVED** — `verb.propagate` (the honesty node: live trace of task → node →
  output) · `pr.time` OPERATOR-OBSERVABLE TIME.
- **TECHNIQUE** — slab `BoxGeometry` body; the spool is a `TorusGeometry` of 24 tight coils
  approximated as one lathed cylinder with a coil-groove `CanvasTexture` ramp (grooves are
  value, not geometry); the trace window is a glass-cased inset — a thin
  `MeshStandardMaterial` shell at `transparent:true, opacity:0.18`, `depthWrite:false`, over
  a dark interior, which is the sanctioned "glass-cased artifact" treatment (bundle_02 §6).
  The ribbon inside is the **only** amber, one thin band.
- **LIVE DATA BINDING** — spool fill fraction ← count of trace rows written for the current
  run (`tracelog.py` JSONL / the `/api/construct/run` row). When no run exists, the window is
  empty and the module prints nothing — an empty spool is the honest idle.
- **FIDELITY GATE** — **G-5**: the module carries designation + class glyph + ≥3 measured facts
  or it is a shape (E8 E-3). Its three facts are rows-captured, run id, and elapsed — all
  real. **G-2**: the glass must not introduce a third hue; a bluish glass tint is the classic
  leak and G-2's 0.10% ceiling catches it.
- **DEPENDS ON** — A-001, T-002 (trace-wire), A-086.

---

**A-005 · PH-05 / COMPANION CRADLE** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 5 (CRADLE ARCS (x4), ALIGNMENT PENTAD,
  SEED NEST SOCKET, LATCH POINT diamond) — the seated cone in the middle is the vessel stand-in.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE (the probe physically carries one model-vessel) ·
  `doc.solo` THE SOLO LAW (one good model, carried).
- **TECHNIQUE** — four `BoxGeometry` arcs swept by rotation about Y at 90° (built once, cloned
  by matrix into `mergeInto()`); the pentad alignment plate is a 5-gon `ShapeGeometry` inlay;
  the nest is a short cone socket. The cradle is empty geometry by default — a mount, not a
  container — and the seated rod is A-016's mesh parented in.
- **LIVE DATA BINDING** — occupancy ← whether a specimen is actually carried in
  `journey_save.json`; the seated rod's own decay state drives its material (A-093). Empty
  cradle = empty geometry, never a ghost outline.
- **FIDELITY GATE** — **G-1**: four arcs must count as four in flat-black silhouette; a cradle
  that reads as a bowl has failed proportion. **G-3**: the cradle itself carries **zero** amber
  — all amber in this cell belongs to whatever is seated.
- **DEPENDS ON** — A-001, A-016.

---

**A-006 · PH-06 / FIELD ANCHOR** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 6 (FIELD INTERFACE SOCKET, AUTH CHANNEL
  PASS-THRU, POWER BRIDGE CONNECT; mount glyph = ring).
- **AEA CONCEPT SERVED** — `seed.9` BOUNDARY (the auth channel is the sacred wall in hardware
  form) · `seed.1` SUBSTRATE.
- **TECHNIQUE** — faceted `IcosahedronGeometry(r, 0)` body flattened on the mount face by a
  scale matrix, with a raised square interface plate and a bored pass-thru (a boolean is not
  available — the pass-thru is modelled as a short cylinder recess plus a darker vertex-colour
  floor, which reads identically at play distance and costs nothing).
- **LIVE DATA BINDING** — the anchor's ring warms only when the probe is docked to a real plant
  socket whose auth actually resolved (`grid.key(auth)` true via `/state.energy.plants[]`
  membership). A locked plant leaves it cold — the refusal is rendered, not hidden.
- **FIDELITY GATE** — **G-2 + G-3**: this is the module most likely to be over-lit, because
  "connected" feels like it wants light. Passes only if amber appears exclusively while a real
  auth is resolved. **G-1**: the flattened icosahedron must not read as a sphere.
- **DEPENDS ON** — A-001, A-059.

---

**A-007 · PH-07 / SIGNAL EAR** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 7 (SIGNAL FIN (x4), BASE CONTACT PAD;
  mount glyph = secondary/diamond) — four swept fins in an asymmetric fan.
- **AEA CONCEPT SERVED** — `verb.observe` · `axis.S` ASYNC (it hears the entity acting
  unattended).
- **TECHNIQUE** — four tapered `BoxGeometry` fins at authored, **unequal** angles (the sheet's
  fan is asymmetric — an evenly-spaced fan is the loop-index tell, E2 §4.2 offender 3), merged;
  base contact pad is a chamfered disc. Flat matte only; no specular anywhere (bundle_02 §6:
  no metal, no chrome).
- **LIVE DATA BINDING** — fin tips carry a single structure-ink tick that brightens (within
  the structure opacity ladder, **not** into amber) with live `/events` arrival rate. Hearing
  is not being alive; it does not earn amber.
- **FIDELITY GATE** — **G-1**: fin count and the asymmetry of the fan both read in silhouette.
  **G-3**: amber census must be **zero** on this module — it is a listener.
- **DEPENDS ON** — A-001.

---

### 2.2 THE BENCH PARTS — A-008 … A-015

`A1_bench_parts.png` is an 8-cell atlas at 1:2, units millimetres, all parts ≈0.4 m. Each cell
carries the index, code, name, four callouts on leader lines, and two mount glyphs (top and
bottom of the caption). The sheet's own note is binding: *"ALL MODULES COMPATIBLE WITH BENCH
STANDARD INTERFACE · ALIGNMENT TOLERANCE ±0.15mm · POWER RAIL 01 · DATA RAIL 01 · TRACE RAIL 01."*
Three rails means every part has three port classes, and a part built with one port is wrong.

**Shared spec, stated once and not repeated per ticket:** body ≤ 0.4 m; one ring collar; port
studs on the sanctioned mount-glyph vocabulary; a mount glyph engraved on the base; the part is
built by a single parameterised generator (E6 §1.6 CGA-lite: `Subdiv` / `Repeat` / `Taper` over
a scope, baked to ONE merged geometry per part). The eight tickets below differ in profile,
port layout and binding — not in method.

---

**A-008 · BT-11 / POWER TAP** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A1_bench_parts.png` cell 1 (POWER NODE INPUT triangle, LOAD PORTS
  (x4), GROUND STUD diamond, MOUNT POINT triangle) — a ribbed cylinder with four barrel ports
  around the waist and **the one amber ring on the top cap**: the only amber in row 1.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE — "the model grid answers." This is the part that
  makes a construct able to draw at all; the first construct in the game is TAP+SCORER (T-001).
- **TECHNIQUE** — `CylinderGeometry(r, r, h, 12)` body; four load ports = `CylinderGeometry`
  studs on a 90° `Repeat` around the waist, each with a `TorusGeometry` collar; vertical ribs
  cut by `Subdiv` into 8 facets with alternating vertex-colour values (this is what makes it
  read as machined rather than extruded). Top cap ring = flat `TorusGeometry`,
  `emissive INK.warm`, idle tier.
- **LIVE DATA BINDING** — the top ring's tier ← whether this chip is seated AND the run is
  drawing (`/api/construct/run` row in flight); the four load ports light **individually** per
  real routed leg, never as a set. Capacity text on the bench plate ← `/state.energy.plants[]`
  `rpm_now / rpm_cap` for the carrier actually used.
- **FIDELITY GATE** — **G-3**: cell 1's amber is exactly one ring; a tap with lit ports at idle
  fails the census before it is looked at. **G-1**: four ports count as four in silhouette at
  the bench camera (fixed high oblique, `bench.js` dock camera).
- **DEPENDS ON** — T-001.

---

**A-009 · GV-22 / GOVERNOR** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A1_bench_parts.png` cell 2 (SETPOINT DIAL, GOVERNOR CORE HEX,
  FEEDBACK PORT diamond, BASE INTERFACE square) — knurled dial cap over a squared body.
- **AEA CONCEPT SERVED** — `op.design` (tag the task with what it needs before running) ·
  `seed.1`'s honest ceiling: the governor is the rate law made an object.
- **TECHNIQUE** — knurled cap = `CylinderGeometry(r, r, h, 24)` with a `Repeat` of thin
  vertical inset boxes merged in (24 knurls; at play distance they collapse to a value band,
  which is correct); the hex core is an `ExtrudeGeometry` 6-gon seated in a square-shouldered
  body; feedback port is a recessed diamond inlay via `ShapeGeometry`.
- **LIVE DATA BINDING** — the dial's index mark position ← the real cap it is enforcing
  (`rpm_cap` / `rpd_cap` from `/state.energy.plants[]`). **Where a plant is uncapped (ollama),
  the dial shows NO needle and the plate prints UNCAPPED** — a parked needle would read as a
  bearing (the `IP-03` law in `panels.js`, reused here verbatim).
- **FIDELITY GATE** — **G-5**: three measured facts or it is a shape — cap, current, and
  window. **G-2**: knurling must not introduce a specular tell; if the cap glints, the material
  is wrong (bundle_02 §6, no chrome).
- **DEPENDS ON** — A-008, T-001.

---

**A-010 · LD-03 / LADDER** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `A1_bench_parts.png` cell 3 (TOP HOOKS (x2) triangle, RUNG TREADS, FOOT
  PADS diamond, LOCK POINT ring) — a leaning ladder, entirely cold, no amber.
- **AEA CONCEPT SERVED** — `seed.7` CEILING-DETECT — "a quality gate flags the ceiling —
  escalate deeper" (`pathfinder.py` reflex → bulk → deep). The ladder IS the escalation.
- **TECHNIQUE** — two stile `BoxGeometry` rails + a `Repeat` of rung boxes, merged into one
  geometry (a ladder built as 14 meshes is 14 draw calls for nothing). Hooks are two small
  bent-box composites. Nothing on this part emits.
- **LIVE DATA BINDING** — rung count ← the real number of tiers configured in `paths.json` /
  `pathfinder.py` for the current task type. Not decorative: if the entity has two tiers, the
  ladder has two rungs. When the tier list is unavailable, the part does not render — an
  invented rung count is a fabricated reading.
- **FIDELITY GATE** — **G-3**: zero amber, always. Escalation is not a celebration.
  **G-4**: the rails must stay hairline-dominant; a chunky ladder is the fastest way to fail
  the ≥76%-at-≤2px clause at this scale.
- **DEPENDS ON** — T-001.

---

**A-011 · SC-07 / SCAFFOLD** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A1_bench_parts.png` cell 4 (UPPER RAIL ring, FOOT PLATE diamond,
  ANCHOR SOCKET square) — an open braced tower with X-bracing on all four faces.
- **AEA CONCEPT SERVED** — `axis.R` PROMPTING — "a frontier-encoded scaffold makes a cheap node
  beat its raw self" (`memory.py` recall-grounded prompts). The literal object of the axis.
- **TECHNIQUE** — CGA-lite is at its best here: `Subdiv` the vertical scope into 3 bays,
  `Repeat` the leg + brace terminal per bay, `Taper` the top bay slightly. All bays baked to one
  merged geometry. The X-braces are thin boxes rotated in-plane, **not** lines — this is a
  SOLID and an additive-line scaffold is a doctrine violation (E8 §5.5).
- **LIVE DATA BINDING** — bay count ← the number of scaffold layers actually applied to the
  prompt for this run (system + recall + task, read from the run's trace rows). A three-bay
  scaffold means three real layers.
- **FIDELITY GATE** — **G-1**: the open lattice must survive flat-black silhouette — if it
  fills in solid, the members are too thick. **G-7**: "point to the anchor socket."
- **DEPENDS ON** — T-001.

---

**A-012 · SR-16 / SCORER** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A1_bench_parts.png` cell 5 (SENSOR ARRAY RING, SCORE OUTPUT,
  CALIBRATION PORT diamond, MOUNT POINT triangle) — the **concentric target face** is the
  subject, and it carries the second amber accent of the sheet.
- **AEA CONCEPT SERVED** — `seed.2` SHARP OBJECTIVE — "every task carries a falsifiable
  scorer." Without this part a run produces no reward, which is the game's whole economy.
- **TECHNIQUE** — a drum body with a large flat face carrying the concentric field as
  double-line rims (four rings on the AEA radii ratios 150/250/360/470 scaled — the same
  citation `panels.js` uses to make rings legal), drawn to a 512px `CanvasTexture`; one amber
  index mark on the innermost ring; a raised sensor collar `TorusGeometry` around the face rim.
- **LIVE DATA BINDING** — the index mark's angle ← the real score returned by the scorer for
  the completed run; **no score = no mark**. Pass/fail is not colour-coded (there is no red);
  a miss is amber withdrawn plus a printed receipt (`bench.js` failure law).
- **FIDELITY GATE** — **G-3 and G-6**: the amber index must be one
  mark ON the concentric motif (E8 E-8, "the hot mark lands on a ring"); at the bench's
  delivered chip size (~90px) the rings must still separate — if not, drop to three rings
  rather than thinning.
- **DEPENDS ON** — T-001.

---

**A-013 · RF-21 / RELAY FORK** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A1_bench_parts.png` cell 6 (FORK TINES (x2), PIVOT AXIS ring, ACTUATOR
  PORT diamond, BASE SOCKET HEX) — a two-tine fork on a pivoting head.
- **AEA CONCEPT SERVED** — `doc.relay` THE GENETIC RELAY (`relay.py`: 5 distinct models, 2/2
  handoffs, toolkit reused downstream) · `axis.M` MULTIPLICITY.
- **TECHNIQUE** — tines are tapered boxes with a `Taper` terminal; the pivot head is a short
  cylinder in a yoke; the base socket is an inset hexagon (`ExtrudeGeometry`). The fork's
  **rotation is real state**, not idle animation: it points at the leg currently carrying the
  capsule, and holds.
- **LIVE DATA BINDING** — tine selection ← which downstream leg the real relay handed to
  (`relay.py` chain rows in `chains.jsonl` / the run trace). Never animated when no relay is
  running (E8 §5.3: motion may add what a still cannot hold, but never a second idle attention
  magnet).
- **FIDELITY GATE** — **G-1**: two tines, and the pivot reads as a pivot at the bench camera.
  **G-3**: amber only on the tine that actually carried.
- **DEPENDS ON** — A-008, T-001.

---

**A-014 · BK-14 / BALLAST KEY** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A1_bench_parts.png` cell 7 (BALANCE RING, MASS SLIDER TRACK, KEY
  SOCKET HEX, INDEX MARK diamond) — an upright bar with a slider track and terminal micro-text
  down its face.
- **AEA CONCEPT SERVED** — `seed.9` BOUNDARY — "a private task NEVER routes to a trains-zone
  plant" (`brief.py`: sensitive → local only). The key is the zone law you can hold.
- **TECHNIQUE** — a slender box body; the slider track is a **cut** channel (two inset boxes
  with a darker vertex-colour floor) with a machined block riding it; the balance ring is a
  `TorusGeometry` collar at the top; the face micro-text is a `CanvasTexture` of real terminal
  glyphs at `NearestFilter` — density as evidence (E8 E-5), so the text is a real string, never
  lorem greeble.
- **LIVE DATA BINDING** — the slider's position ← the construct's declared zone
  (`public` / `private` / `sensitive`, the REQUIRED field in construct-spec v0.1.0); the key
  socket seats only when the chosen carrier's `privacy` ring legally accepts that zone
  (`grid.PLANTS[p].privacy`). An illegal pairing physically will not seat — the law is
  enforced by geometry, which is the best teaching this game does.
- **FIDELITY GATE** — **G-5**: the face text must trace to a real datum (zone, carrier,
  privacy ring) — a mark whose only justification is "looks technical" is cut. **G-6**: at
  chip size the slider position must be readable as a position, not a smudge.
- **DEPENDS ON** — T-001, A-062.

---

**A-015 · CB-09 / CONDUIT BRIDGE** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A1_bench_parts.png` cell 8 (CONDUIT CHANNELS (x3), LINK INTERFACE HEX,
  ALIGNMENT PINS (x2) diamond, MOUNT CLIP square) — an arched three-bore block, the sheet's
  only curved part.
- **AEA CONCEPT SERVED** — `verb.propagate` — the three bores ARE the sheet's three rails
  (POWER 01 / DATA 01 / TRACE 01). The trace rail is the honesty node made plumbing.
- **TECHNIQUE** — the arch is a `LatheGeometry` quarter-profile swept 180° then capped, or
  equivalently an `ExtrudeGeometry` of an arch `Shape` along a short depth with `bevelSize`
  0.004 — take the extrude, it gives the flat planar faces the sheet shows. Three bores =
  three cylinder recesses with `TorusGeometry` collars. Alignment pins are two studs; the mount
  clip is a square inlay.
- **LIVE DATA BINDING** — the **trace** bore alone carries the live packet (A-086) when a run
  is in flight; power and data bores stay structure ink always. Wiring a light into the power
  bore would imply we measure power, and we do not.
- **FIDELITY GATE** — **G-1**: the arch silhouette is this part's whole identity — it is the
  only curved bench part and must be identifiable in flat black among the eight. **G-2**: the
  bore interiors are the darkest values in the cell; if the recess floors are not below the
  outer body's value, the vertex-colour ramp was not applied.
- **DEPENDS ON** — T-001, A-086.

---

### 2.3 THE SPECIMEN VESSELS — A-016 … A-024

`A2_specimen_rods.png` is an 8-cell atlas at 1:2, ≈0.5 m rods, each a reliquary with a **stat
plate** printing SPEED / RELIABILITY / DECAY STATE. `game/ref/a2_rods.png` is the pixel cut and
is the judged target. Cell 7 (SR-41 ACTIVE RELIC) is the sheet's single amber cell — its whole
stat plate is bracketed in amber because that model is online.

**The honesty rule that governs all nine tickets, stated once:** the sheet's numbers
(`0.61 m/s`, `0.99`) are layout fillers. Copying one into the game is a fabricated reading and
a direct honesty-law violation (E8 §5.1). The sheet specifies the **field**; `model_fitness.json`,
`capability_census.json` and `energy_usage.json` supply the **value**. A rod whose numbers match
the sheet has failed, not passed.

---

**A-016 · SR-CHASSIS / THE RELIQUARY ROD (shared generator + stat plate)** — `SOLID` · `L` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png`, the anatomy shared by all eight cells: cap
  (primary triangle) → housing → **encapsulated core** → collar → base lock ring (pentagon),
  plus the six-glyph class strip and the three-line stat plate beneath every cell.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE — the model grid, held one model at a time.
- **TECHNIQUE** — one parameterised generator: `LatheGeometry` cap (quarter-profile, the only
  sanctioned route to a non-spherical cap — the law already written in `artifacts.js`),
  `CylinderGeometry` housing at 8/10/12 facets by family, a glass sleeve
  (`transparent:true, opacity:.16, depthWrite:false`) over an inner core mesh, ring collars as
  `TorusGeometry`, base lock ring as a lathed pentagon plinth. Deterministic seeding by FNV-1a
  over the model id → LCG (the `seals.js` law; **no `Math.random` in any generator**, E6 §4).
  The stat plate is FLAT-UI attached to the object, not geometry (E8 §5.4: plate conventions
  are not world geometry) — it renders in the codex/bench panel, never floating in 3D.
- **LIVE DATA BINDING** — every parameter is a real field: facet count ← family;
  housing height ← context window; collar count ← measured census score; core emissive ←
  online/offline from the live catalog. Absent value ⇒ that feature is **absent**, never
  defaulted.
- **FIDELITY GATE** — **G-1 across all eight**: the eight rods must be distinguishable from one
  another in flat-black silhouette. If two collapse to the same outline the generator's
  parameter spread is too narrow — that is a form decision, not a tuning one (E8 §4.4).
- **DEPENDS ON** — T-040, T-041.

---

**A-017 · SR-03 / COLD RELIQUARY** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png` cell 1 (POLAR SEAL CAP triangle, GRAPHENE
  REINFORCED HOUSING ring, MODEL CORE ENCAPSULATED, BASE LOCK RING pentagon; stat plate reads
  DECAY STATE: STABLE).
- **AEA CONCEPT SERVED** — `seed.1` · the STABLE rung of the decay ladder.
- **TECHNIQUE** — A-016 generator, longest housing, tightest facet count (12), a single thin
  interior filament visible through the sleeve. One structure-ink hairline pair banding the
  housing.
- **LIVE DATA BINDING** — a real local model with a measured non-zero reliability and no
  cooling entry in `energy_usage.json`. **The rod is not built for a model the entity has never
  actually run** (`tried[]` must be non-empty) — an unrun model has no measurements and would
  need invented ones.
- **FIDELITY GATE** — **G-5**: exactly three facts on the plate, all measured, all with units.
- **DEPENDS ON** — A-016.

---

**A-018 · SR-07 / QUIET CARTRIDGE** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png` cell 2 (VENT CAP (SEALED) triangle, QUARTZ
  SLEEVE, SIGNATURE STRAND, LOCK COLLAR; DECAY STATE: DORMANT, SPEED 0.00 m/s).
- **AEA CONCEPT SERVED** — `seed.1` · the DORMANT state — a model present but not drawn from.
- **TECHNIQUE** — A-016 generator; sealed cap (no aperture geometry); the signature strand is a
  single `CatmullRomCurve3` `TubeGeometry` of 5 control points inside the sleeve, structure ink.
- **LIVE DATA BINDING** — `SPEED 0.00` here is legal **only** because it is a measured zero:
  zero calls in the current `energy_usage.json` window. A zero that is really "unknown" prints
  a dash, never a zero (`bench.js` /state law).
- **FIDELITY GATE** — **G-3**: zero amber. A dormant vessel that glows is the honesty law
  broken in one pixel.
- **DEPENDS ON** — A-016.

---

**A-019 · SR-11 / LATTICE REPOSITORY** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png` cell 3 (THERMAL DAMP CAP, SILICATE CHAMBER,
  AI SIGNATURE LATTICE, ISOLATION COLLAR; DECAY STATE: QUIET) — the diagonal lattice through
  the body is this rod's identity.
- **AEA CONCEPT SERVED** — `seed.1` · `seed.9` BOUNDARY (isolation collar = the private-zone
  model that may not leave the machine).
- **TECHNIQUE** — A-016 generator plus a lattice: a `Repeat` of thin crossed boxes on a helical
  pitch inside the chamber, merged; the isolation collar is a double-rim `TorusGeometry` pair
  (two hairlines with a gap — E8 E-7).
- **LIVE DATA BINDING** — built only for a plant whose `privacy` is `local`; the collar's
  presence IS the privacy ring, read from `grid.PLANTS[p].privacy`. No privacy field ⇒ no
  collar ⇒ visibly a different object.
- **FIDELITY GATE** — **G-4**: the lattice is the line-weight trap of the whole set — 76% of
  strokes at ≤2px normalised, or the rod reads as a chunky basket.
- **DEPENDS ON** — A-016.

---

**A-020 · SR-19 / TRACE AMPOULE** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png` cell 4 (PRESSURE SEAL TIP, VACUUM TUBE, MODEL
  TRACE COIL, STABILIZER BAND; DECAY STATE: DRIFTING) — carries a thin amber coil, the sheet's
  second-lightest amber.
- **AEA CONCEPT SERVED** — `verb.propagate` · the DRIFTING rung (measurements moving against
  their own history).
- **TECHNIQUE** — A-016 generator; the coil is a helical `TubeGeometry` over a parametric
  curve, 3 turns, `emissive INK.warm` at idle tier; tangent-oriented segments (the ORIENTATION
  LAW already learned in `artifacts.js` WA-12: under `rotation.y = t` a box's local X is
  radial, so segment boxes must be built tangent or they fan wrong).
- **LIVE DATA BINDING** — "DRIFTING" is assigned only when the model's measured reliability has
  actually moved beyond a pre-registered band across two census runs
  (`capability_census.json` + `model_fitness.json`) — never as flavour.
- **FIDELITY GATE** — **G-3**: one coil, warm tier, and it is the only amber in the cell.
- **DEPENDS ON** — A-016.

---

**A-021 · SR-23 / CORE CANISTER** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png` cell 5 (SHOCK CRADLE CAP, CERAMIC HOUSING,
  ENCODED CORE BLOCK, DAMPER PLATE; DECAY STATE: STABLE) — the widest, heaviest silhouette.
- **AEA CONCEPT SERVED** — `seed.1` · `doc.solo` THE SOLO LAW (the one good model an easy task
  wants).
- **TECHNIQUE** — A-016 generator with the housing scaled to the widest profile and the fewest
  facets (8) so it reads as mass; the encoded core block is a boxy inner solid with engraved
  micro-text `CanvasTexture`; damper plates are two square shoulders.
- **LIVE DATA BINDING** — carried by the highest-scoring model in `capability_census.json` this
  sweep; when the sweep changes, the rod's occupant changes and the world event fires (T-062).
- **FIDELITY GATE** — **G-1**: heaviest silhouette in the set; if it does not read as the
  heaviest, proportion work, not shading.
- **DEPENDS ON** — A-016.

---

**A-022 · SR-29 / NEEDLEKEEPER** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png` cell 6 (NEEDLE SEAL, PHASE GLASS ROD, SIGNATURE
  FILAMENT, GRIP RING; DECAY STATE: SLOW DECAY) — the thinnest silhouette, a needle.
- **AEA CONCEPT SERVED** — `seed.1` · the SLOW-DECAY rung.
- **TECHNIQUE** — A-016 generator at minimum radius; the needle seal is a sharp `LatheGeometry`
  cone; a single grip `TorusGeometry`. This rod exists to prove the generator's parameter
  spread — it is the silhouette extreme opposite A-021.
- **LIVE DATA BINDING** — assigned to a model with a real, rising consecutive-failure count
  (`energy_usage.json` `consec_fail`), short of the cooling threshold of 3.
- **FIDELITY GATE** — **G-1** against A-021 in the same flat-black frame: if the two do not
  read as opposite extremes, the generator is not spreading.
- **DEPENDS ON** — A-016, A-021.

---

**A-023 · SR-41 / ACTIVE RELIC** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png` cell 7 (RADIANT CAP, ACTIVE COOLING SPINE,
  MODEL CORE (ONLINE), POWER COUPLER RING; the **whole stat plate is amber-bracketed** and the
  class strip's first glyph is amber) — the sheet's one live vessel, and the model named in
  `R3_05_gameplay_screen.png`'s trace caption.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE at its live tier · `pr.coherence` (the vessel
  that is currently carrying the route).
- **TECHNIQUE** — A-016 generator; the cooling spine is a `Repeat` of ~10 stacked amber rings
  (`TorusGeometry`, hot tier) down the housing — the highest amber density permitted on any
  single object in this registry, and legal only while the model is genuinely answering. Power
  coupler ring at the base, warm tier. Bracketed stat plate is FLAT-UI (A-064 family).
- **LIVE DATA BINDING** — **this rod exists only while its model appears in a live route.**
  Its ring count lit ← the fraction of the last 60s window this carrier actually served
  (`rpm_now / rpm_cap`, or the literal count when uncapped). When the model goes quiet, the
  rings go out one by one on the attack-decay law (A-087) and the rod becomes an ordinary rod.
- **FIDELITY GATE** — **G-3 is the whole ticket**: this cell is allowed to exceed the plate
  budget locally because the sheet does, but the **frame** census still binds — an ACTIVE RELIC
  on screen means something else must be dark. **G-7**: a stranger must call this one "the live
  one" without being told.
- **DEPENDS ON** — A-016, A-087.

---

**A-024 · SR-58 / DECAY CHAMBER** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A2_specimen_rods.png` cell 8 (FRACTURE CAP, CORRODED SLEEVE, DEGRADED
  SIGNATURE, CRUMBLING BASE; DECAY STATE: ROTTING, RELIABILITY 0.34) — visible fracture through
  the sleeve, entirely cold.
- **AEA CONCEPT SERVED** — `seed.4` FLEXIBILIZE (a node dies; the route falls; the task still
  completes) · `pr.coherence`.
- **TECHNIQUE** — A-016 generator + the **deterministic fracture** routine already written in
  `artifacts.js` (surface integrity expressed as geometry, never as a colour): displaced
  vertices along a seeded plane, plus separated shard boxes at the base. No colour change
  anywhere — rot is form.
- **LIVE DATA BINDING** — built only for a model with ≥3 consecutive real failures and a live
  `cooling` flag, or absent from the live catalog entirely (then it takes the LOST SIGNAL
  tombstone tag, T-064). Fracture seed ← the model id, so the same dead model always cracks the
  same way.
- **FIDELITY GATE** — **G-2**: rot must not tint. If a reviewer can name a colour for "rotten,"
  the two-ink law broke. **G-1**: fracture must read in flat-black silhouette, which means it
  is geometry and not a texture.
- **DEPENDS ON** — A-016, A-093, T-064.

---

### 2.4 THE WORLD ARTIFACTS — A-025 … A-035

**A NAMED CUT, made here rather than discovered later.** `A5_world_artifacts.png` presses
WA-01..WA-08 and `C3_world_artifacts_v3_dimensioned.png` presses WA-09..WA-16. Read side by
side, five of the C3 objects are **revisions of A5 objects, not new ones**:

| A5 | C3 | verdict |
|---|---|---|
| WA-01 MEMORY INGOT | WA-09 MEMORY INGOT | same object, dimensioned revision — **build WA-09 only** |
| WA-02 BIRTH CAPSULE | WA-10 THOUGHT-BIRTH CAPSULE | same object — **build WA-10 only** |
| WA-03 ROT LINK | WA-11 SEVERED ROT LINK | same object — **build WA-11 only** |
| WA-04 TRACE GLASS | WA-12 TRACE RIBBON | same object — **build WA-12 only** |
| WA-05 VERDICT SLATE | WA-13 WATCH VERDICT CORE | same object — **build WA-13 only** |
| WA-06 ARCHIVE SHARD | — | **unique to A5, still owed** |
| WA-07 CONDUIT FOSSIL | — | **unique to A5, still owed** |
| WA-08 SILENCE STONE | — | **unique to A5, still owed** |
| — | WA-14 / WA-15 / WA-16 | new in C3 |

Five tickets that would otherwise have been written are therefore **not written**. Sixteen
artifacts on paper are eleven buildable objects. The C3 set is the revision of record because
it carries real dimensions; A5 keeps authority only for its three uniques.

The eight C3 objects are `[BUILT]` in `game/js/artifacts.js` and judged against the pixel cuts
`game/ref/wa_*.png` in `lab.html`. Their tickets below are **fidelity closeouts**, not builds:
the remaining work is the ledger line, and the named gap if a gate fails.

---

**A-025 · WA-06 / ARCHIVE SHARD** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A5_world_artifacts.png` cell 6 (ARCHIVE LAYER STRATA, FRACTURE PLANE
  EDGE, DATA ECHO IMPRESSIONS, CATALOG INDEX NOTCH) — an irregular flake with a concentric
  impression on its face.
- **AEA CONCEPT SERVED** — `seed.10` BACKWARDS CHANNEL (`memory.py` vector store recall) — a
  fragment of a capsule that outlived its run.
- **TECHNIQUE** — a seeded irregular flake: `IcosahedronGeometry(r, 1)` with vertices displaced
  along a deterministic plane cut so the faces stay planar (organic curvature is banned,
  bundle_02 TECHNICAL §1); strata are parallel inset cut lines down one face; the concentric
  impression is a recessed ring set carried in the vertex-colour attribute as double-line rims,
  not a texture. Catalog index notch = one square inlay.
- **LIVE DATA BINDING** — strata count ← the real number of consolidation passes the recalled
  memory survived (`consolidate.META` `processed`). Collectible existence ← the memory it
  represents actually being in the store; a shard for a memory that does not exist is a
  fabricated object.
- **FIDELITY GATE** — **G-1**: an irregular solid must still read as *this* irregular solid —
  the seeded cut plane makes it reproducible, so the silhouette is comparable across runs. If
  it is not comparable, the seed is not being applied. **G-7**: "point to the catalog index
  notch."
- **DEPENDS ON** — A-033 (that module owns the shared helpers).

---

**A-026 · WA-07 / CONDUIT FOSSIL** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A5_world_artifacts.png` cell 7 (ANCIENT CONDUIT FOSSIL, FLOW PATTERN
  REMAINS, MINERALIZED INSULATION, INTERFACE SCAR RING) — a hollow segmented tube stub standing
  upright.
- **AEA CONCEPT SERVED** — `pr.coherence` RESTORABLE COHERENCE read backwards: this is a route
  that did not reroute. The fossil of a dead path.
- **TECHNIQUE** — open `CylinderGeometry(r, r, h, 10, 1, true)` (`openEnded` true — the interior
  is the point) with a second inner shell, capped by a ring so the wall reads as having
  thickness; mineralised insulation = a `Repeat` of irregular collar blocks around the outside;
  the interface scar ring is a `TorusGeometry` with one segment deliberately absent.
- **LIVE DATA BINDING** — flow-pattern grooves ← the real historical call count for the route it
  fossilises, read once from `events.jsonl` at collection time and **frozen** (a fossil that
  keeps updating is not a fossil). The freeze is recorded in `journey_save.json` with its
  source line.
- **FIDELITY GATE** — **G-3**: zero amber. A dead conduit that glows contradicts both the object
  and E2 Move 7. **G-5**: void ≥ 80% in the codex plate view.
- **DEPENDS ON** — A-033.

---

**A-027 · WA-08 / SILENCE STONE** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A5_world_artifacts.png` cell 8 (SILENCE CORE DENSITY, ACOUSTIC NULL
  SURFACE, CALM FIELD SHEATH, EMPTINESS ANCHOR) — an ovoid with a faint concentric field on its
  face; the most featureless object in the entire library, deliberately.
- **AEA CONCEPT SERVED** — `seed.9` BOUNDARY — the sacred wall. What a private task leaves
  behind is nothing, and this is the object shaped like nothing.
- **TECHNIQUE** — a low-facet `LatheGeometry` ovoid (14 profile points × 10 segments) with an
  almost-flat vertex-colour ramp; the only surface incident is the concentric field, cut
  shallowly into one face. **The hardest ticket in the set for the wrong reason:** there is
  nothing to hide behind. If it reads as a grey egg, the value ramp and the ring depth are the
  only two levers — greebling it is forbidden (E8 E-5: there is no greeble anywhere in the
  sheet set).
- **LIVE DATA BINDING** — `NONE`, and the reason is the object's meaning: it represents work
  done **without leaving a trace outside the machine**. Binding it to a number would destroy the
  only artifact in the game whose honest state is *no data*. The codex entry says exactly that
  in words.
- **FIDELITY GATE** — **G-2 and G-5**; G-3 is trivially zero. Passes when a stranger shown the
  sheet cell and the render calls them the same object **despite** having no feature to point
  at — G-7 at its purest.
- **DEPENDS ON** — A-033.

---

**A-028 · WA-09 / MEMORY INGOT** — `SOLID` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` cell 1 (0.48 m; crystalline
  matrix, stability banding, entangled traces, resonance core) · pixel cut
  `game/ref/wa_ingot.png`.
- **AEA CONCEPT SERVED** — `seed.10` BACKWARDS CHANNEL.
- **TECHNIQUE** — built: tapered prism under a cone with the FACET LAW correction applied (facet
  counts matched so the two solids share edges); two cold hairline stability bands; five
  deterministic entangled slivers; ONE amber resonance core read *through* the matrix and ringed
  by the concentric motif.
- **LIVE DATA BINDING** — provenance `ARCHIVE STRATA-03` is catalogue text and is printed as
  catalogue text; the resonance core sits at warm tier (a stored memory exists — it is not
  working).
- **FIDELITY GATE** — closeout: run G-1..G-7 against `wa_ingot.png` in `lab.html`, record the
  ledger line. Expected failure point is **G-4** (line weight on the entangled slivers at
  delivered size).
- **DEPENDS ON** — none.

---

**A-029 · WA-10 / THOUGHT-BIRTH CAPSULE** — `SOLID` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` cell 2 (0.52 m; glass shell over
  six cold staves, five struts leaning on ONE amber seed, lathed birth-seal dome) · cut
  `game/ref/wa_capsule.png`.
- **AEA CONCEPT SERVED** — `seed.5` SELF-VERSION (a run writes a NEW skill; a later run uses it).
- **TECHNIQUE** — built: glass shell (`transparent`, low `opacity`, `depthWrite:false`) over six
  staves — the shell alone reads as nothing, which is why the staves exist; lathe dome + seal
  stack cap.
- **LIVE DATA BINDING** — the seed is warm when the skill it represents exists in `modules.json`
  / the skills store; absent skill ⇒ no capsule.
- **FIDELITY GATE** — closeout. Expected failure point is **G-2**: transparent shells are the
  most common third-hue leak in the build.
- **DEPENDS ON** — none.

---

**A-030 · WA-11 / SEVERED ROT LINK** — `SOLID` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` cell 3 (0.41 m; open torus arc
  whose gap straddles 2π, flat cut joint faces, rot vector scars, corruption crystals) · cut
  `game/ref/wa_rotlink.png`.
- **AEA CONCEPT SERVED** — `seed.4` FLEXIBILIZE · `doc.verifier` read as a warning.
- **TECHNIQUE** — built: arc torus with the gap midpoint lifted (the arc sweeps from 0, so the
  gap straddles 2π — the fix is recorded in the module); joint faces flat, cut, unfinished;
  scars are cold rules laid across the tube, **never a glow**.
- **LIVE DATA BINDING** — `NONE`, stated: a found object from a failure that already happened.
  Binding a live number to a severed link would imply the failure is ongoing.
- **FIDELITY GATE** — closeout. **G-1** is the interesting one: the gap must be visible from the
  play camera, not only from the sheet's three-quarter.
- **DEPENDS ON** — none.

---

**A-031 · WA-12 / TRACE RIBBON** — `SOLID` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` cell 4 (0.46 m; eight cold
  verticals giving the glass an edge, 2.5 turns of banded tangent-oriented segments, cold time
  ticks) · cut `game/ref/wa_ribbon.png`.
- **AEA CONCEPT SERVED** — `verb.propagate` — the game's autograph object.
- **TECHNIQUE** — built, including the ORIENTATION LAW fix (segments built tangent so they do
  not fan under `rotation.y`). The ribbon is the one amber.
- **LIVE DATA BINDING** — segment count ← the number of trace rows in the run it preserves,
  frozen at collection with the source run id recorded.
- **FIDELITY GATE** — closeout. **G-3**: one continuous amber path — if the census reads high,
  the segments are over-emissive, not too many.
- **DEPENDS ON** — none.

---

**A-032 · WA-13 / WATCH VERDICT CORE** — `SOLID` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` cell 5 (0.39 m; wafer with six
  radial authority channels, rim integrity clasps built on the radial-X law, hexagon judgment
  core on the concentric field) · cut `game/ref/wa_wafer.png`.
- **AEA CONCEPT SERVED** — `seed.6` SELF-MODEL (`hades.py` Law-3 verdicts) · `doc.verifier`.
- **TECHNIQUE** — built; clasps account for local X being radial under `rotation.y`.
- **LIVE DATA BINDING** — the hexagon core is warm when the verdict it carries was a real HADES
  accept; a hold or redo verdict produces the same geometry **cold**. Verdict class ←
  `decisions.jsonl`.
- **FIDELITY GATE** — closeout. **G-6**: the six channels must still count at codex thumbnail
  size.
- **DEPENDS ON** — none.

---

**A-033 · WA-14 / DATA MONOLITH** — `SOLID` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` cell 6 (0.50 m; inscription
  layers as cold rules with ONE amber column of live-looking density) · cut
  `game/ref/wa_monolith.png`.
- **AEA CONCEPT SERVED** — `op.learn` (a run's result measurably improves the next;
  `pathfinder.py` → `paths.json`) · lineage.
- **TECHNIQUE** — built. This module also owns the shared helpers every other artifact ticket
  depends on: the three material families, the primitive helpers (Box / Cylinder / Torus /
  Icosahedron / Octahedron / Lathe / Extrude), the parameter-complete cache-key law, the
  six-glyph grammar, the concentric-field helper and the deterministic fracture routine.
- **LIVE DATA BINDING** — the amber column's row count ← real entries in `paths.json` for the
  crystallised route; an empty `paths.json` renders the column cold and empty, which is the
  honest pre-`op.learn` state.
- **FIDELITY GATE** — closeout. **G-5**: every inscription row must trace to a real datum — this
  is the object most tempted toward decorative text.
- **DEPENDS ON** — none.

---

**A-034 · WA-15 / TRUST SPHERE** — `SOLID` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` cell 7 (0.43 m) · cut
  `game/ref/wa_sphere.png` · governance vocabulary from `B8_governance.png` (the four ascending
  trust seals: forbidden / draft / watched / trusted).
- **AEA CONCEPT SERVED** — `seed.9` BOUNDARY + the governance ladder (`trust.py` CHARTER).
- **TECHNIQUE** — built (faceted sphere, never smooth — a smooth sphere is the one form that
  cannot show facet value separation and would fail E-7 by construction).
- **LIVE DATA BINDING** — the lit ring ← the **live** level from `/state.trust[cap]`, which can
  fall as well as rise. A trust level is never cached inside the artifact.
- **FIDELITY GATE** — closeout. **G-3**: exactly one ring lit, ever.
- **DEPENDS ON** — none.

---

**A-035 · WA-16 / OUTREACH CAPSULE** — `SOLID` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` cell 8 (0.47 m, provenance
  BROADCAST MAST) · cut `game/ref/wa_outreach.png` · ceremony context `B9_the_send.png`.
- **AEA CONCEPT SERVED** — `op.ship` — unskippable: a run produces a REAL external artifact
  (`brief.py`, a HADES-accepted brief).
- **TECHNIQUE** — built.
- **LIVE DATA BINDING** — exists only if a real send was confirmed by the human hand; minted
  from the `decisions.jsonl` send row and carrying that row's timestamp. A drafted-but-unsent
  message mints **nothing** — the machine can draft, only the human can mean it.
- **FIDELITY GATE** — closeout. **G-7**: the stranger must connect this object to the mast
  (A-043) without prompting.
- **DEPENDS ON** — T-028.

---

### 2.5 THE ORGAN BUILDINGS — A-036 … A-043

`A3_organ_buildings.png` is an 8-cell atlas, codes OB-01..OB-08, each with four named callouts
and a class glyph. Only cell 2 (WATCHER GATE) and cell 8 (BROADCAST MAST) carry amber on the
sheet — the verdict aperture and the message lamp. That ratio is the spec, not a suggestion.

**Shared method, stated once:** each organ is a CGA-lite composition (`Subdiv` / `Repeat` /
`Taper`) over a `LatheGeometry` stepped plinth, **baked into ONE merged geometry per organ**
(E6 §1.6 — a grammar that is not baked reintroduces the draw-call problem it exists to solve).
Budget: landmark composites ≤ 7 draw calls across ring 0 (E6 §7), so an organ that cannot merge
does not ship. Analytic vertex AO (`vertexAO()`, INSIDE method) at the plinth contact is what
stops these reading as boxes floating on a plane.

---

**A-036 · OB-01 / MEMORY ARCHIVE** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A3_organ_buildings.png` cell 1 (MEMORY STACKS (x12), ARCHIVE VAULT,
  RECALL CONDUIT; ring class glyph) — a domed drum of twelve vertical ribs on a stepped base ·
  interior/mood `S6_the_archive.png` (vertical strata, one descending light shaft, amber veins).
- **AEA CONCEPT SERVED** — `seed.10` BACKWARDS CHANNEL (`memory.py` vector store recall).
- **TECHNIQUE** — lathed dome + a `Repeat` of 12 rib boxes on the drum (the sheet says twelve;
  twelve is not a guess); recall conduit is a merged `TubeGeometry` run leaving the base. The S6
  interior is **not modelled** (E5 §2, rule of the atmosphere class): one instanced shelf shape
  repeated down a shaft, a vertical fog gradient, one cylinder for the light shaft.
- **LIVE DATA BINDING** — rib segments lit ← `/state.memory.memories` against
  `/state.memory.sessions`. Zero memories ⇒ every rib cold, which is the true state at game open.
- **FIDELITY GATE** — **G-1**: twelve ribs count as twelve at mid distance. **G-6**: the
  designation plate stays readable at real traversal distance, or the plate moves closer to the
  ground — it does not grow (G-6 fails to scale and hierarchy work, never to a tooltip).
- **DEPENDS ON** — A-058, T-006.

---

**A-037 · OB-02 / WATCHER GATE** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A3_organ_buildings.png` cell 2 (VERDICT APERTURE — the sheet's focal
  amber concentric mark — SENTRY RING, ACCESS CAUSEWAY; pentagon class glyph) · aperture states
  from `B8_governance.png` (accept / hold / redo).
- **AEA CONCEPT SERVED** — `seed.6` SELF-MODEL (`hades.py` Law-3 verdicts) · `doc.verifier` THE
  LONE VERIFIER RISK (the watcher survives by strict schema + a DIFFERENT model than the worker).
- **TECHNIQUE** — two flanking pylons (tapered boxes) carrying a suspended aperture: a
  concentric `TorusGeometry` pair with a bladed inner iris built from a `Repeat` of thin wedges.
  The aperture is the **only** emissive surface on the building and it sits on the concentric
  motif (E8 E-8, textbook case). Causeway is a merged slab with cut seams.
- **LIVE DATA BINDING** — aperture tier and blade position ← the live verdict stream
  (`decisions.jsonl` / `hades.py` accept-hold-redo). No verdict pending ⇒ closed and cold. It
  never idles open.
- **FIDELITY GATE** — **G-3**: this is the amber the sheet grants — one aperture, hot only during
  a real verdict. **G-7**: "point to the verdict aperture" is the substituted question, and it
  must be the first thing the eye lands on.
- **DEPENDS ON** — A-058.

---

**A-038 · OB-03 / VOICE MAST** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A3_organ_buildings.png` cell 3 (VOICE EMITTER, HARMONIC COLUMN,
  RESONANCE BASE; hexagon class glyph) — a stepped needle on a ringed circular base, entirely
  cold on the sheet.
- **AEA CONCEPT SERVED** — the speak organ (`speak.py`, `voice/`). Deliberately **not**
  `op.ship`: a spoken line is not an external artifact, and lighting this like the broadcast
  mast would teach the wrong law.
- **TECHNIQUE** — a fluted `LatheGeometry` needle (~14 profile points × 10 radial segments) on a
  three-step lathed plinth with concentric rings cut into the base — the lathe vocabulary that
  serves all seven landmarks (E6 §1.2), written once here and reused.
- **LIVE DATA BINDING** — one structure-ink band on the column brightens **within the structure
  ladder** while the entity is actually speaking (`talk_state.json` turns / the speak organ
  running). It never crosses into amber: speech is not proof.
- **FIDELITY GATE** — **G-3**: zero amber, permanently. **G-4**: a fluted needle at distance is
  the classic line-weight failure — flutes must collapse into a value gradient, not a picket
  fence.
- **DEPENDS ON** — A-058.

---

**A-039 · OB-04 / REFLECTION CHAMBER** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A3_organ_buildings.png` cell 4 (REFLECTION VAULT, ECHO WELLS, MIRROR
  RING; triangle class glyph) — an open-topped cylinder of vertical panels with one small warm
  disc on its face.
- **AEA CONCEPT SERVED** — `seed.6` SELF-MODEL — the entity reports what it is made of and
  judges its own work (`reflect.py`).
- **TECHNIQUE** — open cylinder built as a `Repeat` of 16 panel boxes around a ring (open-topped
  so the interior reads); echo wells are recessed circular cuts in the floor slab; the mirror
  ring is a double-rim torus pair. The one warm disc is a small emissive inlay.
- **LIVE DATA BINDING** — the disc is warm only when a real reflection exists in
  `reflections.jsonl` newer than the last consolidation; it cools when the reflection has been
  acted on. Count ← the file, never a counter the game keeps.
- **FIDELITY GATE** — **G-1**: the open top must read as open in silhouette from the play
  camera's 6 m elevation — if it reads closed, the panel count or the camera assumption is wrong.
- **DEPENDS ON** — A-058.

---

**A-040 · OB-05 / ROUTER NEXUS** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A3_organ_buildings.png` cell 5 (ROUTING NODE, CONDUIT SPINE, DATA CLOT;
  square class glyph) — a cruciform mass with four horizontal arms, the only radially-armed
  building in the set.
- **AEA CONCEPT SERVED** — `axis.P` PATH (the entity defines its own next step) · `op.design` —
  this is `think.py`, one door where the task picks the regime (T-044).
- **TECHNIQUE** — a central tower with four arms placed by matrix and merged; arm ends carry hex
  link interfaces. Conduits leaving the arms are merged `TubeGeometry` runs joining the MST
  conduit graph (E6 §4.4) — **elbows snapped to 45°**, which is what makes the ductwork read as
  drafted rather than sagging.
- **LIVE DATA BINDING** — each arm corresponds to a real regime (solo / council / relay / path,
  per the doctrines); an arm exists only if that regime is actually implemented. Arm-tip marks
  light on the regime that served the current run (`/api/node/run` branch taken).
- **FIDELITY GATE** — **G-1**: four arms and the cruciform plan read from above and from the play
  camera. **G-5**: an arm without an implemented regime is **deleted, not dimmed** — this gate is
  never passed by adding.
- **DEPENDS ON** — A-058, T-044.

---

**A-041 · OB-06 / MIND SPIRE** — `SOLID` · `L` · `[PLANNED]`
- **STYLE REFERENCE** — `A3_organ_buildings.png` cell 6 (THOUGHT BELFRY, COGNITIVE SHAFT, FOCUS
  PLATFORM; diamond class glyph) · the world-scale version is the centre of
  `S9_the_city_revealed.png` (one lit spire on a stepped concentric plinth) · silhouette
  discipline `S1_field_genesis.png`.
- **AEA CONCEPT SERVED** — `axis.M` MULTIPLICITY (`swarm.py`, 8 roles coordinated) ·
  `pr.emergence` EMERGENCE OVER IMPOSITION.
- **TECHNIQUE** — E6 §4 generator 5 (`spire(state)`): a fluted `LatheGeometry` shaft (~14 profile
  points × 12 radial segments ≈ 168 verts), stepped concentric plinth, belfry as a
  `Subdiv`+`Taper` composite, all merged. 200 m per the scale table — the one object that must
  read at 2 km horizon distance as pure silhouette AND at close range with cut lines.
- **LIVE DATA BINDING** — height ← REGISTERED rows in `modules.json` against the total; lit flute
  count ← `/state.trust[*].level > 0`; the vertical beam ← `life.alive_since` uptime. Pre-registry
  the shaft renders **unlit** — the spire grows as the entity is actually accounted for.
- **FIDELITY GATE** — **G-6 at two distances** (the only ticket judged twice): silhouette at
  horizon, cut lines at approach. **G-3**: this beam plus the probe is most of the frame's
  permitted scene amber — everything else in shot must be dark.
- **DEPENDS ON** — A-058, A-097, T-052.

---

**A-042 · OB-07 / FOUNDRY STACK** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A3_organ_buildings.png` cell 7 (MATERIAL STACK, FUSION CHAMBER, CYCLE
  CONDUIT; ring class glyph) — a clustered chimney bundle on a ringed base with external conduits.
- **AEA CONCEPT SERVED** — `seed.3` CRYSTALLIZE (freeze a repeated behaviour into a reusable
  tool) — this is where organs come to exist (P7, the forge sessions).
- **TECHNIQUE** — a `Repeat` of 5 unequal-height cylinder stacks (unequal **by real data**, not
  by taste); external cycle conduits are merged tubes with 45° elbows; the base is a lathed ring
  platform. The building visibly changes shape when the entity's tool count changes.
- **LIVE DATA BINDING** — stack count and heights ← forged organs present in `modules.json` with
  their files verified on disk (`/api/manifest` live per-row flags, T-053). A *planned* organ
  shows **scaffolding** (A-058), never a stack.
- **FIDELITY GATE** — **G-5**: no stack may exist for an unforged organ; this gate fails to
  deletion. **G-1**: the cluster must not read as one chimney.
- **DEPENDS ON** — A-058, T-053.

---

**A-043 · OB-08 / BROADCAST MAST** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A3_organ_buildings.png` cell 8 (MESSAGE LAMP — **the sheet's one hot
  amber mark** — BROADCAST RING, SIGNAL FOOT; pentagon class glyph) · ceremony `B9_the_send.png`
  (the mast beyond the lever, unlit, waiting).
- **AEA CONCEPT SERVED** — `op.ship`. The moral centre: "the machine can draft / only the human
  can mean it."
- **TECHNIQUE** — lathed tapered mast, a broadcast ring collar, a splayed signal foot on a ringed
  base; the message lamp is a single tiny emissive box at the apex, hot tier — **the smallest
  emissive surface in the world carrying the largest meaning**. Bloom does the rest (locked
  0.65/0.4/0.5, never re-tuned for this).
- **LIVE DATA BINDING** — the lamp lights **only** on a confirmed real send (T-008, T-028:
  `send_confirmed` tri-state written by a human action). A refusal renders the refusal plaque in
  structure ink with the real date. Zero sends ⇒ a dark mast, forever, and that is the correct
  art.
- **FIDELITY GATE** — **G-3 is binary here**: the lamp is off, or the send was real. Any state in
  between is a lie. **G-7**: shown the dark render and the sheet, the stranger must still call
  them the same object — the test of whether the mast's *form* is doing the work rather than its
  light.
- **DEPENDS ON** — A-058, T-008, T-028.

---

### 2.6 THE DISTRICT LANDMARKS — A-044 … A-050

`A7_district_landmarks.png` is a 7-cell atlas at 1:250, **units metres**, codes DL-01 / DL-04 /
DL-07 / DL-10 / DL-13 / DL-16 / DL-19. Only cells 1 and 2 carry amber (the nexus alignment groove
and the socket pylon's two power rings). The sheet's note binds: *"ALL LANDMARKS COMPATIBLE WITH
DISTRICT SURVEY STANDARD · ALIGNMENT TOLERANCE ±0.25 m."*

**Shared method:** every one of the seven is *a stepped plinth, a tapered shaft, ring collars and
a cap* — which is exactly the `lathe(profile, segments)` + `profileFromData(...)` pair E6 §1.2
calls the highest sheet-fidelity per line in the chapter. Build the profile library once here;
six of the seven then cost a profile array each. Blender is legal on this group **only as a
measuring instrument** (E6 §5): block out, read the real step ratios and setback angles, type the
numbers into the profile, delete the `.blend`. No export, no loader, no `.glb`.

---

**A-044 · DL-01 / NEXUS SLAB** — `SOLID` · `L` · `[PLANNED]`
- **STYLE REFERENCE** — `A7_district_landmarks.png` cell 1 (NEXUS PLANE CARVING, ALIGNMENT GROOVE
  — amber — BASE RING SOCKET; ring class glyph) — a standing slab, 8 m, with a large concentric
  carving on its face · in-world staging `S4_the_bench.png`.
- **AEA CONCEPT SERVED** — `verb.compose` — assemble subtask results into one coherent whole. This
  is where the player composes; it is the game's core creative act rendered as a place.
- **TECHNIQUE** — a chamfered slab (`BoxGeometry` + edge bevel boxes, merged) on a lathed ring
  socket; the nexus plane carving is the concentric field cut into the face as double-line rims,
  authored into vertex colour with a shallow inset, **not** projected as a decal; vertical striae
  down the face are `Repeat` cut lines. The alignment groove is the single amber: one inset ring,
  warm tier.
- **LIVE DATA BINDING** — the groove goes hot only while a construct is actually running on the
  bench docked to this slab (`/api/construct/run` in flight). Idle bench ⇒ warm at most; empty
  bench ⇒ cold.
- **FIDELITY GATE** — **G-1** at the dock camera (`bench.js` fixed high oblique) *and* at the
  approach camera. **G-4** is the second gate: the carving's rings must hold
  the 1/2/4-per-1024 stroke ratio at the dock camera, where the slab fills much of the frame and
  every stroke is scrutinised.
- **DEPENDS ON** — T-001.

---

**A-045 · DL-04 / SOCKET PYLON** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A7_district_landmarks.png` cell 2 (SOCKET HEAD INTERFACE — amber ring —
  POWER SHAFT CONDUIT, ANCHOR RING PLINTH — second amber ring; pentagon class glyph) — 12 m,
  buttressed, the only two-amber cell on the sheet.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE — the grid answers, and this is the socket it
  answers through. In Act I this is the keyless socket: the first thing that speaks in the dark.
- **TECHNIQUE** — lathe profile with four buttress fins added as `Repeat` boxes and merged; the
  socket head is a recessed cylinder ringed by a `TorusGeometry`; the anchor plinth is a second
  torus at the base. Both rings emissive, warm tier at rest.
- **LIVE DATA BINDING** — head ring ← whether this socket's plant is in `/state.energy.plants[]`
  (online) — a plant whose key is absent leaves the pylon **cold**, which is the honest render of
  a locked provider. Base ring pulses on the attack-decay law per real request served.
- **FIDELITY GATE** — **G-3**: two rings is the ceiling the sheet grants; a third lit element on
  this pylon fails. **G-7**: "point to the socket head interface."
- **DEPENDS ON** — A-051, A-087.

---

**A-046 · DL-07 / METER OBELISK** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A7_district_landmarks.png` cell 3 (MEASUREMENT DIAL, DATA CHANNEL STRIP,
  CALIBRATION PLINTH; hexagon class glyph) — 14 m, a stepped needle obelisk, entirely cold.
- **AEA CONCEPT SERVED** — `verb.observe` — meter telemetry + trace; the state is visible
  (`tracelog.py` goal-stack ledger).
- **TECHNIQUE** — lathe profile with a square-to-octagon transition (the sheet's stepped plinth
  is four diminishing lathed steps); the data channel strip is a long inset cut line running the
  shaft, carrying real terminal micro-text as a `CanvasTexture` at `NearestFilter`; the
  measurement dial is a small concentric inlay near the apex.
- **LIVE DATA BINDING** — the strip's text is the live meter (`/state.energy.plants[]` `rpm_now`,
  `rpd`, throttle list) rendered as terminal rows. **Where a value is unknown it prints a dash**,
  never a zero (the `bench.js` `/state` law, reused verbatim).
- **FIDELITY GATE** — **G-5**: every glyph on the strip traces to a real datum, or it is cut. This
  is the object where "density is evidence" is most easily faked and most cheaply checked.
  **G-6**: the strip is texture at distance (legal, E8 E-5) but the **designation** must remain
  type at traversal distance, ≥ 0.9% of frame width.
- **DEPENDS ON** — A-051.

---

**A-047 · DL-10 / MAST** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A7_district_landmarks.png` cell 4 (SIGNAL SPIRE ARRAY, TENSION CABLE
  ANCHOR, FOUNDATION RING; triangle class glyph) — a guyed needle with three tension cables,
  cold on the sheet.
- **AEA CONCEPT SERVED** — `op.ship`, as the district-scale companion to OB-08. Where OB-08 is the
  organ, DL-10 is the landmark the player navigates by.
- **TECHNIQUE** — lathe needle + three `TubeGeometry` guy cables over `CatmullRomCurve3` with a
  real sag term (a straight cable reads as a stick); foundation ring is a lathed step. The cables
  are the one place a thin tube beats a line, because a `LineSegments` cable would be an additive
  line on a SOLID and therefore a doctrine violation.
- **LIVE DATA BINDING** — `NONE` on the mast body, stated: it is a navigation landmark, not an
  instrument. Its **apex** lamp is a mirror of OB-08's send state and is bound there, not here —
  one datum, one owner.
- **FIDELITY GATE** — **G-1**: three cables and the guyed silhouette read at 60–150 m, which is
  where this object is actually seen. **G-3**: zero amber unless OB-08 is lit.
- **DEPENDS ON** — A-051, A-043.

---

**A-048 · DL-13 / MIRROR** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A7_district_landmarks.png` cell 5 (REFLECTIVE PLANE — with a thin warm
  arc on its rim — RING GIMBAL FRAME, AZIMUTH BASE PLATFORM; square class glyph) — a great disc
  in a gimbal, the S9 wheel silhouette.
- **AEA CONCEPT SERVED** — `seed.6` SELF-MODEL. The entity looking at itself, at district scale.
- **TECHNIQUE** — a large lathed disc (flat, faceted rim — never a smooth mirror; there is no
  chrome in this world) held in a `TorusGeometry` gimbal ring on a stepped azimuth base. The
  reflective plane's face carries the concentric field as cut rings; "reflection" is expressed by
  the ring pattern and by the **ground reflection effect** (A-091), never by a real mirror pass —
  a planar reflection would double the draw calls and break the palette budget.
- **LIVE DATA BINDING** — the gimbal's azimuth ← the real bearing of the last reflected subject
  (the organ most recently reflected on in `reflections.jsonl`). No reflection ⇒ parked at its
  survey datum with the datum printed, so the parked position is not read as a bearing.
- **FIDELITY GATE** — **G-2**: this object is the single largest temptation toward a specular
  tell in the whole registry. If any pixel reads as chrome, the material is wrong. **G-1**: the
  disc-in-gimbal silhouette is one of the two shapes that identify S9's skyline.
- **DEPENDS ON** — A-051, A-091.

---

**A-049 · DL-16 / MERIDIAN** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A7_district_landmarks.png` cell 6 (SOLAR MARK ALIGNER, MERIDIAN CHANNEL,
  CIRCULAR PLATFORM; diamond class glyph) — twin leaning needles with a ring suspended between
  them, on a circular ringed platform.
- **AEA CONCEPT SERVED** — `op.time` (every tick timestamped and observable) · `pr.time`
  OPERATOR-OBSERVABLE TIME (`tracelog.py` DAG, append-only).
- **TECHNIQUE** — two lathed needles placed by matrix at a real, unequal lean; the aligner ring is
  a `TorusGeometry` suspended between them; the platform is a lathed disc with concentric survey
  rings cut in and radial hairlines from the ground shader (E6 §1.3 — the rings belong to the
  ground, not to a new mesh).
- **LIVE DATA BINDING** — the meridian channel's shadow mark ← the entity's real tick clock
  (`/state.life.ticks`, `heartbeat.json`), so the landmark is a clock the player can read. If the
  entity is asleep the mark does not move, and the platform prints the last real tick time —
  a stopped clock that says it is stopped.
- **FIDELITY GATE** — **G-1**: two needles at unequal lean; an equal, symmetric pair is the
  composition-by-loop-index tell. **G-5**: the printed tick is the real one or the plate is blank.
- **DEPENDS ON** — A-051, A-096.

---

**A-050 · DL-19 / LINEAGE ARCHIVE** — `SOLID` · `L` · `[PLANNED]`
- **STYLE REFERENCE** — `A7_district_landmarks.png` cell 7 (ARCHIVE CORE CHAMBER, RETRIEVAL PORT
  ACCESS, RECORD BASE VAULT; ring class glyph) — a massive faceted keep with a concentric medallion
  low on its face; the heaviest silhouette on the sheet.
- **AEA CONCEPT SERVED** — `op.learn` (a run's result measurably improves the next) · `seed.5`
  SELF-VERSION — the lineage of forged organs, dead ends included.
- **TECHNIQUE** — the one landmark the lathe alone cannot make: a CGA-lite mass (`Subdiv` into
  three tiers, `Repeat` buttresses, `Taper` the cap) merged with a lathed medallion inlay.
  Analytic vertex AO matters most here — a 40–60 m keep with no ground-contact darkening is the
  "boxes floating on a plane" failure at its most visible.
- **LIVE DATA BINDING** — the lineage tree renderer (T-009) reads real parent/diff/score rows;
  **dead ends render at full volume**, not faded — a lineage that hides its failures is the
  honesty law broken structurally rather than visually.
- **FIDELITY GATE** — **G-1**: heaviest mass on the skyline reads as the heaviest. **G-5**: every
  lineage row on the plate is a real row; there is no placeholder ancestry.
- **DEPENDS ON** — A-051, T-009.

---

### 2.7 THE FOUNDRY — THE FIFTEEN PLANTS — A-051 … A-057

**A NAMED COMPRESSION, argued rather than assumed.** The order asked for "the 15 plant
identities." Fifteen tickets would be fake granularity, and the sheet itself says why: `D2` R-C
prints, in its own note block, *"ALL PLANTS SHARE THE 20 m ARCHETYPE."* Fifteen towers are one
generator with fifteen real parameter rows — and under E6 §4 **no generator may take a parameter
that is not a real field**. So this section is one generator ticket, five silhouette-archetype
tickets that partition all fifteen, and one capacity-plate ticket. Nothing is lost: the mapping
below is exhaustive and every plant is named.

| archetype | ticket | real plants (from `city.data.js`, verified 2026-07-21) |
|---|---|---|
| HEARTH — local, private, uncapped | A-052 | `ollama` |
| GRID — many turbines, high rate | A-053 | `nvidia` (40 rpm) · `ovh` (400) · `cloudflare` (300) |
| REFLEX — lean, fast, hard-capped | A-054 | `groq` (30) · `cerebras` (30) · `sambanova` (20) |
| BATCH / LOCKED — trains-zone, slow or keyed | A-055 | `gemini` · `mistral` · `openrouter` · `zai` · `github` · `cohere` |
| KEYLESS SOCKET — open to anyone | A-056 | `pollinations` (4 rpm) · `hf` |

**A COLLISION, named not worked around** `[DECISION-LUIS]`. `D2` R-C labels its fifteen cells
THE HEARTH · THE GRID · REFLEX · BATCH · KEYLESS · NEXUS · HADES · COGNITION · VOYAGER ·
BARANDIARAN · BEDAU · DGM · STOP · RESEARCH · SANDBOX. Cells 06–15 are **organ and boss names,
not plants** — the sheet mixed the foundry row with the module registry. The roster of record is
`city.data.js` / `grid.PLANTS` (the fifteen providers above). Either the sheet's cells 06–15 are
re-read as organ sites (A-058), or the foundry row is re-drawn. Luis rules; nothing is built
against the sheet's naming until he does.

---

**A-051 · THE PLANT GENERATOR (shape grammar + the fifteen parameter rows)** — `SOLID` · `L` · `[PLANNED]`
- **STYLE REFERENCE** — `D2_quad_screen_bench_plants_states_v2.png` quadrant R-C (fifteen
  dimensioned tower silhouettes, widths 10–22 m around the 20 m archetype, each over a capacity
  plate) · `S1_field_genesis.png` (the row as it reads in world: silhouette variety and fog, not
  polygon count) · `R3_03_power_plant_turnaround.png` (the ortho the profile numbers are read
  from).
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE — "the model grid answers — plants, generators,
  free energy." The foundry row IS this seed, at world scale.
- **TECHNIQUE** — E6 §4 generators 1–2: `plotRing(plant)` (lathed 3–4-step plinth, 64 segments,
  outer radius ← `zone` band + `models` count, step count ← `privacy` rank) and
  `massing(plant, seed)` (CGA-lite towers, count ← `models`, height ← `rpm_cap`, footprint ←
  `rpd_cap`, setback ← `privacy`), baked to one `InstancedMesh` for rings 0–1. Deterministic
  seeding FNV-1a → LCG on the plant id; **no `Math.random`**. This ticket also **deletes** E2 §4.2
  offender 3 (fifteen near-identical silhouettes at loop-index spacing) — the row is grown, never
  placed.
- **LIVE DATA BINDING** — every parameter above is a real field. Uncapped plant (`ollama`,
  `rpm_cap` null) ⇒ height from that plant's own `rods[].calls` share, and the panel prints
  **UNCAPPED** — never a fabricated ceiling (E2 Move 3's recorded `tier` failure is the pattern
  being prevented).
- **FIDELITY GATE** — **G-1 in aggregate**: fifteen flat-black silhouettes side by side must be
  fifteen distinguishable shapes at small size (the D2 sheet's own requirement). If two collapse,
  the parameter spread is too narrow — a form decision, not a tuning one. **G-4** on the row at
  traversal distance.
- **DEPENDS ON** — A-096 (the ground is built before any tower — E6 §6 step 3).

---

**A-052 · THE HEARTH — local, private, never sleeps, asks no key** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `D2` quadrant R-C cell 01 THE HEARTH (KEYLESS; capacity plate ANYONE /
  ALWAYS) · warmth-in-the-dark staging `S1_field_genesis.png`.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE + `seed.9` BOUNDARY — the only plant a **sensitive**
  task may legally reach (`brief.py`: private → local only). This tower is the sacred wall's
  positive case.
- **TECHNIQUE** — A-051 generator, shortest profile, widest base, no key-plate geometry (the
  absence is the identity); the one plant permitted a warm ground pool beneath it, because it is
  the one plant that is always available.
- **LIVE DATA BINDING** — `ollama`. Window field lit fraction ← **literal count** of requests in
  the last 60 s (there is no denominator to invent). Online ← presence in
  `/state.energy.plants[]`.
- **FIDELITY GATE** — **G-3**: the warm pool is the exception the amber census must survive — if
  the frame's amber exceeds the scene budget with this plant in shot, the pool shrinks, it does
  not dim.
- **DEPENDS ON** — A-051.

---

**A-053 · THE GRID — many turbines, high rate, remote** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `D2` quadrant R-C cell 02 THE GRID (PRIVATE; HIGH / 4.0 tok/s / 24-7) —
  the widest, most repeated silhouette of the row.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE at scale · `axis.M` MULTIPLICITY (many nodes
  answering in parallel).
- **TECHNIQUE** — A-051 generator, tallest tower count via `Repeat`, tightest setback; this is the
  archetype where `InstancedMesh` earns its place (E6 §7 budget: one draw call for the massing).
- **LIVE DATA BINDING** — `nvidia` (40 rpm/model) · `ovh` (400 rpm) · `cloudflare` (300 rpm).
  Turbine count ← `models`; window field ← `rpm_now / rpm_cap`; **offline plants render as empty
  survey plots** (E6 §3.2), which is the game's named antagonist made visible.
- **FIDELITY GATE** — **G-1**: three plants share this archetype and must still differ by real
  parameters — if `nvidia`, `ovh` and `cloudflare` render identically, the generator ignored
  `models`.
- **DEPENDS ON** — A-051.

---

**A-054 · REFLEX — lean, fast, hard-capped** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `D2` quadrant R-C cell 03 REFLEX (CLOUD; FAST / 2.5 tok/s / BURST) — the
  narrowest tower of the row, 12 m.
- **AEA CONCEPT SERVED** — `seed.7` CEILING-DETECT — the reflex tier of `pathfinder.py`'s
  reflex → bulk → deep ladder. This is the plant the ladder starts on.
- **TECHNIQUE** — A-051 generator, narrow profile, few tall verticals, a visible cap collar (the
  hard rate limit as a physical band).
- **LIVE DATA BINDING** — `groq` (30 rpm / 1000 rpd) · `cerebras` (30 rpm) · `sambanova`
  (20 rpm / 20 rpd). The cap collar's fill ← `rpd` against `rpd_cap`; a throttled plant shows its
  throttle from `grid_state.json` and the meter obelisk names it.
- **FIDELITY GATE** — **G-1** against A-053 in one frame: lean must read as lean beside wide.
  **G-3**: cap collars are structure ink; a limit is not an achievement.
- **DEPENDS ON** — A-051.

---

**A-055 · BATCH / LOCKED — trains-zone, slow, sealed behind key-plates** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `D2` quadrant R-C cell 04 BATCH (CLOUD; SLOW / 1.0 tok/s / BATCH) and the
  locked plants with **dark windows** behind key-plates; privacy ring key block bottom-left of
  the same quadrant.
- **AEA CONCEPT SERVED** — `seed.9` BOUNDARY, negative case: a **trains-zone** plant may never
  receive private payload. The lock is the law wearing architecture.
- **TECHNIQUE** — A-051 generator, tallest and slowest profile with a key-plate slab across the
  intake — a real geometric obstruction, not a decal. Dark window field is achieved by the field
  simply having nothing to light, never by painting windows out.
- **LIVE DATA BINDING** — `gemini` · `mistral` · `openrouter` · `zai` · `github` · `cohere`. Key
  present ← `grid.key(auth)` resolving; absent ⇒ the plant does not appear in
  `/state.energy.plants[]` ⇒ **survey rings and a key-plate, nothing else**. `github` is flagged
  RETIRING in `city.data.js` and its plate must say so — a retiring provider that renders healthy
  is a lie the world tells.
- **FIDELITY GATE** — **G-5**: an offline plant must render as *absence*, and the absence must be
  legible as deliberate (rings + rim + plate), not as a missing asset. **G-3**: zero amber on any
  locked plant.
- **DEPENDS ON** — A-051, A-062.

---

**A-056 · THE KEYLESS SOCKET — open to anyone** — `SOLID` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `D2` quadrant R-C cell 05 KEYLESS (capacity plate 0.4 tok/s / ANYONE /
  ALWAYS) — the smallest, barest structure of the row · Act I staging `S1_field_genesis.png`
  ("fifteen silent witnesses / one still speaks").
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE at its first rung — the CHAT rung of the assistant
  ladder (`B6_assistant_ladder.png` rung 1: a single socket in the dark). This is the first thing
  in the game that answers.
- **TECHNIQUE** — A-051 generator at minimum: a plinth, a stub, one socket head. Deliberately the
  least geometry in the world, because the game's opening image is one small thing speaking in an
  enormous dark.
- **LIVE DATA BINDING** — `pollinations` (keyless, 4 rpm, 1 request in flight, public data only) ·
  `hf`. The socket answers on the real keyless ground truth: **one request in flight, sequential**
  — the game must not render parallel draws this plant cannot serve.
- **FIDELITY GATE** — **G-3 + E-1**: this is the scene where void share is highest (S1 measures
  93.5% void). The gate is passed by *not adding* — if the opening frame's void falls below 70%,
  delete the newest thing.
- **DEPENDS ON** — A-051.

---

**A-057 · THE CAPACITY PLATE + THE KEY-PLATE LOCK STATE** — `FLAT-UI` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `D2` quadrant R-C, the fifteen capacity plates beneath the towers (three
  rows: rate · privacy ring · cadence) and the PRIVACY RING KEY legend block (OPEN / CLOUD /
  LOCAL / PRIVATE).
- **AEA CONCEPT SERVED** — `verb.observe` · `seed.9` BOUNDARY — the privacy ring is the zone law
  printed where the player can read it before choosing a carrier.
- **TECHNIQUE** — SVG/DOM in the panel language (`panels.css` tokens, IBM Plex Mono, 10 px labels
  / 13 px body), corner brackets never closed boxes; every printed value passes the existing
  `put()` honesty gate in `panels.js` — the single function through which no unknown may print as
  a number. Dash vocabulary per field type is already defined there and is reused, not re-cut.
- **LIVE DATA BINDING** — `/state.energy.plants[]` per plant: `rpd`, `tokens`, `rpm_now`,
  `rpm_cap`, `rpd_cap`, `throttled[]`, `privacy`. **Unknown prints a dash.** This ticket is E6
  §4.12's panel obligation made concrete: a tower whose height cannot be traced to a printed
  number is decoration.
- **FIDELITY GATE** — **G-6**: the plate is judged at its real CSS box, no zooming; smallest label
  and the designation both readable at ≥ 0.9% of frame width. **G-5**: fifteen plates, and every
  value on every one of them traceable.
- **DEPENDS ON** — A-051, A-063.

---

### 2.8 SITE AND DOCK SOLIDS — A-058 … A-059

---

**A-058 · THE ORGAN SITE — SCAFFOLDING / HALF-BUILT / COMPLETE / LIT** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `D2_quad_screen_bench_plants_states_v2.png` quadrant R-D strip 4 (ORGAN
  SITE: scaffold → lit, five frames, identical framing, amber only in the last two) ·
  `bundle_02/03_TECHNICAL_TARGETS.md` §3 (the four named states).
- **AEA CONCEPT SERVED** — `op.ship` read honestly: an organ that is planned is **not** an organ.
  The scaffolding state is how the game refuses to render intention as achievement.
- **TECHNIQUE** — a shared scaffold shell: `Repeat` of thin frame boxes forming an open cage sized
  to the target organ's bounding box, merged, structure ink at 0.28/0.14. HALF-BUILT swaps a
  fraction of the target's merged geometry in from the base up (a real partial mesh, not a
  transparent ghost). COMPLETE removes the cage. LIT enables the organ's emissive tier. State is
  a swap between four prepared geometries, never a shader fade.
- **LIVE DATA BINDING** — the state is read, never authored: SCAFFOLDING = named in `modules.json`
  with no file on disk · HALF-BUILT = file exists, imports clean, not yet registered ·
  COMPLETE = registered · LIT = registered **and** it has actually run
  (`/api/manifest` live per-row flags, T-053, plus a real run in `events.jsonl`).
- **FIDELITY GATE** — **G-5**: the site must be legible as *deliberately unbuilt*. A stranger
  should read "nothing has been built here yet," never "the asset failed to load." **G-3**: zero
  amber before LIT.
- **DEPENDS ON** — T-052, T-053.

---

**A-059 · THE SOCKET / KIOSK — the probe's dock target** — `SOLID` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `A7_district_landmarks.png` cell 2 for the socket-head vocabulary, scaled
  to the 4.5 m kiosk of `bundle_02/03_TECHNICAL_TARGETS.md` §2 · `S4_the_bench.png` for how the
  probe meets it.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE · `seed.9` BOUNDARY — docking is where the auth
  channel resolves or refuses, in the world rather than in a menu.
- **TECHNIQUE** — a lathed plinth + a hex coupler head matching PH-03's interface exactly (the
  same 6-gon `ExtrudeGeometry` profile — the coupler and the socket are one dimension, so a
  stranger can see that they fit); a recessed alignment ring cut in the deck; concentric ground
  rings around the base from the ground shader, not new geometry.
- **LIVE DATA BINDING** — the coupler's ring warms **only** after a real auth resolves for this
  plant; a locked plant refuses the dock and the refusal is printed verbatim in the run log
  (the `bench.js` refusal law: "the carrier ANSWERED with a refusal — the zone/trust law working,
  printed verbatim").
- **FIDELITY GATE** — **G-7**: shown the probe and the kiosk, a stranger must be able to say which
  part of the probe goes into which part of the kiosk. If they cannot, the interface dimensions
  do not match and the fix is proportion, not lighting.
- **DEPENDS ON** — A-003, A-006, A-100.

---

## 3. CLASS: HOLOGRAM — what the entity SHOWS

Doctrine: lines + additive light. A projection is honestly a representation, so it is allowed to
be made of light — and **only** these three things are. The map and the city-as-diagram stay
HOLOGRAM even where S9 draws them with material (E8 §5.5). Conversely nothing in §2 may creep
into this class: an additive-line solid is a doctrine violation, not a style choice.

Shared technique law for all three: `LineSegments` / `LineBasicMaterial` with
`blending: THREE.AdditiveBlending`, `depthWrite: false`, `transparent: true`, rendered **after**
opaque geometry; structure ink at the sanctioned opacities carries the projection, amber carries
only what is genuinely live. Additive blending is legal here and nowhere else in the world.

---

**A-060 · THE CITY MAP HOLOGRAM** — `HOLOGRAM` · `L` · `[PLANNED]`
- **STYLE REFERENCE** — `S9_the_city_revealed.png` (the city as a diagram: spire at centre,
  ~10 district plots on concentric stepped platforms, conduits thinning outward with bright
  junction nodes, a sunken ring pit, **empty surveyed plots**) · `S2_entity_as_place.png` (the
  ringed core and elevated thought-filaments; "thought-filaments carry intent, not power, not
  matter, only direction").
- **AEA CONCEPT SERVED** — `verb.observe` (the state is visible) · `pr.time`
  OPERATOR-OBSERVABLE TIME — the whole entity, auditable in one look.
- **TECHNIQUE** — the district graph as merged `LineSegments` over the **same** MST topology the
  solid conduits use (E6 §4.4, Prim's over the real provider/zone graph, elbows snapped to 45°) —
  one graph, two renderings, so the hologram can never disagree with the world. Junction nodes are
  small additive quads on the six-glyph grammar. Concentric platform rings reuse the AEA radii
  ratios. One draw call for the lines, one for the nodes.
- **LIVE DATA BINDING** — topology ← the real provider/zone graph; a district's node exists for
  every plant in the registry and is **lit only if that plant is in `/state.energy.plants[]`**;
  per-link brightness ← routed calls from `events.jsonl`. Empty plots are drawn as empty — they
  are the literal set of organs proven-not-wired.
- **FIDELITY GATE** — **G-3 scene budget** is the hard one: S9 measures 1.614% amber of frame and
  5.68% of ink, the highest in the set, and it is still under the 1.7% ceiling. A hologram that
  glows everywhere fails. **G-1**: the spire-plus-ring-pit-plus-wheel silhouette must be
  recognisable as S9's skyline in flat black.
- **DEPENDS ON** — A-041, A-048, A-086. `[DECISION-LUIS]` **E6 §3.5 blocks the S9 read**: S9's
  dominant look is persistent amber conduits at rest, which A11 §4.1's closed list of legal idle
  amber does not permit and E2 Move 7 explicitly ruled against. Path (a) ship dark-until-traffic,
  or path (b) amend A11 §4.1 with a named per-link binding. The generator is written so both are
  one uniform apart; **nothing is built against (b) until Luis rules.**

---

**A-061 · THE CONCENTRIC FIELD PROJECTION** — `HOLOGRAM` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `S5_concentric_map.png` (five rings of glyphs around a lit core; known
  glyphs amber and connected, unknown dim; "what is not known, sleeps") · ring geometry is
  authored data, not art: `aea_elements.js` `rings[]` — core r70, rings 150 / 250 / 360 / 470 in a
  1000 viewBox, per BINDING UI SPEC v1.0 §2.
- **AEA CONCEPT SERVED** — the AEA itself: 5 axes · 10 seeds · 3 verbs · 4 mechanics · 4 ops ·
  3 principles = the 29 elements, arranged as the curriculum. The sacred motif (bundle_02 §4.1).
- **TECHNIQUE** — the **3D companion** to the 2D map screen (A-077): the same four radii lofted as
  additive ring `LineSegments` with the 29 node glyphs as small additive quads at their real
  angular positions. Links drawn **only** once the mission that teaches them completes
  (`AEA.links[].by`), and drawn as a one-shot draw-on animation, never a persistent glow.
- **LIVE DATA BINDING** — discovery state ← `journey_save.json` (missions' `discovers` lists +
  models encountered via real `tried[]` logs). `@partial` elements render as structure-ink
  outline at reduced weight; **amber is reserved for fully live** (T-032). The UNCHARTED SIGNAL
  census (T-035) renders organs present in `/state` but absent from `window.AEA` as markers —
  reality is allowed to outrun the book, visibly, never silently.
- **FIDELITY GATE** — **G-3 two-sided, and this is the object the two-sidedness was written for**:
  the amber census here *is* the save file (A11 §1). Too much amber at hour one is over-lighting;
  too little on a late save means earned understanding is not being rendered. Record both frames
  or the gate has not been run. **G-6**: 29 nodes at delivered size — the hardest legibility test
  in the registry alongside A-073.
- **DEPENDS ON** — A-077, T-032, T-035.

---

**A-062 · CONSTRUCT SCHEMATICS ON THE PLATE** — `HOLOGRAM` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `B5_constructs.png` (six assembled machines as wiring schematics with
  ports, live packets and speed / reliability / trace-rail stat blocks: THE FIRST DRAW · THE
  COUNCIL · THE RELAY · THE PATH · THE GOVERNED HAND · THE WATCHED LOOP) ·
  `B4_doctrine_plates.png` for the law each schematic obeys.
- **AEA CONCEPT SERVED** — `verb.compose` · the six combination doctrines (`doc.solo`,
  `doc.council`, `doc.verifier`, `doc.relay`, `doc.swarm`, `doc.path`) — measured laws, not
  invented ones.
- **TECHNIQUE** — projected above the nexus slab (A-044) as additive `LineSegments` in the port /
  wire / packet grammar B5 establishes; chips are the six-glyph nodes; the stat block is FLAT-UI
  and lives on the bench plate, **not** floating in 3D (E8 §5.4 — plate conventions in world space
  are a category error). The schematic is the *plan*; A-082..A-085's plate is the *instrument*.
- **LIVE DATA BINDING** — the schematic is a render of the player's actual construct spec
  (construct-spec v0.1.0: parts are module ids, zone REQUIRED) — never a stock diagram. A doctrine
  plate shows `READ` until it is `EARNED`, and amber lands only on EARNED (T-039); `doc.relay`
  stays READ until the relay forge exists.
- **FIDELITY GATE** — **G-5**: every port, wire and stat on the projection corresponds to a real
  part in the real spec. A decorative port fails. **G-1**: the six constructs must be
  distinguishable from one another as topologies at a glance — that is what makes the doctrines
  teachable.
- **DEPENDS ON** — A-044, A-082, T-001, T-039.

---

## 4. CLASS: FLAT-UI — the seals, the glyphs, the panels, the plate

Doctrine: SVG / DOM, no 3D. This is ~40% of the output and most of it is already final art
(E5 §1) — `seals.js`, `panels.js` and `probe.css` / `panels.css` are on disk and the B-sheets ARE
the asset. These tickets are therefore mostly **fidelity closeouts** judged in `lab.html` beside
the pixel cuts, plus the HUD and the bench plate, which are new.

Two standing laws for every ticket in this class. **(1) The `put()` gate:** every printed value
passes the single honesty function in `panels.js`; an unknown prints its dash shape, never a
number. **(2) Type law (04 §0):** IBM Plex Mono only, 10 px labels / 13 px body, corner brackets
never closed boxes, no radius, no drop shadow, no bevel.

*(A-057, the capacity plate, is FLAT-UI class and is filed in §2.7 beside the towers it serves,
because a plate separated from its object gets built against the wrong reference.)*

---

**A-063 · IP-01 / RUN PLATE** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C4_instrument_panels_v2.png` cell 1 · pixel cut `game/ref/ip01.png` ·
  original anatomy `A6_instrument_panels.png` cell 1.
- **AEA CONCEPT SERVED** — `op.time` (every tick timestamped and observable) · `verb.observe`.
- **TECHNIQUE** — built: chamfered plate shell (corner-cut outline + inner frame + edge notches,
  two mount slots per side), concentric reticle on the AEA radii ratios, four callouts on leader
  lines drawn *before* the plate body so labels paint over their tails. Data shape
  `{ id, cycles, cksm, firing }`.
- **LIVE DATA BINDING** — the execution mark is the plate's one live tell and is hot **only while
  a run is genuinely out** (`/api/construct/run` in flight); `cycles` and `cksm` are real or
  dashed.
- **FIDELITY GATE** — closeout against `ip01.png`. **G-4** is the expected failure: the plate's
  hairline-to-structure ratio must hold ≥ 76% of strokes at ≤ 2px normalised to a 1024 short side.
- **DEPENDS ON** — none.

---

**A-064 · IP-02 / RECORD BOOK STRIP** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C4_instrument_panels_v2.png` cell 2 · cut `game/ref/ip02.png`.
- **AEA CONCEPT SERVED** — `op.learn` (a run's result measurably improves the next) · `seed.2`
  SHARP OBJECTIVE — the record is the only reward this game gives.
- **TECHNIQUE** — built: eight numbered rows, always eight. The slot number `001..008` is engraved
  on the strip (it is the PANEL'S OWN structure, not data); the **entry glyph is the datum**.
- **LIVE DATA BINDING** — rows ← real per-construct records (speed / cost / reliability / privacy,
  personal bests, T-004). An empty slot engraves its number and prints nothing else — eight rows
  with three real entries is the honest render, never three rows.
- **FIDELITY GATE** — closeout against `ip02.png`. **G-5**: the distinction between engraved
  structure and printed datum must survive a stranger's read, or the panel is teaching that the
  game has eight records when it has three.
- **DEPENDS ON** — T-004.

---

**A-065 · IP-03 / ZONE DIAL** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C4_instrument_panels_v2.png` cell 3 · cut `game/ref/ip03.png` — E8 E-7
  names this panel's ring construction as the exemplar: **each ring is two hairlines with a gap**,
  so it reads as a rim with thickness rather than a stroke.
- **AEA CONCEPT SERVED** — `seed.9` BOUNDARY — the privacy geography (sensitive / private /
  public) as an instrument the player reads before choosing a carrier.
- **TECHNIQUE** — built: four ring bands **are** the AEA radii scaled — the citation that makes
  them legal; sector ticks one per 15°; band blocks straddle each ring at the spokes.
- **LIVE DATA BINDING** — takes a sector NUMBER or a zone WORD (`grid.ZONES`). **No measured
  sector ⇒ NO needle** — a parked needle would read as a bearing. This rule is the panel's most
  quoted law and is reused by A-009 and A-048.
- **FIDELITY GATE** — closeout against `ip03.png`. **G-6**: at its real CSS box the four bands
  must still separate; if they merge, drop a band rather than thinning the strokes.
- **DEPENDS ON** — none.

---

**A-066 · IP-04 / TRUST SEAL** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C4_instrument_panels_v2.png` cell 4 · cut `game/ref/ip04.png` · ladder
  vocabulary `B8_governance.png` (forbidden / draft / watched / trusted as four ascending seals).
- **AEA CONCEPT SERVED** — the governance ladder (`trust.py` CHARTER) · `op.ship`'s gate.
- **TECHNIQUE** — built. Data shape `{ valid_until, hash }`.
- **LIVE DATA BINDING** — level, streak, runs and fails ← `/state.trust[cap]`, live, and the level
  **can fall**. A seal is never cached across a poll.
- **FIDELITY GATE** — closeout against `ip04.png`. **G-3**: amber marks the level actually held
  this instant and nothing else.
- **DEPENDS ON** — none.

---

**A-067 · IP-05 / CARRIER-LOST CARD** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C4_instrument_panels_v2.png` cell 5 · cut `game/ref/ip05.png` · the
  failure grammar of `S7_honest_failure.png` (a severed link, annotated, STATUS: ACKNOWLEDGED;
  "failure is information. not an exception.").
- **AEA CONCEPT SERVED** — `pr.coherence` RESTORABLE COHERENCE, and its honest negative: when the
  game cannot see the entity it says exactly that.
- **TECHNIQUE** — built: the double-hexagon loss sigil, drawn in the six-glyph grammar and
  **always cold**. Data shape `{ code, time }`.
- **LIVE DATA BINDING** — raised on a real fetch failure or a dead carrier
  (`s === null` distinguished from `s === 0`, T-030 — a dead carrier can currently pass an
  observe, which is the bug this card exists to make impossible).
- **FIDELITY GATE** — closeout against `ip05.png`. **G-2**: there is no red in this world; a
  failure card that reads as an alarm has broken the two-ink law. Silence is the sting (T-075:
  core hum ducks .024 → .004 over 300 ms, no alarm tone).
- **DEPENDS ON** — T-030.

---

**A-068 · IP-06 / VERDICT REGISTER** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C4_instrument_panels_v2.png` cell 6 · cut `game/ref/ip06.png` · aperture
  states `B8_governance.png`.
- **AEA CONCEPT SERVED** — `seed.6` SELF-MODEL (`hades.py` Law-3) · `doc.verifier`.
- **TECHNIQUE** — built: eight channels, channel number engraved, **verdict is the datum**
  (`PASS` / `FAIL` / `HOLD` / null).
- **LIVE DATA BINDING** — rows ← real HADES verdicts from `decisions.jsonl`. A null verdict prints
  its dash; a pending verdict is not a `HOLD`.
- **FIDELITY GATE** — closeout against `ip06.png`. **G-5**: eight channels always, real verdicts
  only.
- **DEPENDS ON** — none.

---

**A-069 · IP-07 / LINK METER** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C4_instrument_panels_v2.png` cell 7 · cut `game/ref/ip07.png`.
- **AEA CONCEPT SERVED** — `verb.propagate` — the live trace of task → node → output, metered.
- **TECHNIQUE** — built.
- **LIVE DATA BINDING** — link integrity and latency ← the real run's trace rows; the meter
  degrades as an **event** (jitter, garbage digits, row flicker — T-069), never as ambient
  wallpaper. Scanlines are not signal until something can actually degrade.
- **FIDELITY GATE** — closeout against `ip07.png`. **G-5**: a meter that moves when nothing is
  happening is decoration and fails.
- **DEPENDS ON** — T-069.

---

**A-070 · IP-08 / ROUTE CARD** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `C4_instrument_panels_v2.png` cell 8 · cut `game/ref/ip08.png`.
- **AEA CONCEPT SERVED** — `axis.P` PATH · `op.learn` · `doc.path` THE CRYSTAL PATH (search once
  for the winning model per task-type, then run cheap forever — `pathfinder.py` → `paths.json`).
- **TECHNIQUE** — built.
- **LIVE DATA BINDING** — the route printed is the route actually taken, from the run's trace;
  the crystallised route comes from `paths.json`. An empty `paths.json` prints an empty card,
  which is the honest pre-`op.learn` state and is also the thing the player is working to change.
- **FIDELITY GATE** — closeout against `ip08.png`. **G-7**: a stranger shown the card and the
  cell must call them the same instrument.
- **DEPENDS ON** — T-013.

---

### 4.1 THE 29 ELEMENT SEALS — A-071 … A-074

**A NAMED COMPRESSION, argued.** The order asked for "the 29 element seals." Twenty-nine tickets
would be fake granularity in the opposite direction from the plants: `seals.js` generates all 29
from **one frame press plus six engraving families**, deterministically, reading the index from
`window.AEA` and never copying it. The buildable units are therefore the press and the six
families — and because the sheets group the families three-to-a-sheet, the **fidelity** unit is
the sheet. Four tickets, twenty-nine seals, no seal unaccounted for:

| ticket | families | elements | sheet |
|---|---|---|---|
| A-071 | the press (frames, brackets, field, caption, clip mask) | all 29 | all three |
| A-072 | seeds — THE ORGAN | 10 | `B2_seed_seals.png` |
| A-073 | axes — THE BRANCH · principles — THE MESH | 5 + 3 | `B1_axis_principle_seals.png` |
| A-074 | verbs — THE RELAY · mechanics — THE LATTICE · ops — THE DIAL | 3 + 4 + 4 | `B3_verb_mechanic_op_seals.png` |

Pixel cuts exist per element: `game/ref/el_*.png`, 29 files, straight cuts, never retouched — so
a target on the lab page cannot flatter its replica.

---

**A-071 · THE SEAL PRESS — frames, brackets, field, caption, clip mask** — `FLAT-UI` · `M` · `[BUILT]`
- **STYLE REFERENCE** — the frame language shared by `B1_axis_principle_seals.png`,
  `B2_seed_seals.png` and `B3_verb_mechanic_op_seals.png`: family → shape is binding (circle =
  seed · pentagon = axis · hexagon = principle · triangle = verb · square = mechanic · diamond =
  op), pentagon and triangle point up, and every seal carries index / code / NAME / proof line.
- **AEA CONCEPT SERVED** — the taxonomy itself: 5 axes · 10 seeds · 3 verbs · 4 mechanics ·
  4 ops · 3 principles, with `proof` naming the standalone demo that proved it (honest:
  demo-proven is not live-wired).
- **TECHNIQUE** — built: every family draws as a **path** so one dash vocabulary serves all six;
  a circle has no vertices, so its corner ticks are eight radial notches on the band; the frame is
  also a **clip mask**, so field and engraving can never bleed past the rim; the sacred concentric
  field sits faint under every engraving; deterministic FNV-1a (shift form — ES5 has no
  `Math.imul`) seeding an LCG whose products stay under 2^53 so the arithmetic is exact and
  portable.
- **LIVE DATA BINDING** — the index is **read from `window.AEA`, never copied** into the module;
  caption proof strings are the real `proof` fields. Mechanics are their own ring-3 nodes and
  mirror a seed, so their proof IS the seed's proof — stated, not duplicated.
- **FIDELITY GATE** — **G-1** per family frame against the `el_*.png` cuts. **G-4**: 29 seals is
  where a 1px drift multiplies by 29; the stroke ratio is checked on the *sheet* of seals, not on
  one seal.
- **DEPENDS ON** — none.

---

**A-072 · THE TEN SEED ENGRAVINGS — THE ORGAN** — `FLAT-UI` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `B2_seed_seals.png`, all ten circle-framed medallions, each engraved with
  an abstract mechanism expressing its meaning · cuts `game/ref/el_seed.1.png` …
  `el_seed.10.png`.
- **AEA CONCEPT SERVED** — the ten seeds: SUBSTRATE · SHARP OBJECTIVE · CRYSTALLIZE · FLEXIBILIZE ·
  SELF-VERSION · SELF-MODEL · CEILING-DETECT · TRANSCENDENCE · BOUNDARY · BACKWARDS CHANNEL.
- **TECHNIQUE** — built: the ORGAN engraving — a swept shell whose sweep and node placement are
  seeded per element, so **ten organs do not press ten identical faces**. The one accent is the
  shell actually swept and the node it ends on.
- **LIVE DATA BINDING** — engraving geometry is deterministic from the element id (a seal is a
  drawing, not a reading); **discovery state** is the live part — hidden / sensed / known per
  `journey_save.json` (A-075).
- **FIDELITY GATE** — closeout against the ten cuts. **G-1**: a stranger must be able to match
  each engraving to its cut without the caption — if two seeds' engravings are confusable, the
  seed spread is too narrow, which is a form fix.
- **DEPENDS ON** — A-071.

---

**A-073 · THE AXIS AND PRINCIPLE ENGRAVINGS — THE BRANCH, THE MESH** — `FLAT-UI` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `B1_axis_principle_seals.png` (five pentagon axis seals + three hexagon
  principle seals, scientific heraldry, each citing the real code file that proved it; the sheet's
  own title block states `LINE WEIGHT: 0.18mm`) · cuts `el_axis.*.png`, `el_pr.*.png` · **E8 §6.4
  names this sheet as the fourth first-application target and the hardest G-6.**
- **AEA CONCEPT SERVED** — PATH · MULTIPLICITY · ABSTRACTION · PROMPTING · ASYNC; EMERGENCE OVER
  IMPOSITION · RESTORABLE COHERENCE · OPERATOR-OBSERVABLE TIME.
- **TECHNIQUE** — built: axes engrave THE BRANCH (base node → trunk → apex, branch pairs to
  satellites; the accent is base → one jog → apex cap, one continuous path, one mark); principles
  engrave THE MESH (nodes on two rings, chords between them, one live node).
- **LIVE DATA BINDING** — the proof line under each seal is the real one (`swarm.py · 8 roles
  coordinated`, `test_resilient.py · 429s rerouted`, `tracelog.py DAG`). Where a proof is
  `PARTIAL`, the seal says PARTIAL — it does not round up.
- **FIDELITY GATE** — **G-6 is the binding gate for this ticket** (E8 §6.4): at delivered codex
  size the designation must stay ≥ 0.9% of frame width or it has become texture, and a designation
  is never allowed to be texture. Fails to scale and hierarchy work, never to a tooltip.
- **DEPENDS ON** — A-071.

---

**A-074 · THE VERB, MECHANIC AND OP ENGRAVINGS — THE RELAY, THE LATTICE, THE DIAL** — `FLAT-UI` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `B3_verb_mechanic_op_seals.png` (three triangles, four squares, four
  diamonds) · cuts `el_verb.*.png`, `el_mech.*.png`, `el_op.*.png`.
- **AEA CONCEPT SERVED** — COMPOSE · PROPAGATE · OBSERVE; CRYSTALLIZE · FLEXIBILIZE ·
  SELF-VERSION · CEILING-DETECT; DESIGN · TIME · SHIP · LEARN.
- **TECHNIQUE** — built: verbs engrave THE RELAY (corner nodes, a dashed route, one arrival ring
  as the accent); mechanics engrave THE LATTICE (a bracketed field with dashed lanes and end
  nodes, arms staying four ticks and never closing into a rectangle, a dense terminal-texture
  ruler as evidence, the spine column as the one accent); ops engrave THE DIAL (a ticked ring, a
  pointer, and **the arc actually swept** as the accent).
- **LIVE DATA BINDING** — `op.design` and `op.time` carry `PARTIAL` proofs today and must render
  as partial: DESIGN lands with `think()` (D1) and TIME needs its per-tick stamps (T-045). Neither
  seal may present as complete before its second leg exists.
- **FIDELITY GATE** — closeout against the eleven cuts. **G-5**: the mechanics' ruler is terminal
  texture used as evidence (E8 E-5); if its glyphs are not real strings it is greeble and is cut.
- **DEPENDS ON** — A-071, T-045.

---

**A-075 · THE THREE GLYPH STATES — HIDDEN / SENSED / KNOWN** — `FLAT-UI` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `A4_map_glyphs_seals.png` (the six glyphs in three states: hidden dotted,
  sensed dashed, known solid amber) · `D2` quadrant R-D strip 1 (MAP GLYPH: hidden → sensed →
  known, five frames, amber only in the last) · cuts `game/ref/mg_*.png` (six shapes).
- **AEA CONCEPT SERVED** — the discovery mechanic itself, and A11's thesis: **amber is a variable,
  and the variable is UNDERSTANDING.** The ink ratio of the map is a save file.
- **TECHNIQUE** — built: one dash vocabulary across all six shapes (which is why A-071 draws every
  family as a path). HIDDEN is **not drawn at all** on the sheet; in the map it is the dotted
  placeholder that says a slot exists. SENSED is outline only, dashed, labelled UNCHARTED, no
  fill. KNOWN is solid, amber, named, and connected by links to other known glyphs.
- **LIVE DATA BINDING** — state ← `journey_save.json` discovery (missions' `discovers` lists +
  real `tried[]` model encounters). A glyph never advances on anything but a real discovery event.
- **FIDELITY GATE** — **G-3 two-sided across the save**: an early frame with many KNOWN glyphs is
  a bug in the save read, not a lucky player. **G-1**: the three states must be distinguishable at
  map zoom 0.8, the bottom of the sanctioned range (T-034).
- **DEPENDS ON** — A-071, T-032.

---

**A-076 · THE SIX DOCTRINE PLATES** — `FLAT-UI` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `B4_doctrine_plates.png` (six circular doctrine diagrams, each a small
  wiring schematic with its law and evidence inscribed: THE SOLO LAW — one node, a council crossed
  out · THE DIVERSE COUNCIL — three unlike nodes voting into one · THE LONE VERIFIER RISK — a
  single judge with a fracture · THE GENETIC RELAY — a capsule down a chain of five · THE
  RAMIFICATION — a branching tree with depth caps · THE CRYSTAL PATH — a searched web collapsing
  into one route).
- **AEA CONCEPT SERVED** — `doctrines[]` in `aea_elements.js`: measured laws, not invented ones —
  and the `evidence` string on each is the whole point (`measured · grid experiments v2–v4`,
  `proven · relay.py: 5 distinct models, 2/2 handoffs`).
- **TECHNIQUE** — SVG in the seal press's vocabulary but at plate scale: circular frame, wiring
  schematic in structure ink, the law inscribed beneath, the evidence line beneath that in the
  smallest legal type. The crossed-out council in THE SOLO LAW is drawn with the same dash
  vocabulary as a SENSED glyph — negation is a line state, never a red X (there is no red).
- **LIVE DATA BINDING** — two-state per T-039: `READ` until `earnedBy` is satisfied, then
  `EARNED`. **Amber only on EARNED.** `doc.relay`, `doc.verifier`, `doc.swarm` and `doc.path` are
  `locked:true` in the data and must render locked until their forge lands; `doc.relay` stays READ
  until the relay forge exists, and nothing already shipped regresses.
- **FIDELITY GATE** — **G-5**: the evidence line is the plate's reason to exist; a doctrine plate
  without its real evidence string is a poster. **G-3**: four of six carry zero amber today, and
  that is the correct current render.
- **DEPENDS ON** — A-071, T-039.

---

**A-077 · THE CONCENTRIC MAP SCREEN** — `FLAT-UI` · `L` · `[BUILT, incomplete]`
- **STYLE REFERENCE** — `S5_concentric_map.png` (five rings of glyphs around a lit core; known
  glyphs amber and connected, unknown dim; "what is not known, sleeps") · geometry is authored
  data: `AEA.rings[]`, viewBox 1000, core r70, rings 150 / 250 / 360 / 470.
- **AEA CONCEPT SERVED** — all 29 elements at once — the curriculum as a place. Ring 3 holds three
  arc families (verbs = triangles, mechanics = squares, ops = diamonds) and mechanics discover
  **with** their seed (3 / 4 / 5 / 7).
- **TECHNIQUE** — SVG, 29 nodes, links drawn only once the mission named in `AEA.links[].by`
  completes. Owed polish (T-034): wheel zoom 0.8–2.5 **shipping with its hint**, link
  draw-on-learn choreography, open bloom, CARTOGRAPHY UPDATE materialisation, hover label, FACTS
  counter.
- **LIVE DATA BINDING** — discovery ← `journey_save.json`; station chips E / U / USE / OWN amber
  **only when live state says reached** (T-033); `@partial` renders as reduced-weight structure
  outline (T-032); the boot census diff renders organs in `/state` that are absent from
  `window.AEA` as UNCHARTED SIGNAL markers (T-035).
- **FIDELITY GATE** — **G-6**: 29 labelled nodes at the delivered screen size, judged at 0.8 zoom
  and at 1.0, no zooming to judge. **G-3**: the map is the clearest instance of the census-as-save
  file — both an early and a late frame must be recorded or the gate has not run.
- **DEPENDS ON** — A-075, T-032, T-033, T-034, T-035.

---

### 4.2 THE HUD — THE FOUR CORNERS — A-078 … A-081

Screen furniture lives in the four corners only, never the centre; the centre of the frame is
always the world (`bundle_02/03_TECHNICAL_TARGETS.md` §4). `R3_05_gameplay_screen.png` is the
composed reference and it is exact: mission line top-left, LIVE MEASUREMENTS top-right,
PROBE / VELOCITY plus event log bottom-left, LEYBER / PRESENCE bottom-right, a frame ID at the
bottom edge. `D2` quadrant R-A is the second, warmer composition of the same layout with a key-hint
strip along the bottom centre.

---

**A-078 · HUD TOP-LEFT — THE MISSION LINE** — `FLAT-UI` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `R3_05_gameplay_screen.png` top-left cluster: `M1.4 · THE HONEST LINK` /
  `do: route one live packet through the bench` / `prove: trace receipt appended` /
  `status: RUNNING` — status is the **only** amber word in the cluster · `D2` R-A top-left
  (`MISSION` / `OBJECTIVE` / `STATUS` with a corner-bracket frame).
- **AEA CONCEPT SERVED** — `seed.2` SHARP OBJECTIVE — every task carries a falsifiable scorer, and
  the mission line is where the player reads what will be scored **before** acting.
- **TECHNIQUE** — DOM in the panel type law, corner brackets only, `drift`-free (no parallax on
  screen furniture). Three fixed rows: do / prove / status. Bracket and hairline **draw in** on
  open (T-068), and that choreography is off under `prefers-reduced-motion`.
- **LIVE DATA BINDING** — mission id, `do` and `prove` strings ← `missions.js`; `status` ←
  the real assert engine's current state, never a UI guess. A retroactive listener may complete a
  mission the player already satisfied (T-015), and the line must show that honestly rather than
  re-running it.
- **FIDELITY GATE** — **G-3**: exactly one amber word. **G-5**: `prove:` names a real assert; a
  mission whose proof clause is prose fails this gate at authoring time, not at render time.
- **DEPENDS ON** — T-015.

---

**A-079 · HUD TOP-RIGHT — LIVE MEASUREMENTS** — `FLAT-UI` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `R3_05_gameplay_screen.png` top-right: `LIVE MEASUREMENTS` / `RPM 24 / 60`
  / `RX 3.42 s` / `LOAD 0.61` / `FOG 0.011` / `ZONE PRIVATE` — five rows, all cold · `D2` R-A
  top-right (`SYSTEM LINK`: FPS / TICKS-s / CPU LOAD / BATTERY / TEMP / MEM).
- **AEA CONCEPT SERVED** — `verb.observe` — "meter telemetry + trace: the state is visible", and
  `op.time`.
- **TECHNIQUE** — DOM rows, right-aligned values, every value through `put()`. Row count is fixed;
  a row with no reading prints its dash shape and keeps its place, because a disappearing row
  teaches that the measurement stopped mattering rather than stopped being available.
- **LIVE DATA BINDING** — `RPM` ← `/state.energy.plants[].rpm_now / rpm_cap` for the current
  carrier (the fraction, not a window count — the fraction is what `/state` actually exposes);
  `RX` ← real elapsed on the run in flight; `LOAD` ← the live load fraction; `FOG` ← the engine's
  actual `FogExp2` density, which is a save value and therefore legitimately a measurement;
  `ZONE` ← the construct's declared zone. **Uncapped carrier ⇒ `RPM 24 / UNCAPPED`, never a
  fabricated ceiling.**
- **FIDELITY GATE** — **G-5**: five rows, five real sources, checked one by one — this is the
  single easiest place in the game to smuggle in a number nobody sourced. **G-6**: values readable
  at 1440×900 without leaning in.
- **DEPENDS ON** — A-063, T-030.

---

**A-080 · HUD BOTTOM-LEFT — VELOCITY AND THE EVENT LOG** — `FLAT-UI` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `R3_05_gameplay_screen.png` bottom-left: `PROBE / VELOCITY` / `V 08.4 m/s`
  / `ALT 06.1 m` / `HDG 271.4°` then two timestamped log lines (`[22:14:05] packet dispatched`,
  `[22:14:07] watcher awaiting`) · `D2` R-A bottom-left (a circular `VEL 36.4 m/s` dial + a
  four-line `EVENT LOG` with `ok` status column).
- **AEA CONCEPT SERVED** — `pr.time` OPERATOR-OBSERVABLE TIME — a full, append-only timeline
  anyone can audit, in its smallest possible form.
- **TECHNIQUE** — DOM; the velocity dial is a small concentric SVG on the AEA radii ratios (E8 E-8
  — the hot mark lands on a ring); the log is exactly four lines, oldest scrolling out, timestamps
  in the entity's own clock. **Receipts, never tooltips** — the log is where the game tells the
  truth about what just happened.
- **LIVE DATA BINDING** — `V` / `ALT` / `HDG` ← the probe's real transform (these are the game's
  own physics and are therefore legitimately its own measurements, and the panel says so). Log
  lines ← real events: `/events` arrivals, run receipts from `/api/construct/run`, HADES verdicts.
  **No line is written by the UI for flavour.**
- **FIDELITY GATE** — **G-5**: every log line traces to an event row. **G-4**: the dial is the one
  circular element in the corner furniture and must hold the hairline ratio; a thick dial is the
  fastest "2003 menu" read in the frame.
- **DEPENDS ON** — A-086.

---

**A-081 · HUD BOTTOM-RIGHT — LEYBER PRESENCE** — `FLAT-UI` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `R3_05_gameplay_screen.png` bottom-right: `LEYBER / PRESENCE` — a
  three-ring concentric emblem with a **hexagon** core, beside four rows `STATE` / `MAPPED 11/29` /
  `WATCH HOLD` / `VOICE QUIET`; the hexagon core is the frame's second amber mark · `D2` R-A
  bottom-right (`LEYBER PRESENCE / ACTIVE`, a concentric reticle with a hot centre).
- **AEA CONCEPT SERVED** — the entity's own presence: `seed.6` SELF-MODEL reporting outward, and
  `pr.emergence` — there is no central controller, so presence is a reading, not a status light.
- **TECHNIQUE** — SVG concentric emblem on the AEA radii, hexagon core (principles are hexagons —
  the shape is a citation, not a decoration); four fixed rows in the panel type law. Carrier
  interlock: DO verbs grey out pre-click while presence is LOST (T-036).
- **LIVE DATA BINDING** — `MAPPED n/29` ← real discovery count from `journey_save.json`;
  `WATCH` ← live `/state.trust` / HADES posture; `VOICE` ← `talk_state.json`; presence itself ←
  whether `/state` is answering at all. **CARRIER LOST is a first-class state** (A-095), not a
  frozen last-good reading, and the hum ducks rather than alarms (T-075).
- **FIDELITY GATE** — **G-3**: the hexagon core is one of the two or three amber marks the scene
  budget permits; if presence is LOST it is **cold**, and a cold presence emblem in a dark frame
  is the correct, unsettling art. **G-7**: a stranger must read this corner as "the entity is
  here" without a legend.
- **DEPENDS ON** — A-095, T-036, T-075.

---

### 4.3 THE BENCH PLATE — FOUR STATES — A-082 … A-085

`D2_quad_screen_bench_plants_states_v2.png` quadrant R-B is the spec, drawn as four stacked panels
of the **same** plate: two node chips on a horizontal wire, a task card above, a run affordance
below, and a four-line BENCH LOG at the right of every state. `S4_the_bench.png` is the in-world
staging. **Amber appears ONLY in states 2 and 3, and only on the live element** — that sentence is
the acceptance criterion for all four tickets.

The plate is `[BUILT]` in `game/js/bench.js` (compose grammar, run trace, located failure, `/state`
meter). These four tickets are per-state fidelity closeouts plus the named gaps.

---

**A-082 · BENCH PLATE — STATE 1: COMPOSE** — `FLAT-UI` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 1 (COMPOSE: *place parts · define task · prepare
  run*; two chips `NODE-A socket` and `NODE-B relay` seated on a cold wire with empty ports
  beyond; TASK CARD above with `verify socket link / timeout < 10.0s / retries < 3`;
  `>> RUN [ENTER]` affordance below; BENCH LOG showing only dash rows).
- **AEA CONCEPT SERVED** — `verb.compose` — assemble subtask results into one coherent whole. The
  game's core creative act, at rest.
- **TECHNIQUE** — built: gap list rendered in spine order with the cursor walking that list;
  interleave `gap(0) mid[0] gap(1) mid[1] …` and only ghost-legal gaps render; seating closes the
  wire by redrawing hairlines left-to-right over 180 ms; right-click is UNSEAT grammar plate-wide,
  never the browser menu.
- **LIVE DATA BINDING** — chip rows mirror `modules.json` v0 and **each names the REAL entry point
  it wraps**; the task is the one curated bench task v0 with its tier floor pinned to
  local/keyless; the zone strip ships for TAP only, because TAP is the one writable (the zone
  law).
- **FIDELITY GATE** — **G-3**: **zero amber in this state.** A compose screen with a warm wire has
  already told the player the run succeeded. **G-5**: the four dash rows in the log are dashes,
  not zeroes.
- **DEPENDS ON** — T-001.

---

**A-083 · BENCH PLATE — STATE 2: RUN** — `FLAT-UI` · `L` · `[BUILT]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 2 (RUN: *execute flow · watch packet · measure
  live*; one amber packet on the wire between the chips; `ELAPSED 00:03.447` counting; log rows
  `run.begin` / `packet.a` / `packet.b` / `receipt.01` with the receipt amber) ·
  `R3_05_gameplay_screen.png` bottom-centre (`COMPOSITION PLATE / RUN 02147`, the packet mid-wire,
  caption `TRACE 01 · RX 3.42 s · MODEL SR-41 · MEM 3 RECALLED`) · `S4_the_bench.png`.
- **AEA CONCEPT SERVED** — `verb.propagate` — the honesty node: a live trace of task → node →
  output. The game's autograph, and the one thing in this world that moves light along a line.
- **TECHNIQUE** — built: packet stops are measured from the **locked** layout (entry trunk, each
  chip centre, exit) and the packet **advances only on real trace rows — never interpolated**.
  In RUN all non-exit input is refused by the lock line (flare 120 ms, decay). Reroute marks
  render a fall-through on the draw as **resilience**, not failure.
- **LIVE DATA BINDING** — `POST /api/construct/run` returns a run id immediately and the run
  executes in its own thread; the plate polls `GET /api/construct/run?id=`. Every fetch is
  abortable and timed out. A carrier refusal is printed **verbatim** (the zone/trust law working);
  a wrong answer means **no run exists** — the plate unlocks and the receipt stands.
- **FIDELITY GATE** — **G-3**: one packet, one live element, and the receipt is the only other
  amber. **G-1** of motion (E8 §5.3): the packet's travel must read as *latency*, not as
  animation — if it moves smoothly while the trace is stalled, the interpolation ban was broken.
- **DEPENDS ON** — T-001, T-002, A-086.

---

**A-084 · BENCH PLATE — STATE 3: HALT** — `FLAT-UI` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 3 (HALT: *break occurs · mark exactly ·
  acknowledge*; the wire severed and kinked at the break with an annotation bracket reading
  `BREAK @ 1.24 m / LINK-07`; log rows ending `00:01.241 LINK-07 FAIL` / `run.halt`) ·
  `S7_honest_failure.png` (the severed chain link, `CONDUCTIVITY: OPEN · INTEGRITY: 0% ·
  IMPACT: CONTAINED · STATUS: ACKNOWLEDGED`; "failure is information. not an exception.").
- **AEA CONCEPT SERVED** — `seed.4` FLEXIBILIZE and `pr.coherence` — a failure reroutes and the
  system still completes; where it cannot, the failure is **located**, named and acknowledged.
- **TECHNIQUE** — built: the packet stops **on the wire where it died** and cools in place over
  900 ms; everything eases to 0.35 while **the failing name holds at 1.0** (failure is amber
  withdrawn from everything else, not amber added); the failed seat keeps a structure tick for the
  visit; the frame **holds** until any input, with no sound but the hum — silence is the failure
  sting. A terminal failure with no located link row prints the cause the harness named, not an
  invented wire fault.
- **LIVE DATA BINDING** — break position ← the real trace row that failed; the annotation carries
  the real link id and the real elapsed. A scorer miss is a located fail at the tail; **no scorer
  seated** means the run ran and nothing measured it, and the control line said so in advance.
- **FIDELITY GATE** — **G-2**: no red exists; a halt that reads as an alarm has broken the law.
  **G-5**: the annotation's three facts are all real. **G-7**: a stranger must be able to point at
  *where* it broke — that is the entire design intent of this state.
- **DEPENDS ON** — T-001, A-094.

---

**A-085 · BENCH PLATE — STATE 4: RECORD** — `FLAT-UI` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 4 (RECORD: *run complete · result recorded · cool
  to idle*; the wire whole and cold again; footer `RESULT: PASS · TIME: 00:07.892 ·
  BEST: 00:07.214`; log rows `receipt.final` / `run.end` / `recorded.ok`, **all cold**).
- **AEA CONCEPT SERVED** — `op.learn` (a run's result measurably improves the next) · `seed.2`
  SHARP OBJECTIVE — the measured result is the only reward this game gives.
- **TECHNIQUE** — built: everything cools back to structure ink; A CONSTRUCT'S FIRST RUN is the
  one sanctioned ritual and fires **once per construct**, never again. The result line carries
  last and best; a new best is stated, not celebrated.
- **LIVE DATA BINDING** — `TIME` ← the real measured elapsed; `BEST` ← the persisted personal best
  from the record book (T-004). **Both real or both dashed.** Multi-objective records
  (speed / cost / reliability / privacy) mean a run can be a best on one axis and not another, and
  the plate must say which.
- **FIDELITY GATE** — **G-3**: **zero amber in this state** — the sheet is explicit that amber
  lives only in states 2 and 3. A record screen that glows converts a measurement into a
  congratulation, which is the one thing this game refuses to do.
- **DEPENDS ON** — T-001, T-004.

---

## 5. CLASS: EFFECT — atmosphere, light transport, and the honest negatives

Doctrine: **TIER 3, never modelled** (E5 §3). The field, the sky, the fog, the depth bands, the
light pillars, the reflections, the dust and the embers stay code forever; no amount of concept
fidelity changes that, because they are camera and atmosphere. A11 §6's juice budget binds all of
them: nothing here may become a second attention magnet at idle.

Two tickets in this section (A-087, A-088) are **laws rather than objects**. They are written
fourth and obeyed first: every ticket above them cites them.

---

**A-086 · THE LIVE TRACE PACKET** — `EFFECT` · `L` · `[BUILT, partial]`
- **STYLE REFERENCE** — `bundle_02/02_VISUAL_LAW.md` §4.2, owned motif 2: *"a single amber packet
  travelling along a thin wire. The game's autograph. Nothing else in this world moves light along
  a line."* · `D2` quadrant R-D strip 5 (TRACE WIRE: dark → packet travelling → severed at a link
  → cooled) · `R3_05_gameplay_screen.png` bottom-centre · `S4_the_bench.png`.
- **AEA CONCEPT SERVED** — `verb.propagate` — the honesty node. This effect **is** the AEA's
  central claim rendered as light: you can see who did what, live.
- **TECHNIQUE** — on the plate: DOM/SVG, position driven by real trace rows. In the world: merged
  `TubeGeometry` conduits with `uv.x` read as **arclength**, and the packet as a narrow moving
  window in the emissive term (E6 §1.7 / Move 8 — the trace ships as gradient light, not as a
  uniform-opacity sprite). Idle wires are **structure ink only**; amber appears solely under a
  real trace and its 600–900 ms decay (E2 Move 7, binding).
- **LIVE DATA BINDING** — position advances **only on real trace rows and is never interpolated**
  — the packet's speed is literally the entity's latency, which is why this effect teaches
  something no animation could. Source: the run's trace rows (`tracelog.py` / the
  `/api/construct/run` row) and `events.jsonl` for world conduits.
- **FIDELITY GATE** — **G-3**: one packet per live route, and the frame census still binds.
  **G-1 of motion**: hold a recorded still of the packet mid-wire against the D2 strip 5 frame 2 —
  the packet must be a *segment with falloff*, not a dot, or Move 8 was not applied.
- **DEPENDS ON** — T-002, T-013.

---

**A-087 · THE AMBER ATTACK–DECAY LAW** — `EFFECT` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `bundle_02/03_TECHNICAL_TARGETS.md` §3: *IDLE `#d4a24c` at 35 percent ·
  FIRED `#ffb000` at full · a firing flares in 120 milliseconds and decays back over 600 to 900.
  **Nothing else animates.*** · `D2` quadrant R-D, every strip, where amber appears only in frames
  where the thing is genuinely working.
- **AEA CONCEPT SERVED** — A11's thesis: amber is a variable and the variable is UNDERSTANDING.
  This ticket is that thesis given a time constant.
- **TECHNIQUE** — one shared easing utility over `material.emissiveIntensity` (world) and one CSS
  custom-property transition (UI), both reading the same `EMISSIVE = { idle: 0.35, fired: 1.0 }`
  table already in `engine.js`. Tiers are **verified post-gamma and never re-tuned pre-gamma**
  (T-066's substrate). Under `prefers-reduced-motion` / `html.reduced-motion` the flare becomes an
  instant state change, never a removed state.
- **LIVE DATA BINDING** — a flare may only be triggered by a real event: a trace row, a verdict, a
  served request, a confirmed send. **There is no decorative flare in this game.** That is the
  whole ticket.
- **FIDELITY GATE** — **G-3 across the build**: this law is what makes every other object's census
  passable. It is verified by recording a 3-second still sequence during a real run and confirming
  no amber pixel changes outside a triggered window.
- **DEPENDS ON** — T-066.

---

**A-088 · BLOOM DISCIPLINE** — `EFFECT` · `M` · `[BUILT, contested]`
- **STYLE REFERENCE** — `bundle_02/02_VISUAL_LAW.md` §3 (*no bloom halos, no volumetric god-rays,
  no lens flares*) held against E8 §2 finding 3 (*every sheet clips: max value 1.000 on all nine
  while p99.9 is only 0.44–0.76 — there is always a tiny pure-hot core*).
- **AEA CONCEPT SERVED** — none directly; this ticket exists to stop the light from lying about
  how much is alive.
- **TECHNIQUE** — the composer chain is **locked**: `RenderPass` + `UnrealBloomPass(0.65, 0.4,
  0.5)` + the existing `FinalShader` (LinearToSRGB + interleaved-gradient-noise dither under
  1/255). Bloom re-tune is banned (A11 §6.2). The permitted work is entirely in the final pass:
  (a) reassert amber chroma in clipped highlights, (b) re-seat the void floor toward the measured
  `#010812`. The r128 law holds: composer targets are linear, so **the last pass does the sRGB
  encode**, and the sky `ShaderMaterial` inlines the same ACES curve as the renderer or the
  horizon seams.
- **LIVE DATA BINDING** — `NONE`, and the reason matters: bloom is a camera property. Binding glow
  to data would double-count — the emissive tier already carries the datum, and bloom would
  silently amplify it.
- **FIDELITY GATE** — **G-2**: frame-wide void mean must sit in `#010812`–`#050a10` and **never**
  at `#0a1420` (E8 §2 finding 1: the bright end of the sanctioned band is for local gradient only);
  at least one pixel above 0.95. **T-066 is a live defect**: the probe core blooms to a white blob
  on real GPU, and a white core is amber's chroma destroyed — that is this gate failing today.
- **DEPENDS ON** — T-066, T-067. `[DECISION-LUIS]` E6 §1.12 — keep ACES plus the narrow palette
  guard, or remove ACES entirely and re-tune the sky shader with it. Requires an **on-hardware**
  A/B pair; swiftshader and headless are never the judge.

---

**A-089 · THE SCAN SWEEP** — `EFFECT` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 2 (the scan lens's concentric sensor ring
  with radial index ticks — the sweep's vocabulary is the lens's own face) ·
  `S5_concentric_map.png` (what a completed scan *becomes*: a glyph moving from SENSED to KNOWN).
- **AEA CONCEPT SERVED** — `verb.observe` · `seed.7` CEILING-DETECT — a scan is how the probe
  learns that something is there and that it does not yet understand it.
- **TECHNIQUE** — a single expanding ring on the ground plane, driven in the **existing** ground
  shader as a moving `mod(length(vWpos.xz - uOrigin), …)` band with a hard falloff — zero new
  geometry, zero new draw calls (the ground already does the ring trick). The sweep is one shot,
  it does not loop, and it leaves nothing behind but the discovery it caused. Scanlines are
  explicitly **not** this effect (T-069: scanlines earn their keep or step down).
- **LIVE DATA BINDING** — sweep radius ← the probe's real scan range; a hit is a real object in
  range, and a hit writes a real discovery to `journey_save.json` which the map then renders
  (T-035's census will catch anything the book missed). **A sweep that finds nothing renders as a
  sweep that found nothing** — no reassurance ping.
- **FIDELITY GATE** — **G-3**: the sweep is structure ink; only the *result* (a glyph reaching
  KNOWN) earns amber. **G-5**: an animated ring with no discovery behind it is decoration and is
  cut.
- **DEPENDS ON** — A-002, A-096, A-075.

---

**A-090 · FOG AND THE THREE DEPTH BANDS** — `EFFECT` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `S1_field_genesis.png` (near towers at full contrast, mid at ~40%, far as
  pure silhouette dissolving into a horizon the same colour as the fog) · `S9_the_city_revealed.png`
  · E8 E-6 (measured: the scene sheets are tonally **compressed** — cool-ink p99 lands at
  0.29–0.50 versus 0.42–0.64 on the plates — so scenes buy depth from *separation*, not range).
- **AEA CONCEPT SERVED** — narratively, the antagonist: A12 names FOG as the thing the player
  works against. Mechanically it serves `seed.7` — what you cannot yet resolve is your ceiling.
- **TECHNIQUE** — built: `FogExp2` with fog colour **==** clear colour == horizon base, density as
  a **live variable** (0.011 → 0.009 on `foundry_full`), plus per-district density/colour stepping
  at one lerp per frame. This is already beyond most titles and is protected, not replaced.
- **LIVE DATA BINDING** — density is a save value driven by real world-state progression, which is
  what makes fog with a job rather than fog as a filter. Starvation weather (T-063) dims the field
  strictly from live `/state`, inside the juice budget.
- **FIDELITY GATE** — **G-6 by greyscale**: a greyscale copy of any scene render must still show
  three distinct depths. If it does not, the fix is **fog and silhouette variety, never more
  geometry** (E5 §2). This is the single cheapest gate in the registry to run and the most often
  skipped.
- **DEPENDS ON** — T-063.

---

**A-091 · GROUND REFLECTIONS** — `EFFECT` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `S1_field_genesis.png` (a faint ground reflection under the lit thing —
  and **only** under the lit thing) · `S3_the_probe.png` (the pool of light on the ground beneath
  the probe).
- **AEA CONCEPT SERVED** — indirectly `seed.6` SELF-MODEL: the world shows a thing its own image,
  cheaply and only where something is alive.
- **TECHNIQUE** — built: clone the mesh, `scale.y = -1`, opacity ~0.15 — the sanctioned trick
  (E5 §2.5). **No planar reflection pass, no mirror render target**: both would double draw calls
  and would reflect things that are not lit, which is exactly the discipline the sheet keeps.
  Reflections exist under emissive objects only.
- **LIVE DATA BINDING** — a reflection exists **because** something is emitting; when the emissive
  tier drops to idle the reflection drops with it on the same attack-decay curve, so a reflection
  can never outlive the light that justified it.
- **FIDELITY GATE** — **G-3**: reflected amber counts toward the census — a reflection is not a
  free copy of the frame's light budget. If the census fails with reflections on, the reflection
  opacity comes down before any object is dimmed.
- **DEPENDS ON** — A-087.

---

**A-092 · DUST AND EMBERS** — `EFFECT` · `S` · `[BUILT]`
- **STYLE REFERENCE** — `S1_field_genesis.png` and `S3_the_probe.png` — the faint particulate that
  gives the void a volume. Held against `bundle_02/02_VISUAL_LAW.md` §6: **sprite-sheet particle
  sparkles are a banned tell.**
- **AEA CONCEPT SERVED** — `NONE` directly. This ticket exists to give the void material presence
  (E8 E-1: the darkness is a material, not a background) and it is the one effect permitted to
  serve no element.
- **TECHNIQUE** — built: two `Points` clouds (dust 800, embers 180) inside a total particle budget
  of 4 draw calls with the trail (90) and stars (1,200). Per-point size and alpha need a
  `ShaderMaterial` or an attribute plus `onBeforeCompile` — still one draw call. Points are
  structure ink; embers are the only ones permitted warmth, and only near a live source.
- **LIVE DATA BINDING** — **ember density scales with live activity** (T-071) — a busy entity
  throws more embers; an idle one throws almost none. Dust is ambient and binds to nothing, which
  is stated rather than hidden.
- **FIDELITY GATE** — **G-2**: no sparkle, no sprite twinkle, no additive flare — if a frozen
  frame shows star-shaped points, the banned tell shipped. **G-3**: embers count toward the amber
  census and are the first thing cut when a scene runs hot.
- **DEPENDS ON** — T-071.

---

**A-093 · DECAY AND ROT — THE SIX-STATE MATERIAL SYSTEM** — `EFFECT` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `D2` quadrant R-D strip 2 (MODEL-VESSEL: fresh → stable → drifting →
  cooling → rotting → dead, six frames, identical framing, the last frame a collapsed heap) ·
  `A2_specimen_rods.png` cells 4, 6 and 8 (DRIFTING, SLOW DECAY, ROTTING as drawn states).
- **AEA CONCEPT SERVED** — `seed.4` FLEXIBILIZE (kill a node mid-run — the route falls, the task
  completes) · `pr.coherence`. Decay is how the game teaches that the substrate is not reliable
  and that the architecture is what makes it survivable.
- **TECHNIQUE** — the six states are **material and geometry parameters on one mesh family**, not
  six meshes: vertex-colour value drop, progressive deterministic fracture displacement (the
  routine already in `artifacts.js`), shard separation at the base, and emissive tier withdrawal.
  **No hue shift at any state** — rot is form and value, never colour, because there is no colour
  available for it (two inks, absolute).
- **LIVE DATA BINDING** — states map to real measurements and to nothing else: FRESH / STABLE ←
  measured reliability with no cooling entry · DRIFTING ← reliability moved beyond a
  pre-registered band across two census runs · COOLING ← `consec_fail ≥ 3` and inside the 900 s
  cool window · ROTTING ← sustained failure · DEAD ← absent from the live catalog, which also
  raises the LOST SIGNAL tombstone (T-064) so a hole reads as fate rather than as a bug.
- **FIDELITY GATE** — **G-1 across the strip**: the six frames must be distinguishable in
  flat-black silhouette **in identical framing**, which is the sheet's own discipline. **G-2**: if
  a reviewer can name a colour for "rotten," the ticket failed.
- **DEPENDS ON** — A-016, T-040, T-064.

---

**A-094 · THE HALT BREAK MARK** — `EFFECT` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 3 (the wire severed and kinked with the annotation
  bracket `BREAK @ 1.24 m / LINK-07`) · `D2` R-D strip 5 frame 3 (TRACE WIRE severed at a link) ·
  `S7_honest_failure.png` (the integrity map ringing the fault; STATUS: ACKNOWLEDGED).
- **AEA CONCEPT SERVED** — `pr.coherence` RESTORABLE COHERENCE, and its refusal to hide: *"failure
  is information. not an exception."*
- **TECHNIQUE** — built on the plate; owed in the world. The mark is drawn **exactly where the
  break happened** — position derives from the failing trace row, never from a fixed
  "error location." The packet cools in place over 900 ms; the failing name holds at 1.0 while
  everything else eases to 0.35. The annotation bracket is corner ticks, never a box. The frame
  **holds** until input.
- **LIVE DATA BINDING** — break coordinate, link id and elapsed all come from the real trace. Where
  the harness named the cause but no link row exists, the mark is **not** drawn on the wire and the
  cause is printed instead — inventing a wire fault to have something to draw is the exact failure
  this ticket prevents.
- **FIDELITY GATE** — **G-7**: a stranger must point to where it broke. **G-2**: no red, no alarm
  colour, no shake. **G-5**: three real facts in the annotation or the annotation is cut.
- **DEPENDS ON** — A-086, T-002.

---

**A-095 · THE CARRIER-LOST BLACKOUT** — `EFFECT` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — the ROUND3 category 8 brief (*a CARRIER LOST field where every light has
  gone out and only structure remains*) · `A6_instrument_panels.png` cell 5 / `C4` cell 5 (the
  carrier-lost card) · `S7_honest_failure.png` for the acknowledgement grammar.
- **AEA CONCEPT SERVED** — the honesty law itself, at its most uncomfortable: when the game cannot
  see the entity, it says so and shows so. Nothing is preserved from the last good frame.
- **TECHNIQUE** — every emissive tier in the scene drops to zero on the attack-decay curve; the
  structure ink stays exactly where it is. **No overlay, no vignette, no red border** — the
  blackout is the absence of the thing that was earned, which is why it hurts. Audio: the core hum
  ducks .024 → .004 over 300 ms (T-075) — silence as signal, no alarm tone. Under a WebGL
  context-loss pair the same state is entered (E1 §3.1), so a GPU failure and an entity failure
  are honestly indistinguishable to the player, because to the player they are the same thing.
- **LIVE DATA BINDING** — raised when `/state` stops answering, when a fetch fails, or when a
  carrier reads `s === null` (distinguished from `s === 0` — T-030, without which a dead carrier
  can pass an observe). The card prints the real endpoint and the real time.
- **FIDELITY GATE** — **G-3**: amber census must read **zero** in a carrier-lost frame. Any
  surviving amber is a value the UI cached, and a cached value in a blackout is the single worst
  honesty violation available to this game. **G-1**: the frame must still show its three depth
  bands in structure ink alone.
- **DEPENDS ON** — A-067, A-087, T-030, T-075.

---

**A-096 · THE CONCENTRIC GROUND FIELD** — `EFFECT` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `S1_field_genesis.png` (concentric rings etched into the ground, radiating
  from the lit structure) · `S9_the_city_revealed.png` (the same rings become the district plots) ·
  `bundle_02/02_VISUAL_LAW.md` §4.1: the concentric field is **the sacred motif**.
- **AEA CONCEPT SERVED** — the AEA's own geometry, laid into the world's floor: the map's rings
  and the ground's rings are the same idea at two scales, which is why E8 E-8 can require every
  object and scene to carry the motif somewhere.
- **TECHNIQUE** — E6 §1.3 / E2 Move 1: extend the **existing** `buildGround()` `onBeforeCompile`
  injection from one anchor to N district anchors — concentric survey circles, radial hairlines,
  plot boundaries, plate seams, all on a snap-grid with conduit elbows at 45°. **Zero new
  geometry, zero new draw calls.** This ticket also kills E2 §4.2 offender 1 (`GridHelper(400, 80)`
  at 0.35 — the canonical placeholder floor currently shipping in every boot frame) and offender 4
  (the flat 1600×1600 single-albedo plane).
- **LIVE DATA BINDING** — anchor positions ← the real district/plant layout; ring radii ← `zone`
  bands. A plot exists for every plant in the registry and is **built** only if the plant is in
  `/state.energy.plants[]` — so the empty rings are the literal set of organs proven-not-wired.
- **FIDELITY GATE** — **G-1 of composition**: E6 §6 step 3 is explicit that the ground ships
  **before** any tower, because towers placed on a bare plane get re-tuned twice. Gate: the
  ground-only render must already read as a city plan from the play camera. **G-4**: radial
  hairlines at grazing angle are the worst aliasing case in the build — they hold the stroke ratio
  or they get a distance fade, never a thickening.
- **DEPENDS ON** — none. **This is the first world-geometry ticket and it blocks A-051.**

---

**A-097 · THE LIGHT PILLAR** — `EFFECT` · `S` · `[BUILT, needs Move 7]`
- **STYLE REFERENCE** — `S1_field_genesis.png` (one vertical light pillar over the single lit
  structure — "fifteen silent witnesses / one still speaks") · `S9_the_city_revealed.png` (the
  spire's beam at city scale).
- **AEA CONCEPT SERVED** — `axis.S` ASYNC / `/state.life` — the beam is uptime made visible: the
  entity is alive right now, unattended.
- **TECHNIQUE** — one additive cylinder, which is already built — and which E2 §4.2 offender 6
  names as a **uniform-opacity** additive cylinder, i.e. light with no falloff, which reads 2000s.
  The fix is Move 7's ramp: a vertical alpha ramp in the shader so the beam pools at the base and
  dissolves upward. One cylinder, one extra term, no new draw call.
- **LIVE DATA BINDING** — beam presence and height ← `life.alive_since` uptime; it exists because
  the entity is running, and it goes out when the entity sleeps. A beam over a dead entity would
  be the single most visible lie the world could tell.
- **FIDELITY GATE** — **G-3**: in the S1 composition this beam is most of the frame's permitted
  amber (S1 measures 21.98% of ink amber — the highest in the set — precisely because its whole
  subject is one beacon). **G-2**: the beam's core is allowed to be the >0.95 pixel; its falloff
  must not turn cream under ACES, which is A-088's contested clause landing here.
- **DEPENDS ON** — A-088.

---

**A-098 · THE PROBE TRAIL RIBBON** — `EFFECT` · `S` · `[BUILT, needs Move 10]`
- **STYLE REFERENCE** — `R3_05_gameplay_screen.png` (the probe low in frame trailing a thin line
  of light) · `D2` quadrant R-A (the trail curving across the concentric ground) ·
  `bundle_02/03_TECHNICAL_TARGETS.md` §4 (*the probe sits low in frame, roughly the lower third,
  trailing a thin line of light*).
- **AEA CONCEPT SERVED** — `pr.time` OPERATOR-OBSERVABLE TIME, at its most personal: the trail is
  the player's own append-only timeline, drawn behind them.
- **TECHNIQUE** — Move 10: the existing 90-point `Points` trail gains per-point size and alpha
  (attribute + `onBeforeCompile`), fading to nothing — a ribbon rather than a dotted line. Still
  one draw call. The trail is the **one** motion element permitted at idle, because it is the
  player's own movement and therefore never a competing attention magnet.
- **LIVE DATA BINDING** — the trail is the probe's real path. `NONE` beyond that, stated: it
  measures nothing about the entity, only about the player, and it is labelled as such in the
  codex.
- **FIDELITY GATE** — **G-3**: the trail is warm at most, never hot — the player is not a live
  measurement. **G-4**: at the sheet's proportion the trail is a *hairline*; a thick trail is the
  most common way this frame stops looking like the sheet.
- **DEPENDS ON** — A-087.

---

**A-099 · PLANT LOAD STATES — IDLE / DRAWING / AT LIMIT / BROWNED OUT / RECOVERING** — `EFFECT` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `D2` quadrant R-D strip 3 (PLANT UNDER LOAD, five frames, identical
  framing, the window field filling and then going dark) ·
  `bundle_02/03_TECHNICAL_TARGETS.md` §3.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE and its honest ceiling · `seed.7` CEILING-DETECT —
  a browned-out plant is a ceiling the player can see from a kilometre away.
- **TECHNIQUE** — E6 §1.1, the highest-leverage move in the whole pipeline and it costs **zero
  draw calls**: a procedural window field injected into the mass material via `onBeforeCompile` —
  `cell = floor(vec2(facadeU, vWpos.y) * vec2(COLS, ROWS))`, `lit = step(hash(cell + seed),
  uLoad)`, written **only** into `totalEmissiveRadiance` with `INK.warm` / `INK.hot`. ~35 lines of
  GLSL. This ticket **deletes** E2 §4.2 offender 2 (the hand-placed window quads and the
  random-window `CanvasTexture` at repeat 2×1.2 — a texture pretending to be data in a game whose
  law is data) and E6 §1.1's hand-placed literal coordinate array in the same session.
- **LIVE DATA BINDING** — lit fraction ← `rpm_now / rpm_cap`. **Uncapped plant ⇒ literal count:
  one window per request in the last 60 s, no denominator invented.** AT LIMIT ← the real cap
  reached; BROWNED OUT ← a live throttle entry in `grid_state.json` with `until > now`;
  RECOVERING ← throttle expired, calls resuming. Far districts use the `Points` window cloud
  refreshed on the same poll, and **an impostor never bakes amber** (E6 §3.4 clause 1) — so a
  stale card showing lit windows for an offline plant is unreachable by construction.
- **FIDELITY GATE** — **G-3 is the whole ticket**: the lit count is a pure function of a live
  value, which is what makes the amber census auditable rather than aesthetic. Gate: sample the
  frame, count amber, and confirm the count moves when and only when `rpm_now` moves.
  **G-5**: the plant's panel prints the number the geometry was built from (E6 §4.12) or the
  geometry is decoration.
- **DEPENDS ON** — A-051, A-057.

---

## 6. CLASS: INTERACTION — the eight verbs, as assets

An interaction is the seam between an asset and a mechanic: the camera move, the input grammar,
the choreography, the sound, and the refusal. It is ticketed here because the *feel* of docking is
an art deliverable with a style reference, not an emergent property of two other tickets.

Standing law for all eight: **respect `prefers-reduced-motion`, `html.reduced-motion` and the
`LB.motionOn` equivalent on everything**; a choreography that cannot be turned off is not shipped.
Second law: **receipts, never tooltips** — an interaction reports what happened in the log, in the
entity's own words, and never in a hover bubble.

---

**A-100 · DOCK** — `INTERACTION` · `M` · `[BUILT, partial]`
- **STYLE REFERENCE** — `S4_the_bench.png` (the probe met with the plate) · `D2` quadrant R-A
  key-hint strip (`[E] INTERACT`) · the dock camera is already specified in `bench.js`: a fixed
  high oblique over the slab with the foundry row held in the middle distance.
- **AEA CONCEPT SERVED** — `seed.1` SUBSTRATE + `seed.9` BOUNDARY — docking is the moment the auth
  channel either resolves or refuses, in the world rather than in a menu.
- **TECHNIQUE** — a camera tween from the play camera to the fixed dock camera (eased, ~600 ms,
  instant under reduced motion), the probe's PH-03 coupler aligning to the kiosk's hex head, and
  the plate's brackets and hairlines **drawing in** on arrival (T-068). Coach-mark on first dock
  only, one time, diegetic (T-080). Dock-from-map is the one affordance that closes most of the
  accessibility gap and ships with the screen-reader projection (T-081).
- **LIVE DATA BINDING** — the dock either resolves against a real plant socket or is refused, and
  a refusal prints the carrier's own words verbatim. There is no "docking…" state that is not a
  real handshake.
- **FIDELITY GATE** — **G-1** on the arrival frame against `S4_the_bench.png`: composition,
  probe placement in the lower third, foundry row at mid depth. **G-6**: the plate must be
  readable at the dock camera's actual distance without a second zoom step.
- **DEPENDS ON** — A-001, A-059, T-080, T-081.

---

**A-101 · COMPOSE** — `INTERACTION` · `L` · `[BUILT]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 1 · `B5_constructs.png` (the port / wire / packet
  grammar a composed machine must obey).
- **AEA CONCEPT SERVED** — `verb.compose`. This is the core creative act of the entire game: the
  player's collection of assistants is their character.
- **TECHNIQUE** — built: the gap-and-chip grammar with a cursor that walks the rendered gap list;
  seating closes the wire with a 180 ms left-to-right hairline redraw; **right-click is UNSEAT
  grammar plate-wide**, never the browser menu; only ghost-legal gaps render, so an illegal
  composition is unreachable rather than rejected. Per-rung part pools keep the climb curated
  (5 → 7 → 12 → 14 → 17, T-003) — never all elements at once.
- **LIVE DATA BINDING** — parts are module ids from `modules.json`, each naming the real entry
  point it wraps; zone is REQUIRED in construct-spec v0.1.0; the validator's failure message
  **names the violated clause** (T-056), which is what makes a refusal teach instead of scold.
- **FIDELITY GATE** — **G-3**: compose is cold, always (A-082). **G-7**: a stranger must be able
  to seat a part without instruction — if they cannot find the gap, the gap's affordance is
  under-drawn, and the fix is the plate's line hierarchy, not a label.
- **DEPENDS ON** — A-082, T-001, T-003, T-056.

---

**A-102 · RUN** — `INTERACTION` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 2 (`>> RUN [ENTER]` affordance, ELAPSED counting,
  receipts landing) · `R3_05_gameplay_screen.png` (a run in flight seen from the world).
- **AEA CONCEPT SERVED** — `op.ship` at bench scale — a run must produce a real, measured result
  or it did not happen · `verb.propagate` for the trace it draws.
- **TECHNIQUE** — built: ENTER fires the terminal's primary footer verb (T-082); in RUN all
  non-exit input is refused by the lock line with a 120 ms flare and decay — **the refusal is
  drawn**, so the player learns the state rather than wondering why nothing happened. Audio is
  WebAudio oscillators only, zero assets; speak ticks are 30 ms 340 Hz triangles capped at 12/s
  (T-074), keyed off the same reduced-motion branch as typing.
- **LIVE DATA BINDING** — `POST /api/construct/run` returns a run id immediately; the run executes
  in its own thread; the plate polls by id with every fetch abortable and timed out. The elapsed
  readout is real elapsed. A run against a dead carrier does not produce a fake result — it
  produces CARRIER LOST (A-095).
- **FIDELITY GATE** — **G-5**: every receipt line is a real event. **G-3**: exactly one packet and
  one receipt colour-bearing element at a time.
- **DEPENDS ON** — A-083, A-086, T-001.

---

**A-103 · HALT** — `INTERACTION` · `M` · `[BUILT]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 3 · `S7_honest_failure.png` ·
  `B8_governance.png` (the HALT seal).
- **AEA CONCEPT SERVED** — `seed.4` FLEXIBILIZE · `pr.coherence` · and the governance HALT: the
  membrane test that breaches **halts**, it does not warn.
- **TECHNIQUE** — built: the frame **holds** until any input, with no sound but the hum. Silence
  is the sting. Any input returns to COMPOSE; the held frame ends and the structure tick on the
  failed seat survives, so the settled story cools without erasing what happened.
- **LIVE DATA BINDING** — a halt is raised by a real failing trace row, a real breach, or a real
  refusal. The HALT verb is also legal as an entity action in the end-game (the DGM grant gate
  reads `trust.py` live; the game **detects** the grant, it never performs it).
- **FIDELITY GATE** — **G-2**: no red, no shake, no alarm. **G-7**: a stranger must correctly say
  *what* halted and *where* — if they can only say "something broke," the break mark (A-094) is
  the failing dependency, not this ticket.
- **DEPENDS ON** — A-084, A-094.

---

**A-104 · RECORD** — `INTERACTION` · `M` · `[BUILT, partial]`
- **STYLE REFERENCE** — `D2` quadrant R-B panel 4 (`RESULT: PASS · TIME · BEST`) ·
  `A6_instrument_panels.png` cell 2 / `C4` cell 2 (the record book strip).
- **AEA CONCEPT SERVED** — `op.learn` · `seed.2` SHARP OBJECTIVE. **The measured result is the
  only reward this game gives** — there is no XP, no currency, no confetti.
- **TECHNIQUE** — built at the plate; owed at the book (T-004): multi-objective per-construct
  records across speed / cost / reliability / privacy, with personal bests. A new best is
  **stated**, not celebrated — one line, cold, permanent. The one sanctioned display-scale moment
  in the whole game is ACT COMPLETION (Move 11), and a record is not it.
- **LIVE DATA BINDING** — every recorded value is a real measurement written to the journey save;
  pre-registration plumbing (T-060) writes bars, seeds and margins **before** any scored run, so a
  record cannot be retro-fitted to a result.
- **FIDELITY GATE** — **G-3**: zero amber (A-085). **G-5**: last and best are both real or both
  dashed — a best with no prior run is a fabricated history.
- **DEPENDS ON** — A-085, T-004, T-060.

---

**A-105 · SCAN** — `INTERACTION` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `B7_probe_hardware.png` cell 2 (the lens that does it) ·
  `S5_concentric_map.png` (what a scan produces: a glyph advancing) · `A4_map_glyphs_seals.png`
  (the three states it moves between).
- **AEA CONCEPT SERVED** — `verb.observe` · `seed.7` CEILING-DETECT. Scanning is the game's verb
  for *"I do not understand this yet, and I am going to find out."*
- **TECHNIQUE** — key-bound (the hint strip ships **with** the key — a discoverability clause, not
  a nicety: the K key is a standing violation today, T-079), the sweep effect (A-089), then a
  CARTOGRAPHY UPDATE materialisation on the map (T-034) and a named feed line
  ("new element mapped — M"). Under reduced motion the materialisation is a state change, not a
  removal of the event.
- **LIVE DATA BINDING** — a scan writes a real discovery to `journey_save.json` and only for
  something really in range. A scan of something already KNOWN says so and costs nothing. The
  boot census (T-035) means the world can contain things the codex has not named, and a scan is
  how the player finds them.
- **FIDELITY GATE** — **G-3**: the sweep is cold; only the discovered glyph earns amber, and it
  earns it once. **G-5**: no scan ever produces a reassurance message with no datum behind it.
- **DEPENDS ON** — A-089, A-075, T-034, T-079.

---

**A-106 · COLLECT** — `INTERACTION` · `M` · `[PLANNED]`
- **STYLE REFERENCE** — `C3_world_artifacts_v3_dimensioned.png` (what is collected, at real
  dimensions) · `A5_world_artifacts.png` (the three uniques) · `S6_the_archive.png` (where the
  descent that yields them happens).
- **AEA CONCEPT SERVED** — `seed.10` BACKWARDS CHANNEL and `op.ship` — an artifact is proof that
  something real happened and survived the run that made it.
- **TECHNIQUE** — pick-up is a short camera-relative lift with the artifact's own oscillation
  about the sheet's three-quarter view (**±35°, not a free turntable** — the lab's argued
  constraint: a free turntable shows the back of an object at an arbitrary moment, which makes
  A/B against a fixed drawing unreadable and a still capture non-deterministic). The artifact then
  enters the codex at its real dimension against the metre scale.
- **LIVE DATA BINDING** — **an artifact may only be minted by a real event** — a memory that
  exists, a verdict that was rendered, a send that a human confirmed. The mint records its source
  row in `journey_save.json`, and the codex shows that provenance. There are no found objects with
  no history.
- **FIDELITY GATE** — **G-6**: the artifact is judged at its **real on-screen diameter** in the
  codex, no zooming — E8 G-6's exact clause. **G-5**: provenance is printed and is real.
- **DEPENDS ON** — A-025 … A-035, T-013.

---

**A-107 · UNDOCK** — `INTERACTION` · `S` · `[PLANNED]`
- **STYLE REFERENCE** — `S3_the_probe.png` (the probe alone in the dark again, 97.6% void — the
  composition undock returns the player to) · `D2` quadrant R-A (the play camera and its key-hint
  strip).
- **AEA CONCEPT SERVED** — `pr.emergence` EMERGENCE OVER IMPOSITION, quietly: the player leaves,
  and the entity carries on without them. Undock is the moment the game stops being a menu.
- **TECHNIQUE** — the dock tween reversed, plus the plate's brackets **draining** rather than
  vanishing (the release-early drain of the hold-to-confirm grammar, T-068); the OS/HUD returns to
  its spatial homes (COMMS on yaw, SYSTEM anchored, T-071). Under reduced motion the transition is
  a cut, and the cut is not treated as a lesser experience.
- **LIVE DATA BINDING** — layout and journey state persist through `POST /api/layout` /
  `/api/journey`, atomic and file-locked (T-010) — undocking is a real save point, and if the save
  fails the game says so rather than pretending.
- **FIDELITY GATE** — **G-1** on the first frame after undock against `S3_the_probe.png`: void
  share ≥ 70% for a scene, and the probe back in the lower third. If the HUD is still holding
  dock-scale furniture, the transition did not complete. **G-3**: the amber census must return to
  the field budget within the decay window, not instantly and not slowly.
- **DEPENDS ON** — A-100, T-010, T-068, T-071.

---

## 7. THE CUTS, THE COLLISIONS AND THE DECISIONS

A backlog that only adds is a wish list. Four things were **cut** and four **collisions** are
named rather than worked around.

### 7.1 What was cut, and why

1. **Five artifact tickets (WA-01..WA-05).** They are earlier revisions of WA-09..WA-13, not
   separate objects (§2.4 table). Building both sets would put five near-duplicate collectibles in
   a game whose whole aesthetic is scarcity.
2. **Eight plant tickets.** The D2 sheet's own note says *"ALL PLANTS SHARE THE 20 m ARCHETYPE."*
   Fifteen towers are one generator and fifteen real parameter rows; fifteen tickets would be fake
   granularity, and E6 §4 forbids a generator taking a parameter that is not a real field anyway.
   All fifteen plants are named and mapped in §2.7 — nothing was dropped, only un-duplicated.
3. **Twenty-five seal tickets.** `seals.js` generates all 29 from one press and six engraving
   families, deterministically, reading the index from `window.AEA`. Four tickets cover 29 seals
   with a sheet-per-ticket fidelity unit (§4.1).
4. **Every Blender ticket.** E6 §5 retired the `.blend → .glb → GLTFLoader` path on two silent
   failures (r128's GLTFLoader ignores `KHR_materials_emissive_strength`, so Blender emission
   arrives clamped dead; Blender 4.1+ silently drops `COLOR_0`, and vertex colours **are** our
   material model). Blender survives in this registry only as a **measuring instrument** — block
   out, read the real proportions, type them into `profileFromData`, delete the `.blend`. The
   precedent is already on disk: the probe was E5's named first Blender model and shipped as
   primitives instead.

Without those four cuts this registry would be 145 tickets. It is 107, and nothing buildable was
lost.

### 7.2 Collisions, named

- **`[DECISION-LUIS]` The S9 conduit read (E6 §3.5, blocks A-060).** S9's dominant look is
  persistent amber conduits at rest. A11 §4.1's closed list of legal idle amber does not contain
  conduits, and E2 Move 7 ruled explicitly that idle wires are structure ink only. **S9 as drawn
  cannot ship under current law.** Path (a): conduits idle cold, the city lights up when the
  entity works — arguably better, because it makes the sheet's beauty a reward rather than
  wallpaper. Path (b): amend A11 §4.1 with a named per-link binding (cumulative routed calls,
  log-scaled, capped). The generator is written so both are one uniform apart.
- **`[DECISION-LUIS]` The D2 R-C plant roster (blocks A-051's captions, not its geometry).** The
  sheet's fifteen cells are named THE HEARTH · THE GRID · REFLEX · BATCH · KEYLESS · NEXUS ·
  HADES · COGNITION · VOYAGER · BARANDIARAN · BEDAU · DGM · STOP · RESEARCH · SANDBOX. Cells 06–15
  are **organ and boss names, not plants** — the sheet mixed the foundry row with the module
  registry. The roster of record is `city.data.js` / `grid.PLANTS`. Either cells 06–15 are re-read
  as organ sites (A-058), or the foundry row is re-drawn.
- **`[DECISION-LUIS]` ACES (E6 §1.12, gates A-088 and A-097).** ACES desaturates amber toward
  cream-white in every bloom core — degrading "amber = alive" exactly where it matters most — and
  lifts the toe on the near-black void. Removing it is **not** a one-line edit: `engine.js`
  deliberately inlines the same curve in the sky `ShaderMaterial` so sky and fogged ground match,
  and removing one without the other seams the horizon. Requires an on-hardware A/B pair.
- **E8 §2 finding 2 (gates every G-3 in this file).** Plates run 3–6% amber-of-ink with 30–60% of
  it hot; scenes run 5–22% with ≤25% hot. Using one budget for both produces either dead plates or
  over-lit scenes. E8 marks the two-class split `[DECISION-LUIS]` — **until it is confirmed, every
  G-3 in this registry is provisional**, and that is stated rather than assumed away.

### 7.3 The two objects most likely to be got wrong

Stated in advance so the loop can be spent on them rather than discovering them:

1. **A-027 SILENCE STONE.** Nothing to hide behind, no live binding by design, and greebling is
   forbidden. If it reads as a grey egg there are exactly two levers (value ramp, ring depth) and
   six passes is the escalation bell (E8 §4.4) — after which it is a form decision, not tuning.
2. **A-060 THE CITY MAP HOLOGRAM.** The most beautiful sheet in the library is also the one that
   is currently illegal. The temptation will be to build the pretty version and litigate later.
   Build path (a). If Luis rules (b), it is one uniform.

---

## 8. COVERAGE — all 35 sheets accounted for

Every sheet is either a ticket's style reference, an explicitly superseded revision, or a
deliberate non-target. Nothing is unaccounted for.

| sheet | tickets served | note |
|---|---|---|
| `S1_field_genesis` | A-051 · A-056 · A-090 · A-096 · A-097 | the scene-class budget target (E8 §6.3) |
| `S2_entity_as_place` | A-060 | conduits are curves, never meshes (E5 §2) |
| `S3_the_probe` | A-001 · A-091 · A-107 | 97.6% void — the composition undock returns to |
| `S4_the_bench` | A-044 · A-083 · A-086 · A-100 | |
| `S5_concentric_map` | A-061 · A-077 · A-105 | |
| `S6_the_archive` | A-036 · A-106 | interior is instancing + fog, never modelled |
| `S7_honest_failure` | A-067 · A-084 · A-094 · A-103 | |
| `S8_keyart_a11` | — | **non-target by design**: key art, not a build reference |
| `S9_the_city_revealed` | A-041 · A-048 · A-060 · A-096 | the world target (E6 §3); amber read is gated |
| `A1_bench_parts` | A-008 … A-015 | 8 cells, 8 tickets |
| `A2_specimen_rods` | A-016 … A-024 · A-093 | 8 cells + the shared chassis |
| `A3_organ_buildings` | A-036 … A-043 | 8 cells, 8 tickets |
| `A4_map_glyphs_seals` | A-071 · A-075 | |
| `A5_world_artifacts` | A-025 … A-027 | five cells superseded by C3 (§2.4) |
| `A6_instrument_panels` | A-063 … A-070 | **superseded as judged target by C4**; kept for anatomy |
| `A7_district_landmarks` | A-044 … A-050 | 7 cells, 7 tickets |
| `B1_axis_principle_seals` | A-073 | E8 §6.4 first-application target |
| `B2_seed_seals` | A-072 | |
| `B3_verb_mechanic_op_seals` | A-074 | |
| `B4_doctrine_plates` | A-076 | |
| `B5_constructs` | A-062 · A-101 | |
| `B6_assistant_ladder` | — | **the six rungs render as Act screens**, tracked as engine deltas T-027 / T-029, not as asset tickets; referenced by A-056 (rung 1) |
| `B7_probe_hardware` | A-001 … A-007 | 7 cells, 7 tickets; E8 §6.1 first target |
| `B8_governance` | A-034 · A-037 · A-066 · A-103 | |
| `B9_the_send` | A-035 · A-043 | the ceremony is T-028's staging, the objects are ticketed |
| `C1_world_artifacts_v2` | — | **superseded** by C3 (v2 → v3 dimensioned) |
| `C2_contact_sheet_index` | — | **non-target by design**: the library's own index |
| `C3_world_artifacts_v3_dimensioned` | A-028 … A-035 | the revision of record; cuts in `game/ref/wa_*.png` |
| `C4_instrument_panels_v2` | A-063 … A-070 | the judged target; cuts in `game/ref/ip0*.png` |
| `D1_quad_screen_..._v1` | — | **superseded** by D2 |
| `D2_quad_screen_..._v2` | A-051 … A-058 · A-078 … A-085 · A-093 · A-099 | four quadrants, the densest single reference in the library |
| `R3_01_probe_turnaround` | A-001 | the ortho the probe's dimensions are read from |
| `R3_02_three_landmarks_turnaround` | A-044 · A-045 · A-047 | |
| `R3_03_power_plant_turnaround` | A-051 | the 20 m archetype's real profile |
| `R3_05_gameplay_screen` | A-078 … A-081 · A-086 · A-098 | the composed screen, exact |

### 8.1 The registry by class

| class | ids | count | built | planned |
|---|---|---|---|---|
| SOLID | A-001 … A-056 · A-058 · A-059 | 58 | 8 | 50 |
| HOLOGRAM | A-060 … A-062 | 3 | 0 | 3 |
| FLAT-UI | A-057 · A-063 … A-085 | 24 | 16 | 8 |
| EFFECT | A-086 … A-099 | 14 | 6 | 8 |
| INTERACTION | A-100 … A-107 | 8 | 4 | 4 |
| **total** | **A-001 … A-107** | **107** | **34** | **73** |

*(A-057, the capacity plate, is FLAT-UI class and is filed in §2.7 beside the towers it serves.
`built` counts tickets whose object exists on disk; **none of them is DONE**, because DONE
requires a `fidelity_ledger.jsonl` line and the ledger does not exist yet.)*

### 8.2 The first five, in order

Not a plan — the next five sessions, each ending with one ledger line:

1. **A-096** the concentric ground field. Zero new geometry, kills two named 2000s offenders, and
   E6 §6 is explicit that the ground ships **before** any tower. It blocks A-051.
2. **A-001** the probe, against `B7` cell 1 — E8 §6.1's first target and the cleanest SOLID-class
   test of E-7. Its live defect (T-066, the core blooming to a white blob) is the first gap.
3. **A-063 … A-070** the eight panels against `C4` — E8 §6.2. Already near-final art, so any
   failure is ours and cheap, and it teaches the gate loop before the loop is spent on geometry.
4. **A-090 / A-097** the `/probe` scene still against `S1` — E8 §6.3, the scene-class budget and
   the three-band test.
5. **A-073** the axis and principle seals against `B1` — E8 §6.4, FLAT-UI at small delivered size,
   the hardest G-6 in the registry.

Four of those five are E8 §6's own first-application list. The fifth is the ground, because
without it the other four are photographed against a placeholder floor.

---

## Changelog

- **2026-07-21 — v1.** Authored as the asset-producer pass over the 35 sheets in
  `design/concepts/`, `E5_3D_TRANSLATION.md` (the four asset classes), `E6_ART_PIPELINE.md` (the
  sanctioned trick stack, the generator set, the performance budget, the Blender ruling),
  `E8_FIDELITY_LAW.md` (the eight essence clauses and the seven gates), `INDEX.md` §3 (the T-001..
  T-082 registry's conventions, which this file matches and does not collide with),
  `aea_elements.js` (the 29 elements and 6 doctrines, by id), and a read of `game/js/*.js`,
  `city.data.js`, `grid.PLANTS` and `controlroom.py:77–129` on this date. Sheets read at full
  resolution for panel-level reference: A1, A2, A3, A5, A7, B7, D2, R3_05.
  **Findings that changed the backlog rather than being written around:** WA-01..WA-05 identified
  as superseded revisions of WA-09..WA-13 (five tickets cut); the D2 R-C plant roster found to
  contain organ names in cells 06–15 (raised as `[DECISION-LUIS]`); the Blender-derived tickets
  E5 §3 would have implied deleted under E6 §5; and every G-3 in the file marked provisional
  pending E8 §2 finding 2's two-class split.
