"""access.py - EVERY DIMENSION OF ACCESS, not just modality.

Luis, 2026-07-30: "are you sure we don't have more access besides modality? We should explore all
types of access before entering more... besides modality, what do we need to know?"

The right question, and the honest answer was no. `modality.py` answered ONE dimension - what shape
of data a model speaks. Whether the entity can actually USE a given capability depends on at least
six, and this repo already holds data on most of them in `grid.PLANTS` and has never crossed it
with modality even once.

THE SIX DIMENSIONS OF ACCESS:

  1 MODALITY   what shape of data          -> already mapped (modality.py, toolkinds.py)
  2 PLANT      WHO serves it               -> 10+ plants in grid.PLANTS, never crossed with #1
  3 PRIVACY    may THIS data go there      -> local / no-train / trains. A HARD gate: a plant that
                                              trains on input can never see private data, whatever
                                              its capabilities are. This is already in the code and
                                              nothing consults it per-capability.
  4 BUDGET     how often, how much         -> rpm / rpd / tpd / max_inflight. Access is not binary,
                                              it is rationed. cerebras is 5 rpm; sambanova 20/day.
  5 REACH      is the key actually here    -> a plant in the table with no key is a plant we do not
                                              have, and the table cannot tell you which.
  6 LOCALITY   does it need the network    -> local means no egress, no quota, works offline. The
                                              difference between a capability and a DEPENDENCY.

WHY THIS MATTERS BEFORE ADDING MORE. The senses survey found embeddings on NVIDIA and wired them.
If ollama serves embeddings LOCALLY, then recall is available offline, privately, unmetered - and
we just made a network call, on a metered quota, sending private memory text to a third party, for
something the machine could do itself. That is not a small difference: privacy is dimension 3 and
it is the one that cannot be bought back later.

    python -m aea.tooling.access            the matrix
    python -m aea.tooling.access --probe    actually call one per (plant, modality) cell
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

from aea.kernel import grid

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

OUT = os.path.join(str(grid.STATE), "access.json")
UA = "aea-access/1"

# The doors, per modality. Same table as modality.py deliberately - if they ever disagree, one of
# them is lying about the world.
DOORS = {
    "understand": "/chat/completions",
    "recall":     "/embeddings",
    "rank":       "/ranking",
}


def keyed(p: dict) -> bool:
    """Dimension 5: is the key actually present. A plant in the table with no key is a plant we do
    not have, and the table alone cannot tell you which."""
    return (p.get("auth") is None) or bool(os.environ.get(p["auth"], "").strip())


def _get(url: str, token: str = "", timeout: int = 20) -> tuple:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, **({"Authorization": f"Bearer {token}"} if token else {})})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read().decode("utf-8", "ignore")[:200]
        except Exception:
            return e.code, str(e.reason)[:120]
    except Exception as e:
        return 0, f"{type(e).__name__}: {str(e)[:100]}"


def _post(base: str, door: str, body: dict, token: str = "", timeout: int = 45) -> tuple:
    try:
        req = urllib.request.Request(
            base + door, data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "User-Agent": UA,
                     **({"Authorization": f"Bearer {token}"} if token else {})})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "ignore")[:400]
    except urllib.error.HTTPError as e:
        try:
            return e.code, e.read().decode("utf-8", "ignore")[:200]
        except Exception:
            return e.code, str(e.reason)[:120]
    except Exception as e:
        return 0, f"{type(e).__name__}: {str(e)[:100]}"


def catalogue(name: str, p: dict) -> tuple:
    """What this plant says it serves. Not what it will actually give us - see `probe`."""
    if not p.get("openai"):
        return [], "not an openai-shaped plant; its catalogue needs its own client"
    tok = os.environ.get(p["auth"] or "", "")
    st, body = _get(p["base"] + "/models", tok)
    if st != 200:
        return [], f"HTTP {st}: {str(body)[:70]}"
    try:
        return sorted({d.get("id", "") for d in json.loads(body).get("data") or []}), ""
    except Exception as e:
        return [], f"unparseable: {str(e)[:60]}"


# What an id looks like when it is an embedder or a reranker. Crude on purpose and only used to
# SUGGEST a probe target - the probe is what decides.
def _looks(mid: str, kind: str) -> bool:
    m = mid.lower()
    if kind == "recall":
        return any(w in m for w in ("embed", "e5", "bge", "gte", "nomic", "arctic", "minilm"))
    if kind == "rank":
        return any(w in m for w in ("rerank", "ranking", "cross-encoder"))
    return not any(w in m for w in ("embed", "rerank", "whisper", "tts", "guard", "stable",
                                    "flux", "sdxl"))


def run(do_probe: bool = False) -> dict:
    rows = []
    print("=" * 104)
    print("ACCESS - six dimensions, not one")
    print("=" * 104)
    print(f"  {'plant':11s} {'key':4s} {'privacy':9s} {'rpm':>6s} {'rpd':>7s} {'models':>7s}  note")
    plants = {}
    for name, p in grid.PLANTS.items():
        has = keyed(p)
        ids, why = (catalogue(name, p) if has else ([], "no key in the environment"))
        plants[name] = dict(keyed=has, privacy=p.get("privacy"), rpm=p.get("rpm"),
                            rpd=p.get("rpd"), n=len(ids), why=why, ids=ids[:400])
        rpm = p.get("rpm")
        rpd = p.get("rpd")
        print(f"  {name:11s} {'yes' if has else 'NO':4s} {str(p.get('privacy')):9s} "
              f"{str(rpm)[:6]:>6s} {str(rpd)[:7]:>7s} {len(ids):7d}  {why[:44] or p.get('note','')[:44]}")

    # ------------------------------------------------------------------ THE CROSS: plant x modality
    print()
    print("  WHICH PLANT COULD SERVE WHICH MODALITY (by catalogue, before probing)")
    print(f"  {'plant':11s} {'understand':>11s} {'recall':>8s} {'rank':>6s}   examples of recall")
    for name, d in plants.items():
        if not d["keyed"] or not d["ids"]:
            continue
        emb = [i for i in d["ids"] if _looks(i, "recall")]
        rnk = [i for i in d["ids"] if _looks(i, "rank")]
        txt = [i for i in d["ids"] if _looks(i, "understand")]
        rows.append(dict(plant=name, understand=len(txt), recall=len(emb), rank=len(rnk),
                         recall_ids=emb[:6]))
        print(f"  {name:11s} {len(txt):11d} {len(emb):8d} {len(rnk):6d}   "
              + ", ".join(x[:26] for x in emb[:2]))

    # ------------------------------------------------------------------ THE PROBE
    probes = []
    if do_probe:
        print()
        print("  PROBE - a catalogue entry is not access. One call per (plant, modality) that has a")
        print("  candidate. THE QUESTION THAT MATTERS: can we do RECALL locally and privately?")
        for r in rows:
            p = grid.PLANTS[r["plant"]]
            tok = os.environ.get(p["auth"] or "", "")
            if r["recall_ids"]:
                mid = r["recall_ids"][0]
                t0 = time.time()
                st, body = _post(p["base"], DOORS["recall"],
                                 {"model": mid, "input": ["ping"]}, tok)
                ok = st == 200 and '"embedding"' in body
                probes.append(dict(plant=r["plant"], modality="recall", model=mid, status=st,
                                   ok=ok, seconds=round(time.time() - t0, 2), note=body[:90]))
                print(f"    {r['plant']:11s} recall  {mid[:34]:34s} "
                      f"{'WORKS' if ok else 'HTTP ' + str(st):9s} {round(time.time()-t0,2)}s")
                if not ok:
                    print(f"        {body[:96]}")

    res = dict(at=time.strftime("%Y-%m-%d %H:%M:%S"), plants=plants, cross=rows, probes=probes)
    grid.atomic_save_json(OUT, res)
    print(f"\n  -> {os.path.relpath(OUT, str(grid.ROOT))}")
    return res


if __name__ == "__main__":
    run(do_probe="--probe" in sys.argv)
