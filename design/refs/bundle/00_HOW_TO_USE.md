# 00 · HOW TO USE THIS BUNDLE (ChatGPT image generation)

The bundle exists so the generator "goes full on the scenes" — it gets the whole world, the whole
style, and one precise scene per image. One-line prompts produce generic sci-fi; this does not.

## Per generation (repeat for each scene)

1. Start a fresh ChatGPT conversation (image generation on).
2. **Attach three files:** `01_STYLE_LAW.md` + `02_WORLD_BRIEF.md` + ONE file from `SCENES/`.
3. Paste this instruction:

   > Read the three attached files. Generate the image described in the SCENE file, obeying
   > 01_STYLE_LAW absolutely — palette, composition laws, and the FORBIDDEN list are hard
   > constraints. The image is a production art-direction reference for this game, not a poster.
   > Give me 3 distinct variants: one wide/calm, one tighter/more dramatic, one your best synthesis.

4. If a variant drifts off-brand, reply quoting the exact violated line from 01_STYLE_LAW
   (e.g. "FORBIDDEN: lens-flare soup") and ask for a correction — the law file is the referee.
5. Save keepers as `<scene-id>_<n>.png` (e.g. `I1-bench-plate_2.png`).

## What comes back to the repo

Drop all keepers in one folder and hand them over. They get curated together with the local forge
batch; the WINNERS are committed to `design/refs/` as the locked visual spec (`REFS.md` maps each
ref to the game surface it governs). From then on a visual slice is DONE only when the real render
matches its reference side-by-side.

## Scene index

| file | scene | what it specs |
|---|---|---|
| SCENES/W1_INSTRUMENT_AT_REST.md | the world at rest | the world render (engine.js) |
| SCENES/W2_THE_IGNITION.md | the core flaring on a real draw | the fire/wow moment |
| SCENES/W3_THE_FOG_FRONTIER.md | earned amber vs cold fog organ | organ states |
| SCENES/W4_THE_FLIGHT.md | the probe tiny over the instrument | flight scale + atmosphere |
| SCENES/W5_THE_WHOLE_ONE.md | every organ lit — the endgame poster | the destination image |
| SCENES/W6_THE_STAKE.md | the ladder reaching a paid cloud rod | the metered-reach beat |
| SCENES/G1_THE_SEAT.md | seating a part on the rail | the compose verb |
| SCENES/G2_THE_FALL_THROUGH.md | rerouting down dead rods to the hearth | resilience made visible |
| SCENES/G3_THE_EARNED_TITLE.md | a being earning its first real name | the naming payoff |
| SCENES/I1_THE_BENCH_PLATE.md | the bench as a milled instrument | the bench UI (probe.css/bench.js) |
| SCENES/I2_THE_RUN_TRACE.md | the live trace + receipts | the run-log surface |
| SCENES/I3_THE_FLIGHT_HUD.md | the minimal diegetic HUD | the in-flight overlay |
