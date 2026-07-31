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
import json, os, re, sys, time, subprocess, signal
from datetime import datetime, timezone

from aea.kernel import grid
from aea.kernel import pulse  # durable persistence + the nervous signal (the brain view watches)
from aea.kernel import decide  # the wire from the loop that THINKS to this one, which ACTS

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
    # THE WAKE GETS FIRST REFUSAL. R1 of the wiring ladder, and the smallest possible version of it:
    # the deliberating loop may REORDER the actions this loop already performs, and may not add one.
    # `decide.KNOWN` is the whole surface and it holds exactly the three below. No capability
    # ceiling is touched, so this wire is reversible by deleting seven lines.
    #
    # Until today `aea/loop/aea.py` decided an action every tick and NOTHING READ IT. This is the
    # line that makes the deliberation load-bearing.
    #
    # The ladder underneath is NOT legacy and must not be removed. It is the correct default for an
    # entity with no better idea, and it already encodes a measured failure: a brief that failed for
    # an external reason re-ran byte-identically forty-eight times a day and starved every branch
    # below it, with twelve identical trust-ledger entries as the receipt.
    cand, why = decide.choose()
    hb["last_wake_why"] = why                      # visible in --status either way
    if cand:
        log(f"  {decide.explain(cand, why)}")
        pulse.emit("wake", "chose", f"{cand['action']} :: {why}")
        if cand.get("kind") == "tool":
            # R2a. A TOOL IS NOT A SUBPROCESS, so it does not go down the argv path. It is stashed
            # for `tick` to invoke through `hands`, which re-checks seat, zone and ledger at the
            # call site - the gate is on the invoke, not on this decision.
            hb["_pending_tool"] = dict(tool=cand["tool"], args=cand["args"])
            return cand["action"], [], 0
        hb.pop("_pending_tool", None)
        return cand["action"], cand["argv"], cand["timeout"]
    hb.pop("_pending_tool", None)
    pulse.emit("wake", "no-decision", why, ok=True)   # ok=True: declining is not a fault

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


VOICE_CFG = "voice_wake.json"        # state/voice_wake.json: {"enabled": bool, "from": 8, "to": 22}


def speak_brief(hb: dict) -> bool:
    """SAY THE BRIEF ALOUD, unprompted. The first thing this entity does with a voice that nobody
    launched by hand.

    Everything built for the voice until now ran only when a person typed the command, which meant
    the entity had a mouth and no way to open it. This is the wire: the wake already produces a
    brief every day, so the moment it succeeds there is something REAL to say - content the system
    generated as its own work, not a greeting invented to have something to speak.

    THREE GUARDS, and each one is here because speaking into an empty room is worse than silence:

      OPT-IN      off unless state/voice_wake.json says enabled. A machine that starts talking
                  after an update, in a house, at night, is not a feature.
      QUIET HOURS a wake ticks around the clock; a person does not. Default 08:00-22:00 local.
      CONTENT     the brief must actually exist and be long enough to be worth a sentence. An
                  empty or placeholder brief is spoken as NOTHING, never as "nothing to report" -
                  law H3, a placeholder is not content.

    Failure is swallowed on purpose: a mute speaker, a busy audio device or a missing file must
    never take down the forever-loop. The heartbeat records whether it spoke, so a silent day is
    diagnosable rather than invisible.
    """
    try:
        cfg = grid.load_json(os.path.join(grid.STATE, VOICE_CFG),
                             {"enabled": False, "from": 8, "to": 22})
        if not cfg.get("enabled"):
            return False
        hour = datetime.now().hour
        lo, hi = int(cfg.get("from", 8)), int(cfg.get("to", 22))
        if not (lo <= hour < hi):
            log(f"  voice: {hour}:00 is outside {lo}-{hi}, staying quiet")
            return False
        p = os.path.join(grid.STATE, "brief_output.md")
        if not os.path.exists(p):
            return False
        raw = open(p, encoding="utf-8").read()
        body = re.sub(r"[#*_`>\-]+", " ", raw)
        body = re.sub(r"\s+", " ", body).strip()
        if len(body) < 80:
            log("  voice: the brief is too thin to be worth saying")
            return False
        # TWO SENTENCES, the same bound the conversation organ enforces. MEASURED: 367 characters
        # is 24 seconds of speech, and a wake that monologues at someone over breakfast is the
        # dashboard failure in audio form.
        parts = [s for s in re.split(r"(?<=[.!?])\s+", body) if len(s.strip()) > 15][:2]
        line = " ".join(parts).strip()[:320]
        if not line:
            return False
        from aea.io import speak as _speak
        ok = _speak.speak("Morning. " + line, cloud_ok=True)
        hb["last_spoke"] = now_iso()
        log(f"  voice: {'spoke' if ok else 'FAILED to speak'} {len(line)} chars of the brief")
        pulse.emit("voice", "brief", line[:80], ok=bool(ok))
        return bool(ok)
    except Exception as e:                 # never let the mouth kill the loop
        log(f"  voice: skipped ({str(e)[:70]})")
        return False


# R3 - THE DECLARED POST-CONDITION PER ACTION. An exit code is not evidence that the work happened:
# MEASURED, `consolidate` exited 0 twenty-five times in one recorded run while `state_bytes` rose
# monotonically with zero decreases. The process succeeded; the consolidation did not.
#
# Each entry is (predicate-in-words, observe) where `observe` returns a comparable scalar. The row
# is graded on STRICTLY INCREASED between before and after. An action with no entry here records an
# UNATTRIBUTABLE outcome rather than a success - which is the honest answer and doubles as the work
# list of what still needs a post-condition. Declaring a predicate we cannot observe would be worse
# than declaring none, because it would look verified.
POST = {
    "ASLEEP:consolidate": ("consolidated session count strictly increases",
                           lambda: corpus_state()[0]),
}


def _post_for(action: str):
    for prefix, spec in POST.items():
        if action.startswith(prefix):
            return spec
    return None


def _record_outcome(hb, action, kind, exit_ok, tail, *, verify=None, exc=None, args=None):
    """Every branch of the tick ends here. A tick that acted and recorded nothing is the hole R3
    exists to close, so this is called from ALL of them - including the refusals and the rest.

    `exit_ok` AND `effect_ok` ARE DIFFERENT FACTS AND THEY ARE STORED SEPARATELY. The row's `ok`
    means VERIFIED SUCCESS - a declared post-condition was evaluated and held. It does NOT mean the
    process exited 0, because exit 0 was recorded 25 times while the work did not happen. When they
    disagree, the disagreement is the finding, and it is exactly what a store built on exit codes
    can never surface. With no declared post-condition the row is UNATTRIBUTABLE: we did not fail,
    we simply did not establish anything, and saying so is what puts the action on the work list."""
    effect_ok = bool(isinstance(verify, dict) and verify.get("result"))
    try:
        from aea.kernel import outcomes
        row = outcomes.build(action, kind, effect_ok, src="wake", args=args, verify=verify, exc=exc,
                             note=str(tail or "")[:280], decision_id=hb.get("total_ticks"))
        row["exit_ok"] = bool(exit_ok)
        row["effect_ok"] = effect_ok
        row["disagreed"] = bool(exit_ok) and isinstance(verify, dict) and not effect_ok
        outcomes.write(row)
    except Exception as e:
        # An outcome that cannot be written must be VISIBLE. It does not kill the tick - the entity
        # must keep breathing - but it is never silent, because a store with invisible holes in it
        # is worse than no store: it reads as evidence.
        log(f"  OUTCOME NOT RECORDED ({type(e).__name__}: {str(e)[:120]})")
        pulse.emit("life", "outcome-lost", f"#{hb.get('total_ticks')} {action}: {str(e)[:90]}", ok=False)


def tick(hb: dict, demo: bool):
    hb["total_ticks"] += 1
    action, args, tmo = choose_action(hb)
    if demo and action.startswith("AWAKE"):        # keep the demo cheap: skip the 60s brief, do a memory slice
        action, args, tmo = "ASLEEP:consolidate(demo)", ["-m", "aea.memory.consolidate", "--limit", "1"], 300
    # R2a - THE TOOL PATH. Separate from the script path because the gate is different: `run_script`
    # spawns a subprocess with an argv we control entirely, while `hands.invoke` re-checks the seat,
    # the zone and the trust ledger before a byte moves. The result is recorded exactly as loudly as
    # a script run, and a REFUSAL is recorded too - a gate that fires silently teaches nobody.
    pend = hb.pop("_pending_tool", None)
    if pend:
        from aea.kernel import hands
        t0 = time.time()
        verify, exc = None, None
        try:
            # THE ALLOW-LIST IS DERIVED FROM THE DECISION TABLES, NOT TYPED HERE. A hand-kept copy
            # is the failure `_moves()` was built to prevent, one layer further out: wiring a tool
            # into `decide` while forgetting this tuple produces a wake that chooses correctly and
            # a daemon that refuses it, and the log reads as a permission problem rather than a
            # missing line. `zone="sensitive"` still gates the network tools out structurally, so
            # deriving the list widens nothing that the zone does not already permit.
            allow = tuple({s["tool"] for s in decide.TOOL_KNOWN.values()}
                          | {s["tool"] for s in decide.FREE_ARG.values()})
            out = hands.invoke(pend["tool"], pend["args"], zone="sensitive", allow=allow,
                               src="wake")
            # THE POST-CONDITION FOR A TOOL, and it replaces a hardcoded `True`. This line read
            # `ok, tail = True, str(out)[:300]`: ANY non-raising return was a success. But
            # `hands.py:342` returns the STRING "ERROR: no such state file" as a perfectly normal
            # value, so reading a file that does not exist was recorded as the tool working. A
            # returned error message is a failed post-condition, not a result.
            body = str(out)
            held = not body.lstrip().upper().startswith("ERROR:")
            verify = dict(pred="the tool returned a payload rather than an error",
                          result=held, detail=body[:120])
            ok, tail = held, body[:300]
        except hands.Refused as e:
            # A REFUSAL IS THE GATE WORKING, not the move being wrong. It is recorded, and it is
            # not evidence about the entity's judgement.
            ok, tail, exc = False, f"REFUSED: {str(e)[:140]}", None
            verify = dict(pred="the gate permitted the call", result=False, detail=str(e)[:120])
        except Exception as e:
            ok, tail, exc = False, f"{type(e).__name__}: {str(e)[:140]}", e
        _record_outcome(hb, action, "tool", ok, tail, verify=verify, exc=exc, args=pend.get("args"))
        el = round(time.time() - t0, 2)
        pulse.emit("life", "tool", f"#{hb['total_ticks']} {action} {pend['args']} "
                                   f"{'ok' if ok else 'FAIL'} {el}s", ok=ok)
        hb["history"] = (hb.get("history", [])
                         + [f"{now_iso()} {action} {'ok' if ok else 'FAIL'} :: {tail[:80]}"])[-30:]
        log(f"tick {hb['total_ticks']}  {action} {pend['args']}  "
            f"{'ok' if ok else 'FAIL'} ({el}s)  {tail[:90]}")
        return

    if not args:
        # A REST MUST BE AS VISIBLE AS AN ACT, and until now it was not: this branch logged to a
        # file and returned, while every acting branch emitted to the bus. An observer watching
        # events could not tell a resting entity from a dead one - which is the exact failure the
        # decide module is built around, already present here.
        #
        # It matters more the further up the ladder we go: a deviation-triggered loop rests most of
        # the time, so silence becomes the normal case and a crash hides inside it perfectly.
        why = hb.get("last_wake_why") or "corpus fully consolidated; nothing owed"
        log(f"tick {hb['total_ticks']}  RESTING - {why}")
        pulse.emit("life", "rest", f"#{hb['total_ticks']} {why}", ok=True)
        # A REST IS RECORDED TOO, and it is not bookkeeping. "It stopped choosing what fails" is
        # satisfied perfectly by an entity that declines everything, so the certificate has to be
        # able to tell "it learned" from "it went quiet". That needs the declines counted, not just
        # the acts. It is UNATTRIBUTABLE by construction: nothing was attempted, so nothing about
        # the move was established.
        _record_outcome(hb, action or "REST", "rest", False, why)
        return
    log(f"tick {hb['total_ticks']}  {action}  -> running {' '.join(args)}")
    pulse.emit("life", "tick", f"#{hb['total_ticks']} {action}")
    # SNAPSHOT BEFORE. The predicate is declared in POST and observed on both sides, so the verdict
    # is re-derivable rather than asserted. `run_script` returns `r.returncode == 0`, which is the
    # third of the three lies: exit 0 was recorded 25 times while the work did not happen.
    spec = _post_for(action)
    before = None
    if spec:
        try:
            before = spec[1]()
        except Exception:
            spec = None                       # cannot observe it -> refuse to claim it
    ok, tail = run_script(args, tmo)
    pulse.emit("life", "tick-done", f"#{hb['total_ticks']} {action} {'ok' if ok else 'FAIL'}", ok=ok)
    if action.startswith("AWAKE"):
        if ok:
            hb["last_brief_date"] = today()
            hb["brief_fails"] = 0
            speak_brief(hb)                        # THE ENTITY SPEAKS WITHOUT BEING LAUNCHED
        else:
            hb["brief_fails"] = int(hb.get("brief_fails", 0)) + 1
            _notice_and_propose(hb, tail)
    # SNAPSHOT AFTER, and grade on the declared predicate rather than the exit code. An action with
    # no declared post-condition records UNATTRIBUTABLE - honest, and it is the work list.
    verify = None
    if spec:
        try:
            after = spec[1]()
            verify = dict(pred=spec[0], result=bool(after is not None and before is not None
                                                    and after > before),
                          detail=f"{before} -> {after}")
        except Exception:
            verify = None
    if verify is not None and ok and not verify["result"]:
        # THE EXIT CODE AND THE WORLD DISAGREE, which is the case worth catching. The process said
        # it succeeded and the thing it was for did not happen.
        log(f"  POST-CONDITION FAILED though the process exited 0: {verify['pred']} ({verify['detail']})")
        pulse.emit("life", "post-failed", f"#{hb['total_ticks']} {action} {verify['detail']}", ok=False)
        ok = False
    _record_outcome(hb, action, "script", ok, tail, verify=verify, args=list(args or []))
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
