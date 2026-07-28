"""The one part every organism contains. Without it there is nothing to read, repair or judge."""
from __future__ import annotations

import time

from aea.lab import overseer as OV
from aea.lab.parts.base import Part
from aea.lab.parts.read import stated


class Call(Part):
    key, stage, order = "call", "fire", 1
    kind, metric, requires = "enabling", None, ()

    def run(self, ctx):
        carried = ctx.rec.get("carried")
        prompt = "%s\n\n%s" % (carried, ctx.prompt) if carried else ctx.prompt
        # PRIOR TURNS GO ON THE WIRE. A carried string and a message history are two different
        # containers and this part now sends both; sending only the first is defect 13.
        msgs = ctx.history + [{"role": "user", "content": prompt}]
        t0 = time.time()
        r = ctx.fuel.call(ctx.rod, msgs, max_tokens=ctx.max_tokens, temperature=ctx.temperature)
        seen = OV.inspect(r, max_tokens=ctx.max_tokens, prompt=prompt)
        ctx.text = seen["text"] or ""
        ctx.flags = list(seen["flags"])
        ctx.ok = bool(r.get("ok"))
        ctx.tok_out += r.get("tokens") or 0
        ctx.tok_in += r.get("prompt_tokens") or 0
        # Both directions. conversation spends nothing extra on output and everything on input.
        # THE NAIVE READ. A bare call's capacity IS that a value comes back, so the stated number is
        # extracted here and read parts refine it. Moving this into Validation during the parts
        # refactor meant an organism with no guard read NOTHING - a silent capability loss that no
        # import check could see. The Addition Law, broken on our own code.
        ctx.claim("call", stated(ctx.text), "stated")
        # THE WHOLE REPLY. `raw` was ctx.text[-320:] and that single slice is the root of four
        # recorded defects: it erased a creature (defect 5, 74% of replies were longer), it made
        # every chain body-read a tail read (defect 14), and it silently collapses distinctness
        # counts - two replies differing only in their opening are counted as one, which is how
        # x09, x10, x12 and x19 all measure `distinct_replies`. A stored reply is the only thing
        # that makes a run re-scorable; storing a slice of it is storing a guess.
        ctx.note(elapsed_s=round(time.time() - t0, 3), prompt_chars=len(prompt),
                 chars=len(ctx.text), tok_out=r.get("tokens"), tok_in=r.get("prompt_tokens"),
                 raw=ctx.text)
