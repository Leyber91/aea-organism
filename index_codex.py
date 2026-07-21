"""index_codex.py - THE WHOLE BOOK OF LUIS, indexed: his real documents (the TRIVERSE CODEX,
the portfolio masters, the AEA briefs) chunked + embedded LOCALLY into codex_index.json, so the
entity reaches his ACTUAL writing when he talks to it - not just the distilled summary book.

Privacy: everything embeds on local Ollama; recall chunks are injected only into private-zone
(no-train) or local prompts, same doctrine as the seed. The index is gitignored.

  python index_codex.py               # (re)index all roots (incremental: skips unchanged files)
  python index_codex.py --recall "what is the Witness Debt?"
  python index_codex.py --board
"""
from __future__ import annotations
import json, os, sys, glob, re, time
import grid, pulse
from consolidate import embed, _cos     # the same local embedding organ

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

INDEX = os.path.join(grid.HERE, "codex_index.json")
CHUNK, OVERLAP, MAX_PER_FILE = 900, 150, 60

ROOTS = [
    # (label, glob, cap_files)  - the canonical book of him, broad but bounded
    ("triverse-codex", "<REDACTED-PATH>/Desktop/TRIVERSE/CODEX/**/*.md", 120),
    ("triverse-core",  "<REDACTED-PATH>/Desktop/TRIVERSE/CORE/**/*.md", 40),
    ("portfolio",      "<REDACTED-PATH>/<REDACTED-PATH>/Documents/PORTFOLIO/*.md", 30),
    ("aea-city",       os.path.join(grid.HERE, "*.md"), 20),
]


def load_index() -> dict:
    return grid.load_json(INDEX, {"files": {}, "chunks": []})

def save_index(ix: dict):
    grid.atomic_save_json(INDEX, ix)


def chunk_text(text: str) -> list[str]:
    text = re.sub(r"\n{3,}", "\n\n", text)
    out, i = [], 0
    while i < len(text) and len(out) < MAX_PER_FILE:
        piece = text[i:i + CHUNK]
        out.append(" ".join(piece.split()))
        i += CHUNK - OVERLAP
    return [c for c in out if len(c) > 120]


def index():
    ix = load_index()
    t0, added, skipped, files_done = time.time(), 0, 0, 0
    for label, pattern, cap in ROOTS:
        paths = sorted(glob.glob(pattern, recursive=True))[:cap]
        print(f"[{label}] {len(paths)} files")
        for path in paths:
            try:
                mtime = os.path.getmtime(path)
                key = path.lower()
                if ix["files"].get(key) == mtime:
                    skipped += 1; continue                     # unchanged since last index
                text = open(path, encoding="utf-8", errors="ignore").read()
                name = os.path.basename(path)
                ix["chunks"] = [c for c in ix["chunks"] if c["file"].lower() != key]   # re-index clean
                for ch in chunk_text(text):
                    ix["chunks"].append({"text": ch, "emb": embed(ch), "file": key,
                                         "name": name, "src": label})
                    added += 1
                ix["files"][key] = mtime
                files_done += 1
                if files_done % 5 == 0:
                    save_index(ix)                             # crash-safe progress
                    print(f"  ...{files_done} files, {added} chunks, {round(time.time()-t0)}s")
            except Exception as e:
                print(f"  ! {os.path.basename(path)}: {str(e)[:60]}")
    save_index(ix)
    pulse.emit("memory", "codex-indexed", f"+{added} chunks from {files_done} files ({skipped} unchanged)")
    print(f"\nINDEXED: +{added} chunks from {files_done} files ({skipped} unchanged) "
          f"-> {len(ix['chunks'])} total in {round((time.time()-t0)/60,1)} min")


def recall(query: str, k: int = 3) -> list[str]:
    ix = load_index()
    if not ix["chunks"]:
        return []
    q = embed(query)
    top = sorted(ix["chunks"], key=lambda c: -_cos(q, c["emb"]))[:k]
    pulse.emit("memory", "codex-recall", query[:70])
    return [f"[{c['name']}] {c['text'][:500]}" for c in top]


def board():
    ix = load_index()
    by = {}
    for c in ix["chunks"]:
        by[c["src"]] = by.get(c["src"], 0) + 1
    print(f"CODEX INDEX: {len(ix['chunks'])} chunks from {len(ix['files'])} files")
    for s, n in sorted(by.items()):
        print(f"  {s:16} {n} chunks")


if __name__ == "__main__":
    a = sys.argv
    if "--recall" in a:
        for r in recall(a[a.index("--recall") + 1]):
            print(" -", r[:220], "\n")
    elif "--board" in a:
        board()
    else:
        index()
