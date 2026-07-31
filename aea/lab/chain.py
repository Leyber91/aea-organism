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

    def __init__(self, rod, form="none", *, start=0, temperature=0.2, max_tokens=800, seat=None,
                 notes=None, method=None):
        """`seat` lets a chain run any assembly, so the ascending series v1..vN can be measured on a
        sequence. Without it the chain seats call + carry only, which is a v2 organism - x21 tested
        World 3's component on a bare call and hand-wrote the shaping the parts were meant to do."""
        assert form in CARRY_FORMS, form
        self.rod, self.form = tuple(rod), form
        self.start, self.temperature, self.max_tokens = start, temperature, max_tokens
        self.history, self.carried = [], ""
        # PER-STEP EXTRA TEXT, keyed by 1-based step. Built for carrying a NON-RECOMPUTABLE token: a
        # probe about a numeric value can always be answered by doing the arithmetic again, so a
        # value probe cannot separate retrieval from recomputation on its own. A random token can
        # only be reproduced by having kept it.
        self.notes = dict(notes or {})
        if method:
            self.STEP_METHOD = method
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
            # THE HISTORY IS THE CONTAINER for `conversation`, so it goes on the wire. It was built
            # here and dropped for the whole life of the container (defect 13), which starved the arm
            # and produced the only "conversation" finding in the project.
            # keep_full=True OR EVERY READ BELOW IS A TAIL READ. `Organism.run` sets rec["text"]
            # only under this flag, so `r.get("text") or r.get("raw")` fell through to `raw`, which
            # fire.py defines as ctx.text[-320:]. read_work() then judged whether the reply showed
            # its working from the last 320 characters of a reply the frame exists to make longer.
            r = self.org.run(task, temperature=self.temperature, max_tokens=self.max_tokens,
                             carried=carried if "carry" in self.seat else "", keep_full=True,
                             history=history if self.form == "conversation" else None)
            # A carrier quotes what it carries: echoes_prompt is this part's signature, not debris.
            flags = [f for f in r["flags"] if f != "echoes_prompt"]
            if not r["ok"]:
                rec["flags"].append("call_failed")
                rec["trace"].append({"step": i + 1, "ok": False})
                break
            text = r.get("text") or r.get("raw") or ""
            # THE CARRY VARIANT WINS THE READ when its instruction appends a number after the
            # answer. `checkpoint` ends "STATE: value=48379, step=1" and `free` ends with a note, so
            # the naive last-number read returns the STEP INDEX. That regression scored three whole
            # rods at 0.00 solo in x23b and read as "the task is too hard for this fleet".
            if self.form in ("checkpoint", "free"):
                value = Carry.extract(self.form, text, r["answer"])
            else:
                value = r["answer"] if r["answer"] is not None else Carry.extract(self.form, text, value)
            carried = Carry.pack(self.form, text, value)
            if self.form == "conversation":
                history = history + [{"role": "user", "content": task["data"]},
                                     {"role": "assistant", "content": text}]
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
                                 # THE WHOLE REPLY, SO A READ CAN BE REVISED AT ZERO COST. The row
                                 # stored `chars` and no text, so every value here was final: a
                                 # defect found later in read.py or Carry.extract could not be
                                 # re-scored off disk and the run had to be re-bought. That is the
                                 # same mistake as storing text[:400] in the harness, one layer down.
                                 "text": text,
                                 "tok_out": r.get("tok_out"), "tok_in": r.get("tok_in"),
                                 "chars": r.get("chars"), "carried_chars": len(carried),
                                 # WHAT THE CONTAINER ACTUALLY WEIGHS. `carried` is empty for
                                 # `conversation` because its state is messages, not a string, so
                                 # carried_chars alone prices the largest container at zero.
                                 "context_chars": len(carried) + sum(len(m["content"])
                                                                     for m in history),
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
        rec["context_max"] = max([s["context_chars"] for s in t] or [0])
        self.history, self.carried = history, carried
        return rec

    # THE PROBE. Retrieval is a different capability from storage, and nothing in this lab has ever
    # measured it: every metric so far asks whether the CURRENT value survived, never whether an
    # EARLIER one can be reached. A container holds sixteen exchanges; the question is whether the
    # organism can produce one of them on request.
    PROBE = ("Earlier in this task you completed step %d. State the value you gave as the result of "
             "step %d. Do not recalculate and do not explain. Reply with only that number.")

    def ask(self, question, *, goal="State a thing you were given earlier.", label="probe"):
        """One question put to the finished organism, forked from its stored state.

        FORKED, NEVER APPENDED. Each question sees exactly the history the chain ended with and
        nothing else, so N questions are N independent questions rather than a conversation the
        organism is having with its own answers. That also removes question ORDER as a variable:
        there is no order, because no question can see another.
        """
        task = {"id": label, "truth": None, "data": question, "goal": goal, "method": ""}
        r = self.org.run(task, temperature=self.temperature, max_tokens=self.max_tokens,
                         carried=self.carried if "carry" in self.seat else "", keep_full=True,
                         history=list(self.history) if self.form == "conversation" else None)
        text = (r.get("text") or "") if r.get("ok") else ""
        return {"ok": bool(r.get("ok")), "text": text, "last": _last_int(text),
                "answer": r.get("answer"),
                "tok_in": r.get("tok_in"), "tok_out": r.get("tok_out")}

    def probe(self, step):
        """Ask for a value already produced. Forked from the stored history, never appended to it,
        so three probes are three independent questions rather than a conversation about itself.

        EVERY CONTAINER BRINGS WHAT IT HAS. `checkpoint` and `free` hand over their final carried
        string and `conversation` hands over the whole history, because the question is not whether
        the probe is answerable in the abstract - it is whether THIS container put the answer
        somewhere reachable. A checkpoint holding only the current value should fail, and it should
        fail holding its real contents rather than holding nothing.
        """
        task = {"id": "probe", "truth": None, "data": self.PROBE % (step, step),
                "goal": "State a value you produced earlier.", "method": ""}
        r = self.org.run(task, temperature=self.temperature, max_tokens=self.max_tokens,
                         carried=self.carried if "carry" in self.seat else "", keep_full=True,
                         history=list(self.history) if self.form == "conversation" else None)
        text = (r.get("text") or r.get("raw") or "") if r.get("ok") else ""
        return {"step": step, "ok": bool(r.get("ok")), "text": text,
                "last": _last_int(text), "answer": r.get("answer"),
                "tok_in": r.get("tok_in"), "tok_out": r.get("tok_out")}

    def _body(self, i, op, value, carried, history):
        """Step 1 states the starting value; that is the TASK, not the carry. After that `none`
        gives nothing back and the rod must hold it. Removing the start from step 1 as well made
        every arm fail at step 1 on 48371 + 6 - a control broken in the opposite direction."""
        head = "You are continuing a calculation, one step at a time."
        opening = "The starting value is %s.\n\n" % self.start if i == 0 else ""
        if self.form == "conversation":
            # THE HEAD BELONGS TO EVERY ARM. It was omitted here entirely, so the conversation arm
            # was framed differently from the other three in addition to its container - two
            # variables at once. It goes in the first turn only, because the history carries it
            # forward from there; that difference IS the container and not a confound.
            extra = self.notes.get(i + 1, "")
            return "%s\n\n%sStep %d: %s%s" % (head, opening, i + 1, op, extra) if i == 0 \
                else "Step %d: %s%s" % (i + 1, op, extra)
        # `carried` is prepended by the Call part, not here, so a seat without `carry` gets nothing.
        return "%s\n\n%sStep %d: %s%s%s" % (head, opening, i + 1, op, self.notes.get(i + 1, ""),
                                            INSTRUCTION[self.form])
