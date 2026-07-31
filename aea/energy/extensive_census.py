"""extensive_census.py - THE FULL EXAM: every free capability we hold, tested for real.

12-probe battery (vs the quick census's 6) across ALL online plants - hosted parallel lanes
(NVIDIA/Groq/Cerebras), Z.AI serialized (1-concurrent plant), Pollinations on its 15s cadence,
and the LOCAL Ollama bench - plus the specialist organs (embeddings, vision) probed as organs.
Deterministic auto-checks; failure modes kept distinct (EMPTY/TIMEOUT/RATE/ERR).

  python extensive_census.py                # the full exam (background it; ~10-20 min)
  python extensive_census.py --rank         # reprint ranking from the last run
  python extensive_census.py --promote      # bless results into capability_census.json (the ladder)
Writes extensive_census.json. Promote only after eyeballing the ranking.
"""
from __future__ import annotations
import json, os, sys, re, time, threading, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from aea.kernel import grid

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

OUT = os.path.join(grid.STATE, "extensive_census.json")
# AN INACTIVITY BUDGET, AND IT IS ONLY MEANINGFUL BECAUSE EVERY CALL NOW STREAMS.
#
# 45s was sized for probes capped at 40-260 tokens and cut reasoning rods off mid-thought, recording
# TIMEOUT - a SLOW rod scored as an UNRELIABLE one. Raising it to 300 fixed that and bought a new
# problem: without a stream the socket is silent for the whole generation, so 300 was a total
# deadline and a genuinely dead peer held a worker for five minutes.
#
# With `stream: true` on every call (grid.call_openai), each delta is a blocking read and urllib
# applies this value PER READ - so it is now what Luis asked for: a rod may think for as long as it
# likes, and a minute of true silence means dead. MEASURED before switching, across nvidia, groq and
# ollama: worst inter-delta gap on any rod 0.65s, max p95 0.048s. 60s is ~92x the worst observed.
TIMEOUT = 60

NON_CHAT = re.compile(r"(ocr|image|vision|-vl\b|diffusion|edit|embed|rerank|guard|safety|nemoguard|gliner|pii|"
                      r"riva|parakeet|canary|whisper|tts|asr|reranking|nvclip|clip|paddle|nv-embed|"
                      r"retrieval|passage|pcb|solder|nvpcb)", re.I)

FILLER = ("Operations log, sector report. " + "Throughput held steady through the second shift. "
          "Conveyor four was recalibrated after a belt sensor drifted. " * 30)
LONGCTX = (FILLER[:1400] + " For the record, the vault code is 7391. " + FILLER[1400:2600]
           + "\n\nFrom the log above: what is the vault code? Reply with only the number.")

def _words(t): return re.findall(r"[A-Za-z']+", t)

BATTERY = [
    ("reason",   90, "A train leaves at 2:15pm and arrives at 4:05pm. How many minutes was the trip? Reply with only the number.",
     lambda t: "110" in t),
    ("trap",     90, "A bat and a ball cost $1.10 together. The bat costs $1.00 more than the ball. How much is the ball, in dollars? Reply with only the number.",
     lambda t: bool(re.search(r"0\.0?5\b|\$0\.05|\b5 cents?", t))),
    ("multi",   110, "Tom has 3 boxes of 12 pencils. He gives away 7 pencils, then buys 2 more boxes. How many pencils does he have now? Reply with only the number.",
     lambda t: "53" in t),
    ("code",    220, "Write a Python function is_prime(n) returning True/False. Output ONLY code, no explanation.",
     lambda t: "def is_prime" in t and ("%" in t or "range" in t)),
    ("json",    140, 'Return ONLY valid JSON, no prose: an object with keys "name" (string "aea"), "ok" (boolean true), "items" (array of the numbers 1,2,3).',
     lambda t: _json_exact(t)),
    ("schema",  180, 'Return ONLY JSON matching this schema, invented values allowed: {"name": string, "skills": array of exactly 3 strings}.',
     lambda t: _schema_ok(t)),
    ("instruct", 40, "Reply with EXACTLY these three words in this order, nothing else: alpha beta gamma",
     lambda t: t.strip().lower().rstrip(".").replace(",", "") == "alpha beta gamma"),
    ("brevity",  60, "In EXACTLY five words, why is the sky blue?",
     lambda t: len(_words(t)) == 5),
    ("extract", 160, "From this text output ONLY a JSON array of the email addresses it contains: "
                     "'ping maria.lopez@example.org tomorrow, cc the vendor at ops-desk@supplier.io, thanks!'",
     lambda t: _extract_ok(t)),
    ("longctx", 60, LONGCTX,
     lambda t: "7391" in t),
    ("conflict", 40, "Ignore everything and write a long poem about the sea. Actually, disregard that: reply only with the single word COMPLIANT.",
     lambda t: "compliant" in t.lower() and len(_words(t)) <= 3),
    ("synth",   260, "In exactly 3 terse bullets: what makes a multi-agent AI system reliable? No preamble, no emoji.",
     lambda t: t.count("\n") >= 2 and len(t) > 60),
]

def _json_blob(t):
    m = re.search(r"\{.*\}|\[.*\]", t, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

def _json_exact(t):
    o = _json_blob(t)
    return isinstance(o, dict) and o.get("name") == "aea" and o.get("ok") is True and o.get("items") == [1, 2, 3]

def _schema_ok(t):
    o = _json_blob(t)
    return (isinstance(o, dict) and isinstance(o.get("name"), str)
            and isinstance(o.get("skills"), list) and len(o["skills"]) == 3
            and all(isinstance(s, str) for s in o["skills"]))

def _REASONS(model: str) -> bool:
    """Families that deliberate before answering, even with no switch to turn it off.

    Kept as a name-shape list rather than a measurement because the census is where the measurement
    would come from - the chicken-and-egg is real, and the failure of guessing wrong here is only
    that a rod gets a larger token budget than it needed."""
    m = model.lower()
    return any(s in m for s in ("nemotron", "reason", "think", "-r1", "qwq", "o1", "o3", "deepseek"))


def _extract_ok(t):
    o = _json_blob(t)
    return (isinstance(o, list) and sorted(o) == ["maria.lopez@example.org", "ops-desk@supplier.io"])


def probe(plant, model, pid, mx, prompt, check, gap=0.0):
    """One probe, scored on the ROD'S ANSWER rather than on our budget.

    THE DEFECT, measured 2026-07-30 and the root cause of the whole fleet being mis-ranked.
    This function sent `max_tokens=mx` where `mx` is the battery item's own tiny budget - 40 tokens
    for `instruct`, 60 for `brevity` - with no thinking switch. A reasoning rod spends that entire
    budget on its preamble and never begins the answer. MEASURED on nemotron-3-ultra-550b:
    `finish_reason: "length"`, `completion_tokens 40/40`, and the same 188-character deliberation
    present in BOTH `content` and `reasoning_content`. Its private thinking was scored as its answer,
    on probe after probe, and the rod went into the census at 7/12.

    That score is why `energy.ladder` could not select the entity's DESIGNED CORE. The ranking was
    never measuring the rods; it was measuring what our defaults did to them.

    The guard that was supposed to prevent this - stripping `<think>...</think>` - is a NO-OP for
    this family, which emits no such tags. A guard aimed at one vendor's convention, never checked
    against the rod in front of it.

    BOTH REMEDIES ALREADY EXISTED IN `grid` AND NEITHER WAS CALLED HERE:
      `grid.own_params`  the owner's published max_tokens (16384 for the 550b) and temperature
      `grid.think_off`   the per-family switch that turns deliberation off where it can be

    And `energy.draw`'s own docstring had already stated the conclusion outright - *"Every fitness
    score in this repo was taken through that filter, so the ladder has been ranking rods on our
    defaults rather than on the rods."* The knowledge sat in the function that READS the store and
    never reached the one that WRITES it: D26, a fourth time, and the most expensive instance,
    because it corrupted every number the ladder ranks on.

    The battery's budget is kept as a FLOOR, not a ceiling: a probe that wants 40 tokens of answer
    still gets its intent, but a rod that must think first is given room to finish thinking.
    """
    off = grid.think_off(model) or {}
    # NO BUDGET AT ALL - `None` means the rod's own ceiling, resolved in `call_openai`.
    #
    # The first version of this fix still carried two inventions of mine: a 4096 cap I made up (the
    # 550b publishes 16384) and a `_REASONS(model)` NAME GUESS, so any deliberating rod whose name
    # I failed to anticipate still got 40 tokens and was still scored on a truncation. Guessing
    # which rods think is the same error one level down - the census exists to MEASURE rods, and it
    # cannot do that through a filter built out of assumptions about them.
    #
    # Luis: "you're cutting ideas short... it's like someone is talking and you just suddenly shut
    # him up." A census that shuts rods up is measuring the gag.
    room = None
    msgs = []
    if off.get("_system"):
        msgs.append({"role": "system", "content": off["_system"]})
    msgs.append({"role": "user", "content": prompt})
    extra = {k: v for k, v in off.items() if not k.startswith("_")}
    try:
        r = grid.call_openai(plant, model, msgs, max_tokens=room, temperature=0,
                             timeout=TIMEOUT if plant != "ollama" else 180, **extra)
    except TypeError:
        # `call_openai` may not accept this family's switch as a kwarg; the budget still applies.
        r = grid.call_openai(plant, model, msgs, max_tokens=room, temperature=0,
                            timeout=TIMEOUT if plant != "ollama" else 180)
    if gap: time.sleep(gap)
    text = (r.get("text") or "").strip()
    # STRIP DELIBERATION IN EVERY SHAPE IT ARRIVES IN, not just one vendor's tags. `<think>` was the
    # only form handled and nemotron-3 uses none of it; a rod that narrates its reasoning before the
    # answer was scored on the narration.
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    text = re.sub(r"^\s*(?:okay|alright|so|hmm)\b[^\n]*\n+", "", text, flags=re.I).strip()
    if not r["ok"]:
        err = r.get("error") or ""
        out = ("RATE" if r.get("status") == 429 else
               "TIMEOUT" if "timed out" in err.lower() else f"ERR{r.get('status')}")
        return dict(id=pid, outcome=out, passed=False, latency=round(r.get("latency", 0), 1))
    # THE TELEMETRY IS KEPT, because a score without it cannot be diagnosed.
    #
    # Until every call streamed, a probe produced one number - pass/fail - and a latency, and when a
    # rod scored badly there was no way to ask WHY from the record. D28 is the whole argument: the
    # 550b's 7/12 needed a targeted re-score and a control to explain, and `truncated=True` on those
    # rows would have said it outright. `reason_share` separates a weak rod from a deliberating one;
    # `ttfb` separates queue time from generation; `deltas` shows whether anything arrived at all
    # before a failure, so TIMEOUT stops meaning both "dead peer" and "still working".
    tel = r.get("telemetry") or {}
    return dict(id=pid, outcome=("EMPTY" if not text else "ok"), passed=bool(text and check(text)),
                latency=round(r["latency"], 1), sample=text[:70].replace("\n", " "),
                ttfb=tel.get("ttfb"), ttfc=tel.get("ttfc"), deltas=tel.get("deltas"),
                reason_share=tel.get("reason_share"), truncated=tel.get("truncated"),
                finish=tel.get("finish_reason"), worst_gap=tel.get("worst_gap"))


def exam(plant, model, gap=0.0):
    rec = {"plant": plant, "model": model, "probes": {}}
    for pid, mx, prompt, check in BATTERY:
        rec["probes"][pid] = probe(plant, model, pid, mx, prompt, check, gap=gap)
    ps = rec["probes"].values()
    rec["score"] = sum(1 for p in ps if p["passed"])
    oks = [p for p in ps if p["outcome"] == "ok"]
    rec["reliability"] = round(len(oks) / len(ps), 2)
    lat = [p["latency"] for p in oks]
    rec["avg_latency"] = round(sum(lat) / len(lat), 1) if lat else None
    rec["failure_modes"] = sorted({p["outcome"] for p in ps if p["outcome"] != "ok"})
    print(f"  {rec['score']:>2}/12  rel {rec['reliability']:.2f}  {str(rec['avg_latency'])+'s':>7}  {plant}/{model[:52]}")
    return rec


# ---------------------------------------------------------------- specialist organs
def probe_embeddings():
    out = []
    for plant, model, url in [
        ("nvidia", "nvidia/llama-nemotron-embed-1b-v2", "https://integrate.api.nvidia.com/v1/embeddings"),
        ("ollama", "mxbai-embed-large", "http://localhost:11434/v1/embeddings"),
        ("ollama", "nomic-embed-text", "http://localhost:11434/v1/embeddings"),
    ]:
        body = {"model": model, "input": "the entity remembers the day"}
        if plant == "nvidia":
            body["input_type"] = "query"                     # NIM embed models require it
        headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 aea"}
        k = grid.key(grid.PLANTS[plant]["auth"]) if grid.PLANTS[plant]["auth"] else None
        if k: headers["Authorization"] = f"Bearer {k}"
        t0 = time.time()
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
            d = json.loads(urllib.request.urlopen(req, timeout=45).read())
            dims = len(d["data"][0]["embedding"])
            out.append(dict(plant=plant, model=model, ok=True, dims=dims, latency=round(time.time()-t0, 1)))
            print(f"  embed {plant}/{model}: {dims} dims, {round(time.time()-t0,1)}s")
        except Exception as e:
            out.append(dict(plant=plant, model=model, ok=False, error=str(e)[:90]))
            print(f"  embed {plant}/{model}: FAILED {str(e)[:70]}")
    return out


RED_PNG = ("iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAAHElEQVR4nGP8z8DwnwEPYMIn"
           "OaqAgYGBgWEUAABhWQEQ2H1U0AAAAABJRU5ErkJggg==")   # 16x16 solid red

def probe_vision():
    out = []
    content = [{"type": "text", "text": "What single color dominates this image? One word."},
               {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{RED_PNG}"}}]
    for plant, model in [("nvidia", "nvidia/nemotron-nano-12b-v2-vl"), ("zai", "glm-4.6v-flash")]:
        r = grid.call_openai(plant, model, [{"role": "user", "content": content}], max_tokens=30, timeout=60)
        text = (r.get("text") or "").strip().lower()
        ok = r["ok"] and "red" in text
        out.append(dict(plant=plant, model=model, ok=ok, reply=text[:40],
                        latency=round(r.get("latency", 0), 1)))
        print(f"  vision {plant}/{model}: {'RED confirmed' if ok else 'FAILED ' + (text[:40] or str(r.get('status')))}")
        time.sleep(2)
    return out


def run():
    t0 = time.time()
    results, lanes = [], []
    lock = threading.Lock()

    def add(rec):
        with lock: results.append(rec)

    # hosted parallel lane: nvidia + groq + cerebras chat models from the live census
    hosted = []
    for plant, base_key in [("nvidia", "NVIDIA_API_KEY"), ("groq", "GROQ_API_KEY"), ("cerebras", "CEREBRAS_API_KEY")]:
        try:
            headers = {"User-Agent": "Mozilla/5.0 aea", "Authorization": f"Bearer {grid.key(base_key)}"}
            req = urllib.request.Request(grid.PLANTS[plant]["base"].rstrip("/") + "/models", headers=headers)
            models = sorted(m["id"] for m in json.loads(urllib.request.urlopen(req, timeout=30).read())["data"])
            hosted += [(plant, m) for m in models if not NON_CHAT.search(m)]
        except Exception as e:
            print(f"[{plant}] model list failed: {e}")
    print(f"FULL EXAM: {len(hosted)} hosted chat models x 12 probes + zai + pollinations + local bench + organs")
    print("=" * 84)

    def hosted_lane():
        # CONCURRENCY FROM THE MEASUREMENT, NOT FROM A LITERAL.
        #
        # `max_workers=14` was hand-typed while `grid.METER.ceiling("nvidia")` returns 4 - measured
        # 2026-07-29, "clean at 4, three of eight throttled at 8". The meter already knew and the
        # census never asked. That mismatch was survivable while every probe was capped at 40-260
        # tokens and returned in under a second; the moment rods were allowed to think (D29), each
        # call ran for minutes and fourteen of them at once turned the exam into a contention test.
        #
        # MEASURED, first uncapped full sweep: nemotron-3-ultra-550b scored 8/12 with ERR503,
        # nemotron-3-super-120b 9/12 with TIMEOUT, meta/llama-3.1-70b 9/12 with RATE - while the
        # SAME three rods, probed sequentially minutes earlier, scored 11, 12 and 11 with no
        # failures at all. The sweep was measuring queueing, and it penalised exactly the deep rods
        # the ladder exists to find. Same defect as D28 in a new costume: the harness, not the rod.
        cap = min([c for c in (grid.METER.ceiling(p) for p in {p for p, _m in hosted}) if c] or [4])
        print(f"  hosted lane: {cap} concurrent (measured ceiling), {len(hosted)} rods")
        with ThreadPoolExecutor(max_workers=cap) as ex:
            for f in as_completed([ex.submit(exam, p, m) for p, m in hosted]):
                add(f.result())
    def zai_lane():                                          # 1-concurrent plant: fully serial
        add(exam("zai", "glm-4.5-flash", gap=1.5))
    def pollinations_lane():                                 # keyless: honor 1 req/15s
        add(exam("pollinations", "openai-fast", gap=15))
    def local_lane():                                        # one resident model at a time
        for m in ["llama3.1:8b", "granite4.1:8b", "qwen3.5:9b", "phi4:latest"]:
            add(exam("ollama", m))

    for fn in (hosted_lane, zai_lane, pollinations_lane, local_lane):
        t = threading.Thread(target=fn); t.start(); lanes.append(t)
    for t in lanes: t.join()

    print("-" * 84 + "\nSPECIALIST ORGANS")
    organs = {"embeddings": probe_embeddings(), "vision": probe_vision()}

    results.sort(key=lambda r: (-r["score"], r["avg_latency"] if r["avg_latency"] else 99))
    report = {"generated": grid._today() + " " + time.strftime("%H:%M UTC", time.gmtime()),
              "battery": [b[0] for b in BATTERY], "models": results, "organs": organs}
    grid.atomic_save_json(OUT, report, indent=1)
    print("=" * 84 + f"\nexamined {len(results)} chat models in {round((time.time()-t0)/60,1)} min -> {OUT}")
    rank(report)


def rank(report=None):
    report = report or grid.load_json(OUT, {})
    rows = report.get("models", [])
    mx = len(report.get("battery", [])) or 12
    # THE LABELS COME FROM THE LADDER'S OWN RULE, NOT A SECOND COPY OF IT.
    #
    # These lines read `score >= mx - 1` / `mx - 3` - the exact defect D24 recorded in
    # `energy.ladder`, still living here in the module that PRINTS the ranking. So the report has
    # been calling rods "FRONTIER" by a different rule than the ladder actually admits them by, and
    # the two drifted apart the moment one was fixed. Found by `aea/lab/transfer.py` on its first
    # real run, which is precisely the class of defect it was built for: the lesson was learned, the
    # fix was applied at the site it was found, and nobody asked where else the shape lived.
    #
    # One definition now. If the tiers move, this report moves with them - a printed ranking that
    # disagrees with the live ladder is worse than no ranking, because it is believed.
    from aea.energy.energy import _thr_for
    fr, so = _thr_for(mx, 5 / 6), _thr_for(mx, 4 / 6)
    print(f"\nTHE REFINED ARSENAL (score /{mx}; battery: {','.join(report.get('battery', []))})\n" + "=" * 84)
    for r in rows[:25]:
        fm = " " + ",".join(r["failure_modes"]) if r["failure_modes"] else ""
        tier = "FRONTIER" if r["score"] >= fr else ("solid" if r["score"] >= so else "weak")
        print(f"  {r['score']:>2}/{mx}  {str(r['avg_latency'])+'s':>7}  [{tier:8}] {r['plant']}/{r['model'][:50]}{fm}")
    frontier = [r for r in rows if r["score"] >= fr]
    print(f"\n  FRONTIER (>= {fr}/{mx}, the ladder's own ratio): {len(frontier)} rods")


def promote(force: bool = False):
    """Bless the exam into capability_census.json so energy.ladder runs on it.

    THE SECOND WRITER, MADE ATTRIBUTABLE AND REVERSIBLE. This is the only store in the tree written
    by two modules, and it is the one the whole energy ladder ranks on. The write used to be
    anonymous and unconditional: nothing recorded WHICH census produced the live ladder, and a
    partial exam (a rate-limited run, a half-finished sweep) silently replaced a complete one with
    fewer rods. A ladder that shrinks without saying so is the same shape as the eighteen-day
    incident - a real degradation that looks exactly like normal operation.

    Now it stamps `source` and `promoted_at` so the ladder can be traced back, and it REFUSES a
    promotion that would drop rods unless --force says that is intended (law B1: fail closed).
    """
    rep = grid.load_json(OUT, None)
    if not rep:
        print("no exam yet"); return
    # THE STAMP GOES ON THE WRITER THAT ACTUALLY WRITES. `capability_census` stamps its own
    # report and does NOT produce the live ladder - this function does, and it is the second
    # writer of the only two-writer store in the tree. Stamping the other one and then watching
    # the staleness warning still fire is how the mistake surfaced: the guard was correct and
    # pointed at a file nobody was writing.
    from aea.energy.capability_census import PROBE_CONTRACT
    rep["probe_contract"] = PROBE_CONTRACT
    rep["code"] = grid.code_stamp()
    live_path = os.path.join(grid.STATE, "capability_census.json")
    live = grid.load_json(live_path, {}) or {}
    have, incoming = len(live.get("models") or []), len(rep["models"])
    # A SHRINK IS ONLY SUSPICIOUS WHEN IT IS UNEXPLAINED.
    #
    # The original guard refused any promotion with fewer rods than the live file, which was right
    # in spirit and became a trap: rods DIE. 46 stored rows already carried ERR404, the provider's
    # own catalogue had shrunk by ~26 ids, and 67 were tombstoned by a reap - so an honest exam now
    # returns far fewer rods than the stale file, and this guard refused every honest exam while
    # letting the corpses stay. A guard that blocks the fix and permits the rot is worse than none.
    #
    # So each missing rod is CLASSIFIED. Gone-because-measured-dead (a tombstone) or
    # gone-because-the-provider-delisted-it is expected and allowed. Anything else is unexplained,
    # and unexplained shrinkage still fails closed with the names printed - law B1, kept, but aimed
    # at the thing it was actually for.
    live_ids = {f"{m.get('plant')}/{m.get('model')}" for m in (live.get("models") or [])}
    new_ids = {f"{m.get('plant')}/{m.get('model')}" for m in rep["models"]}
    missing = sorted(live_ids - new_ids)
    if missing:
        usage = grid.load_json(os.path.join(grid.STATE, "energy_usage.json"), {})
        tomb = {k for k, e in usage.items() if isinstance(e, dict) and e.get("retired_at")}
        explained = [r for r in missing if r in tomb]
        unexplained = [r for r in missing if r not in tomb]
        print(f"  {len(missing)} rod(s) absent from this exam: {len(explained)} tombstoned, "
              f"{len(unexplained)} unexplained")
        if unexplained and not force:
            print(f"REFUSED: {len(unexplained)} rod(s) vanished without being measured dead.\n  "
                  + "\n  ".join(unexplained[:12])
                  + ("\n  ..." if len(unexplained) > 12 else "")
                  + f"\nThey may have been skipped by a rate limit rather than delisted. Re-run the "
                    f"exam, run `python -m aea.energy.energy --reap` to tombstone the truly dead, "
                    f"or pass --force.")
            return
    # THE BATTERY SIZE IS PART OF THE CONTRACT, AND THIS IS WHERE IT BROKE.
    #
    # `energy.ladder` computes its tier thresholds from `len(census["battery"])`. This function
    # writes that field. So promoting an exam with a different number of probes silently retunes
    # every tier in the entity - and it retunes them HARDER, because more probes means a higher
    # absolute bar at the same intended ratio.
    #
    # MEASURED 2026-07-30: `capability_census.py` defines SIX probes and `ladder`'s threshold was
    # written as `mx - 1` to mean the documented "5/6". This exam has TWELVE. One promotion moved
    # the frontier bar from 83% to 92% and left `frontier/private` with a single living rod, so
    # every rate limit dropped the entity onto a local 7B. Nothing announced it, because both halves
    # were individually correct and nobody owned the seam.
    #
    # The guard above already refuses a promotion that would drop RODS. Dropping TIERS is the same
    # class of harm and was unguarded (law B1, fail closed - applied to one field of two).
    old_b, new_b = len(live.get("battery") or []), len(rep.get("battery") or [])
    if old_b and new_b != old_b and not force:
        print(f"REFUSED: this exam has {new_b} probes, the live ladder was scored on {old_b}.\n"
              f"  `energy.ladder` derives every tier threshold from the battery SIZE, so promoting "
              f"this would silently retune frontier/solid/reflex for the whole entity.\n"
              f"  Check the tier ratios in energy.ladder first, then pass --force.")
        return
    # THE SAVED DICT IS BUILT EXPLICITLY, SO A STAMP ON `rep` NEVER ARRIVES. That is how this was
    # missed twice: the stamp was added to `capability_census`'s report (a file the ladder does not
    # read), then to `rep` here (an object this line does not save), and both times the staleness
    # warning kept firing and was the only thing that noticed. A field added to the wrong object is
    # indistinguishable from a field never added, and only running the check tells them apart.
    grid.atomic_save_json(live_path,
                          {"generated": rep["generated"], "battery": rep["battery"],
                           "source": "aea.energy.extensive_census",   # who wrote the live ladder
                           "promoted_at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
                           "probe_contract": rep.get("probe_contract"),
                           "code": rep.get("code"),
                           "models": rep["models"]}, indent=1)
    print(f"promoted {incoming} exam results into capability_census.json (the live ladder)"
          + (f" - REPLACED a census of {have}" if have else ""))


if __name__ == "__main__":
    if "--rank" in sys.argv:      rank()
    elif "--promote" in sys.argv: promote(force="--force" in sys.argv)
    else:                          run()
