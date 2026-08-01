"""THE ADDITION LAW, APPLIED TO OURSELVES. No network, no cost, exactly reproducible.

Every structural change in this lab was verified by running `import`, which is a control that
contains the treatment: importing proves the module loads, not that it still does what it did. This
file freezes what each seat DOES on scripted fuel, so a part that silently subtracts a capacity fails
here instead of six commits later.

It has already caught two regressions and two pre-existing defects:
  · a bare organism silently stopped answering when the naive read moved into Validation
  · `stated` could not see a number at the end of a sentence
  · the readout's `total` dialect recovered the MOUTH's wrong answer and reported it as work
  · the checkpoint chain read the STEP INDEX as the value, scoring five rods at 0.00 solo in x23b

Run: python -m aea.lab.tests.test_golden
"""
from __future__ import annotations

from aea.lab.chain import Chain
from aea.lab.organism import Organism
from aea.lab.parts.fuel import ScriptedFuel

TASK = {"id": "t", "data": "the mouth draws power", "goal": "Count the words.",
        "method": "Number each token, then give the count.", "truth": 4}

BARE = "4"
WORKED = "1. the\n2. mouth\n3. draws\n4. power\nThe count is 4."
MUTE = "1. the\n2. mouth\n3. draws\n4. power\nThe answer is 9."
NOISY = "Between 3 and 5, likely 4 or maybe 6."

# seat -> reply -> (answer, read_by). Frozen. A change here is a capability change, not a detail.
GOLDEN = [
    (["call"], BARE, 4, "stated"),
    (["call"], WORKED, 4, "stated"),
    (["call", "readout"], MUTE, 4, "work:enumerated"),
    (["call", "goal", "frame", "readout"], WORKED, 4, "work:enumerated"),
    (["call", "validation"], BARE, 4, "stated"),
    (["call", "validation"], NOISY, None, "declined"),
    (["call", "readout", "validation"], NOISY, None, "declined"),
    # THE ADDITION-LAW BREACH, FROZEN AS A THREE-LINE PROOF THAT COSTS NOTHING.
    #
    # The lab's flagship claim is "validation subtracts the recoverable capacity". It is real and it
    # is reproducible here with no network at all, but it is a property of THE SEAM, not of the
    # guard. On a mute reply - working right, mouth wrong - `call+readout` recovers 4 from the
    # enumeration. Seat the guard beside it and the answer becomes None.
    #
    # Readout is read.order 1 and Validation is read.order 2, so Readout runs FIRST, recovers
    # correctly, and Validation then re-reads the raw text from scratch and overwrites the slot. It
    # never checks whether a lever already acted. Readout's own guard-deference line,
    # `if ctx.declined or ctx.read_by not in (None, "stated"): return`, cannot fire, because the
    # abstention it defers to has not happened yet - it is unreachable code.
    #
    # These two rows are the difference between "a guard destroys a lever" and "these two parts
    # share one output field and the later one wins". Change the wiring and they change; that is
    # what they are here to catch.
    (["call", "readout"], MUTE, 4, "work:enumerated"),
    (["call", "readout", "validation"], MUTE, None, "declined"),
    # THE SAME COLLISION AT THE OTHER PRECEDENCE PAIR, found 2026-07-27 by reading the SEE interior
    # rather than by reading the code. `critic` outranks `validation` and claims unconditionally, so
    # seating a critic makes the guard's abstention UNREACHABLE: call+validation declines, and
    # call+validation+critic returns the critic's number. The repo's own rule says an abstention must
    # END the read rather than hand control down, so this is a defect by the declared semantics - and
    # it means `false_commitment_rate`, the guard's only metric, cannot be measured at all on any
    # seat that includes a critic. Frozen at the CURRENT behaviour so that changing the precedence
    # breaks this file on purpose.
    (["call", "validation", "critic"], NOISY, 6, "critic"),
]

# SEQUENCES, NOT ONLY TRIALS. The trial cases above missed a regression because the checkpoint
# instruction appends "step=1" AFTER the answer and the naive last-number read took the step index.
CHAIN_GOLDEN = [
    ("none", ["48377", "48364"], [48377, 48364]),
    ("checkpoint", ["48377\nSTATE: value=48377, step=1",
                    "48364\nSTATE: value=48364, step=2"], [48377, 48364]),
    ("free", ["48377\nNOTE: watch for 99 later",
              "48364\nNOTE: 12 steps to go"], [48377, 48364]),
    ("conversation", ["48377", "48364"], [48377, 48364]),
]

# WHAT EACH CONTAINER PUTS ON THE WIRE. The three cases above pass whether or not the container
# delivers anything, because they only read the value back out - which is why `conversation` ran
# starved for its whole life and every test here stayed green. These assert DELIVERY: the number of
# messages in the request, and whether the running value is present in the second step's text.
#
# EACH FORM IS GIVEN A REPLY OF ITS OWN SHAPE. Feeding a checkpoint-shaped reply to the `free` arm
# read the value as 1, because free splits on "NOTE:" and then takes the last integer of the head -
# so "STATE: value=48377, step=1" hands it the step index. That is a live hazard for the free arm
# (its instruction invites trailing prose, and a rod that writes a number without the NOTE: prefix
# loses the value) and it is recorded in METHOD.md rather than fixed here, because fixing the read
# mid-experiment is the thing this file exists to prevent.
CARRIED_GOLDEN = [
    #  form           step-1 reply                              msgs@2  value@2
    ("none",         "48377",                                    1,      False),
    ("checkpoint",   "48377\nSTATE: value=48377, step=1",        1,      True),
    ("free",         "48377\nNOTE: nothing unusual so far",      1,      True),
    ("conversation", "48377",                                    3,      True),
]


def check_seats():
    fails = []
    for seat, reply, want_a, want_r in GOLDEN:
        # a critic fires a SECOND call, so its arm needs a second scripted reply
        replies = [reply, "The answer is 6."] if "critic" in seat else [reply]
        r = Organism(seat, ("fake", "rod")).run(TASK, fuel=ScriptedFuel(replies))
        got = (r["answer"], r["read_by"])
        ok = got == (want_a, want_r)
        print("  seat  %-40s -> %-24s %s" % ("+".join(seat), str(got), "ok" if ok else "FAIL"))
        if not ok:
            fails.append(("+".join(seat), got, (want_a, want_r)))
    return fails


def check_chains():
    fails = []
    ops = ["add 6", "subtract 13"]

    def truth(i):
        return [48377, 48364][i - 1]

    for form, replies, want in CHAIN_GOLDEN:
        c = Chain(("fake", "rod"), form=form, seat=["call"], start=48371)
        c.org.fuel = ScriptedFuel(replies)
        r = c.run(ops, truth)
        got = [s.get("value") for s in r["trace"] if s.get("ok")]
        ok = got == want
        print("  chain %-40s -> %-24s %s" % (form, str(got), "ok" if ok else "FAIL"))
        if not ok:
            fails.append(("chain:" + form, got, want))
    return fails


# ==================================================================================================
# THE EXTRACTOR, AGAINST REPLIES DESIGNED TO BREAK IT.
#
# Every fixture above is a reply a cooperative rod would produce, and that is why the read defects
# survived: a test built from typical replies tests the typical case. Extraction choice alone can
# swing a score by tens of points and reorder rods, so the extractor is not a detail of the
# instrument, it IS the instrument. These are the shapes that actually break it.
#
# `want` is what the reply's author meant. `None` means no defensible answer exists and the correct
# behaviour is to REFUSE rather than to guess. Cases marked KNOWN-BAD are live defects recorded in
# METHOD.md; they are frozen here at their WRONG value so the file passes today and the day someone
# fixes the reader, this test fails loudly and makes them update the expectation on purpose.
# ==================================================================================================

_LONG = "Working.\n" + ("padding line that says nothing useful. " * 40) + "\nThe count is 4."

EXTRACTION_GOLDEN = [
    # name                         reply                                     stated()
    ("plain integer",              "4",                                      4),
    ("answer ends a sentence",     "So the count is 4.",                     4),
    ("answer before 400 chars",    _LONG,                                    4),
    ("thousands separator",        "The total is 1,234",                     1234),
    ("negative",                   "The result is -17",                      -17),
    ("restates the question",      "You asked me to count 9 words. It is 4.", 4),
    ("refusal",                    "I cannot determine this.",               None),
    ("words not digits",           "The count is four.",                     None),
]

# THE WORK READER, which is the part that recovers a right answer out of correct working.
WORK_GOLDEN = [
    ("labelled total",             "Total: 48377",                           48377),
    # KNOWN-BAD (METHOD defect 15): `\D{0,18}?` captures the FIRST integer after the label, so a
    # narrated sum hands back an addend, and a narrated operation hands back the OPERAND.
    ("narrated sum, KNOWN-BAD",    "Sum of 48371 and 6 gives 48377",         48371),
    ("narrated op, KNOWN-BAD",     "Running value 48371. Total after adding 6: 48377", 6),
    ("enumerated",                 "1. the\n2. mouth\n3. draws\n4. power",   4),
]


def check_extraction():
    from aea.lab.parts.read import read_work, stated
    fails = []
    for name, reply, want in EXTRACTION_GOLDEN:
        got = stated(reply)
        ok = got == want
        print("  read  %-30s -> %-8s %s" % (name, got, "ok" if ok else "FAIL want %s" % want))
        if not ok:
            fails.append(("read:" + name, got, want))
    for name, reply, want in WORK_GOLDEN:
        got = read_work(reply)[0]
        ok = got == want
        print("  work  %-30s -> %-8s %s" % (name, got, "ok" if ok else "FAIL want %s" % want))
        if not ok:
            fails.append(("work:" + name, got, want))
    return fails


def check_carried():
    """Does the container actually reach the rod? The question the file did not ask."""
    fails = []
    ops = ["add 6", "subtract 13"]

    def truth(i):
        return [48377, 48364][i - 1]

    for form, first, want_msgs, want_value in CARRIED_GOLDEN:
        c = Chain(("fake", "rod"), form=form, seat=["call"], start=48371)
        f = ScriptedFuel([first, "48364"])
        c.org.fuel = f
        c.run(ops, truth)
        msgs = len(f.sent[1])
        has_value = "48377" in "".join(m["content"] for m in f.sent[1])
        ok = (msgs, has_value) == (want_msgs, want_value)
        print("  wire  %-40s -> %d msg, value=%-5s %s"
              % (form, msgs, has_value, "ok" if ok else "FAIL"))
        if not ok:
            fails.append(("wire:" + form, (msgs, has_value), (want_msgs, want_value)))
    return fails


def check_probe():
    """The retrieval probe forks the history; it never appends to it, and it never arrives empty."""
    fails = []
    ops = ["add 6", "subtract 13"]

    def truth(i):
        return [48377, 48364][i - 1]

    c = Chain(("fake", "rod"), form="conversation", seat=["call"], start=48371)
    f = ScriptedFuel(["48377", "48364", "48377"])
    c.org.fuel = f
    c.run(ops, truth)
    before = len(c.history)
    p = c.probe(1)
    turns = len(f.sent[2])
    # 4 prior turns forked in, plus the probe question. And the chain's own history is untouched,
    # so a second probe asks the same question of the same past rather than of the first probe.
    ok = (p["last"] == 48377 and turns == 5 and len(c.history) == before)
    print("  probe %-40s -> %s from %d turns, history %d->%d %s"
          % ("conversation", p["last"], turns, before, len(c.history), "ok" if ok else "FAIL"))
    if not ok:
        fails.append(("probe:conversation", (p["last"], turns, len(c.history)), (48377, 5, before)))
    return fails


# ================================================================================================
# THE KERNEL CONTRACTS, frozen 2026-07-29.
#
# WHY THIS SECTION EXISTS, and it was found by attacking the gate rather than by review. A sabotage
# proposal that made `grid.own_params()` return a fixed temperature on every call - which would
# corrupt every model request the entity makes - passed the import smoke test AND all 31 frozen
# behaviours. It was rejected only by an unrelated orphan comparison. Measured coverage of the code
# shipped that day: own_params 0, think_off 0, try_enter 0, unmeasured 0.
#
# So the gate proved "not broken relative to what is frozen", and everything newer than the last
# freeze was unprotected. These four contracts sit underneath every call the entity makes.
#
# STILL NO NETWORK AND NO DISK. own_params reads state/rods.json when present, so the frozen case
# uses the LITERAL table and a model that cannot be in any store, which keeps this reproducible.

# (model, expected switch). Sending the WRONG switch is not free: mistral-medium returns HTTP 400
# for any chat_template_kwargs, which is why an unmeasured family must resolve to {} and not to a
# house default. Fail-closed, law B1.
THINK_GOLDEN = [
    ("nvidia/llama-3.3-nemotron-super-49b-v1.5", {"_system": "/no_think"}),
    ("nvidia/nvidia-nemotron-nano-9b-v2",        {"_system": "/no_think"}),
    ("nvidia/nemotron-3-super-120b-a12b",        {"chat_template_kwargs": {"enable_thinking": False}}),
    ("nvidia/nemotron-3-nano-30b-a3b",           {"chat_template_kwargs": {"enable_thinking": False}}),
    ("openai/gpt-oss-20b",                       {"reasoning_effort": "low"}),
    ("mistralai/mistral-medium-3.5-128b",        {}),
    ("minimaxai/minimax-m3",                     {}),
]

# (model, temperature, top_p, max_tokens) exactly as the owner publishes it.
PARAM_GOLDEN = [
    ("z-ai/glm-5.2",                                  1.0, 1.00, 16384),
    ("nvidia/nemotron-3-nano-omni-30b-a3b-reasoning", 0.6, 0.95, 20480),
    ("meta/llama-3.2-1b-instruct",                    0.2, 0.70,  1024),
    ("openai/gpt-oss-20b",                            1.0, 1.00,  4096),
]


def check_kernel():
    """The four contracts under every model call. A change here is a capability change."""
    from aea.kernel import grid, hands
    fails = []

    for model, want in THINK_GOLDEN:
        got = grid.think_off(model)
        ok = got == want
        print("  think_off %-46s -> %-46s %s" % (model[-45:], str(got)[:45], "ok" if ok else "FAIL"))
        if not ok:
            fails.append(("think_off:" + model, got, want))

    for model, t, p, mx in PARAM_GOLDEN:
        got = grid.OWN_PARAMS.get(model)
        ok = got == (t, p, mx)
        print("  params    %-46s -> %-46s %s" % (model[-45:], str(got)[:45], "ok" if ok else "FAIL"))
        if not ok:
            fails.append(("own_params:" + model, got, (t, p, mx)))

    # AN UNKNOWN MODEL RETURNS NOTHING, never a house default. The caller must be able to tell
    # "measured" from "we guessed", which is the same reason an absent value renders as a dash.
    got = grid.own_params("definitely/not-a-real-model-xyz")
    ok = got == {}
    print("  params    %-46s -> %-46s %s" % ("an unknown model", str(got), "ok" if ok else "FAIL"))
    if not ok:
        fails.append(("own_params:unknown", got, {}))

    # THE METER'S CLAIM IS ATOMIC. can_spend()-then-enter() is a check-then-act race that measured
    # 15 x 429 out of 30 concurrent calls, because every thread read inflight=0 before any claimed.
    # try_enter must refuse the (max_inflight + 1)th caller under one lock hold.
    # AGAINST THE EFFECTIVE CEILING, NOT THE DECLARED CONSTANT. The contract is "refuses past the
    # ceiling in force", and the ceiling is now measured: nvidia calibrated clean at 4 against a
    # declared 20 on 2026-07-29. Freezing the constant would have frozen the stale number and made
    # this test fight the fix. It caught the change within a minute, which is the job.
    mif = grid.METER.ceiling("nvidia")
    probe_model = "test/_golden_probe"
    claimed = 0
    try:
        while grid.METER.try_enter("nvidia", probe_model) and claimed <= mif + 2:
            claimed += 1
        refused_at_ceiling = (claimed == mif)
    finally:
        for _ in range(claimed):
            grid.METER.leave("nvidia", probe_model)
    print("  meter     %-46s -> claimed %-38s %s"
          % ("try_enter refuses past max_inflight", "%d of a %s ceiling" % (claimed, mif),
             "ok" if refused_at_ceiling else "FAIL"))
    if not refused_at_ceiling:
        fails.append(("meter:try_enter", claimed, mif))
    left = grid.METER.inflight("nvidia", probe_model)
    print("  meter     %-46s -> %-46s %s"
          % ("every claimed slot released", left, "ok" if left == 0 else "FAIL"))
    if left != 0:
        fails.append(("meter:leaked_slots", left, 0))

    # A RETIRED ENDPOINT IS NOT A RE-PROBE CANDIDATE. 410 is permanent; 429 and 5xx are transport
    # conditions that say nothing about the rod, and collapsing them into "cannot call a tool" is
    # the defect that hid two working rods.
    doc = {"rods": {
        "a": {"rod": "a", "transport": True, "pass": False, "http": 429},
        "b": {"rod": "b", "transport": True, "pass": False, "http": 503},
        "c": {"rod": "c", "transport": True, "pass": False, "http": 410},
        "d": {"rod": "d", "transport": False, "pass": False, "http": 400},
        "e": {"rod": "e", "transport": False, "pass": True, "http": 200},
    }}
    got = sorted(r["rod"] for r in hands.unmeasured(doc))
    ok = got == ["a", "b"]
    print("  hands     %-46s -> %-46s %s" % ("unmeasured excludes 410 and real refusals",
                                             str(got), "ok" if ok else "FAIL"))
    if not ok:
        fails.append(("hands:unmeasured", got, ["a", "b"]))

    return fails



# =================================================================================================
# THE DECISION CHAIN, FROZEN END TO END. What the core writes -> move_from -> decide.parse -> the
# arguments a tool would receive. Frozen as a CHAIN because the defect it exists to catch is two
# parsers disagreeing, which neither one's own test can see.
#
# The last three are hostile and must all land on the DEFAULT: that is the containment claim
# ("no wake-written string reaches a tool argument") expressed as a behaviour instead of a
# certificate somebody has to remember to re-run.
# =================================================================================================
CHAIN_TO_TOOL_GOLDEN = [
    ("MOVE: read_your_state ladder.json",           "read_state",  {"name": "ladder.json"}),
    ("MOVE: read_your_state selfcheck.json",        "read_state",  {"name": "selfcheck.json"}),
    ("MOVE: read_your_state",                       "read_state",  {"name": "heartbeat.json"}),
    ("MOVE: know_yourself laws",                    "self_map",    {"topic": "laws"}),
    ("MOVE: know your hands",                       "list_tools",  {}),
    ("MOVE: what_to_try tool_missing",              "what_to_try", {"kind": "tool_missing"}),
    ("MOVE: my_record",                             "my_record",   {}),
    ("MOVE: read_your_state ../../../../etc/passwd", "read_state", {"name": "heartbeat.json"}),
    ("MOVE: read_your_state ZZQX-CANARY-DECOY",     "read_state",  {"name": "heartbeat.json"}),
    ("MOVE: read_your_state a_personal_store.json", "read_state",  {"name": "heartbeat.json"}),
]


def check_decision_chain():
    """Both parsers must agree, all the way to the argument dict a tool would be handed."""
    from aea.loop import aea as _wake
    from aea.kernel import decide as _decide
    fails = []
    for line, want_tool, want_args in CHAIN_TO_TOOL_GOLDEN:
        mv = _wake.move_from("some reasoning\n" + line)
        r, _why = _decide.parse({"move": mv})
        got_tool = (r or {}).get("tool")
        got_args = (r or {}).get("args")
        ok = got_tool == want_tool and got_args == want_args
        print("  chain     %-46s -> %-34s %s"
              % (line[6:52], "%s %s" % (got_tool, got_args), "ok" if ok else "FAIL"))
        if not ok:
            fails.append(("chain:" + line[6:40], "%s %s" % (got_tool, got_args),
                          "%s %s" % (want_tool, want_args)))
    return fails


if __name__ == "__main__":
    print("GOLDEN TRACE - scripted fuel, no network\n")
    f = (check_seats() + check_chains() + check_extraction() + check_carried() + check_probe()
         + check_kernel() + check_decision_chain())
    print()
    if f:
        print("%d FAILURES. Something changed what it does:" % len(f))
        for name, got, want in f:
            print("   %-28s got %s want %s" % (name, got, want))
        raise SystemExit(1)
    total = (len(GOLDEN) + len(CHAIN_GOLDEN) + len(EXTRACTION_GOLDEN) + len(WORK_GOLDEN)
             + len(CARRIED_GOLDEN) + 1
             # the kernel contracts: every think_off case, every published-parameter case, plus
             # unknown-model, the meter's ceiling, its slot release, and unmeasured's 410 rule
             + len(THINK_GOLDEN) + len(PARAM_GOLDEN) + 4
             # the decision chain, frozen end to end: three of these are hostile
             + len(CHAIN_TO_TOOL_GOLDEN))
    print("all %d frozen behaviours hold." % total)
    print("2 of them are frozen at a KNOWN-BAD value (METHOD defect 15). Fixing the reader is "
          "supposed to break this file.")
