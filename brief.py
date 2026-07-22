"""brief.py - THE MORNING BRIEF: the first REAL task the free swarm does for Luis.

Connected to his world with REAL data (his live GitHub activity + live AI news), routed by the PROVEN
regime rule (easy synthesis of given data -> ONE good model, not a council), the PRIVATE section
boundary-LOCKED to local Ollama (zone=sensitive can only reach local plants), every node traced
(goal-stack + append-only JSONL), and HADES signs off at the end (Law 3 accountability). No stubs.

  public sections -> hosted free grid (NVIDIA/Groq, no-train)     |  private section -> LOCAL ONLY
"""
import grid, orchestrator, hades, trust, json, sys, time, urllib.request
from tracelog import Trace
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

GH_USER = "Leyber91"
ROOT_GOAL = "Produce Luis's morning brief: what he's actively moving on, one AI opportunity, and today's first focus."
# Luis's REAL day, fetched from his Calendar+Gmail into a LOCAL gitignored file. Reasoned over LOCAL-only.
try:
    PRIV = grid.load_json("private_today.json", {})
    PRIVATE_BLOCK = ("DATE: " + PRIV.get("date", "today") + "\nCALENDAR:\n- " + "\n- ".join(PRIV.get("calendar", []))
                     + "\nINBOX SIGNAL:\n- " + "\n- ".join(PRIV.get("inbox_signal", [])))
except Exception as e:
    PRIV, PRIVATE_BLOCK = {}, f"[no private_today.json: {e}]"

meter = grid.METER; router = grid.Router(meter); pool = orchestrator.load_pool()

fetch_json = grid.fetch_json   # one home (was duplicated verbatim here and in aea.py)


def grid_public(T, parent, goal, prompt, tier="bulk", depth=1, mx=400):
    """A traced PUBLIC reasoning node -> hosted free grid. Regime rule: easy synthesis -> ONE good model."""
    node = T.spawn(goal, parent=parent, zone="public", depth=depth)
    n = orchestrator.pick(pool, tier, "public", meter)
    if not n:
        T.done(node, "ERR: no public node free", model="none"); return node, "(grid busy)"
    T.mark(node, "route", f"regime=easy-synthesis->single {tier}; picked {n['plant']}/{n['model']}")
    r = orchestrator.call_node(n, prompt, meter, mx)
    txt = (r.get("text") or "").strip() if r.get("ok") else f"ERR: {r.get('error', '')[:80]}"
    T.done(node, txt, model=f"{n['plant']}/{n['model']}")
    return node, txt


def grid_private(T, parent, goal, prompt, depth=3, mx=300, cap="text"):
    """A traced PRIVATE node. zone=sensitive => ZONES boundary allows LOCAL ONLY. depth=3 -> a small FAST
    local model (qwen3:1.7b) so the private step doesn't cold-load a 9B past the timeout. Returns the plant to PROVE it."""
    node = T.spawn(goal, parent=parent, zone="sensitive", depth=depth)
    T.mark(node, "route", "zone=sensitive -> LOCAL ONLY (ZONES['sensitive']={local}); private data never leaves the machine")
    r = grid.complete(prompt, capability=cap, zone="sensitive", depth=depth, max_tokens=mx, router=router)
    plant, model = r.get("plant"), r.get("model")
    txt = (r.get("text") or "").strip() or f"ERR: {r.get('error')}"
    T.done(node, txt, model=f"{plant}/{model}")
    return node, txt, plant


def main():
    t0 = time.time()
    T = Trace(ROOT_GOAL)
    print(f"ROOT GOAL: {ROOT_GOAL}\n" + "=" * 78)

    # ---- Section 1: project status (PUBLIC, real GitHub) ----
    try:
        raw = fetch_json(f"https://api.github.com/users/{GH_USER}/repos?sort=pushed&per_page=15&type=owner")
        repos = [r for r in raw if not r.get("fork")][:8]            # authorship integrity: never present a FORK as his work
        n_forks = sum(1 for r in raw if r.get("fork"))
        repo_block = "\n".join(f"- {r['name']} ({r.get('language') or '?'}, pushed {r['pushed_at'][:10]}): "
                               f"{(r.get('description') or 'no description')[:90]}" for r in repos)
        print(f"[real data] fetched {len(repos)} of his OWN recently-pushed repos for {GH_USER} ({n_forks} forks excluded)")
    except Exception as e:
        repo_block = f"(GitHub fetch failed: {e})"; print(f"[warn] GitHub fetch failed: {e}")
    s1, status_txt = grid_public(T, T.root, "summarize what Luis is actively moving on (from real repos)",
        f"Luis's most-recently-pushed GitHub repos:\n{repo_block}\n\n"
        "In EXACTLY 3 terse bullets, summarize what he is actively moving on. Concrete, no preamble, no emoji.")

    # ---- Section 2: one AI opportunity (PUBLIC, real Hacker News) ----
    try:
        hn = fetch_json("https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI%20agent&hitsPerPage=12")
        story_block = "\n".join(f"- {h['title']} ({h.get('points', 0)} pts) {h.get('url') or ''}"
                                for h in hn.get("hits", []) if h.get("title"))[:1800]
        print(f"[real data] fetched {len(hn.get('hits', []))} fresh AI stories from Hacker News")
    except Exception as e:
        story_block = f"(HN fetch failed: {e})"; print(f"[warn] HN fetch failed: {e}")
    s2, opp_txt = grid_public(T, T.root, "pick the single most relevant AI opportunity for Luis",
        f"Fresh AI stories from Hacker News today:\n{story_block}\n\n"
        "Luis is an AI engineer building agentic/multi-agent systems on free infrastructure. Pick the SINGLE "
        "most relevant story as an opportunity. Output one line naming it, then ONE short sentence why it matters to him. No preamble, no emoji.", tier="deep", mx=700)

    # ---- Section 3: today's first focus (PRIVATE -> LOCAL ONLY) ----
    s3, focus_txt, priv_plant = grid_private(T, T.root, "plan Luis's day from his real calendar+inbox (private)",
        f"Luis's real day and inbox today:\n{PRIVATE_BLOCK}\n\nIn EXACTLY 3 terse bullets: (1) the best use of his FREE block, "
        "(2) the one email that needs an action today, (3) one thing worth reading. No preamble, no emoji.", mx=320)
    boundary_ok = (priv_plant == "ollama")
    print(f"[boundary] private 'today' section ran on: {priv_plant}  -> {'LOCAL-ONLY HELD' if boundary_ok else 'BREACH!!'}")

    # ---- Section 4: assemble DETERMINISTICALLY (local, no model) - private content must NOT reach the grid ----
    syn = T.spawn("assemble the brief (deterministic, local)", parent=[s1, s2, s3], zone="sensitive", depth=1,
                  why="the merge combines PUBLIC + PRIVATE -> deterministic template, never a grid model (no leak)")
    T.mark(syn, "assemble", "Python template; no LLM ever sees the public+private combination")
    brief_md = (f"# Morning brief - {PRIV.get('date', 'today')}\n\n"
                f"## What you're moving on\n{status_txt}\n\n"
                f"## One opportunity\n{opp_txt}\n\n"
                f"## Today\n{focus_txt}\n")
    T.done(syn, brief_md, model="deterministic/local")

    # ---- HADES signs off LOCALLY (Law 3): the brief holds private data, so its watcher is LOCAL + heterogeneous (no leak) ----
    verdict, who = hades.watch_local(ROOT_GOAL, brief_md, meter, worker_model="granite4.1:3b")

    with open("brief_output.md", "w", encoding="utf-8") as f:
        f.write(brief_md + f"\n\n---\n_brief generated on the free grid in {round(time.time()-t0,1)}s; "
                f"private section local-only ({priv_plant}); HADES: {verdict.get('verdict')}_\n")

    print("\n" + "=" * 78 + "\nTHE BRIEF\n" + "=" * 78 + f"\n{brief_md}\n")
    print("=" * 78 + "\nTHE TRACE (goal-tree; [zone] + model per node; merge = DAG)\n" + "=" * 78)
    print(T.tree_str())
    print(f"vertical lineage check - what node {s3.id} can see looking UP:\n  {T.lookup(s3)}\n")
    print("=" * 78 + "\nACCOUNTABILITY + BOUNDARY\n" + "=" * 78)
    print(f"  privacy boundary : private 'today' section -> {priv_plant}  ({'HELD - local only' if boundary_ok else 'BREACH'})")
    print(f"  grid exposure    : public sections only; assembly + HADES both LOCAL -> private data never reached the grid")
    print(f"  HADES verdict    : ({who}) on_goal={verdict.get('on_goal')} correct={verdict.get('correct')} "
          f"-> {verdict.get('verdict')}  [{verdict.get('why')}]")
    print(f"  trace written    : brief_trace.jsonl   |   brief written: brief_output.md")
    print(f"  wall time        : {round(time.time()-t0,1)}s on free + local infra")

    # ---- TRUST LEDGER (Law 3 extended): every run stamps the ledger; autonomy is earned, never assumed ----
    clean = (verdict.get("verdict") == "accept")
    sections_ok = all("ERR" not in t[:40] for t in (status_txt, opp_txt, focus_txt))
    trust.record("gather_public", "fetch failed" not in status_txt.lower())
    trust.record("reason_private_local", boundary_ok and "ERR" not in focus_txt[:40])
    t_state = trust.record("produce_brief", clean and sections_ok,
                           note=f"hades={verdict.get('verdict')} sections_ok={sections_ok}")
    print(f"  trust ledger     : produce_brief -> {t_state['why']}")
    # The exit code must tell the truth (review 2026-07-10: a brief full of ERR holes exited 0,
    # live.py stamped it done for the day and never retried - the heartbeat lie).
    return 0 if (clean and sections_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
