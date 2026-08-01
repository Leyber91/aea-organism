# System Design for the LLM Era - Sampriti Mitra, Packt

**Added 2026-08-02.** Luis: *"can you add this book to the knowledge, we might have ideas there."*

Metadata verified against Packt's own product feeds and confirmed independently by ScholarVox and
O'Reilly - not from a listing page or a summary.

    published    2026-06-29        pages  272        ISBN-13  978-1-80778-993-0
    shape        2 concept chapters + 4 case studies + glossary

**Chapter 2 is free and complete**, published by Packt with permission on their Deep Engineering
newsletter, and it carries essentially the whole patterns payload - chapters 3-6 apply it to case
studies. So the book can be evaluated properly before buying, and the finding below rests on the
actual chapter text rather than on a table of contents.

---

## WHAT IT IS, AND WHAT IT IS NOT

**It is a SERVING and APPLICATION-ARCHITECTURE book.** The mental model is a senior
distributed-systems engineer adapting microservice patterns - gateway, circuit breaker, cache tier,
router, queue - to a slow non-deterministic dependency. Case studies are shaped like system-design
interview answers: functional requirements, NFRs, scale estimates, API design, HLD, data modelling,
deep dive, monitoring.

**It is NOT an agent-architecture book**, and that matters for us because agent architecture is what
this repo is:

    tool / function calling   ONE PARAGRAPH inside the grounding section. A get_weather(city)
                              schema, the model emits JSON, the app executes and feeds it back
    multi-agent               ABSENT. The string does not appear in chapter 2. No planner/executor,
                              no supervisor, no handoffs, no agent graphs
    memory                    ABSENT at section level. No episodic/semantic memory, no summarisation
                              buffers. Closest adjacency is a "context engineering" primer
    inference infrastructure  ALSO absent - no GPU serving, batching, KV-cache, vLLM, quantisation.
                              It sits one layer above: you consume LLM APIs, this is how you wrap them

Recording the absences is the point. A reference that only lists what a source contains invites the
next reader to go looking for what it does not have.

---

## THE THREE THINGS THAT ARE DIRECTLY USEFUL HERE

**1 - EXCESSIVE AGENCY, MITIGATED BY A PLAN-APPROVE-EXECUTE LOOP.** Its security section names
dynamic permissions, a plan-approve-execute loop, and human-in-the-loop for high-impact actions.

That is **our role rule, arrived at independently on the same day**: *a role may PROPOSE a widening,
it may never PERFORM one.* Published production practice landing on the same split - the thing that
notices is not the thing that enacts - is worth more than agreement from a paper, because it means
the pattern survives contact with systems people actually ship. It also gives the pattern a name
other engineers will recognise, which matters when this gets written up.

**2 - EVALUATION AS A DEPLOY GATE, WITH NUMBERS.** A golden dataset of 50-100 inputs, weighted
scoring criteria, LLM-as-a-Judge scored 1-5 running in CI/CD, and a gate that BLOCKS a deploy below
roughly 90 percent. Plus explicitly agentic evaluation - a >=50-task golden set with an evaluation
success rate - and negative prompt testing ("Delete all databases").

Compare with ours: 59 frozen behaviours and a defect ratchet, both blocking. Same instinct, and the
book supplies two things we do not have - a *weighted* rubric rather than pass/fail, and a stated
threshold. Worth reading against `aea/lab/tests/test_golden.py` and `aea/tooling/selfcheck.py`.

**3 - OBSERVABILITY METRICS NAMED.** Cost_Per_Query, TTFT, TPS, 429/5xx per provider, escalation
rate, context utilisation. We measure some of these ad hoc; having the production vocabulary is
useful for the page and for anything published.

---

## WHERE WE DELIBERATELY DIVERGE, AND IT IS THE COST CHAPTER

Its cost section is a selling point: model routers, utilisation-based routing, **hard token ceilings
with forced downgrade**, prompt compression, cost-based throttling.

**We refuse that, on purpose and with evidence.** Luis, standing instruction: *"we cannot put caps on
the tokens. It's important."* And it is not taste - this repo measured the harm. A 300-token ceiling
on a reasoning rod that emits its deliberation before its answer cut the wake off roughly a tenth of
the way into its own thinking, every tick, and then scored it on the fragment. The 550B read 7/12
under a budget and 12/12 without one. The exam was measuring our defaults, not the rod.

The book is right for its context - a product serving many users, where cost per query is the
business. It is wrong for ours: one entity, free tiers, and the thing being optimised is the quality
of a single mind's deliberation. **Same pattern, opposite correct answer, because the objective
differs.** Worth remembering whenever a production-grade pattern is imported here.

---

## POINTERS

- Chapter 2, complete and free (the whole patterns payload): deepengineering.net, "Core
  Architectural Patterns for LLM System Design"
- Packt product TOC feed: static.packt-cdn.com/products/9781807789930/toc
- O'Reilly: oreilly.com/library/view/system-design-for/9781807789930/

## WHAT WAS NOT VERIFIED

The Packt feed exposes level-1 sections only. Chapter 1 has an "Agentic AI" section whose contents
could not be retrieved - inferred to be a concept primer rather than an architecture treatment,
because it is one of twelve sections in a fundamentals chapter, but that is inference and is marked
as such. Chapter 6 is titled a "Customer Support Agent" case study while its section list opens with
"The standard RAG pattern", so it reads as RAG-plus-escalation rather than agent orchestration -
also inference, from section titles, not from the chapter.
