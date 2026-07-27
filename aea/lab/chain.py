"""A sequence runner. The unit is a CHAIN of steps, not a trial.

Extracted from organism.py 2026-07-27: a single-trial runner and a sequence runner are different
concerns, and Chain was half the file. Every part that acts BETWEEN calls needs this; nothing that
acts inside one call does.
"""
from __future__ import annotations

import re

from aea.lab.organism import Organism
from aea.lab.parts.carry import FORMS as CARRY_FORMS
from aea.lab.parts.carry import INSTRUCTION, Carry
from aea.lab.parts.read import read_work


def _last_int(text):
    n = re.findall(r"-?\d+", (text or "").replace(",", ""))
    return int(n[-1]) if n else None


class Chain:
    """One organism over a SEQUENCE, carrying state in a stated container.

    THE CONTROL CARRIES NOTHING. x21's `none` arm handed the running value forward, which is a
    checkpoint, so the baseline contained the treatment and its -0.09 was void. Here `none` means
    the rod must hold the value itself.
    """

    # THE GOAL STATES AN OBJECTIVE. THE FRAME STATES A PROCEDURE. The first version of these had the
    # goal say "Reply with ONLY the resulting number", which is a MANNER instruction in the goal slot:
    # it suppressed working to zero, so the frame could not deliver shows_working, the readout had
    # nothing to recover from, and validation had one number and nothing to guard. Three of eight
    # capacities were unmeasurable and x22 was stopped at 6 of 16 cells to fix it.
    STEP_GOAL = "Give the value that results from applying this step."
    STEP_METHOD = ("Take the running value, write it down, apply the single operation named below to "
                   "it, and show that arithmetic. Then give the result on its own final line. Do not "
                   "re-do earlier steps.")

    def __init__(self, rod, form="none", *, start=0, temperature=0.2, max_tokens=800, seat=None):
        """`seat` lets a chain run any assembly, so the ascending series v1..vN can be measured on a
        sequence. Without it the chain seats call + carry only, which is a v2 organism - x21 tested
        World 3's component on a bare call and hand-wrote the shaping the parts were meant to do."""
        assert form in CARRY_FORMS, form
        self.rod, self.form = tuple(rod), form
        self.start, self.temperature, self.max_tokens = start, temperature, max_tokens
        keys = list(seat) if seat else (["call"] + (["carry"] if form != "none" else []))
        if form != "none" and "carry" not in keys:
            keys.append("carry")
        self.org = Organism(keys, rod, label="chain:%s:%s" % ("+".join(keys), form),
                            config={"carry": {"form": form}})
        self.seat = self.org.keys

    def run(self, ops, truth_fn):
        rec = {"rod": "%s/%s" % self.rod, "form": self.form, "steps": len(ops),
               "temperature": self.temperature, "trace": [], "flags": []}
        history, value, carried = [], self.start, ""
        for i, op in enumerate(ops):
            prev_value = value
            # The parts do the shaping. Goal and Frame prepend their own text, so v2 and v3 differ
            # from v1 by what they SEAT rather than by what the harness writes into the string.
            task = {"id": "chain", "truth": truth_fn(i + 1),
                    "data": self._body(i, op, value, carried, history),
                    "goal": self.STEP_GOAL, "method": self.STEP_METHOD}
            r = self.org.run(task, temperature=self.temperature, max_tokens=self.max_tokens,
                             carried=carried if "carry" in self.seat else "")
            # A carrier quotes what it carries: echoes_prompt is this part's signature, not debris.
            flags = [f for f in r["flags"] if f != "echoes_prompt"]
            if not r["ok"]:
                rec["flags"].append("call_failed")
                rec["trace"].append({"step": i + 1, "ok": False})
                break
            text = r.get("text") or r.get("raw") or ""
            value = r["answer"] if r["answer"] is not None else Carry.extract(self.form, text, value)
            carried = Carry.pack(self.form, text, value)
            if self.form == "conversation":
                history = history + [{"role": "user", "content": task["data"]},
                                     {"role": "assistant", "content": text[:2000]}]
            # The capacity fields. A part adds a CAPACITY, not accuracy, so the trace has to record
            # what became possible at this step and not only whether the number was right.
            rb = r.get("read_by") or "none"
            rec["trace"].append({"step": i + 1, "ok": True, "value": value,
                                 "truth": truth_fn(i + 1), "hit": value == truth_fn(i + 1),
                                 "showed_work": read_work(text)[0] is not None,
                                 # ON_TASK: did it APPLY the operation, or hand back what it was
                                 # given? Orthogonal to length, unlike the <400-char proxy it replaces.
                                 "on_task": value is not None and value != prev_value,
                                 "from_work": rb.startswith("work:"),
                                 "declined": rb == "declined",
                                 "repaired": bool(r.get("repaired")),
                                 "read_by": rb,
                                 "tok_out": r.get("tok_out"), "tok_in": r.get("tok_in"),
                                 "chars": r.get("chars"), "carried_chars": len(carried),
                                 "flags": flags})
            rec["flags"] += flags

        t = [s for s in rec["trace"] if s.get("ok")]
        rec["completed"] = len(t)
        rec["final"] = t[-1]["value"] if t else None
        rec["final_truth"] = truth_fn(len(ops))
        rec["correct"] = bool(t) and t[-1]["step"] == len(ops) and t[-1]["hit"]
        rec["first_miss"] = next((s["step"] for s in t if not s["hit"]), None)
        rec["hits"] = sum(1 for s in t if s["hit"])
        rec["tok_out"] = sum(s.get("tok_out") or 0 for s in t)
        rec["tok_in"] = sum(s.get("tok_in") or 0 for s in t)
        rec["tok_total"] = rec["tok_out"] + rec["tok_in"]
        rec["carried_max"] = max([s["carried_chars"] for s in t] or [0])
        return rec

    def _body(self, i, op, value, carried, history):
        """Step 1 states the starting value; that is the TASK, not the carry. After that `none`
        gives nothing back and the rod must hold it. Removing the start from step 1 as well made
        every arm fail at step 1 on 48371 + 6 - a control broken in the opposite direction."""
        head = "You are continuing a calculation, one step at a time."
        opening = "The starting value is %s.\n\n" % self.start if i == 0 else ""
        if self.form == "conversation":
            return "%sStep %d: %s" % (opening, i + 1, op)
        # `carried` is prepended by the Call part, not here, so a seat without `carry` gets nothing.
        return "%s\n\n%sStep %d: %s%s" % (head, opening, i + 1, op, INSTRUCTION[self.form])
