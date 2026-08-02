"""python -m aea.tooling.page - build the page, scan it, write it only if it is clean."""
from __future__ import annotations

import os
import sys

from aea.tooling.page import guard, sources
from aea.tooling.page.render import build
from aea.tooling.page.sources import OUT

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    html = build()
    bad = guard.scan(html)
    if bad:
        print("REFUSING TO WRITE - the page carries something that must never be published:")
        for b in bad:
            print("   " + b)
        return 1
    # THE HONESTY GATE, which existed as a comment in render.py and as nothing else. A rung drawn in
    # the climb while nothing in the tree reaches its functions is a hand-typed claim in generated
    # clothes, and the page's whole standing is that nothing on it is typed by hand.
    lies = guard.honesty(sources.load("ladder.json", {}))
    if lies:
        print("REFUSING TO WRITE - the page would claim something the tree does not support:")
        for b in lies:
            print("   " + b)
        print("   Fix the wiring or drop the declaration. Do not exempt the check.")
        return 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(html)
    print("wrote %s  (%dKB, privacy scan clean, ladder claims wired)" % (OUT, len(html) // 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
