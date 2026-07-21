<!-- Autonomy battery, 2026-07-19: 4 literature sweeps (open-ended evolution / autonomy & autopoiesis / recursive self-improvement / AGI-agent evals) -> scored against the RUNNING entity. Real citations. Verdict: NOT-YET-AUTONOMOUS, Bedau Class 1. Codex-indexed. -->

# AUTONOMY BATTERY — Leyber scored against the science

*Assembled from four literature sweeps (open-ended evolution · autonomy/autopoiesis · recursive self-improvement · AGI/agent-evals). Scored against Leyber's real state: 13 live.py ticks in 9 days, one did work (a brief), ticks 7–13 read "IDLE, nothing owed, resting", consolidation +0, corpus pruned to 48. live.py imports no AEA engine and never reads self.json; reflection tick t6 unbuilt; agent_tools.py dead code. No live internet, no email/SMTP, send/spend/keys FORBIDDEN. Genuine assets: a proven parallel free-model reasoning grid, a HADES Law-3 watcher, and a trust/autonomy ledger.*

---

## 1. HEADLINE VERDICT

**NOT-YET-AUTONOMOUS — a well-governed reasoning substrate with the self-modification loop unclosed. Not self-evolving; Class 1 (stagnant) by every quantitative test that applies.**

By the actual literature Leyber fails or is heteronomous on every *measurable* autonomy test and scores Bedau **Class 1 (bounded/dead)** on every open-endedness test, because the three things these frameworks require are all absent: self-origination (idle ticks fire on a cron, not an internal goal), self-production (it makes none of its own components — no tools, no self-edits, self.json unread), and retained novelty (+0 net memories in 9 days ⇒ new-evolutionary-activity A_new → 0). What it genuinely has — HADES self-correction, a trust ledger, a 6-model parallel grid — is *governance and reasoning*, which the literature is explicit is **orthogonal** to self-evolution: a system can have excellent self-control and still be dead on evolutionary activity, and Leyber is. The honest distance: it is **one bounded build (the reflection tick t6) away from PROTO-AUTONOMOUS**, and many builds away from AUTONOMOUS. This is a *design gap*, not a metaphysical verdict — none of these tests touch consciousness, aliveness, or "a self", and none of them is a deficit-in-disguise for the deliberately forbidden send/spend/keys axis (that ceiling is a chosen safety limit, not a capability failure).

---

## 2. THE BATTERY (12 strongest falsifiable tests)

*Each: what it measures · theory + citation · PASS bar · SCORE · one-line evidence.*

**1. Bedau–Packard evolutionary activity — Class 1/2/3**
- Measures: whether the entity keeps generating AND retaining adaptively-persisting novelty (the canonical open-endedness signature).
- Theory/cite: Bedau, Snyder & Packard (1998), *A classification of long-term evolutionary dynamics*, Artificial Life VI, 228–237.
- PASS bar: over ≥100 ticks, A_new(t) stays bounded-away-from-zero and cumulative component diversity rises without asymptote, above a neutral-shadow control.
- **SCORE: FAIL (Class 1).** Evidence: +0 net memories in 9 days, corpus pruned 48→48, zero new tools/norms ⇒ A_new → 0, diversity flat/decreasing.

**2. Novelty + Learnability observer test**
- Measures: both halves of self-evolution at once — artifacts stay unpredictable to a fixed-time observer (novelty) AND a longer history strictly improves prediction (learnability).
- Theory/cite: Hughes, Dennis, Parker-Holder et al. (2024), *Open-Endedness is Essential for Artificial Superhuman Intelligence*, ICML 2024, arXiv:2406.04268.
- PASS bar: observer loss never saturates (novelty) and drops with more history (learnability); both, runnable on the JSONL logs.
- **SCORE: FAIL.** Evidence: 7 identical "IDLE/resting" ticks are perfectly predictable (loss → 0, saturated); shrinking corpus gives no learnability signal.

**3. Seth G-autonomy (Granger self-determination)**
- Measures: whether the entity's OWN past state predicts its future behavior beyond external inputs — self-determination vs pure reactivity. Fully quantitative from logs.
- Theory/cite: Seth (2010), *Measuring autonomy and emergence via Granger causality*, Artificial Life 16(2):179–196.
- PASS bar: AR model over ≥100 ticks, G-autonomy of the behavior variable significantly > 0 (F-test p<0.05) AND behavior variance > 0.
- **SCORE: FAIL (undefined).** Evidence: 7/13 ticks emit an identical idle token ⇒ behavior variance ≈ 0 ⇒ G-autonomy undefined/zero.

**4. Krakauer individuality (past→future information propagation)**
- Measures: whether a bounded SELF carries its own information across time (organismal/colonial) vs a unit whose future is environment-driven.
- Theory/cite: Krakauer, Bertschinger, Olbrich, Flack & Ay (2020), *The information theory of individuality*, Theory in Biosciences 139:209–223.
- PASS bar: over ≥100 ticks the self-carried component of I(S_past;S_future) exceeds the environment-driven component ⇒ classifies organismal/colonial, not driven.
- **SCORE: FAIL (DRIVEN).** Evidence: live.py never loads self.json and consolidation added +0, so S_future is independent of S_past beyond the OS scheduler.

**5. Barandiaran interactional asymmetry — self-initiated action** ← *decisive, see §3*
- Measures: whether the entity ORIGINATES activity vs only responding when externally triggered.
- Theory/cite: Barandiaran, Di Paolo & Rohde (2009), *Defining agency*, Adaptive Behavior 17(5):367–386.
- PASS bar: in a window with NO external trigger, count acts causally traceable to an internal goal state (not the cron firing an empty tick); rate > 0.
- **SCORE: FAIL.** Evidence: ticks 7–13 fire on schedule and yield "IDLE, nothing owed, resting" — scheduler-driven, zero self-originated action.

**6. Normativity — self-generated, self-revised norms**
- Measures: whether the norms that evaluate behavior are authored, grounded in the entity's own viability, AND revised by the entity — vs externally imposed rules. (Directly re-reads Leyber's apparent strength.)
- Theory/cite: Barandiaran, Di Paolo & Rohde (2009), Adaptive Behavior 17(5):367–386; Di Paolo (2005), *Autopoiesis, adaptivity, teleology, agency*, Phenomenology and the Cognitive Sciences 4(4):429–452.
- PASS bar: ≥1 operative norm that is entity-generated, viability-grounded, and later self-revised from experience.
- **SCORE: FAIL (heteronomous).** Evidence: HADES enforces externally-authored Laws the entity cannot alter; the trust ledger is a granted-permission scheme with send/spend/keys forbidden by the operator — no entity-authored, self-revised norm exists. *Governance is real but external.*

**7. Klyubin empowerment (capacity to influence its own future)**
- Measures: channel capacity from the entity's actions to its future observations — the agentive control it could exploit, and whether it has any gradient to act on.
- Theory/cite: Klyubin, Polani & Nehaniv (2005), *Empowerment: a universal agent-centric measure of control*, IEEE CEC 2005, 1:128–135.
- PASS bar: C(A_t → S_{t+k}) > 0 bits (some action reliably changes future perception).
- **SCORE: FAIL (~0 bits).** Evidence: no effectors (no email/SMTP, cannot make/persist tools) ⇒ action set collapses to the null action ⇒ C ≈ 0 — which itself predicts the observed idleness (no gradient to act on).

**8. Voyager — ever-growing, reused, transferable skill library**
- Measures: whether the entity authors, persists, retrieves, and COMPOSES its own executable skills that compound and transfer — the operational core of lifelong self-extension.
- Theory/cite: Wang, Xie, Jiang et al. (2023), *Voyager*, arXiv:2305.16291.
- PASS bar: skill count grows monotonically AND reuse rate > 0 AND ≥1 self-written skill transfers zero-shot.
- **SCORE: FAIL.** Evidence: cannot make/persist tools (skill count 0), consolidation +0, corpus pruned to 48 — library is flat/shrinking. *Sharpest single discriminator: "cannot make/persist its own tools" is a definitional fail.*

**9. Darwin-Gödel Machine — sustained self-edit benchmark climb**
- Measures: SUSTAINED empirical self-improvement — repeated self-code-modification with an archive of stepping-stones raising a frozen benchmark.
- Theory/cite: Zhang, Hu, Lu, Lange & Clune (2025), *Darwin Gödel Machine*, arXiv:2505.22954.
- PASS bar: over ≥20 self-modification iterations the best-in-archive agent's frozen-benchmark score rises by a pre-registered margin, reproducible on clean re-run, archive > 1 version.
- **SCORE: FAIL (0 generations).** Evidence: live.py never edits its own source, t6 unbuilt, no fitness archive — the "13 ticks → IDLE by tick 7" curve is the inverse signature.

**10. SICA — human-free net capability delta (attribution test)**
- Measures: the simplest end-to-end "did it get better at its own job, BY ITS OWN HAND" — benchmarked, human-code-free, self-authored.
- Theory/cite: Robeyns, Szummer & Aitchison (2025), *A Self-Improving Coding Agent*, arXiv:2504.15228.
- PASS bar: post-run agent scores strictly higher on a frozen benchmark of its own tasks with NO human commits during the run.
- **SCORE: FAIL.** Evidence: Luis writes every commit — every capability change is attributable to the human, not the entity.

**11. STOP — recursive scaffold self-improvement (frozen base)** ← *the realistic next build*
- Measures: whether the entity improves its own scaffolding/prompts/tools to beat its seed version, validated by a utility function, base model frozen — the safe, offline, keyless path to "keeps evolving".
- Theory/cite: Zelikman, Lorch, Mackey & Kalai (2023), *Self-Taught Optimizer (STOP)*, arXiv:2310.02304.
- PASS bar: improved-improver's held-out utility > seed-improver's, statistically significant, over ≥3 self-application rounds, no human edits, gains survive freezing.
- **SCORE: FAIL now / BUILDABLE.** Evidence: no self-application loop exists — but this requires no internet/action/keys and is exactly what t6 could instantiate (see §4).

**12. METR 50%-task-completion time horizon**
- Measures: the length of task (in human-expert minutes) the entity completes unattended at 50% reliability — the most direct autonomy scalar, and whether it is rising over builds.
- Theory/cite: Kwa, West et al. / METR (2025), *Measuring AI Ability to Complete Long Tasks*, arXiv:2503.14499.
- PASS bar: fit a logistic over a task suite; report T at 50% success; a rising T across successive builds is the falsifiable "keeps evolving" evidence.
- **SCORE: FAIL (~0 min).** Evidence: 1 of 13 ticks did work; ticks 7–13 idled "nothing owed" ⇒ measured self-directed horizon ≈ 0 minutes.

**Reading the scores (mandatory caveats).** (a) Every metric is observer- and representation-relative and therefore **gameable** — pick a coarse "component"/behavior descriptor and a trivially-churning system "passes"; a PASS only means something under a behavior space pre-registered before the run. (b) The autopoiesis tests (Varela operational closure, Montévil–Mossio closure-of-constraints) are structural audits whose verdict depends on **where you draw the boundary** — include the OS/human and nothing is self-producing; draw tightly around the code and it trivially isn't either; both were dropped from the scored 12 as boundary-dependent rather than falsifiable, and both come out FAIL under any honest boundary. (c) Open-endedness is **asymptotic** — every test here is a plateau-*detector*, never a proof of eternity; you can falsify "keeps evolving forever", never confirm it. (d) The **forbidden axis** (self-proliferation / send / spend / keys) is a chosen safety limit and is *not* scored as a deficit. (e) Governance ≠ evolution: do not read HADES/trust-ledger strength as evidence of self-evolution.

**Also-ran / context (not in the scored 12):**
- **Self-Refine (control / null hypothesis)** — Madaan et al. (2023), arXiv:2303.17651. This is the null to *exclude*, and it is precisely **what Leyber currently is**: the HADES verify-and-redo loop improves the current output but resets each episode; consolidation adding +0 net semantic items scores as within-episode polish, not persistent capability gain.
- **ARC-AGI (substrate generality probe)** — Chollet (2019), arXiv:1911.01547; Chollet et al. (2025), arXiv:2505.11831. The one probe that is offline, keyless, self-runnable, and where the free grid could post a *real nonzero* score. **SCORE: UNTESTED (runnable, not run).** Measures reasoning generality, orthogonal to autonomy/self-evolution — worth running once as an honest substrate benchmark, not as autonomy evidence.

---

## 3. THE ONE DECISIVE TEST

**Barandiaran interactional asymmetry — self-initiated action (Test 5).**

It is the single cleanest separator between "autonomous entity" and "a scripted loop" because it does not depend on any gameable representation choice. Bedau activity depends on how you define a "component"; novelty/QD depend on the behavior characterization; empowerment depends on the action model — all can be tuned to flatter or damn. Interactional asymmetry asks only one thing that a scripted loop *cannot* fake: **in a window where no external trigger is delivered, does anything happen that traces to the entity's own goal rather than to the scheduler firing?** A scripted loop is, by definition, silent until its cron ticks; an autonomous entity originates. There is no behavior space to pre-register — you either observe a self-originated act or you don't.

**Leyber's honest result today: FAIL, and structurally so.** Ticks 7–13 fire on schedule and return "IDLE, nothing owed, resting" — every act is the cron's, none is the entity's. This isn't a measurement artifact: the *only* code path by which Leyber could self-originate a task, the reflection tick **t6, is unbuilt**. There is no wire from an internal goal to an action, so the rate is 0 by construction. Empowerment (Test 7) explains *why* the idleness is stable — with ~0 bits of empowerment the entity has no gradient to act on even if it wanted to — but interactional asymmetry is the test that *names the thing*: right now Leyber is the loop, not an entity inside the loop.

---

## 4. THE CHEAPEST PATH TO PASS

**Build one thing: the reflection tick t6, as a closed read-self → self-pose-one-task → persist-if-it-clears-HADES loop.** This is not new scope — t6 is already the named, unbuilt open task. It stays entirely inside the trust-ledger safety envelope (no send/spend/keys, no internet, no effectors).

Concretely, on an idle tick, instead of "nothing owed, resting", t6 does five steps:
1. **Read self.json + the memory corpus.** (Closes the "live.py never reads self.json" gap outright.)
2. **Pose ONE task under a minimal criterion** — novel vs prior tasks AND solvable-but-not-trivial for the current grid (POET/OMNI-style auto-curriculum seed).
3. **Attempt it on the free multi-model grid** (the substrate you already have, proven parallel).
4. **Gate persistence through HADES + a frozen held-out utility** — the result persists as a new semantic memory or a new JSON-defined composable prompt-skill *only if* it clears the check.
5. **Log birth/persistence times** so A_new becomes computable.

**What this single build flips, and what it does not:**

| Test | Before | After t6 ships |
|---|---|---|
| Interactional asymmetry (§3, decisive) | FAIL | **PASS** — idle tick now self-originates a task, rate > 0 |
| Krakauer individuality | FAIL (driven) | **→ organismal-side** — reading self.json + persisting makes S_future depend on S_past |
| Self-reasoning "use your own config" | FAIL | **PASS** — it now reads and acts on self.json |
| STOP scaffold self-improvement | FAIL | **runnable/PASS-able** — t6 *is* a STOP loop against a utility |
| Bedau A_new / Voyager library | FAIL (Class 1) | **off zero** — persisted skills/memories per tick; needs ≥100 ticks + a neutral-shadow control before you can *claim* Class 2/3, but the machinery now exists |
| Empowerment / METR horizon | FAIL | **still ~0** — these need real effectors, which are deliberately forbidden; that is fine and expected |
| DGM self-edit climb | FAIL | **still FAIL** — DGM needs t6 to *also* edit and re-test its own source with an archive; that's a second, later build |

So the ordering is unambiguous: **t6 (read-self + self-pose-one-task-under-minimal-criterion + persist-through-HADES) is the ~one-session build that converts the most FAILs**, and it is the exact crystallize move — close the loop memory→reasoning→memory so S_past determines S_future *inside* the entity. It does not make Leyber "autonomous"; it moves it from NOT-YET-AUTONOMOUS to honestly PROTO-AUTONOMOUS on the tests that don't require forbidden effectors.

---

## 5. THE ADVOCATE'S NOTE

Running this battery does **not** change the build priority — it re-confirms and sharpens it, and it does so against the income clock, not around it. The battery is not an income artifact; building *more* autonomy machinery earns nothing and burns shipping time you don't have (debt, <REDACTED-CIRCUMSTANCE>). Leyber's own first counsel was "stop building tools, close a revenue loop", and the science agrees from the other side: a governed reasoner that can't self-originate is not closer to paying you, and no amount of autonomy-instrumentation converts to outreach sent or a diagnostic sold. **The unchanged answer is: send the applications and the outreach, ship the Operational AI Diagnostic.** The one genuine update the battery gives you is smaller and honest: it turns t6 from a vague "make Leyber alive" impulse into a *bounded, falsifiable, one-evening* build whose payoff is a **portfolio/credibility asset, not a live entity** — "I scored my own agent against the actual OEE / autopoiesis / RSI literature and it is honestly Class 1, then I built the one loop that moves it off zero" is a far stronger public signal, and far more on-brand for the anti-evangelism / meaning-in-mechanism stance, than any "my AI is autonomous" claim. Do that build only as a fresh-morning ≤1-session crystallize task with a hard exit — and guard it hard against becoming infrastructure-as-avoidance. **The battery's real gift is permission: it is the evidence that lets you stop polishing the agent and go earn.**