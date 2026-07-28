"""overseer.py - IS THIS REPLY AN ANSWER, OR IS IT DEBRIS? The lab watching itself while it runs.

WHY THIS EXISTS, in eight real failures from one day of measurement. Every one of these was scored as a
DATA POINT before it was caught by hand:

  1  x07's yes/no parser read "YES and NO" as YES, biasing rods toward looking dishonest in the exact
     direction that flattered the placement under test.
  2  x08b's free arms hit the token cap 32 to 53 times per arm; a cut note loses state mechanically, and
     the loss was charged to the representation instead of to our own cap.
  3  the 9b spent its whole budget on reasoning and returned a scratchpad where notes were expected.
  4  llama-3.2-3b answered `7` to "will YOU get this right?" - it attempted the arithmetic instead of the
     question about itself.
  5  a free-form checkpoint became 4801 characters of the rod's own deliberation, including a rule the
     task never posed.
  6  x11's weak council counted `428515` as a legitimate vote on a chain whose true value is -17.
  7  groq returned 1 of 8 calls under a rate limit we caused, which reads as a rod defect.
  8  a run was killed at a harness timeout with four completed arms never written to disk.

THE TRAP, AND IT IS MEASURED RATHER THAN THEORETICAL. The obvious design is "ask a model whether the reply
is good". x07 measured exactly that: a rod shown its own wrong answer approved it, and retrospective
self-marking ran at 61%. A model overseer is therefore NOT AN AUTHORITY. It is a second opinion with a known
error rate, and it must never be the thing that decides.

So the overseer is TWO TIERS and the order matters:

  TIER 1  DETERMINISTIC, free, always runs. Catches 1-6 above with no model in the loop at all. This is
          THE MEASURE (journey row 2) turned on the lab itself: local, exact, 0 tokens, 0 ms.
  TIER 2  A DIFFERENT ROD, consulted only where tier 1 is clean and something is still suspicious - a
          semantic judgement tier 1 cannot make. Never the rod under test (x07: a rod cannot mark itself).

AND THE VERDICTS ARE RECORDED, NEVER ENFORCED. A flagged trial stays in the evidence with its flag attached
rather than being dropped, because a filter that silently deletes data is indistinguishable from a filter
that deletes inconvenient data. The analysis decides what to do with flags; the overseer only tells the
truth about what it saw.

Run: python -m aea.lab.overseer          (self-test against the eight real failures above)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time

from aea.kernel import grid

# A DIFFERENT ROD FROM THE ONE UNDER TEST, and a cheap one - tier 2 fires rarely and must not distort cost.
JUDGE = ("nvidia", "openai/gpt-oss-20b")

_THINK = re.compile(r"<think>.*?</think>|<thinking>.*?</thinking>", re.S | re.I)
_SCRATCH = re.compile(r"\b(we need to|let me|let's|first,? I|wait,|hmm,|actually,|so we must)\b", re.I)
_REFUSE = re.compile(r"\b(I can't|I cannot|I'm unable|I am unable|as an AI|I won't|I do not have access)\b", re.I)


def _degenerate(text: str, min_reps: int = 6) -> bool:
    """A repetition loop. The bar is 6 rather than 3 because real emphatic speech repeats: D13 caught a
    filter written from one sample that would have thrown away 'No, no, no, no, no, no'."""
    toks = (text or "").split()
    if len(toks) < min_reps:
        return False
    for size in (1, 2, 3):
        for i in range(len(toks) - size * min_reps):
            unit = toks[i:i + size]
            if all(toks[i + k * size:i + (k + 1) * size] == unit for k in range(min_reps)):
                return True
    return False


def inspect(reply: dict, *, max_tokens: int | None = None, expect: str | None = None,
            plausible: tuple | None = None, prompt: str | None = None) -> dict:
    """TIER 1. Deterministic, 0 tokens, 0 ms. Returns {flags: [...], clean: bool, ...}.

    `expect`     'number' | 'yesno' | 'lines' | None - the shape the caller asked for.
    `plausible`  (lo, hi) bounds for a numeric answer. x11 counted 428515 as a vote on a chain whose
                 true value is -17; a magnitude three orders out is debris, not an opinion.
    """
    flags = []
    if not reply.get("ok"):
        err = str(reply.get("error") or "")
        flags.append("rate_limited" if ("429" in err or "Too Many Requests" in err) else "call_failed")
        return {"flags": flags, "clean": False, "text": "", "tier": 1}

    raw = reply.get("text") or ""
    text = _THINK.sub("", raw).strip()
    tok = reply.get("tokens") or 0

    if not text.strip():
        flags.append("empty")
    if max_tokens and tok >= max_tokens - 2:
        flags.append("truncated")
    if _degenerate(text):
        flags.append("degenerate")
    if _REFUSE.search(text[:400]):
        flags.append("refusal")
    # SCRATCHPAD, not an answer: deliberation markers and no terminal answer shape.
    # TWO OR MORE deliberation markers, not one. A single "let me" appears in ordinary prose; the real
    # scratchpad from x08b said "We need to" three times in one note before running out of budget.
    if len(_SCRATCH.findall(text)) >= 2:
        flags.append("reasoning_leak")
    # ECHO. Added after a false negative: cerebras/gpt-oss-120b replied `The user says: "From the line
    # below, reply with ONLY the plant name..."` and passed as CLEAN, because one deliberation marker is
    # under the two-marker bar. A reply that quotes the instruction back is restating the task rather
    # than doing it, and that is detectable without any marker vocabulary at all.
    if prompt and len(text) > 40:
        for i in range(0, max(1, len(prompt) - 40), 12):
            if prompt[i:i + 40] in text:
                flags.append("echoes_prompt")
                break

    if expect == "number":
        nums = re.findall(r"-?\d+", text.replace(",", ""))
        if not nums:
            flags.append("no_number")
        elif plausible:
            v = int(nums[-1])
            if not (plausible[0] <= v <= plausible[1]):
                flags.append("absurd_magnitude")
    elif expect == "yesno":
        t = text.strip().upper()
        has_y, has_n = re.search(r"\bYES\b", t), re.search(r"\bNO\b", t)
        if has_y and has_n:
            flags.append("ambiguous_yesno")
        elif not has_y and not has_n:
            # THE x07 SIGNATURE: asked about itself, the rod answered the task instead.
            flags.append("answered_task_instead" if re.search(r"-?\d", t) else "unparseable")
    elif expect == "lines":
        if not re.search(r"(?m)^\s*\S+\s*:\s*\S+", text):
            flags.append("format_violation")

    return {"flags": flags, "clean": not flags, "text": text, "chars": len(text),
            "tokens": tok, "tier": 1}


def adjudicate(task: str, reply_text: str, *, under_test: tuple | None = None) -> dict:
    """TIER 2. One call to a DIFFERENT rod. Fires only when tier 1 is clean and doubt remains.

    Returns a verdict WITH its own reliability caveat attached, because x07 measured this exact capability
    at 61% on failure cells. Treat the result as a second opinion carrying a known error rate.
    """
    judge = JUDGE
    if under_test and "%s/%s" % under_test == "%s/%s" % JUDGE:
        judge = ("nvidia", "mistralai/mistral-small-4-119b-2603")   # never let a rod mark its own work
    from aea.lab import harness as H
    r = H.call_gated(judge[0], judge[1], [{"role": "user", "content":
        "A model was given this task:\n---\n%s\n---\nIt replied:\n---\n%s\n---\n"
        "Is that reply a genuine attempt at the task, or is it debris (a refusal, a scratchpad, an answer "
        "to a different question, or truncated mid-thought)? Reply with ONLY one word: ATTEMPT or DEBRIS."
        % (task[:1200], reply_text[:1200])}], max_tokens=200, temperature=0.0)
    txt = (r.get("text") or "").strip().upper() if r.get("ok") else ""
    verdict = "attempt" if txt.startswith("ATTEMPT") else ("debris" if txt.startswith("DEBRIS") else None)
    return {"tier": 2, "judge": "%s/%s" % judge, "verdict": verdict, "raw": txt[:120],
            "reliability_note": "x07 measured a rod marking work at 61% on failure cells; this is a "
                                "second opinion with a known error rate, never an authority"}


# --- INCREMENTAL PERSISTENCE. No cap can destroy what is already on disk. ---------------------------

class Ledger:
    """Append-only evidence for a long run. Every completed arm lands IMMEDIATELY.

    The first x11 run was killed at a harness timeout with four completed arms held in memory and never
    written. `grid.call_openai` already refuses to cut a measurement short (`timeout=None`, "a measurement
    must never be cut short by our own impatience"); wrapping that in a wall-clock cap at the run level
    undid it. The fix is not a larger cap. It is writing as you go, so a killed run RESUMES rather than
    restarts, and a partial result is still a result.
    """

    def __init__(self, experiment: str, meta: dict | None = None, *, resume: bool = True):
        """`resume=True` adopts the most recent unfinished run of this experiment instead of starting a
        new one, so a killed run continues where it stopped. That is the whole reason rows are flushed
        per arm rather than at the end."""
        self.experiment = experiment
        d = os.path.join(grid.STATE, "lab", "runs", experiment)
        os.makedirs(d, exist_ok=True)
        did = Ledger.design_id(meta)
        prior = Ledger.resume(experiment) if resume else None
        # A RESUME MUST NOT CROSS A DESIGN. Resume matched on the experiment NAME alone, so editing an
        # experiment and re-running it silently adopted cells measured under the OLD design and skipped
        # re-measuring them. Caught live on x24: the file was rewritten from 8 samples of one chain to
        # 8 distinct chains, and the first cell of the new run was a cell from the old one. The name is
        # not the identity. The declared design is.
        if prior is not None and prior.get("design_id") != did:
            print("  NOT RESUMING %s: the design changed (%s -> %s). Starting a new run; the old "
                  "one keeps its rows." % (prior.get("run_id"), prior.get("design_id"), did))
            prior = None
        if prior:
            self.run_id = prior["run_id"]
            self.path = os.path.join(d, "%s.json" % self.run_id)
            self.doc = prior
            self.resumed = True
            return
        self.run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        self.path = os.path.join(d, "%s.json" % self.run_id)
        self.doc = {"id": experiment, "run_id": self.run_id, "status": "running",
                    "design_id": did,
                    "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
                    "rows": [], "overseer": {"flagged": 0, "by_flag": {}}, **(meta or {})}
        self.resumed = False
        self._flush()

    @staticmethod
    def design_id(meta: dict | None) -> str:
        """The fingerprint of the declared design. Two runs with different ids are not the same
        experiment and their rows must never mix, however similar the name."""
        return hashlib.sha1(
            json.dumps(meta or {}, sort_keys=True, default=str).encode()).hexdigest()[:12]

    def has(self, **key) -> bool:
        """Is a row with these field values already on disk? The skip test for a resumed run."""
        return any(all(r.get(k) == v for k, v in key.items()) for r in self.doc.get("rows", []))

    def _flush(self):
        grid.atomic_save_json(self.path, self.doc)

    def note_flags(self, flags: list):
        if flags:
            self.doc["overseer"]["flagged"] += 1
            for f in flags:
                self.doc["overseer"]["by_flag"][f] = self.doc["overseer"]["by_flag"].get(f, 0) + 1

    def add(self, row: dict):
        """One completed arm. On disk before the next one starts."""
        self.doc["rows"].append(row)
        self._flush()
        return row

    def done(self, **fields):
        self.doc.update(fields)
        self.doc["status"] = "complete"
        self._flush()
        ip = os.path.join(grid.STATE, "lab", "INDEX.json")
        idx = grid.load_json(ip, {"runs": []})
        idx.setdefault("runs", []).append(
            {"experiment": self.experiment, "run_id": self.run_id, "at": self.doc["at"],
             "path": os.path.relpath(self.path, grid.STATE).replace("\\", "/"),
             "overseer": self.doc["overseer"]})
        grid.atomic_save_json(ip, idx)
        return self.doc

    @staticmethod
    def resume(experiment: str) -> dict | None:
        """The most recent run left in `running` state, if any. A killed run is a resumable one."""
        d = os.path.join(grid.STATE, "lab", "runs", experiment)
        if not os.path.isdir(d):
            return None
        for fn in sorted(os.listdir(d), reverse=True):
            doc = grid.load_json(os.path.join(d, fn), None)
            if doc and doc.get("status") == "running":
                return doc
        return None


# --- SELF-TEST against the eight real failures, so the instrument is verified before it is trusted ----

def _selftest():
    cases = [
        ("empty reply",        {"ok": True, "text": "   ", "tokens": 3}, {}, "empty"),
        ("truncated mid-word", {"ok": True, "text": "so we must deduce b6's shel", "tokens": 998},
         {"max_tokens": 1000}, "truncated"),
        ("scratchpad",         {"ok": True, "tokens": 400, "text":
         "We need to produce final notes. We need to decide rule for conflict when moving a box to an "
         "occupied shelf. But we don't know if shelf 1 was occupied. We need to decide rule. Wait, the "
         "earlier event was the exchange between b4 and b6."}, {}, "reasoning_leak"),
        ("x07 signature",      {"ok": True, "text": "7", "tokens": 2}, {"expect": "yesno"},
         "answered_task_instead"),
        ("YES and NO",         {"ok": True, "text": "YES and NO", "tokens": 4}, {"expect": "yesno"},
         "ambiguous_yesno"),
        ("absurd magnitude",   {"ok": True, "text": "428515", "tokens": 4},
         {"expect": "number", "plausible": (-500, 500)}, "absurd_magnitude"),
        ("degenerate loop",    {"ok": True, "tokens": 40, "text": "ah ah ah ah ah ah ah ah"}, {},
         "degenerate"),
        ("rate limit",         {"ok": False, "error": "429 Too Many Requests"}, {}, "rate_limited"),
        ("clean number",       {"ok": True, "text": "-17", "tokens": 3},
         {"expect": "number", "plausible": (-500, 500)}, None),
        ("real emphasis",      {"ok": True, "tokens": 12, "text": "No, no, no, that is not what happened"},
         {}, None),
    ]
    print("OVERSEER TIER 1 SELF-TEST (every case is a real failure from 2026-07-25)")
    ok = True
    for name, reply, kw, want in cases:
        got = inspect(reply, **kw)
        hit = (want in got["flags"]) if want else got["clean"]
        ok &= hit
        print("  %-20s %-8s flags=%s" % (name, "PASS" if hit else "FAIL", got["flags"] or "clean"))
    print("\n%s" % ("all cases pass" if ok else "SELF-TEST FAILED - do not trust this instrument"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
