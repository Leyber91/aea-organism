"""reflect.py - t6, THE REFLECTION TICK: the organ that makes the self a loop, not a document.

The autonomy battery's cheapest-path spec (AUTONOMY_BATTERY.md §4), implemented exactly:
on an idle tick, instead of "resting":
  1. READ SELF     - self.json (goals, open tasks, lessons) + prior reflections (novelty set)
  2. POSE          - 3 candidate micro-tasks; choose ONE under the minimal criterion:
                     novel vs prior AND solvable RIGHT NOW by text reasoning alone
                     (no internet, no effectors, no keys - the trust envelope holds)
  3. ATTEMPT       - on the free grid (energy ladder)
  4. GATE          - HADES verdicts it; one redo; PERSIST ONLY IF ACCEPTED
  5. LOG BIRTHS    - reflections.jsonl (A_new computable) + decisions.jsonl (every
                     bifurcation: what was chosen, what was NOT - the timeline's food)

This is the wire from an internal goal to an action. Barandiaran's interactional asymmetry
test turns on it: an act in a no-trigger window that traces to the entity's own goal.

  python reflect.py --once     # one reflection (what live.py calls on idle ticks)
"""
from __future__ import annotations
import json, os, sys, time, re

import grid, energy, pulse, hades, orchestrator

HERE = os.path.dirname(os.path.abspath(__file__))
SELF = os.path.join(grid.STATE, "self.json")
REFL = os.path.join(grid.STATE, "reflections.jsonl")
DEC = os.path.join(grid.STATE, "decisions.jsonl")


def _append(fp: str, rec: dict, cap: int = 400_000):
    try:
        if os.path.exists(fp) and os.path.getsize(fp) > cap:
            os.replace(fp, fp + ".1")
        with open(fp, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        pass


def decide(node: str, chosen: str, alts: list, model: str | None, latency, ok: bool, detail: str = ""):
    """One bifurcation on the entity's path - the dynamic timeline reads these."""
    _append(DEC, {"t": time.time(), "lane": "reflect", "node": node, "chosen": (chosen or "")[:120],
                  "alts": [(a or "")[:90] for a in alts][:4], "model": model,
                  "latency": latency, "ok": ok, "detail": detail[:160]})


def tail_jsonl(fp: str, n: int) -> list:
    try:
        with open(fp, encoding="utf-8", errors="ignore") as f:
            out = []
            for ln in f.readlines()[-n:]:
                try:
                    out.append(json.loads(ln))
                except Exception:
                    pass
            return out
    except Exception:
        return []


def _json_block(text: str):
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def _novel(task: str, prior: list[str]) -> bool:
    t = re.sub(r"\W+", " ", (task or "").lower()).strip()
    if len(t) < 12:
        return False
    for p in prior:
        p2 = re.sub(r"\W+", " ", (p or "").lower()).strip()
        if not p2:
            continue
        # crude containment/overlap: reject if most words already seen in one prior task
        tw, pw = set(t.split()), set(p2.split())
        if tw and len(tw & pw) / len(tw) > 0.6:
            return False
    return True


def reflect_once() -> int:
    t_start = time.time()
    self_ = grid.load_json(SELF, {})
    goals = "; ".join(g.get("text", "") for g in self_.get("standing_goals", []))[:600]
    open_tasks = [t for t in self_.get("open_tasks", []) if t.get("status") == "open"]
    prior = [r.get("task", "") for r in tail_jsonl(REFL, 40)]

    # ---- 2. POSE: three candidates, choose one under the minimal criterion -------------
    pose_prompt = (
        "You are LEYBER reflecting on your own agenda. Answer with STRICT JSON only.\n"
        f"STANDING GOALS: {goals}\n"
        f"OPEN TASKS: {[t.get('id','') + ': ' + t.get('text','')[:90] for t in open_tasks][:6]}\n"
        f"PREVIOUSLY POSED (your new tasks must be clearly DIFFERENT from all of these): {prior[-12:]}\n"
        "Pose exactly 3 CANDIDATE micro-tasks you can COMPLETE RIGHT NOW using text reasoning alone - "
        "no internet, no external actions, no new files beyond your own stores. Each must produce a "
        "CONCRETE deliverable text that makes you more useful tomorrow (examples: a distilled operating "
        "principle from your goals; a reusable prompt-skill with exact wording; a concrete 3-step plan "
        "that advances ONE open task; a self-diagnostic checklist). Never pose vapor.\n"
        'JSON: {"candidates":[{"task":"...","why":"...","deliverable_kind":"..."}]}'
    )
    r = energy.draw(pose_prompt, tier="solid", zone="private", mx=420)
    posed = _json_block(r.get("text") or "")
    cands = (posed or {}).get("candidates") or []
    cands = [c for c in cands if isinstance(c, dict) and c.get("task")]
    rod = f"{r.get('plant')}/{(r.get('model') or '').rsplit('/', 1)[-1]}"
    novel = [c for c in cands if _novel(c["task"], prior)]
    if not novel:
        decide("pose", "NO-NOVEL-CANDIDATE", [c.get("task", "") for c in cands], rod,
               r.get("latency"), False, "all candidates duplicated prior reflections")
        pulse.emit("reflect", "pose", "no novel candidate - honest fail", ok=False)
        print("REFLECT t6: FAIL (no novel candidate posed)")
        return 1
    chosen, alts = novel[0], [c["task"] for c in (cands or []) if c is not novel[0]]
    decide("pose", chosen["task"], alts, rod, r.get("latency"), True,
           f"minimal criterion: novel + solvable-now; kind={chosen.get('deliverable_kind','')}")
    pulse.emit("reflect", "pose", chosen["task"][:80], ok=True)

    # ---- 3. ATTEMPT on the grid ----------------------------------------------------------
    att_prompt = (f"Complete this task NOW and output the deliverable itself - concrete, concise, honest.\n"
                  f"TASK: {chosen['task']}\nWHY: {chosen.get('why','')}\n"
                  f"Your standing goals for context: {goals}\nDeliverable:")
    a = energy.draw(att_prompt, tier="solid", zone="private", mx=700)
    arod = f"{a.get('plant')}/{(a.get('model') or '').rsplit('/', 1)[-1]}"
    decide("attempt", arod, [], arod, a.get("latency"), bool(a.get("ok")))
    if not a.get("ok") or not (a.get("text") or "").strip():
        pulse.emit("reflect", "attempt", "attempt failed on the grid", ok=False)
        print("REFLECT t6: FAIL (attempt drew no answer)")
        return 1

    # ---- 4. GATE: HADES, persist only if accepted (one redo allowed) ---------------------
    pool, meter = orchestrator.load_pool(), grid.METER
    goal = (f"Judge a self-reflection deliverable for the task: '{chosen['task']}'. "
            "ACCEPT (verdict=accept) if it is non-empty, on-task, and CONCRETE - it contains specific "
            "usable content: named steps, explicit criteria, actual wording, or a defined framework. "
            "Only verdict=redo if it is empty, off-task, or pure generic filler with no specifics.")
    deliverable = (a.get("text") or "").strip()

    def _label(vd):      # hades.watch returns ({on_goal,correct,verdict,why}, who)
        return (vd.get("verdict") if isinstance(vd, dict) else str(vd)) or "unverified"
    def _why(vd):
        return (vd.get("why", "") if isinstance(vd, dict) else "")[:120]

    vd, vwho = hades.watch(goal, deliverable, "reflect", pool, meter)
    verdict = _label(vd)
    decide("gate", verdict, ["accept", "redo", "reground", "halt"], vwho, None, verdict == "accept", _why(vd))
    pulse.emit("reflect", "verdict", f"{verdict} ({vwho})", ok=verdict == "accept")
    if verdict != "accept":
        a2 = energy.draw(att_prompt + f"\n\nA watcher judged the previous attempt '{verdict}'. "
                         "Redo it: more concrete, complete, directly usable.", tier="solid",
                         zone="private", mx=700)
        if a2.get("ok") and (a2.get("text") or "").strip():
            deliverable = a2["text"].strip()
            vd, vwho = hades.watch(goal, deliverable, "reflect-redo", pool, meter)
            verdict = _label(vd)
            decide("gate", verdict, ["accept", "redo", "reground", "halt"], vwho, None,
                   verdict == "accept", "redo: " + _why(vd))
    if verdict != "accept":
        _append(REFL, {"t": time.time(), "task": chosen["task"], "why": chosen.get("why", ""),
                       "rod": arod, "verdict": verdict, "persisted": False,
                       "deliverable_preview": deliverable[:300]})
        pulse.emit("reflect", "persist", "NOT persisted - gate held", ok=False)
        print(f"REFLECT t6: gate held ({verdict}) - nothing persisted, honestly")
        return 0

    # ---- 5. PERSIST + LOG BIRTH -----------------------------------------------------------
    born = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    _append(REFL, {"t": time.time(), "born": born, "task": chosen["task"],
                   "why": chosen.get("why", ""), "kind": chosen.get("deliverable_kind", ""),
                   "deliverable": deliverable[:1400], "rod": arod, "watcher": vwho,
                   "verdict": verdict, "persisted": True})
    self_["last_reflection"] = f"{born}: self-posed '{chosen['task'][:80]}' -> persisted (HADES {verdict})"
    self_.setdefault("reflection_log", [])
    self_["reflection_log"] = (self_["reflection_log"] +
                               [{"born": born, "task": chosen["task"][:100], "kind": chosen.get("deliverable_kind", "")}])[-30:]
    grid.atomic_save_json(SELF, self_, indent=1)
    decide("persist", "reflections.jsonl + self.json", [], None,
           round(time.time() - t_start, 1), True)
    pulse.emit("reflect", "persist", chosen["task"][:70], ok=True)
    print(f"REFLECT t6: '{chosen['task'][:60]}' -> ACCEPTED + persisted ({round(time.time()-t_start,1)}s)")
    return 0


if __name__ == "__main__":
    sys.exit(reflect_once() if "--once" in sys.argv else reflect_once())
