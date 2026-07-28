"""energy.py - ONE CONTINUUM: the brain draws models as ENERGY through a single mouth.

Luis's law: the models are not the mind - they are the energy the mind burns. So no organ may
ever name a model again. Every draw comes here; this reads the LIVE measurements (capability
census + fitness sweep + the meter's rate state) and burns the best rod available RIGHT NOW,
falling down the ranked ladder when one fails. The mind persists; the fuel is fungible. If every
hosted plant died tomorrow, draw() degrades to the local floor and the entity is still alive.

Also closes fitness-from-use: every real call updates energy_usage.json (rolling ok-rate +
latency per rod), so the entity's self-knowledge is fed by living, not by stale sweeps. A rod
that fails 3 draws in a row is COOLING (skipped) until a sweep or a successful retry clears it.

  from energy import draw
  r = draw("prompt", tier="frontier", zone="private")     # -> dict(ok, text, plant, model, tried)

  tiers: frontier (census >=5/6) | solid (4/6) | reflex (fit + fast) | local (ollama floor)
  zones: public | private (no-train+local) | sensitive (local ONLY - the hard boundary)

  python energy.py            # show the energy ladder per tier/zone + usage state
"""
from __future__ import annotations
import json, os, sys, time
from aea.kernel import grid
from aea.energy import rodprobe
from aea.kernel import pulse

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

HERE = grid.HERE
USAGE = os.path.join(grid.STATE, "energy_usage.json")
CAPABILITY = os.path.join(grid.STATE, "capability_census.json")
FITNESS = os.path.join(grid.STATE, "model_fitness.json")
COOL_AFTER = 3          # consecutive live failures -> rod cools ...
COOL_SECONDS = 900      # ... for 15 minutes, then it may retry (review 2026-07-10: cooling was a
                        # PERMANENT tombstone - nothing could ever reset consec_fail because a
                        # cooling rod was never drawn again; tiers decayed monotonically to the floor)
LOCAL_FLOOR = [("ollama", "qwen2.5:7b"), ("ollama", "granite4.1:8b"), ("ollama", "llama3.1:8b")]

_meter = grid.METER      # the shared meter - one truth across every organ and process


def _load(path, default):
    return grid.load_json(path, default)


def _usage():
    return _load(USAGE, {})

def _save_usage(u):
    with grid.file_lock(USAGE):
        grid.atomic_save_json(USAGE, u, indent=1)


def _record_use(plant, model, ok, latency):
    u = _usage()
    k = f"{plant}/{model}"
    e = u.get(k, {"calls": 0, "ok": 0, "fail": 0, "consec_fail": 0, "ema_latency": None})
    e["calls"] += 1
    if ok:
        e["ok"] += 1; e["consec_fail"] = 0; e.pop("cooled_at", None)
        e["ema_latency"] = round(latency if e["ema_latency"] is None else 0.7 * e["ema_latency"] + 0.3 * latency, 1)
    else:
        e["fail"] += 1; e["consec_fail"] += 1
        if e["consec_fail"] >= COOL_AFTER:
            e["cooled_at"] = time.time()          # start (or extend) the cooldown window
    e["last"] = time.strftime("%Y-%m-%d %H:%M", time.gmtime())
    u[k] = e
    _save_usage(u)


def _cooling(plant, model):
    """Cooldown, not tombstone: after COOL_SECONDS the rod gets another chance; a success clears it."""
    e = _usage().get(f"{plant}/{model}")
    if not e or e["consec_fail"] < COOL_AFTER:
        return False
    return (time.time() - e.get("cooled_at", 0)) < COOL_SECONDS


def _params_b(model: str) -> float:
    """Parameter-count heuristic from the model name (675b > 119b > 8b). MoE active counts ignored."""
    import re
    sizes = [float(m) for m in re.findall(r"(\d+(?:\.\d+)?)b", model.lower())]
    return max(sizes) if sizes else 0.0


def ladder(tier: str = "frontier", zone: str = "private", order: str | None = None) -> list[tuple[str, str]]:
    """The ranked energy rods for a tier+zone, from the LIVE censuses. Local floor always appended.
    order='depth': among qualified rods prefer PARAMETER DEPTH (the counsel duel 2026-07-11:
    675b beat 119b decisively on judgment at equal latency; precision ranking stays the default)."""
    allowed = grid.ZONES[zone]
    census = _load(CAPABILITY, {})
    cap = census.get("models", [])
    mx = len(census.get("battery", [])) or 6           # thresholds scale with the battery size
    fit = {(n["plant"], n["model"]): n for n in _load(FITNESS, {}).get("nodes", [])}
    rods: list[tuple[str, str]] = []

    def zone_ok(plant):
        return plant in grid.PLANTS and grid.PLANTS[plant]["privacy"] in allowed

    if tier == "frontier":
        rows = [r for r in cap if r["score"] >= mx - 1]
    elif tier == "solid":
        rows = [r for r in cap if r["score"] >= mx - 2]
    elif tier == "reflex":
        rows = [r for r in cap if r["score"] >= mx - 2 and (r["avg_latency"] or 9) < 1.2]
    else:                                              # local
        rows = []
    if order == "depth":
        rows.sort(key=lambda r: (-_params_b(r["model"]), -r["score"],
                                 r["avg_latency"] if r["avg_latency"] is not None else 9))
    else:
        rows.sort(key=lambda r: (-r["score"], r["avg_latency"] if r["avg_latency"] is not None else 9))
    for r in rows:
        p, m = r["plant"], r["model"]
        if not zone_ok(p):
            continue
        f = fit.get((p, m))
        if f and f["reliability"] < 1.0 and p != "ollama":
            continue                                   # the fitness lesson: refuse known-broken rods
        rods.append((p, m))
    if not cap and tier != "local":                    # no census yet -> fall back to the fitness sweep
        for (p, m), f in sorted(fit.items(), key=lambda kv: kv[1].get("avg_latency") or 9):
            if f["reliability"] == 1.0 and zone_ok(p):
                rods.append((p, m))
    for p, m in LOCAL_FLOOR:                           # the floor: always alive, always last
        if zone_ok(p) and (p, m) not in rods:
            rods.append((p, m))
    return rods


def draw(prompt: str, tier: str = "solid", zone: str = "private", mx: int | None = None,
         temp: float | None = None, timeout: int = 60, system: str | None = None,
         order: str | None = None) -> dict:
    """THE MOUTH. Burn the best live rod; on failure fall down the ladder; never raise.
    Returns dict(ok, text, plant, model, latency, tried).

    `mx` and `temp` default to None meaning USE WHAT THIS ROD'S OWNER PUBLISHES. Passing a value
    still wins, so every existing explicit call site is unchanged. MEASURED 2026-07-28: the owners
    publish temperature 0.2 to 1.0 and max_tokens 1024 to 20480, while this function sent 0.2 and
    500 to all of them. `nemotron-3-nano-omni` asks for 20480 and was getting 500; a reasoning rod
    handed too small a budget spends it thinking and returns nothing, which is the empty-reply
    failure already recorded in unstick.py. Every fitness score in this repo was taken through that
    filter, so the ladder has been ranking rods on our defaults rather than on the rods.
    """
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    tried = []
    for plant, model in ladder(tier, zone, order=order):
        known = rodprobe.facts(model)
        if known.get("nvidia_catalog_state", "").startswith("http4"):
            # measured as not served. Trying it again burns a slot in the ladder to learn nothing.
            tried.append(f"{plant}/{model}:not-served"); continue
        pub = grid.own_params(model)
        use_mx = mx if mx is not None else int(min(pub.get("max_tokens", 500), 4096))
        use_temp = temp if temp is not None else pub.get("temperature", 0.2)
        if _cooling(plant, model):
            tried.append(f"{plant}/{model}:cooling"); continue
        ok_spend, _, why = _meter.can_spend(plant, model)
        if not ok_spend:
            tried.append(f"{plant}/{model}:{why}"); continue
        r = grid.call_openai(plant, model, msgs, max_tokens=use_mx, temperature=use_temp,
                             timeout=(180 if plant == "ollama" else timeout))
        text = (r.get("text") or "").strip()
        good = bool(r["ok"] and text)                  # EMPTY = failure (the silent-killer lesson)
        if r.get("status") == 429:
            _meter.mark_throttled(plant, model)        # rate-limit = the METER's problem, not the rod's
        else:                                          # fitness only judges the rod's own behaviour
            _record_use(plant, model, good, r.get("latency", 0))
            _meter.record(plant, model, tokens=r.get("tokens", 0))
            if good:
                _meter.clear_strike(plant, model)
        tried.append(f"{plant}/{model}:{'ok' if good else ('empty' if r['ok'] else r.get('status'))}")
        pulse.emit("energy", "draw", f"{plant}/{model.rsplit('/',1)[-1]} {tier}/{zone} "
                   f"{'ok' if good else tried[-1].split(':')[-1]} {round(r.get('latency',0),1)}s", ok=good)
        if good:
            return dict(ok=True, text=text, plant=plant, model=model,
                        latency=round(r.get("latency", 0), 1), tried=tried)
    pulse.emit("energy", "starved", f"no rod answered ({len(tried)} tried)", ok=False)
    return dict(ok=False, text="", plant=None, model=None, latency=0, tried=tried)


def board():
    print("THE ENERGY CONTINUUM - ranked rods per tier (zone=private)\n" + "=" * 76)
    for tier in ("frontier", "solid", "reflex", "local"):
        rods = ladder(tier, "private")
        print(f"  {tier:8} ({len(rods):2} rods): " + " > ".join(f"{p}/{m.split('/')[-1][:28]}" for p, m in rods[:4])
              + (" > ..." if len(rods) > 4 else ""))
    u = _usage()
    if u:
        print("-" * 76 + "\n  LIVE USE (fitness-from-use):")
        for k, e in sorted(u.items(), key=lambda kv: -kv[1]["calls"])[:10]:
            rate = round(100 * e["ok"] / e["calls"]) if e["calls"] else 0
            cool = "  COOLING" if e["consec_fail"] >= COOL_AFTER else ""
            print(f"    {k[:52]:52} {e['calls']:>3} calls  {rate:>3}% ok  ema {e['ema_latency']}s{cool}")


if __name__ == "__main__":
    board()
