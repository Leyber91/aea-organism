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


def _retire(plant, model, why="410 Gone"):
    """A tombstone, which is the one case a cooldown cannot express.

    MEASURED 2026-07-30: `nvidia/mistralai/mistral-small-4-119b-2603` sits at position 0 of the
    frontier ladder and answers 410 Gone. Every frontier draw - every wake tick - opened a
    connection to a retired endpoint, waited, failed, and fell through, forever. The cooldown does
    not help: it expires by design so the rod "gets another chance", which is right for a throttle
    or a blip and wrong for an endpoint that has been withdrawn.

    The repo already knew this. `hands.probe` maps 410 to `retired` and `hands.unmeasured` excludes
    it with the comment *Gone is permanent and re-probing a retired endpoint forever is the same
    wasted wake as U4*. That knowledge lived in the tool-calling probe and never reached the ladder
    that burns the rods - the census says the model exists, the endpoint says it does not, and law
    "ask the live thing, never the description of it" decides which one wins."""
    u = _usage()
    k = f"{plant}/{model}"
    e = u.get(k, {"calls": 0, "ok": 0, "fail": 0, "consec_fail": 0, "ema_latency": None})
    e["retired_at"] = time.time()
    e["retired_why"] = why
    u[k] = e
    _save_usage(u)


def _cooling(plant, model):
    """Cooldown, not tombstone: after COOL_SECONDS the rod gets another chance; a success clears it.

    EXCEPT for a rod that answered Gone. That one is skipped permanently - see `_retire`."""
    e = _usage().get(f"{plant}/{model}")
    if not e:
        return False
    if e.get("retired_at"):
        return True
    if e["consec_fail"] < COOL_AFTER:
        return False
    return (time.time() - e.get("cooled_at", 0)) < COOL_SECONDS


def _thr_for(mx: int, ratio: float) -> int:
    """The tier threshold for a battery of `mx` probes at `ratio` - THE one definition.

    Module-level, and public-ish, because it had TWO copies. `ladder()` computed it inline and
    `extensive_census.rank()` printed its tier labels from `score >= mx - 1` - the count form D24
    was written about, still standing in the module that PRINTS the ranking. The moment one was
    fixed the two disagreed, so the report called rods FRONTIER by a rule the ladder did not use.
    Found by `aea/lab/transfer.py` on its first real run.

    A printed ranking that disagrees with the live ladder is worse than no ranking, because it is
    believed."""
    return max(1, round(mx * ratio))


def _params_b(model: str) -> float:
    """Parameter-count heuristic from the model name (675b > 119b > 8b). MoE active counts ignored.

    RETURNS 0.0 WHEN THE NAME CARRIES NO SIZE, which is not the same statement as "this model has
    zero parameters" - and every caller that sorts on it reads the second. See `_depth_key`."""
    import re
    sizes = [float(m) for m in re.findall(r"(\d+(?:\.\d+)?)b", model.lower())]
    return max(sizes) if sizes else 0.0


def _depth_key(rows: list):
    """A depth sort that does not punish a rod for having no digits in its name.

    THE DEFECT, found by an adversarial re-read of the fix that shipped an hour earlier and was
    reported as verified. `order="depth"` sorted on `-_params_b(model)`, and `_params_b` returns
    0.0 for any name without a size in it. Unknown size therefore sorted as SMALLEST-POSSIBLE.
    MEASURED: `mistralai/mistral-nemotron` (score 10, reliability 1.0, 0.8s) landed at frontier
    rank 6, BELOW `ollama/granite4.1:8b`; `minimaxai/minimax-m3` (score 9) and `ollama/phi4:latest`
    (score 10) had the same problem. `aea/loop/aea.py` `core()` had just been pointed at this
    ordering, so the entity's deliberation was ranking strong hosted rods under local 8b models on
    the strength of a naming convention.

    A missing measurement is not a measurement of zero - the same shape as the NaN guard in
    `decide._finite` and the `DEAD` gate in `movecontrol`. An unknown here is given the MEDIAN of
    the sizes we do know, so it sorts among its peers rather than beneath everything: the honest
    statement is "no information", and the least-wrong stand-in for no information is typical.
    """
    known = sorted(s for s in (_params_b(r["model"]) for r in rows) if s > 0)
    mid = known[len(known) // 2] if known else 0.0
    return lambda r: (-(_params_b(r["model"]) or mid), -r["score"],
                      r["avg_latency"] if r["avg_latency"] is not None else 9)


def ladder(tier: str = "frontier", zone: str = "private", order: str | None = None) -> list[tuple[str, str]]:
    """The ranked energy rods for a tier+zone, from the LIVE censuses. Local floor always appended.
    order='depth': among qualified rods prefer PARAMETER DEPTH (the counsel duel 2026-07-11:
    675b beat 119b decisively on judgment at equal latency; precision ranking stays the default)."""
    allowed = grid.ZONES[zone]
    census = _load(CAPABILITY, {})
    cap = census.get("models", [])
    mx = len(census.get("battery", [])) or 6
    # THE THRESHOLD IS A RATIO, NOT `mx - 1`. MEASURED 2026-07-30, and this one line cost the entity
    # its whole fleet. The docstring above still says "frontier (census >=5/6) | solid (4/6)" - the
    # ratios this tier was designed around, 83% and 67%. The threshold was written as `mx - 1`,
    # which equals 5/6 only while the battery has six probes. The battery grew to TWELVE, so the bar
    # silently became 11/12 = 92% and 10/12 = 83%. GROWING THE EXAM SHRANK THE LADDER, and nothing
    # announced it: `frontier/private` fell to ONE living rod (groq), so every rate limit dropped
    # the entity onto a local 7B while a live 550B sat unused.
    #
    # A count-based threshold is a proxy for "good enough"; the ratio is the thing meant. Law B2,
    # and the most expensive instance of it in this repo so far.
    def _thr(ratio):
        return _thr_for(mx, ratio)

    fit = {(n["plant"], n["model"]): n for n in _load(FITNESS, {}).get("nodes", [])}
    usage = _usage()
    rods: list[tuple[str, str]] = []

    def zone_ok(plant):
        return plant in grid.PLANTS and grid.PLANTS[plant]["privacy"] in allowed

    def dead(p, m):
        """A tombstoned rod is not a rod. `ladder()` never checked this and `draw()` checked it only
        at call time, so corpses stayed in the ranking - and because the census scored them when
        they were alive, they carried the HIGHEST scores and sorted to the FRONT. The frontier's top
        two entries were both 410 Gone, holding the two best slots against living rods."""
        return bool(usage.get(f"{p}/{m}", {}).get("retired_at"))

    # THE DEEP-ROD EXEMPTION IS GONE, AND ITS REMOVAL IS THE POINT.
    #
    # It was added 2026-07-30 to admit rods the score gate rejected, on the theory that `score`
    # conflated format-compliance with judgement: nemotron-3-ultra-550b sat at 7/12 with reliability
    # 1.0 while narrating its way through probes that wanted exact strings. The theory was WRONG,
    # and the exemption was scaffolding around a defect one layer up (D28) - the census was handing
    # every rod a 40-256 token budget and scoring its truncated deliberation. With a fair budget the
    # same rod scores **12/12** and needs no exemption at all.
    #
    # MEASURED against the honest census before removing it: rods admitted ONLY by the exemption =
    # **ZERO**. It had become a bypass of the score gate that admitted nothing, and its admission
    # test was `_params_b(model) >= 100` - a NAME HEURISTIC - so a rod called "...-500b" with
    # reliability 1.0 and 6/12 would have walked into the tier that feeds the core mind.
    #
    # KEPT AS A LESSON RATHER THAN AS CODE: when a measurement looks wrong, the cheap move is a
    # bypass and the correct one is to fix the measurement. The bypass would have gone on working
    # here forever, quietly, admitting on a name.
    if tier == "frontier":
        rows = [r for r in cap if r["score"] >= _thr(5 / 6)]
    elif tier == "solid":
        rows = [r for r in cap if r["score"] >= _thr(4 / 6)]
    elif tier == "reflex":
        rows = [r for r in cap if r["score"] >= _thr(4 / 6) and (r["avg_latency"] or 9) < 1.2]
    else:                                              # local
        rows = []
    if order == "depth":
        rows.sort(key=_depth_key(rows))
    else:
        rows.sort(key=lambda r: (-r["score"], r["avg_latency"] if r["avg_latency"] is not None else 9))
    # EXCLUSION IS FOR THE DEAD; UNRELIABILITY ONLY DEMOTES.
    #
    # The old rule dropped any rod whose `model_fitness` entry read reliability < 1.0, permanently
    # and absolutely. The lesson behind it is real and stays - a rod that empties or hangs must not
    # be preferred. But the sweep that feeds it is a stored snapshot, and MEASURED 2026-07-30 it
    # threw out `nvidia/meta/llama-3.1-70b-instruct`, which scores 11/12 with reliability 1.0 in the
    # newer 12-probe census and answers in 1.0s live. The fleet's joint-best scorer was excluded by
    # an older, smaller sweep it had already outgrown.
    #
    # Two stores disagreed and the staler one won by being the only one consulted. So: the dead are
    # excluded by TOMBSTONE (measured from the endpoint, not inferred), and merely-doubted rods sort
    # to the back of their tier where `draw` reaches them only after the trusted ones fail. Nothing
    # known-broken gets preferred, and nothing gets silently deleted from the fleet.
    doubted: list[tuple[str, str]] = []
    for r in rows:
        p, m = r["plant"], r["model"]
        if not zone_ok(p) or dead(p, m):
            continue
        f = fit.get((p, m))
        if f and f["reliability"] < 1.0 and p != "ollama" and r.get("reliability", 0) < 1.0:
            doubted.append((p, m))                     # the fitness lesson: never PREFER a known-broken rod
            continue
        rods.append((p, m))
    rods.extend(doubted)
    if not cap and tier != "local":                    # no census yet -> fall back to the fitness sweep
        for (p, m), f in sorted(fit.items(), key=lambda kv: kv[1].get("avg_latency") or 9):
            if f["reliability"] == 1.0 and zone_ok(p) and not dead(p, m):
                rods.append((p, m))
    # THE FLOOR IS ALWAYS LAST, AND IT IS NOW ENFORCED RATHER THAN ASSERTED.
    #
    # This comment used to read "the floor: always alive, always last" and had become false: a LOCAL
    # rod that scores well enters the tier on merit through the census, so `ollama/phi4:latest`
    # (score 10) sat at frontier rank 3, ahead of hosted rods. Nobody wrote that rule; it was a
    # by-product of ranking on score alone, and the comment kept claiming otherwise.
    #
    # The rule is worth keeping and worth being true: a local rod is the SURVIVAL floor, reached
    # when the hosted plants are gone, not a competitor for the entity's best thinking. The
    # exception is a zone where local is all that is permitted - `sensitive` - and there this
    # partition leaves the ordering untouched because every rod in it is local anyway.
    local_last = [r for r in rods if grid.PLANTS.get(r[0], {}).get("privacy") == "local"]
    rods = [r for r in rods if r not in local_last] + local_last
    for p, m in LOCAL_FLOOR:                           # the named floor, after everything else
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
        # NO INVENTED CEILING. This line used to read
        #     int(min(pub.get("max_tokens", 500), 4096))
        # which did two harmful things at once: it defaulted an unlisted rod to FIVE HUNDRED tokens,
        # and it capped a listed one at 4096 even when its owner published 16384 or 20480. So the
        # entity's deepest rods were cut off at a quarter of what they will give, and the docstring
        # right below already said the ladder "has been ranking rods on our defaults rather than on
        # the rods".
        #
        # There is nothing to save. NVIDIA bills neither tokens nor requests; the only real limits
        # are 40 req/min PER MODEL (the Meter's job, not this line's) and the rod's own window. So
        # `None` travels down to `call_openai`, which sends the published ceiling or omits the field
        # and lets the provider apply the model's own maximum.
        use_mx = mx                                  # None -> the rod's own ceiling
        use_temp = temp                              # None -> the owner's published temperature
        if _cooling(plant, model):
            tried.append(f"{plant}/{model}:cooling"); continue
        ok_spend, _, why = _meter.can_spend(plant, model)
        if not ok_spend:
            tried.append(f"{plant}/{model}:{why}"); continue
        r = grid.call_openai(plant, model, msgs, max_tokens=use_mx, temperature=use_temp,
                             timeout=(180 if plant == "ollama" else timeout))
        text = (r.get("text") or "").strip()
        good = bool(r["ok"] and text)                  # EMPTY = failure (the silent-killer lesson)
        if r.get("status") == 410:
            # GONE IS PERMANENT. Not a cooldown - a tombstone, or the ladder re-opens a withdrawn
            # endpoint on every tick for the life of the entity.
            _retire(plant, model)
            tried.append(f"{plant}/{model}:410-retired")
            pulse.emit("energy", "retired", f"{plant}/{model.rsplit('/',1)[-1]} answered 410 Gone "
                       f"- tombstoned, the ladder will not try it again", ok=False)
            continue
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


def reap(plants=("nvidia",), workers: int = 8, timeout: int = 40, verbose: bool = True) -> dict:
    """Ask every rod in the census whether it is still there, and TOMBSTONE the ones that are not.

    THE DEFECT THIS CLOSES, measured 2026-07-30. The census holds 115 models. Probing the 24 deepest
    NVIDIA entries found SIX alive: `mistral-large-3-675b`, `qwen3.5-397b`, `qwen3.5-122b`,
    `stockmark-2-100b`, `qwen3-next-80b` and `dracarys-70b` all answer **410 Gone**; another eight
    answer 404. The census is a graveyard with a ranking on top, and because the ladder ranks by
    stored score, the corpses sort to the FRONT - a 675b tombstone outranks every living rod.

    This is not a fifth census. Four already exist (`probe`, `capability_census`,
    `extensive_census`, `model_fitness`) and each writes its own file; none of them writes the ONE
    store the ladder consults at draw time. `hands.probe` has mapped 410 to `retired` since
    2026-07-28 and `hands.unmeasured` excludes it as *"Gone is permanent"* - that knowledge simply
    never reached the module that burns the rods. So the job here is a wire, not a new instrument:
    ask the endpoint, and write the answer where `_cooling` will read it.

    WHY IT ASKS RATHER THAN READS. Every number in every census file is a description of a past
    moment; a 410 is the present tense. The whole reason the entity spent a day thinking with a 7B
    is that a stored file said a withdrawn endpoint was frontier-grade.

    404 is tombstoned alongside 410: Gone and Not Found differ in what they promise about the past,
    and not at all in what they offer now. A 429 or a 5xx is NEVER tombstoned - that is a transport
    condition, and recording it as deadness is the exact mistake `hands.unmeasured` was written to
    undo.
    """
    import concurrent.futures as _cf
    census = _load(CAPABILITY, {}).get("models", [])
    rods = [(m.get("plant"), m.get("model")) for m in census
            if m.get("plant") in plants and m.get("model")]
    if verbose:
        print(f"reaping {len(rods)} rods across {list(plants)}")

    def _ask(pm):
        plant, model = pm
        try:
            r = grid.call_openai(plant, model, [{"role": "user", "content": "ping"}],
                                 max_tokens=8, temperature=0.0, timeout=timeout)
            return plant, model, r.get("status"), bool(r.get("ok") and (r.get("text") or "").strip())
        except Exception:
            return plant, model, None, False

    dead, live, unclear = [], [], []
    with _cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for plant, model, status, ok in ex.map(_ask, rods):
            if status in (404, 410):
                _retire(plant, model, why=f"{status} at reap")
                dead.append(f"{plant}/{model}:{status}")
            elif ok:
                live.append(f"{plant}/{model}")
            else:
                unclear.append(f"{plant}/{model}:{status}")
    if verbose:
        print(f"  live {len(live)}   TOMBSTONED {len(dead)}   unclear {len(unclear)} "
              f"(429/5xx/empty - deliberately NOT retired)")
        for d in dead:
            print(f"    tombstoned {d}")
        print("\n  frontier/private after the reap:")
        for p, m in ladder("frontier", "private")[:8]:
            print(f"    {p}/{m}")
    return dict(live=live, dead=dead, unclear=unclear)


if __name__ == "__main__":
    if "--reap" in sys.argv[1:]:
        args = [a for a in sys.argv[1:] if not a.startswith("-")]
        reap(plants=tuple(args) if args else ("nvidia",))
    else:
        board()
