"""fuel.py - THE UNIT SYSTEM. No measurement exists without the fuel it was taken on.

Luis, 2026-07-25: "the whole autonomous entity architecture needs to be adapted to the size and
thinking capability of the fuel" -> and then, decisively: "they will always be present."

He is right, and it is a structural claim rather than an editorial one. A capability score is not a
property of a module; it is a property of a MODULE-ON-A-FUEL pairing. The same composition measured
on two rods is two different organisms:

    Arbiter imperans on groq/llama-3.3-70b      repaired 6 of 6
    Arbiter imperans on nvidia/nemotron-9b      repaired 0 - no repair at all

Same genome. One closes C-50; the other does not. So "the AEA is 60% complete" is a sentence with no
meaning, in the same way "the rod is 4 long" has no meaning. Completion is always completion ON A
STATED FUEL, and the final gate C-64 can only ever be claimed as "sustained unattended operation, on
this fuel."

This module makes the stamp mandatory. `require()` refuses a result that does not carry one - the same
discipline axes.raise_axis() applies to receipts. A number without its units is not a weaker finding,
it is not a finding.

WHAT IS TAMED AND WHAT IS NOT (2026-07-25):
  tamed        rod · provider · n · max_tokens · latency · reliability (failures/attempts)
  KNOWN, UNSET temperature - every measurement so far was taken at 0.2 and never varied. The variance
               attributed to noise in chapter I is partly unmeasured sampling.
  UNTAMED      thinking mode - setting it by system prompt produced IDENTICAL output and IDENTICAL
               token counts (3245 both ways on nemotron-9b). The instruction was ignored; the real
               control is an API parameter we have not found.
  UNMEASURED   context window · build family as a variable in its own right
"""
from __future__ import annotations

import os
import time

from aea.kernel import grid

# the fuels actually used this session, with what is known about each. `size` is the vendor's own
# parameter count where the name states it; None where the name does not say and we did not verify.
KNOWN = {
    "nvidia/meta/llama-3.2-1b-instruct":        dict(provider="nvidia", size="1b",   family="llama"),
    "nvidia/meta/llama-3.2-3b-instruct":        dict(provider="nvidia", size="3b",   family="llama"),
    "nvidia/nvidia/nvidia-nemotron-nano-9b-v2": dict(provider="nvidia", size="9b",   family="nemotron"),
    "nvidia/openai/gpt-oss-20b":                dict(provider="nvidia", size="20b",  family="gpt-oss"),
    "nvidia/meta/llama-3.3-70b-instruct":       dict(provider="nvidia", size="70b",  family="llama"),
    "nvidia/nvidia/nemotron-3-super-120b-a12b": dict(provider="nvidia", size="120b", family="nemotron"),
    "groq/llama-3.3-70b-versatile":             dict(provider="groq",   size="70b",  family="llama"),
    "nvidia/mistralai/mistral-small-4-119b-2603": dict(provider="nvidia", size="119b", family="mistral"),
    "ollama/qwen2.5:7b":                        dict(provider="ollama", size="7b",   family="qwen"),
    # THE BIG RODS, probed reachable 2026-07-25. The two nemotrons emitted REASONING as their visible
    # text at max_tokens=12 ("The user wants...") - they are chain-of-thought rods, so any measurement
    # on them needs a much larger token budget and a check that survives a long preamble. This is the
    # `thinking` variable appearing as a property of the FUEL rather than a setting we choose.
    "nvidia/nvidia/nemotron-3-ultra-550b-a55b": dict(provider="nvidia", size="550b", family="nemotron",
                                                    reasoning=True),
    "nvidia/nvidia/nemotron-3-super-120b-a12b": dict(provider="nvidia", size="120b", family="nemotron",
                                                    reasoning=True),
}

# probed reachable but too slow for an n=8 sweep, and the reason is recorded rather than the rod being
# quietly dropped: deepseek-v4-pro 31.1s, minimax-m3 12.7s, nemotron-super-49b 30.8s for one 12-token
# reply. Any of them costs more wall clock than the other eight rods combined.
TOO_SLOW = {
    "nvidia/deepseek-ai/deepseek-v4-pro": "31140ms for a 12-token reply",
    "nvidia/minimaxai/minimax-m3": "12730ms",
    "nvidia/nvidia/llama-3.3-nemotron-super-49b-v1.5": "30838ms",
}

# rods the catalogue lists and does not serve. Measured 2026-07-25: not incapable, UNREACHABLE.
WITHDRAWN = {
    "nvidia/nvidia/llama-3.1-nemotron-ultra-253b-v1": "404 Not Found",
    "nvidia/nvidia/nemotron-4-340b-instruct":         "404 Not Found",
    "nvidia/mistralai/mistral-large-3-675b-instruct-2512": "410 Gone - withdrawn",
}


def stamp(plant: str, model: str, *, n: int, temperature: float = 0.2,
          thinking: str | None = None, max_tokens: int | None = None,
          attempts: int | None = None, failures: int = 0) -> dict:
    """Build the unit stamp that must accompany any measurement.

    `thinking` records what was ASKED for, and is annotated as unverified, because the only method
    tried (a system instruction) demonstrably did nothing.
    """
    key = f"{plant}/{model}"
    known = KNOWN.get(key, {})
    return {
        "rod": key,
        "provider": known.get("provider", plant),
        "size": known.get("size"),                     # null when the name does not state it
        "family": known.get("family"),
        "n": n,
        "temperature": temperature,
        "thinking_requested": thinking,
        "thinking_verified": False,                    # never true until an API parameter is found
        "max_tokens": max_tokens,
        "reliability": (None if attempts is None else
                        {"attempts": attempts, "failures": failures,
                         "ok_rate": round((attempts - failures) / attempts, 3) if attempts else None}),
        "at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
    }


def require(result: dict) -> dict:
    """Refuse a measurement with no fuel stamp. Mirrors axes.raise_axis refusing a proofless raise."""
    f = result.get("fuel")
    if not isinstance(f, dict) or not f.get("rod"):
        return {"ok": False, "refused": "a measurement without a fuel stamp is not a measurement - "
                                        "a capability score is a property of the MODULE-ON-FUEL pairing"}
    if f.get("n") is None:
        return {"ok": False, "refused": "a stamp without n cannot be read - 3 trials cannot separate "
                                        "2/3 from 3/3"}
    return {"ok": True, "fuel": f}


def unstamped(dirpath: str) -> list:
    """Every stored result in a directory that carries no fuel stamp. The debt, listed."""
    out = []
    if not os.path.isdir(dirpath):
        return out
    for fn in sorted(os.listdir(dirpath)):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        rec = grid.load_json(os.path.join(dirpath, fn), {})
        res = rec.get("result") or {}
        if not (res.get("fuel") or {}).get("rod"):
            out.append(fn)
    return out
