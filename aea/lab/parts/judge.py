"""Parts that annotate after the answer exists. Neither changes the answer."""
from __future__ import annotations

from aea.lab.parts.base import Part


class Measure(Part):
    """A gauge. It changes what can be known, not what was answered."""

    key, stage, order = "measure", "judge", 1
    kind, metric, requires = "gauge", "can_know", ("call",)

    def run(self, ctx):
        a, truth = ctx.answer, ctx.task["truth"]
        ctx.verdict = "pass" if a == truth else ("abstain" if a is None else "fail")
        # A verdict with no objective is Arbiter vacui: clean, confident, about nothing.
        ctx.note(verdict_is_empty=not (ctx.has("goal") or ctx.has("frame")))


class Latency(Part):
    """A channel. Requires nothing beneath it and depends on everything."""

    key, stage, order = "latency", "judge", 2
    kind, metric, requires = "channel", "separability", ()

    def run(self, ctx):
        ctx.note(clock=ctx.rec.get("elapsed_s"))
