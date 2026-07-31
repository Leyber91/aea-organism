"""brief.py - THE MORNING BRIEF: the first REAL task the free swarm does for Luis.

Connected to his world with REAL data (his live GitHub activity + live AI news), routed by the PROVEN
regime rule (easy synthesis of given data -> ONE good model, not a council), the PRIVATE section
boundary-LOCKED to local Ollama (zone=sensitive can only reach local plants), every node traced
(goal-stack + append-only JSONL), and HADES signs off at the end (Law 3 accountability). No stubs.

  public sections -> hosted free grid (NVIDIA/Groq, no-train)     |  private section -> LOCAL ONLY
"""
import json, sys, time, urllib.request
import os
import datetime as _dt

from aea.kernel import grid
from aea.mind import orchestrator
from aea.mind import hades
from aea.kernel import trust
from aea.kernel import hands
from aea.kernel.tracelog import Trace
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

GH_USER = "Leyber91"
ROOT_GOAL = "Produce Luis's morning brief: what he's actively moving on, one AI opportunity, and today's first focus."
# Luis's REAL day, fetched from his Calendar+Gmail into a LOCAL gitignored file. Reasoned over LOCAL-only.
try:
    PRIV = grid.load_json("private_today.json", {})
    # STALE DATA MUST ANNOUNCE ITSELF. This read `PRIV["date"]` and printed it under the heading
    # "today", so a private file last written on 2026-06-28 was presented to the model, and to Luis,
    # as the current day - for a month. That is the honesty law's exact failure: not a wrong number,
    # a real number wearing the wrong label. The file is not refreshed here (that is a separate
    # organ's job); what changes is that its age is stated, so nothing downstream can mistake it.
    _pd = PRIV.get("date", "")
    _today = _dt.datetime.now().strftime("%Y-%m-%d")
    if _pd and _pd[:10] != _today:
        # The parens matter: `"..." % x.days * -1` binds the % first and then multiplies the STRING
        # by -1, which yields "" and silently drops the whole warning. Caught by reading the output.
        try:
            _days = (_dt.date.today() - _dt.date.fromisoformat(_pd[:10])).days
            _age = " (%d DAYS STALE)" % _days
        except Exception:
            _age = " (STALE)"
        _hdr = "DATE OF THIS PRIVATE DATA: %s%s - TODAY IS %s. Do not describe it as today's." \
               % (_pd, _age, _today)
    elif not _pd:
        _hdr = "DATE OF THIS PRIVATE DATA: unknown. Do not describe it as today's."
    else:
        _hdr = "DATE: " + _pd
    PRIVATE_BLOCK = (_hdr + "\nCALENDAR:\n- " + "\n- ".join(PRIV.get("calendar", []))
                     + "\nINBOX SIGNAL:\n- " + "\n- ".join(PRIV.get("inbox_signal", [])))
except Exception as e:
    PRIV, PRIVATE_BLOCK = {}, f"[no private_today.json: {e}]"

meter = grid.METER; router = grid.Router(meter); pool = orchestrator.load_pool()

fetch_json = grid.fetch_json   # one home (was duplicated verbatim here and in aea.py)


# EVERY STRING THIS FILE SUBSTITUTES FOR A SECTION IT COULD NOT PRODUCE. A placeholder must be
# declared in one place or the completeness check cannot know about it.
PLACEHOLDERS = ("(grid busy)", "(no local node)", "(unavailable)", "(none)", "-")


def section_ok(t: str) -> bool:
    """Is this section REAL CONTENT, or something standing where content should be?

    The old check was `all("ERR" not in t[:40] ...)`, and it had two holes that both point the same
    way - toward reporting a hole as a clean run:

      1 A PLACEHOLDER IS NOT AN ERROR STRING. When no public node was free, `grid_public` returned
        "(grid busy)". It contains no "ERR", so the brief shipped with an empty section, exited 0,
        and `trust.record("produce_brief", True)` counted it toward PROMOTION. The entity earned
        autonomy for briefs it had not written.
      2 ONLY THE FIRST 40 CHARACTERS WERE READ. An error surfacing mid-section was invisible.

    Under the honesty law an absent value renders as a dash and is never counted as present. This is
    that law applied to the one artifact that actually gets read.
    """
    t = (t or "").strip()
    if not t or len(t) < 20:
        return False
    if "ERR" in t:
        return False
    return t.lower() not in {p.lower() for p in PLACEHOLDERS}


def grid_public(T, parent, goal, prompt, tier="bulk", depth=1, mx=None):
    """A traced PUBLIC reasoning node -> hosted free grid. Regime rule: easy synthesis -> ONE good model.

    `mx=None` READS THE DECLARED KNOB. It used to be the literal 400, chosen by nobody in
    particular, and a ceiling below a rod's published window only truncates thinking - measured, a
    550B rod scored 7/12 under a 40-token budget and 12/12 without it while a non-deliberating
    control did not move. The knob carries bounds and a reason; see aea/kernel/knobs.py."""
    from aea.kernel import knobs
    mx = knobs.get("produce_brief", "public_max_tokens") if mx is None else mx
    node = T.spawn(goal, parent=parent, zone="public", depth=depth)
    n = orchestrator.pick(pool, tier, "public", meter)
    if not n:
        T.done(node, "ERR: no public node free", model="none"); return node, "(grid busy)"
    T.mark(node, "route", f"regime=easy-synthesis->single {tier}; picked {n['plant']}/{n['model']}")
    r = orchestrator.call_node(n, prompt, meter, mx)
    txt = (r.get("text") or "").strip() if r.get("ok") else f"ERR: {r.get('error', '')[:80]}"
    T.done(node, txt, model=f"{n['plant']}/{n['model']}")
    return node, txt


def grid_private(T, parent, goal, prompt, depth=None, mx=None, cap="text"):
    """A traced PRIVATE node. zone=sensitive => ZONES boundary allows LOCAL ONLY. depth=3 -> a small FAST
    local model (the router picks ollama/granite4.1:3b, the reliable non-thinking instruct)
    so the private step doesn't cold-load a 9B past the timeout. Returns the plant to PROVE it."""
    # THE KNOB THE ENTITY IS ALLOWED TO TURN, AND THE IMPASSE IT EXISTS FOR. `unstick.propose` has
    # returned {"move": "raise_budget", "knob": "max_tokens", "to": 900} against this capability for
    # weeks - correctly, because a reasoning rod spends its budget thinking and emits content only
    # afterwards, so at 300 it can answer correctly and still return an empty string. Nothing could
    # ever apply that proposal, because this number was a literal at a call site. Reading it here is
    # what lets the R3 loop close: a move can be applied, its outcome observed, and the record can
    # then change what happens next. Bounds and the reason live in aea/kernel/knobs.py.
    from aea.kernel import knobs
    mx = knobs.get("produce_brief", "max_tokens") if mx is None else mx
    depth = knobs.get("produce_brief", "depth") if depth is None else depth
    node = T.spawn(goal, parent=parent, zone="sensitive", depth=depth)
    T.mark(node, "route", "zone=sensitive -> LOCAL ONLY (ZONES['sensitive']={local}); private data never leaves the machine")
    T.mark(node, "knob", f"max_tokens={mx} (declared knob produce_brief.max_tokens)")
    # A CRASHED SERVER IS NOT A WRONG ANSWER, AND IT MUST NOT COST A STREAK.
    #
    # This capability sat at DRAFT with 34 failures in 40 for eighteen days. Every recorded failure
    # read `hades=unverified sections_ok=False`, and the stored brief showed why: this section came
    # back `ERR: llama-server process has terminated: exit status 0xc0000005`. An access violation in
    # the local server was written into the ledger as the capability failing, which demoted it, and
    # promotion needs SEVEN consecutive clean runs it could then never assemble.
    #
    # The lab's own harness has forbidden this since chapter I - a network failure is not a wrong
    # answer, and conflating them turns an outage into a capability finding. The entity was doing
    # exactly that to itself. ollama restarts a crashed llama-server on the next request, so one
    # retry converts the commonest failure in the record into a slower success.
    for attempt in range(3):
        r = grid.complete(prompt, capability=cap, zone="sensitive", depth=depth, max_tokens=mx,
                          router=router)
        txt = (r.get("text") or "").strip()
        if txt:
            break
        err = str(r.get("error") or "")
        # THE TRANSPORT LAYER SAYS SO; THIS LAYER DOES NOT GUESS. The first version of this matched
        # substrings - "terminated", "0xc0000005", "connection" - which is whack-a-mole against every
        # provider's error phrasing, forever, and it would have silently stopped working the first
        # time a plant reworded a message. grid.call_openai now labels the failure at the only layer
        # that can know what kind it was.
        transport = bool(r.get("transport"))
        T.mark(node, "retry", "attempt %d returned nothing (%s): %s"
               % (attempt + 1, "transport" if transport else "empty", err[:90]))
        if not transport and attempt >= 1:
            break
        time.sleep(2 + 3 * attempt)
    plant, model = r.get("plant"), r.get("model")
    txt = txt or f"ERR: {r.get('error')}"
    T.done(node, txt, model=f"{plant}/{model}")
    return node, txt, plant


def main():
    t0 = time.time()
    T = Trace(ROOT_GOAL)
    print(f"ROOT GOAL: {ROOT_GOAL}\n" + "=" * 78)

    # ---- Section 1: project status (PUBLIC, real GitHub) ----
    # THE FETCH GOES THROUGH THE GATE NOW. These two calls are the only outbound reads the wake
    # makes, and until 2026-07-28 they went straight to `grid.fetch_json` with NO permission check
    # of any kind: `hands.allowed()` existed, enforced `gather_public` at the call site, and no wake
    # path reached it. Law B5 says a permission the model can talk past is a decoration; a
    # permission nothing calls is not even that. `reach()` returns the fetch outcome separately from
    # the model's prose, because grading `gather_public` on a substring of a summary is law G1's
    # named defect and it was live here.
    fetch_ok = {"github": None, "hn": None}

    def reach(label: str, url: str):
        """One permitted outbound read. Returns (parsed, error-or-None) and records the OUTCOME."""
        v = hands.allowed("json_get", "public")
        if not v["ok"]:
            fetch_ok[label] = False
            return None, "refused: " + v["why"]
        try:
            data = fetch_json(url)
            fetch_ok[label] = True
            return data, None
        except Exception as ex:
            fetch_ok[label] = False
            return None, "%s: %s" % (type(ex).__name__, str(ex)[:90])

    try:
        raw, ferr = reach("github", f"https://api.github.com/users/{GH_USER}/repos?sort=pushed&per_page=15&type=owner")
        if ferr:
            raise RuntimeError(ferr)
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
        hn, ferr = reach("hn", "https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI%20agent&hitsPerPage=12")
        if ferr:
            raise RuntimeError(ferr)
        story_block = "\n".join(f"- {h['title']} ({h.get('points', 0)} pts) {h.get('url') or ''}"
                                for h in hn.get("hits", []) if h.get("title"))[:1800]
        print(f"[real data] fetched {len(hn.get('hits', []))} fresh AI stories from Hacker News")
    except Exception as e:
        story_block = f"(HN fetch failed: {e})"; print(f"[warn] HN fetch failed: {e}")
    s2, opp_txt = grid_public(T, T.root, "pick the single most relevant AI opportunity for Luis",
        f"Fresh AI stories from Hacker News today:\n{story_block}\n\n"
        "Luis is an AI engineer building agentic/multi-agent systems on free infrastructure. Pick the SINGLE "
        "most relevant story as an opportunity. Output one line naming it, then ONE short sentence why it matters to him. No preamble, no emoji.", tier="deep")

    # ---- Section 3: today's first focus (PRIVATE -> LOCAL ONLY) ----
    s3, focus_txt, priv_plant = grid_private(T, T.root, "plan Luis's day from his real calendar+inbox (private)",
        f"Luis's real day and inbox today:\n{PRIVATE_BLOCK}\n\nIn EXACTLY 3 terse bullets: (1) the best use of his FREE block, "
        "(2) the one email that needs an action today, (3) one thing worth reading. No preamble, no emoji.")
    boundary_ok = (priv_plant == "ollama")
    print(f"[boundary] private 'today' section ran on: {priv_plant}  -> {'LOCAL-ONLY HELD' if boundary_ok else 'BREACH!!'}")

    # ---- Section 4: assemble DETERMINISTICALLY (local, no model) - private content must NOT reach the grid ----
    syn = T.spawn("assemble the brief (deterministic, local)", parent=[s1, s2, s3], zone="sensitive", depth=1,
                  why="the merge combines PUBLIC + PRIVATE -> deterministic template, never a grid model (no leak)")
    T.mark(syn, "assemble", "Python template; no LLM ever sees the public+private combination")
    # THE HEADING DATES THE BRIEF, NOT THE PRIVATE FILE. This read `PRIV["date"]`, so a private
    # snapshot last written on 2026-06-28 titled the brief "Morning brief - 2026-06-28" for a month
    # while every public section in it was fetched minutes earlier. Law H2: stale data must announce
    # its age, and the failure it names is a REAL number under the WRONG label - which is what a
    # month-old date at the top of today's brief is. The prompt already warned the model; the
    # artifact Luis actually reads still lied. The private section now carries its own age instead.
    _brief_day = _dt.datetime.now().strftime("%Y-%m-%d (%A)")
    _pdate = (PRIV.get("date") or "")[:10]
    _pnote = ""
    if _pdate and _pdate != _dt.datetime.now().strftime("%Y-%m-%d"):
        try:
            _pn = (_dt.date.today() - _dt.date.fromisoformat(_pdate)).days
            _pnote = f"  \n*calendar and inbox below are from {_pdate}, {_pn} days old*"
        except Exception:
            _pnote = f"  \n*calendar and inbox below are from {_pdate}*"
    elif not _pdate:
        _pnote = "  \n*no dated private snapshot available*"
    brief_md = (f"# Morning brief - {_brief_day}\n\n"
                f"## What you're moving on\n{status_txt}\n\n"
                f"## One opportunity\n{opp_txt}\n\n"
                f"## Today{_pnote}\n{focus_txt}\n")
    T.done(syn, brief_md, model="deterministic/local")

    # ---- HADES signs off LOCALLY (Law 3): the brief holds private data, so its watcher is LOCAL + heterogeneous (no leak) ----
    verdict, who = hades.watch_local(ROOT_GOAL, brief_md, meter, worker_model="granite4.1:3b")

    # THE ARTIFACT MUST LAND WHERE IT CAN BE FOUND. This was a bare relative path, so the brief
    # landed in whatever directory the process happened to start in - repo root when run by hand,
    # somewhere else when run by a scheduler. state/brief_output.md was eighteen days stale while
    # fresh briefs were being written elsewhere and never read. The repo's own rule: never hardcode
    # a state path, always resolve through grid.STATE.
    _out = os.path.join(grid.STATE, "brief_output.md")
    with open(_out, "w", encoding="utf-8") as f:
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
    print(f"  trace written    : brief_trace.jsonl   |   brief written: {_out}")
    print(f"  wall time        : {round(time.time()-t0,1)}s on free + local infra")

    # ---- TRUST LEDGER (Law 3 extended): every run stamps the ledger; autonomy is earned, never assumed ----
    clean = (verdict.get("verdict") == "accept")
    sections_ok = all(section_ok(t) for t in (status_txt, opp_txt, focus_txt))
    # GRADED ON THE FETCH ITSELF. This read `"fetch failed" not in status_txt.lower()`, where
    # status_txt is a MODEL's three-bullet summary - so the capability passed whenever the model
    # avoided a phrase, and would have passed with both fetches dead. Law G1: grade the outcome,
    # never a proxy for it. `None` means the branch never ran, which is not a pass.
    trust.record("gather_public", all(v is True for v in fetch_ok.values()))
    trust.record("reason_private_local", boundary_ok and "ERR" not in focus_txt[:40])
    t_state = trust.record("produce_brief", clean and sections_ok,
                           note=f"hades={verdict.get('verdict')} sections_ok={sections_ok}")
    print(f"  trust ledger     : produce_brief -> {t_state['why']}")
    # The exit code must tell the truth (review 2026-07-10: a brief full of ERR holes exited 0,
    # live.py stamped it done for the day and never retried - the heartbeat lie).
    return 0 if (clean and sections_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
