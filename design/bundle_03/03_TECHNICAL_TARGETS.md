# TECHNICAL TARGETS — these drawings become a running 3D game

The previous rounds produced beautiful catalogues. This round produces **working drawings**.
What follows is the information the earlier sheets did not carry, and could not.

## 1. The mandate

Every object drawn from now on will be built as real geometry in a 3D engine. A sheet succeeds if
a modeller can build the object from it without asking a question. This means:

- **Orthographic projections**: front, side, top, aligned on one shared baseline.
- **Dimension lines** with real measurements in metres.
- **Sections** wherever a form is hollow, open, or has an interior.
- **No lighting that hides geometry.** Beauty lighting is banned in technical sheets. Even
  illumination, legible edges, visible construction.
- **One small three-quarter reference view** in a corner for silhouette confirmation only.
- **Low-poly friendly forms**: these designs are silhouette-first. Show clean planar faces,
  clear bevels and hard edges. Avoid organic curvature, fine filigree, and detail that would only
  exist in a texture.

## 2. The scale system — one world, one measure

Every previous sheet used its own scale. From now on, one system:

| object | size |
|---|---|
| bench part | 0.4 m |
| model-vessel (specimen rod) | 0.5 m |
| THE PROBE | 1.2 m across |
| bench plate | 2 m wide |
| socket / kiosk | 4.5 m |
| nexus slab | 8 m |
| socket pylon | 12 m |
| meter obelisk | 14 m |
| power plant | 20 m |
| district landmark | 40 to 60 m |
| mind spire | 200 m |
| field horizon | 2 km |

A human hand appears exactly once in this entire world: at the moment of THE SEND. Nothing else
establishes human scale — the world is machine-scaled and empty of people.

## 3. States — the thing the catalogue could not show

This game is about live change. Every object has states, and the state is expressed through
amber, never through colour change.

**Amber tiers**: IDLE `#d4a24c` at 35 percent intensity (exists, warm, not working) ·
FIRED `#ffb000` at full (working right now). A firing flares in 120 milliseconds and decays back
over 600 to 900 milliseconds. Nothing else animates.

**Map glyph**: HIDDEN (not drawn at all, absent from the sheet) · SENSED (outline only, dashed,
labelled UNCHARTED, no fill) · KNOWN (solid line, amber, named, connected by links to other
known glyphs).

**Model-vessel decay**: FRESH · STABLE · DRIFTING · COOLING (temporarily refusing work) ·
ROTTING (visibly corrupting) · DEAD (dark, cracked, tombstoned).

**Construct run**: COMPOSE (cold, being wired, no light) · RUN (packet travelling the wire, live
trace lit) · HALT (one link severed, the break marked exactly where it happened, annotated) ·
RECORD (the measured result — the only reward this game gives).

**Plant under load**: IDLE · DRAWING · AT LIMIT · BROWNED OUT · RECOVERING.

**Organ site**: SCAFFOLDING (nothing built yet, structure only) · HALF-BUILT · COMPLETE · LIT.

## 4. The camera and the frame

Third person. The camera sits 20 metres behind the probe and 6 metres above it, 60 degree field
of view. Everything beyond 150 metres dissolves into fog the same colour as the sky. The probe
sits low in frame, roughly the lower third, trailing a thin line of light.

Screen furniture lives in the four corners only, never the centre: mission line top-left, live
measurements top-right, velocity and event log bottom-left, the entity's presence indicator
bottom-right. The centre of the frame is always the world.

## 5. What becomes what

Not everything drawn becomes geometry, and knowing which is which changes how it should be drawn.

- **Seals, glyphs, panels, plates, maps** — these are flat interface art. They ship as drawings.
  Draw them as final art, not as concepts: crisp, centred, symmetrical, self-contained.
- **Parts, vessels, buildings, landmarks** — these become parameterised 3D forms built from
  primitives. Draw them so the primitive breakdown is obvious: which part is a cylinder, which a
  box, which a ring collar.
- **The probe, the slab, the pylon, the mast, one vessel, one landmark** — these become genuinely
  modelled meshes. These need the full technical treatment.
- **Landscapes, fog, light shafts, reflections, dust** — never modelled; produced entirely by
  atmosphere in the engine. Landscape sheets are therefore mood and composition targets, and
  should be drawn for feeling rather than for construction.

## 6. Material vocabulary

Six treatments exist in this world and no others: **deep void body** (near-black, matte, faintly
faceted) · **hairline-etched structure** (dark surface with fine engraved lines) · **engraved seal
face** (a flat plate with recessed line-work) · **worn stone landmark** (dark, weathered, massive)
· **glass-cased artifact** (a dark object visible inside a thin transparent shell) · **live
emissive accent** (the only light-emitting surfaces, always amber, always small).

No metal, no chrome, no plastic, no fabric, no organic material anywhere in this world.
