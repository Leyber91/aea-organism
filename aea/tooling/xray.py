"""xray.py - WHAT THIS SYSTEM IS MADE OF RIGHT NOW, read from the code rather than from a document.

TWO READERS, ONE ARTIFACT, AND THAT IS THE WHOLE POINT.

  a human   wants to see the connections: what calls what, what is reachable, what is dead
  the entity wants the same thing about ITSELF, because `design/THE_ELEMENTS.md` Tier 2 lists
            "WHAT AM I MADE OF RIGHT NOW" as a question it cannot currently answer, and because
            self-modification is meaningless without a machine-readable description of the CURRENT
            self to diff a proposal against

A hand-drawn architecture diagram is stale the day after it is drawn. This one is derived, so it
cannot lie for longer than it takes to re-run.

WHY IT DESERVED TO EXIST, MEASURED. A review on 2026-07-28 found: twenty-one systems touching model
budgets, six independent model selectors none of which called another, and the ENTIRE notice-stuck /
get-unstuck kernel - impasse, unstick, crystal - orphaned from every wake path. None of that was
hidden. It was simply never rendered, and the cost was eighteen days of an entity repeating one
failing action. Every one of those three is a question this file answers in under a second.

IT PARSES. IT DOES NOT IMPORT. That is not a performance choice - it is a correctness one, and it
was learned the same day: `tooling/build_graph` and `tooling/export_city` rewrote tracked repo files
merely on being imported. An analyser that imports the code it studies runs the code it studies. So
everything here goes through `ast`, and nothing in the tree is executed.

WHAT IT DELIBERATELY DOES NOT DO. No live per-line execution tracing. That is weeks of work and it
answers a question nobody asked; static reachability plus live ledger state answers the real one,
which is "is this wired in, and is it running".

  python -m aea.tooling.xray            the map, as text
  python -m aea.tooling.xray --json     state/xray.json, for the dashboard and for the entity
  python -m aea.tooling.xray --orphans  only what nothing reaches
"""
from __future__ import annotations

import ast
import json
import os
import re
import sys
import time

from aea.kernel import grid

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../aea
OUT = os.path.join(grid.STATE, "xray.json")

# THE DOORS INTO THIS SYSTEM. Reachability is meaningless without saying "reachable FROM WHAT", and
# the distinction between these two sets is the one that mattered: a module reachable only from the
# server is not reachable by an unattended wake, and the unattended wake is the thing left alone.
ENTRIES = {
    "wake": ["aea.loop.live", "aea.loop.aea", "aea.organs.brief"],
    "server": ["aea.server.controlroom"],
    # A CLI TOOL AND AN EXPERIMENT ARE DOORS TOO. Counting only wake+server called `lab.harness`
    # and every `lab.parts.*` orphaned, when they are the library the experiments import. The
    # question is never "orphaned" in the abstract, it is "reachable FROM WHAT" - so the doors a
    # HUMAN opens are declared here rather than left implicit, and the leftover set becomes the
    # honest one: code no door of any kind reaches.
    "tools": [],        # filled at scan time: every aea.tooling.* module
    "lab": [],          # filled at scan time: every numbered experiment
}

# Module-level calls that TOUCH THE WORLD. A module doing any of these at import time acts merely on
# being named, which makes it unusable inside anything that scans or tests the tree.
#
# QUALIFIED, because a bare attribute name is not a call to the thing you think it is. MEASURED
# 2026-07-28: five of six reported violations were `str.replace` - `META = STORE.replace(".json",
# ".meta.json")` was being read as a filesystem write. A detector that fires on every `.replace()`
# in the tree trains the reader to ignore the one real hit, which is the only way this check fails.
BARE_CALLS = {"open", "exec", "eval"}
QUALIFIED_CALLS = {
    "os": {"makedirs", "remove", "replace", "rename", "system", "mkdir", "rmdir", "unlink"},
    "shutil": {"rmtree", "copy", "move", "copytree"},
    "subprocess": {"run", "Popen", "call", "check_output"},
    "json": {"dump"},
    "grid": {"atomic_save_json", "save_json"},
    "urllib.request": {"urlopen"},
}
SIDE_EFFECT_CALLS = BARE_CALLS | {c for s in QUALIFIED_CALLS.values() for c in s}


def _dotted(node) -> str:
    """`os.path.join` from an ast.Attribute chain, or "" when the receiver is a value rather than a
    module - which is exactly the case that made `.replace()` on a string look dangerous."""
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return ""

STATE_WRITERS = {"atomic_save_json", "save_json", "dump"}
STATE_READERS = {"load_json", "load"}


def _modname(path: str) -> str:
    rel = os.path.relpath(path, os.path.dirname(PKG))
    return rel[:-3].replace(os.sep, ".")


def _files() -> list:
    out = []
    for root, dirs, files in os.walk(PKG):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", "site_assets", "tests")]
        for f in files:
            if f.endswith(".py") and f != "__init__.py":
                out.append(os.path.join(root, f))
    return sorted(out)


def _toplevel_calls(tree: ast.Module) -> list:
    """Calls that run at IMPORT time - module level, and not inside any def/class/if __main__."""
    hits = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(node, ast.If):
            # `if __name__ == "__main__":` is the guard; anything inside it is not import-time.
            src = ast.dump(node.test)
            if "__name__" in src and "__main__" in src:
                continue
        for sub in ast.walk(node):
            if not isinstance(sub, ast.Call):
                continue
            f = sub.func
            if isinstance(f, ast.Name):
                if f.id in BARE_CALLS:
                    hits.append({"call": f.id, "line": getattr(sub, "lineno", 0)})
                continue
            if not isinstance(f, ast.Attribute):
                continue
            dotted = _dotted(f)                      # "" when the receiver is a value, not a module
            if not dotted:
                continue
            mod, _, attr = dotted.rpartition(".")
            for prefix, calls in QUALIFIED_CALLS.items():
                if attr in calls and (mod == prefix or mod.endswith("." + prefix)):
                    hits.append({"call": dotted, "line": getattr(sub, "lineno", 0)})
                    break
    return hits


def _state_touch(tree: ast.Module) -> dict:
    """Which state files this module reads and writes. Found by pairing a load/save call with the
    nearest .json literal, which is how every write site in this repo is actually written.

    THREE DEFECTS FIXED 2026-07-28, all of them producing stores that do not exist:
      1. A BARE EXTENSION is not a filename. `pid + ".json"` contributed a store literally named
         ".json", and `LEAK_SCAN = (".py", ".md", ".json")` contributed the same one from a tuple
         of extensions that is not a path at all. The panel then reported a three-way write
         collision on a store nobody has ever written, which is a false alarm in the one place whose
         entire purpose is catching real ones.
      2. A FORMAT PLACEHOLDER is not a filename either: "%s_latest.json" and "filename like
         heartbeat.json" both appeared as stores.
      3. THE MODULE-LEVEL SCAN WAS ORDER-DEPENDENT. `writes.add(v) if not reads else reads.add(v)`
         classified a constant as a read or a write based on whether any read had been seen EARLIER
         in the walk, which is arbitrary. Now a module-level constant is recorded only when the
         assignment is a plain literal or a path join, and it is attributed to neither side until a
         real call site references it.
    """
    def is_store(v):
        if not isinstance(v, str) or not (v.endswith(".json") or v.endswith(".jsonl")):
            return False
        base = os.path.basename(v)
        if base in (".json", ".jsonl"):
            return False                       # a bare extension, not a name
        return "%" not in v and " " not in base

    # NAME -> filename, from module-level constants. Resolving these at the CALL SITE is what keeps
    # the real collisions visible: `STORE = os.path.join(grid.STATE, "capability_census.json")`
    # followed by `grid.atomic_save_json(STORE, ...)` is a write, and dropping it to avoid the
    # phantom stores traded four false positives for every true one. Both directions are defects.
    consts = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            for s in ast.walk(node.value):
                if isinstance(s, ast.Constant) and is_store(s.value):
                    consts[node.targets[0].id] = os.path.basename(s.value)
                    break

    reads, writes = set(), set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
        if name not in (STATE_WRITERS | STATE_READERS):
            continue
        found = {os.path.basename(s.value) for s in ast.walk(node)
                 if isinstance(s, ast.Constant) and is_store(s.value)}
        found |= {consts[s.id] for s in ast.walk(node)
                  if isinstance(s, ast.Name) and s.id in consts}
        (reads if name in STATE_READERS else writes).update(found)
    return {"reads": sorted(reads), "writes": sorted(writes), "declared": sorted(consts.values())}


def scan() -> dict:
    """Every module, its internal imports, its import-time behaviour, its state files."""
    mods = {}
    for path in _files():
        name = _modname(path)
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src)
        except Exception as e:
            mods[name] = {"module": name, "path": os.path.relpath(path, os.path.dirname(PKG)),
                          "error": str(e)[:120], "imports": [], "lines": 0}
            continue
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("aea"):
                for a in node.names:
                    cand = "%s.%s" % (node.module, a.name)
                    imports.add(cand)
                    imports.add(node.module)
            elif isinstance(node, ast.Import):
                for a in node.names:
                    if a.name.startswith("aea"):
                        imports.add(a.name)
        doc = (ast.get_docstring(tree) or "").strip().splitlines()
        mods[name] = {
            "module": name,
            "path": os.path.relpath(path, os.path.dirname(PKG)).replace(os.sep, "/"),
            "package": name.split(".")[1] if name.count(".") > 1 else "-",
            "lines": len(src.splitlines()),
            "headline": (doc[0] if doc else "")[:150],
            "imports": sorted(imports),
            "import_time_effects": _toplevel_calls(tree),
            "state": _state_touch(tree),
            "defs": sorted(n.name for n in tree.body
                           if isinstance(n, (ast.FunctionDef, ast.ClassDef))),
        }

    # Keep only edges that point at a module we actually have. `from aea.kernel import grid` yields
    # both "aea.kernel" and "aea.kernel.grid"; only the second resolves, which is what we want.
    known = set(mods)
    for m in mods.values():
        m["imports"] = sorted(i for i in m["imports"] if i in known and i != m["module"])
    return mods


def reach(mods: dict, roots: list) -> set:
    """Everything transitively imported from these roots."""
    seen, stack = set(), [r for r in roots if r in mods]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(mods[cur]["imports"])
    return seen


def _doors(mods: dict) -> dict:
    """The human-opened doors, derived rather than listed, so a new tool or experiment counts the
    day it lands instead of the day someone remembers to add it (law S1: derive the map)."""
    e = {k: list(v) for k, v in ENTRIES.items()}
    e["tools"] = sorted(n for n in mods if n.startswith("aea.tooling."))
    e["lab"] = sorted(n for n in mods if n.startswith("aea.lab.")
                      and re.match(r"x\d", n.rsplit(".", 1)[-1]))
    return e


def role_of(name: str, orphaned: bool) -> str:
    """WHY a module has no caller, which is the part the old count threw away.

    "88 orphaned" was three unrelated facts added together, and the sum alarmed without directing:
    51 of them are experiments that are SUPPOSED to run once and produce evidence, 9 are CLI tools a
    human runs, and only the remainder are capabilities built and left unreachable. An invariant
    that cannot separate a correct state from a defect trains the reader to skim it (law W3).

      live      reachable from a wake or the server
      tool      reachable from a CLI tool a human runs
      evidence  reachable from a numbered lab experiment
      paused    the game API, parked by an explicit decision
      unwired   NO door of any kind reaches it. THIS is the only one that is a defect.
    """
    if not orphaned:
        return "live"
    if name.startswith("aea.gameapi."):
        return "paused"
    return "unwired"


def build() -> dict:
    mods = scan()
    wake = reach(mods, ENTRIES["wake"])
    server = reach(mods, ENTRIES["server"])
    live = wake | server

    doors = _doors(mods)
    by_tool = reach(mods, doors["tools"])
    by_lab = reach(mods, doors["lab"])

    for name, m in mods.items():
        m["reachable_from_wake"] = name in wake
        m["reachable_from_server"] = name in server
        m["orphaned"] = name not in live
        # ROLE ANSWERS "reachable from WHICH door", most load-bearing door first. A module the wake
        # reaches is live even if a tool also imports it; one only a tool reaches is a tool's
        # library, not a defect.
        m["role"] = ("live" if name in live else
                     "tool" if name in by_tool else
                     "evidence" if name in by_lab else
                     role_of(name, True))
        m["imported_by"] = sorted(o for o, x in mods.items() if name in x["imports"])

    # WHO WRITES WHAT. Two modules writing one store is not automatically wrong, but it is always
    # worth knowing - every state-corruption defect in this repo's history is a second writer
    # nobody remembered.
    stores = {}
    for name, m in mods.items():
        for f in m["state"]["writes"]:
            stores.setdefault(f, {"writers": [], "readers": []})["writers"].append(name)
        for f in m["state"]["reads"]:
            stores.setdefault(f, {"writers": [], "readers": []})["readers"].append(name)

    return {
        "schema": "aea.xray/1",
        "generated": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "modules": mods,
        "entries": ENTRIES,
        "counts": {
            "modules": len(mods),
            "reachable_from_wake": len(wake),
            "reachable_from_server": len(server),
            "orphaned": sum(1 for m in mods.values() if m["orphaned"]),
            "lines": sum(m["lines"] for m in mods.values()),
            # by ROLE, because the bare orphan count adds three different facts together
            "by_role": {r: sum(1 for m in mods.values() if m["role"] == r)
                        for r in ("live", "tool", "evidence", "paused", "unwired")},
            "unwired": sum(1 for m in mods.values() if m["role"] == "unwired"),
        },
        "orphans": sorted(n for n, m in mods.items() if m["orphaned"]),
        "unwired": sorted(n for n, m in mods.items() if m["role"] == "unwired"),
        "import_time_effects": sorted(
            (n for n, m in mods.items() if m["import_time_effects"])),
        "stores": stores,
        "live": live_state(),
    }


def live_state() -> dict:
    """The running truth beside the structural one. A module can be wired in and never have run."""
    def j(name, default):
        try:
            return grid.load_json(os.path.join(grid.STATE, name), default)
        except Exception:
            return default

    led = j("trust_ledger.json", {})
    seats = (j("seats.json", {}) or {}).get("seats", {})
    goals = (j("goals.json", {}) or {}).get("goals", [])
    crystal = (j("crystal.json", {}) or {}).get("parts", {})
    exp = (j("experience.json", {}) or {}).get("attempts", [])
    alarms = j("trust_alarms.json", {})
    hb = j("heartbeat.json", {})
    return {
        "capabilities": {k: {"level": v.get("level"), "streak": v.get("streak"),
                             "runs": v.get("runs"), "fails": v.get("fails"),
                             "down": v.get("down", 0)}
                         for k, v in (led or {}).items()},
        "seats": {k: {"capability": v.get("capability"), "zone": v.get("zone"),
                      "rod": v.get("rod"), "runs": v.get("runs"), "wins": v.get("wins")}
                  for k, v in (seats or {}).items()},
        "goals": [{"id": g.get("id"), "status": g.get("status"), "capability": g.get("capability"),
                   "runs": g.get("runs")} for g in (goals or [])],
        "crystal_parts": len(crystal or {}),
        "experience_attempts": len(exp or []),
        "open_alarms": (alarms or {}).get("open", []),
        "heartbeat": {"boots": hb.get("boot_count"), "ticks": hb.get("total_ticks"),
                      "alive_since": hb.get("alive_since"),
                      "last_brief_date": hb.get("last_brief_date")},
    }


def outline(d: dict = None, budget: int = 3000) -> str:
    """THE FIRST PAGES OF THE BOOK. What you hand a model instead of the book.

    You do not give a student the whole volume and expect comprehension. You give the front matter:
    a map of the whole, dense enough that nothing is invisible, short enough to hold at once, and
    specific enough that the reader knows which chapter to open. Then they open one chapter.

    THE NUMBERS THAT FORCE THIS SHAPE, measured 2026-07-28:

        raw source          ~220,000 tokens   fits in nothing we can run for free
        state/xray.json      ~21,000 tokens   fits, but it is the index, not the outline
        this outline          ~2,500 tokens   fits in every rod we have measured

    NOTHING IS LOST, and that is the whole design constraint rather than a nice property. Every
    module appears. What is dropped is DETAIL, never EXISTENCE - a module reduced to one line is
    still a module the reader knows to ask about, and `xray.json` holds the full record for any name
    that appears here. An outline that omits an entry is a lie; an outline that abbreviates one is
    an index.

    The spine is given in full because thirteen modules ARE the entity; everything else is named,
    sized, and grouped.
    """
    d = d or build()
    c = d["counts"]
    mods = d["modules"]
    L = []
    L.append("AEA CODEBASE OUTLINE  (generated %s)" % d["generated"])
    L.append("%d modules, %d lines. %d reachable from an unattended wake; %d orphaned."
             % (c["modules"], c["lines"], c["reachable_from_wake"], c["orphaned"]))
    L.append("Full record for any name below: state/xray.json -> modules[<name>].")
    L.append("")
    L.append("== THE SPINE: everything an unattended wake can reach ==")
    spine = sorted((n for n, m in mods.items() if m["reachable_from_wake"]),
                   key=lambda n: -mods[n]["lines"])
    for n in spine:
        m = mods[n]
        L.append("  %-26s %4dL  %s" % (n.replace("aea.", ""), m["lines"], m["headline"][:74]))
    L.append("")
    L.append("== NOT REACHED BY ANY WAKE: built, tested, and wired to nothing ==")
    by_pkg = {}
    for n in d["orphans"]:
        by_pkg.setdefault(mods[n]["package"], []).append(n)
    for pkg in sorted(by_pkg, key=lambda p: -sum(mods[x]["lines"] for x in by_pkg[p])):
        names = sorted(by_pkg[pkg], key=lambda x: -mods[x]["lines"])
        tot = sum(mods[x]["lines"] for x in names)
        L.append("  %-10s %2d modules, %5dL" % (pkg, len(names), tot))
        # kernel is the one that matters: it is supposed to BE the entity, so it is named in full.
        show = names if pkg == "kernel" else names[:6]
        for x in show:
            L.append("      %-30s %4dL  %s" % (x.replace("aea.", ""), mods[x]["lines"],
                                               mods[x]["headline"][:56]))
        if len(names) > len(show):
            L.append("      ... %d more: %s" % (len(names) - len(show),
                                                ", ".join(x.split(".")[-1] for x in names[len(show):])))
    L.append("")
    L.append("== STATE: what is written, and by whom ==")
    for f, v in sorted(d["stores"].items()):
        w = sorted(set(v["writers"]))
        if not w:
            continue
        flag = "  <- MORE THAN ONE WRITER" if len(w) > 1 else ""
        L.append("  %-28s %s%s" % (f, ", ".join(x.replace("aea.", "") for x in w)[:60], flag))
    lv = d["live"]
    L.append("")
    L.append("== LIVE ==")
    L.append("  capabilities: " + ", ".join(
        "%s=%s" % (k, ["FORBIDDEN", "DRAFT", "WATCHED", "TRUSTED"][v["level"] or 0])
        for k, v in sorted(lv["capabilities"].items())))
    L.append("  open alarms: %s" % (", ".join(lv["open_alarms"]) or "none"))
    L.append("  heartbeat: %s boots, %s ticks, last brief %s"
             % (lv["heartbeat"].get("boots"), lv["heartbeat"].get("ticks"),
                lv["heartbeat"].get("last_brief_date")))
    return "\n".join(L)


def render(d: dict) -> str:
    c = d["counts"]
    L = ["XRAY - what this system is made of, parsed from the code", "=" * 96,
         "%d modules, %d lines. reachable from a WAKE: %d. from the SERVER: %d. ORPHANED: %d."
         % (c["modules"], c["lines"], c["reachable_from_wake"], c["reachable_from_server"],
            c["orphaned"])]

    L.append("")
    L.append("ORPHANED - nothing imports these from any entry point, so no wake can reach them:")
    for n in d["orphans"]:
        m = d["modules"][n]
        L.append("   %-38s %4d lines  %s" % (n, m["lines"], m["headline"][:44]))
    if not d["orphans"]:
        L.append("   (none)")

    L.append("")
    L.append("ACTS AT IMPORT TIME - runs when merely named:")
    for n in d["import_time_effects"]:
        calls = ", ".join(sorted({e["call"] for e in d["modules"][n]["import_time_effects"]}))
        L.append("   %-38s %s" % (n, calls))
    if not d["import_time_effects"]:
        L.append("   (none)")

    L.append("")
    L.append("STORES WITH MORE THAN ONE WRITER:")
    multi = {k: v for k, v in d["stores"].items() if len(set(v["writers"])) > 1}
    for f, v in sorted(multi.items()):
        L.append("   %-30s <- %s" % (f, ", ".join(sorted(set(v["writers"])))))
    if not multi:
        L.append("   (none)")

    lv = d["live"]
    L.append("")
    L.append("LIVE: %d capabilities, %d seats, %d goals, %d crystal parts, %d experience attempts"
             % (len(lv["capabilities"]), len(lv["seats"]), len(lv["goals"]),
                lv["crystal_parts"], lv["experience_attempts"]))
    if lv["open_alarms"]:
        L.append("   OPEN ALARMS: %s" % ", ".join(lv["open_alarms"]))
    return "\n".join(L)


if __name__ == "__main__":
    d = build()
    if "--json" in sys.argv:
        grid.atomic_save_json(OUT, d, indent=1)
        print("wrote %s (%d modules)" % (OUT, d["counts"]["modules"]))
    if "--orphans" in sys.argv:
        for n in d["orphans"]:
            print("%-40s %s" % (n, d["modules"][n]["headline"][:60]))
    else:
        print(render(d))
