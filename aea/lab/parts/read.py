"""Parts that turn a reply into an answer. Both sit at the READ stage and the ORDER between them
is the seam that cost 18 points in x16: a guard's abstention must END the read, not hand it on."""
from __future__ import annotations

import re

from aea.lab.parts.base import Part

# The readout speaks three dialects. It spoke one until 2026-07-26 and was scored inert on a battery
# it was simply blind to: counting work is a numbered list, algebra is not.
_ENUM = re.compile(r"(?m)^\s*(\d{1,3})[.)]\s+\S")
_SOLVE = re.compile(r"(?m)^\s*\?\[?\s*([a-zA-Z])\s*=\s*(-?\d{1,6})")
_TOTAL = re.compile(r"(?i)\b(?:total|sum|answer|result)\b\D{0,18}?(-?\d{1,6})")
_NUM = re.compile(r"(?<![\d.])(-?\d{1,5})(?![\d.])")


def read_work(text):
    """The answer as the WORK gives it. A solved variable or a labelled total is terminal;
    an enumeration index is only the result when the task was a count."""
    t = text or ""
    m = list(_SOLVE.finditer(t))
    if m:
        return int(m[-1].group(2)), "solved"
    m = list(_TOTAL.finditer(t))
    if m:
        return int(m[-1].group(1)), "total"
    idx = [int(x.group(1)) for x in _ENUM.finditer(t)]
    return (max(idx), "enumerated") if idx else (None, None)


def stated(text):
    n = _NUM.findall((text or "").replace(",", ""))
    return int(n[-1]) if n else None


class Validation(Part):
    """A guard. It converts a silent commitment into a visible abstention, which is the job.
    Scored on accuracy it looks harmful; that is a category error, not a finding."""

    key, stage, order = "validation", "read", 2
    kind, metric, requires = "guard", "false_commitment_rate", ("call",)

    def run(self, ctx):
        t = (ctx.text or "").strip()
        nums = _NUM.findall(t.replace(",", ""))
        bare = re.fullmatch(r"[^\d]{0,24}?(-?\d{1,5})[^\d]{0,24}", t)
        if bare:
            ctx.answer, ctx.read_by = int(bare.group(1)), "stated"
        elif len(set(nums)) != 1:
            m = re.search(r"(?:answer|result|total|is)\D{0,12}(-?\d{1,5})\s*$", t, re.I)
            if m:
                ctx.answer, ctx.read_by = int(m.group(1)), "stated"
            else:
                ctx.answer, ctx.read_by, ctx.declined = None, "declined", True


class Readout(Part):
    """A lever. It recovers an answer the mouth got wrong, and only where no frame was seated:
    a method frame takes muteness from 28/288 to 0/360, so the frame preempts it."""

    key, stage, order = "readout", "read", 1
    kind, metric, requires = "lever", "accuracy", ("call",)

    def run(self, ctx):
        if ctx.answer is not None or ctx.declined:
            return
        val, dialect = read_work(ctx.text)
        if val is not None:
            ctx.answer, ctx.read_by = val, "work:" + dialect
