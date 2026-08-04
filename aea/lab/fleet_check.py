"""fleet_check.py - R5's FIRST RUN: the record makes a claim about the world, so go ask the world.

    python -m aea.lab.fleet_check              propose, probe, settle, write the run
    python -m aea.lab.fleet_check --dry        show the claims it would make, probe nothing

THE CLAIM CLASS, and why it is this one. R5 needs a hypothesis the entity already HOLDS - not one a
human hands it, or the rung certifies the human (D51: a label is not a measurement). Measured
2026-08-04 across 398 things the entity actually asserted: 60.3% were about itself, 38.4% about
Luis, and **1.0% about the AI field** - which is the only subject the five dispatch topics can fetch
evidence about. Claims and evidence about different worlds, so R5's gate was very nearly unreachable
by construction, the same defect class as R1's original gate.

`energy_usage.json` closes that gap and nothing else in the record does. It carries rows the SYSTEM
wrote about the world - "this rod has failed 97 consecutive times" - which are (a) claims the entity
holds as fact and acts on by refusing to use the rod, (b) about something outside itself, and (c)
decidable in seconds by asking. That is the whole of R5 in one file: a belief, held, checkable, and
never checked.

PRE-REGISTERED, WRITTEN BEFORE THE FIRST RUN so it cannot be fitted afterwards. Ten rods carry a
cooldown right now and the split is the test:

    THREE FAILED TODAY   meta/llama-3.2-1b-instruct (109), groq/openai/gpt-oss-20b (97),
                         groq/groq/compound-mini (95)
                         PREDICTED: DIED. They carry the signature of the malformed
                         `response_format` fixed hours ago (D53) and have not been re-probed since.
    SEVEN FAILED IN JULY genuinely uncertain, no mechanism proposed
                         PREDICTED: some CORROBORATE.

    UNINFORMATIVE IF ALL TEN DIE. Then the probe is measuring our own fix rather than the record's
    claim, and this file says so instead of counting ten deaths as ten discoveries.

WHY A PROBE'S BYTES MAY BE CITED. `artefacts.CITABLE_SRC` requires that the address not be chosen by
the thing under test. Here the rod id is read verbatim out of the row making the claim - the claim
picks the address - so the source could have refuted it, which is the point of the allow-list.

WHAT THIS CANNOT SHOW, said before the result:
  - that a rod which answers ONE probe is healthy. One 200 refutes "cannot answer"; it establishes
    nothing about the next hundred calls, and the claim is written narrowly for that reason
  - that a rod which fails is genuinely gone. A second failure CORROBORATES and does not confirm -
    the word is refused in `hypotheses.py` and the reason is affirming the consequent
  - whether the cooldown was ever CORRECT policy. That is a design question; this measures a fact
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
import uuid

from aea.energy import energy
from aea.kernel import artefacts, grid, hypotheses

# One short, cheap question. A rod that answers this at all refutes "cannot answer"; a long prompt
# would confound "the rod is gone" with "the rod choked on the ask", which is D53's mistake wearing
# a different hat.
PROBE = [{"role": "user", "content": "Reply with the single word: ok"}]
TIMEOUT = 60


SCHEMA_PROBE = [{"role": "user", "content":
                 "Return a person as JSON with keys name and skills (skills is a list of strings)."}]
SCHEMA_SHAPE = {"type": "object",
                "properties": {"name": {"type": "string"},
                               "skills": {"type": "array", "items": {"type": "string"}}},
                "required": ["name", "skills"]}


def doubted_capabilities(census: dict = None, limit: int = 12) -> list:
    """Rods the CENSUS says cannot produce structured output - a second claim class, and a richer one.

    WHY THIS CLASS EXISTS. The fleet-belief class is spent: every rod still cooled corroborated, so
    running it again yields runs with no deaths, and R5's gate counts runs in which something DIED.
    A gate cannot be met by repeating a question whose answer has stopped changing.

    WHY THESE CLAIMS ARE LIKELY FALSE, and this is a prediction with a mechanism rather than a hope.
    `capability_census.json` was generated 2026-07-31 and its battery includes a `schema` probe. The
    malformed `response_format` (D53) was live on EVERY schema call ever made until 2026-08-04, so
    that probe sent a payload the plants reject and recorded the rejection as the ROD's failure. The
    census now asserts that 72 of 95 rods cannot do structured output. Two signatures give it away:

        ERR400          the plant refused the request. That is our payload, not the rod
        outcome ok      the rod ANSWERED and the checker rejected the answer - code fences, prose
        but passed=false  around the JSON, exactly what a rod does when nothing constrains its format

    ERR404 is excluded on purpose. A model the catalogue does not serve really cannot do this, and
    including those would pad the run with claims chosen because they were safe to leave standing.
    A class assembled to produce deaths is not a test."""
    c = census if census is not None else grid.load_json(
        os.path.join(grid.STATE, "capability_census.json"), {})
    out = []
    for n in (c.get("models") or []):
        p = (n.get("probes") or {}).get("schema") or {}
        if p.get("passed"):
            continue
        outcome = str(p.get("outcome") or "")
        if outcome in ("ERR404", "ERR500"):
            continue                      # genuinely unserved; not a claim this class may touch
        why = ("the plant refused the request (%s) - the signature of the malformed response_format"
               % outcome) if outcome.startswith("ERR4") else (
              "the rod answered (%s) and the checker rejected its FORMAT" % outcome)
        out.append(dict(key="%s/%s" % (n.get("plant"), n.get("model")),
                        plant=n.get("plant"), model=n.get("model"),
                        outcome=outcome, sample=str(p.get("sample") or "")[:80],
                        generated=c.get("generated"), why=why))
    return out[:limit]


def run_capability_claim(cand: dict, run: str = "") -> dict:
    """One census claim, stated then tested with a WELL-FORMED schema.

    `run` IS THE INVESTIGATION, NOT THE CLAIM, and the caller must name it. This defaulted to
    `"capability_%d" % int(time.time())`, and twelve concurrent probes launched inside the same
    second collided onto one id. The collision was a bug and its RESULT was correct: one question -
    "can these rods do structured output after all?" - asked of twelve rods is ONE run, and R5's
    gate counts runs in which something died.

    Fixing it toward uniqueness would have turned 2 runs into 7 and met a five-run gate by widening
    a batch, which is the "lower the bar to what fits in an evening" defect R4b's own note names.
    A gate must not be satisfiable by changing how you count. So the id is now explicit: whoever
    starts an investigation names it, and a shared name is a deliberate statement that these claims
    answer one question."""
    run = run or ("capability_%s" % uuid.uuid4().hex[:8])
    h = hypotheses.propose(
        claim="rod %s cannot produce structured output" % cand["key"],
        from_record=("capability_census.json[%s] generated %s: schema probe passed=false, "
                     "outcome=%s, sample=%r"
                     % (cand["key"], cand["generated"], cand["outcome"], cand["sample"][:50])),
        killer=("send it a json schema now that response_format is well-formed; a reply that "
                "parses as JSON and carries both required keys refutes it"),
        holds_fixed=["the plant is reachable", "rate limits are not saturated at probe time",
                     "the census's own checker was the only thing that changed"],
        run=run)
    t0 = time.time()
    try:
        r = grid.call_openai(cand["plant"], cand["model"], SCHEMA_PROBE,
                             max_tokens=300, schema=SCHEMA_SHAPE, timeout=90)
    except Exception as e:
        r = dict(ok=False, status=None, text="", error="%s: %s" % (type(e).__name__, str(e)[:110]))
    text = (r.get("text") or "").strip()
    parsed, keys = None, []
    if text:
        try:
            parsed = json.loads(text)
            keys = sorted(parsed) if isinstance(parsed, dict) else []
        except Exception:
            parsed = None
    refuted = bool(parsed is not None and "name" in keys and "skills" in keys)
    body = json.dumps(dict(rod=cand["key"], status=r.get("status"), ok=bool(r.get("ok")),
                           text=text[:600], keys=keys, parsed=parsed is not None,
                           error=str(r.get("error") or "")[:250],
                           latency=round(time.time() - t0, 2)), ensure_ascii=False).encode("utf-8")
    art = artefacts.store(body, "probe://schema/%s" % cand["key"], run=run,
                          status=r.get("status") or (200 if refuted else 0),
                          src="probe", note="R5 capability probe")
    cite = art.get("id") or art.get("sha256")
    among = [x for x in artefacts.rows() if x.get("run") == run]
    if refuted:
        s = hypotheses.settle(
            h["hid"], "DIED", [cite],
            consequence=("re-census %s for the schema capability; the 2026-07-31 row recorded a "
                         "malformed request as this rod's own limit, and anything that routed away "
                         "from it for structured work routed on a false premise" % cand["key"]),
            why="answered a well-formed schema with valid JSON carrying %s" % keys,
            among_artefacts=among)
    else:
        s = hypotheses.settle(
            h["hid"], "CORROBORATED", [cite],
            why="asked with a well-formed schema and still did not return the required shape "
                "(status %s, parsed=%s, keys=%s)" % (r.get("status"), parsed is not None, keys),
            among_artefacts=among)
    hypotheses.write_run(run, "can %s produce structured output after all?" % cand["key"], [s])
    return dict(hid=s["hid"], rod=cand["key"], status=s["status"], keys=keys,
                status_code=r.get("status"))


def believed_dead(usage: dict = None) -> list:
    """Every rod the record currently asserts cannot answer, with the row that asserts it."""
    u = usage if usage is not None else grid.load_json(energy.USAGE, {})
    out = []
    for k, v in (u or {}).items():
        if not isinstance(v, dict) or not v.get("cooled_at"):
            continue
        plant, model = (k.split("/", 1) + [""])[:2]
        out.append(dict(key=k, plant=plant, model=model,
                        consec_fail=v.get("consec_fail"), calls=v.get("calls"), ok=v.get("ok"),
                        last=v.get("last"), cooled_at=v.get("cooled_at")))
    out.sort(key=lambda r: -(r.get("cooled_at") or 0))
    return out


# THE NUMERIC STOPPING RULE the ladder's power text asks for, and the first run did not have.
#
# One probe is DECISIVE for a death - a single 200 carrying text refutes "cannot answer" outright,
# and no number of further probes makes that refutation truer. It is NOT decisive the other way:
# a CORROBORATED resting on n=1 says only "it failed once", which is exactly the strength of
# evidence that produced the 111-consecutive-failure rows this rung was built to doubt. So the rule
# is asymmetric on purpose, because the logic is asymmetric: stop at the first success, and require
# PROBES consecutive failures before letting the record's claim stand.
PROBES = 2


def run_one(rod: dict, run: str = "") -> dict:
    """One claim, stated then tested, with the stopping rule applied. What `hands.check_a_belief`
    calls, and the smallest complete R5 path in the repo."""
    run = run or "belief_%d" % int(time.time())
    h = hypotheses.propose(
        claim="rod %s cannot answer" % rod["key"],
        from_record=("energy_usage.json[%s]: consec_fail=%s, ok=%s of %s calls, cooled, last %s"
                     % (rod["key"], rod["consec_fail"], rod["ok"], rod["calls"], rod["last"])),
        killer="ask the rod up to %d times; any 200 carrying non-empty text refutes it" % PROBES,
        holds_fixed=["the account's rate limits are not saturated at probe time",
                     "the plant is reachable from this machine"],
        run=run)
    results, lock = {}, threading.Lock()
    attempts = []
    for i in range(PROBES):
        _probe(rod, run, results, lock, tag="#%d" % (i + 1))
        res = results.get(rod["key"]) or {}
        attempts.append(dict(n=i + 1, answered=res.get("answered"), status=res.get("status"),
                             cite=res.get("cite")))
        if res.get("answered"):
            break                      # a death is decided by ONE success; stop, do not pad
    among = [r for r in artefacts.rows() if r.get("run") == run]
    last = results.get(rod["key"]) or {}
    cites = [a["cite"] for a in attempts if a.get("cite")]
    if not cites:
        return dict(hid=h["hid"], status="UNSETTLED", why="no artefact was stored")
    if last.get("answered"):
        s = hypotheses.settle(
            h["hid"], "DIED", cites,
            consequence=("clear the cooldown for %s and return it to the ladder; the record's "
                         "consec_fail=%s measured something other than this rod's ability to answer"
                         % (rod["key"], rod["consec_fail"])),
            why="probed live %d time(s) and it answered %r" % (len(attempts), last.get("text", "")[:40]),
            among_artefacts=among)
    else:
        s = hypotheses.settle(
            h["hid"], "CORROBORATED", cites,
            why="probed live %d consecutive time(s), none answered (last status %s)"
                % (len(attempts), last.get("status")),
            among_artefacts=among)
    hypotheses.write_run(run, "does the record's claim about %s hold?" % rod["key"], [s])
    return dict(hid=s["hid"], rod=rod["key"], status=s["status"], attempts=len(attempts),
                consequence=s.get("consequence", ""), why=s.get("why", ""))


def _probe(rod: dict, run: str, results: dict, lock: threading.Lock, tag: str = "") -> None:
    """Ask one rod. Store the raw answer as an artefact whichever way it goes.

    A FAILURE IS STORED TOO, and that is deliberate. If only successes became artefacts, a
    CORROBORATED verdict would have nothing to cite and `settle` would refuse it - so the store
    would quietly only ever be able to record deaths, which is a store that can only agree."""
    t0 = time.time()
    try:
        r = grid.call_openai(rod["plant"], rod["model"], PROBE, max_tokens=32, timeout=TIMEOUT)
    except Exception as e:
        r = dict(ok=False, status=None, text="", error="%s: %s" % (type(e).__name__, str(e)[:120]))
    text = (r.get("text") or "").strip()
    answered = bool(r.get("ok")) and bool(text)
    # the bytes we actually received, recorded as received
    body = json.dumps(dict(rod=rod["key"], status=r.get("status"), ok=bool(r.get("ok")),
                           text=text[:400], error=str(r.get("error") or "")[:300],
                           latency=round(time.time() - t0, 2)),
                      ensure_ascii=False).encode("utf-8")
    art = artefacts.store(body, "probe://%s%s" % (rod["key"], tag), run=run,
                          status=r.get("status") or (200 if answered else 0),
                          src="probe", note="R5 fleet probe %s" % tag)
    with lock:
        results[rod["key"]] = dict(answered=answered, status=r.get("status"), text=text[:120],
                                   error=str(r.get("error") or "")[:160],
                                   cite=art.get("id") or art.get("sha256"),
                                   latency=round(time.time() - t0, 2))


def run(dry: bool = False) -> dict:
    rods = believed_dead()
    run_id = "fleet_%d" % int(time.time())
    print("=" * 100)
    print("R5 RUN %s - the record says %d rods cannot answer. Ask them." % (run_id, len(rods)))
    print("=" * 100)
    if not rods:
        print("  the record asserts nothing to test - no rod is cooled")
        return dict(run=run_id, n=0, why="no claim in the record")

    # 1. PROPOSE - every claim on disk, fsynced, BEFORE a single probe runs.
    #
    # `--dry` MUST NOT WRITE. The first version proposed and then stopped, which left ten permanent
    # OPEN claims in the store for a preview that tested nothing - a store where "proposed" does not
    # imply "was going to be probed" is a store whose open count means nothing. A dry run prints the
    # claims it WOULD make; only a real run commits them.
    if dry:
        for rod in rods:
            print("  WOULD PROPOSE  %-46s  consec_fail=%s ok=%s/%s  last %s"
                  % (rod["key"][-46:], rod["consec_fail"], rod["ok"], rod["calls"], rod["last"]))
        print("\n  %d claims NOT written - --dry commits nothing." % len(rods))
        return dict(run=run_id, n=len(rods), dry=True)

    claims = []
    for rod in rods:
        h = hypotheses.propose(
            claim="rod %s cannot answer" % rod["key"],
            from_record=("energy_usage.json[%s]: consec_fail=%s, ok=%s of %s calls, cooled, "
                         "last %s" % (rod["key"], rod["consec_fail"], rod["ok"], rod["calls"],
                                      rod["last"])),
            killer="ask the rod once; any 200 carrying non-empty text refutes it",
            holds_fixed=["the account's rate limits are not saturated at probe time",
                         "the plant is reachable from this machine"],
            run=run_id)
        claims.append((rod, h))
        print("  PROPOSED  %-46s  %s" % (rod["key"][-46:], h["hid"]))
    print("\n  %d claims written and fsynced. Nothing has been asked yet." % len(claims))

    # 2. PROBE - concurrent, one thread per rod
    print("\n  probing %d rods concurrently..." % len(claims))
    results, lock, threads = {}, threading.Lock(), []
    for rod, _h in claims:
        t = threading.Thread(target=_probe, args=(rod, run_id, results, lock))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # 3. SETTLE - against the artefacts just stored, run-scoped
    among = [r for r in artefacts.rows() if r.get("run") == run_id]
    settled = []
    for rod, h in claims:
        res = results.get(rod["key"]) or {}
        if not res.get("cite"):
            print("  UNSETTLED %-46s  no artefact stored" % rod["key"][-46:])
            continue
        if res["answered"]:
            s = hypotheses.settle(
                h["hid"], "DIED", [res["cite"]],
                consequence=("clear the cooldown for %s and return it to the ladder; the record's "
                             "consec_fail=%s measured something other than this rod's ability to "
                             "answer" % (rod["key"], rod["consec_fail"])),
                why="probed live and it answered %r in %ss" % (res["text"][:40], res["latency"]),
                among_artefacts=among)
        else:
            s = hypotheses.settle(
                h["hid"], "CORROBORATED", [res["cite"]],
                why="probed live and it did not answer (status %s) %s"
                    % (res.get("status"), res.get("error", "")[:80]),
                among_artefacts=among)
        settled.append(s)
        print("  %-12s %-46s  %s" % (s["status"], rod["key"][-46:],
                                     (res["text"][:40] if res["answered"] else
                                      "status %s" % res.get("status"))))

    # 4. THE RUN OBJECT
    died = [s for s in settled if s["status"] == "DIED"]
    corr = [s for s in settled if s["status"] == "CORROBORATED"]
    note = ""
    if settled and len(died) == len(settled):
        note = ("UNINFORMATIVE AS PRE-REGISTERED: every claim died, so this run measured the "
                "response_format fix (D53) rather than the record's claim. Counted, not celebrated.")
    p = hypotheses.write_run(run_id, "does the record's claim that these rods cannot answer hold?",
                             settled, note=note)

    print("\n" + "=" * 100)
    print("  %d claims -> %d DIED, %d CORROBORATED, %d unsettled"
          % (len(claims), len(died), len(corr), len(claims) - len(settled)))
    print("  PRE-REGISTERED: the three that failed today DIE; some July rods CORROBORATE.")
    today = [s for s in settled if "2026-08-04" in str(s.get("from_record") or "")]
    print("  today's rods: %d of %d died" % (sum(1 for s in today if s["status"] == "DIED"),
                                             len(today)))
    if note:
        print("  " + note)
    print("  run object: %s" % p)
    print("=" * 100)
    return dict(run=run_id, n=len(claims), died=len(died), corroborated=len(corr), path=p)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    run(dry=a.dry)
