# REF-13 · THE RUNTIME FABRIC PLATE — layer 10 of the construction stack

**Locks:** the CODEX DETAIL PLATE format — the surface the game uses to show one layer of the
86-item census, with the codex claim and the substrate finding side by side and their
disagreements marked. The pattern generalises: every one of the 11 layers gets this plate.

**Generated:** 2026-07-25, first try, ChatGPT Image 2.0, zero attachments (field lesson 9 —
self-contained prompt in a continuing conversation).

## What landed (verified against the render)

- 11 rows, exactly 11, every string verbatim.
- Exactly 4 `≠` markers, on the 4 correct rows (C-76, C-79, C-80, C-84).
- C-80 given heavier rules — the gating contradiction reads first.
- Amber budget honoured exactly: 1 chamber in the inset + 3 words. 4 marks total, under 5%.
- The engraved 5-column register survives at this density. Image 2.0 holds tabular text.

## The one defect — a FABRICATED NUMBER, mine not the engine's

`C-78 · FALSIFY · 2 FILES` cannot be reproduced. Re-verified 2026-07-25:

    grep -rl "falsify" aea/            -> 0 files
    grep -rli "falsif|adversarial|refut" --include=*.py aea/ | grep -v pycache
        -> 4 files (grid, anchor, axes, autonomy) — but that is a DIFFERENT claim

The literal named execution path does not exist. `0 FILES` is the verified cell. The `2` came
from the census and I carried it into an image without re-deriving it. Corrected below.

Also missing, non-blocking: no legend for `≠`. Standalone, the plate is mute about its own
most important mark.

## The corrected prompt (paste-ready, self-contained)

Identical to the first generation with two changes:

1. row C-78 MACHINE cell reads `0 FILES`, not `2 FILES`
2. add, engraved small at the head of the gutter column between CANON and MACHINE:
   `≠ = THE CODEX AND THE CODE DISAGREE`

Foot line is unchanged and still true: `11 ITEMS · 3 FOUND · 4 CONTRADICTIONS · 1 GATES FORTY`
— the 3 found are C-81/C-83/C-84, the 4 contradictions are C-76/C-79/C-80/C-84.

## The verified content block (re-derive before any reshoot)

| id | canon | machine | verified how |
|---|---|---|---|
| C-76 | MISSING | IT TICKS | `loop/aea.py` ticks; no fixed 10-step order |
| C-77 | COMPRESSED | 0 FILES | `grep -rl peer_debate aea/` = 0 |
| C-78 | COMPRESSED | 0 FILES | `grep -rl falsify aea/` = 0 |
| C-79 | MISSING | 4 FILES | axes, autonomy, reflect, controlroom |
| C-80 | EMBODIED | 0 FILES | `grep -rl checkpoint aea/` = 0 — the root |
| C-81 | EMBODIED | PRESENT | pulse + `state/*.json` = 35 files |
| C-82 | COMPRESSED | NOT CHECKED | — |
| C-83 | OUT OF SCOPE | PRESENT | `grid.call_openai`, one function |
| C-84 | COMPRESSED | PRESENT | `energy_usage.json` keyed per rod |
| C-85 | OUT OF SCOPE | NOT CHECKED | — |
| C-86 | OUT OF SCOPE | NOT CHECKED | — |
