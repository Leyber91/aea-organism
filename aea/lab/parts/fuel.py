"""FUEL IS A COMPONENT, so it is seated rather than imported.

Law IV says the same seat on different fuel is a different organism. The code did not believe that:
fire.py called the live harness directly, so fuel was welded into the part instead of handed to it.
That made every test hit the network and made a recorded or scripted rod impossible.

Three fuels, one interface. A creature does not know which it is running on.
"""
from __future__ import annotations


class Fuel:
    kind = "abstract"

    def call(self, rod, messages, *, max_tokens, temperature):
        raise NotImplementedError


class LiveFuel(Fuel):
    """The real wire. The default, and the only one that spends anything."""

    kind = "live"

    def call(self, rod, messages, *, max_tokens, temperature):
        from aea.lab import harness as H
        return H.call_gated(rod[0], rod[1], messages,
                            max_tokens=max_tokens, temperature=temperature)


class ScriptedFuel(Fuel):
    """Replies handed in, in order. For tests: no network, no cost, exactly reproducible."""

    kind = "scripted"

    def __init__(self, replies, tokens=8):
        self.replies, self.tokens, self.seen = list(replies), tokens, []
        # THE WHOLE REQUEST, not only its last turn. A container whose state is message history is
        # invisible to a recorder that keeps one string, which is how defect 13 survived a test file
        # written to catch exactly this class of fault.
        self.sent = []

    def call(self, rod, messages, *, max_tokens, temperature):
        self.sent.append([dict(m) for m in messages])
        self.seen.append(messages[-1]["content"])
        text = self.replies[len(self.seen) - 1] if len(self.seen) <= len(self.replies) else ""
        return {"ok": True, "text": text, "tokens": self.tokens,
                "prompt_tokens": len(messages[-1]["content"]) // 4}


class ReplayFuel(Fuel):
    """Replies from a stored run. Re-score an experiment without spending a call - which is how the
    readout was taught two dialects and both batteries re-scored at zero cost."""

    kind = "replay"

    def __init__(self, texts):
        self.texts, self.i = list(texts), 0

    def call(self, rod, messages, *, max_tokens, temperature):
        t = self.texts[self.i] if self.i < len(self.texts) else ""
        self.i += 1
        return {"ok": True, "text": t, "tokens": 0, "prompt_tokens": 0}


DEFAULT = LiveFuel()
