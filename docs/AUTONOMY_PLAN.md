# THE PATH TO TRUE AUTONOMY (AEA-grounded)

**"Truly autonomous" here =** the entity runs unattended on FREE compute, survives its own limits and
failures with no babysitting, stays on-goal, ships useful work for Luis, and improves itself — and
keeps doing all of that even if paid AI disappears tomorrow. A companion that doesn't need a credit card.

---

## THE POWERPLANT — full capability map (verified limits, June 2026)

| Plant | Zone | VERIFIED free limit | On 429 / at-limit | Role |
|---|---|---|---|---|
| **NVIDIA NIM** | residential (no-train) | **40 rpm PER model**, 51 models serve, INDEPENDENT buckets (0/121 429 at once) | reroute to another of its 51 models (independent) | the firehose — swarm backbone, tools, deep reasoning |
| **Groq** | residential (no-train) | 30–60 rpm, sub-0.3s, **939 tok/s** (gpt-oss-20b) | reroute | fast / reflex tier, strict-JSON planner |
| **Cerebras** | residential (no-train) | **5 rpm / 30K TPM / 8K ctx** (VERIFIED, burst 12→5) | reroute (fills at exactly 5) | BATCH / leaf only — not interactive |
| **Z.AI GLM** | public (API content no-train per ToS) | ~1 concurrent (serialize), reasoning + vision | reroute | vision lane, public worker |
| **Ollama (local)** | residential (local) | **unlimited**, ~27 tok/s warm, ONE model resident | n/a (no limit) | the always-on private FLOOR — survives losing all paid AI |
| **Pollinations** | outskirts (keyless) | 1 req / 15s | reroute | last-resort keyless fallback |

**Aggregate:** ~2,200 req/min, ~59 independent parallel buckets, + unlimited local. The grid operator
(`Meter`) now knows each limit exactly, cools a 429'd bucket (exponential backoff), and reroutes around
it WITHOUT blocking the buckets that aren't throttled (proven: `test_resilient.py`, 15/15 under load).

---

## AEA AUTONOMY SCOREBOARD — what's done, what's left

**PROVEN (~19 of 26 elements)** — substrate, multiplicity, P-path L4, A-abstraction L3 (memory+REAL
tools), R-prompting L3, **S-async L5** (genetic-memory relay), compose / propagate / observe; seeds
1, 2, 3 (crystallize), 5 (self-version), 7 (ceiling-detect), 8 (transcendence toolset), 10 (backwards
channel); op:learn; **seed-4 flexibilize + restorable-coherence (just proven: the 429-reroute)**;
emergence-over-imposition.

**REMAINING for true autonomy (the real to-do):**
1. **op:ship** — the entity must produce REAL external artifacts (a brief, a draft, a posted thing),
   not just text. It has never done Luis's actual work. *This is the big one.*
2. **op:time / S-async L4 (unattended)** — a scheduled run that fires with no human (cron / task
   scheduler), so it works while Luis sleeps.
3. **seed-9 boundary preservation** — enforce that private data NEVER routes to a public/trains bucket;
   wire `anonymize-guard` on anything outbound. (zone-filter exists; enforcement + guard owed.)
4. **self-improvement loop (stronger seed-5)** — crystallize BEHAVIORS from Luis's real use (not just
   paths/tools), so the entity gets measurably better at being *his* assistant over time.
5. **restartability** — survive a crash/reboot from the persisted capsule + `grid_state.json` (the
   state persists; prove a cold restart resumes correctly).

---

## MILESTONES (ordered)

1. **Resilient grid operator** (429-reroute, non-blocking, adaptive) — ✅ DONE (`test_resilient.py`).
2. **Wire the resilient draw as the swarm's standard call path** — every agent call auto-reroutes; no
   single 429 can ever stall the swarm. (Small wiring job on top of step 1.)
3. **Phase 4 — the first real useful task that SHIPS + self-improves:** a daily brief on the free grid
   (fetch relevant AI news + project status + one opportunity; crystallize what Luis marks useful so
   tomorrow's brief is sharper). Proves op:ship + the self-improvement loop + the resilience thesis at
   full scale.
4. **Scheduling** (unattended cron run) + **boundary enforcement** (private → no-train/local only).
5. **The companion loop** — the entity continuously crystallizes behaviors from Luis's use and improves.

**When 1–5 are proven, the entity is truly autonomous:** it runs itself on free compute, survives its
own limits, ships useful work, stays in its lane, and gets better — without needing paid AI. That is
the AEA, alive, and a companion for Luis.

**The discipline (unchanged):** every milestone past #2 must produce real USE, not more mechanism.
The machinery is now largely built and proven; the project earns its keep only when it does Luis's work.
