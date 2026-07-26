"""State that outlives the call. The only part whose unit is a SEQUENCE rather than a trial:
run the same seat twice independently and a part that persists state has nowhere to put anything."""
from __future__ import annotations

import re

from aea.lab.parts.base import Part

FORMS = ("none", "checkpoint", "conversation", "free")

_STATE = re.compile(r"(?im)^\s*STATE:\s*value\s*=\s*(-?\d{1,9})\s*,\s*step\s*=\s*(\d{1,4})")

INSTRUCTION = {
    "none": "",
    "checkpoint": ("\n\nAfter your answer, on a new line, write exactly:\n"
                   "STATE: value=<the current number>, step=<the step number you just completed>"),
    "conversation": "",
    "free": ("\n\nAfter your answer, on a new line beginning NOTE:, write anything you want your "
             "future self to know before the next step."),
}


class Carry(Part):
    """UNMEASURED as of 2026-07-27. x21's no-carry control handed the running value to the baseline,
    so the control contained the treatment and the -0.09 result is void."""

    key, stage, order = "carry", "carry", 1
    kind, metric, requires = "lever", "accuracy_over_sequence", ("call",)

    def run(self, ctx):
        form = ctx.cfg("carry", "form", "checkpoint")
        ctx.note(carry_form=form, carried=self.pack(form, ctx.text, ctx.answer))

    @staticmethod
    def pack(form, text, value):
        """What the next step is given. `none` is deliberately empty: a control that hands the
        running value forward IS a checkpoint, and that is the bug this method exists to prevent."""
        if form == "none":
            return ""
        if form == "checkpoint":
            m = _STATE.search(text or "")
            v = int(m.group(1)) if m else value
            return "The running value is %s." % v
        if form == "free":
            note = (text or "").split("NOTE:", 1)
            body = note[1].strip()[:1200] if len(note) > 1 else "(none)"
            return "The running value is %s.\nYour note to yourself: %s" % (value, body)
        return ""
