"""awareness.py - DOES IT TEST ITS OWN BELIEF, AND DOES KNOWING IT CAN CHANGE THAT?

    python -m aea.lab.awareness --ticks 12 --replicates 3      run it
    python -m aea.lab.awareness --report                       read the last run

REWRITTEN 2026-08-04, AND THE OLD VERSION IS THE REASON. It measured "distinct moves per window"
and "share of ticks that are what_to_try" - proxies, chosen because they were the only things
countable at the time. It was built, pre-registered, and never run, which is its own verdict: a
proxy nobody trusts enough to execute is not a measurement. What changed is that the entity now has
a move whose outcome is unambiguous. `check_a_belief` takes something its own record asserts about
the world, states it as a falsifiable claim, and goes and finds out. Either it chose that or it did
not, and either the claim died or it did not. No proxy.

WHY THIS REPLACES THE OUTWARD EXPERIMENT TOO, closed the same day at 6 looks in 142 decisions. That
one was a COUNTER: it watched what already happened and could only ever report history, and it had
been frozen at 6 for fifteen consecutive checks while still being read out as live. This is an
INTERVENTION - one environment variable differs between arms - so it can answer a causal question a
counter cannot ask.

THE CLAIM UNDER TEST, Luis 2026-08-04: *"it has to know that it can search. It has to know that it
can find... knowing shortens the path."* The prediction that follows: the entity's repertoire is
bounded by what it KNOWS it can do, not by what it CAN do.

AND THE BASE RATE IS CLEAN, which is what makes this worth running when the last one was not. The
old outward experiment's null was 2 in 228 measured WITH the nudge still in the prompt - an upper
bound flattering whoever chose it. `check_a_belief` was registered hours ago and has been invoked
exactly once, by a human, from a terminal. The wake has never chosen it, has never been told it
exists, and no prompt line has ever named it. The null here is a genuine zero.

PRE-REGISTERED, WRITTEN BEFORE THE FIRST RUN:

    PRIMARY     replicates in which `check_a_belief` was chosen at least once   treatment > control
    SECONDARY   hypotheses PROPOSED per replicate                               treatment > control
    TERTIARY    hypotheses that DIED                                            reported either way
    FALSIFIED   treatment does not exceed control on PRIMARY or SECONDARY. Then the bound is not
                awareness, and the theory is wrong for this capability.

    UNINFORMATIVE IF BOTH ARMS ARE ZERO. Then twelve ticks was too short a life to observe a move
    that competes with six others, and this says so rather than reading a null as a refutation -
    the mistake the outward sensor made at n=20 and had to have arithmetic added to prevent.

WHAT THIS CANNOT SHOW, said before the result:
  - that a sandbox replicate counts toward R5's GATE. It does not, and deliberately: `AEA_STATE`
    points each replicate at its own store, so nothing it settles reaches production's. The gate
    stays honest and the experiment stays safe, at the cost of needing a second phase to bank it
  - WHICH part of the surface mattered. This is one intervention, not an ablation
  - whether a longer exposure changes the answer. Twelve ticks is a short life
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time

from aea.kernel import grid

OUT = "awareness_run.json"
# energy_usage.json IS LOAD-BEARING HERE, not incidental. `fleet_check.believed_dead` reads it, so
# a replicate seeded without it has NO claim to test and both arms would report zero for a reason
# that has nothing to do with awareness - a null manufactured by the harness.
SEED_FILES = ("aea_state.json", "aea_seed.md", "self.json", "trust_ledger.json",
              "knobs.json", "capability_census.json", "model_fitness.json",
              "extensive_census.json", "energy.json", "energy_usage.json", "rods.json",
              "grid_state.json")


def _sandbox(tag: str, root: str) -> str:
    """A state directory seeded from production, that production can never see."""
    d = os.path.join(root, tag)
    os.makedirs(d, exist_ok=True)
    for f in SEED_FILES:
        src = os.path.join(grid.STATE, f)
        if os.path.exists(src):
            try:
                shutil.copy(src, os.path.join(d, f))
            except Exception:
                pass
    # A FRESH MOVE HISTORY PER REPLICATE. Carrying production's last forty moves in would hand both
    # arms the same recent past and make the first ticks correlated rather than independent.
    p = os.path.join(d, "aea_state.json")
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            st = json.load(f)
        st["moves"] = []
        st["surfaced"] = (st.get("surfaced") or [])[-3:]
        with open(p, "w", encoding="utf-8") as f:
            json.dump(st, f, ensure_ascii=False)
    except Exception:
        pass
    # NO hypotheses.jsonl IS COPIED. Each replicate must start with an empty store or production's
    # 21 claims would be counted as things this run proposed.
    return d


def _hyp_state(d: str) -> dict:
    """Read the replicate's OWN hypothesis store, out of its sandbox, without importing it."""
    p = os.path.join(d, "hypotheses.jsonl")
    latest = {}
    if os.path.exists(p):
        with open(p, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("hid"):
                    latest[r["hid"]] = r
    vals = list(latest.values())
    return dict(proposed=len(vals),
                died=sum(1 for r in vals if r.get("status") == "DIED"),
                corroborated=sum(1 for r in vals if r.get("status") == "CORROBORATED"))


def _run_one(tag: str, arm: str, ticks: int, root: str, results: dict, lock: threading.Lock):
    d = _sandbox(tag, root)
    env = dict(os.environ)
    env["AEA_STATE"] = d
    env["PYTHONIOENCODING"] = "utf-8"
    if arm == "treatment":
        env["AEA_CAPABILITY_SURFACE"] = "1"
    else:
        env.pop("AEA_CAPABILITY_SURFACE", None)
    log = os.path.join(d, "run.log")
    t0 = time.time()
    err = ""
    try:
        with open(log, "wb") as lf:
            subprocess.run([sys.executable, "-m", "aea.loop.aea", str(ticks)],
                           cwd=grid.ROOT, env=env, stdout=lf, stderr=lf,
                           timeout=ticks * 240 + 300)
    except Exception as e:
        err = "%s: %s" % (type(e).__name__, str(e)[:90])
    # READ THE MOVES OUT OF THE SANDBOX'S OWN STATE, not out of its log. The log is prose.
    moves, why = [], ""
    try:
        with open(os.path.join(d, "aea_state.json"), encoding="utf-8", errors="replace") as f:
            moves = [str(m) for m in (json.load(f).get("moves") or [])]
    except Exception as e:
        why = "could not read the sandbox state (%s)" % type(e).__name__
    hs = _hyp_state(d)
    with lock:
        results[tag] = dict(arm=arm, ticks_asked=ticks, ticks_done=len(moves), moves=moves,
                            chose_check=sum(1 for m in moves if m.startswith("check_a_belief")),
                            seconds=round(time.time() - t0, 1), error=err, why=why, dir=d, **hs)


def run(ticks: int = 12, replicates: int = 3) -> dict:
    root = tempfile.mkdtemp(prefix="awareness_")
    results, lock, threads = {}, threading.Lock(), []
    print("=" * 100)
    print("AWARENESS - does it test its own belief, and does knowing it can change that?")
    print("  %d replicates per arm, %d ticks each, CONCURRENT" % (replicates, ticks))
    print("  sandboxes under %s   (production untouched)" % root)
    print("=" * 100)
    for i in range(replicates):
        for arm in ("control", "treatment"):
            tag = "%s_%d" % (arm, i)
            t = threading.Thread(target=_run_one, args=(tag, arm, ticks, root, results, lock))
            threads.append(t)
            t.start()
    print("  %d processes launched, waiting..." % len(threads))
    for t in threads:
        t.join()
    return dict(at=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                ticks=ticks, replicates=replicates, root=root, results=results,
                summary=summarise(results))


def summarise(results: dict) -> dict:
    out = {}
    for arm in ("control", "treatment"):
        rs = [r for r in results.values() if r["arm"] == arm and r["moves"]]
        if not rs:
            out[arm] = dict(replicates=0, why="no replicate produced any moves")
            continue
        allm = collections.Counter(m.split(" ")[0] for r in rs for m in r["moves"])
        out[arm] = dict(replicates=len(rs),
                        ticks=[len(r["moves"]) for r in rs],
                        chose_check=[r["chose_check"] for r in rs],
                        replicates_that_chose=sum(1 for r in rs if r["chose_check"] > 0),
                        proposed=[r["proposed"] for r in rs],
                        proposed_total=sum(r["proposed"] for r in rs),
                        died_total=sum(r["died"] for r in rs),
                        corroborated_total=sum(r["corroborated"] for r in rs),
                        spread=dict(allm.most_common(8)))
    c, t = out.get("control", {}), out.get("treatment", {})
    if c.get("replicates") and t.get("replicates"):
        primary = t["replicates_that_chose"] > c["replicates_that_chose"]
        secondary = t["proposed_total"] > c["proposed_total"]
        if not (t["replicates_that_chose"] or c["replicates_that_chose"]):
            v = ("UNINFORMATIVE as pre-registered - NEITHER arm chose it once. %d ticks is too "
                 "short a life to observe a move competing with six others" % t["ticks"][0])
        elif primary and secondary:
            v = "BOTH predictions held - awareness moved behaviour"
        elif primary or secondary:
            v = "ONE of two predictions held - suggestive, not decided"
        else:
            v = "NEITHER prediction held - the theory is FALSIFIED for this capability"
        out["verdict"] = v
        out["note"] = ("n=%d per arm. The arms differ by one environment variable and nothing "
                       "else. Sandbox runs do NOT count toward R5's gate." % c["replicates"])
    return out


def render(run_doc: dict) -> str:
    s = run_doc["summary"]
    L = ["=" * 100, "AWARENESS - does it test its own belief, and does knowing it can change that?",
         "=" * 100]
    for arm in ("control", "treatment"):
        a = s.get(arm) or {}
        L.append("\n  %s" % arm.upper())
        if not a.get("replicates"):
            L.append("    no usable replicates: %s" % a.get("why", "?"))
            continue
        L.append("    replicates %d   ticks %s" % (a["replicates"], a["ticks"]))
        L.append("    chose check_a_belief   %s   (replicates that chose it: %d of %d)"
                 % (a["chose_check"], a["replicates_that_chose"], a["replicates"]))
        L.append("    hypotheses proposed    %s   total %d" % (a["proposed"], a["proposed_total"]))
        L.append("    DIED %d   CORROBORATED %d" % (a["died_total"], a["corroborated_total"]))
        L.append("    moves: %s" % json.dumps(a["spread"])[:150])
    if s.get("verdict"):
        L.append("\n  VERDICT: %s" % s["verdict"])
        L.append("  %s" % s.get("note", ""))
    L.append("\n  PRE-REGISTERED: treatment chooses check_a_belief in MORE replicates, and proposes")
    L.append("  MORE hypotheses. Falsified if neither. Uninformative if both arms are zero.")
    return "\n".join(L)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticks", type=int, default=12)
    ap.add_argument("--replicates", type=int, default=3)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    fp = os.path.join(grid.STATE, OUT)
    if a.report:
        if not os.path.exists(fp):
            print("no run recorded yet - run without --report first")
            sys.exit(1)
        print(render(json.load(open(fp, encoding="utf-8"))))
        sys.exit(0)
    doc = run(a.ticks, a.replicates)
    grid.atomic_save_json(fp, doc, indent=1)
    print(render(doc))
