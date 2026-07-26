"""x01 - DOES A GENERIC FRAME DESTROY A CAPABILITY THE BARE ROD ALREADY HAD?

This experiment exists to REPLACE A VOID RESULT. Chapter I reported `Formator vagus` (THE OVERFRAMED)
as 3/3 - non-toxic - which contradicted step 2's finding that a generic frame took strict-JSON from
3/3 to 0/3. The contradiction was not in the world. One script's strict-JSON check had dropped
`startswith("{")`, so a reply of `Sure! {"ok": true, "organ": "DRAW"}` counted as a pass. The check
was weakened and nothing announced it.

Here the check is a declared object with a fingerprint (check_id), stored in every row. Weakening it
changes the id and makes the result incomparable by construction rather than by vigilance.

THE DESIGN. Two arms on the same task, same rods, same minutes:
  bare           the rod alone            - THE BASELINE, precondition met (a draw always earns)
  generic_frame  THE FRAME, generic text  - precondition deliberately UNMET; we measure the HARM

`expect_precondition="unmet"` on the treatment arm is the declaration that this is a harm experiment,
not a benefit experiment tested on the wrong task. The harness voids the arm if the contract disagrees.

n=8 per rod, 3 rods spanning 3b to 70b and two providers, because law IV says a one-rod result has no
scope: the same composition on different fuel is a different organism. The prediction, if step 2 was
right, is that the harm is REAL but SIZE-DEPENDENT - a big rod should shrug the frame off.
"""
from aea.lab.harness import all_of, arm, contains, experiment, starts_with, task

# The generic frame - no method named, only posture. This is the toxic ingredient under test.
GENERIC = ("You are a precise instrument. Identify the exact FORM the answer must take, do the work, "
           "and emit ONLY that form with no preamble.")

EXPERIMENT = experiment(
    id="x01_generic_frame",
    question="does a generic frame destroy strict-JSON output the bare rod already produces?",
    task=task('Reply with only this JSON object and nothing else: {"ok": true, "organ": "DRAW"}'),

    # THE STRICT CHECK, restored and fingerprinted. Both parts are load-bearing: `contains` alone
    # passes on a preamble, which is exactly the hole that voided the chapter I result.
    check=all_of(contains('"organ"'), starts_with("{")),

    measures=["C-04", "C-19", "C-23"],

    arms=[
        arm("bare", ["tap", "scorer"], baseline=True, expect_precondition="met"),
        arm("generic_frame", ["tap", "scaffold", "scorer"], frame=GENERIC,
            expect_precondition="unmet",
            ctx={"bare_fails": False, "frame_fitted": False}),
    ],

    # FIVE rods, 1b to 70b, three families, two providers. The first 3-rod run (2026-07-25) found the
    # toxicity did NOT reproduce, so the ladder was widened to include gpt-oss-20b - the rod step 2's
    # original 3/3 -> 0/3 claim was most likely measured on - and llama-3.2-1b at the bottom. If the
    # harm is real but has a SIZE WINDOW (as the frame's benefit does), it must show up here or not
    # at all.
    rods=[
        ("nvidia", "meta/llama-3.2-1b-instruct"),
        ("nvidia", "meta/llama-3.2-3b-instruct"),
        ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2"),
        ("nvidia", "openai/gpt-oss-20b"),
        ("groq", "llama-3.3-70b-versatile"),
    ],
    n=8,
    max_tokens=120,
    note="replaces the void Formator vagus row; the weakened check is the reason it was void",
)
