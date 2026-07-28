"""site.py - THE EVIDENCE SITE. Builds web/lab/ from the archive. Data-driven, not baked.

WHY THIS REPLACES THE ONE-FILE REPORT. A 500KB page with the numbers baked into it is a SNAPSHOT:
it is stale the moment the next cell lands, it cannot be read by anything but a human, and adding an
experiment means regenerating the whole thing. This builds a MANIFEST plus one JSON per run, and the
page discovers what exists at load time. An experiment that produces evidence tomorrow gets its
section tomorrow, with no edit to any HTML.

THE HONESTY LAW APPLIES TO THE SITE ITSELF. An experiment with no stored replies does not vanish
from the index and does not render as a blank. It renders as a NAMED GAP that states what is missing
and the exact command that would fill it. A missing measurement is information.

THE CONVENTIONS ARE DECLARED IN THE MANIFEST so tooling never guesses a path:

  evidence   state/lab/runs/<experiment>/<run_id>.json      canonical, append-only, never edited
  site data  web/lab/data/<experiment>/<run_id>.json        trimmed for the browser
  latest     web/lab/data/<experiment>/latest.json          pointer copy
  index      web/lab/data/index.json                        the manifest

  experiment  x<NN>[letter]_<slug>          run  <YYYYMMDD>T<HHMMSS>Z

  python -m aea.lab.site            build
  python -m aea.lab.site --serve    build, then serve on 7801
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time

from aea.kernel import grid

SCHEMA = "aea.lab.site/1"
MAX_REPLIES_PER_RUN = 300      # capped for the browser; the count omitted is written into the file
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "site_assets")


def runs_root():
    return os.path.join(grid.STATE, "lab", "runs")


def site_root():
    return os.path.join(grid.WEB, "lab")


def experiments():
    d = runs_root()
    return sorted(e for e in os.listdir(d) if os.path.isdir(os.path.join(d, e))) \
        if os.path.isdir(d) else []


def run_files(experiment):
    d = os.path.join(runs_root(), experiment)
    return sorted(f[:-5] for f in os.listdir(d) if f.endswith(".json")) if os.path.isdir(d) else []


def _texts(doc):
    """Every stored reply in a run, whatever shape it was stored in. Three regimes exist and this
    is the one place that knows all three, so nothing downstream has to."""
    out = []

    def rec(x, ctx):
        if isinstance(x, dict):
            c = dict(ctx)
            for key in ("form", "rod", "arm", "chain", "sample", "step", "trial"):
                if key in x and not isinstance(x[key], (dict, list)):
                    c[key] = x[key]
            body = x.get("text") if isinstance(x.get("text"), str) else None
            if body is None and isinstance(x.get("raw"), str):
                body = x["raw"]
            if body is not None:
                out.append({"ctx": c, "text": body,
                            "truth": x.get("truth"), "value": x.get("value"),
                            "anchored": x.get("anchored"), "read_by": x.get("read_by"),
                            "hit": x.get("hit_anchored", x.get("hit", x.get("passed"))),
                            "parse_fail": x.get("parse_fail"),
                            "read_disagrees": x.get("read_disagrees"),
                            "flags": x.get("flags") or []})
            for v in x.values():
                rec(v, c)
        elif isinstance(x, list):
            for v in x:
                rec(v, ctx)
    rec(doc, {})
    return out


def regime(doc):
    """FULL, TAIL or NONE. TAIL is the 320-character slice that produced four recorded defects."""
    has_full = has_tail = False

    def rec(x):
        nonlocal has_full, has_tail
        if isinstance(x, dict):
            if isinstance(x.get("text"), str):
                has_full = True
            if isinstance(x.get("raw"), str):
                has_tail = True
            for v in x.values():
                rec(v)
        elif isinstance(x, list):
            for v in x:
                rec(v)
    rec(doc)
    return "FULL" if has_full else "TAIL" if has_tail else "NONE"


def trim(doc):
    """One run, shaped for the browser. Cells in full; replies capped with the omission stated."""
    rows = [r for r in doc.get("rows", []) if r.get("kind") != "pilot"]
    pilots = [r for r in doc.get("rows", []) if r.get("kind") == "pilot"]
    texts = _texts(doc)
    cells = []
    for r in rows:
        cells.append({k: v for k, v in r.items() if k not in ("records", "trials")})
    return {
        "schema": SCHEMA, "id": doc.get("id"), "run_id": doc.get("run_id"),
        "design_id": doc.get("design_id"), "at": doc.get("at"), "status": doc.get("status"),
        "meta": {k: v for k, v in doc.items()
                 if k not in ("rows", "records", "verdict", "arm_a", "arm_b", "chain_bank")
                 and not isinstance(v, (list, dict))},
        "verdict": doc.get("verdict") or [],
        "pilots": pilots, "cells": cells,
        "regime": regime(doc),
        "replies_total": len(texts),
        "replies_shown": min(len(texts), MAX_REPLIES_PER_RUN),
        "replies_omitted": max(0, len(texts) - MAX_REPLIES_PER_RUN),
        "replies": texts[:MAX_REPLIES_PER_RUN],
    }


def build():
    root = site_root()
    data = os.path.join(root, "data")
    os.makedirs(data, exist_ok=True)
    if os.path.isdir(ASSETS):
        dst = os.path.join(root, "assets")
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(ASSETS):
            shutil.copyfile(os.path.join(ASSETS, f), os.path.join(dst, f))
        shutil.copyfile(os.path.join(ASSETS, "index.html"), os.path.join(root, "index.html"))

    index = {"schema": SCHEMA, "built": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
             "conventions": {
                 "evidence": "state/lab/runs/<experiment>/<run_id>.json",
                 "site_data": "web/lab/data/<experiment>/<run_id>.json",
                 "latest": "web/lab/data/<experiment>/latest.json",
                 "experiment_id": "x<NN>[letter]_<slug>",
                 "run_id": "<YYYYMMDD>T<HHMMSS>Z"},
             "regimes": {
                 "FULL": "the whole reply is stored; the run can be re-scored at zero token cost",
                 "TAIL": "only the last 320 characters; four recorded defects came from this slice",
                 "NONE": "no reply text at all; this run can never be re-read"},
             "experiments": []}

    for e in experiments():
        ed = os.path.join(data, e)
        os.makedirs(ed, exist_ok=True)
        entry = {"id": e, "runs": [], "latest": None, "regime": "NONE",
                 "replies": 0, "rescorable": False, "cells": 0, "status": "NEVER_RUN"}
        for rid in run_files(e):
            doc = grid.load_json(os.path.join(runs_root(), e, "%s.json" % rid), None)
            if not doc:
                continue
            t = trim(doc)
            grid.atomic_save_json(os.path.join(ed, "%s.json" % rid), t)
            entry["runs"].append({"run_id": rid, "at": t["at"], "status": t["status"],
                                  "design_id": t["design_id"], "regime": t["regime"],
                                  "cells": len(t["cells"]), "replies": t["replies_total"]})
        if entry["runs"]:
            best = max(entry["runs"], key=lambda r: (r["replies"], r["run_id"]))
            newest = entry["runs"][-1]
            entry["latest"] = newest["run_id"]
            entry["regime"] = best["regime"]
            entry["replies"] = best["replies"]
            entry["cells"] = newest["cells"]
            entry["rescorable"] = best["regime"] == "FULL"
            entry["status"] = ("COMPLETE" if best["regime"] == "FULL" else
                               "PARTIAL_EVIDENCE" if best["regime"] == "TAIL" else "NO_EVIDENCE")
            shutil.copyfile(os.path.join(ed, "%s.json" % newest["run_id"]),
                            os.path.join(ed, "latest.json"))
        # THE GAP IS DATA. An experiment with no readable evidence keeps its row and states the
        # command that would fill it, rather than disappearing from the index.
        entry["reboot_command"] = "python -m aea.lab.%s" % e
        index["experiments"].append(entry)

    counts = {}
    for x in index["experiments"]:
        counts[x["status"]] = counts.get(x["status"], 0) + 1
    index["summary"] = counts
    grid.atomic_save_json(os.path.join(data, "index.json"), index)
    return index


if __name__ == "__main__":
    ix = build()
    print("built %s" % site_root())
    print("%d experiments  %s" % (len(ix["experiments"]), ix["summary"]))
    for x in ix["experiments"]:
        print("  %-34s %-16s %-6s %5s replies  %s"
              % (x["id"][:33], x["status"], x["regime"], x["replies"] or "-",
                 "" if x["rescorable"] else "NOT re-scorable"))
    if "--serve" in sys.argv:
        import http.server
        import socketserver
        os.chdir(site_root())
        print("\nserving %s on http://localhost:7801" % site_root())
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", 7801), http.server.SimpleHTTPRequestHandler) as s:
            s.serve_forever()
