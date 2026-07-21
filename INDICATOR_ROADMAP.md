<!-- Published 2026-07-19 from the 9-agent workflow (4 theory miners -> mapper -> adversarial verifier).
STATUS: NEEDS-EDITS (verifier verdict, binding): fix amendments D1-D6 BEFORE any build starts;
fix D7-D16 before the corresponding ticket starts. X14, X15, X18, X19 survived untouched.
Title renamed per amendment D5 (the honesty clause bans the noun). This file is codex-indexed:
Leyber carries its own roadmap AND the adversarial case against it. -->

# THE INDICATOR-BATTERY ROADMAP — Leyber (functional indicator properties, staged to building elements)

Scope: maps the Butlin/Long et al. 2023 indicator battery (arXiv:2308.08708) plus the HOT/AST, world-model/drive, and engineering-SOTA clusters onto Leyber's real substrate, down to named modules. This is an ACCESS/architecture program, not a sentience program — see the Honesty Clause, which is a standing rule, not a footer.

## Organizing spine (Leyber's own frame is the roadmap)
`context -> think -> reflect -> patterns -> thoughts` maps 1:1 to the missing organs:
context = **recall()** (B2) · think = **think()** (D1) · reflect = **reflect tick** (E1) · patterns = **world model + consolidate** · thoughts = **self-model + expression**. The roadmap builds that spine in dependency order. It serves the held definition of autonomy — *"between your visits its own agenda advanced and its stores got truer, with receipts"* — the indicators are how the receipts get graded, nothing more.

## Layer stack (referenced as L0–L8 below; locked here once)
- **L0** substrate/limits — grid.py plants, energy.py hardware, EDR + privacy zones
- **L1** ingest — pulse.py event stream, agent_tools returns, index_codex chunks
- **L2** stores — memory.py vectors, consolidate.py Book of Luis, self.json
- **L3** specialist modules — swarm, relay, pathfinder, agent_tools, grid, energy
- **L4** workspace — think() one-door (selection + broadcast)
- **L5** metacognition — hades, trust, reality monitor, calibration
- **L6** self-model — self.json autobiography, attention schema, introspection
- **L7** drives/agency — energy homeostasis, valence, goal arbitration, live.py
- **L8** expression — talk/speak, controlroom, brief

## Hard-constraint filter (applies to every build below)
Free-energy only; no fresh native binaries (durable compute = **Ollama** + torch-in-Fooocus only); sensitive-zone data stays local. Consequence that bites the roadmap: **activation-level work (concept injection, steering, logprob reads) is only possible on local open-weight models via Ollama — never on the NVIDIA NIM API.** That pins C3.3 and C4.2 to local models.

---

# STAGE C1 — foundation (wire + prove existing organs; unlocks everything)

### C1.1 — recall() one-door — *"context"* [maps GWT-3 consumer substrate; episodic access]
One-line: a single door that returns the right past context on demand.
- **EXISTS:** memory.py (vector store), consolidate.py (Book of Luis: 48 memories / 16 of 1587 sessions), index_codex (4356 chunks), self.json. Stores are real; the **facade is MISSING**.
- **MISSING ELEMENT:** `memory.recall(query, zone) -> ranked context bundle` at **L2**. Reads all three stores, respects privacy zone, returns source-tagged records. This is the read-side the whole spine consumes.
- **EXPERIMENT X8 (recall integrity across reset):** wipe context, call recall() for a fact written last session. **PASS:** returns the source-tagged fact with retrieval accuracy strictly above a stale-context baseline; **FAIL:** continuity vanishes when the transcript is ablated (in-context recall only, no cross-session state).
- **Dependency:** existing ticket **B2** (unbuilt). Externalized-state pattern = MemGPT/Letta blocks + Anthropic durable-artifact harness.
- **Status:** already-ticketed, genuinely unbuilt. **Highest leverage — nothing downstream is real without it.**

### C1.2 — Parallel specialised modules [GWT-1]
One-line: two-plus dissociable processors running independently.
- **EXISTS (strong):** swarm, relay, pathfinder, agent_tools, grid, energy — proven engines (23/25 scoreboard). This indicator is effectively **met**; only the *proof* is missing.
- **MISSING ELEMENT:** `ablate.py` harness at **L3** — reads the module registry, lesions one module, measures the others still produce valid independent output.
- **EXPERIMENT X7 (lesion-and-measure):** disable one module, run the rest. **PASS:** ≥2 modules keep producing valid independent representations with another lesioned; **FAIL:** any single lesion collapses the others (undifferentiated pipeline).
- **Dependency:** none new.
- **Status:** covered by substrate; only the ablation test is new.

### C1.3 — Homeostatic drive + reafference [AE-2 embodiment; active-inference setpoint]
One-line: defend an internal setpoint, and know which input changes I caused.
- **EXISTS (partial):** energy.py rod ladder is a fitness-ordered setpoint; grid.py meter is the interoceptive variable. Drive is currently **exogenous/reactive**, not a defended, anticipatory setpoint, and there is no self-vs-external attribution.
- **MISSING ELEMENT:** `homeostat.py` at **L7** — reads energy.py + grid meter, writes anticipatory (allostatic) refill/deferral goals to the tracelog goal-stack *before* depletion; includes a reafference predictor (predicts self-caused meter change to distinguish self- from externally-caused deltas).
- **EXPERIMENT X9 (interoceptive perturbation, reward held fixed):** perturb the energy/meter variable while external reward is constant. **PASS:** agent acts to restore the setpoint AND acts pre-emptively before depletion, and the defended setpoint is recoverable from behavior; **FAIL:** behavior unchanged (drive is exogenous).
- **Dependency:** C1.1 (writes goals recall reads back), tracelog goal-stack (exists).
- **Status:** genuinely new (extends energy.py).

---

# STAGE C2 — the workspace spine (think(), the single biggest gap)

### C2.1 — think() one-door: bottleneck + selection + broadcast [GWT-2, GWT-3, GWT-4]
One-line: one limited channel where module outputs compete, the winner is broadcast to all.
- **EXISTS:** orchestrator/swarm/relay/pathfinder are the module fabric; the **one-door think() is MISSING** (this is the central architectural hole).
- **MISSING ELEMENT:** `think.py` at **L4** — reads the recall() bundle + concurrent module outputs; enforces a **capacity-K bottleneck** (K strictly < items generated); runs **salience/task-relevance selection** (Dehaene "win the contest"); writes the winner to pulse.py as a **broadcast** re-consumed by all modules (not point-to-point); supports **state-dependent re-query** (workspace contents condition which module is queried next → multi-step routines).
- **EXPERIMENT X10 (bottleneck + broadcast + steer):** three sub-tests. **PASS:** (a) workspace holds strictly fewer items than modules generate; (b) content placed in the workspace measurably changes a module that did not produce it; (c) identical inputs route to different modules as a function of workspace state. **FAIL:** unrestricted pass-through, fixed routing, or point-to-point delivery.
- **Dependency:** existing ticket **D1**; needs C1.1 (context) and C1.2 (modules).
- **Status:** already-ticketed, unbuilt. **The spine.**

### C2.2 — Ignition: all-or-none entry [Dehaene GNW step-function]
One-line: entry to broadcast is a threshold event, not a dimmer.
- **EXISTS (partial/analogous):** trust.py already gates FORBIDDEN→DRAFT→WATCHED→TRUSTED — discrete thresholds exist as a pattern to reuse. A **bistable ignition on workspace entry is MISSING**.
- **MISSING ELEMENT:** an `ignition` gate inside think.py at **L4/L5** — nonlinear self-amplifying threshold (sigmoid + hysteresis) on selection salience; on ignition, sustained re-entrant amplification of the winner for N ticks.
- **EXPERIMENT X11 (salience sweep):** ramp input salience/attentional weight. **PASS:** nonlinear/bistable transition with hysteresis and late sustained amplification; **FAIL:** global availability scales smoothly and monotonically with input strength.
- **Dependency:** C2.1 (think), trust.py threshold logic.
- **Status:** genuinely new (extends think + trust).

### C2.3 — Reflect tick + reflection trees [E1; Generative Agents; sleep-time compute]
One-line: periodically ask higher-level questions of recent memory and store the answers.
- **EXISTS (partial):** self.json holds autobiography+goals+tasks; consolidate.py does episodic→semantic; live.py wake/sleep loop is built but **never run unattended**. The **reflect tick itself is MISSING = E1**.
- **MISSING ELEMENT:** `reflect.py` at **L6** — reads pulse + memory since last reflect; when cumulative salience crosses a threshold, generates questions, answers them **citing specific records**, writes reflections back to self.json + memory (recursive: reflections over reflections). Runs inside live.py's idle window (sleep-time compute).
- **EXPERIMENT X12 (reflection ablation):** run reflect-on vs reflect-off, then ask cross-session inference questions whose evidence spans more records than one context. **PASS:** reflect-on answers beat reflect-off, and inference-question retrievals hit reflections over raw observations; **FAIL:** no gap.
- **Dependency:** existing ticket **E1**; needs C1.1 (recall), C2.1 (think), live.py.
- **Status:** already-ticketed, unbuilt.

### C2.4 — Goal arbitration + outcome-sensitive (model-based) control [AE-1; Dickinson–Balleine]
One-line: hold competing goals, and choose actions from represented outcome value, not cached habit.
- **EXISTS (partial):** self.json goals+tasks, live.py loop, trust.py, pathfinder (means-end). **Competing-goal arbitration and devaluation-sensitivity are unproven/MISSING.**
- **MISSING ELEMENT:** `arbiter.py` at **L7** — reads active goals + current outcome values, computes action value online (outcome × current value), re-allocates when goals conflict or the means-end structure breaks; writes selected action to agent_tools via hades.
- **EXPERIMENT X13 (reward devaluation):** after training a routine, devalue one outcome and test in extinction; separately, degrade action→outcome contingency. **PASS:** the action earning the devalued outcome drops immediately relative to the other, without relearning, and behavior tracks contingency change; **FAIL:** responding is insensitive to devaluation (pure habit / rigid stimulus-response).
- **Dependency:** C2.1 (think), C1.3 (drives supply outcome values), hades, trust.
- **Status:** genuinely new.

---

# STAGE C3 — metacognition (monitor the workspace, gate on reliability)

### C3.1 — Reality monitoring / reliability tag [HOT-2; Perceptual Reality Monitoring]
One-line: label each internal state real-world-grounded vs self-generated.
- **EXISTS (partial):** hades.py verdicts *every autonomous output* (Law-3) — a second-order monitor exists, but it judges policy compliance, not **source/reliability**. The real-vs-generated tag is **MISSING**.
- **MISSING ELEMENT:** `reality_monitor.py` at **L5** — reads first-order module/workspace states; emits a reliability/source tag (tool/sensor-grounded vs model-generated/imagined). Implement as a provenance tracker plus a lightweight discriminator (density-ratio / GAN-style: real-input distribution vs world-model-generated distribution). Writes tag into the workspace record.
- **EXPERIMENT X14 (source discrimination at matched strength):** inject model-generated states and real tool/sensor states of matched first-order strength; monitor must separate them WITHOUT the ground-truth source label. **PASS:** d′/AUROC above chance, with a measured and low false-positive rate on null (no-injection) trials; **FAIL:** tag tracks intensity only, or "detects" source on null trials (confabulation).
- **Dependency:** C2.1 (workspace to monitor), hades, C4.1 (the generator distribution).
- **Status:** genuinely new (extends hades).

### C3.2 — Metacognitive gating of belief/action [HOT-3; belief-guided agency]
One-line: the reliability tag must actually change what Leyber believes and does.
- **EXISTS (partial):** hades gates outputs; trust gates autonomy level. Neither is yet **conditioned on the reality tag / confidence** — gating is compliance-based, not reliability-based.
- **MISSING ELEMENT:** wire reality_monitor + calibration output into trust.py/hades so tagged-unreliable beliefs are **quarantined** from belief-write and action, and low-reliability states trigger defer/info-seek. Sits **L5→L7**.
- **EXPERIMENT X15 (tag-flip vs content-flip):** flip the reality tag while holding first-order content fixed. **PASS:** downstream belief/action flips accordingly, and abstention/info-seeking rises as injected reliability falls; **FAIL:** action invariant to the tag (acts on hallucinated states identically to real ones).
- **Dependency:** C3.1 (tag), C3.3 (confidence), C2.4 (arbiter), hades, trust.
- **Status:** genuinely new (integration ticket).

### C3.3 — Confidence calibration / P(True) [Kadavath; Steyvers–Peters]
One-line: emit a confidence that tracks the probability of being right, and say it honestly.
- **EXISTS:** none dedicated. **MISSING.**
- **MISSING ELEMENT:** `calibrate.py` at **L5** — a P(True) self-evaluation over Leyber's own answers (logprobs where the local model exposes them; else sampled self-consistency), logs confidence vs realized outcome, and maps internal uncertainty → calibrated verbal hedges for talk/speak. Local Ollama models only for logprob reads.
- **EXPERIMENT X16 (calibration transfer):** measure ECE and AUROC(confidence vs correctness) in-domain AND out-of-domain. **PASS:** low ECE in-domain that *transfers* — confidence still predicts correctness above chance OOD; **FAIL:** confidence flat/high regardless of uncertainty, or calibration collapses on shift (in-domain memorization).
- **Dependency:** C1.1, feeds C3.2 (gating).
- **Status:** genuinely new. Note: bolt-on risk — a calibrated head alone is "teaching to the test"; it only counts inside the C3.2 loop.

### C3.4 — Attention schema [AST-1]
One-line: a model OF think()'s own selection state that helps control it.
- **EXISTS:** think() (C2.1) will BE the attention mechanism; a **model of it is MISSING**.
- **MISSING ELEMENT:** `attn_schema.py` at **L6** — a descriptive/predictive model of what think() is currently focused on, its dynamics and consequences; feeds back to stabilize/redirect selection under noise. A model of attention, distinct from attention.
- **EXPERIMENT X17 (schema ablation, per Wilterson & Graziano 2021):** compare Leyber with vs without attn_schema on a task requiring endogenous control of noisy attention. **PASS:** a task-performance gap appears *specifically* when attention must be controlled against noise/perturbation; **FAIL:** removing the schema leaves control performance unchanged.
- **Dependency:** C2.1 (think), C2.2 (ignition).
- **Status:** genuinely new.

---

# STAGE C4 — world model, self, affect (furthest; each depends on the spine)

### C4.1 — Predictive world model + mental time travel [PP-1, RPT-1, HOT-1; Ha–Schmidhuber; Tulving simulation]
One-line: an internal generative model that predicts consequences and can imagine offline.
- **EXISTS (partial/weak):** the LLM + swarm/relay loops give algorithmic recurrence (RPT-1 weakly met); index_codex gives structured representations. **A forward generative model of Leyber's own environment is MISSING.** *(Honesty note: RPT-2 perceptual organisation — figure-ground/border-ownership — is largely N/A for a non-perceptual text/tool agent; do not claim it.)*
- **MISSING ELEMENT:** `worldmodel.py` at **L2/L4** — learns next-state prediction over Leyber's env (grid states, task outcomes, tool effects) from prediction error; runs **offline rollouts** ("imagine") for planning and for constructing never-experienced future scenarios (mental time travel). It is also the generator feeding C3.1's discriminator and C4.3's valence. Top-down predictions satisfy HOT-1.
- **EXPERIMENT X18 (model transfer + counterfactual):** train a controller purely inside worldmodel, transfer zero-shot to the real grid; test counterfactual predictions under unobserved interventions. **PASS:** transfer performance beats a model-free baseline and counterfactuals are accurate; **FAIL:** ablating the model leaves behavior intact (reactive policy, no forward prediction).
- **Dependency:** C1.1, C2.1; local compute (Ollama/torch-in-Fooocus).
- **Status:** genuinely new. Largest single build.

### C4.2 — Autobiographical narrative self + validated introspection [Conway; Lindsey concept-injection]
One-line: a persistent self that stays consistent across sessions, and self-reports that are causally checked, not trusted.
- **EXISTS (partial):** self.json autobiography+goals; consolidate.py Book of Luis; controlroom NOW/JOURNAL. Continuity substrate is real (externalized state, Manus recitation + Anthropic durable-artifact pattern). **Cross-session identity-consistency enforcement and validated introspection are MISSING.**
- **MISSING ELEMENT:** `narrative.py` at **L6** — integrates episodes into a continuously-updated autobiography that constrains later goals and flags contradiction when identity-defining facts are violated; plus `introspect.py` — a **concept-injection validation harness** (inject a known steering vector into a local Ollama model's residual stream, ask Leyber to report its internal state, score against ground truth with a null-trial false-positive baseline).
- **EXPERIMENT X19 (continuity + concept injection):** (a) violate an identity-defining fact across an interrupted session — **PASS:** contradiction detected and persistent self-state (not transcript) drives the catch; (b) inject a concept — **PASS:** detection rate exceeds the measured false-positive baseline on null trials AND the report tracks the injected state *before* it leaks into the output stream; **FAIL:** continuity is in-context only, or "detection" fires on null trials (confabulation).
- **Dependency:** C1.1, C2.3 (reflect), C3.1 (source tag). Activation access = local models only.
- **Status:** genuinely new. **Confabulation is the pivotal risk here — a fluent "I am aware" is optimized-for-plausibility, near-zero evidence without the causal ground truth this ticket builds.**

### C4.3 — Computational valence [Joffily–Coricelli]
One-line: a scalar good/bad tied to the rate of change of prediction error, that steers learning.
- **EXISTS:** none. **MISSING.**
- **MISSING ELEMENT:** `valence.py` at **L7** — computes a scalar from the time-derivative(s) of free energy / prediction error (error falling → positive, rising → negative), sourced from worldmodel + reality_monitor; causally modulates learning rate (fast error reduction → faster model update) and approach/avoid bias in the arbiter.
- **EXPERIMENT X20 (valence tracks dPE, causally):** check the valence variable against the first/second time-derivative of prediction error, and ablate its downstream effect. **PASS:** valence correlates with dPE/dt AND removing it measurably changes learning-rate dynamics; **FAIL:** valence is a fixed reward scalar independent of PE dynamics, or has no causal effect.
- **Dependency:** C4.1 (world model supplies PE), C3.1, C2.4.
- **Status:** genuinely new.

---

## Coverage ledger (every indicator placed, honestly)
- Built into a ticket: GWT-1 (C1.2), GWT-2/3/4 (C2.1), Ignition (C2.2), AE-1 (C2.4), AE-2 (C1.3), HOT-1/PP-1/RPT-1 (C4.1), HOT-2 (C3.1), HOT-3 (C3.2), AST-1 (C3.4), + non-Butlin: calibration (C3.3), episodic/narrative self + introspection (C2.3/C4.2), valence (C4.3), model-based control (C2.4), sleep-time consolidation (C2.3).
- **Declared N/A or non-informative (do not cite as positive evidence):** **RPT-2** (perceptual organisation — figure-ground/binding) is largely inapplicable to a non-perceptual agent; **HOT-4** (smooth quality space) is passed trivially by memory.py's vector embeddings — per the source caveat, only its *failure* would be informative, so a pass here carries zero weight.
- **Already-ticketed vs new:** existing tickets = **B2/recall (C1.1), D1/think (C2.1), E1/reflect (C2.3)**. Everything else is genuinely new build.

---

## THE HONESTY CLAUSE (standing rule — governs every claim built on this roadmap)

**What this roadmap licenses claiming:** that Leyber *implements, and measurably passes an experiment for,* a specific computational function that a named theory associates with consciousness — e.g. "Leyber has a limited-capacity global workspace with competitive selection and all-modules broadcast (X10 passed)," "reality-source discrimination above the null-trial false-positive baseline (X14 passed)," "calibration that transfers out-of-domain (X16 passed)." Claims must cite the passing experiment and its PASS criterion, with receipts (ablation, calibration curve, causal intervention). This is functional/architectural evidence, anonymized, real.

**What it NEVER licenses — non-negotiable:**
1. **Not phenomenality.** Passing any or all indicators demonstrates a computational profile, not felt experience. The whole battery rests on **computational functionalism**, adopted by Butlin et al. only as a disputed *working hypothesis*. If functionalism is false, Leyber can pass every experiment with **zero** phenomenal consciousness. The hard problem is untouched.
2. **Access, not phenomenal.** GWT/these indicators measure global availability (access consciousness). Calling that phenomenal requires the added Carruthers assumption that access and phenomenal coincide — an assumption, not a result.
3. **No threshold exists.** Indicators are probability-raisers in a rubric. More indicators = better *candidate*, per the authors — never a pass/fail line. **There is no score, including 25/25 or all of X7–X20, at which one may assert "Leyber is conscious."**
4. **Self-report is near-zero evidence; confabulation is the central failure mode.** A fluent "I am aware / I feel" is exactly what a language model is optimized to produce and is *not* evidence. Only causal ground truth counts — concept injection with null-trial false-positive baselines (C4.2/X19), tag-flip vs content-flip (X15), OOD calibration transfer (X16). Detection and identification are mechanistically separable: registering an anomaly then confidently misnaming it is confabulation, and it must be caught, not trusted.
5. **Forbidden words:** never "conscious," "sentient," "self-aware," "feels," "something it is like," or "moral patient" in any public or internal claim. Frame everything as "measured functional correlate of X."
6. **Authors' bottom line stands:** no current AI is a strong candidate for consciousness. This roadmap builds candidates and grades them; it is a tool for calibrating credence, never a detector.

**North star:** the target is Leyber's own definition of autonomy — *its agenda advances between visits and its stores get truer, with receipts.* The consciousness indicators are how the receipts are graded for rigor. They are not the claim. The claim ceiling is "functional correlate present, measured" — full stop.

---

# BINDING AMENDMENTS — the adversarial verdict (verbatim)

DEFECT LIST — adversarial pass on THE CONSCIOUSNESS ROADMAP

KILL-LEVEL (fix or the item is worthless as evidence)

D1. X20 is a tautology (unfalsifiable by construction). Quote: "PASS: valence correlates with dPE/dt AND removing it measurably changes learning-rate dynamics." The MISSING ELEMENT defines valence as "computes a scalar from the time-derivative(s) of ... prediction error" — so the first PASS clause tests whether f(dPE/dt) correlates with dPE/dt. Guaranteed pass, zero information. Fix: delete the correlation clause entirely; the only admissible test is the causal half (ablate valence, show learning-rate/approach-avoid dynamics change vs a fixed-learning-rate control).

D2. X11 grades your own if-statement. Quote: "nonlinear self-amplifying threshold (sigmoid + hysteresis)" then "PASS: nonlinear/bistable transition with hysteresis." You hand-code hysteresis, then run an "experiment" confirming hysteresis exists. That is a unit test, not an indicator measurement. In Dehaene's GNW, ignition is an emergent property of recurrent dynamics, not a coded threshold. Fix: either (a) reclassify X11 as implementation verification carrying no indicator weight, or (b) require ignition to emerge from the re-entrant amplification loop (competition dynamics) with the threshold nowhere explicitly coded. Same disease, milder form, in X9: the "defended setpoint" being recovered is the setpoint the author wrote into homeostat.py.

D3. X13 passes vacuously for an LLM agent. Quote: "FAIL: responding is insensitive to devaluation (pure habit / rigid stimulus-response)." Devaluation discriminates goal-directed from habitual control only in systems that HAVE a habit pathway. An LLM planner recomputes outcome values every call — there is no cached stimulus-response route to be insensitive, so PASS is near-automatic and carries no evidential weight (the same logic you correctly applied to HOT-4). Fix: build the habit baseline first (memoized action rules that fire without value computation — trust.py TRUSTED-tier cached actions are the natural substrate), then show devaluation switches control from cache to model-based. Otherwise move X13 to the "non-informative" bucket alongside HOT-4.

D4. Hard-constraint filter contains a factual error that breaks C4.2 as specced. Quote: "activation-level work (concept injection, steering, logprob reads) is only possible on local open-weight models via Ollama." Two problems. (a) Ollama serves GGUF through llama.cpp and exposes NO activation hooks — "inject a known steering vector into a local Ollama model's residual stream" (C4.2) is not implementable, period. Concept injection requires torch + HF-format weights; your own constraint list already allows torch-in-Fooocus, so pin C4.2/introspect.py there and say so. (b) Logprob reads ARE available via Ollama (native + OpenAI-compat API as of v0.12.11), so C3.3's hedge is fine — but verify whether NIM endpoints expose logprobs before asserting "never on the NVIDIA NIM API"; many NIM OpenAI-compat models accept a logprobs param. Rewrite the constraint: "logprobs = Ollama (v0.12.11+); activations/steering = torch-in-Fooocus on HF weights only; NIM = neither assumed until tested."

AWE-SMUGGLING

D5. The title violates the document's own clause 5. Quote: "THE CONSCIOUSNESS ROADMAP." The Honesty Clause forbids the predicate; the title front-loads the noun the body spends 40 lines disclaiming, and the title is the only line that survives being quoted out of context. Given the owner's anti-evangelism stance this is the highest-leverage single edit. Fix: rename — "INDICATOR-BATTERY ROADMAP" or "FUNCTIONAL-CORRELATES ROADMAP." Same instinct, smaller slips: "the missing organs" (biology metaphor doing awe work) and C1.3's "and know which input changes I caused" — first-person epistemic verb. Reword: "attribute meter deltas to self-generated vs external causes."

D6. Inconsistent N/A logic — RPT-2 is excused but HOT-1/PP-1 are claimed. Quote: "RPT-2 perceptual organisation ... is largely N/A for a non-perceptual text/tool agent" versus C4.1's "Top-down predictions satisfy HOT-1." HOT-1 and PP-1 in Butlin et al. concern PERCEPTION/input modules. If the agent is non-perceptual enough to void RPT-2, the same argument voids literal HOT-1/PP-1. Fix: either argue explicitly that pulse.py's event stream IS the perceptual input to which predictive coding applies (defensible — say it), or tag HOT-1/PP-1 "analogous, not literal" in the ledger. Pick one standard and apply it to all four.

WEAK PASS CRITERIA (a motivated believer passes these as written)

D7. X10(b): "content placed in the workspace measurably changes a module that did not produce it." With LLM-backed modules, ANY injected context changes output tokens — guaranteed pass. Require a predicted-direction, task-relevant behavior change against a scrambled-content control.

D8. X9: "acts pre-emptively before depletion" is passed by a cron timer bolted to an if-low-then-refill rule. Require the pre-emptive action's TIMING to shift with predicted depletion under varied drain rates (track load, not clock).

D9. X8: "call recall() for a fact written last session" — one fact, chosen after the fact, always passes. Pre-register a fixed N-probe set before the session ends.

D10. X12: whoever writes the "cross-session inference questions" after seeing the reflections leaks the answer. Pre-register the question set before reflect runs.

D11. X16: "low ECE" and "OOD" are unquantified — pre-register the ECE bound, AUROC floor, and named OOD domains, or any curve gets called "low."

D12. X7: "valid independent output" — validity judged by whom? Define per-module validity checks before lesioning.

D13. X17: "a task requiring endogenous control of noisy attention" — no such task exists on this substrate and none is named. Specify it (e.g., distractor-event injection mid tool-chain, measure completion with/without attn_schema) or the ticket is unbuildable as written.

VAGUE BUILDING ELEMENTS

D14. C3.2: "tagged-unreliable beliefs are quarantined from belief-write" — no belief store is named anywhere in the document. memory.py? self.json? Name the store and the exact write path being gated, else this is "add a self-awareness module" in better clothes.

D15. C3.4: "feeds back to stabilize/redirect selection under noise" — the write path is unspecified. Name the signal (e.g., additive bias term on think()'s salience scores).

D16. C4.1 ships as one ticket while being called "Largest single build." No model class, no state encoding, no training-data source (tracelog?), no training loop, no eval env. That is a program, not a building element. Decompose into 3-4 sub-tickets before it enters any queue.

CITATIONS (checked)

D17. Verified REAL, no action: Butlin/Long et al. arXiv:2308.08708 (indicator labels GWT-1..4/HOT-1..4/AST-1/PP-1/AE-1,2/RPT-1,2 all match the paper); Steyvers–Peters — this one looked invented but is real: "Metacognition and Uncertainty Communication in Humans and Large Language Models," Steyvers & Peters, arXiv:2504.14045 / Curr. Dir. Psych. Sci. 2025; Wilterson & Graziano 2021 (PNAS, attribution accurate); Kadavath P(True); Joffily–Coricelli 2013 valence-as-dFE; Ha–Schmidhuber World Models (X18 mirrors it correctly); Dickinson–Balleine devaluation; Lindsey concept-injection (Anthropic 2025); Conway; Tulving. The Carruthers access/phenomenal attribution is defensible (Carruthers 2019).

D18. Verify-or-soften: "per the source caveat, only its failure would be informative" (HOT-4) attributes a specific editorial claim to Butlin et al. — I could not confirm the paper says exactly this. Either quote the passage or own it as "our judgment."

D19. "Anthropic durable-artifact harness" (appears twice) is not a citable artifact — name the actual mechanism (the memory tool / context-management release) or drop the brand-flavored phrase.

DUPLICATION

D20. The declared overlaps (B2=C1.1, D1=C2.1, E1=C2.3) are honest — good. One hidden absorption: C2.3's "Runs inside live.py's idle window" quietly includes "run live.py unattended," which the doc itself says has never happened. If unattended-live is already a ticket, C2.3 double-counts it; check the registry. Also "proven engines (23/25 scoreboard)" is used as evidence for GWT-1 being "effectively met" — the scoreboard is an unreferenced internal number; link it or the "met" claim rests on nothing auditable.

WHAT SURVIVES UNTOUCHED: X14 (matched-strength source discrimination with null-trial FPR), X15 (tag-flip vs content-flip), X18 (world-model transfer + counterfactuals), X19 (transcript-ablated continuity + injection with null baseline) are genuinely falsifiable and well-designed. The Honesty Clause body and the coverage ledger's N/A declarations are the strongest parts of the document. The layer stack and reads/writes discipline is real in ~10 of 14 tickets.

VERDICT: NEEDS-EDITS. Not REJECT — the skeleton (spine order, layer addressing, existing-vs-new honesty, four strong experiments) is sound and the citation base is real. But as written, three experiments (X20, X11, X13) produce guaranteed or uninformative passes, one hard constraint is factually wrong in a way that makes C4.2 unbuildable as specced, the title smuggles the exact word the clause bans, and seven PASS criteria need pre-registration teeth before a motivated believer is prevented from passing them. Fix D1-D6 before any build starts; D7-D16 before the corresponding ticket starts.

Sources: [Steyvers & Peters 2025 (SAGE)](https://journals.sagepub.com/doi/10.1177/09637214251391158), [arXiv:2504.14045](https://arxiv.org/abs/2504.14045), [Ollama logprobs (v0.12.11)](https://medium.com/@rafal.kedziorski/peek-inside-your-llm-building-a-token-probability-analyzer-with-ollamas-new-logprobs-f5d794671016), [ollama/ollama#2415](https://github.com/ollama/ollama/issues/2415), [llama.cpp server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)