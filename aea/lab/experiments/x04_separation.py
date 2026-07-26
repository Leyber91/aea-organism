"""x04 - DOES SELF-CRITICISM REQUIRE A SEPARATE CALL? (law II)

THE STAKE. Law II is chapter I's strongest-looking result: asked to answer AND critique itself in one
breath, a rod found 0 errors in 9 trials; asked in a SEPARATE call, it found 9 of 9. That is a large
effect, and it is the reason THE CRITIC is anchored as a separate call rather than a prompt section.
It has never been through the harness, and it was measured on one rod at n=9.

THE DESIGN. Three arms, one variable - WHERE the criticism happens:
  bare        answer alone                                              - THE BASELINE
  one_breath  answer, then criticise yourself, then give a final answer - ALL IN ONE CALL
  separated   answer, then a SECOND call criticises and states the final - two calls

x03 has already shown why the task choice is the whole experiment: on the bat-and-ball trap, three of
five rods answered correctly bare, so `answer_may_be_wrong` was false on those rods and every critic
arm there measured cost and nothing else. This uses the LILY PAD trap, which is harder - the intuitive
answer (24) is more attractive than the correct one (47) because halving feels like halving the time.
Rods that answer it bare will still VOID, and that is the honest outcome rather than a lowered floor.
"""
from aea.lab.harness import arm, experiment, last_number_is, task

TRAP = ("In a lake there is a patch of lily pads. Every day the patch doubles in size. "
        "It takes 48 days for the patch to cover the entire lake. "
        "How many days does it take to cover half the lake? Answer with only the number.")

# ONE BREATH - the answer and its criticism in a single call. This is the form law II says fails.
ONE_BREATH = ("Answer in three labelled steps in ONE reply: (1) ANSWER - your first answer. "
              "(2) CRITIQUE - find the strongest error in your own answer above. "
              "(3) FINAL - the corrected answer alone on the last line.")

EXPERIMENT = experiment(
    id="x04_separation",
    question="must self-criticism happen in a separate call, or is one-breath self-critique enough?",
    task=task(TRAP),
    check=last_number_is("47"),
    measures=["C-50", "C-43", "C-78", "C-14"],

    arms=[
        arm("bare", ["tap", "scorer"], baseline=True, expect_precondition="met"),
        # one_breath seats THE FRAME, so its precondition is bare_fails AND frame_fitted. The frame
        # DOES name a method (three labelled steps), so frame_fitted is true; bare_fails is the claim
        # this run's own baseline adjudicates, per rod.
        arm("one_breath", ["tap", "scaffold", "scorer"], frame=ONE_BREATH,
            expect_precondition="met",
            ctx={"bare_fails": True, "frame_fitted": True}),
        arm("separated", ["tap", "critic", "scorer"],
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
    max_tokens=260,
    note="law II - the last of chapter I's four laws never put through the harness",
)
