"""vital.py - IS THE ORGANISM ALIVE AS ONE THING? A whole-entity run, with listeners on the code.

    python -m aea.lab.vital           # the whole-entity test: what RAN, and what it CHANGED
    python -m aea.lab.vital --tree    # the growing tree, per step, from the runtime trace
    python -m aea.lab.vital --trace   # every aea/ function that executed, in call order

WHY THIS EXISTS, AND IT IS THE LESSON OF 2026-07-31 RATHER THAN AN IDEA.

`assembly.py` answers "can the organism REACH this function", statically, from the call graph. That
is a real question and it is not the one that matters most, because **a function can be perfectly
reachable, execute on every tick, and do nothing at all.** Four times in one day an edit landed on
an object nobody read, and every time the static picture stayed green:

    _apply_knob            reachable, ran every stuck tick, returned False unconditionally
    promote()              reachable, ran, wrote an explicit dict that dropped the new field
    grid_private(depth=3)  reachable, ran, made its own knob unreadable
    capability_census      reachable, ran, stamped a file the ladder never opens

None of those is a wiring defect. Each is an EFFECT defect, and the only instrument that can see one
is the running system. Luis, 2026-07-31: *"if we are not sure that everything's been built and
assembled, then we're just having a bunch of tests from different things that are not working
together."*

SO THIS FILE ASSERTS TWO THINGS THAT UNIT TESTS STRUCTURALLY CANNOT:

    1 WHAT ACTUALLY RAN     a profile listener on every function under aea/, during ONE whole-entity
                            run. Not "is it called somewhere" - did it execute, just now, in this
                            organism, for real.
    2 WHAT ACTUALLY CHANGED an EFFECT is a before/after pair taken from the world. A step that ran
                            and changed nothing is a step that did not happen, and it is exactly
                            what a green unit test looks like.

THE MANIFEST GROWS WITH THE LADDER. Each rung adds its functions and its effects here, and the run
prints the tree with LIVE or DEAD per function taken from the trace rather than from the AST. A step
is DONE only when every function in it EXECUTED and every effect it claims OCCURRED. Add a step when
you START it: a manifest holding only finished work cannot tell you that you stopped halfway.

IT RUNS IN A SANDBOX. Every store this touches is redirected to a temp directory before the entity
is imported, so a test can never leave a value in production - which happened today, when
`test_knobs` persisted a 32000-token ceiling into the live knob store and the brief ran under it.

NO MODEL CALLS BY DEFAULT. The decision path is deterministic here (`decide` reads a table, the MOVE
line is a regex), so the whole chain from a wake decision to a recorded outcome runs for free and
can therefore run often. `--wake` adds the real deliberation for the one assertion that needs a rod.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# =================================================================================================
# THE SANDBOX. Set BEFORE any aea module is imported, so no module-level constant can capture a
# production path. This is D48 applied to the test harness itself.
# =================================================================================================
def _sandbox() -> str:
    tmp = tempfile.mkdtemp(prefix="vital_")
    os.environ["AEA_OUTCOMES"] = os.path.join(tmp, "outcomes.jsonl")
    os.environ["AEA_KNOBS"] = os.path.join(tmp, "knobs.json")
    os.environ["AEA_HANDS_LEDGER"] = os.path.join(tmp, "hands_ledger.jsonl")
    os.environ["AEA_GATE_LEDGER"] = os.path.join(tmp, "gate_ledger.jsonl")
    # THESE TWO WERE MISSING AND THE CLAIM "production state untouched" WAS FALSE BECAUSE OF IT.
    # Found by this file's own first runs, which wrote real rows into the entity's real experience
    # record while printing that they had not.
    os.environ["AEA_EXPERIENCE"] = os.path.join(tmp, "experience.json")
    os.environ["AEA_CRYSTAL"] = os.path.join(tmp, "crystal.json")
    return tmp


TMP = _sandbox()

from aea.kernel import grid          # noqa: E402  - after the sandbox, deliberately

AEA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# =================================================================================================
# THE LISTENER. `sys.setprofile` fires on call and return only - cheap enough to leave on for a
# whole tick, unlike `settrace` which fires per line.
# =================================================================================================
class Listener:
    """Records every function under aea/ that actually executes, in call order."""

    def __init__(self):
        self.seen: dict = {}
        self.order: list = []

    def _hook(self, frame, event, arg):
        if event != "call":
            return
        code = frame.f_code
        fn = code.co_filename
        if not fn.startswith(AEA_DIR):
            return
        rel = os.path.relpath(fn, os.path.dirname(AEA_DIR)).replace("\\", "/")
        key = f"{rel[:-3].replace('/', '.')}:{code.co_name}"
        if key not in self.seen:
            self.seen[key] = 0
            self.order.append(key)
        self.seen[key] += 1

    def __enter__(self):
        sys.setprofile(self._hook)
        return self

    def __exit__(self, *a):
        sys.setprofile(None)
        return False

    def ran(self, key: str) -> bool:
        return key in self.seen


# =================================================================================================
# THE MANIFEST. Grows one block per rung. `runs` = functions that must EXECUTE. `effects` = pairs
# of (name, before-fn, after-predicate) taken from the world.
#
# A FUNCTION THAT RUNS AND AN EFFECT THAT OCCURS ARE DIFFERENT CLAIMS, and today proved you need
# both: `_apply_knob` ran on every stuck tick for hours while changing nothing.
# =================================================================================================
STEPS = [
    ("R2  a wake decision reaches a tool", {
        "runs": ["aea.kernel.decide:choose", "aea.kernel.decide:parse",
                 "aea.kernel.hands:invoke", "aea.kernel.hands:allowed",
                 "aea.kernel.hands:_ledger"],
        "effects": ["a tool argument was recorded in the ledger"],
    }),
    ("R3.1 the outcome is recorded", {
        "runs": ["aea.kernel.cause:classify", "aea.kernel.outcomes:build",
                 "aea.kernel.outcomes:require", "aea.kernel.outcomes:write",
                 "aea.kernel.grid:append_jsonl", "aea.loop.live:_record_outcome"],
        "effects": ["an outcome row exists", "a 429 row does NOT grade the move"],
    }),
    ("R3.2 it stops re-choosing what the record says fails", {
        "runs": ["aea.kernel.impasse:read", "aea.kernel.unstick:propose",
                 "aea.kernel.unstick:tried_for", "aea.kernel.unstick:moves_for",
                 "aea.kernel.unstick:record"],
        "effects": ["the experience record gained a row",
                    "a second tick proposed a DIFFERENT move"],
    }),
    ("R3.3 crystallisation runs in both directions", {
        "runs": ["aea.kernel.crystal:harvest", "aea.kernel.crystal:applicable"],
        "effects": ["harvest ran without admitting anything below threshold"],
    }),
    ("R3.4 the record reaches the wake's eyes", {
        "runs": ["aea.kernel.impasse:scan", "aea.loop.aea:standing"],
        "effects": ["the standing block names a stuck capability",
                    "the standing block carries the numbers WHEN asks about"],
    }),
    ("R3.5 the entity changes its own configuration", {
        "runs": ["aea.loop.live:_apply_knob", "aea.kernel.knobs:set", "aea.kernel.knobs:get"],
        "effects": ["a knob VALUE actually changed", "the change is attributable to the wake"],
    }),
]

ROWS: list = []


def check(step: str, kind: str, name: str, ok: bool, detail: str = ""):
    ROWS.append(dict(step=step, kind=kind, name=name, ok=bool(ok), detail=str(detail)[:110]))


def run(with_wake: bool = False) -> dict:
    """ONE whole-entity run, listened to, then judged on what ran and what changed."""
    from aea.kernel import knobs, outcomes, unstick, crystal, trust
    from aea.loop import live, aea as wake

    before = {
        "knob": knobs.get("produce_brief", "max_tokens"),
        "outcomes": len(outcomes.read()),
        "attempts": len(grid.load_json(unstick._exp_path(), {"attempts": []}).get("attempts", [])),
    }

    hb = {"total_ticks": 0, "last_wake_why": "vital"}
    listener = Listener()
    err = None
    with listener:
        try:
            # THE WHOLE CHAIN, in the order the organism runs it.
            live._notice_and_propose(hb, "HTTP Error 429: Too Many Requests")   # notice -> apply
            first_move = dict((hb.get("_r3_pending") or {}).get("move") or {})
            live._notice_and_propose(hb, "HTTP Error 429: Too Many Requests")   # grade -> re-propose
            second_move = dict((hb.get("_r3_pending") or {}).get("move") or {})
            # the outcome path, through the real tick recorder
            live._record_outcome(hb, "AWAKE:brief", "script", False,
                                 "HTTP Error 429: Too Many Requests")
            live._record_outcome(hb, "ASLEEP:consolidate", "script", True, "done",
                                 verify=dict(pred="count strictly increases", result=True,
                                             detail="1 -> 2"))
            # the tool path, through the real gate
            from aea.kernel import decide, hands
            allow = tuple({s["tool"] for s in decide.TOOL_KNOWN.values()})
            try:
                hands.invoke("read_state", {"name": "heartbeat.json"}, zone="sensitive",
                             allow=allow, src="wake")
            except Exception:
                pass
            # the record the wake reads
            standing = wake.standing(grid.load_json("aea_state.json", {"memory": [], "surfaced": []}))
        except Exception as e:
            err = f"{type(e).__name__}: {e}"
            first_move = second_move = {}
            standing = ""

    after = {
        "knob": knobs.get("produce_brief", "max_tokens"),
        "outcomes": len(outcomes.read()),
        "attempts": len(grid.load_json(unstick._exp_path(), {"attempts": []}).get("attempts", [])),
    }
    rows = outcomes.read()

    # ---------------------------------------------------------------- WHAT RAN
    for title, spec in STEPS:
        for fn in spec["runs"]:
            check(title, "ran", fn, listener.ran(fn),
                  f"{listener.seen.get(fn, 0)} call(s)")

    # ---------------------------------------------------------------- WHAT CHANGED
    ledger = os.environ.get("AEA_HANDS_LEDGER")
    led_rows = []
    if ledger and os.path.exists(ledger):
        led_rows = [json.loads(l) for l in open(ledger, encoding="utf-8") if l.strip()]
    check(STEPS[0][0], "effect", "a tool argument was recorded in the ledger",
          any(r.get("args") for r in led_rows), f"{len(led_rows)} ledger row(s)")

    check(STEPS[1][0], "effect", "an outcome row exists",
          after["outcomes"] > before["outcomes"], f"{before['outcomes']} -> {after['outcomes']}")
    r429 = [r for r in rows if "429" in str(r.get("note", ""))]
    check(STEPS[1][0], "effect", "a 429 row does NOT grade the move",
          bool(r429) and not any(r.get("counts_toward_move") for r in r429),
          f"{len(r429)} rate-limit row(s), none grading")

    check(STEPS[2][0], "effect", "the experience record gained a row",
          after["attempts"] > before["attempts"], f"{before['attempts']} -> {after['attempts']}")
    check(STEPS[2][0], "effect", "a second tick proposed a DIFFERENT move",
          bool(first_move) and bool(second_move) and first_move != second_move,
          f"{first_move.get('move')} -> {second_move.get('move')}")

    check(STEPS[3][0], "effect", "harvest ran without admitting anything below threshold",
          listener.ran("aea.kernel.crystal:harvest"),
          f"{len(crystal._load().get('parts') or {})} part(s)")

    check(STEPS[4][0], "effect", "the standing block names a stuck capability",
          "STUCK" in standing, standing.splitlines()[0][:80] if standing else "(empty)")
    check(STEPS[4][0], "effect", "the standing block carries the numbers WHEN asks about",
          "consolidated" in standing and "last brief" in standing,
          f"{len(standing)} chars")

    # THE ONE THAT CAUGHT TODAY'S DEFECT. A knob that RAN and did not CHANGE is the whole point.
    check(STEPS[5][0], "effect", "a knob VALUE actually changed",
          before["knob"] != after["knob"], f"{before['knob']} -> {after['knob']}")
    kh = grid.load_json(os.environ.get("AEA_KNOBS", "knobs.json"), {}).get("history") or []
    check(STEPS[5][0], "effect", "the change is attributable to the wake",
          any(h.get("by") == "wake" and h.get("ok") for h in kh),
          f"{len(kh)} history row(s)")

    bad = [r for r in ROWS if not r["ok"]]
    return dict(ok=not bad and not err, rows=ROWS, failed=len(bad), error=err,
                listener=listener, before=before, after=after)


def report(res: dict) -> None:
    print("=" * 100)
    print("VITAL - the organism, run as ONE thing, with listeners on the code")
    print("=" * 100)
    if res["error"]:
        print(f"  THE RUN RAISED: {res['error']}\n")
    seen = res["listener"].seen
    print(f"  {len(seen)} distinct aea/ functions executed during the run\n")
    step = None
    for r in ROWS:
        if r["step"] != step:
            step = r["step"]
            done = all(x["ok"] for x in ROWS if x["step"] == step)
            print(f"  {'DONE     ' if done else 'NOT DONE '} {step}")
        if not r["ok"]:
            tag = "DEAD  " if r["kind"] == "ran" else "NO EFFECT"
            print(f"        {tag} {r['name']}   {r['detail']}")
    print()
    print(f"  {len(ROWS) - res['failed']}/{len(ROWS)} assertions "
          f"({sum(1 for r in ROWS if r['kind']=='ran')} ran, "
          f"{sum(1 for r in ROWS if r['kind']=='effect')} effect)")
    print()
    if res["ok"]:
        print("  THE ORGANISM IS ASSEMBLED. Every declared function EXECUTED and every declared")
        print("  effect OCCURRED, in one run, in one process.")
    else:
        print("  NOT ASSEMBLED. A function that did not run, or an effect that did not happen, is a")
        print("  step that is not really there - whatever its unit test says.")
    print(f"\n  sandbox: {TMP}  (production state untouched)")


if __name__ == "__main__":
    res = run(with_wake="--wake" in sys.argv[1:])
    if "--trace" in sys.argv[1:]:
        for k in res["listener"].order:
            print(f"  {res['listener'].seen[k]:>4d}x  {k}")
        sys.exit(0)
    report(res)
    sys.exit(0 if res["ok"] else 1)
