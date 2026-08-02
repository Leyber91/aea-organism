"""python -m aea.tooling.page - build the SITE, scan every file, write only if all of them pass.

THE GUARD NOW COVERS WHAT IT CLAIMS TO. It scanned one string, because there used to be one file.
The moment the page became a site, scanning `index.html` alone would be a privacy guard reading a
quarter of what it publishes while reporting on all of it - the same shape as a scan over an empty
tree agreeing with everything. Every file is scanned before any file is written, and it is all or
nothing on purpose: a half-written site is a page whose stylesheet describes marks that are not
there.

WHAT ACTUALLY RUNS WHERE, because publishing the generator invites the wrong assumption. GitHub
Pages is a static file server: it serves bytes and executes nothing. `index.html`, `assets/*.css`,
`assets/*.js` and `assets/field.svg` are served and run in the reader's browser. The Python that
produced them runs HERE, on this machine, and is published beside the output as provenance - source
to read, never source that executes. Anything the page states was computed before it was uploaded.
"""
from __future__ import annotations

import os
import sys

from aea.tooling.page import guard, sources
from aea.tooling.page.render import build_site

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    site = build_site()

    leaks = {name: guard.scan(text) for name, text in site.items() if guard.scan(text)}
    if leaks:
        print("REFUSING TO WRITE - the site carries something that must never be published:")
        for name, pats in sorted(leaks.items()):
            for p in pats:
                print("   %s: %s" % (name, p))
        return 1

    # WELL-FORMEDNESS: every file must parse as the type its name claims. See guard.parses.
    broken = [msg for name, text in site.items() for msg in guard.parses(name, text)]
    if broken:
        print("REFUSING TO WRITE - the build produced a file that is not what its name says:")
        for b in broken:
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

    root = os.path.dirname(sources.OUT)
    written = []
    for name, text in site.items():
        path = os.path.join(root, *name.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(text)
        written.append((name, len(text), text.count("\n") + 1))

    print("wrote %d files, %dKB total (privacy scan clean, ladder claims wired)"
          % (len(written), sum(n for _f, n, _l in written) // 1024))
    for name, n, lines in sorted(written, key=lambda x: -x[1]):
        print("   %-20s %7d bytes %6d lines" % (name, n, lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
