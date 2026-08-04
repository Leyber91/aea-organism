"""console.py - EVERYTHING THAT IS GOING ON, IN ONE PLACE, AND ONLY WHAT IS TRUE RIGHT NOW.

    python -m aea.tooling.console            the whole picture, once
    python -m aea.tooling.console --watch    the same, refreshing
    python -m aea.tooling.console --json     the same, as data

WHY THIS EXISTS AND WHY IT IS NOT ANOTHER DASHBOARD. `/state` already consolidates identity, life,
memory, energy and trust; `pulse` already streams every organ's signal into `events.jsonl`. Neither
answers the question a person actually has when they sit down: **is it running, and what is it doing
right now.**

THE HONESTY DEFECT THIS FIXES, found live 2026-08-03. `controlroom`'s status printed
`alive since 2026-07-10 20:08:57 UTC | wakes 270 ticks 453` with NO PROCESS RUNNING. It reads
`heartbeat.json` and reports it as aliveness, so it says the same thing with the machine off. That
is a number that is not system truth at the moment it is displayed, which is the one law this
project does not bend. So every line below is tagged with WHERE IT CAME FROM:

    LIVE    a process was checked, this second
    FILE    read off disk - true when it was written, and the age is shown
    DERIVED computed from the two

AND THE MIND HAS NO READER, which is the other half. `live.log` is rendered in several views;
`wake.log` - written by the DELIBERATING loop, the thing every rung above R0 is about - is rendered
nowhere. A store with a writer and no reader is the R1 defect, and it was reintroduced this morning
by the same author who wrote that sentence down. This is its reader.

ONE SNAPSHOT, TWO RENDERERS. `snapshot()` is the only place that decides what is true; the terminal
view and the web view both draw it. A second copy of this logic in a template is how two instruments
start disagreeing about the same machine.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

from aea.kernel import grid


# THESE TWO CARRY THEIR REASON, and the first version did not. Caught by the defect ratchet the
# moment this file shipped: both were `except: return <empty>`, so an unreadable log rendered as
# "(nothing yet)" - which reads as THE MIND HAS NEVER WRITTEN rather than I COULD NOT READ IT.
#
# That is D19/D21 - a null indistinguishable from a real result - committed inside the console
# written to fix exactly that class of lie. The counter-discipline is `decide.py`'s first law:
# every refusal returns (value, why). It is the discipline that does not travel, and this is the
# proof, since the author had quoted it four hours earlier.

def _age(path: str) -> tuple:
    """(seconds since written, why-not). Absent and unreadable are different facts about a file."""
    if not os.path.exists(path):
        return None, "does not exist"
    try:
        return round(time.time() - os.path.getmtime(path), 1), ""
    except Exception as e:
        return None, "unreadable (%s)" % type(e).__name__


def _tail(path: str, n: int = 8) -> tuple:
    """(last n lines, why-not). An empty file and an unreadable one are not the same event."""
    if not os.path.exists(path):
        return [], "does not exist"
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = [x.rstrip() for x in f.readlines()[-n:]]
        return lines, ("" if lines else "the file is empty")
    except Exception as e:
        return [], "unreadable (%s)" % type(e).__name__


def _running() -> dict:
    """WHICH PROCESSES EXIST, ASKED OF THE OS. Not of a pid file, which is a claim about the past.

    `live_pid.json` held pid 55376 from 2026-07-19 for two weeks after that process died, and every
    reader that trusted it believed the loop was up."""
    out = dict(controlroom=[], live=[], wake=[], asked=True, why="")
    try:
        r = subprocess.run(
            ["wmic", "process", "where", "name='python.exe'", "get", "ProcessId,CommandLine", "/format:csv"],
            capture_output=True, text=True, timeout=20)
        rows = [x for x in (r.stdout or "").splitlines() if "python" in x.lower()]
        if not rows:                                  # wmic is deprecated on newer Windows
            raise RuntimeError("wmic returned nothing")
    except Exception:
        try:
            # THE START TIME COMES WITH IT, and its absence caused a false report.
            #
            # The console showed the mind's pid and `state written Ns ago`, and those two facts LOOK
            # like one. They are not: the state age is when the LAST tick COMMITTED, not how long
            # the tick in flight has been running. On 2026-08-03 a 336s state age was reported as "a
            # wake has been thinking for 336 seconds and is about to overlap the next spawn" - and
            # the tick had in fact taken 123.9s and finished. An event was flagged that never
            # happened, from a number that was true about something else.
            #
            # With concurrency now reachable, "how long has THIS wake been running" is the question
            # that decides whether the next spawn overlaps, and nothing measured it. The OS has the
            # answer; inferring it from a file mtime was the mistake.
            r = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | "
                 "ForEach-Object { \"$($_.ProcessId)|$([int]((Get-Date) - $_.CreationDate)"
                 ".TotalSeconds)|$($_.CommandLine)\" }"],
                capture_output=True, text=True, timeout=30)
            rows = [x for x in (r.stdout or "").splitlines() if x.strip()]
        except Exception as e:
            out["asked"] = False
            out["why"] = "could not enumerate processes (%s) - RUNNING STATE IS UNKNOWN, not false" \
                         % type(e).__name__
            return out
    for line in rows:
        low = line.lower()
        # `pid|age_seconds|commandline` from the powershell path; the wmic CSV path has no age, so
        # it is reported as None rather than as zero - an unknown runtime must not read as "just
        # started", which is the null-that-looks-like-a-result shape this whole file is about.
        parts = line.split("|")
        pid, age = "", None
        if len(parts) >= 3 and parts[0].strip().isdigit():
            pid = parts[0].strip()
            if parts[1].strip().isdigit():
                age = int(parts[1].strip())
        else:
            for part in line.replace("|", ",").split(","):
                q = part.strip()
                if q.isdigit():
                    pid = q
        entry = "%s (%ss)" % (pid, age) if age is not None else pid
        # THE RAW PID IS KEPT ALONGSIDE THE DISPLAY STRING, and its absence made this file lie.
        #
        # When runtime was added to the display, `live` began holding "77140 (256s)" instead of
        # "77140" - and the staleness check compares the recorded pid against that list. So the
        # console reported `live_pid.json names 77140 and no such process exists` WHILE SHOWING
        # 77140 as the running loop, one line above. A formatting change silently broke a
        # comparison, which is the same shape as every other defect found today.
        out.setdefault("live_pids", [])
        out.setdefault("all_pids", []).append(pid)
        if "aea.loop.live" in low:
            out["live"].append(entry)
            out["live_pids"].append(pid)
        elif "aea.loop.aea" in low:
            out["wake"].append(entry)
            out.setdefault("wake_age_s", []).append(age)
        elif "controlroom" in low:
            out["controlroom"].append(entry)
    return out


def snapshot() -> dict:
    """The whole picture. Every value carries where it came from."""
    S = grid.STATE
    now = time.time()
    live_log = os.path.join(S, "live.log")
    wake_log = os.path.join(S, "wake.log")
    snap = dict(at=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(now)), at_epoch=now)

    # ---- LIVE: what is actually running -------------------------------------------------------
    proc = _running()
    pidfile = grid.load_json(os.path.join(S, "live_pid.json"), {}) or {}
    snap["processes"] = dict(
        source="LIVE" if proc["asked"] else "UNKNOWN", why=proc["why"],
        controlroom=proc["controlroom"], live=proc["live"], wake=proc["wake"],
        recorded_live_pid=pidfile.get("pid"),
        pidfile_is_stale=bool(pidfile.get("pid")
                              and str(pidfile["pid"]) not in (proc.get("live_pids") or [])
                              and proc["asked"]))

    # ---- the two loops ------------------------------------------------------------------------
    hb = grid.load_json(os.path.join(S, "heartbeat.json"), {}) or {}
    try:
        mind = json.load(open(os.path.join(S, "aea_state.json"), encoding="utf-8", errors="replace"))
    except Exception:
        mind = {}
    hb_age, hb_why = _age(os.path.join(S, "heartbeat.json"))
    body_log, body_why = _tail(live_log, 10)
    body_log_age, _ = _age(live_log)
    snap["body"] = dict(source="FILE", ticks=hb.get("total_ticks"), wakes=hb.get("boot_count"),
                        alive_since=hb.get("alive_since"),
                        heartbeat_age_s=hb_age, heartbeat_why=hb_why,
                        log=body_log, log_why=body_why, log_age_s=body_log_age)
    ms_age, ms_why = _age(os.path.join(S, "aea_state.json"))
    mind_log, mind_why = _tail(wake_log, 10)
    mind_log_age, _ = _age(wake_log)
    snap["mind"] = dict(source="FILE", tick=mind.get("tick"),
                        memories=len(mind.get("memory") or []),
                        state_age_s=ms_age, state_why=ms_why,
                        log=mind_log, log_why=mind_why, log_age_s=mind_log_age)

    # ---- the clamps ---------------------------------------------------------------------------
    try:
        from aea.kernel import wake as _w
        ws = _w.state(hb=hb)
        snap["wake_budget"] = dict(source="DERIVED", spent=ws["spent_24h"], per_day=ws["per_day"],
                                   permitted=ws["permitted_now"], why=ws["refused_because"],
                                   seconds_since_last=ws["seconds_since_last"],
                                   cadence_s=ws["decision"]["seconds"], cadence_by=ws["decision"]["by"],
                                   stop_present=ws["stop_present"])
    except Exception as e:
        snap["wake_budget"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))
    try:
        from aea.kernel import egress as _e
        es = _e.state()
        snap["egress"] = dict(source="DERIVED", spent=es["spent_24h"],
                              per_day=es["budget"]["per_day_ceiling"],
                              permitted=es["permitted_now"], why=es["refused_because"],
                              bits_per_day=es["budget"]["bits_per_day"],
                              seconds_since_last=es["seconds_since_last"])
    except Exception as e:
        snap["egress"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))

    # ---- fuel: can it think at all right now --------------------------------------------------
    try:
        from aea.kernel import wake as _w2
        f = _w2.fuel()
        snap["fuel"] = dict(source="LIVE", ok=f["ok"], blind=f.get("blind"),
                            rod=("%s / %s" % f["rod"]) if f["rod"] else None,
                            why=f["why"], checked=f["checked"])
    except Exception as e:
        snap["fuel"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))

    # ---- R5: what it claimed before it looked, and how those claims ended ----------------------
    # `hypotheses.state` was reported UNWIRED by `ladder.verify_funcs` - written, correct, and
    # reachable from nothing. The honest fix for a state function nobody reads is a panel, not a
    # deletion: R5's whole content is claims that were allowed to be wrong, and a rung whose
    # results are invisible cannot be checked by the person the honesty law is for.
    try:
        from aea.kernel import hypotheses as _hy
        hs = _hy.state()
        snap["r5"] = dict(source="FILE", **hs)
    except Exception as e:
        snap["r5"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))

    # ---- can the mind still FORM a thought, not just have one ---------------------------------
    # THE PANEL THAT WAS MISSING. Phase 2 (the formatter) failed on 98% of the last 40 ticks and
    # every other panel read green, because `move_from` reads the core's own text and the four
    # output fields survived. The cost was invisible and total: the failure string went into
    # `note_to_self`, `tick` copies that into memory, and 430 of 739 memory entries became
    # "(structuring failed: HTTP Error 429)". Found 2026-08-04 only by reading the rod's own
    # reasoning trace, which until that day was discarded at the socket. Measure the pipe, not
    # only the water.
    try:
        import re as _re
        _wl = os.path.join(grid.STATE, "wake.log")
        with open(_wl, encoding="utf-8", errors="replace") as _f:
            _t = _f.read()[-400_000:]
        _blocks = _re.split(r"(?=^=== THE AEA WAKES)", _t, flags=_re.M)[1:]
        _recent = _blocks[-40:]
        _bad = sum(1 for b in _recent if _re.search(r"structur\w+ failed|structure_failed", b, _re.I))
        _mem = grid.load_json(os.path.join(grid.STATE, "aea_state.json"), {}).get("memory") or []
        _poison = sum(1 for m in _mem[-40:] if "structuring failed" in str(m))
        snap["structure"] = dict(source="DERIVED", window=len(_recent), failed=_bad,
                                 rate=(round(_bad / len(_recent), 3) if _recent else None),
                                 memory_poisoned_last40=_poison, memory_total=len(_mem))
    except Exception as e:
        snap["structure"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))

    # ---- what it is stuck on, and what it proposed --------------------------------------------
    try:
        from aea.kernel import impasse
        rows = impasse.scan()
        snap["impasse"] = dict(source="DERIVED",
                               stuck=[dict(cap=r["capability"], why=r["why"],
                                           fails=r["consecutive_failures"], level=r["level"])
                                      for r in rows if r.get("stuck")],
                               total=len(rows),
                               working=len([r for r in rows if r.get("verdict") == "working"]))
    except Exception as e:
        snap["impasse"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))

    # ---- the ladder ---------------------------------------------------------------------------
    #
    # READ FROM THE FILE, NOT RECOMPUTED, AND THE AGE IS SHOWN BECAUSE OF IT. `ladder.build()` takes
    # 15.1 seconds measured - it walks the hands ledger, 338 outcomes, the decision log and the
    # dispatch certificate - so recomputing it on a 15-second poll would spend the machine's time
    # re-deriving numbers that move once an hour. The cost of that choice is that this section is a
    # SNAPSHOT, and a snapshot presented as live is the exact lie this console exists to stop. So
    # the age travels with it and `stale` is computed rather than left to the reader's judgement.
    #
    # AND THE FIELD IS `measured`, NOT `evidence`. The first version of this file read
    # `r.get("evidence")`, which does not exist in `ladder.json` - every rung rendered blank and the
    # ladder LOOKED empty and outdated when the data was there and fresh. A fix lands on the object
    # you NAME, not the one you meant; the name was invented here rather than read off the schema.
    lad_path = os.path.join(S, "ladder.json")
    lad = grid.load_json(lad_path, {}) or {}
    rungs = lad.get("rungs") or lad.get("ladder") or []
    lad_age, lad_why = _age(lad_path)

    def _one_line(m):
        """The measured dict as one honest line, or a dash. Never a guess."""
        if not isinstance(m, dict):
            return ""
        keep = [(k, v) for k, v in m.items()
                if k not in ("met",) and isinstance(v, (int, float, bool, str)) and v not in (None, "")]
        return "  ".join("%s=%s" % (k, v) for k, v in keep[:5])

    snap["ladder"] = dict(
        source="FILE", age_s=lad_age, age_why=lad_why,
        generated=lad.get("generated"),
        stale=bool(lad_age is not None and lad_age > 3600),
        refresh_with="python -m aea.tooling.ladder   (15s - it re-walks every record)",
        rungs=[dict(id=r.get("id"), title=r.get("title"), status=r.get("status"),
                    measured=_one_line(r.get("measured"))[:120])
               for r in rungs if isinstance(r, dict)])

    # ---- R5's store ---------------------------------------------------------------------------
    try:
        from aea.kernel import artefacts
        st = artefacts.stats()
        snap["artefacts"] = dict(source="FILE", **st)
    except Exception as e:
        snap["artefacts"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))
    # R5's CERTIFICATE, RUN HERE SO IT IS NOT A DOCUMENT NOBODY EXECUTES. Its controls run on every
    # call in a temp store, so this also re-proves the bound each time the console is opened - which
    # is the difference between a certificate and a claim somebody made once.
    try:
        from aea.lab import research_cert
        rc = research_cert.certify()
        snap["research_cert"] = dict(source="DERIVED", verdict=rc["verdict"],
                                     controls_all_fire=rc["controls_all_fire"],
                                     controls=len(rc["controls"]),
                                     failing=[c["check"] for c in rc["controls"] if not c["ok"]],
                                     blocked_on=rc["blocked_on"])
    except Exception as e:
        snap["research_cert"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))

    # ---- the derived signals nothing else computes ---------------------------------------------
    #
    # WIRED HERE RATHER THAN LEFT STANDALONE, and the orphan ratchet is why. `sensors.py` shipped
    # reachable from nothing and selfcheck immediately read 135 orphaned against a 134 line - one
    # more module in a tree where 134 of 177 are already dead, which is the exact complaint that
    # started this. A tool nobody calls is not a tool, and raising the ratchet to admit it would
    # have been the dishonest fix.
    try:
        from aea.tooling import sensors
        snap["sensors"] = dict(source="DERIVED", **sensors.all_signals())
    except Exception as e:
        snap["sensors"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))

    # ---- one line per PART, measured by its action ----------------------------------------------
    #
    # WIRED, because the orphan ratchet caught this file shipping reachable from nothing - the
    # second time in one session. A tool nobody calls is not a tool, and 134 of 177 modules here
    # are already dead. `parts.survey()` reads only production stores, so it costs a few file
    # reads and answers the question that matters: which parts have DEMONSTRATED their action.
    try:
        from aea.tooling import parts as _parts
        ps = _parts.survey()
        snap["parts"] = dict(
            source="DERIVED",
            demonstrated=len([p for p in ps if p["verdict"] == "DEMONSTRATED"]),
            never=[p["part"] for p in ps if p["verdict"] == "NEVER"],
            unmeasured=[p["part"] for p in ps if p["verdict"] == "UNMEASURED"],
            total=len(ps))
    except Exception as e:
        snap["parts"] = dict(source="ERROR", why="%s: %s" % (type(e).__name__, str(e)[:80]))

    # ---- trust ---------------------------------------------------------------------------------
    tl = grid.load_json(os.path.join(S, "trust_ledger.json"), {}) or {}
    snap["trust"] = dict(source="FILE", caps=[
        dict(cap=k, level=(v or {}).get("level"), runs=(v or {}).get("runs"),
             fails=(v or {}).get("fails"))
        for k, v in sorted(tl.items()) if isinstance(v, dict)])
    return snap


# =================================================================================================
# THE TERMINAL RENDERER
# =================================================================================================

def _tag(src: str) -> str:
    return {"LIVE": "[live]", "FILE": "[file]", "DERIVED": "[calc]",
            "UNKNOWN": "[????]", "ERROR": "[ERR ]"}.get(src, "[    ]")


def render_text(s: dict = None) -> str:
    s = s or snapshot()
    L = []
    w = L.append
    w("=" * 96)
    w("THE ENTITY - everything going on, %s" % s["at"])
    w("=" * 96)

    p = s["processes"]
    if not p.get("controlroom") and not p.get("live") and not p.get("wake"):
        w("  %s NOTHING IS RUNNING%s" % (_tag(p["source"]), ("  - " + p["why"]) if p.get("why") else ""))
    else:
        w("  %s controlroom %-14s life loop %-14s mind %s" % (
            _tag(p["source"]), ",".join(p["controlroom"]) or "-",
            ",".join(p["live"]) or "NOT RUNNING", ",".join(p["wake"]) or "idle"))
    if p.get("pidfile_is_stale"):
        w("       WARNING live_pid.json names %s and no such process exists - the file is stale"
          % p.get("recorded_live_pid"))

    b, m = s["body"], s["mind"]
    w("")
    w("  %s BODY  tick %-6s wakes %-5s heartbeat written %ss ago" % (
        _tag(b["source"]), b["ticks"], b["wakes"], b["heartbeat_age_s"]))
    w("  %s MIND  tick %-6s memories %-5s state written %ss ago" % (
        _tag(m["source"]), m["tick"], m["memories"], m["state_age_s"]))

    wb, eg, fu = s["wake_budget"], s["egress"], s["fuel"]
    w("")
    if wb.get("source") != "ERROR":
        w("  %s WAKE   %s of %s today   next in %.0fs by %s   %s%s" % (
            _tag(wb["source"]), wb["spent"], wb["per_day"], wb["cadence_s"], wb["cadence_by"],
            "PERMITTED" if wb["permitted"] else "REFUSED",
            "" if wb["permitted"] else " (%s)" % str(wb["why"])[:60]))
        if wb.get("stop_present"):
            w("       state/STOP EXISTS - thinking and reaching are both halted")
    if eg.get("source") != "ERROR":
        w("  %s EGRESS %s of %s today   %.2f bits/day   %s%s" % (
            _tag(eg["source"]), eg["spent"], eg["per_day"], eg["bits_per_day"],
            "PERMITTED" if eg["permitted"] else "REFUSED",
            "" if eg["permitted"] else " (%s)" % str(eg["why"])[:60]))
    if fu.get("source") != "ERROR":
        w("  %s FUEL   %s" % (_tag(fu["source"]),
                              fu["rod"] if fu["ok"] else "NONE - " + str(fu["why"])[:70]))
    r5 = s.get("r5") or {}
    if r5.get("source") not in (None, "ERROR") and r5.get("total"):
        w("  %s CLAIMS %d stated before looking   %s   deaths naming a consequence %d of %d" % (
            _tag(r5["source"]), r5["total"],
            "  ".join("%s %d" % (k, v) for k, v in sorted((r5.get("by_status") or {}).items())),
            r5.get("deaths_with_consequence", 0), r5.get("died", 0)))
    st = s.get("structure") or {}
    if st.get("source") not in (None, "ERROR"):
        w("  %s FORMING %d of last %d ticks FAILED to structure (%.0f%%)   memory poisoned %d of last 40%s" % (
            _tag(st["source"]), st["failed"], st["window"], 100.0 * (st.get("rate") or 0),
            st["memory_poisoned_last40"],
            "   HEALTHY" if not st["failed"] else "   THE MIND CANNOT FORM ITS THOUGHT"))

    sen = s.get("sensors") or {}
    if sen.get("source") != "ERROR":
        mr, ex = sen.get("move_runs") or {}, sen.get("outward_experiment") or {}
        w("")
        if mr.get("ok"):
            w("  [calc] MOVES  %s x%d in a row  (longest ever %d, %d distinct in %d)%s"
              % (mr["current_move"], mr["streak"], mr["longest_ever"],
                 mr["distinct_in_window"], mr["window"],
                 "   REPEATING" if mr.get("repeating") else ""))
        if ex.get("ok"):
            w("  [calc] OUTWARD EXPERIMENT  %d decisions, %d outward, %d dispatched -> %s"
              % (ex["decisions"], ex["outward_chosen"], ex["dispatches_that_ran"], ex["verdict"]))
        to = sen.get("tool_outcomes") or {}
        if to.get("ok"):
            bad = [t for t in to["tools"] if t.get("barren")]
            if bad:
                w("  [calc] BARREN  %s" % ", ".join(
                    "%s %d/%d (%s%%)" % (t["tool"], t["barren"], t["ran"], t["barren_rate"])
                    for t in bad[:4]))

    im = s["impasse"]
    if im.get("source") != "ERROR":
        w("")
        w("  %s STUCK  %d of %d capabilities" % (_tag(im["source"]), len(im["stuck"]), im["total"]))
        for r in im["stuck"]:
            w("       %-22s %s" % (r["cap"], r["why"][:66]))

    pt = s.get("parts") or {}
    if pt.get("source") == "DERIVED":
        w("  [calc] PARTS  %d of %d DEMONSTRATED by action%s%s" % (
            pt["demonstrated"], pt["total"],
            ("   NEVER: " + ", ".join(pt["never"])) if pt["never"] else "",
            ("   UNMEASURED: " + ", ".join(pt["unmeasured"])) if pt["unmeasured"] else ""))

    rc = s.get("research_cert") or {}
    if rc.get("source") == "DERIVED":
        w("  %s R5 CERT  %-12s %d/%d controls fire%s" % (
            _tag(rc["source"]), rc["verdict"], rc["controls"] - len(rc["failing"]), rc["controls"],
            ("   FAILING: " + ", ".join(rc["failing"][:2])) if rc["failing"] else ""))
        if rc.get("blocked_on"):
            w("             blocked on: %s" % ", ".join(rc["blocked_on"]))
    a = s["artefacts"]
    if a.get("source") != "ERROR":
        w("  %s R5     %s artefacts, %s distinct, %s bytes%s" % (
            _tag(a["source"]), a.get("reads_with_bytes"), a.get("distinct_artefacts"),
            a.get("total_bytes"), "   (the bound has never run in production)"
            if not a.get("rows") else ""))

    lad = s["ladder"]
    if lad["rungs"]:
        w("")
        age = lad.get("age_s")
        w("  %s THE LADDER   generated %s%s" % (
            _tag(lad["source"]), lad.get("generated") or "?",
            ("   %.0f min ago%s" % (age / 60.0, "  STALE - refresh it" if lad.get("stale") else ""))
            if age is not None else ("   age unknown: %s" % lad.get("age_why"))))
        for r in lad["rungs"]:
            w("       %-5s %-32s %-9s %s" % (r["id"], (r["title"] or "")[:32],
                                             r["status"], (r.get("measured") or "-")[:52]))
        w("       refresh: %s" % lad.get("refresh_with"))

    w("")
    w("  MIND, last lines  (state/wake.log - rendered nowhere else)")
    for line in (m["log"] or ["(no lines: %s)" % (m.get("log_why") or "unknown")]):
        w("       " + line[:104])
    w("")
    w("  BODY, last lines  (state/live.log)")
    for line in (b["log"] or ["(no lines: %s)" % (b.get("log_why") or "unknown")]):
        w("       " + line[:104])
    return "\n".join(L)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if "--json" in sys.argv:
        print(json.dumps(snapshot(), indent=1, default=str))
        sys.exit(0)
    if "--watch" in sys.argv:
        try:
            every = 20
            if "--every" in sys.argv:
                every = max(5, int(sys.argv[sys.argv.index("--every") + 1]))
            while True:
                os.system("cls" if os.name == "nt" else "clear")
                print(render_text())
                print("\n  refreshing every %ds - ctrl-c to stop" % every)
                time.sleep(every)
        except KeyboardInterrupt:
            print("\nstopped")
        sys.exit(0)
    print(render_text())
