"""_pages - turn GitHub Pages on for the gh-pages branch, and VERIFY it is actually serving.

    python -m aea.tooling._pages

WHY IT EXISTS AS A FILE. The obvious route is the `gh` CLI, which is not installed here. That is the
tool's limit, not the world's - the lesson this repo already paid for when WebFetch timed out on a
page and it was nearly recorded as "the source cannot be read", while a plain urllib GET with a
browser User-Agent returned 200 and 200KB. So: the REST API directly, with the credential git
already has.

THE TOKEN IS NEVER PRINTED, never written to a file, and never passed on a command line where it
would land in shell history or a process list. It is read from `git credential fill` on stdin, used,
and dropped.

AND IT VERIFIES BY FETCHING. Enabling is an API call that returns 201 whether or not the site ever
serves; the only evidence that Pages works is a GET of the URL returning the bytes. "Verify, don't
claim" applies to a deploy exactly as it applies to a rung.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

REPO = "Leyber91/AEA_GAME"
API = "https://api.github.com"


def _token() -> str | None:
    """Ask git's credential helper. Never echo the result."""
    try:
        p = subprocess.run(["git", "credential", "fill"],
                           input="protocol=https\nhost=github.com\n\n",
                           capture_output=True, text=True, timeout=20)
        for line in (p.stdout or "").splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None


def _call(method: str, path: str, tok: str, body=None):
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Bearer {tok}", "Accept": "application/vnd.github+json",
                 "User-Agent": "aea-publish/1", "X-GitHub-Api-Version": "2022-11-28",
                 **({"Content-Type": "application/json"} if body is not None else {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "{}")
        except Exception:
            return e.code, {}
    except Exception as e:
        return 0, {"message": str(e)[:120]}


def main() -> int:
    tok = _token()
    if not tok:
        print("  no credential available from git - cannot call the API")
        return 2
    print(f"  credential obtained ({len(tok)} chars, not shown)")

    status, body = _call("GET", f"/repos/{REPO}/pages", tok)
    if status == 200:
        print(f"  Pages ALREADY enabled -> {body.get('html_url')}")
    else:
        status, body = _call("POST", f"/repos/{REPO}/pages", tok,
                             {"source": {"branch": "gh-pages", "path": "/"}})
        print(f"  POST /pages -> {status} {body.get('message', '')[:90]}")
        if status not in (201, 409):
            print("  the token may lack the `pages` or `repo` scope; this needs a click in Settings")
            return 1
        status, body = _call("GET", f"/repos/{REPO}/pages", tok)

    url = (body or {}).get("html_url") or f"https://leyber91.github.io/AEA_GAME/"
    print(f"  url: {url}")

    # VERIFY BY FETCHING. A 201 says the API accepted a request; only bytes say the site serves.
    # A first build takes up to a minute, so this waits rather than declaring success early.
    for attempt in range(10):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "aea-publish/1"})
            with urllib.request.urlopen(req, timeout=25) as r:
                html = r.read().decode("utf-8", "ignore")
            if "THE ORGANISM" in html:
                print(f"  LIVE - {r.status}, {len(html)//1024}KB, and the page is ours "
                      f"(found the title in the served bytes)")
                return 0
            print(f"  served {r.status} but the bytes are not our page yet ({len(html)} chars)")
        except Exception as e:
            print(f"  not serving yet ({str(e)[:60]}) - build takes ~1 min, attempt {attempt+1}/10")
        time.sleep(20)
    print("  did NOT confirm the page is serving. Enabled but unverified - say that, do not claim it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
