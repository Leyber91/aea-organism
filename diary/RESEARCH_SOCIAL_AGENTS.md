# RESEARCH - who has actually made simulated conversation work

*2026-07-30. Luis: "I think that some people have tried this before, and they succeeded. We need to
search why they did it, how they did it." Fifty-six agents, five lenses, every cited paper handed to
a separate agent told to REFUTE it - that field is full of systems that sound real.*

## THE THREE THINGS THAT CHANGE WHAT WE BUILD

1. **Nobody has published a sustained four-way SPOKEN conversation that holds.** Every success is
   short, framed, textual, or interview-format. We are not behind a solved problem; we are at the
   edge of an unsolved one. Plan accordingly and do not wait for a recipe.

2. **Our personas are the worst-measured condition.** One-line "filter prompts" are literally the
   demographics-only condition: 74% of the human test-retest ceiling against 83% for
   interview-grounded seeds. The fix is writing, not architecture, and it costs an afternoon.

3. **Almost every extra model call is FREE.** An utterance is 10-15 seconds of TTS audio, so
   everything except the current speaker's generation runs in the SHADOW of the previous
   utterance's playback. Only ONE generation is on the critical path per turn. Bids, impressions,
   reflection, probes and filtering are all free if the loop is a producer/consumer around the
   audio queue. This inverts how expensive the whole ladder below looks.

## THE ONE UNAMBIGUOUS SUCCESS, AND WHAT DID THE WORK

CICERO: 40 anonymous Diplomacy games, 82 human players, 5,277 messages, no in-game message
indicating suspicion, over 2x average human score. **The mechanism was not the language model.** It
was an INTENT CHOSEN OUTSIDE THE MODEL that every utterance had to serve, plus a filter cascade
that discarded ~24% of candidates. Intent-grounding alone moved plan-consistency 76.19 -> 92.86.

The counterweight that keeps this honest: Park's PAID HUMAN CROWDWORKERS writing in character
scored TrueSkill 22.95 - BELOW an agent with nothing but an observation log at 25.64. Authored
characterisation is necessary and nowhere near sufficient.

---

# THE PLAN - Four Voices That Hold

---

## 1 - WHO SUCCEEDED, AND HOW NARROWLY

**CICERO** is the only unambiguous pass: 40 anonymous Diplomacy games, 82 human players, 5,277 messages, no in-game message indicating suspicion, >2x average human score [DOCUMENTED, Science 378:1067]. The mechanism doing most of the work was not the language model - it was an **intent chosen outside the model** that every utterance had to serve, plus a filter cascade that discarded ~24% of candidates at 65% recall. Intent-grounding alone moved plan-consistency 76.19 -> 92.86 and "notably high quality vs average human" 20.64 -> 37.30.

**Social Simulacra** hit a 41% error rate against a 50% ceiling on contamination-controlled data, beating human crowdworkers faking threads (32%) - with a scheduler that was pure arithmetic (p~N(0.65), 8-reply cap, 50% new speaker) [DOCUMENTED, UIST '22].

**HUMA** ran a four-person group chat with one AI and got near-chance detection - but humans in the control were correctly identified only 46.7% of the time, so the discrimination task itself was weak [DOCUMENTED, arXiv 2511.17315, preprint].

**Jones & Bergen**: GPT-4.5 judged human 73% of the time *with* a persona prompt, 21% without [DOCUMENTED].

Honest reading: every success is **short, framed, textual, or interview-format**. CICERO had stake, consequence and anonymity handed to it by a game. Social Simulacra generated threads, not conversation. Nobody has published a sustained four-way *spoken* conversation that holds. Two mechanisms recur across all of them: an externally-chosen goal the utterance serves, and a rich first-person seed. Neither is a bigger model.

---

## 2 - THE MECHANISM LADDER

**The cost insight that governs everything below.** An utterance is ~10-15 seconds of TTS audio. Every call except the *current* speaker's generation runs in the shadow of the previous utterance's playback. Budget in wall-clock latency, not calls: only one 8B generation is on the critical path per turn. Bids, impressions, reflection, filtering and probes are all free if pipelined. Design the loop as producer/consumer around the audio queue before anything else, or every rung below reads as expensive when it is not.

### Above the line - a weekend, near-zero per-turn cost, attacks all three causes of the eight-turn wall

**L0 - Prohibition block + mechanical loop detector**
Write CAMEL's four named failures as explicit negative constraints in every persona prompt: never thank another speaker for their contribution, never announce what you are about to say instead of saying it, never restate the previous speaker before responding, never ask a question you are about to answer yourself. Add a non-LLM detector: if the last N utterances exceed a lexical-overlap threshold or contain only acknowledgement acts, force a topic change or Keep Silent.
*Cost:* ~20 lines of prompt, one regex pass. Zero calls.
*Fixes:* flake replies ("that's a great point, let me think about that"), mutual-thanking loops, the acknowledgement filler that almost certainly dominates turn 9.
*Evidence:* CAMEL (NeurIPS 2023) documents all four from observed runs, including cases where both agents recognise the loop and cannot exit. [DOCUMENTED - but note CAMEL never measured believability; this is a diagnostic taxonomy, so the fix is INFERENCE.]

**L1 - Replace one-line "filter prompts" with long first-person seed documents**
Each voice gets (a) a multi-paragraph first-person transcript - how it talks, what it has done, what it believes, what it refuses, built from concrete incidents not adjectives - and (b) a separate list of **15-30 atomic, checkable statements** ("I distrust institutions", "I was a field medic", "I never swear"). Bias statements toward the concrete: Dialogue NLI's contradiction reduction was 32.5% -> 8.96% on possessions but only 8.0% -> 5.7% on abstract attributes.
*Cost:* one afternoon of writing. Zero runtime calls. Context only.
*Fixes:* the current setup is literally the demographics-only condition, the worst one ever measured.
*Evidence:* interview-grounded 83% vs demographics-only 74% of the human test-retest ceiling, n=1,052 [DOCUMENTED, arXiv 2411.10109 v3]. Jones & Bergen's 73% vs 21% was driven by the persona prompt, not the base model [DOCUMENTED].
*Counterweight, do not skip it:* Park's paid human crowdworkers writing in character scored TrueSkill 22.95, **below** an agent with nothing but an observation log at 25.64. Authored characterisation alone does not finish the job. L1 is necessary and insufficient.

**L2 - The probe harness. Buys zero believability. Still rung 2.**
Every 4 turns, fork each voice's context, inject a fixed probe, score the response with a **deterministic Python function** (a lexical tic that must appear, a stance it must not abandon, a format rule, a fact it must hold), log, discard the fork. No judge, no rater. Probe **relational and preference** dimensions, not "who are you?" - drift concentrates at Relational +0.63 and Coding-Self +0.61 vs flat Identity +0.09 on a 0-3 rubric.
*Cost:* 1 forked 8B call per voice per 4 turns, in the audio shadow.
*Fixes:* nothing. It converts "it degrades around turn eight" into a curve, and every rung below is judged against whether it moves that curve right. Without it you will ship prompt tweaks and believe they worked.
*Evidence:* Li et al., COLM 2024 (arXiv 2402.10962) - significant drift within 8 rounds, stability ~0.9 -> ~0.6-0.7 by round 8. ContextEcho (arXiv 2605.24279) for the probe suite shape and the snapshot-then-probe pattern.

**L3 - System-prompt repetition, placed at the END of the context**
Re-inject each voice's persona block and its currently-relevant statements immediately before its own generation, at the tail of the prompt, not only at the top.
*Cost:* ~200-400 tokens × 4 per turn. You are rebuilding the prompt anyway.
*Fixes:* the measured cause of the eight-turn wall - attention to system-prompt tokens holds *within* a turn and drops sharply *across turn boundaries*, so position at the boundary is what matters.
*Evidence:* Li et al. - π(t) "remains almost constant" within a turn, "significant decreases across turns"; SPR is a studied baseline that works at a capability cost. Split-softmax is better but needs attention access the hosted rods do not give. Restate only the **active** subset (statements relevant to the current topic), keeping the rest as passive contradiction-checks - dumping all statements in every turn is APC's worst-performing memory condition.
*Measure the cost:* SPR trades stability for capability. The probe curve from L2 must be read against a capability check, not alone.

**L4 - One voice per rod, and one voice made immovable**
Put at least one of the four on the 49B and one on the 550B. Then write into exactly one voice's prompt that it does not move on the session's central question.
*Cost:* zero build. Changes the latency profile - which is a feature, since uniform response timing is itself a tell.
*Fixes:* convergence at the weight level, which no system prompt reaches. Sycophancy is RLHF-trained-in, so four voices on one model share the trait; a prompted personality cannot change what the preference model rewarded. Measured capitulation under bare challenge: 32% (GPT-4) to 86% (Claude 1.3), with false admission of a non-existent mistake up to 98%, unchanged when restricted to answers the model was >=95% confident about [DOCUMENTED, arXiv 2310.13548].
*Evidence for the immovable voice:* Ashery et al. (Sci Adv 2025) - a same-model population converges to a shared convention by default, and the committed-minority fraction needed to flip it ranges 2% to 67% by model. At N=4 you cannot express 2%; the equivalent move is one hard-coded holdout.

> **HARD LINE.** L0-L4 cost roughly one weekend, add almost nothing per turn, and attack all three measured causes of the eight-turn wall (drift, convergence, no pursuit). Do not build anything below this line until the L2 probe curve shows they landed. If L1 alone moves the curve as much as everything below, the architecture work is not where the believability is - and finding that out now is worth more than the rest of this document.

### Below the line - real engineering, in this order

**L5 - One central scheduler (never per-voice self-selection)**
A single external component picks the next speaker. Composition: (a) each voice submits a **0-4 urgency bid** with Werewolf Arena's exact anchors, level 4 reserved for "someone addressed me directly"; (b) tie-break weighted toward whoever was mentioned last turn; (c) a per-voice-per-strategy **recency penalty** min(1, k/N) over a small fixed move set (agree-and-extend, challenge, ask-for-detail, bring-in-a-quiet-voice, tell-a-story, Keep Silent) so nobody repeats a move; (d) an FSM constraint - after A addresses B, A may not immediately speak again; (e) a 50% chance the next turn comes from a voice not yet in the current exchange; (f) a **patience counter** per voice, ~6-8, reset on speaking or being addressed, decremented otherwise; (g) every generated turn is a structured object `{speaker, addressee: name|room|null, expects_response: bool}` - **emit** the addressee, never infer it.
*Cost:* 4 single-digit 8B calls per turn, all in the audio shadow. The FSM, the recency penalty and the patience counter are arithmetic.
*Fixes:* ping-pong lock-in between two voices, dominance, mechanical equality, the round-robin fallback showing through on the ~80% of turns with no explicit addressee.
*Evidence:* Meta's MultiLIGHT measured the three architectures directly - dedicated central speaker model 54.4% next-speaker accuracy from dialogue history, joint 49.5%, **N independent silence-or-utterance decisions 35.8%**, the worst, and the collapse was architectural not capacity (that was the 2.7B model). Conditioning generation on **all four** persona descriptions plus a speaker-labelled transcript took mistaken identity from 25.5% to 2.2% [DOCUMENTED, arXiv 2304.13835]. Addressee-recognition base rate ~20% explicit, GPT-4o barely above chance [DOCUMENTED, arXiv 2501.16643]. HUMA's Keep Silent + min(1,k/N). Social Simulacra's 50%-new-speaker and 8-reply cap. Roundtable/Dunbar for patience.
*Note:* do not quote 85.0% as the ceiling - that figure required showing the model the utterance whose speaker it was predicting, which a live system does not have.

**L6 - The persistent per-voice store** - full spec in §3.
*Cost:* 1 importance call + 1 embedding per record written; retrieval is pure arithmetic.
*Fixes:* impressions dying on process exit. Right now the system runs the no-memory ablation, TrueSkill 21.21 - **below** the human-authored baseline of 22.95.
*Evidence:* the observation memory stream is the single largest ablation delta, 21.21 -> 25.64 [DOCUMENTED; the +4.43 decomposition is arithmetic on published means in a fixed removal order, so read it as an ordering, not a separable effect size].

**L7 - Intent + candidate filtering (CICERO-lite)**
Each voice carries a private, persistent **intent** chosen outside the model - a stance to defend, a fact to extract from a named other, a favour to ask, a subject to avoid - written to its store so it survives exit. Before speaking, one cheap call asks whether the last utterance warrants abandoning the intent; if so, rewrite it from this moment. Generate k=4 candidates on the 8B; drop any that does not advance the intent, contradicts a stored statement or commitment, or repeats a phrase already used; pick the survivor.
*Cost:* 4 short generations + 1 filter pass. Absorbed by the audio window if pipelined.
*Fixes:* the actual disease. Every utterance's current intent is "keep talking", so nothing accumulates and turn 9 is thin.
*Evidence:* CICERO's intent-grounding ablation on 126 expert-annotated situations (game-state grounding -> intent grounding): consistent-with-plan 83.33 -> 92.86, notably-high-quality-vs-human 29.37 -> 37.30; the filter cascade dropped 24% of messages at 65% recall and experts preferred survivors 62% of the time (p<0.05) [DOCUMENTED]. The planning half of Generative Agents is *not* the model here - that scored +1.24 and cost the most; take only the standing-intent and react-or-replan kernel [INFERENCE].

**L8 - The knowledge ledger - code-owned, zero model calls**
For every fact introduced, record which voices were present when it was said. Inject a one-line mental-state reminder into the speaking prompt: "Nadia was not present when X was said; she does not know it."
*Cost:* zero calls. A dict.
*Fixes:* the tell that everyone knows everything. Has nothing to do until L6 or L11 creates asymmetry - write the code any time, enable it then.
*Evidence:* FANToM strict all-question-types - human 87.5, GPT-4+CoT 26.6 [DOCUMENTED]. SimpleToM: >95% mental-state accuracy but 49.5% behaviour prediction; feeding the model its own mental-state answer back lifts it to 82.8, while a system-prompt nudge does nothing (49.5 -> 47.3) [DOCUMENTED]. You have perfect ground truth about who heard what. Spending it on a model that scores 26.6 is the mistake.

**L9 - Scored predictive impressions**
Per ordered pair (observer, target), keep **k=3** hypotheses, each a sentence plus a float: "X will deflect when money comes up." Before the target speaks, the top hypothesis emits a one-line prediction. After, a cheap judge marks hit/miss. Update `V ← V + 0.3-(r − V)` with r = ±1; promote at V >= 0.7; drop the lowest and generate a replacement.
*Cost:* (3+k) 8B calls per pair per update, dropping to 2 once validated. Update every 4 turns, not every turn: 4 voices × 3 targets is the dominant background cost - never on the 550B.
*Fixes:* the rebuilt-summary impression, which is literally `top_k=0`, the categorically worst setting in the published sweep. Also produces the only honest live number available - prediction accuracy per pair - and prediction **error** is the resource: a voice confidently wrong about another is exactly the friction eight turns of polite summary lacks.
*Evidence:* Hypothetical Minds, ICLR 2025 (arXiv 2407.07086). The ablation ladder shows the gain lives in the **evaluation and refinement** steps, not in having a model of the other. Constants (α=0.3, V_thr=0.7, k default 5, diminishing past 3) verified; check the repo before hardcoding. Altera's validation is directly runnable here: perceived vs true state regressed r=0.646 at one observer, 0.807 at five-plus, slope ~0.37 - do not trust an impression built from one exchange.
*Split cadence (ToMnet):* a slow `character` field rebuilt rarely from all past sessions, a fast `stance` field rebuilt every few turns. Never at the same cadence.

**L10 - Reflection**
Accumulate importance per voice; on threshold, run two stages - "what are the 3 most salient high-level questions about the subjects in these statements?", then each question as a retrieval query, then "what 5 high-level insights can you infer? (example format: insight (because of 1, 5, 3))". Write insights back into the same stream as first-class retrievable records **with their citations**.
*Cost:* ~4 calls per firing on the 49B, entirely off the speaking path.
*Fixes:* a voice that can only echo the transcript. With reflection, a voice arrives at turn 20 holding a conclusion nobody said out loud.
*Evidence:* +3.01 TrueSkill, second-largest component [DOCUMENTED]. Retune the threshold: 150 is calibrated to their event rate at 2-3 firings per game day. Target every 6-10 turns. Keep the citation format - it is the free audit trail that catches a hallucinated reflection against the transcript.

**L11 - Real repair through the real whisper loop**
Route each voice's *input* through the actual whisper transcript of the others' TTS audio, not the clean text. Give each voice private facts from its own store that the others lack.
*Cost:* zero extra calls. The ASR errors are free and genuine.
*Fixes:* perfect mutual comprehension. Target ~1 other-initiated repair per 1.4 minutes with the three initiator types present (open "huh?", restricted "who?", candidate-understanding "you mean X?").
*Evidence:* Dingemanse et al. (PLoS ONE 2015), 12 languages across five continents. This is the only repair mechanism that satisfies an honesty law - the misunderstanding is a true system event, not a performed one.

**L12 - Floors as a data structure (schism, side sequences)**
Represent active floors as a list of member sets, not one global queue. At patience zero, a voice opens a two-person side sequence for 2-4 turns rather than waiting.
*Cost:* near-zero compute. Expensive in audio plumbing - two simultaneous streams on CPU means two TTS processes or serialising the split and accepting no true overlap.
*Evidence:* Dunbar's ~4 is the fission boundary; a four-voice floor sits exactly where real groups start splitting. [The believability payoff is INFERENCE - neither Dunbar nor the Roundtable evaluated believability.]

**L13 - Planning.** Do not build. See §6.

---

## 3 - THE MEMORY DESIGN

### Files

`state/voices/<name>.json` - one per voice, plus a shared `state/session/<id>.json`.

```
voice.json
  seed              : str            # L1 long first-person document. Static, authored.
  statements        : [str]          # 15-30 atomic checkable claims. Static.
  identity          : {              # cross-session, consolidated, small, ALWAYS queried
      traits        : [str],
      beliefs       : [str],
      commitments   : [{text, first_turn, session_id, survived_regen: bool}],
      character_of  : {other: str}   # slow-cadence impression, rebuilt rarely
    }
  stream            : [MemoryRecord] # episodic, session-scoped, consolidated on exit
  impressions       : {other: {
      hypotheses    : [{text, V: float, hits: int, misses: int}],   # k=3
      last5         : [{turn, gist, i_agreed: bool, it_landed: bool, affinity}],  # FIFO, len 5
      stance        : str            # fast-cadence, rebuilt every ~4 turns
    }}
  intent            : {goal: str, since_turn: int, revisions: [str]}

MemoryRecord = {
  id, text, kind: observation|reflection|commitment,
  t_created: turn_index, t_accessed: turn_index,
  importance: int 1-10, embedding: [float]|null, cites: [id]
}

session.json
  turns   : [{n, speaker, addressee, text, facts: [fact_id], present: [name]}]
  ledger  : {fact_id: {text, introduced_turn, heard_by: [name]}}   # L8, code-owned
```

The `last5` FIFO is deliberately five structured rows, not prose. Ashery et al. showed H=5 structured rows - own choice, partner choice, outcome, running score - is enough to generate genuine population-level social dynamics. It is cheaper and better-defined than a transcript re-read, and it survives process exit as-is.

### Retrieval at speaking time - three separate channels

Do not merge these. ID-RAG's result is that the identity channel must be queried **inside** the decision loop, not summarised into a preamble at load.

**Channel A - identity (no scoring, always injected, placed at the END of the prompt).**
The seed, plus the **active** subset of `statements` - those relevant to the current topic. Score relevance by embedding cosine against the last 3 turns, take top-k (start k=6). The remainder stay passive: never injected, only used as premises for the output-time contradiction check. This is APC's active/passive split, and it is what gives you re-anchoring without recitation. Plus all `commitments` from `identity` (these are few and always relevant).

**Channel B - episodic (Generative Agents scoring, retuned).**

```
score = 1.0*recency + 1.0*importance + 1.0*relevance     # all alphas = 1
each term min-max normalised to [0,1] across the candidate set, THEN summed

recency    = 0.977 ** (turns_now - t_accessed)
importance = record.importance / 10
relevance  = cosine(embed(query), record.embedding)
```

Retrieval refreshes `t_accessed`, so used memories stay hot - that single detail is what makes a callback to turn 6 at turn 28 feel earned rather than random.

**Do not copy 0.995.** It is per sandbox *game hour*, half-life ln(0.5)/ln(0.995) ≈ 138 hours; over their whole 2-day run 0.995^48 = 0.79, so recency barely moved their ranking. Per *turn* it is effectively uniform and the term does nothing. **0.977 per turn gives a half-life of ~30 turns**, roughly one conversation. Tune against the L2 curve; this is the one constant you must own. [The retuning is INFERENCE; the mechanism is DOCUMENTED.]

Importance is one short call at write time using the verbatim 1-10 poignancy prompt with its 2/8 calibration anchors, on the 49B. It runs off the speaking path.

**Channel C - relationship (two fixed queries, per interaction, never cached).**
Run against the speaker's own stream: `"What is <A>'s relationship with <B>?"` and `"<B> is <B's current stance>"`. Summarise the retrieved records into a paragraph. Inject alongside the `last5` rows verbatim and the top hypothesis about B rendered as a prediction ("you expect Nadia to deflect on cost"). No affinity float - see §6.

### Embeddings

Needed for the **relevance** term, the **active/passive** split, and **Summarize-and-Forget** clustering. Three separate mechanisms depend on them, so add them: a small local sentence encoder on CPU (all-MiniLM-L6-v2, 384-dim, ~80MB is the standard choice). **No vector DB.** At four voices and one session the stream is hundreds to low thousands of rows; brute-force numpy cosine over that is trivial. Installing a vector store here is infrastructure-as-avoidance.

Without embeddings, fall back to token-overlap or BM25. What breaks: paraphrased callbacks are missed entirely - a voice will fail to recall "she said money was tight" when the current topic is "the budget", which is precisely the failure that reads as *not actually remembering*. Recency and importance still work, so the store degrades to a chronological log with salience. Usable for L6 as a stopgap, fatal for L7's contradiction filter and L9's stance retrieval.

### Consolidation

**Every ~8 turns (background, 49B, off the speaking path):** reflection fires if accumulated importance crosses the retuned threshold; `stance` rebuilt per pair; hypothesis values updated.

**On exit - four steps, in order:**

1. **Regeneration filter.** For each first-person claim the voice made this session, mask it and regenerate that slot from the surrounding context on the same rod; ask the 49B whether original and alternative contradict. If they do, the voice never held that belief - it improvised it. **Only claims that survive become `commitments`.** Everything else stays episodic and dies. This is what stops you persisting noise, and improvised beliefs are exactly what contradict at turn 40. [ChatProtect: ~80% F1 detection, up to 89.5% removal, prompt-only, black-box - DOCUMENTED.]
2. **Summarize-and-Forget.** Cluster the session's new records by embedding similarity, summarise each cluster into a higher-level record, then delete older records whose embeddings closely resemble newer ones, governed by a single threshold θ ∈ (0,1). This bounds the store instead of letting it grow linearly. θ is the one knob.
3. **Promote.** Hypotheses with V >= 0.7 fold into `identity.character_of[other]`. Hypotheses below the floor are dropped, not archived.
4. **Reflections** are already in the stream with citations; carry the ones whose cited records survived step 2.

**On boot:** load `seed`, `statements`, `identity` (traits, beliefs, commitments, character_of), and validated hypotheses. **Do not load the raw prior transcript.** LOCOMO measured that shortcut: humans 87.9 F1 on recall over 300-turn / up-to-35-session conversations, GPT-4-Turbo at 4K ~32.1, best RAG/long-context ~41.4. Feeding the transcript back is not a fix.

---

## 4 - THE TELLS, RANKED BY LOUDNESS

1. **All four converge into one voice.** Same register, same clause length, same hedges, same rhythm - different TTS timbres carrying identical prose. Three independent causes stack: shared weights, attention decay across turn boundaries, and RLHF-trained sycophancy that no prompt overrides. This is the loudest and it is the one L1-L4 exist for.
2. **Nobody holds a position.** In multi-agent deliberation, 29% of answer changes are strict conformity - changing because peers disagree, independent of argument quality - and conformity is 57-77% correct-to-wrong. Even *vacuous* arguments draw 20-39% error adoption among agents classified as resistant. Four voices that never end a topic still disagreeing is the second-loudest tell.
3. **Perfect mutual comprehension.** Zero repairs across thirty minutes. Humans repair once per 1.4 minutes in every language studied. A group that never once says "wait, what?" is not a group.
4. **Mechanical turn-taking.** Equal turn shares, uniform gaps, strict serialisation, no overlap, no long silence. Real multi-party talk is faster and more overlapping than dyadic, and real groups are *unequal* in a way that is stable - "quietest self-selects" actively enforces the opposite.
5. **Everyone addresses the room.** ~20% of real turns carry an explicit addressee; the other 80% are established by gaze, prosody, sequential position and epistemic authority. A system that either names or doesn't has no third mode.
6. **Acknowledgement filler and flake replies.** "That's a great point, let me think about that." Announcing a contribution instead of making it. Mutual thanking that neither party can exit.
7. **Facts evaporate.** Multi-round deliberation erases 21.7-72.4% of issue-critical facts at system level (60.5-84.8% per agent) against 19.2% for a no-interaction control - so the loss is caused by the interaction, not by summarisation. The conversation gets more agreeable and less informed simultaneously.
8. **Everyone knows everything.** No information asymmetry, so no gossip, no coalition, no "she doesn't know that yet", no reason to explain anything to anyone.
9. **No side sequences, no schism, no re-merge.** Four is the fission boundary; a floor that never splits in half an hour is structurally impossible.
10. **Nobody is ever surprised.** No one predicts another wrong, so nothing is discovered and nothing is revised.
11. **Register formality.** Instruction-tuning makes agents excessively polite and cooperative and pushes the register formal - Park reported this as his own failure mode.
12. **Response length inflation.** Turns get measurably longer as context fills - 2.27x to 10.12x against a length-matched filler control. A conversation where every turn is longer than the last is a machine warming up.

---

## 5 - THE EVALUATION PROTOCOL

**Refuse automatic overlap metrics outright.** BLEU-4 against human dialogue judgment: Pearson 0.1392 (p=0.17) on Twitter, 0.1132 (p=0.26) on Ubuntu, embedding-average *negative* at −0.1631. Any number of that family is noise.

**Frozen material.** 10 scenarios × 30 turns, 3 runs each = 30 transcripts per rung. Fix these before the first rung and never change them; a changed scenario set invalidates every prior comparison.

**Two controls, non-negotiable.**
- **No-interaction control.** Same four personas, same opening, no cross-talk. Four extra generations per scenario. 37% of position changes occur under self-reflection *alone*, so this is the floor any "the impressions improved it" claim must beat.
- **Length-matched filler control.** Replace the transcript with lorem-ipsum padded to the same character count and re-probe. If a voice degrades there too, the problem is context length, not persona, and no prompt will fix it.

**Tier 1 - automatic, free, nightly, honesty-law-legal.** All computed from real transcripts:
persona probe stability vs turn index (L2) - function-word coordination matrix over the eight LIWC classes, ordered pairs only, **aggregated across many sessions** - per-pair estimates on 30 turns are pure noise and the published effects are single-digit percentage points even at corpus scale - Gini of turn share and of words-per-turn - hypothesis accuracy per ordered pair - other-initiated repair rate per minute against 1.4 - self-repetition n-gram overlap - addressee entropy - stance reversals with **no new argument in the intervening turns** (this is measured sycophancy in your own system) - committed-fact drop rate against the pre-conversation baseline - response length vs turn index.

**Tier 2 - LLM judge on the 550B, as a multiplier not a substitute.** Position-randomised. **Validate on a 50-item subset against your own labels and report the agreement number.** GPT-4-class judges reach >80% agreement with human preference - equal to human-human - but carry position, verbosity and self-enhancement bias. An unvalidated judge means you optimise its verbosity bias, which is the exact direction the system already drifts.

**Tier 3 - humans, once per major rung, never per tweak.** Best-Worst Scaling: 4-tuples of transcripts, "which group sounds most like real people", ~2N tuples, 30-50 raters, aggregated with Bradley-Terry. **Rank ablations against each other in one sitting; never rate a single system** - within-subject ranking removes the calibration noise that kills small studies. Park used 100 raters for 5 conditions; 30-50 gets a usable signal only for *structural* changes. Decide the minimum detectable effect before collecting. If you cannot state the MDE, do not run this tier.

**The rung that must be run.** One rung that changes **nothing but the persona prompts**. If it moves the ranking as much as the architecture rungs, the architecture work is not where believability lives. Jones & Bergen: 73% with the persona prompt, 21% without, same experimental frame.

**Turns-to-disbelief** - play the audio, listener presses a key when they stop believing it, analyse with Kaplan-Meier and log-rank between rungs - is worth logging as an **exploratory secondary**. It is stated in the units of the actual problem, but no cited work validates it and "eight" is an unblinded n=1 self-report. It cannot be the primary endpoint. [INFERENCE, flagged.]

**How the protocol itself fails - the five ways, in order of likelihood:**
1. You rate one system instead of ranking ablations, and rater calibration noise swamps a real effect.
2. **You optimise the believability rating and drift away from humanness.** Park's paid human-authored condition ranked *fourth of five*, below two ablated agents. The rating measures legibility and narrative coherence, not being a person. The stated goal - "a genuine conversation" - is the second thing, and the metric will reward the first.
3. The LLM judge is unvalidated, so you tune to its biases.
4. No no-interaction control, so spontaneous instability is credited to the impression system.
5. **You evaluate transcripts when the product is audio.** Gaps, overlap, latency and silence are half the signal and are invisible in text. Any rung touching L5 or L12 must be judged on audio.

---

## 6 - WHAT NOT TO BUILD

- **Daily planning / recursive schedule decomposition.** Last in the ablation at +1.24, the most call-hungry component of the three, and most of what it buys - spatial and temporal scheduling of a day - does not exist in a conversation. Keep only the two-line kernel: a standing intent, and a react-or-continue check (L7).
- **Third-order theory of mind.** "What A thinks B thinks of C" scores 15-20% joint accuracy on a benchmark designed to be tractable, costs a call per pair, and no listener will ever detect its absence. Cap impressions at order-1 (what they want/believe) plus order-2 **about the self only**, and only as a pre-send check.
- **A numeric affinity, trust, or relationship float.** This is a fabricated resource and it violates the honesty law directly. The best-evaluated system in this space deliberately has none - the relationship *is* whatever A's own memories about B return when asked. The one legitimate number is hypothesis value V, because it is a record of scored predictions against observed behaviour.
- **A vector database.** Hundreds to low thousands of rows. numpy.
- **Task-oriented multi-agent frameworks as the frame.** Take AutoGen's pluggable speaker-selection interface and the FSM transition graph - ~30 lines, both free. Refuse the SOP/artifact/terminal-state frame entirely: a conversation has no terminal state, no verifiable output, and no standard operating procedure, which is exactly why none of their metrics say anything about whether talk sounds real. Their transcripts are notoriously stilted and none of the four papers ever asked a human about the dialogue.
- **Split-softmax, classifier-free guidance, or any attention-level fix.** Requires logit/attention access the hosted rods do not expose. SPR at the end of the context is the substitute. And note: CFG helps at round 1 and degrades over extended rounds - do not build toward it.
- **Any fine-tuning or preference optimisation.** CPU only, no GPU. Take APC's *scorer* (two ~300M CPU cross-encoders) and drop its DPO half. Take MultiLIGHT's architectural lesson (central, not decentralised) and drop its 400M trained speaker model.
- **Full concurrent PIANO.** Ten modules × four agents will not fit CPU-only at conversational latency. Two loops joined by a short bottleneck summary: fast speech on the 8B, slow impression on the 49B every N turns.
- **ReCon second-order revision on every utterance.** It doubles per-turn latency and *measurably lowered persuasiveness* - the agent became concise and stopped making rousing statements. Adding a politeness filter to every line in a conversation that already flattens is the wrong direction. Gate it to real social friction: being named, being contradicted, being caught.
- **Feeding the prior transcript as long context for cross-session identity.** ~41 F1 against a human 87.9. Persist the identity graph; let the transcript die.
- **Injecting another voice's evaluation as bare social pressure.** "Nadia thinks your argument is weak" with nothing attached *is* the "are you sure?" condition, and the measured response is capitulation at 32-86%. If you inject it, inject the argument with it.
- **ChatProtect in the speaking path.** One extra generation plus one judgement per sentence is prohibitive live. Consolidation only.
- **The constants, copied blind.** 0.995 decay (uniform at turn granularity), the 150 reflection threshold (calibrated to a sandbox game day), 8-round conversation caps (theirs, not yours). Port the mechanism, retune the number against the L2 curve.
- **A rebuilt-summary impression, in any form.** It is `top_k=0` - the categorically worst setting in the published sweep, worse than any k>0. Keep old guesses alongside new ones and let bad ones fall out by score.