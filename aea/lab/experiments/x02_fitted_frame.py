"""x02 - DOES A FITTED FRAME (ONE THAT NAMES THE METHOD) EARN ITS COST?

THE STAKE. x01 retracted the harm half of THE FRAME's justification: an unfitted frame is tax, not
poison. That leaves this experiment carrying the module ENTIRELY. `anchor.scaffold` closes C-04, C-19
and C-23, and its precondition (`bare_fails AND frame_fitted`) now rests on one n=3 result from a
single rod - the same evidentiary standard that just failed under measurement. If the benefit does not
reproduce either, THE FRAME has no measured justification at all and chapter I's spine is wrong.

THE DESIGN. Same task, same rods, same minutes:
  bare          the rod alone                                    - THE BASELINE
  fitted_frame  a frame that NAMES THE METHOD, step by step       - the treatment

The fitted arm declares `bare_fails=True`, which is what makes its precondition read as met. That
declaration is a CLAIM, and this run's own baseline adjudicates it per rod: on any rod where bare
scores 8/8 the arm is VOID ON THAT ROD, because a frame cannot rescue a capability that was never
missing. Expect exactly that on the large rods - and it is not a failure of the experiment, it is the
precondition being enforced instead of assumed. The finding lives or dies on the rods where bare
genuinely fails.

THE TASK is word-counting: cheap, unambiguously checkable, and a known weak spot for small rods
because it requires positional bookkeeping rather than recall.
"""
from aea.lab.harness import arm, experiment, last_number_is, task

WORDS = "the mouth draws power through the ladder and the measure closes the wire"   # 13 words

# THE FITTED FRAME - it names the METHOD (split, number, report the final index). This is the whole
# distinction from x01's generic frame, which named only a posture.
FITTED = ("To count words: split the sentence on spaces, number each token 1,2,3..., then report the "
          "FINAL index. Show the numbered list, then the count alone on the last line.")

EXPERIMENT = experiment(
    id="x02_fitted_frame",
    question="does a frame that names the method convert failure into success, and on which fuel?",
    task=task("Count the words in the sentence below and reply with ONLY the number.\n" + WORDS),
    check=last_number_is("13"),

    measures=["C-04", "C-19", "C-23", "C-16"],

    arms=[
        arm("bare", ["tap", "scorer"], baseline=True, expect_precondition="met"),
        arm("fitted_frame", ["tap", "scaffold", "scorer"], frame=FITTED,
            expect_precondition="met",
            ctx={"bare_fails": True, "frame_fitted": True}),
    ],

    rods=[
        ("nvidia", "meta/llama-3.2-1b-instruct"),
        ("nvidia", "meta/llama-3.2-3b-instruct"),
        ("nvidia", "nvidia/nvidia-nemotron-nano-9b-v2"),
        ("nvidia", "openai/gpt-oss-20b"),
        ("groq", "llama-3.3-70b-versatile"),
    ],
    n=8,
    max_tokens=220,
    note="the ONLY remaining evidence for THE FRAME's precondition after x01 retracted the harm claim",
)
