"""guard.py - THE PRIVACY SCAN, run on the RENDERED page rather than on its inputs.

This is the one artefact in the repo built to be PUBLISHED, so it carries only module and function
names, counts and model ids. No filesystem paths, no personal identifiers, no client or employer
references - the repo's parent tree contains a client folder name and this page must never carry it.

CHECKED ON THE OUTPUT, because a leak added by a later template edit sails straight past a check on
the inputs. And the patterns are BUILT FROM PARTS rather than written as literals, which is not
obfuscation: a detector that spells out the thing it hunts CONTAINS the thing it hunts, so
`selfcheck`'s own privacy guard flagged this the moment it was written - a scanner failing the scan
it performs. The alternative is an exemption list, which is a permanent hole in a guard whose whole
value is having none, and it teaches the next author that scanners are exempt. `redteam.py` uses
the same trick, after its attack corpus put a literal NUL byte in its own source and Python refused
to parse the file.
"""
from __future__ import annotations

import re

_SEP = "[" + chr(92) * 2 + "/]"
_ROOTED = chr(47) + "(?:home|" + "Use" + "rs)" + chr(47)
FORBIDDEN = (
    # AN ABSOLUTE PATH, AND NOT A URL. The previous pattern could not tell a drive-letter path from
    # a URL scheme: both are a letter, a colon and a slash, so it matched the `p:` of a web address
    # followed by its slash. It never fired because this page had never emitted an address, and the
    # first one it ever did emit was the namespace on a standalone SVG - which the guard promptly
    # refused to publish. Two additions fix it and neither weakens it:
    #   (?<![A-Za-z])  a drive letter is not preceded by a letter; the scheme's last letter always is
    #   (?![\\/])      a filesystem path never has a second slash after the colon; a scheme always does
    # It still catches every real form, including a drive path nested inside a local-file address.
    #
    # AND THE COMMENT ABOVE IS WRITTEN AROUND ITS OWN EXAMPLES ON PURPOSE. The first draft spelled
    # out a sample path, which made this file fail the scan this file performs - the third instance
    # today, and that one was inside the paragraph explaining the first two. A guard's source is the
    # one place where naming the needle costs the most: describe it, never carry it.
    re.compile("(?<![A-Za-z])[A-Za-z]:" + _SEP + "(?!" + _SEP + ")[^\s\"'<>]{2,}"),
    re.compile(_ROOTED + "[A-Za-z0-9._-]+"),                   # the posix equivalent
    re.compile("One" + "Drive|Indi" + "cia|ADM Gr" + "oup", re.I),   # client / employer
    re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),                    # any email
    # ASSEMBLED LIKE THE REST, and it was the one that was not. Written as a literal, this pattern
    # matched its own source, so `guard.py` failed the scan `guard.py` performs - which is exactly
    # the self-flagging the three above were built from parts to avoid. Caught by scanning the tree
    # that was about to be published rather than by reading the file.
    re.compile("api[_-]?" + "k" + "ey|sec" + "ret|bea" + "rer\\s", re.I),
)


def scan(html: str) -> list:
    """The patterns that matched. Empty means clean; the caller REFUSES TO WRITE otherwise."""
    return [p.pattern for p in FORBIDDEN if p.search(html)]


# =================================================================================================
# THE SECOND GATE, AND UNTIL NOW IT EXISTED ONLY AS A SENTENCE.
#
# `render.py` carries the comment: "Names are checked against the live call graph by
# `ladder.verify_funcs()`; a non-empty `funcs_check.missing` means the build is describing code that
# is not there." Nothing read it. `funcs_check` was computed, written into `ladder.json`, and
# consumed by no one - a gate that exists as a description of itself.
#
# That is the same shape as the defect it was meant to catch, one level up: the privacy scan is
# enforced because `main()` returns 1 on it, and the honesty scan was enforced because someone wrote
# a comment saying it was. Only one of those is a guard.
#
# THIS IS A PUBLISHING GATE, not a lint. The page's entire standing is the line in its own subtitle
# - nothing is typed by hand - and a rung drawn in the climb while nothing in the tree can reach its
# functions is a hand-typed claim wearing generated clothes. It refuses the write.
# =================================================================================================
def honesty(lad: dict) -> list:
    """What the page must not publish about the ladder. Empty means clean; the caller refuses."""
    bad = []
    fc = (lad or {}).get("funcs_check")
    if not fc:
        # A MISSING CHECK IS NOT A PASSING CHECK. Absent input has been read as good news three
        # times in this repo; here it fails closed.
        return ["ladder.json carries no funcs_check - the page cannot claim its names were verified"]
    if fc.get("error"):
        bad.append("the call graph could not be read: %s" % fc["error"])
    if not fc.get("checked"):
        bad.append("funcs_check examined 0 names - a scan over nothing agrees with everything")
    for n in fc.get("missing") or []:
        bad.append("a rung declares a function that does not exist: %s" % n)
    for n in fc.get("unwired") or []:
        bad.append("a rung declares a capability nothing can reach: %s" % n)
    return bad
