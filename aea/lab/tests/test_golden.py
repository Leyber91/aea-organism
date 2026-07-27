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
]

# SEQUENCES, NOT ONLY TRIALS. The trial cases above missed a regression because the checkpoint
# instruction appends "step=1" AFTER the answer and the naive last-number read took the step index.
CHAIN_GOLDEN = [
    ("none", ["48377", "48364"], [48377, 48364]),
    ("checkpoint", ["48377\nSTATE: value=48377, step=1",
                    "48364\nSTATE: value=48364, step=2"], [48377, 48364]),
    ("free", ["48377\nNOTE: watch for 99 later",
              "48364\nNOTE: 12 steps to go"], [48377, 48364]),
]


def check_seats():
    fails = []
    for seat, reply, want_a, want_r in GOLDEN:
        r = Organism(seat, ("fake", "rod")).run(TASK, fuel=ScriptedFuel([reply]))
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


if __name__ == "__main__":
    print("GOLDEN TRACE - scripted fuel, no network\n")
    f = check_seats() + check_chains()
    print()
    if f:
        print("%d FAILURES. Something changed what it does:" % len(f))
        for name, got, want in f:
            print("   %-28s got %s want %s" % (name, got, want))
        raise SystemExit(1)
    print("all %d frozen behaviours hold." % (len(GOLDEN) + len(CHAIN_GOLDEN)))
