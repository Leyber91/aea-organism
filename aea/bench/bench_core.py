"""bench_core.py - THE BENCH HARNESS (P0): compose a construct, run it for real, measure it.

The game's core creative act made executable (R1 composition reframe): a construct spec is a
pointer set of module ids into modules.json; running it walks the parts in spine order and
fires each part's REAL entry point - TAP through energy.draw, GOVERNOR through
grid.METER.can_spend, LADDER through energy.ladder - metered, zone-lawed, trust-gated. There
is no second execution engine (A14 section 3, binding): the bench is a harness over the same
organs that already run the entity.

The P0 SPEC ADDENDUM contracts, honored here:
  TAP     = thin wrapper over energy.draw; config {tier, zone, prompt_source} ->
            payload {text, latency_ms, tried[], plant, model}
  SCORER  = receipt-measured fields ONLY: {pass, axes: {latency_ms, tokens, ok, zone}};
            no model-judged quality number exists at P0
  task v0 = {id, prompt, expect: {contains|exact}, tier_floor}; ONE curated task ships,
            tier_floor pinned local so the first run cannot ladder-walk a bad grid day
  runs    = start_run() -> run_id immediately, executes in its own thread; every trace row
            is RUN-TAGGED and APPENDED to bench_runs.json via grid.file_lock +
            atomic_save_json - append-only, restart-survivable; the file is the truth,
            any in-memory copy is a cache, never the truth (E1 checklist 7.6)
  ms      = the harness's own perf_counter around each fire - never energy.draw's
            0.1s-rounded latency (the run contract)
  trust   = evaluated per part AT FIRE TIME: allowed -> fire; draft_only -> draft path only
            (artifact produced, nothing leaves); otherwise refuse, naming the level.
            P0's parts bind no charter row; the LAW ships regardless, before P3 puts
            RECALL on the bench
  zone    = REQUIRED in construct spec v0.1.0 - a spec without it is refused naming the
            clause. The honest kill: zone=sensitive with local ollama down is genuine
            starvation; a plant-kill on a healthy grid reroutes and PASSES (reroute marks
            in tried[], resilience working - never rendered as failure)

  python bench_core.py           # dry proof: validator verdicts + last/best (no draw)
  python bench_core.py --fire    # run the opening construct for real (spends a draw)
"""
from __future__ import annotations
import json, os, random, sys, threading, time
from time import perf_counter

from aea.kernel import grid
from aea.energy import energy
from aea.kernel import pulse
from aea.kernel import trust

HERE = grid.HERE
# the aea/ package dir - the base the forge_gate resolves a part's source file against. After the
# 2026-07-22 subpackage reorg the parts live under aea/<domain>/ and modules.json carries the
# domain-relative path (energy/energy.py); grid.HERE now points at aea/kernel/, not aea/.
_PKG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_FP = os.path.join(grid.STATE, "modules.json")
RUNS_FP = os.path.join(grid.STATE, "bench_runs.json")

SPEC_VERSION = "0.1.0"
FIREABLE = ("tap", "scaffold", "governor", "ladder", "scorer")  # the P0 opening pool (A13 s3)
ALLOWED_POLICY = {"scaffold": {"template"}}  # the only dial the harness genuinely honors at P0:
                                             # TAP's zone IS the spec's zone (the zone law) and
                                             # tier is the task's tier_floor pin - a policy key
                                             # with no enforcement path is a fake lever (A7 law)
STALE_S = len(energy.LOCAL_FLOOR) * 180 + 60
                # DERIVED, never asserted (crash rider 2026-07-20): worst honest single link =
                # TAP walking every local-floor rod at ollama's 180s timeout, plus a 60s margin.
                # A rod added to the floor widens this automatically instead of making live
                # runs flap running -> lost -> done.
ROTATE_BYTES = 400_000
                # bench_runs.json stays BOUNDED (the chains.jsonl idiom): every append rewrites
                # the whole file under the lock and growth widens the os.replace-vs-reader
                # window. Rotation happens at run open only (never mid-run), archives to .1,
                # folds LAST/BEST forward and preserves the run counter - see _rotated.

# the ONE curated bench task - task format v0 (P0 SPEC ADDENDUM); open target, reflex-cheap
TASKS = {
    "t-01": {"id": "t-01", "name": "FIRST DRAW",
             "prompt": "Reply with exactly one line: PROBE ONLINE",
             "expect": {"contains": "ONLINE"},
             "tier_floor": "local"},
}
DEFAULT_TASK = "t-01"

# the opening construct: TAP + SCORER, one click, one visible run (D-P1; R1 finding 10)
DEFAULT_CONSTRUCT = {
    "construct_version": SPEC_VERSION,
    "manifest_version": SPEC_VERSION,
    "id": "c-01",
    "parts": ["tap", "scorer"],
    "wiring": [["tap", "scorer"]],
    "rods": {"default": {"tier": "local"}},
    "policies": {},
    "zone": "private",
}

_RUN_LOCK = threading.Lock()   # one packet, one run at a time (E4 s8.2) - in-process guard;
                               # a run fired from another process stays metered by the grid


def _manifest() -> dict:
    """modules.json fresh from disk on every call - the file is the truth, never a cache."""
    return grid.load_json(MANIFEST_FP, {})


# --------------------------------------------------------------------------------------
# 1. The validator - construct spec v0, a pure re-walk (A14 s3). Every failure names its
#    violated clause; never a generic lock.
# --------------------------------------------------------------------------------------
def validate_spec(spec) -> dict:
    """Returns {ok: True} or {ok: False, refused: <the clause, in receipt diction>}."""
    def refuse(clause: str) -> dict:
        return {"ok": False, "refused": clause}
    if not isinstance(spec, dict):
        return refuse("a construct spec is a JSON object (construct spec v0.1.0)")
    cv = spec.get("construct_version")
    if cv is None:
        return refuse("construct_version REQUIRED - stamp the spec (construct spec v0.1.0); "
                      "an unstamped spec refuses loudly, never half-runs (A14 s4.3)")
    if cv != SPEC_VERSION:
        return refuse(f"construct_version '{cv}' is not {SPEC_VERSION} - version mismatch "
                      "refuses loudly, never half-runs (A14 s4.3)")
    zone = spec.get("zone")
    if not zone:
        return refuse("zone REQUIRED - construct spec v0.1.0, the zone law (P0 SPEC ADDENDUM): "
                      "private | sensitive | public")
    if zone not in grid.ZONES:
        return refuse(f"zone '{zone}' is not a zone - the zone law names three: "
                      "private | sensitive | public")
    man = _manifest() or {}
    mods = man.get("modules") or {}
    if not mods:
        return refuse("modules.json missing or empty - the registry of record; "
                      "parts are module ids (A14 s2.1)")
    mv = spec.get("manifest_version")
    if mv is not None and mv != man.get("manifest_version"):
        return refuse(f"manifest_version '{mv}' does not match the registry's "
                      f"'{man.get('manifest_version')}' - version mismatch refuses loudly, "
                      "never half-runs (A14 s4.3)")
    parts = spec.get("parts")
    if not isinstance(parts, list) or not parts or not all(isinstance(p, str) for p in parts):
        return refuse("parts REQUIRED - a construct is a pointer set of module ids (A14 s3)")
    seen = set()
    for p in parts:
        if p in seen:
            return refuse(f"part '{p}' seated twice - one seat per part at P0")
        seen.add(p)
        row = mods.get(p)
        if row is None:
            return refuse(f"part '{p}' is not a registered module id (modules.json - "
                          "the registry law)")
        if not row.get("bench_part"):
            return refuse(f"part '{p}' is not a bench part (bench_part false - the gate wraps "
                          "every construct; it is never slotted)")
        status = row.get("status")
        if status == "FORGE-PENDING":
            q = (row.get("forge") or {}).get("queue")
            return refuse(f"part '{p}' is FORGE-PENDING (forge queue {q}) - forged in a pair "
                          "session first, slotted after (A9)")
        if status == "INGREDIENT":
            return refuse(f"part '{p}' is INGREDIENT - proven in isolation, not wired "
                          "(A9's fog list)")
        if status != "BUILT":
            return refuse(f"part '{p}' status '{status}' - only BUILT parts fire")
        fp = os.path.join(_PKG_DIR, row.get("file") or "")
        if not (row.get("file") and os.path.isfile(fp) and os.path.getsize(fp) > 0):
            return refuse(f"part '{p}': {row.get('file')} missing or empty on disk - "
                          "LOST SIGNAL (the forge_gate check)")
        if p not in FIREABLE:
            return refuse(f"part '{p}' has no P0 fire path - the opening pool is "
                          "THE DRAW, THE FRAME, THE METER, THE LADDER, THE MEASURE (A13 s3)")
    if parts[0] != "tap":
        return refuse("no draw at the head - a construct draws through THE DRAW; it holds the head "
                      "(rail law)")
    if "scorer" in parts and parts[-1] != "scorer":
        return refuse("SCORER holds the tail - after the measure there is nothing left to "
                      "measure (rail law)")
    for edge in spec.get("wiring") or []:
        if not (isinstance(edge, (list, tuple)) and len(edge) == 2
                and all(e in seen for e in edge)):
            return refuse(f"wiring edge {edge} names an unseated part - every edge runs "
                          "between declared parts (A14 s3)")
    for p, pol in (spec.get("policies") or {}).items():
        if p not in seen:
            return refuse(f"policy for '{p}' which is not seated - policies bind seated "
                          "parts only")
        declared = set(((mods.get(p) or {}).get("config") or {}).keys())
        honored = ALLOWED_POLICY.get(p, set())
        for k in (pol or {}):
            if k not in declared:
                return refuse(f"policy key '{k}' is outside part '{p}' declared config "
                              "surface (modules.json)")
            if k not in honored:
                return refuse(f"policy key '{p}.{k}' has no enforcement path at P0 - "
                              "read-only truth beats a fake lever (A7 law); writable dials "
                              "arrive with their rungs")
    return {"ok": True}


# --------------------------------------------------------------------------------------
# 2. The part contracts (P0 SPEC ADDENDUM)
# --------------------------------------------------------------------------------------
def tap(prompt: str, tier: str = "local", zone: str = "private",
        prompt_source: str = "task") -> dict:
    """TAP (player-facing: THE DRAW): a thin wrapper over energy.draw; lights the MOUTH organ.
    latency_ms is the harness's own perf_counter around the draw - never draw()'s
    rounded seconds. tokens stays None: energy.draw does not surface a token count,
    and an absent measurement renders absent, never invented (honesty law).
    TICKETED P1 (warden rider 2026-07-20): grid.call_openai already measures tokens; the
    plumb is one line in draw()'s return dict + this payload - the null is lawful today,
    a forever-null is a dead axis. zone in this payload is the ENFORCED REQUEST echoed
    through, not an independent measurement: energy.ladder selects rods by this zone and
    the receipt's plant field is the cross-check."""
    t0 = perf_counter()
    r = energy.draw(prompt, tier=tier, zone=zone, mx=160)
    ms = round((perf_counter() - t0) * 1000, 1)
    return {"ok": bool(r.get("ok")), "text": r.get("text") or "", "latency_ms": ms,
            "tried": r.get("tried") or [], "plant": r.get("plant"), "model": r.get("model"),
            "tokens": None, "zone": zone}


SCAFFOLDS = {
    "plain": "{prompt}",
    "bench": "You are on the bench. Answer exactly and only what is asked.\n{prompt}",
}


def scaffold(prompt: str, template: str = "plain") -> str:
    """SCAFFOLD - the prompt scaffold: shapes the task prompt before the draw.
    A pure transform; nothing leaves the machine."""
    return SCAFFOLDS.get(template, SCAFFOLDS["plain"]).replace("{prompt}", prompt)


def score(payload: dict, task: dict) -> dict:
    """SCORER - receipt-measured fields ONLY (P0 part contract): pass + axes
    {latency_ms, tokens, ok, zone}. No model-judged quality number exists at P0 -
    an invented number would be the first dishonest pixel."""
    exp = task.get("expect") or {}
    text = (payload.get("text") or "").strip()
    drew = bool(payload.get("ok"))
    if "exact" in exp:
        hit = text == exp["exact"]
    elif "contains" in exp:
        hit = exp["contains"].lower() in text.lower()
    else:
        hit = bool(text)                       # open target: a real answer returned
    return {"pass": bool(drew and hit),
            "axes": {"latency_ms": payload.get("latency_ms"),
                     "tokens": payload.get("tokens"),
                     "ok": drew,
                     "zone": payload.get("zone")}}


_LEVEL_BY_NAME = {name: lvl for lvl, name in trust.LEVEL_NAMES.items()}


def trust_gate(part_id: str, row: dict) -> dict:
    """THE TRUST LAW at fire time (P0 SPEC ADDENDUM, binding from P0): the part's manifest
    trust binding is evaluated at THIS moment, never cached (the call-time predicate law,
    A14 s4.2). allowed -> fire; draft_only -> draft path only (an artifact may be produced,
    nothing leaves the machine - so a part whose verbs reach outward holds); otherwise
    refuse, naming the level. The manifest's min_level dial is ENFORCED here (warden rider
    2026-07-20): a declared dial with no enforcement path is the exact fake-lever class the
    validator refuses for policy keys (A7 law). P0's parts bind no charter row -> fire;
    the LAW ships."""
    binding = (row or {}).get("trust")
    if not binding:
        return {"fire": True, "why": "no charter binding (P0 part)"}
    floor_name = binding.get("min_level")
    floor = _LEVEL_BY_NAME.get(floor_name) if floor_name is not None else None
    if floor_name is not None and floor is None:
        return {"fire": False, "why": f"refused - min_level '{floor_name}' is not a trust "
                                      "level (manifest drift refuses loudly, A14 s4.3)"}
    caps = binding.get("capability")
    caps = caps if isinstance(caps, list) else [caps]
    drafted = []
    for cap in caps:
        try:
            t = trust.check(cap)
        except KeyError as e:
            return {"fire": False, "why": f"refused - {str(e)[:140]}"}
        if floor is not None and t["level"] < floor:
            return {"fire": False,
                    "why": f"refused - {cap} at {t['name']}, the manifest binds min_level "
                           f"{floor_name} (a declared dial is enforced, never decorative)"}
        if t["allowed"]:
            continue
        if t.get("draft_only"):
            reaches = set(row.get("capabilities") or []) & {"draw", "act-external"}
            if reaches:
                return {"fire": False,
                        "why": f"draft_only - {cap} at DRAFT: the draft path holds, "
                               "nothing leaves"}
            drafted.append(cap)
            continue                            # DRAFT and nothing leaves: artifact allowed
        return {"fire": False, "why": f"refused - {cap} at {t['name']} (trust law)"}
    if drafted:                                 # the run row must SAY it ran under draft terms
        return {"fire": True, "draft": True,
                "why": f"draft terms - {', '.join(drafted)} at DRAFT: artifact only, "
                       "nothing leaves"}
    return {"fire": True, "why": "trust binding holds"}


# --------------------------------------------------------------------------------------
# 3. The run store - bench_runs.json, append-only, restart-survivable. Rows are only ever
#    ADDED, never rewritten (pr.time's bench law, A13 s2.6); every row carries its run_id
#    (the run-tag law - the entity's own concurrent draws can never misattribute here).
# --------------------------------------------------------------------------------------
def _save_retrying(st: dict, attempts: int = 12) -> None:
    """atomic_save_json with a Windows truth-tax retry: os.replace is DENIED while a
    concurrent poller holds the file open for read (no FILE_SHARE_DELETE) - proven live
    2026-07-20, first fire, r-01: a trace row lost the race to its own status poller.
    The reader is gone in milliseconds; retry (jittered, so two writers cannot re-collide
    in step) inside the held lock rather than lose a row. If it still fails after the
    budget, fail LOUD - a run whose rows cannot land must halt honestly, never trace
    silently into nowhere. End rows get a longer budget from _append_rows: losing one
    zombies a run into CARRIER LOST (crash rider 2026-07-20)."""
    for _ in range(attempts):
        try:
            grid.atomic_save_json(RUNS_FP, st)
            return
        except PermissionError:
            time.sleep(0.05 + random.random() * 0.05)
    grid.atomic_save_json(RUNS_FP, st)


def _append_rows(rows: list) -> None:
    attempts = 40 if any(r.get("type") == "end" for r in rows) else 12
    with grid.file_lock(RUNS_FP) as locked:
        if not locked:              # degraded-unlocked is grid law, but never silent here:
            pulse.emit("bench", "lock-timeout",   # a lost append must be diagnosable
                       "bench_runs.json lock timed out - appending unlocked, rows may race",
                       ok=False)
        st = grid.load_json(RUNS_FP, {"version": "0.1.0", "rows": []})
        st.setdefault("rows", []).extend(rows)
        _save_retrying(st, attempts)


def _rotated(st: dict) -> dict:
    """Inside the held lock, at run open ONLY (never mid-run): when bench_runs.json
    outgrows ROTATE_BYTES, archive the whole store to bench_runs.json.1 and start fresh,
    preserving (1) the RUN COUNTER via run_base - run ids never collide across rotations -
    and (2) every construct|task|zone LAST/BEST fold via carry, so the pane's rider
    survives rotation (crash rider 2026-07-20). Rows are archived, never destroyed."""
    try:
        if os.path.getsize(RUNS_FP) <= ROTATE_BYTES:
            return st
    except OSError:
        return st
    rows = st.get("rows", [])
    carry = dict(st.get("carry") or {})        # keys not re-seen fold forward untouched
    for c, t, z in {(r.get("construct"), r.get("task"), r.get("zone"))
                    for r in rows if r.get("type") == "start"}:
        carry[f"{c}|{t}|{z}"] = _last_best(st, c, t, z)   # folds these rows AND the old carry
    grid.atomic_save_json(RUNS_FP + ".1", st)
    return {"version": st.get("version", "0.1.0"),
            "run_base": st.get("run_base", 0) + sum(1 for r in rows
                                                    if r.get("type") == "start"),
            "carry": carry, "rows": []}


def _open_run(spec: dict, task: dict) -> str:
    """Mint a sequential run_id and land the start row in ONE locked read-modify-write."""
    with grid.file_lock(RUNS_FP) as locked:
        if not locked:
            pulse.emit("bench", "lock-timeout",
                       "bench_runs.json lock timed out - start row lands unlocked", ok=False)
        st = _rotated(grid.load_json(RUNS_FP, {"version": "0.1.0", "rows": []}))
        n = 1 + st.get("run_base", 0) + sum(1 for r in st.get("rows", [])
                                            if r.get("type") == "start")
        run_id = f"r-{n:02d}"
        st.setdefault("rows", []).append(
            {"run_id": run_id, "type": "start", "t": round(time.time(), 3),
             "construct": spec.get("id") or "c-unnamed", "task": task["id"],
             "zone": spec["zone"], "parts": list(spec["parts"])})
        _save_retrying(st)
    return run_id


def _last_best(st: dict, construct=None, task=None, zone=None) -> dict:
    """LAST/BEST from the append-only rows plus any rotation carry (the addendum rider).
    LAST = the newest completed run's total; BEST = the fastest PASSING run's total.
    Folds by construct id + task + ZONE (warden rider 2026-07-20): a rerun of the same
    id at another zone can never pollute this zone's BEST."""
    starts, ends = {}, []
    for r in st.get("rows", []):
        if r.get("type") == "start":
            starts[r.get("run_id")] = r
        elif r.get("type") == "end":
            s = starts.get(r.get("run_id"), {})
            if construct and s.get("construct") != construct:
                continue
            if task and s.get("task") != task:
                continue
            if zone and s.get("zone") != zone:
                continue
            ends.append(r)
    last = ends[-1].get("total_ms") if ends else None
    passing = [e["total_ms"] for e in ends if e.get("pass") and e.get("total_ms") is not None]
    best = min(passing) if passing else None
    carry = (st.get("carry") or {}).get(f"{construct}|{task}|{zone}")
    if carry:                                  # rotated-away runs still count in the rider
        if last is None:
            last = carry.get("last_ms")
        cb = carry.get("best_ms")
        best = cb if best is None else (best if cb is None else min(best, cb))
    return {"last_ms": last, "best_ms": best}


def last_best(construct=None, task=None, zone=None) -> dict:
    return _last_best(grid.load_json(RUNS_FP, {"rows": []}), construct, task, zone)


# --------------------------------------------------------------------------------------
# 4. Run execution - the harness walks the spine and fires real entry points.
# --------------------------------------------------------------------------------------
def _fire(part: str, row: dict, ctx: dict, spec: dict, task: dict):
    """Fire ONE part's real entry point. Returns (ok, receipt). The caller measures ms."""
    pol = (spec.get("policies") or {}).get(part) or {}
    if part == "tap":
        payload = tap(ctx["prompt"], tier=ctx["tier"], zone=ctx["zone"])
        ctx["payload"] = payload
        receipt = {"plant": payload["plant"], "model": payload["model"],
                   "tried": payload["tried"],          # tried[] = the LADDER micro-hops:
                   "chars": len(payload["text"])}      # reroute marks render as resilience
        return bool(payload["ok"]), receipt
    if part == "scaffold":
        template = pol.get("template", "plain")
        ctx["prompt"] = scaffold(ctx["prompt"], template=template)
        return True, {"template": template, "chars": len(ctx["prompt"])}
    if part == "governor":
        rods = energy.ladder(ctx["tier"], ctx["zone"])
        if not rods:
            return False, {"why": f"no rod on the ladder for {ctx['tier']}/{ctx['zone']}"}
        plant, model = rods[0]
        ok_spend, wait, why = grid.METER.can_spend(plant, model)
        # GOVERNOR before the draw refuses BEFORE any spend (GRAFT-A1: order is semantics)
        return bool(ok_spend), {"rod": f"{plant}/{model}", "why": why, "wait": wait}
    if part == "ladder":
        rods = energy.ladder(ctx["tier"], ctx["zone"])
        return bool(rods), {"rods": len(rods),
                            "top": [f"{p}/{m.rsplit('/', 1)[-1]}" for p, m in rods[:4]]}
    if part == "scorer":
        if ctx["payload"] is None:
            return False, {"why": "nothing to score - SCORER measures a TAP payload"}
        s = score(ctx["payload"], task)
        ctx["score"] = s
        return True, s          # a pass=False is a scored truth, never a scorer failure
    return False, {"why": f"part '{part}' has no fire path in this harness"}


def _execute(run_id: str, spec: dict, task: dict) -> None:
    """The run thread body. This thread only APPENDS to bench_runs.json; the GET handler
    reads the file - the file is the truth (E1 checklist 7.6). A failing link lands its
    row THE MOMENT it fails, so the trace pane sees the failure mid-run (R1 finding 6)."""
    mods = _manifest().get("modules", {})
    # THE REACH / THE STAKE: seating LADDER reaches UP the tier ladder to a cloud rod (a real metered
    # request that spends real budget and can starve on a bad grid day). Bare BRAIN+SCORER stays on the
    # free local hearth (the awe-beat guard). The zone's privacy law still bounds the reach - a
    # sensitive-zone draw stays on-machine no matter what (energy.ladder filters rods by zone).
    reach = "ladder" in (spec.get("parts") or [])
    tier = ("reflex" if reach
            else (task.get("tier_floor")                    # else the task pins local (the free hearth)
                  or ((spec.get("rods") or {}).get("default") or {}).get("tier")
                  or "reflex"))
    ctx = {"prompt": task["prompt"], "zone": spec["zone"], "tier": tier,
           "payload": None, "score": None}
    t_run = perf_counter()
    pulse.emit("bench", "run-start", f"{run_id} {spec.get('id')} {task['id']} zone={spec['zone']}")
    try:
        for seq, part in enumerate(spec["parts"]):
            gate = trust_gate(part, mods.get(part) or {})
            if not gate["fire"]:
                total = round((perf_counter() - t_run) * 1000, 1)
                _append_rows([
                    {"run_id": run_id, "type": "link", "seq": seq, "part": part,
                     "t": round(time.time(), 3), "ms": 0.0, "ok": False,
                     "receipt": {"why": gate["why"]}},
                    {"run_id": run_id, "type": "end", "t": round(time.time(), 3),
                     "ok": False, "pass": False, "halted_at": part, "total_ms": total}])
                pulse.emit("bench", "halt", f"{run_id} {part}: {gate['why']}", ok=False)
                return
            _append_rows([{"run_id": run_id, "type": "link_open", "seq": seq,
                           "part": part, "t": round(time.time(), 3)}])
            t0 = perf_counter()
            try:
                ok, receipt = _fire(part, mods.get(part) or {}, ctx, spec, task)
            except Exception as e:
                ok, receipt = False, {"error": str(e)[:180]}
            ms = round((perf_counter() - t0) * 1000, 1)   # the harness's own clock, per link
            link = {"run_id": run_id, "type": "link", "seq": seq, "part": part,
                    "t": round(time.time(), 3), "ms": ms, "ok": ok, "receipt": receipt}
            if gate.get("draft"):
                link["draft"] = True   # fired under draft terms: artifact only, nothing leaves
            _append_rows([link])
            pulse.emit("bench", "link", f"{run_id} {part} {ms}ms {'ok' if ok else 'FAIL'}",
                       ok=ok)
            if not ok:
                total = round((perf_counter() - t_run) * 1000, 1)
                _append_rows([{"run_id": run_id, "type": "end", "t": round(time.time(), 3),
                               "ok": False, "pass": False, "halted_at": part,
                               "total_ms": total}])
                pulse.emit("bench", "run-end", f"{run_id} HALTED AT {part} {total}ms",
                           ok=False)
                return
        total = round((perf_counter() - t_run) * 1000, 1)
        s = ctx["score"]
        end = {"run_id": run_id, "type": "end", "t": round(time.time(), 3), "ok": True,
               "total_ms": total, "scored": s is not None,
               "pass": bool(s["pass"]) if s else None,
               "axes": (s or {}).get("axes")}
        if s is None:
            end["receipt"] = "UNSCORED - no record without SCORER"
        _append_rows([end])
        pulse.emit("bench", "run-end",
                   f"{run_id} {'pass' if end['pass'] else ('fail' if s else 'unscored')} "
                   f"{total}ms", ok=True)
    except Exception as e:                       # the harness itself broke: say so, honestly
        total = round((perf_counter() - t_run) * 1000, 1)
        try:
            _append_rows([{"run_id": run_id, "type": "end", "t": round(time.time(), 3),
                           "ok": False, "pass": False, "halted_at": "harness",
                           "total_ms": total, "error": str(e)[:180]}])
        except Exception as e2:                  # the end row itself could not land: pulse it
            pulse.emit("bench", "row-lost",      # so the zombie run is diagnosable, never silent
                       f"{run_id} end row could not land: {str(e2)[:80]}", ok=False)
        pulse.emit("bench", "run-end", f"{run_id} harness error: {str(e)[:80]}", ok=False)


def _execute_released(run_id: str, spec: dict, task: dict) -> None:
    try:
        _execute(run_id, spec, task)
    finally:
        _RUN_LOCK.release()


# --------------------------------------------------------------------------------------
# 5. The run contract (P0 SPEC ADDENDUM) - what controlroom.py wires to.
# --------------------------------------------------------------------------------------
def start_run(req: dict) -> dict:
    """POST /api/construct/run -> {run_id} immediately; the run executes in its own thread.
    An illegal spec is refused as a receipt naming the clause - no run is minted.
    req: {spec?: construct spec, task?: task id} - defaults to the opening construct
    (TAP + SCORER) on the one curated task."""
    req = req or {}
    task_id = req.get("task") or DEFAULT_TASK
    task = TASKS.get(task_id)
    if not task:
        return {"ok": False,
                "refused": f"unknown bench task '{task_id}' - P0 ships exactly one: {DEFAULT_TASK}"}
    spec = req.get("spec") or DEFAULT_CONSTRUCT
    v = validate_spec(spec)
    if not v["ok"]:
        return {"ok": False, "refused": v["refused"]}
    if not _RUN_LOCK.acquire(blocking=False):
        return {"ok": False, "refused": "one packet, one run at a time - a run is live (E4 s8.2)"}
    try:
        run_id = _open_run(spec, task)
    except Exception as e:
        _RUN_LOCK.release()
        return {"ok": False, "error": f"could not open the run: {str(e)[:140]}"}
    try:
        # Thread START inside the guard (crash blocker 2026-07-20): if the OS refuses the
        # thread (RuntimeError under pressure - correlated, since every request already
        # spawns one), the lock must NOT latch shut until restart and the minted start row
        # must not zombie into CARRIER LOST. Once start() SUCCEEDS, release belongs to
        # _execute_released's finally ALONE - never release twice.
        threading.Thread(target=_execute_released, args=(run_id, spec, task),
                         daemon=True).start()
    except Exception as e:
        _RUN_LOCK.release()
        try:                                     # resolve the minted start row honestly
            _append_rows([{"run_id": run_id, "type": "end", "t": round(time.time(), 3),
                           "ok": False, "pass": False, "halted_at": "harness",
                           "total_ms": 0.0,
                           "error": f"run thread could not start: {str(e)[:140]}"}])
        except Exception:
            pulse.emit("bench", "row-lost", f"{run_id} end row could not land", ok=False)
        return {"ok": False, "error": f"run thread could not start: {str(e)[:140]}"}
    return {"ok": True, "run_id": run_id, "status": "running",
            "task": task["id"], "zone": spec["zone"]}


def run_status(run_id: str) -> dict:
    """GET /api/construct/run?id= - the persisted run row, folded from the append-only
    run-tagged rows. Reads the file on every call (the file is the truth). Includes the
    LAST/BEST readout for the pane's one-line rider."""
    if not run_id:
        return {"ok": False, "error": "id= REQUIRED - poll by run_id (the run-tag law)"}
    st = grid.load_json(RUNS_FP, {"rows": []})
    rows = [r for r in st.get("rows", []) if r.get("run_id") == run_id]
    if not rows:
        return {"ok": False, "error": f"unknown run '{run_id}'"}
    out = {"ok": True, "run_id": run_id, "status": "running", "links": [], "open_link": None}
    last_t = 0.0
    for r in rows:
        t = r.get("t")
        if isinstance(t, (int, float)):        # a hand-poisoned row never breaks the fold
            last_t = max(last_t, t)
        kind = r.get("type")
        if kind == "start":
            out.update(construct=r.get("construct"), task=r.get("task"),
                       zone=r.get("zone"), parts=r.get("parts"), started=r.get("t"))
        elif kind == "link_open":
            out["open_link"] = {"part": r.get("part"), "seq": r.get("seq"), "t": r.get("t")}
        elif kind == "link":
            link = {k: r.get(k) for k in ("seq", "part", "ms", "ok", "receipt")}
            if r.get("draft"):
                link["draft"] = True           # ran under draft terms - the row says so
            out["links"].append(link)
            out["open_link"] = None
        elif kind == "end":
            out["status"] = "done" if r.get("ok") else "halted"
            out.update(ended=r.get("t"), total_ms=r.get("total_ms"),
                       run_ok=r.get("ok"), scored=r.get("scored"), **{"pass": r.get("pass")})
            if r.get("axes") is not None:
                out["axes"] = r["axes"]
            if r.get("halted_at"):
                out["halted_at"] = r["halted_at"]
            if r.get("receipt"):
                out["receipt"] = r["receipt"]
            if r.get("error"):
                out["error"] = r["error"]
    if out["status"] == "running" and time.time() - last_t > STALE_S:
        out["status"] = "lost"
        # evidence only, cause unproven (crash rider 2026-07-20): the same stale state is
        # reachable with the process alive and a save that lost its race - r-01's real class
        out["receipt"] = f"CARRIER LOST - no row landed for {int(time.time() - last_t)}s"
    out.update(_last_best(st, out.get("construct"), out.get("task"), out.get("zone")))
    return out


# --------------------------------------------------------------------------------------
# 6. `python bench_core.py` - dry proof; --fire runs the opening construct for real
# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    mods = _manifest().get("modules", {})
    print(f"bench_core - manifest rows: {len(mods)} | tasks: {', '.join(TASKS)}")
    v = validate_spec(DEFAULT_CONSTRUCT)
    print("opening construct (tap+scorer):", "LEGAL" if v["ok"] else v["refused"])
    bad = dict(DEFAULT_CONSTRUCT)
    bad.pop("zone", None)
    print("zoneless spec refusal:", validate_spec(bad)["refused"])
    print("last/best:", last_best())
    if "--fire" in sys.argv:
        out = start_run({})
        print("fire:", out)
        if out.get("ok"):
            while True:
                time.sleep(0.5)
                s = run_status(out["run_id"])
                if s.get("status") != "running":
                    print(json.dumps(s, ensure_ascii=False, indent=1))
                    break
