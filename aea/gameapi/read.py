"""aea.gameapi.read - the /game/* GET handlers: pure reads, re-homed to the REAL organ functions.

Never reimplements an organ - it calls the same functions the control room already exposes, behind
the honesty firewall. Imports are lazy (inside the handlers) so the seam can be mounted from
controlroom without an import cycle (controlroom imports gameapi; gameapi reads controlroom.state).
"""
from __future__ import annotations

from .honesty import receipt


def state() -> dict:
    """/game/state - the folded live snapshot (identity / life / energy / trust / brief).

    Wraps controlroom.state(): every value is read from the same files the entity writes; an absent
    field stays None and the client renders a dash, never a guess.
    """
    from aea.server import controlroom  # lazy: avoid the controlroom <-> gameapi import cycle
    return receipt(controlroom.state)


def run(run_id: str) -> dict:
    """/game/run?id= - the persisted run trace (links / axes / receipt / pass) for one ignition.

    Wraps bench_core.run_status(): reads bench_runs.json fresh every call (the file is the truth).
    status 'halted' is the visible blue fail; 'lost' is a carrier-lost receipt. Missing id -> a
    receipt naming the requirement, never a crash.
    """
    from aea.bench import bench_core
    from aea.kernel import grid

    def _run():
        out = bench_core.run_status(run_id)
        if isinstance(out, dict) and out.get("links"):
            # cost_u = REAL metered requests this run spent. A keyless-unlimited plant (the local
            # hearth) is genuinely free -> 0; a rate-capped plant costs 1 against a real budget.
            # Never a fabricated stake on a free draw (the honesty law over the game's want).
            cost = 0
            for link in out["links"]:
                rc = link.get("receipt")
                plant = rc.get("plant") if isinstance(rc, dict) else None
                p = grid.PLANTS.get(plant or "", {})
                if plant and (p.get("rpm") is not None or p.get("rpd") is not None):
                    cost += 1
            out["cost_u"] = cost
        return out
    return receipt(_run)


def axes() -> dict:
    """/game/axes - C-11, the entity's position in the 5-D growth space.

    The progression readout, and it is the SAME number the architecture is judged by: canon defines
    growth as movement through five axes (L0..L5 each), so the game shows coordinates rather than
    experience points. A level appears here only because a receipt raised it (OP1 axis-extension);
    `rung` is null wherever canon never named that rung - an honest gap, never a filled-in guess.
    """
    from aea.mind import axes as ax

    def _a():
        st = ax.load()
        pos = ax.position()
        rows = []
        for a in ax.AXES:
            lv = st["levels"][a]
            rows.append({"axis": a, "name": ax.AXIS[a]["name"], "line": ax.AXIS[a]["line"],
                         "proof_module": ax.AXIS[a]["proof"], "level": lv, "top": ax.TOP,
                         "rung": ax.rung(a, lv),
                         "next_rung": ax.rung(a, lv + 1) if lv < ax.TOP else None})
        return {"ok": True, "axes": rows, "sum": pos["sum"], "max": pos["max"],
                "walked": pos["walked"], "raised": st.get("raised", [])[-8:]}
    return receipt(_a)


def foundry() -> dict:
    """/game/foundry - THE FUEL, honestly. Every source on the map with the only three facts that
    matter: is it connected, what is its metabolism, and what has it actually served today.

    A dark plant is NAMED, never hidden - the map shows what you could connect and what holding that
    key would buy you, because the opening of the game is going and getting one. Metabolism is the real
    free-tier shape (a sustained 40/min with no daily cap is a different animal from a fast 30/min that
    dies at 1000/day), read from grid.PLANTS rather than described - add a plant there and it appears
    here. Nothing is scored or ranked: the caps are the truth and the player draws the conclusion.
    """
    import os
    from aea.kernel import grid

    def _f():
        # energy_usage is keyed by ROD ("plant/model"), never by plant - fold the rods up to their
        # plant. A plant with no rods on record reports null (the client renders a dash): we have not
        # drawn on it, which is NOT the same fact as having drawn zero times.
        usage = grid.load_json(os.path.join(grid.STATE, "energy_usage.json"), {})
        out = []
        for name, p in grid.PLANTS.items():
            auth = p.get("auth")
            prefix = name + "/"
            calls, rods = 0, 0
            for rod, v in usage.items():
                if rod.startswith(prefix):
                    rods += 1
                    calls += ((v or {}).get("calls") or 0)
            out.append({
                "plant": name,
                "privacy": p.get("privacy"),          # local | no-train | trains | none -> the zone law
                "keyless": not auth,                  # can a stranger draw on it with no setup at all
                "connected": True if not auth else bool(grid.key(auth)),
                "key_env": auth,                      # the exact variable to set; null when keyless
                "rpm_cap": p.get("rpm"),              # null = unmetered by the minute
                "rpd_cap": p.get("rpd"),              # null = no daily ceiling
                "calls_served": calls if rods else None,   # ALL-TIME, not today - never mislabel a clock
                "rods_met": rods if rods else None,        # distinct models of this plant encountered
            })
        lit = sum(1 for r in out if r["connected"])
        return {"ok": True, "connected": lit, "total": len(out), "plants": out}
    return receipt(_f)


def events(since: float = 0.0) -> dict:
    """/game/events?since= - the live nervous signal (pulse), one real row per emitted event.

    Wraps pulse.tail(): the real event stream the entity writes as it acts. One conduit particle
    per real row - never a decorative one. Returns {ok, events:[...]}.
    """
    from aea.kernel import pulse

    def _tail():
        return {"ok": True, "events": pulse.tail(since)}
    return receipt(_tail)
