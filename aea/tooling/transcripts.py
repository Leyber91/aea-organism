"""transcripts.py - READ BACK EVERY COUNCIL AND EVERY CONVERSATION THIS MACHINE HAS HELD.

Luis, 2026-07-30: "remember to record all these interactions and councils in json logs, I would
love to see the transcripts."

He is right that they were being lost, and the way they were being lost is worth recording: the
council wrote `last.json` and OVERWROTE IT every run. Every argument held before the most recent
one was destroyed by the next one. The summary survived and the transcript did not - which is
exactly backwards, because a council's conclusion can be regenerated in ninety seconds and the
argument that produced it cannot. WHICH position moved, and what moved it, only exists in the
transcript.

Same defect in the party: `party.json`, one file, overwritten. Twenty-two conversations were held
and one survives.

WHAT THIS DOES. Lists what exists, prints one back in full, and renders a local HTML page for
reading properly. The HTML is written to disk and opened by hand - it is NEVER published anywhere,
because these transcripts contain whatever was actually discussed, and this session's councils
have already talked about Luis's debt and his working hours. A reader that quietly uploads is a
worse defect than a reader that does not exist.

    python -m aea.tooling.transcripts                 what is on disk
    python -m aea.tooling.transcripts --show 3        print the 3rd-newest in full
    python -m aea.tooling.transcripts --html          write a local page and say where it is
    python -m aea.tooling.transcripts --grep "money"  every turn matching, across everything
"""
from __future__ import annotations

import glob
import html
import json
import os
import re
import sys

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

COUNCIL = os.path.join(str(grid.STATE), "council", "runs")
ROSTERS = os.path.join(str(grid.STATE), "council", "rosters")
PARTY = os.path.join(str(grid.STATE), "lab", "party")
PAGE = os.path.join(str(grid.STATE), "council", "transcripts.html")


def _load(p: str) -> dict:
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return {}


def runs() -> list:
    """Everything on disk, newest first, normalised into one shape so a council and a conversation
    can be read side by side."""
    out = []
    for p in sorted(glob.glob(os.path.join(COUNCIL, "*.json")), reverse=True):
        d = _load(p)
        if not d:
            continue
        out.append(dict(kind="council", path=p, at=d.get("at", ""),
                        title=(d.get("question") or "")[:150],
                        seats=d.get("seats") or [], log=d.get("log") or {},
                        agreement=d.get("agreement") or {}, moved=d.get("moved") or {},
                        rounds=d.get("rounds", 0), seconds=d.get("seconds", 0)))
    seen_turns = set()
    for p in sorted(glob.glob(os.path.join(PARTY, "runs", "*.json"))
                    + glob.glob(os.path.join(PARTY, "party.json")), reverse=True):
        d = _load(p)
        if not d.get("turns"):
            continue
        # `party.json` is a COPY of the newest stamped run, so without this the most recent
        # conversation appears twice and the list quietly lies about how many were held.
        key = (d.get("at", ""), len(d["turns"]), d["turns"][0]["text"][:60])
        if key in seen_turns:
            continue
        seen_turns.add(key)
        out.append(dict(kind="party", path=p, at=d.get("at", ""),
                        title=f"{len(d['turns'])} turns, "
                              f"{len({t['who'] for t in d['turns']})} speakers",
                        turns=d["turns"], impressions=d.get("impressions") or {}))
    out.sort(key=lambda r: r.get("at", ""), reverse=True)
    return out


def show(r: dict, width: int = 96) -> str:
    L = ["=" * width, f"{r['kind'].upper()}   {r.get('at', '')}", "=" * width]
    if r["kind"] == "council":
        L.append(f"\nTHE QUESTION\n  {r['title']}")
        if r["seats"]:
            L.append("\nWHO WAS IN THE ROOM")
            for s in r["seats"]:
                L.append(f"  {s.get('name', '?'):14s} {s.get('tier', ''):7s}"
                         + ("  HELD" if s.get("held") else ""))
                seed = (s.get("seed") or "").split("\n")[0]
                if seed:
                    L.append(f"       {seed[:150]}")
        rounds = max((len(v) for v in r["log"].values()), default=0)
        for i in range(rounds):
            L.append(f"\n{'-' * width}\nROUND {i + 1}"
                     + ("   (independent)" if i == 0 else "   (having read each other)"))
            for name, turns in r["log"].items():
                if i < len(turns):
                    L.append(f"\n  {name}")
                    for para in turns[i].split("\n"):
                        if para.strip():
                            L.append("       " + para.strip())
        if r["agreement"]:
            L.append(f"\n{'-' * width}\nWHERE THEY LANDED")
            L.append("  overlap  " + "  ".join(f"{k} {v}" for k, v in r["agreement"].items()))
            if r["moved"]:
                L.append("  moved    " + "  ".join(f"{k} {v}" for k, v in r["moved"].items())
                         + "   (vocabulary, not position - go and read both rounds)")
    else:
        L.append("")
        for i, t in enumerate(r["turns"], 1):
            L.append(f"  [{i:02d}] {t['who']}")
            L.append(f"       {t['text']}")
        if r.get("impressions"):
            L.append(f"\n{'-' * width}\nWHAT EACH ONE ENDED UP THINKING")
            for who, imps in r["impressions"].items():
                for other, imp in (imps or {}).items():
                    txt = imp.get("text", imp) if isinstance(imp, dict) else imp
                    L.append(f"  {who:8s} of {other:8s} {str(txt)[:110]}")
    return "\n".join(L)


def page(rs: list) -> str:
    """A local HTML page. Written to disk, opened by hand, never uploaded - see the header."""
    e = html.escape
    P = ["<meta charset='utf-8'><title>transcripts</title>", "<style>",
         "body{background:#0b0b0b;color:#c9c9c9;font:14px/1.6 'IBM Plex Mono',Consolas,monospace;",
         "max-width:52rem;margin:2rem auto;padding:0 1.2rem;font-variant-numeric:tabular-nums}",
         "h1{color:#d4a24c;font-size:15px;letter-spacing:.14em;text-transform:uppercase}",
         "h2{color:#ffb000;font-size:14px;margin:2.6rem 0 .3rem;border-top:1px solid #222;",
         "padding-top:1.2rem}",
         ".q{color:#e8e8e8;margin:.2rem 0 1rem}.meta{color:#666;font-size:12px}",
         ".seat{color:#8ab4d8;margin-top:1.1rem}.held{color:#d4a24c}",
         ".r{color:#666;font-size:12px;letter-spacing:.1em;margin-top:1.6rem}",
         "p{margin:.35rem 0 .35rem 1.4rem;white-space:pre-wrap}",
         ".who{color:#8ab4d8;margin:.9rem 0 0}.land{color:#777;font-size:12px;margin-top:1rem}",
         "</style>", f"<h1>transcripts &mdash; {len(rs)} on disk</h1>",
         "<div class=meta>local file, never uploaded. every council and conversation this machine "
         "has held.</div>"]
    for r in rs:
        P.append(f"<h2>{e(r['kind'])} &middot; {e(r.get('at', ''))}</h2>")
        if r["kind"] == "council":
            P.append(f"<div class=q>{e(r['title'])}</div>")
            for s in r["seats"]:
                cls = "seat held" if s.get("held") else "seat"
                P.append(f"<div class='{cls}'>{e(s.get('name', '?'))} "
                         f"<span class=meta>{e(s.get('tier', ''))}"
                         + ("  HELD" if s.get("held") else "") + "</span></div>")
                P.append(f"<p class=meta>{e((s.get('seed') or '').split(chr(10))[0][:220])}</p>")
            rounds = max((len(v) for v in r["log"].values()), default=0)
            for i in range(rounds):
                P.append(f"<div class=r>ROUND {i + 1}"
                         + (" &mdash; independent" if i == 0 else " &mdash; having read each other")
                         + "</div>")
                for name, turns in r["log"].items():
                    if i < len(turns):
                        P.append(f"<div class=who>{e(name)}</div><p>{e(turns[i])}</p>")
            if r["agreement"]:
                P.append("<div class=land>overlap &nbsp;"
                         + "&nbsp; ".join(f"{e(k)} {v}" for k, v in r["agreement"].items())
                         + "</div>")
        else:
            P.append(f"<div class=q>{e(r['title'])}</div>")
            for t in r["turns"]:
                P.append(f"<div class=who>{e(t['who'])}</div><p>{e(t['text'])}</p>")
    return "\n".join(P)


def main() -> None:
    a = sys.argv[1:]
    rs = runs()
    if not rs:
        print("nothing on disk yet - run `python -m aea.mind.council \"...\"`")
        return
    if "--grep" in a:
        pat = re.compile(a[a.index("--grep") + 1], re.I)
        n = 0
        for r in rs:
            src = ([(k, t) for k, v in r.get("log", {}).items() for t in v]
                   if r["kind"] == "council" else
                   [(t["who"], t["text"]) for t in r.get("turns", [])])
            for who, txt in src:
                if pat.search(txt):
                    n += 1
                    print(f"\n  {r['at']}  {r['kind']}  {who}")
                    for m in pat.finditer(txt):
                        s = max(0, m.start() - 120)
                        print(f"       ...{txt[s:m.end() + 160].strip()}...")
                        break
        print(f"\n  {n} match(es) across {len(rs)} transcript(s)")
        return
    if "--html" in a:
        os.makedirs(os.path.dirname(PAGE), exist_ok=True)
        open(PAGE, "w", encoding="utf-8").write(page(rs))
        print(f"  wrote {len(rs)} transcript(s) -> {PAGE}")
        print("  local file. open it in a browser; it is not published anywhere.")
        return
    if "--show" in a:
        i = int(a[a.index("--show") + 1]) - 1
        if 0 <= i < len(rs):
            print(show(rs[i]))
        else:
            print(f"  only {len(rs)} on disk")
        return
    print(f"{'#':>3}  {'when':19s} {'kind':8s} {'':4s} what")
    for i, r in enumerate(rs, 1):
        extra = (f"{len(r.get('seats', []))} seats" if r["kind"] == "council"
                 else f"{len(r.get('turns', []))} turns")
        print(f"{i:3d}  {r.get('at', ''):19s} {r['kind']:8s} {extra:9s} {r['title'][:60]}")
    print(f"\n  --show N to read one, --html for a page, --grep PATTERN to search all of them")


if __name__ == "__main__":
    main()
