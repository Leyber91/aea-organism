"""export_city.py - dump the REAL grid state into city.data.js for the 3D city.
The city reads this; nothing is fake. Run after any key/registry change."""
import json
from aea.kernel import grid

ZONE = {"local": "residential", "no-train": "residential", "trains": "industrial", "none": "outskirts"}

plants = []
for pid, c in grid.PLANTS.items():
    online = (c["auth"] is None) or bool(grid.key(c["auth"]))
    plants.append({
        "id": pid,
        "zone": ZONE[c["privacy"]],
        "privacy": c["privacy"],
        "online": online,
        "note": c["note"],
        "rpm": c.get("rpm") or 0,
        "rpd": c.get("rpd") or 0,
        "models": sum(1 for g in grid.GENERATORS if g[0] == pid),
    })

with open("city.data.js", "w", encoding="utf-8") as f:
    f.write("window.CITY=" + json.dumps({"plants": plants}) + ";")

on = [p["id"] for p in plants if p["online"]]
print(f"{len(plants)} plants, {len(on)} ONLINE: {', '.join(on)}")
