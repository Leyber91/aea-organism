"""The one part every organism contains. Without it there is nothing to read, repair or judge."""
from __future__ import annotations

import time

from aea.lab import harness as H
from aea.lab import overseer as OV
from aea.lab.parts.base import Part


class Call(Part):
    key, stage, order = "call", "fire", 1
    kind, metric, requires = "enabling", None, ()

    def run(self, ctx):
        carried = ctx.rec.get("carried")
        prompt = "%s\n\n%s" % (carried, ctx.prompt) if carried else ctx.prompt
        t0 = time.time()
        r = H.call_gated(ctx.rod[0], ctx.rod[1], [{"role": "user", "content": prompt}],
                         max_tokens=ctx.max_tokens, temperature=ctx.temperature)
        seen = OV.inspect(r, max_tokens=ctx.max_tokens, prompt=prompt)
        ctx.text = seen["text"] or ""
        ctx.flags = list(seen["flags"])
        ctx.ok = bool(r.get("ok"))
        ctx.tok_out += r.get("tokens") or 0
        ctx.tok_in += r.get("prompt_tokens") or 0
        # Both directions. conversation spends nothing extra on output and everything on input.
        ctx.note(elapsed_s=round(time.time() - t0, 3), prompt_chars=len(prompt),
                 chars=len(ctx.text), tok_out=r.get("tokens"), tok_in=r.get("prompt_tokens"),
                 raw=ctx.text[-320:])
