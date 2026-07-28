"""stats.py - THE INTERVAL, computed, instead of THE BAND, declared.

WHY THIS REPLACES THE BAND. Every result in this lab is read against `BAND = 0.10`, and that number
came from ONE accident: in x16 the same assembly ran twice under two names and scored 0.70 and 0.60.
A single observation of a difference is not a noise floor, it is an anecdote about noise, and it has
been load-bearing for nine experiments. It is also FLAT - the same 0.10 whether a cell holds 8 trials
or 128 - when the actual uncertainty of a rate depends on how many trials produced it.

AND THE UNIT IS WRONG, which matters more than the threshold. A 16-step chain contributes 16 per-step
outcomes, and they are NOT independent: miss step 4 and the running value is wrong for the rest, so
steps 5..16 are almost certainly wrong too. Pooling `hits / of` across sequences treats 128 correlated
outcomes as 128 independent ones and shrinks the apparent error by roughly the square root of the
cluster size. That is why small differences have looked meaningful.

So: THE SEQUENCE IS THE UNIT. Resample whole sequences, never steps. A rate keeps its per-step
numerator because that is the quantity of interest; the UNCERTAINTY is computed by shaking the
sequences, which is the level at which the samples are actually independent.

Nothing here is a significance test and none of it is called one. These are intervals, reported.
"""
from __future__ import annotations

import math
import random

Z95 = 1.959964


def wilson(k, n, z=Z95):
    """Score interval for a proportion. Correct at small n where the normal approximation is not:
    at 8/8 the normal interval is [1.0, 1.0], which claims certainty from eight trials."""
    if not n:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, centre - half), 3), round(min(1.0, centre + half), 3))


def _rate(seqs):
    """Per-step rate over a bag of sequences. Each sequence is (hits, steps)."""
    of = sum(s[1] for s in seqs)
    return (sum(s[0] for s in seqs) / of) if of else None


rate = _rate


def boot(seqs, reps=4000, seed=11, z=Z95):
    """Percentile interval for a per-step rate, resampling SEQUENCES.

    A sequence enters or leaves the sample whole, so the correlation between its own steps is
    preserved instead of being averaged away. With few sequences the interval comes out wide, and
    that width is the honest reading of a cell built from eight chains.
    """
    seqs = [s for s in seqs if s and s[1]]
    if len(seqs) < 2:
        return (None, None)
    rng = random.Random(seed)
    n = len(seqs)
    out = []
    for _ in range(reps):
        r = _rate([seqs[rng.randrange(n)] for _ in range(n)])
        if r is not None:
            out.append(r)
    if not out:
        return (None, None)
    out.sort()
    lo = out[int(0.025 * (len(out) - 1))]
    hi = out[int(0.975 * (len(out) - 1))]
    return (round(lo, 3), round(hi, 3))


def boot_diff(a, b, reps=4000, seed=11):
    """Interval for rate(a) - rate(b), resampling each arm's sequences independently.

    Unpaired, and it says so: at temperature 0.2 the same prompt does not give the same reply, so
    sequence i of one arm and sequence i of another are not a matched pair and must not be treated
    as one. `excludes_zero` is reported as what it is - an interval that does not cover zero - and
    never as significance.
    """
    a = [s for s in a if s and s[1]]
    b = [s for s in b if s and s[1]]
    if len(a) < 2 or len(b) < 2:
        return {"diff": None, "lo": None, "hi": None, "excludes_zero": None}
    ra, rb = _rate(a), _rate(b)
    rng = random.Random(seed)
    out = []
    for _ in range(reps):
        xa = _rate([a[rng.randrange(len(a))] for _ in range(len(a))])
        xb = _rate([b[rng.randrange(len(b))] for _ in range(len(b))])
        if xa is not None and xb is not None:
            out.append(xa - xb)
    out.sort()
    lo = out[int(0.025 * (len(out) - 1))]
    hi = out[int(0.975 * (len(out) - 1))]
    return {"diff": round(ra - rb, 3), "lo": round(lo, 3), "hi": round(hi, 3),
            "excludes_zero": bool(lo > 0 or hi < 0)}


# THE NOISE FLOOR, AND IT IS NOT OURS - IT IS THE SUBSTRATE'S. Published measurements put pass@1
# standard deviation at 5 to 15 percentage points across random seeds on small benchmarks, with
# further swings of several points from batch size, GPU count and inference backend ALONE at fixed
# temperature. So an effect smaller than this is not a small effect; it is indistinguishable from
# rerunning the same thing. Every number this lab has published sits at or below it.
NOISE_FLOOR = 0.05
MIN_SAMPLES = 10          # per cell, before a difference may be read at all


def sd(values):
    """Spread across repeats of the same cell. A rate reported without this is a point estimate
    pretending to be a measurement."""
    v = [x for x in values if x is not None]
    if len(v) < 2:
        return None
    m = sum(v) / len(v)
    return round((sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5, 4)


def mde(n, base=0.5, z_a=1.959964, z_b=0.8416):
    """MINIMUM DETECTABLE EFFECT at this n. Answered BEFORE the run, not after.

    If the smallest difference the design can see is larger than the difference expected, the run
    cannot answer its own question and should not be bought. That check has never been made here:
    the flagship claims rest on cells of 3 and 4.
    """
    if not n:
        return None
    import math
    se = math.sqrt(2 * base * (1 - base) / n)
    return round((z_a + z_b) * se, 3)


def powered(n, effect):
    """Can a cell of this size see an effect of this size, against the substrate's own noise?"""
    m = mde(n)
    return {"n": n, "effect": effect, "mde": m, "noise_floor": NOISE_FLOOR,
            "ok": bool(m and effect >= m and effect >= NOISE_FLOOR),
            "reading": ("cannot be read: n=%d sees %.3f at best, and the substrate's own noise is "
                        "%.2f" % (n, m or 1.0, NOISE_FLOOR)
                        if not (m and effect >= m and effect >= NOISE_FLOOR)
                        else "readable: %.3f exceeds both the %.3f detection limit and the %.2f "
                             "noise floor" % (effect, m, NOISE_FLOOR))}


def mcnemar(b, c):
    """Exact two-sided McNemar on PAIRED outcomes. `b` = A right and B wrong, `c` = the reverse.

    THE PAIR IS THE POINT. Running the same chain under two containers and comparing the two pools
    throws away the fact that a hard chain is hard under both; pairing removes task difficulty from
    the comparison entirely, and task difficulty is the dominant variance term in an arithmetic
    chain. Only the discordant pairs carry information, which is why this is honest about small n:
    eight pairs that all agree say nothing, and the test says nothing.
    """
    n = b + c
    if not n:
        return {"b": b, "c": c, "discordant": 0, "p": None}
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) * (0.5 ** n)
    return {"b": b, "c": c, "discordant": n, "p": round(min(1.0, 2 * tail), 4)}


def describe(k, n, seqs=None):
    """One cell, with its uncertainty attached. A rate printed alone is the old mistake."""
    d = {"k": k, "n": n, "rate": round(k / n, 3) if n else None}
    d["wilson95"] = wilson(k, n)
    if seqs:
        d["boot95_by_sequence"] = boot(seqs)
        d["sequences"] = len(seqs)
    return d


if __name__ == "__main__":
    print("WHAT THE FLAT BAND HID\n")
    print("  a cell of 8 trials, 6 passed:")
    print("    band says       0.75 +/- 0.10   ->  [0.65, 0.85]")
    print("    wilson says     %s" % (wilson(6, 8),))
    print("\n  a cell of 128 pooled steps, 96 hit, from 8 chains of 16:")
    print("    wilson on 128 (WRONG - steps are not independent): %s" % (wilson(96, 128),))
    seqs = [(16, 16), (16, 16), (16, 16), (16, 16), (16, 16), (16, 16), (0, 16), (0, 16)]
    print("    bootstrap by sequence (right):                     %s" % (boot(seqs),))
    print("\n  same numerator, and the honest interval is several times wider.")
