"""artefacts.py - R5's BOUND: ONE READ, AND THE BYTES ARE HASHED WHERE THEY ARRIVE.

    python -m aea.kernel.artefacts            the store, and the self-test with its controls

R5's declared bound is A FABRICATED SOURCE: every citation must resolve to bytes actually fetched,
hashed at fetch time. A research organ is the first component in this system with a MOTIVE to invent
a reference - every bound below is about what LEAVES the machine, and this is the first one about
what comes IN and gets written down as true.

WHY THE HASH THAT ALREADY EXISTED DOES NOT CARRY IT. Measured 2026-08-03: `hands.invoke` writes
`result_sha=sha256(out)` on every successful call (hands.py:1185). `out` is THE TOOL'S RETURN STRING
- what the entity was shown. Between the socket and that string the bytes are cut four times:

    hands._web_fetch       r.read().decode(...)[:8000]      the wire, cut at 8000
    dispatch.run           str(body)[:4000]                 cut again, then fenced
    hands._look_outward    str(x["text"])[:1200]            per source
    hands._look_outward    (head + body)[:6000]             the whole reply

So a citation checked against `result_sha` proves the entity quoted ITS OWN CONTEXT. It does not
prove a server ever sent those bytes. That is D51's shape in its most convincing costume: a hash is
the strongest-looking label there is, and that one measures the summary.

AND THE PROOF SHAPE IS DIFFERENT FROM EVERY BOUND BELOW, which is what decides where this code goes:

    R2's bound   what is REPRESENTABLE   697 of 1,112,064 codepoints, none alphabetic.
                                         An injection cannot be EXPRESSED
    R5's bound   what is PRODUCIBLE      bytes the entity never saw, hashed at a moment it does
                                         not control. A source cannot be INVENTED

A bound on what is producible has to sit at the point of production. That is the socket, and there
were THREE of them - `_web_fetch`, `_api_json`, and `_s_arxiv` carrying its own copy of the same
open. A hash added at one covers a third of the bytes while the certificate still prints CERTIFIED,
which is why the first edit of R5 is not adding a hash: it is making one read exist to add it to.
(One executor per shape, never two - the same defect `dry`/`run` already paid for in `dispatch.py`.)

WHAT THIS CHANGES FOR CALLERS, STATED EXACTLY - the first version of this docstring said "it does
not change any caller's behaviour" and an adversarial pass proved that false against HEAD. Redirect
policy, timeout and decoding are passed IN and are unchanged. **Status handling changed in one
place and only one:** `_api_json` and `_s_arxiv` used to raise on a non-200 BEFORE reading the body;
they now read and store it, then check `row["status"]`. That is deliberate - a 202 challenge page is
how an engine refuses a non-browser client, and it is now on disk instead of being a number in an
exception - but it is a change, and a docstring that denied it was a label over a measurement.

WHAT IS DELIBERATELY NOT AN ARTEFACT, and this exclusion is load-bearing rather than tidy. The model
POST in `hands._chat` does not come through here. A store that held model responses beside fetched
pages would make A FABRICATED SOURCE CITABLE BY CONSTRUCTION: the organ with the motive to invent a
reference would be writing into the very store that proves references real. The rule is one line -
**the artefact store holds bytes from SOURCES, never bytes from MODELS** - and it is why routing
"every socket in the file" through here would have been the wrong instinct. Also excluded:
`_web_search_scraper_dead`, which is an unreferenced headstone, and routing it would make a dead
route look wired.

THE FOUR READS THAT DO COME THROUGH, all of them the entity's outward surface:
`_web_fetch`, `_api_json` (hn / hf / github), `_s_arxiv`, and `_json_get`.

WHO CAN CHECK A CITATION, stated exactly, because the first version implied more. Verification is
LOCAL: `verify` and `quotes` recompute from the bytes on disk and need nothing from the running
process, so a citation can be checked by anything with access to the store - a later run, a
different tool, a person. It is NOT remotely reproducible: re-fetching the URL does not reproduce
the digest, because pages change. That is not a weakness in the design, it is the reason the bytes
are hashed AT ARRIVAL rather than cited by address - an address is a promise about the future and a
digest is a fact about what was received. The store is gitignored deliberately: the bytes are
third-party content and the ledger is runtime state.

THE ENTITY CANNOT INFLUENCE ANY OF IT, and these are checkable rather than assumed:
  it does not choose the URL      `dispatch.run` takes results in document order; `_look_outward`
                                  deliberately does not expose `max_fetch` (hands.py:332)
  it never sees the raw bytes     the four truncations above
  the filename IS the digest      writing to it is writing the content it names
  resolution is RUN-SCOPED        a citation resolves only against the artefacts of ITS run, so
                                  quoting a hash from elsewhere in the store is not a citation
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request

from aea.kernel import grid

DIRNAME = "artefacts"
LEDGER = "artefacts.jsonl"

# A CAP, AND IT IS LOGGED - silent truncation reads as completion (structure conversation, §7).
# Generous on purpose: the pages this fetches are search results and abstracts, and the budget
# above already bounds volume at 36 reads a day.
MAX_BYTES = 2_000_000

# The citation id is a PREFIX, and it is an index into one run's set - never a cryptographic
# identifier. `verify` compares the FULL digest recomputed from disk. The prefix exists because a
# model has to copy it verbatim into a find, and 64 hex characters copied by hand is a dropped
# citation waiting to happen.
ID_CHARS = 16

# THE FLOOR ON A QUOTE. Raised from 12 on 2026-08-03: at twelve characters a fragment can be
# verbatim and still invert its source, and a short fragment is cheap to find in any page. Forty is
# not a fix - see `context()` for why there cannot be one - it just makes the cheap attack cost
# more than reading the sentence would have.
MIN_QUOTE = 40


# =================================================================================================
# THE READ CONTEXT - who is doing this read, and for which inquiry.
#
# WHY IT CANNOT BE DECIDED INSIDE THE READ. `_api_json` serves `dispatch.run` (whose query is a
# literal from the closed topic table) AND `hands._web_search` called directly by the entity (whose
# query is prose the model wrote). Same function, same host, two completely different provenances -
# so the fact has to come from the CALLER and there is no honest way to infer it lower down.
#
# THREAD-LOCAL, AND PROPAGATED BY HAND INTO WORKERS. Both outbound paths fan out through a
# ThreadPoolExecutor - `_web_search` across four routes, `dispatch.run` across three fetches - and a
# thread-local does NOT cross that boundary. A context that silently failed to propagate would mark
# dispatch's own fetches as `tool` and make them uncitable, which is a bound that fails CLOSED and
# would still be a bug. `carry()` captures the parent's context and restores it inside the worker.
#
# THE DEFAULT IS THE UNTRUSTED ONE. An unmarked read is `tool`, never `dispatch`: a route nobody has
# classified yet is not evidence.
_CTX = threading.local()


def context_get() -> tuple:
    return (getattr(_CTX, "src", "") or "tool", getattr(_CTX, "run", "") or "")


def context_set(src: str = "", run: str = ""):
    _CTX.src, _CTX.run = (src or "tool"), (run or "")


class using:
    """`with artefacts.using("dispatch", run_id):` - marks every read made inside it."""

    def __init__(self, src: str, run: str = ""):
        self.src, self.run, self.prev = src, run, None

    def __enter__(self):
        self.prev = context_get()
        context_set(self.src, self.run)
        return self

    def __exit__(self, *a):
        context_set(*self.prev)
        return False


def carry(fn):
    """Wrap a callable so it runs in the CALLER's read context, not the worker's fresh one."""
    src, run = context_get()

    def _inner(*a, **kw):
        with using(src, run):
            return fn(*a, **kw)
    return _inner


def _dir() -> str:
    """Resolved at CALL time. A path bound at import cannot be sandboxed by a test (D48)."""
    return os.environ.get("AEA_ARTEFACT_DIR") or os.path.join(grid.STATE, DIRNAME)


def _ledger_path() -> str:
    return os.environ.get("AEA_ARTEFACT_LEDGER") or os.path.join(grid.STATE, LEDGER)


def _blob(digest: str) -> str:
    return os.path.join(_dir(), digest + ".bin")


def digest_of(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def cite_id(digest: str) -> str:
    return str(digest or "")[:ID_CHARS]


def store(data: bytes, url: str, run: str = "", status=None, note: str = "",
          truncated: bool = False, at: float = None, src: str = "", tool: str = "") -> dict:
    """Put bytes on disk under their own digest and leave one row. Returns the row.

    ORDER IS BYTES-THEN-ROW, and the reverse would be worse than useless. A crash between them
    leaves an artefact with no row, which is an orphan and harmless. Rows-first would leave a row
    pointing at a file that does not exist - indistinguishable from an artefact someone deleted,
    which is exactly the signal this store exists to make legible.

    `src` AND `tool` ARE THE PROVENANCE, AND WITHOUT THEM THE BOUND DOES NOT HOLD. Found by an
    adversarial pass 2026-08-03, reproduced: `web_fetch` and `json_get` are entity-callable tools
    whose ADDRESS THE MODEL WRITES (`hands.allowed('web_fetch','public')` returns ok right now, and
    `converse` grants both to the online seat). Their bytes were landing in this store beside
    dispatch's certified fetches with nothing to tell them apart - so the entity could fetch a URL
    it composed, have it hashed, and cite it. "A source cannot be INVENTED" was false for two of the
    four routed sites, and this module's own docstring said the opposite.

    THE RACE, reproduced 5 of 5 by the same pass: three threads storing identical bytes raced on a
    shared `<digest>.bin.part` and two died with WinError 32. `_web_search` fires four routes
    concurrently, so this was on the live path, not a theoretical one. The temp name is now unique
    per process and thread."""
    at = time.time() if at is None else at
    d = digest_of(data)
    os.makedirs(_dir(), exist_ok=True)
    p = _blob(d)
    if not os.path.exists(p):                      # identical bytes are one artefact, by definition
        tmp = "%s.%d.%d.part" % (p, os.getpid(), threading.get_ident())
        try:
            with open(tmp, "wb") as f:
                f.write(data)
            os.replace(tmp, p)
        except OSError:
            # Another writer won the race with the SAME BYTES - the digest guarantees that. The
            # artefact is present either way; only lose if it is genuinely absent.
            if not os.path.exists(p):
                raise
            try:
                os.remove(tmp)
            except OSError:
                pass
    row = dict(sha256=d, id=cite_id(d), url=str(url)[:400], run=str(run or ""),
               src=str(src or ""), tool=str(tool or ""),
               at=at, iso=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(at)),
               bytes=len(data), status=status, truncated=bool(truncated), note=str(note)[:200])
    grid.append_jsonl(_ledger_path(), row)
    return row


def note_failure(url: str, why: str, run: str = "", status=None, at: float = None,
                 src: str = "", tool: str = "") -> dict:
    """A read that produced no bytes STILL LEAVES A ROW.

    Without this, "we never tried" and "it failed" are the same picture from outside - the
    null-that-reads-as-a-result, which this repo has now paid for in `_host`, in `egress._load` and
    in `web_search` reporting a captcha page as an empty result set."""
    at = time.time() if at is None else at
    row = dict(sha256=None, id=None, url=str(url)[:400], run=str(run or ""),
               src=str(src or ""), tool=str(tool or ""),
               at=at, iso=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(at)),
               bytes=0, status=status, truncated=False, note=str(why)[:200])
    grid.append_jsonl(_ledger_path(), row)
    return row


def read(url: str, headers: dict = None, timeout: float = 300.0, opener=None,
         run: str = "", max_bytes: int = MAX_BYTES, src: str = "", tool: str = "") -> tuple:
    """THE ONE READ. Returns (raw_bytes, row). Raises what the caller's own code raised before.

    Every argument that could change a caller's behaviour is passed IN and defaulted to nothing:
    `opener` carries the redirect policy, `timeout` the read deadline, and NO status check happens
    here because the callers checked differently and a refactor may not decide that for them.

    `timeout` is an inactivity budget and is never None. A rod that thinks for minutes must survive;
    a peer that stops sending without closing must not hang the loop forever - measured cost of the
    alternative: two experiments sat 28 and 64 minutes on one second of CPU each.

    THE STORE IS INSIDE THE TRY, and the first version's was not. Measured by the adversarial pass:
    with the store directory unwritable a 400,114-byte response was fetched, `_web_fetch` returned
    an error string, and the ledger went 0 -> 0 rows. A read that reached a server and vanished
    without a trace is the exact shape this module exists to make impossible."""
    ctx_src, ctx_run = context_get()
    src, run = (src or ctx_src), (run or ctx_run)
    req = urllib.request.Request(url, headers=dict(headers or {}))
    op = opener or urllib.request.build_opener()
    try:
        with op.open(req, timeout=timeout) as r:
            status = getattr(r, "status", None)
            data = r.read(max_bytes + 1)
    except Exception as e:
        note_failure(url, "%s: %s" % (type(e).__name__, str(e)[:120]), run=run, src=src, tool=tool)
        raise
    truncated = len(data) > max_bytes
    if truncated:
        data = data[:max_bytes]
    try:
        row = store(data, url, run=run, status=status, truncated=truncated, src=src, tool=tool,
                    note=("read capped at %d bytes" % max_bytes) if truncated else "")
    except Exception as e:
        # THE BYTES ARRIVED AND COULD NOT BE KEPT. That is a different event from a failed read and
        # it must not be silent: the caller still gets its bytes, and the ledger says why no
        # artefact exists for them. A citation against this read will correctly fail to resolve.
        note_failure(url, "STORE FAILED (%s: %s) - bytes arrived, no artefact"
                     % (type(e).__name__, str(e)[:90]), run=run, status=status, src=src, tool=tool)
        raise
    return data, row


# =================================================================================================
# VERIFICATION. Everything below recomputes from disk and needs nothing from the running process -
# a certificate that trusts the process it is certifying is a comment.
# =================================================================================================

def rows(path: str = None) -> list:
    p = path or _ledger_path()
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
                out.append(dict(sha256=None, id=None, url="", note="UNPARSEABLE LEDGER LINE"))
    return out


# WHICH ROWS MAY BE CITED AT ALL. An allow-list, not a deny-list, so a route nobody has thought of
# yet is already refused - the same discipline as `READABLE_STATES`.
#
# `web_fetch` and `json_get` are entity-callable and THE MODEL WRITES THE ADDRESS. Their bytes are
# still hashed and still stored, because the ledger's job is to record every read - but they are not
# EVIDENCE, because a source the entity chose is not a source that could have refuted it. Only reads
# composed by `dispatch` from the closed topic table may ground a citation.
#
# `probe` JOINS THE LIST 2026-08-04, and it belongs on the principle above rather than beside it.
# The rule is not "only HTTP through dispatch"; the rule is that the address must not have been
# chosen by the thing whose claim is being tested. A fleet probe's address is a rod id read
# verbatim out of `energy_usage.json` - the very record whose assertion ("this rod has failed 97
# times and cannot answer") is under test. The entity does not pick which rod to ask; the claim
# picks it. So the source could have refuted the claim, which is exactly what the allow-list is
# protecting, and it is the reason R5's first run can ground its citations at all.
#
# The narrow reading would have been to keep the list at `dispatch` and let fleet evidence be
# uncitable. That fails the honesty law from the other side: the bytes ARE evidence, hashed at the
# socket, addressed by the record, and refusing to let them ground a citation would force the
# alternative of a verdict with no citation - which `hypotheses.settle` refuses outright.
CITABLE_SRC = ("dispatch", "probe")


def resolve(cite: str, among: list = None, require_citable: bool = True):
    """The row a citation names, or None. `among` SCOPES IT TO ONE RUN and that is the point.

    `among` IS NOW REQUIRED, and the default that made it optional was the defect. Found by four
    independent readers 2026-08-03: not one production call site passed `run=`, nothing read
    `row['run']`, and `among=None` fell back to the whole store - so "resolution is RUN-SCOPED" was
    a sentence in this docstring with no mechanism under it. A model could quote any hash it had
    ever been near, for any claim, and the check would pass while proving nothing about THIS
    inquiry. Maintenance callers that genuinely want the store-wide question pass `among=rows()`
    explicitly, so that answer is always something somebody asked for.

    `require_citable` enforces provenance: a row whose bytes came from an address the MODEL wrote is
    not evidence, whatever it hashes to."""
    c = str(cite or "").strip().lower()
    if not c:
        return None
    if among is None:
        raise ValueError("resolve() requires `among` - a citation is scoped to ITS run. "
                         "Pass among=rows() explicitly for the store-wide maintenance question.")
    for r in among:
        if not r.get("sha256"):
            continue
        if require_citable and str(r.get("src") or "") not in CITABLE_SRC:
            continue
        if r["sha256"] == c or str(r.get("id") or "") == c[:ID_CHARS]:
            return r
    return None


def latest_for(url: str, run: str = "", among: list = None):
    """The most recent artefact row for this URL in this run, or None.

    THE LEDGER IS HOW A CITATION ID GETS BACK TO THE CALLER, and it has to be, because the row is
    created three frames below where it is needed: `dispatch.run` invokes a TOOL, the tool returns a
    string, and the row is born inside `hands._web_fetch`. Threading an out-parameter through a tool
    boundary would put a research concern inside the tool contract; reading the record back does not.

    THE DEFECT THIS CLOSES, found 2026-08-03 and verified on the exact lines: nothing ever showed
    the entity an artefact id, so the find schema `{"artefact": "<16 hex>", ...}` was UNSATISFIABLE
    BY ANY HONEST RUN. R5's whole extraction step was impossible as specified, and it would have
    surfaced as the model failing to produce valid citations - i.e. as the model's fault."""
    u, r = str(url or ""), str(run or "")
    best = None
    for x in (among if among is not None else rows()):
        if not x.get("sha256"):
            continue
        if str(x.get("url") or "")[:400] != u[:400]:
            continue
        if r and str(x.get("run") or "") != r:
            continue
        if best is None or (x.get("at") or 0) >= (best.get("at") or 0):
            best = x
    return best


def verify(row: dict) -> tuple:
    """(ok, why). Recompute the digest from the bytes on disk and compare to what was written at
    fetch time. A mismatch is not a bad citation - it is a TAINTED STORE, and the caller must treat
    it as such rather than dropping one find and continuing."""
    d = str((row or {}).get("sha256") or "")
    if not d:
        return False, "row carries no digest - it is a failure row, not an artefact"
    p = _blob(d)
    if not os.path.exists(p):
        return False, "artefact is missing from disk"
    with open(p, "rb") as f:
        data = f.read()
    got = digest_of(data)
    if got != d:
        return False, "DIGEST MISMATCH: stored bytes hash to %s, the row says %s" % (got[:16], d[:16])
    if row.get("bytes") is not None and int(row["bytes"]) != len(data):
        return False, "length disagrees: %d on disk, %d in the row" % (len(data), int(row["bytes"]))
    return True, ""


def quotes(row: dict, quote: str, encoding: str = "utf-8") -> tuple:
    """(ok, why) - is this quote VERBATIM in the stored bytes?

    THIS IS THE CHECK THE WHOLE BOUND RESTS ON, and hash-membership is not a substitute for it. A
    find that names a real artefact and invents what it said is the fabrication this rung is about;
    resolving the hash would wave it straight through. Decoded with the same codec the caller used
    to show it, because a quote is compared against what could have been read, not against bytes."""
    q = str(quote or "")
    if len(q.strip()) < MIN_QUOTE:
        return False, ("quote is too short to be evidence of anything (%d chars, %d required)"
                       % (len(q.strip()), MIN_QUOTE))
    ok, why = verify(row)
    if not ok:
        return False, why
    with open(_blob(row["sha256"]), "rb") as f:
        text = f.read().decode(encoding, "ignore")
    at = text.find(q)
    if at < 0:
        # One normalisation, and only one: whitespace. HTML wraps lines wherever it likes and a
        # quote that differs by a newline is the same quote. Anything beyond this is deciding what
        # the model MEANT, which is a move a fabrication check may never make.
        flat = " ".join(text.split())
        at = flat.find(" ".join(q.split()))
        if at < 0:
            return False, "quote does not appear in the stored bytes"
        text = flat
    return True, "at=%d" % at


def context(row: dict, quote: str, window: int = 240, encoding: str = "utf-8") -> str:
    """The bytes AROUND a quote, so a cherry-pick is visible to whoever reads the certificate.

    VERBATIM IS NOT FAITHFUL, and this is the limit the adversarial pass found and the one no hash
    can close. Reproduced 2026-08-03 against real bytes: a page reading *"we are often asked whether
    the export API is deprecated. It is not, and there are no plans to retire it"* yields the
    perfectly verbatim 28-character quote *"the export API is deprecated"*, which passes every stage
    and INVERTS the source. The skeptic that checked it called it the strongest finding in the set.

    There is no mechanical fix, because faithfulness is a semantic property and this module only
    decides byte-identity. What there is: make the neighbourhood visible. A quote whose surrounding
    240 characters contradict it is legible to a human reading the run, and to any later check that
    wants to look. The bound stays what it can honestly be - THE SOURCE EXISTS AND SAID THESE BYTES
    - and the certificate stops implying more than that."""
    ok, _ = verify(row)
    if not ok:
        return ""
    with open(_blob(row["sha256"]), "rb") as f:
        text = f.read().decode(encoding, "ignore")
    q = str(quote or "")
    at = text.find(q)
    if at < 0:
        text = " ".join(text.split())
        q = " ".join(q.split())
        at = text.find(q)
        if at < 0:
            return ""
    a = max(0, at - window)
    b = min(len(text), at + len(q) + window)
    return ("..." if a else "") + text[a:b] + ("..." if b < len(text) else "")


def stats() -> dict:
    rs = rows()
    good = [r for r in rs if r.get("sha256")]
    bad = [r for r in rs if not r.get("sha256")]
    distinct = {r["sha256"] for r in good}
    return dict(rows=len(rs), reads_with_bytes=len(good), failed_reads=len(bad),
                distinct_artefacts=len(distinct),
                on_disk=len([n for n in os.listdir(_dir())
                             if n.endswith(".bin")]) if os.path.isdir(_dir()) else 0,
                total_bytes=sum(int(r.get("bytes") or 0) for r in good))


# =================================================================================================
# THE SELF-TEST. Every check gets a POSITIVE CONTROL on the defect class it claims to cover, or it
# does not count - and this file's whole reason to exist is a check that looked right and measured
# the wrong object.
# =================================================================================================

def selftest() -> list:
    """Runs entirely in a temp store. Returns [(name, ok, detail)]."""
    import tempfile
    out = []

    def chk(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    with tempfile.TemporaryDirectory() as td:
        old_d = os.environ.get("AEA_ARTEFACT_DIR")
        old_l = os.environ.get("AEA_ARTEFACT_LEDGER")
        os.environ["AEA_ARTEFACT_DIR"] = os.path.join(td, "artefacts")
        os.environ["AEA_ARTEFACT_LEDGER"] = os.path.join(td, "artefacts.jsonl")
        try:
            body = (b"the quick brown fox jumps over the lazy dog, and the measurement was taken "
                    b"at twelve hundred hours on a Tuesday in the rain")
            r1 = store(body, "https://example.invalid/a", run="RUN1", status=200, src="dispatch")
            r2 = store(b"a different document entirely, about something else and somewhere else",
                       "https://example.invalid/b", run="RUN2", status=200, src="dispatch")
            long_q = "jumps over the lazy dog, and the measurement was taken"

            chk("digest is of the RAW bytes", r1["sha256"] == hashlib.sha256(body).hexdigest())
            chk("the file is named by its digest", os.path.exists(_blob(r1["sha256"])))
            chk("a stored artefact verifies", verify(r1)[0])
            chk("a quote that IS there resolves", quotes(r1, long_q)[0])
            chk("the quote's offset is reported", "at=" in quotes(r1, long_q)[1])
            chk("context shows the neighbourhood", long_q in context(r1, long_q))

            # ---- READ() IS EXERCISED, AND THIS IS THE CHECK THAT WAS MISSING -------------------
            #
            # THE DEFECT, found by an adversarial pass on 2026-08-03 and reproduced: this suite
            # tested `store`, `verify`, `quotes` and `resolve` and NEVER CALLED `read` - the one
            # function that hashes at arrival, which is the entire bound. A reviewer replaced
            # `read` with an implementation that hashed a truncated summary instead of the wire
            # bytes and all fourteen checks still passed. Fourteen of fourteen, seven of them
            # controls, and not one of them touched the claim.
            #
            # That is D51 in the file whose own docstring cites D51: A LABEL IS NOT A MEASUREMENT,
            # and the reader wrote the label. The seam that makes it testable was already there -
            # `read(opener=...)` - and was used by nobody.
            wire = b"HEAD\n" + b"z" * 300 + b"\nthe payload sentence that only exists on the wire"

            class _FakeResp:
                status = 200

                def __init__(self, data):
                    self._d = data

                def read(self, n=None):
                    return self._d if n is None else self._d[:n]

                def __enter__(self):
                    return self

                def __exit__(self, *a):
                    return False

            class _FakeOpener:
                def __init__(self, data):
                    self.data = data

                def open(self, req, timeout=None):
                    return _FakeResp(self.data)

            got, rr = read("https://example.invalid/wire", opener=_FakeOpener(wire),
                           run="RUN1", src="dispatch", tool="web_fetch")
            chk("read() returns the wire bytes unmodified", got == wire)
            chk("read() hashes THE WIRE, not a summary",
                rr["sha256"] == hashlib.sha256(wire).hexdigest())
            chk("read() records provenance", rr["src"] == "dispatch" and rr["tool"] == "web_fetch")
            chk("read() stores the artefact under that digest", verify(rr)[0])
            chk("a quote from deep in the wire resolves",
                quotes(rr, "the payload sentence that only exists on the wire")[0])

            # POSITIVE CONTROL ON THE DEFECT CLASS ITSELF: an implementation that hashes what the
            # CALLER would show instead of what arrived must be caught. This is the exact mutation
            # the adversarial pass used, and it must now fail.
            summary = wire[:64]
            fake_row = store(summary, "https://example.invalid/wire", run="RUN1", src="dispatch")
            chk("CONTROL hashing a truncated summary is NOT the wire digest",
                fake_row["sha256"] != rr["sha256"])
            chk("CONTROL the summary cannot serve the wire's quote",
                not quotes(fake_row, "the payload sentence that only exists on the wire")[0])

            # A READ THAT FAILS AT THE SOCKET STILL LEAVES A ROW.
            class _DeadOpener:
                def open(self, req, timeout=None):
                    raise OSError("connection refused")

            before = len(rows())
            try:
                read("https://example.invalid/dead2", opener=_DeadOpener(), src="dispatch")
            except OSError:
                pass
            chk("a socket failure inside read() leaves a row", len(rows()) == before + 1)

            # --- the controls. Each one must say NO. ---
            chk("CONTROL a fabricated quote is refused",
                not quotes(r1, "and then the fox explained its reasoning at some length")[0])
            chk("CONTROL a too-short quote is refused", not quotes(r1, "the fox jumped")[0])
            chk("CONTROL a citation from another run does not resolve",
                resolve(r2["id"], among=[r1]) is None)
            chk("CONTROL an unknown citation does not resolve",
                resolve("0" * 16, among=[r1, r2]) is None)

            # PROVENANCE CONTROL: bytes from an address the MODEL wrote are stored and are NOT
            # citable. Without this, `web_fetch`/`json_get` launder a model-chosen URL into evidence.
            mine = store(b"bytes fetched from an address the model composed, at length",
                         "https://whatever.invalid/x", run="RUN1", src="tool", tool="web_fetch")
            chk("CONTROL a model-addressed read is stored", verify(mine)[0])
            chk("CONTROL a model-addressed read is NOT citable",
                resolve(mine["id"], among=[mine]) is None)
            chk("...and it resolves only when provenance is waived",
                resolve(mine["id"], among=[mine], require_citable=False) is not None)
            try:
                resolve(r1["id"])
                unscoped_ok = False
            except ValueError:
                unscoped_ok = True
            chk("CONTROL resolve() refuses an unscoped citation", unscoped_ok)

            with open(_blob(r1["sha256"]), "wb") as f:      # tamper
                f.write(body + b" plus a sentence nobody fetched")
            ok, why = verify(r1)
            chk("CONTROL an altered artefact fails verification", not ok, why)
            chk("CONTROL a quote against an altered artefact is refused", not quotes(r1, long_q)[0])
            os.remove(_blob(r1["sha256"]))
            chk("CONTROL a missing artefact fails verification", not verify(r1)[0])

            note_failure("https://example.invalid/dead", "HTTPError: 504", run="RUN1",
                         src="dispatch")
            fr = [r for r in rows() if str(r.get("note", "")).startswith("HTTPError")]
            chk("a failed read leaves a row", len(fr) == 1)
            # THE VACUOUS CONTROL, FIXED. It used to call `resolve("")`, which returns None on the
            # empty string BEFORE the pool is read - so it passed against an empty pool and tested
            # nothing. Cite the failure row by the id of a REAL artefact and confirm the pool of
            # failure rows cannot serve it.
            chk("a failure row is not citable", resolve(r2["id"], among=fr) is None)

            capped = store(b"x" * 10, "https://example.invalid/c", truncated=True,
                           note="read capped at 10 bytes", src="dispatch")
            chk("a cap is recorded, never silent", capped["truncated"] and "capped" in capped["note"])

            # THE RACE, reproduced 5 of 5 by the adversarial pass: concurrent stores of identical
            # bytes shared one `.part` file and died on os.replace. `_web_search` fans out four
            # concurrent reads, so this is the live path.
            payload, errs = b"y" * 200_000, []

            def _hammer():
                try:
                    store(payload, "https://example.invalid/race", src="dispatch")
                except Exception as e:
                    errs.append("%s: %s" % (type(e).__name__, str(e)[:60]))

            ts = [threading.Thread(target=_hammer) for _ in range(4)]
            [t.start() for t in ts]
            [t.join() for t in ts]
            chk("CONTROL concurrent identical stores do not race", not errs, "; ".join(errs[:2]))
        finally:
            for k, v in (("AEA_ARTEFACT_DIR", old_d), ("AEA_ARTEFACT_LEDGER", old_l)):
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
    return out


if __name__ == "__main__":
    if "--json" in sys.argv:
        print(json.dumps(dict(stats=stats(),
                              selftest=[dict(check=n, ok=o, detail=d) for n, o, d in selftest()]),
                         indent=1))
        sys.exit(0)
    print("=" * 92)
    print("ARTEFACTS - R5's bound. One read, hashed where the bytes arrive.")
    print("=" * 92)
    s = stats()
    print("  rows %(rows)d   with bytes %(reads_with_bytes)d   failed %(failed_reads)d   "
          "distinct %(distinct_artefacts)d   on disk %(on_disk)d   %(total_bytes)d bytes" % s)
    print()
    res = selftest()
    for n, ok, d in res:
        print("  %-52s %s%s" % (n, "ok" if ok else "FAIL", ("   " + d) if d and not ok else ""))
    bad = [n for n, ok, _ in res if not ok]
    print()
    print("  %d of %d checks pass%s" % (len(res) - len(bad), len(res),
                                        "" if not bad else "   FAILING: " + ", ".join(bad)))
    sys.exit(1 if bad else 0)
