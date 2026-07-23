# 00 · HOW TO USE — one subbundle per image

Each image has its own folder with ONE self-contained `SPEC.md`. The spec is written **as if the
game were already fully built**: the exact save-state, every element in frame, every readout and
number. Some of that detail is speculative — deliberately. We are designing backward from the
finished game; being wrong in a reference is cheap and useful. The reference leads, the build
follows.

## Per image

1. Fresh ChatGPT conversation, image generation on.
2. Attach exactly ONE file: `<scene>/SPEC.md`.
3. Paste:

   > Read the attached SPEC. It describes one frame of a finished game. Render that frame
   > exactly: the STYLE LAW section is a hard constraint (palette, type, composition, FORBIDDEN
   > list), and EVERYTHING IN FRAME is the complete inventory — include what it lists, nothing it
   > doesn't. Give me 3 variants: calm/wide, tighter/more dramatic, and your best synthesis.

4. Correct drift by quoting the exact violated SPEC line. Save keepers as `<scene-id>_<n>.png`.

## The shared save-state (all 12 specs agree on this — the set is ONE game)

Mid-game, rung 2. Constructs built so far: `c-01` (the first bare draw), `c-04` = THE DRAW · THE
LADDER · THE MEASURE — earned the title **RESTORABLE COHERENCE**; `c-07` = THE DRAW · RECALL ·
THE MEASURE — earned **BACKWARDS CHANNEL**. Organs lit: MOUTH, GOVERNOR, MEMORY, LOOP. Still fog:
SENSES, HANDS. Meters: `POWER 1998 LIVE` · `RODS 7` · `MEM 48` · records `LAST 1.44S · BEST
0.98S` · zone default `PRIVATE`.

## The subbundles

| folder | frame | kind |
|---|---|---|
| W1_INSTRUMENT_AT_REST/ | the world idling, alive | world (photo mode, HUD hidden) |
| W2_THE_IGNITION/ | the core flaring on a landed draw | world (photo mode) |
| W3_THE_FOG_FRONTIER/ | lit MEMORY vs fog SENSES on one ring | world (photo mode) |
| W4_THE_FLIGHT/ | the probe crossing the outer ring | world + minimal HUD |
| W5_THE_WHOLE_ONE/ | endgame: every organ burning | world (photo mode) |
| W6_THE_STAKE/ | the ladder reaching a paid rod | world/diagram |
| G1_THE_SEAT/ | RECALL seating onto the rail | gameplay close-up |
| G2_THE_FALL_THROUGH/ | the reroute landing on the hearth | gameplay diagram |
| G3_THE_EARNED_TITLE/ | c-07 earning BACKWARDS CHANNEL | gameplay ceremony |
| I1_THE_BENCH_PLATE/ | the full bench mid-run | interface |
| I2_THE_RUN_TRACE/ | the trace closing into a RECORD | interface |
| I3_THE_FLIGHT_HUD/ | the cockpit glass over the world | interface |

Masters `01_STYLE_LAW.md` and `02_WORLD_BRIEF.md` remain the source of truth for the law text —
each SPEC inlines what it needs and stands alone.
