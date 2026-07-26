"""x03 - MUST A JUDGE OVERRULE RATHER THAN ADVISE? (law III)

THE STAKE. THE CRITIC is the fifth and final module of chapter I's "complete set" creature, and it
carries C-43, C-50 and C-78 - falsification as a first-class path. Its entire justification is one
n=3..8 single-rod matrix asserting that a judge which returns FEEDBACK is destructive (7/8 -> 2/8)
while a judge which STATES THE CORRECTED ANSWER repairs (3/6 -> 6/6). That is the same evidentiary
standard that has now failed twice under measurement. If law III does not reproduce, chapter I's
complete creature has no measured basis.

THE DESIGN. Three arms, the same trap task, the same rods, the same minutes:
  bare              answer it alone                                   - THE BASELINE
  advise_revise     a separate call critiques, then the SAME rod revises with that critique in hand
  overrule          a separate call is handed the answer and states the corrected answer ITSELF

All three are separated calls, so this isolates ONE variable: who writes the final answer. That is
the difference law III actually claims, and chapter I's version confounded it with separation.

THE TASK is the bat-and-ball trap: 1.10 total, bat costs 1.00 more than the ball. The intuitive wrong
answer (10) is strongly attractive and the correct one (5) requires setting up the algebra, so a rod
that is merely fluent fails and a rod that is corrected succeeds. Any movement is visible.
"""
from aea.lab.harness import arm, experiment, last_number_is, task

TRAP = ("A bat and a ball cost 1.10 in total. The bat costs 1.00 more than the ball. "
        "How much does the ball cost? Answer in cents.")

EXPERIMENT = experiment(
    id="x03_judge",
    question="does a judge have to state the corrected answer itself, or is critique enough?",
    task=task(TRAP),
    check=last_number_is("5"),
    measures=["C-43", "C-50", "C-78", "C-14"],

    arms=[
        arm("bare", ["tap", "scorer"], baseline=True, expect_precondition="met"),
        # DECLARED "unmet" - and the harness caught me declaring "met" here first. THE CRITIC's
        # precondition already requires judge_overrules, so the advise form is BY CONSTRUCTION the
        # precondition-violating arm. The contract predicted this arm is tax before a token was spent;
        # this experiment tests whether it is merely tax or actively destructive.
        arm("advise_revise", ["tap", "critic", "scorer"],
            expect_precondition="unmet",
            ctx={"answer_may_be_wrong": True, "judge_overrules": False, "judge_capable": True}),
        arm("overrule", ["tap", "critic", "scorer"],
            expect_precondition="met",
            ctx={"answer_may_be_wrong": True, "judge_overrules": True, "judge_capable": True}),
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
    note="law III; the ONLY evidence for C-43/C-50/C-78 and it has never been through the harness",
)
