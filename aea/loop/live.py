"""live.py - THE CONTINUOUS LIFE. The entity that is always alive, even when it sleeps.

Luis's model: the computer is not always on - that is fine. When it runs, the entity is AWAKE and
serves; when the machine is off, the process dies but its state is on disk - ASLEEP, still alive -
and it resumes on the next wake. Continuity lives in the files, not in the process.

TWO MODES, like a real nervous system:
  AWAKE  - if today's brief isn't done, produce it (serve Luis).
  ASLEEP - otherwise consolidate the transcript backlog (episodic -> semantic memory), a slice per
           tick, until the whole corpus is learned. Idle time becomes memory. Runs on LOCAL power.

It NEVER dies on an error (a bad tick is logged and the loop continues), writes a HEARTBEAT every
tick so its aliveness is visible, and RESUMES from heartbeat.json across restarts (proves it
survived sleep). Heavy work is delegated to the proven scripts as subprocesses, so a crash in one
can never take down the life.

  python live.py                          # run forever, 30-min ticks (production)
  python live.py --interval 1 --ticks 2   # bounded demo (prove heartbeat + restart-resume)
  python live.py --status                 # print the heartbeat and exit
"""
from __future__ import annotations
import json, os, sys, time, subprocess, signal
from datetime import datetime, timezone

from aea.kernel import grid
from aea.kernel import pulse  # durable persistence + the nervous signal (the brain view watches)

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(grid.STATE)              # repo root (grid.STATE = ROOT/state); cwd for '-m aea.*' subprocess runs
HEARTBEAT = os.path.join(grid.STATE, "heartbeat.json")
LOG = os.path.join(grid.STATE, "live.log")
PIDLOCK = os.path.join(grid.STATE, "live.instance")
PY = sys.executable
CONSOLIDATE_SLICE = 3          # sessions learned per idle (sleep) tick

_stop = {"now": False}
def _on_signal(*_):            # a clean sleep, not a crash: mark asleep and exit
    _stop["now"] = True


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def load_hb() -> dict:
    return grid.load_json(HEARTBEAT, {"alive_since": now_iso(), "boot_count": 0, "total_ticks": 0,
                                      "last_brief_date": None, "consolidated_sessions": 0, "history": []})

def save_hb(hb: dict):
    grid.atomic_save_json(HEARTBEAT, hb, indent=2)     # kill-safe (review 2026-07-10)

def log(msg: str):
    line = f"{now_iso()}  {msg}"
    try:
        open(LOG, "a", encoding="utf-8").write(line + "\n")
    except Exception:
        pass
    print(line)


def run_script(args: list[str], timeout: int) -> tuple[bool, str]:
    """Delegate heavy work to a proven script; isolate its failure from the life."""
    try:
        r = subprocess.run([PY] + args, cwd=REPO, capture_output=True, text=True, timeout=timeout)
        tail = (r.stdout or r.stderr or "").strip().splitlines()
        return r.returncode == 0, (tail[-1] if tail else "")
    except subprocess.TimeoutExpired:
        return False, f"timeout>{timeout}s"
    except Exception as e:
        return False, str(e)[:80]


def corpus_state() -> tuple[int, int]:
    """(consolidated-AND-existing, total) across ALL projects (2026-07-19: the old single-project
    count + ghost-processed ids made the loop believe 'nothing owed' while today's sessions sat
    unmined). Counts only the intersection of processed ids with files that still exist."""
    try:
        import glob
        from aea.memory import consolidate
        total = len(glob.glob(os.path.join(consolidate.PROJECTS_ROOT, "*", "*.jsonl")))
        meta = grid.load_json(consolidate.META, None)
        if meta is not None:
            return meta.get("processed", 0), total
        return len(consolidate.load_store().get("processed", [])), total
    except Exception:
        return 0, 0


BRIEF_GIVE_UP = 3        # consecutive failures after which the brief stops monopolising the loop


def choose_action(hb: dict) -> tuple[str, list[str], int]:
    """AWAKE if today's brief is undone, else ASLEEP (consolidate) if backlog remains, else IDLE.

    THE STARVATION FIX. This used to return AWAKE:brief on EVERY tick until the brief succeeded. A
    brief that fails for an external reason therefore re-ran the byte-identical action forty-eight
    times a day, and every branch below it - consolidation, the reflection tick - was unreachable for
    the entire outage. `state/trust_ledger.json` holds the receipt: twelve identical entries on
    2026-07-21 at half-hour spacing, and no brief has been produced since 2026-07-20.

    Repeating an action that has failed three times in a row with one cause is not persistence, it is
    the definition of stuck. After BRIEF_GIVE_UP the loop stops paying for it and does the work it can
    still do. The brief is retried on the next calendar day, or immediately once a move is applied.
    """
    stuck = int(hb.get("brief_fails", 0)) >= BRIEF_GIVE_UP
    if hb.get("last_brief_date") != today() and not stuck:
        return "AWAKE:brief", ["-m", "aea.organs.brief"], 240
    done, total = corpus_state()
    if total and done < total:
        return "ASLEEP:consolidate", ["-m", "aea.memory.consolidate", "--limit", str(CONSOLIDATE_SLICE)], 600
    # NOT resting: t6 the reflection tick - self-originate ONE task (the autonomy organ, gated by HADES).
    # This is the wire from an internal goal to an action - what makes the self a loop, not a document.
    if os.path.exists(os.path.join(os.path.dirname(HERE), "organs", "reflect.py")):
        return "REFLECT:self", ["-m", "aea.organs.reflect", "--once"], 240
    return "IDLE", [], 0


def _notice_and_propose(hb: dict, tail: str):
    """THE WIRE FROM A FAILING WAKE TO THE MACHINERY THAT KNOWS WHAT TO CHANGE.

    Until now `impasse`, `unstick` and `crystal` were CLI-only: a full five-rung notice/diagnose/vary/
    record/crystallise loop that no wake path could reach. The entity could be asked whether it was
    stuck and would answer correctly, and nothing ever asked it.

    Two things happen here and the order matters.

    1 THE OUTCOME IS RECORDED EVEN WHEN THE SUBPROCESS DIED. `organs/brief.py` writes the ledger
      itself on a normal run, but a timeout or a crash never reaches that line - so the failure mode
      MOST likely to kill an unattended system was the one the consecutive-failure alarm could never
      see. When the child produced no ledger entry, this writes one, with the cause.

    2 A DIAGNOSIS IS COMPUTED AND SURFACED. `unstick.propose` is still PROPOSE-only by design: it
      writes what it would change and why. Nothing here applies a move. Varying without recording is
      thrashing, and applying without a human is a ceiling this charter has not granted.
    """
    cap = "produce_brief"
    try:
        from aea.kernel import trust, impasse, unstick
        cause = (tail or "").strip()[:70] or "no output"

        # 1 - did the child manage to record anything? Compare the run count before and after.
        led = grid.load_json(trust.LEDGER, {})
        before = (led.get(cap) or {}).get("runs", 0)
        if hb.get("_brief_runs_seen") == before:
            trust.record(cap, False, note="wake: child produced no verdict (%s)" % cause)
        hb["_brief_runs_seen"] = (grid.load_json(trust.LEDGER, {}).get(cap) or {}).get("runs", 0)

        # 2 - diagnose, and say what to change.
        d = impasse.read(cap)
        if d.get("stuck"):
            p = unstick.propose(cap, zone="sensitive")
            move = (p.get("move") or {}) if isinstance(p, dict) else {}
            hb["proposed_move"] = move
            log("  STUCK: %s" % str(d.get("why"))[:90])
            if move:
                log("  PROPOSED: %s %s -> %s" % (move.get("move"), move.get("knob"),
                                                 str(move.get("to"))[:44]))
                log("  WHY: %s" % str(move.get("why"))[:100])
                pulse.emit("life", "propose", "%s: %s -> %s"
                           % (cap, move.get("move"), str(move.get("to"))[:40]), ok=False)
            else:
                log("  EXHAUSTED: every declared move has been tried. Ask for help.")
    except Exception as e:
        log("  (notice/propose failed, loop continues: %s)" % str(e)[:80])


def tick(hb: dict, demo: bool):
    hb["total_ticks"] += 1
    action, args, tmo = choose_action(hb)
    if demo and action.startswith("AWAKE"):        # keep the demo cheap: skip the 60s brief, do a memory slice
        action, args, tmo = "ASLEEP:consolidate(demo)", ["-m", "aea.memory.consolidate", "--limit", "1"], 300
    if not args:
        log(f"tick {hb['total_ticks']}  IDLE (corpus fully consolidated; nothing owed) - resting")
        return
    log(f"tick {hb['total_ticks']}  {action}  -> running {' '.join(args)}")
    pulse.emit("life", "tick", f"#{hb['total_ticks']} {action}")
    ok, tail = run_script(args, tmo)
    pulse.emit("life", "tick-done", f"#{hb['total_ticks']} {action} {'ok' if ok else 'FAIL'}", ok=ok)
    if action.startswith("AWAKE"):
        if ok:
            hb["last_brief_date"] = today()
            hb["brief_fails"] = 0
        else:
            hb["brief_fails"] = int(hb.get("brief_fails", 0)) + 1
            _notice_and_propose(hb, tail)
    done, total = corpus_state()
    hb["consolidated_sessions"] = done
    hb["history"] = (hb.get("history", []) + [f"{now_iso()} {action} {'ok' if ok else 'FAIL'} :: {tail[:80]}"])[-30:]
    log(f"tick {hb['total_ticks']}  {action}  {'ok' if ok else 'FAIL'}  ({tail[:70]})  | corpus {done}/{total}")


def main():
    a = sys.argv
    if "--status" in a:
        hb = load_hb()
        done, total = corpus_state()
        print(json.dumps({k: hb.get(k) for k in
              ("alive_since", "boot_count", "total_ticks", "last_brief_date", "consolidated_sessions")}, indent=2))
        print(f"corpus consolidated: {done}/{total}")
        print("recent:"); [print("  " + h) for h in hb.get("history", [])[-6:]]
        return

    interval = int(a[a.index("--interval") + 1]) if "--interval" in a else 1800
    max_ticks = int(a[a.index("--ticks") + 1]) if "--ticks" in a else None
    demo = "--demo" in a or max_ticks is not None
    signal.signal(signal.SIGINT, _on_signal)
    try:
        signal.signal(signal.SIGTERM, _on_signal)
    except Exception:
        pass

    # SINGLE-INSTANCE guard (review 2026-07-10): two lives racing the same heartbeat/brief was
    # silent double-work. The lock handle is held for the process lifetime; the OS releases it
    # on any death, so there is no stale-lock problem.
    _instance = open(PIDLOCK, "a+b")
    try:
        import msvcrt
        _instance.seek(0); msvcrt.locking(_instance.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        print("another live.py is already running - this one yields."); return
    except ImportError:
        pass

    hb = load_hb()
    hb["boot_count"] += 1                            # every start = a WAKE; proves survival across sleep
    save_hb(hb)
    log(f"=== WAKE #{hb['boot_count']} ===  alive since {hb['alive_since']} | "
        f"resuming at tick {hb['total_ticks']} | interval {interval}s"
        + (f" | {max_ticks} ticks then sleep" if max_ticks else " | forever"))

    n = 0
    while not _stop["now"]:
        try:
            tick(hb, demo)
        except Exception as e:
            log(f"tick error (survived): {e}")       # the life never dies on a bad tick
        # THE SAVE IS INSIDE THE GUARD TOO, and it was not.
        #
        # `tick` was wrapped so a bad tick could never kill the life, and then the very next line
        # wrote to disk UNGUARDED. On Windows a save raises PermissionError whenever anything else
        # holds the file open for a few milliseconds - an editor, a sync client, a virus scanner -
        # so the one call that exists to prove the entity is still alive was also the one call that
        # could end it, for a reason that resolves itself in 50ms. A heartbeat that dies of a
        # transient write is worse than no heartbeat, because the log stops mid-sentence and looks
        # like a crash.
        try:
            save_hb(hb)                               # persist EVERY tick -> asleep-still-alive
        except Exception as e:
            log(f"heartbeat save failed (survived, will retry next tick): {str(e)[:80]}")
        n += 1
        if max_ticks and n >= max_ticks:
            break
        for _ in range(interval):                     # responsive sleep so a stop is a clean sleep
            if _stop["now"]:
                break
            time.sleep(1)

    log(f"=== SLEEP ===  ran {n} ticks this wake; total {hb['total_ticks']}; state persisted. Still alive on disk.")


if __name__ == "__main__":
    main()
