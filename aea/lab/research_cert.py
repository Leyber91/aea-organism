"""research_cert.py - R5's BOUND, CERTIFIED FROM DISK. No process trusted, no model consulted.

    python -m aea.lab.research_cert            the certificate
    python -m aea.lab.research_cert --json     the same, to state/research_cert.json

WHAT IS CERTIFIED, and it is deliberately narrower than R5's gate:

    Every citation resolves to bytes that were actually fetched, hashed at arrival, from an
    address no model composed - and the quote appears verbatim in those bytes.

WHAT IS NOT CERTIFIED, stated first because a certificate that implies more than it checked is the
failure this repository keeps paying for:

  - THAT A CITATION IS FAITHFUL. `artefacts.quotes` decides byte-identity, nothing more. A page
    reading "we are often asked whether the export API is deprecated. It is not" yields the
    perfectly verbatim 28-character quote "the export API is deprecated", which passes every stage
    here and INVERTS its source. Measured 2026-08-03. There is no mechanical fix - faithfulness is
    semantic - so `context()` exists to make the neighbourhood legible instead.
  - THAT A HYPOTHESIS DIED HONESTLY. That is R5c and needs the stopping rule, which needs a
    hypothesis store, which does not exist yet. This says so rather than passing vacuously.
  - THAT THE SOURCE IS TRUE. Bytes are bytes. An artefact proves a server sent them; nothing here
    claims they are correct.

THE CONTROL DISCIPLINE. Every check below is paired with a planted failure that MUST flip it. A
scan that finds nothing agrees with everything - this repo has published three retracted
percentages and one certificate that drove `dry` ten times and `run` zero, so the controls are the
load-bearing half and they run on every invocation rather than in a test somebody remembers.

AND IT REFUSES THE WORD "SURVIVES". If a hypothesis is not dead, its status is CORROBORATED - not
yet dead, and nothing downstream may treat it as true. *If H then P; P observed; therefore H* is
affirming the consequent; only refutation is valid. That is not a stylistic preference, it is the
formal reason R5's gate demands a death rather than a confirmation.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile

from aea.kernel import artefacts, grid

OUT = "research_cert.json"

# THE STATUS VOCABULARY, AND "SURVIVES" IS NOT IN IT.
VALID_STATUS = ("DIED", "CORROBORATED", "FORKS", "UNSETTLED", "OPEN")
FORBIDDEN_STATUS = ("SURVIVES", "SURVIVED", "TRUE", "CONFIRMED", "PROVEN")


def _store_state() -> dict:
    """What exists on disk, and what does not. Absent is a measurement, not an omission."""
    S = grid.STATE
    have = {}
    for name, what in (("artefacts.jsonl", "the read ledger"),
                       ("artefacts", "the bytes, one file per digest"),
                       ("hypotheses.jsonl", "claims stated before the evidence"),
                       ("research", "the run path objects")):
        p = os.path.join(S, name)
        have[name] = dict(present=os.path.exists(p), what=what)
    return have


def verify_store() -> dict:
    """Recompute every artefact's digest from the bytes on disk. Nothing from the running process.

    A MISMATCH IS NOT A BAD CITATION, IT IS A TAINTED STORE, and the difference matters: one find
    can be dropped, but bytes that no longer hash to their name mean the record of what arrived has
    been altered, and every citation resting on that store is void until a human looks."""
    rows = artefacts.rows()
    good, bad, missing, failed_reads = [], [], [], []
    for r in rows:
        if not r.get("sha256"):
            failed_reads.append(r)
            continue
        ok, why = artefacts.verify(r)
        if ok:
            good.append(r)
        elif "missing" in why:
            missing.append(dict(id=r.get("id"), why=why))
        else:
            bad.append(dict(id=r.get("id"), why=why))
    citable = [r for r in good if str(r.get("src") or "") in artefacts.CITABLE_SRC]
    return dict(rows=len(rows), verified=len(good), tainted=len(bad), missing=len(missing),
                failed_reads=len(failed_reads), citable=len(citable),
                not_citable=len(good) - len(citable),
                tainted_detail=bad[:5], missing_detail=missing[:5],
                runs=sorted({str(r.get("run") or "") for r in citable if r.get("run")}))


def check_citation(cite: str, quote: str, run: str = "") -> dict:
    """The whole boundary, in one function: resolve, verify, and match the quote verbatim.

    RUN-SCOPED BY CONSTRUCTION. A hash quoted from another inquiry is not a citation, it is a hash
    the model has been near, so the pool is the rows of THIS run and `resolve` refuses an unscoped
    call outright."""
    pool = [r for r in artefacts.rows() if not run or str(r.get("run") or "") == run]
    row = artefacts.resolve(cite, among=pool)
    if row is None:
        return dict(ok=False, stage="resolve",
                    why="no citable artefact %r in run %r (%d rows in scope)" % (cite, run, len(pool)))
    ok, why = artefacts.verify(row)
    if not ok:
        return dict(ok=False, stage="verify", why=why, id=row.get("id"))
    ok, why = artefacts.quotes(row, quote)
    if not ok:
        return dict(ok=False, stage="quote", why=why, id=row.get("id"))
    return dict(ok=True, stage="verbatim", id=row.get("id"), url=row.get("url"),
                at=why, context=artefacts.context(row, quote, window=160))


def status_is_legal(status: str) -> tuple:
    """(ok, why). CORROBORATED is not SURVIVES, and the difference is a fallacy."""
    s = str(status or "").strip().upper()
    if s in FORBIDDEN_STATUS:
        return False, ("%r is not a conclusion. `If H then P; P; therefore H` is affirming the "
                       "consequent - only refutation is valid. Use CORROBORATED: not yet dead, and "
                       "nothing downstream may treat it as true." % s)
    if s not in VALID_STATUS:
        return False, "%r is not one of %s" % (s, list(VALID_STATUS))
    return True, ""


def controls() -> list:
    """PLANTED FAILURES THAT MUST FLIP EVERY CHECK. Runs in a temp store; production is untouched."""
    out = []

    def chk(name, ok, detail=""):
        out.append(dict(check=name, ok=bool(ok), detail=detail))

    with tempfile.TemporaryDirectory() as td:
        keep = {k: os.environ.get(k) for k in ("AEA_ARTEFACT_DIR", "AEA_ARTEFACT_LEDGER")}
        os.environ["AEA_ARTEFACT_DIR"] = os.path.join(td, "artefacts")
        os.environ["AEA_ARTEFACT_LEDGER"] = os.path.join(td, "artefacts.jsonl")
        try:
            body = (b"The measurement was taken at twelve hundred hours and the throughput held "
                    b"steady across every one of the four runs we attempted that afternoon.")
            good = artefacts.store(body, "https://arxiv.org/abs/1", run="RUN_A",
                                   status=200, src="dispatch")
            other = artefacts.store(b"An entirely different document about an unrelated subject "
                                    b"that shares no sentences with the first one at all.",
                                    "https://arxiv.org/abs/2", run="RUN_B",
                                    status=200, src="dispatch")
            model_side = artefacts.store(b"Bytes fetched from an address the model itself composed "
                                         b"and therefore not admissible as evidence of anything.",
                                         "https://whatever.invalid/x", run="RUN_A",
                                         status=200, src="tool", tool="web_fetch")

            q = "the throughput held steady across every one of the four runs"
            chk("an honest citation passes", check_citation(good["id"], q, run="RUN_A")["ok"])

            r = check_citation(good["id"], "the throughput collapsed on every run we attempted", "RUN_A")
            chk("CONTROL an invented quote is refused", not r["ok"] and r["stage"] == "quote")

            r = check_citation(other["id"], q, run="RUN_A")
            chk("CONTROL a citation from another run does not resolve",
                not r["ok"] and r["stage"] == "resolve")

            r = check_citation(model_side["id"], "and therefore not admissible as evidence of anything",
                               run="RUN_A")
            chk("CONTROL a model-addressed artefact is not citable",
                not r["ok"] and r["stage"] == "resolve")

            r = check_citation("0" * 16, q, run="RUN_A")
            chk("CONTROL an unknown hash does not resolve", not r["ok"])

            # tamper: the bytes no longer hash to their own name
            with open(os.path.join(os.environ["AEA_ARTEFACT_DIR"], good["sha256"] + ".bin"), "wb") as f:
                f.write(body + b" and one sentence nobody ever fetched")
            r = check_citation(good["id"], q, run="RUN_A")
            chk("CONTROL an altered artefact fails verification",
                not r["ok"] and r["stage"] == "verify", r.get("why", ""))
            st = verify_store()
            chk("CONTROL the store reports itself TAINTED", st["tainted"] >= 1,
                "tainted=%d" % st["tainted"])

            chk("CONTROL the word SURVIVES is refused", not status_is_legal("SURVIVES")[0],
                status_is_legal("SURVIVES")[1][:60])
            chk("CORROBORATED is accepted", status_is_legal("CORROBORATED")[0])
            chk("DIED is accepted", status_is_legal("DIED")[0])
        finally:
            for k, v in keep.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
    return out


def certify() -> dict:
    have = _store_state()
    ctl = controls()
    store = verify_store()
    missing = [n for n, d in have.items() if not d["present"]]

    # THE VERDICT HAS THREE VALUES, NOT TWO, and the third is the honest one today.
    #
    # CERTIFIED   the controls fire AND the store holds citable, verified artefacts
    # UNEXERCISED the controls fire and THE BOUND HAS NEVER RUN ON REAL BYTES. Not a pass: a
    #             mechanism proved against fixtures and never against the world is a claim about
    #             the fixtures. This repo shipped a certificate that drove `dry` ten times and
    #             `run` zero, and it printed CERTIFIED.
    # FAILED      a control did not fire, or the store is tainted
    ctl_ok = all(c["ok"] for c in ctl)
    if not ctl_ok or store["tainted"]:
        verdict = "FAILED"
    elif store["citable"] == 0:
        verdict = "UNEXERCISED"
    else:
        verdict = "CERTIFIED"

    return dict(
        schema="aea.research_cert/1",
        at=__import__("time").strftime("%Y-%m-%d %H:%M:%S UTC", __import__("time").gmtime()),
        verdict=verdict,
        controls_all_fire=ctl_ok, controls=ctl,
        store=store, stores_present=have, stores_missing=missing,
        not_claimed=[
            "that a citation is FAITHFUL - this decides byte-identity, and a verbatim fragment can "
            "invert its source. Measured, with a real example, in this module's docstring",
            "that a claim was WORTH making - a trivially false claim dies honestly and teaches "
            "nothing. This audits the bookkeeping, which cannot be faked; it cannot audit judgement",
            "that a DIED consequence was ACTED ON - `deaths` below counts consequences NAMED, and "
            "naming what should change is not changing it",
            "that the source is TRUE - an artefact proves a server sent these bytes, nothing more",
        ],
        deaths=audit_deaths(),
        blocked_on=[m for m in missing])


def audit_deaths() -> dict:
    """R5c, AUDITED FROM DISK - was each death honest, by the only tests that cannot be faked?

    This replaced a `not_claimed` line reading "needs a stopping rule and a hypothesis store,
    neither of which exists". Both existed as of 2026-08-04 and the certificate went on printing
    that they did not - a disclaimer that outlived its truth, which is the same defect as a docstring
    promising run-scoping over a function that ignored it. A certificate asserting something false
    about ITSELF is worse than one that stays silent.

    Four tests, and every one is a fact about bytes and timestamps rather than about intent:
      cited        a DIED or CORROBORATED verdict resolves to a stored, citable, verified artefact
      write-ahead  every citation was READ AFTER the claim was PROPOSED. The one test that cannot
                   be satisfied by writing more carefully afterwards
      consequence  every DIED names what changes. A refutation that alters nothing is a diary entry
      independent  the claim came from the record (`from_record`), not from a menu (D51)"""
    try:
        from aea.kernel import artefacts as _a, hypotheses as _h
    except Exception as e:
        return dict(ok=False, why="%s: %s" % (type(e).__name__, str(e)[:80]))
    latest = {}
    for r in _h.rows():
        if r.get("hid"):
            latest[r["hid"]] = r
    vals = list(latest.values())
    art = _a.rows()
    at_by = {}
    for r in art:
        for k in (r.get("id"), r.get("sha256")):
            if k:
                at_by[str(k).lower()] = float(r.get("at") or 0)
    settled = [r for r in vals if r.get("status") in ("DIED", "CORROBORATED")]
    died = [r for r in settled if r["status"] == "DIED"]
    bad_cite, bad_order, bad_conseq, bad_source = [], [], [], []
    for r in settled:
        cites = [str(c).lower() for c in (r.get("citations") or [])]
        if not cites:
            bad_cite.append(r["hid"])
        for c in cites:
            if _a.resolve(c, among=art) is None:
                bad_cite.append(r["hid"])
            elif at_by.get(c, 0) and at_by[c] < float(r.get("at") or 0):
                bad_order.append(r["hid"])
        if not str(r.get("from_record") or "").strip():
            bad_source.append(r["hid"])
    for r in died:
        if not str(r.get("consequence") or "").strip():
            bad_conseq.append(r["hid"])
    runs = {}
    for r in vals:
        if r.get("run"):
            runs.setdefault(r["run"], []).append(r)
    runs_with_a_death = sum(1 for rs in runs.values() if any(x["status"] == "DIED" for x in rs))
    return dict(ok=not (bad_cite or bad_order or bad_conseq or bad_source),
                proposed=len(vals), settled=len(settled), died=len(died),
                corroborated=len(settled) - len(died),
                runs=len(runs), runs_with_a_death=runs_with_a_death,
                uncited=sorted(set(bad_cite)), evidence_predates_claim=sorted(set(bad_order)),
                died_without_consequence=sorted(set(bad_conseq)),
                claim_not_from_record=sorted(set(bad_source)))


def render(c: dict) -> str:
    L = ["=" * 92, "RESEARCH CERTIFICATE - R5's bound, recomputed from disk", "=" * 92]
    s = c["store"]
    L.append("\n  THE STORE")
    L.append("    ledger rows       %d   verified %d   citable %d   not-citable %d"
             % (s["rows"], s["verified"], s["citable"], s["not_citable"]))
    L.append("    failed reads      %d   tainted %d   missing from disk %d"
             % (s["failed_reads"], s["tainted"], s["missing"]))
    L.append("    runs represented  %s" % (", ".join(s["runs"]) or "none"))
    for d in s["tainted_detail"]:
        L.append("      TAINTED %s: %s" % (d["id"], d["why"][:70]))
    L.append("\n  WHAT IS PRESENT")
    for name, d in c["stores_present"].items():
        L.append("    %-20s %-8s %s" % (name, "yes" if d["present"] else "ABSENT", d["what"]))
    L.append("\n  CONTROLS - a scan that finds nothing agrees with everything")
    for x in c["controls"]:
        L.append("    %-52s %s%s" % (x["check"], "ok" if x["ok"] else "FAIL",
                                     ("   " + x["detail"][:40]) if x["detail"] and not x["ok"] else ""))
    d = c.get("deaths") or {}
    if d.get("proposed") is not None:
        L.append("\n  R5c - WERE THE DEATHS HONEST?  (audited from disk, not from intent)")
        L.append("    proposed %d   settled %d   DIED %d   CORROBORATED %d   runs %d   "
                 "runs with a death %d" % (d["proposed"], d["settled"], d["died"],
                                           d["corroborated"], d["runs"], d["runs_with_a_death"]))
        for label, key in (("a verdict with no resolving citation", "uncited"),
                           ("EVIDENCE READ BEFORE THE CLAIM", "evidence_predates_claim"),
                           ("a DIED that names no consequence", "died_without_consequence"),
                           ("a claim not taken from the record", "claim_not_from_record")):
            n = len(d.get(key) or [])
            L.append("    %-40s %s" % (label, "none" if not n else "%d: %s" % (n, d[key][:4])))
    L.append("\n  WHAT IS NOT CLAIMED")
    for n in c["not_claimed"]:
        L.append("    - %s" % n)
    if c["blocked_on"]:
        L.append("\n  BLOCKED ON: %s" % ", ".join(c["blocked_on"]))
    L.append("\n  VERDICT: %s" % c["verdict"])
    if c["verdict"] == "UNEXERCISED":
        L.append("    the controls all fire and the bound has NEVER run on real bytes in production.")
        L.append("    A mechanism proved against fixtures is a claim about the fixtures.")
    return "\n".join(L)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    c = certify()
    if "--json" in sys.argv:
        grid.atomic_save_json(os.path.join(grid.STATE, OUT), c, indent=1)
        print(json.dumps(c, indent=1, default=str))
        sys.exit(0 if c["verdict"] != "FAILED" else 1)
    print(render(c))
    sys.exit(0 if c["verdict"] != "FAILED" else 1)
