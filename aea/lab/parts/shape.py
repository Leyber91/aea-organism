"""Parts that build the prompt. They run before anything is sent."""
from __future__ import annotations

from aea.lab.parts.base import Part, template, variant_of


class Goal(Part):
    key, stage, order = "goal", "shape", 1
    kind, metric, requires = "lever", "accuracy", ("call",)

    def run(self, ctx):
        ctx.prompt = "%s\n%s" % (ctx.task["goal"], ctx.prompt)


class Frame(Part):
    """A METHOD frame prepends a procedure. A MANNER frame prepends a bearing and is the poison."""

    key, stage, order = "frame", "shape", 2
    kind, metric, requires = "lever", "accuracy", ("call",)

    def run(self, ctx):
        v = ctx.cfg("frame", "variant") or ctx.cfg("frame", "names") or variant_of("frame")
        ctx.prompt = template("frame", v).format(prompt=ctx.prompt, **ctx.task)
        ctx.note(frame_variant=v)
