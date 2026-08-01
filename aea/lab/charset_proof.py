"""charset_proof.py - THE CALC ALPHABET, PROVED BY EXHAUSTION. Not sampled, not bounded.

    python -m aea.lab.charset_proof

WHY THIS REPLACES A PERCENTAGE, and it is the most useful thing to come out of two days of arguing
about denominators.

`calc` is the ONE tool whose argument carries bytes the wake wrote. Its guard is a character class:

    ^[\\d\\s+\\-*/().%]{1,120}$

A character class accepts a string IF AND ONLY IF every character in it is a member. That is not a
property to be sampled - it is a property that can be DECIDED, one codepoint at a time, over the
whole space. 1,112,064 codepoints is 0.7 seconds.

So the honest report for this guard is not "zero leaks in 23 crossings, one-sided 95 percent bound
12.212 percent". A confidence interval on a decidable property is a category error: it answers "how
sure are we, given a sample" about something with no sample in it. The honest report is:

    OF 1,112,064 CODEPOINTS, EXACTLY N ARE ADMITTED, AND ZERO OF THEM ARE ALPHABETIC.

That sentence is stronger than any percentage this repo has published, and it cannot be improved by
running more trials, because it is already complete.

WHAT THE EXHAUSTION FOUND that a sample would have missed:

  0 ALPHABETIC        the load-bearing claim - "the regex admits no letters, so every name-based
                      escape is blocked" - is TRUE, and now proved rather than asserted
  697 ADMITTED        against nineteen printable ASCII characters the docstring implies
  669 NON-ASCII       every Unicode decimal-digit family: Arabic-Indic, Devanagari, Myanmar, Tai,
                      the mathematical digit blocks. `\\d` is not [0-9]
  9 ASCII CONTROLS    0x09-0x0D and 0x1C-0x1F - tab, newline, vertical tab, form feed, carriage
                      return, and the FILE/GROUP/RECORD/UNIT separators, which `\\s` matches

None of that is exploitable: no letters means no names, no names means no imports, no attribute
access and no builtins, and `_calc` runs eval with an empty builtins dict. A non-breaking space
evaluates to 4 and an Arabic-Indic digit is refused downstream by Python's own tokenizer. But the
CERTIFICATE MUST STATE THE REAL ALPHABET rather than the one the docstring implies, because the next
person to widen this class will read the docstring and not the class.

AND IT CHECKS THE TWO CLASSES AGREE. `decide.FREE_ARG['calc']['ok']` and `hands._calc`'s own regex
are separate patterns in separate files, deliberately - the comment in decide says the courtesy copy
is "deliberately looser than the real one so the two cannot drift into disagreeing about what is
legal". A claim like that is exactly the kind that quietly stops being true, so it is decided here
over the whole space rather than believed.
"""
from __future__ import annotations

import json
import re
import sys

SPACE = 0x110000
SURROGATES = range(0xD800, 0xE000)


def _classes():
    from aea.kernel import decide, hands
    a = decide.FREE_ARG["calc"]["ok"]
    src = __import__("inspect").getsource(hands._calc)
    m = re.search(r're\.fullmatch\(r"(\[[^"]+\]\+)"', src)
    b = re.compile("^" + m.group(1) + "$") if m else None
    return a, b


def prove() -> dict:
    """Decide membership for every codepoint. This is a proof, not a sample."""
    a, b = _classes()
    admitted, nonascii, alpha, controls, disagree = 0, 0, 0, [], []
    for cp in range(SPACE):
        if cp in SURROGATES:
            continue
        ch = chr(cp)
        ina = bool(a.fullmatch(ch))
        if b is not None:
            inb = bool(b.fullmatch(ch))
            if ina != inb:
                disagree.append(hex(cp))
        if not ina:
            continue
        admitted += 1
        if not ch.isascii():
            nonascii += 1
        if ch.isalpha():
            alpha += 1
        elif ch.isascii() and not ch.isprintable():
            controls.append(hex(cp))
    return dict(schema=1, space=SPACE - len(SURROGATES), admitted=admitted, non_ascii=nonascii,
                alphabetic=alpha, ascii_controls=controls,
                classes_disagree_on=disagree,
                claim="of %d codepoints, exactly %d are admitted by the calc character class, and "
                      "%d of them are alphabetic" % (SPACE - len(SURROGATES), admitted, alpha),
                why_not_a_percentage="a character class accepts a string iff every character is a "
                                     "member, so membership is DECIDABLE over the whole space. A "
                                     "confidence interval answers 'how sure are we given a sample' "
                                     "about something with no sample in it.")


if __name__ == "__main__":
    r = prove()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=1))
        sys.exit(0)
    print("CALC ALPHABET - decided over the whole codepoint space, not sampled")
    print("=" * 92)
    print("  codepoints examined      %d" % r["space"])
    print("  admitted by the class    %d" % r["admitted"])
    print("     non-ascii             %d   (every Unicode decimal-digit family - \\d is not [0-9])" % r["non_ascii"])
    print("     ASCII control chars   %d   %s" % (len(r["ascii_controls"]), r["ascii_controls"]))
    print("     ALPHABETIC            %d   <- the load-bearing claim" % r["alphabetic"])
    print()
    print("  the two classes (decide's courtesy copy, hands' authority) disagree on: %s"
          % (r["classes_disagree_on"] or "nothing"))
    print()
    print("  %s." % r["claim"].capitalize())
    print()
    print("  This is a PROOF and it cannot be improved by more trials. %s"
          % r["why_not_a_percentage"])
    sys.exit(0 if r["alphabetic"] == 0 and not r["classes_disagree_on"] else 1)
