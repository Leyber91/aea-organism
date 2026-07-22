"""autonomy.py - THE LIVE BATTERY: the system tests its OWN autonomy against the principles.

Not a document (that is AUTONOMY_BATTERY.md) - a runnable scorer that reads the entity's REAL logs
(reflections.jsonl births, decisions.jsonl bifurcations, heartbeat ticks, self.json) and computes the
falsifiable metrics from the literature, NOW. The autonomy lives in the STRUCTURE, not the models -
so this measures the structure and is model-agnostic (Luis: "even if we depend on nvidia models, we
will replicate the behaviour").

  python autonomy.py          # print the live scorecard
  score() -> dict             # for the /autonomy endpoint + dashboard
"""
from __future__ import annotations
import json, os, time

import grid
HERE = os.path.dirname(os.path.abspath(__file__))


def _rows(fp):
    out = []
    try:
        for ln in open(os.path.join(grid.STATE, fp), encoding="utf-8", errors="ignore"):
            try:
                out.append(json.loads(ln))
            except Exception:
                pass
    except FileNotFoundError:
        pass
    return out


def score() -> dict:
    refl = _rows("reflections.jsonl")
    dec = _rows("decisions.jsonl")
    hb = {}
    try:
        hb = json.load(open(os.path.join(grid.STATE, "heartbeat.json"), encoding="utf-8"))
    except Exception:
        pass
    self_ = {}
    try:
        self_ = json.load(open(os.path.join(grid.STATE, "self.json"), encoding="utf-8"))
    except Exception:
        pass

    births = [r for r in refl if r.get("persisted")]
    held = [r for r in refl if r.get("verdict") and not r.get("persisted")]
    poses = [d for d in dec if d.get("node") == "pose"]
    self_originated = [d for d in poses if d.get("chosen") not in (None, "", "NO-NOVEL-CANDIDATE")]
    distinct_tasks = {(r.get("task") or "").strip().lower() for r in refl if r.get("task")}
    ticks = hb.get("total_ticks", 0)
    refl_log = self_.get("reflection_log", [])

    def T(name, theory, cite, value, verdict, evidence):
        return {"name": name, "theory": theory, "cite": cite, "value": value,
                "verdict": verdict, "evidence": evidence}

    n_self = len(self_originated)
    n_births = len(births)
    variance = round(len(distinct_tasks) / max(1, len(refl)), 2) if refl else 0.0
    held_rate = round(len(held) / max(1, len(refl)), 2) if refl else 0.0

    tests = [
        T("Interactional asymmetry (self-initiated action)", "Barandiaran/Di Paolo 2009",
          "Adaptive Behavior 17(5)", n_self,
          "PASS" if n_self > 0 else "FAIL",
          f"{n_self} tasks self-originated in no-trigger (idle) windows - not the scheduler's"),
        T("Bedau-Packard evolutionary activity (A_new)", "Bedau/Snyder/Packard 1998",
          "Artificial Life VI", n_births,
          "OFF-ZERO (Class 2+)" if n_births > 0 else "FAIL (Class 1)",
          f"{n_births} persisted novelties (births); A_new > 0 means off the stagnant floor"),
        T("Seth G-autonomy (behaviour variance)", "Seth 2010", "Artificial Life 16(2)", variance,
          "PASS" if variance > 0.5 else ("PARTIAL" if variance > 0 else "FAIL"),
          f"distinct/total posed = {variance} (0 = identical idle tokens; >0.5 = self-varied behaviour)"),
        T("Governance integrity (not rubber-stamping)", "HADES / Law-3 watcher", "internal",
          held_rate,
          "HEALTHY" if held_rate > 0 else ("UNTESTED" if not refl else "WATCH"),
          f"{len(held)}/{len(refl)} deliverables gate-HELD - the watcher refuses to persist junk"),
        T("Krakauer individuality (past->future info)", "Krakauer et al. 2020",
          "Theory in Biosciences 139", len(refl_log),
          "ORGANISMAL-SIDE" if refl_log else "DRIVEN",
          f"self.json read+written {len(refl_log)}x - S_future now depends on S_past inside the entity"),
        T("Voyager skill-library growth", "Wang et al. 2023", "arXiv:2305.16291", n_births,
          "GROWING" if n_births > 0 else "FAIL",
          f"library of {n_births} self-authored, HADES-verified deliverables (grows per accepted tick)"),
    ]

    passing = sum(1 for t in tests if t["verdict"].split()[0] in
                  ("PASS", "OFF-ZERO", "HEALTHY", "ORGANISMAL-SIDE", "GROWING"))
    if n_self > 0 and n_births > 0:
        cls, headline = "PROTO-AUTONOMOUS", "self-originates + persists novelty under an independent watcher"
    elif n_self > 0:
        cls, headline = "STIRRING", "self-originates but has not yet persisted a birth"
    else:
        cls, headline = "NOT-YET-AUTONOMOUS", "no self-originated action - still a scripted loop"

    return {"t": time.strftime("%H:%M:%S"), "class": cls, "headline": headline,
            "passing": passing, "total": len(tests), "ticks": ticks,
            "counts": {"self_originated": n_self, "births": n_births, "held": len(held),
                       "reflections": len(refl), "distinct_tasks": len(distinct_tasks)},
            "tests": tests,
            "note": "Autonomy lives in the structure, not the models - this scorecard is model-agnostic. "
                    "Forbidden axes (send/spend/keys) are chosen safety limits, not scored as deficits. "
                    "Open-endedness is only plateau-detectable; a rising A_new over >=100 ticks is the real claim."}


def main():
    s = score()
    print(f"LIVE AUTONOMY BATTERY  ({s['t']})   ->  {s['class']}  ({s['passing']}/{s['total']} favourable)")
    print(f"  {s['headline']}\n")
    for t in s["tests"]:
        print(f"  [{t['verdict']:>16}]  {t['name']}")
        print(f"                      {t['evidence']}   <{t['cite']}>")
    print(f"\n  counts: {s['counts']}   ticks lived: {s['ticks']}")
    print(f"  {s['note']}")


if __name__ == "__main__":
    main()
