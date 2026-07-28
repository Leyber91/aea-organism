"""A second call on the same fuel, looking at the first one's answer. The first stage that costs."""
from __future__ import annotations

from aea.lab import overseer as OV
from aea.lab.parts.base import Part, template, variant_of
from aea.lab.parts.read import read_work, stated


class Critic(Part):
    """Upside bounded at +0.12, inside the band. Losses to -0.55, all on high baselines.
    Seat when stuck, remove when not: it breaks what was already right."""

    key, stage, order = "critic", "repair", 1
    kind, metric, requires = "lever", "accuracy", ("call",)

    def run(self, ctx):
        v = ctx.cfg("critic", "variant") or variant_of("critic")
        p = template("critic", v).format(prompt=ctx.prompt, text=ctx.text or "(none)")
        r = ctx.fuel.call(ctx.rod, [{"role": "user", "content": p}],
                          max_tokens=ctx.max_tokens, temperature=ctx.temperature)
        seen = OV.inspect(r, max_tokens=ctx.max_tokens, prompt=p)
        if not r.get("ok"):
            ctx.note(critic_error=r.get("error"))
            ctx.flags.append("call_failed")
            return
        before = ctx.answer
        text = seen["text"] or ""
        # Flags describe the reply the organism produced. Unioning both calls' flags discarded 75%
        # of critic trials and removed exactly the messy first answers a critic exists for.
        ctx.flags = list(seen["flags"])
        ctx.tok_out += r.get("tokens") or 0
        ctx.tok_in += r.get("prompt_tokens") or 0
        val = stated(text)
        if val is None:
            val = read_work(text)[0]
        ctx.claim("critic", val, "critic")
        ctx.note(repaired=val != before, tok_out_critic=r.get("tokens"), raw_critic=text[-320:])
