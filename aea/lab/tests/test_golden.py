"""THE ADDITION LAW, APPLIED TO OURSELVES. No network, no cost, exactly reproducible.

Every refactor today was verified by running `import`, which is a control that contains the
treatment: importing proves nothing about behaviour. This file freezes what each seat DOES on a
scripted fuel, so a part that silently subtracts a capacity fails here instead of six commits later.

It exists because the parts refactor moved the naive stated-read into Validation, and an organism
with no guard silently stopped answering at all. Nothing caught it.

Run: python -m aea.lab.tests.test_golden
"""
from __future__ import annotations

from aea.lab.organism import Organism
from aea.lab.parts.fuel import ScriptedFuel

TASK = {"id": "t", "data": "the mouth draws power", "goal": "Count the words.",
        "method": "Number each token, then give the count.", "truth": 4}

WORKED = "1. the\n2. mouth\n3. draws\n4. power\nThe count is 4."
BARE = "4"
MUTE = "1. the\n2. mouth\n3. draws\n4. power\nThe answer is 9."
NOISY = "Between 3 and 5, likely 4 or maybe 6."

# seat -> reply -> (answer, read_by). Frozen. A change here is a capability change and must be argued.
GOLDEN = [
    (["call"], BARE, 4, "stated"),
    (["call"], WORKED, 4, "stated"),
    (["call", "readout"], MUTE, 4, "work:enumerated"),
    (["call", "goal", "frame", "readout"], WORKED, 4, "work:enumerated"),
    (["call", "validation"], BARE, 4, "stated"),
    (["call", "validation"], NOISY, None, "declined"),
    (["call", "readout", "validation"], NOISY, None, "declined"),
]


def check():
    fails = []
    for seat, reply, want_answer, want_read in GOLDEN:
        o = Organism(seat, ("fake", "rod"))
        r = o.run(TASK, fuel=ScriptedFuel([reply]))
        got = (r["answer"], r["read_by"])
        ok = got == (want_answer, want_read)
        print("  %-42s %-22s -> %-18s %s"
              % ("+".join(seat), reply.splitlines()[-1][:21], str(got), "ok" if ok else "FAIL"))
        if not ok:
            fails.append((seat, reply, got, (want_answer, want_read)))
    return fails


if __name__ == "__main__":
    print("GOLDEN TRACE - scripted fuel, no network\n")
    f = check()
    print()
    if f:
        print("%d FAILURES. A seat changed what it does:" % len(f))
        for seat, _, got, want in f:
            print("   %-40s got %s want %s" % ("+".join(seat), got, want))
        raise SystemExit(1)
    print("all %d seats behave as frozen." % len(GOLDEN))
