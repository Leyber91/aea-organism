"""Parts that build the prompt. They run before anything is sent."""
from __future__ import annotations

from aea.lab.parts.base import Part


class Goal(Part):
    key, stage, order = "goal", "shape", 1
    kind, metric, requires = "lever", "accuracy", ("call",)

    def run(self, ctx):
        ctx.prompt = "%s\n%s" % (ctx.task["goal"], ctx.prompt)


class Frame(Part):
    """A METHOD frame prepends a procedure. A MANNER frame prepends a bearing and is the poison."""

    key, stage, order = "frame", "shape", 2
    kind, metric, requires = "lever", "accuracy", ("call",)

    MANNER = "You are on the bench. Answer exactly and only what is asked."

    def run(self, ctx):
        if ctx.cfg("frame", "names") == "manner":
            ctx.prompt = "%s\n\n%s" % (self.MANNER, ctx.prompt)
            ctx.note(frame_names="manner")
        else:
            ctx.prompt = "%s\n\n%s" % (ctx.task["method"], ctx.prompt)
            ctx.note(frame_names="method")
