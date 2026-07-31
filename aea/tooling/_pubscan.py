"""_pubscan - the last gate before bytes go public. Run as a FILE, never through a shell.

Written because the same scan was attempted three times inline and the shell ate the backslashes
every time - `\\\\Users` arrived as `\\U`, an invalid escape, and the check crashed instead of
running. CLAUDE.md already carries the rule ("never test a regex or a path through a shell heredoc;
write the test to a real file and run the file") and it was ignored three times in one hour on the
one check whose failure mode is publishing a client's name to the internet.

    python -m aea.tooling._pubscan <path>     exit 0 = clean, exit 1 = do not publish
"""
from __future__ import annotations

import re
import sys

FORBIDDEN = {
    "absolute path": re.compile(r"[A-Za-z]:[\\/]{1,2}Users[\\/]|/home/[a-z]+/"),
    "client/employer": re.compile(r"OneDrive|<REDACTED-EMPLOYER>|<REDACTED-EMPLOYER>", re.I),
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w]{2,}"),
    "api key": re.compile(r"(sk-|gsk_|nvapi-)[A-Za-z0-9]{12,}"),
    "private store": re.compile(r"luis_memory|converse_|private_today", re.I),
}


def scan(path: str) -> list:
    text = open(path, encoding="utf-8", errors="replace").read()
    return [(name, m.group(0)[:70]) for name, pat in FORBIDDEN.items()
            for m in pat.finditer(text)]


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
    hits = scan(target)
    size = len(open(target, encoding="utf-8", errors="replace").read())
    print(f"  {target}  {size // 1024} KB")
    if hits:
        print(f"  REFUSING: {len(hits)} thing(s) that must never be published")
        for name, what in hits[:20]:
            print(f"     {name}: {what}")
        sys.exit(1)
    print(f"  clean against {len(FORBIDDEN)} patterns - safe to publish")
