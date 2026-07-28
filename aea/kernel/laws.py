"""laws.py - THE LAWS, LOADABLE. One file the entity reads about how to behave, not what to do.

`design/THE_LAWS.md` is the source. This is the only way to get it into a prompt, so there is exactly
one copy and it cannot drift from the version a human reads.

WHY IT IS A FILE AND NOT A CONSTANT IN CODE. A law that lives in a docstring is discoverable by
whoever opens that module and nobody else. Thirty-odd rules were earned across one session and they
were scattered across nine modules, a session log, and three memory files. A rule nobody can retrieve
at the moment of judgment is not a rule, it is a note - and that is itself law W6.

WHY THE WHOLE THING IS NOT ALWAYS SENT. It costs tokens on every wake, which is the correct pressure
against the file becoming a wish list. `for_zone` sends the sections that bear on the work at hand;
`text()` sends everything when something is genuinely deciding how to act.

  python -m aea.kernel.laws            the laws, as the entity receives them
  python -m aea.kernel.laws --section IV
"""
from __future__ import annotations

import os
import re
import sys

from aea.kernel import grid

PATH = os.path.join(grid.ROOT, "design", "THE_LAWS.md")

# Which sections bear on which kind of work. A wake producing a brief does not need the structure
# laws; a wake proposing a change to its own source needs all of them.
FOR = {
    "produce": ("I", "IV"),
    "measure": ("I", "II"),
    "act": ("I", "III", "IV"),
    "unstick": ("I", "II", "V"),
    "self_modify": ("I", "II", "III", "IV", "V", "VI"),
    "all": ("I", "II", "III", "IV", "V", "VI", "VII"),
}
_ROMAN = ("I", "II", "III", "IV", "V", "VI", "VII")


def text() -> str:
    """The whole file. Returns a plain marker rather than raising if it is missing, because a wake
    must not die because a document moved."""
    try:
        with open(PATH, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return "[THE_LAWS.md unavailable: %s]" % str(e)[:80]


def sections() -> dict:
    """Split on the `## <roman> - NAME` headings. Keyed by the numeral."""
    body = text()
    out, cur, buf = {}, None, []
    for line in body.splitlines():
        m = re.match(r"^##\s+([IVX]+)\s+-\s+(.+)$", line.strip())
        if m:
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1), [line]
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out


def for_zone(kind: str = "all") -> str:
    """The sections that bear on this kind of work, as a prompt block.

    An unknown kind returns EVERYTHING rather than nothing. That direction is deliberate: the failure
    of sending too many laws is a token cost, and the failure of sending none is a system acting
    without them.
    """
    want = FOR.get(kind, FOR["all"])
    have = sections()
    parts = [have[r] for r in want if r in have]
    if not parts:
        return text()
    return ("THE LAWS THIS SYSTEM OPERATES UNDER. Each was earned by a real failure; none is a "
            "preference. They bind you.\n\n" + "\n\n".join(parts))


def count() -> int:
    return len(re.findall(r"^\*\*[A-Z]\d+\.", text(), re.M))


if __name__ == "__main__":
    if "--section" in sys.argv:
        print(sections().get(sys.argv[sys.argv.index("--section") + 1], "(no such section)"))
    elif "--for" in sys.argv:
        print(for_zone(sys.argv[sys.argv.index("--for") + 1]))
    else:
        s = sections()
        print("THE LAWS: %d laws in %d sections, %d chars (~%d tokens if sent whole)"
              % (count(), len(s), len(text()), len(text()) // 4))
        for r in _ROMAN:
            if r in s:
                head = s[r].splitlines()[0].replace("## ", "")
                n = len(re.findall(r"^\*\*[A-Z]\d+\.", s[r], re.M))
                print("  %-4s %-16s %2d laws  %5d chars" % (r, head.split(" - ")[-1], n, len(s[r])))
        print()
        print("for a wake that produces:      %5d chars" % len(for_zone("produce")))
        print("for a wake that acts:          %5d chars" % len(for_zone("act")))
        print("for a self-modification:       %5d chars" % len(for_zone("self_modify")))
