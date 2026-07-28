"""export_city.py - dump the REAL grid state into city.data.js for the 3D city.
The city reads this; nothing is fake. Run after any key/registry change.

TWO DEFECTS FIXED 2026-07-28, both found by IMPORTING every module rather than by reading them.

  1 THE WORK RAN AT IMPORT. Every line below sat at module level with no `__main__` guard, so
    `import aea.tooling.export_city` - from a test sweep, a graph build, an editor's autocomplete -
    rewrote a tracked repo file as a side effect. A module that acts when it is merely named cannot
    be reasoned about, and the audit's note that `city.data.js` was "stale" was wrong in a worse
    way: it was whatever the last accidental import happened to produce.

  2 THE WRITE PATH WAS RELATIVE. `open("city.data.js", "w")` resolves against the CURRENT WORKING
    DIRECTORY, so the file landed wherever the process happened to start. That is discovery D8, the
    one this repo learned the hard way: never hardcode or relativise a path - go through `grid`,
    which walks up to the repo root. A missed write-site silently splits state.
"""
import json
import os

from aea.kernel import grid

ZONE = {"local": "residential", "no-train": "residential", "trains": "industrial",
        "none": "outskirts"}
OUT = os.path.join(grid.ROOT, "city.data.js")


def build() -> list:
    """The grid's real shape. `online` is a KEY-PRESENCE check on the environment, not a probe -
    nothing here touches the network."""
    plants = []
    for pid, c in grid.PLANTS.items():
        plants.append({
            "id": pid,
            "zone": ZONE[c["privacy"]],
            "privacy": c["privacy"],
            "online": (c["auth"] is None) or bool(grid.key(c["auth"])),
            "note": c["note"],
            "rpm": c.get("rpm") or 0,
            "rpd": c.get("rpd") or 0,
            "models": sum(1 for g in grid.GENERATORS if g[0] == pid),
        })
    return plants


def export() -> list:
    plants = build()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("window.CITY=" + json.dumps({"plants": plants}) + ";")
    return plants


if __name__ == "__main__":
    p = export()
    on = [x["id"] for x in p if x["online"]]
    print(f"{len(p)} plants, {len(on)} ONLINE: {', '.join(on)} -> {OUT}")
