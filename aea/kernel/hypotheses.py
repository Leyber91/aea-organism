"""hypotheses.py - R5's POWER: a claim written down BEFORE the evidence that could kill it.

    python -m aea.kernel.hypotheses            the selftest, with controls
    python -m aea.kernel.hypotheses --state    what is proposed, settled, and still open

WHY THIS MODULE EXISTS, and it is one sentence: **there is not a single artefact in `state/` that
is a prediction.** Every record this entity keeps is post-hoc. R3 writes the outcome after it acts.
R4 writes the read after it reads. HADES judges output that already exists. A system that only
records what happened cannot be wrong about anything - it can be incomplete, it can be stale, but
it can never be REFUTED, because it never said anything before the world answered. R5 is the rung
where it starts saying things first.

THE WRITE-AHEAD RULE IS THE WHOLE MECHANISM, and it is checked, not promised. `settle` refuses any
citation whose artefact was READ BEFORE the claim was PROPOSED. Timestamps come from the artefact
ledger, which hashes at the socket, so the ordering is a fact about bytes rather than a courtesy.
Without that check "stated before the evidence" is a sentence in a docstring with nothing under it -
which is precisely what four readers found in `resolve()` on 2026-08-03, where run-scoping was
documented and unimplemented and a model could quote any hash it had ever been near.

THE VOCABULARY IS NOT OURS TO INVENT. `research_cert.VALID_STATUS` already fixes it, and this module
imports rather than redeclares it, so a status this file accepts and the certifier rejects cannot
exist. In particular the word SURVIVES is refused: a hypothesis consistent with the evidence is
CORROBORATED, and treating consistency as confirmation is affirming the consequent. Only refutation
is valid.

A DEATH MUST NAME WHAT CHANGES. `status="DIED"` without a `consequence` is refused. A refutation
that alters nothing is a diary entry - the entity noticing it was wrong and carrying on identically
is the failure this rung is built against, and the reason R5 is "the hypothesis leads to another
path" rather than "the hypothesis is tested".

WHAT THIS MODULE DOES NOT CLAIM:
  - that the claim was WORTH making. A trivially false claim dies honestly and teaches nothing;
    that is a judgement, and this file only does bookkeeping that cannot be faked
  - that the consequence was ACTED ON. It records what should change, not that anything did
  - that the probe was FAIR. An address chosen to produce a known answer still resolves; provenance
    is `artefacts.CITABLE_SRC`'s job and it is enforced there, not here
"""
from __future__ import annotations

import json
import os
import time
import uuid

from aea.kernel import artefacts, grid

STORE = "hypotheses.jsonl"
RUNDIR = "research"

# THE VOCABULARY COMES FROM THE CERTIFIER. Importing it means a status this module writes and the
# certificate refuses cannot exist - the alternative is two lists that agree until one is edited.
try:
    from aea.lab.research_cert import VALID_STATUS
except Exception:                                  # the certifier is a lab module; never hard-depend
    VALID_STATUS = ("DIED", "CORROBORATED", "FORKS", "UNSETTLED", "OPEN")

# Refused by name, with the reason, because it is the specific mistake this vocabulary exists to
# stop and a silent rejection would teach nothing.
REFUSED_WORDS = {
    "survives": ("SURVIVES asserts confirmation from consistency, which is affirming the "
                 "consequent. Use CORROBORATED: not yet dead, and that is all."),
    "confirmed": ("CONFIRMED claims the evidence established the claim. Evidence can only fail to "
                  "kill it. Use CORROBORATED."),
    "proven": "PROVEN is not available to an empirical claim. Use CORROBORATED or DIED.",
}


def _path() -> str:
    return os.path.join(grid.STATE, STORE)


def _rundir() -> str:
    return os.path.join(grid.STATE, RUNDIR)


def rows(path: str = None) -> list:
    """Every row, unparseable lines included as a marked row rather than dropped.

    A silently-skipped bad line is a hypothesis that quietly stops existing, which would let a
    corrupt write erase a claim and leave the store looking healthy."""
    p = path or _path()
    out = []
    if not os.path.exists(p):
        return out
    with open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                out.append(dict(hid=None, claim="", note="UNPARSEABLE STORE LINE"))
    return out


def _append(row: dict) -> None:
    """Append and FLUSH. The claim must be on disk before the probe runs, or the ordering this rung
    rests on is a hope about scheduling."""
    p = _path()
    with grid.file_lock(p):
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())


def status_is_legal(status: str):
    """(ok, why). The certifier's own test, applied at the write instead of at the audit."""
    s = str(status or "").strip()
    low = s.lower()
    if low in REFUSED_WORDS:
        return False, REFUSED_WORDS[low]
    if s not in VALID_STATUS:
        return False, "status %r is not one of %s" % (s, ", ".join(VALID_STATUS))
    return True, ""


def propose(claim: str, from_record: str, killer: str, run: str = "",
            holds_fixed=None, at: float = None) -> dict:
    """State a claim BEFORE looking. Returns the row; raises if it is not a hypothesis.

    `from_record` - WHERE IN THE ENTITY'S OWN RECORD THIS CLAIM ALREADY LIVES. Required, and it is
    the guard against the failure that would make this whole rung theatre: if the claim comes from
    a menu a human wrote, R5 demonstrates the menu. D51 - a label is not a measurement. A claim must
    be something the record ALREADY ASSERTS, so that killing it changes what the entity holds true.

    `killer` - THE OBSERVATION THAT WOULD REFUTE IT, named before the evidence exists. A claim with
    no stated killer is not falsifiable and is refused here rather than discovered to be unfalsifiable
    after the evidence is in, when the killer can be chosen to fit what arrived.

    `holds_fixed` - what is assumed constant. Duhem-Quine: a refutation lands on the conjunction of
    the claim and its auxiliaries, so a death is only attributable if the auxiliaries were named in
    advance. Optional, recorded, never inferred."""
    claim = str(claim or "").strip()
    from_record = str(from_record or "").strip()
    killer = str(killer or "").strip()
    if not claim:
        raise ValueError("a hypothesis needs a claim")
    if not from_record:
        raise ValueError("a hypothesis needs `from_record` - where the entity's own record already "
                         "asserts this. A claim from a menu tests the menu, not the entity (D51)")
    if not killer:
        raise ValueError("a hypothesis needs `killer` - the observation that would refute it, named "
                         "BEFORE the evidence. An unfalsifiable claim cannot die and cannot pass R5")
    row = dict(schema="aea.hypothesis/1",
               hid=uuid.uuid4().hex[:16],
               at=float(at if at is not None else time.time()),
               run=str(run or ""),
               claim=claim, from_record=from_record, killer=killer,
               holds_fixed=list(holds_fixed or []),
               status="OPEN", settled_at=None, citations=[], consequence="", why="")
    _append(row)
    return row


def get(hid: str, among: list = None) -> dict:
    for r in (among if among is not None else rows()):
        if r.get("hid") == hid:
            return r
    return None


def settle(hid: str, status: str, citations: list, consequence: str = "", why: str = "",
           among_artefacts: list = None, at: float = None) -> dict:
    """Close a claim against evidence. Raises rather than writing a settlement that proves nothing.

    FIVE REFUSALS, each one a way a settlement could look valid and be empty:

      unknown hid            settling a claim that was never proposed IS the post-hoc case
      illegal status         SURVIVES / CONFIRMED / PROVEN, and anything outside VALID_STATUS
      DIED with no consequence   a refutation that changes nothing is a diary entry
      a citation that does not resolve   run-scoped and provenance-checked by `artefacts.resolve`
      EVIDENCE OLDER THAN THE CLAIM      the write-ahead rule, and the only one that cannot be
                                         satisfied by writing more carefully after the fact

    The last is the load-bearing one. Read times come from the artefact ledger, which hashes at the
    socket; the claim's time comes from a line flushed and fsynced before any probe ran. If the
    bytes arrived first, the claim was fitted to them, and no amount of honest intent changes that."""
    ok, why_bad = status_is_legal(status)
    if not ok:
        raise ValueError(why_bad)
    all_rows = rows()
    row = get(hid, among=all_rows)
    if row is None:
        raise ValueError("no hypothesis %r - a settlement without a prior proposal is post-hoc by "
                         "construction" % hid)
    if str(status) == "DIED" and not str(consequence or "").strip():
        raise ValueError("a DIED hypothesis must name its consequence - what changes now that this "
                         "is false. A refutation that alters nothing is a diary entry")

    cites = [str(c).strip().lower() for c in (citations or []) if str(c).strip()]
    if str(status) in ("DIED", "CORROBORATED") and not cites:
        raise ValueError("%s needs at least one citation - a verdict with no evidence is an "
                         "opinion" % status)

    among = among_artefacts if among_artefacts is not None else artefacts.rows()
    resolved = []
    for c in cites:
        r = artefacts.resolve(c, among=among)
        if r is None:
            raise ValueError("citation %r does not resolve to a stored, citable artefact in this "
                             "run" % c[:24])
        # THE WRITE-AHEAD CHECK.
        read_at = float(r.get("at") or 0)
        if read_at and read_at < float(row.get("at") or 0):
            raise ValueError(
                "citation %r was read %.1fs BEFORE the claim was proposed - that is evidence the "
                "claim was fitted to, not evidence it risked" % (c[:16], float(row["at"]) - read_at))
        resolved.append(r.get("id") or r.get("sha256"))

    out = dict(row)
    out.update(status=str(status), settled_at=float(at if at is not None else time.time()),
               citations=cites, consequence=str(consequence or ""), why=str(why or ""),
               resolved=resolved, schema="aea.hypothesis.settled/1")
    _append(out)
    return out


def state() -> dict:
    """The store, folded. Later rows for a hid win, so a settlement supersedes its proposal."""
    latest = {}
    for r in rows():
        h = r.get("hid")
        if h:
            latest[h] = r
    vals = list(latest.values())
    by_status = {}
    for r in vals:
        by_status[r.get("status") or "?"] = by_status.get(r.get("status") or "?", 0) + 1
    died = [r for r in vals if r.get("status") == "DIED"]
    return dict(total=len(vals), by_status=by_status,
                died=len(died),
                deaths_with_consequence=sum(1 for r in died if str(r.get("consequence") or "").strip()),
                runs=sorted({r.get("run") for r in vals if r.get("run")}),
                open=[r["hid"] for r in vals if r.get("status") == "OPEN"])


def write_run(run: str, question: str, hypotheses: list, note: str = "") -> str:
    """The run path object: what was asked, what was claimed, how each claim ended.

    Written LAST, from the store, so it can never disagree with it - a summary computed from its own
    inputs at the same moment it is written is a summary that cannot drift."""
    d = _rundir()
    os.makedirs(d, exist_ok=True)
    hs = [h for h in hypotheses if h]
    doc = dict(schema="aea.research_run/1", run=str(run),
               at=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
               question=str(question), note=str(note),
               n=len(hs),
               died=sum(1 for h in hs if h.get("status") == "DIED"),
               corroborated=sum(1 for h in hs if h.get("status") == "CORROBORATED"),
               unsettled=sum(1 for h in hs if h.get("status") not in ("DIED", "CORROBORATED")),
               hypotheses=hs)
    p = os.path.join(d, "%s.json" % str(run))
    grid.atomic_save_json(p, doc, indent=1)
    return p


# ---------------------------------------------------------------------------------------------
def selftest() -> list:
    """Every refusal gets a CONTROL. A store that accepts everything certifies nothing."""
    import tempfile
    checks = []

    def chk(name, ok, detail=""):
        checks.append((name, bool(ok), detail))

    tmp = tempfile.mkdtemp(prefix="hyp_")
    old = os.environ.get("AEA_STATE")
    os.environ["AEA_STATE"] = tmp
    try:
        # a real artefact to cite, stored AFTER the claim
        h = propose("rod nvidia/example cannot answer",
                    from_record="energy_usage.json: consec_fail=97, ok=0 in 97 calls",
                    killer="ask the rod; any 200 with non-empty text refutes it",
                    run="t1")
        chk("a hypothesis can be proposed", bool(h.get("hid")) and h["status"] == "OPEN")
        chk("it records WHERE the claim came from", bool(h["from_record"]))
        chk("it records its killer BEFORE the evidence", bool(h["killer"]))

        for bad, label in ((dict(claim="", from_record="x", killer="y"), "no claim"),
                           (dict(claim="c", from_record="", killer="y"), "no from_record"),
                           (dict(claim="c", from_record="x", killer=""), "no killer")):
            try:
                propose(**bad)
                chk("CONTROL a hypothesis with %s is refused" % label, False)
            except ValueError:
                chk("CONTROL a hypothesis with %s is refused" % label, True)

        artefacts.context_set(src="dispatch", run="t1")
        a = artefacts.store(b"HTTP 200 - the rod answered: ok", "probe://nvidia/example",
                            run="t1", status=200, src="dispatch")
        cite = a.get("id") or a.get("sha256")
        rowset = artefacts.rows()

        s = settle(h["hid"], "DIED", [cite],
                   consequence="clear the cooldown and return the rod to the ladder",
                   among_artefacts=rowset)
        chk("a claim can DIE against a real citation", s["status"] == "DIED")
        chk("the death names its consequence", bool(s["consequence"]))

        for word in ("SURVIVES", "CONFIRMED", "PROVEN"):
            try:
                settle(h["hid"], word, [cite], among_artefacts=rowset)
                chk("CONTROL %s is refused" % word, False)
            except ValueError:
                chk("CONTROL %s is refused" % word, True)

        try:
            settle(h["hid"], "DIED", [cite], consequence="", among_artefacts=rowset)
            chk("CONTROL a DIED with no consequence is refused", False)
        except ValueError:
            chk("CONTROL a DIED with no consequence is refused", True)

        try:
            settle("nosuchhid", "CORROBORATED", [cite], among_artefacts=rowset)
            chk("CONTROL settling an unproposed claim is refused", False)
        except ValueError:
            chk("CONTROL settling an unproposed claim is refused", True)

        try:
            settle(h["hid"], "CORROBORATED", ["deadbeefdeadbeef"], among_artefacts=rowset)
            chk("CONTROL an unresolvable citation is refused", False)
        except ValueError:
            chk("CONTROL an unresolvable citation is refused", True)

        try:
            settle(h["hid"], "CORROBORATED", [], among_artefacts=rowset)
            chk("CONTROL a verdict with no citation is refused", False)
        except ValueError:
            chk("CONTROL a verdict with no citation is refused", True)

        # THE WRITE-AHEAD CONTROL: evidence that predates the claim
        h2 = propose("a claim made after its evidence", from_record="x", killer="y", run="t1")
        old_art = artefacts.store(b"bytes that arrived long before the claim",
                                  "probe://nvidia/older", run="t1", status=200, src="dispatch",
                                  at=float(h2["at"]) - 600.0)
        try:
            settle(h2["hid"], "DIED", [old_art.get("id")], consequence="c",
                   among_artefacts=artefacts.rows())
            chk("CONTROL evidence OLDER than the claim is refused", False)
        except ValueError as e:
            chk("CONTROL evidence OLDER than the claim is refused", "BEFORE" in str(e))

        st = state()
        chk("the state folds settlements over proposals", st["died"] == 1, str(st["by_status"]))
        chk("a death without a consequence cannot exist",
            st["deaths_with_consequence"] == st["died"])

        p = write_run("t1", "does the record's claim about dead rods hold?", [s])
        chk("a run object is written", os.path.exists(p))
        doc = json.load(open(p, encoding="utf-8"))
        chk("the run object counts its own deaths", doc["died"] == 1)
    finally:
        if old is None:
            os.environ.pop("AEA_STATE", None)
        else:
            os.environ["AEA_STATE"] = old
    return checks


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if "--state" in sys.argv:
        print(json.dumps(state(), ensure_ascii=False, indent=1))
        sys.exit(0)
    res = selftest()
    for name, ok, detail in res:
        print("  %-56s %s%s" % (name, "ok" if ok else "FAIL", ("   " + detail) if detail else ""))
    bad = [r for r in res if not r[1]]
    print("\n  %d of %d checks pass" % (len(res) - len(bad), len(res)))
    sys.exit(1 if bad else 0)
