"""aea.py - THE AEA: a seeded, persistent, always-on entity. NOT a swarm - ONE core mind on a loop,
seeded with WHO Luis is, keeping continuity across ticks (memory), watched by HADES. The swarm is a
subroutine the core can call for hard problems; the CORE is a single big FREE model (Luis's pick:
nemotron-550b, 40 rpm) with fallback so the loop never dies.

A real deployment is `while True` + sleep (or scheduled). Here we run N ticks to PROVE the essence:
it reasons FROM his life-state, REMEMBERS across ticks (persistent evolving state), and ACTS each tick.

  python aea.py [N_TICKS]
"""
import grid, orchestrator, hades, energy, json, os, time, sys, re, urllib.request
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_PATH = os.path.join(grid.STATE, "aea_seed.md")
STATE_PATH = os.path.join(grid.STATE, "aea_state.json")
STANDING_GOAL = ("Serve Luis's real, current priorities honestly given his projects and the income clock; "
                 "surface only what truly matters right now; never invent; weigh against shipping + income.")

meter = grid.METER            # the shared meter (a private Meter here used to clobber energy's - review 2026-07-10)
pool = orchestrator.load_pool()

# THE CORE draws ENERGY, it does not name fuel (Luis's continuum law): energy.draw reads the live
# capability census + fitness + meter and burns the best frontier rod available right now, falling
# down the ladder on failure - all the way to the local floor, so the heartbeat never stops.
def core(prompt, max_tokens=800):
    r = energy.draw(prompt, tier="frontier", zone="private", mx=max_tokens, timeout=90)
    if r["ok"]:
        return r["text"], f"{r['plant']}/{r['model']}"
    return "", f"none (all rods failed: {r['tried'][-3:]})"

STRUCT_SCHEMA = {"type": "object", "additionalProperties": False,
    "properties": {"matters_now": {"type": "string"}, "changed": {"type": "string"},
                   "action": {"type": "string"}, "note_to_self": {"type": "string"}},
    "required": ["matters_now", "changed", "action", "note_to_self"]}

def structure(reasoning):
    """Phase 2 = the FORMATTER tool: a cheap strict-JSON model turns the core's free reasoning into 4 clean
    fields (guaranteed parseable). The big model thinks; this formalizes. Self-contained, never raises."""
    try:
        k = grid.key("GROQ_API_KEY")
        body = json.dumps({"model": "openai/gpt-oss-120b", "temperature": 0, "max_tokens": 1200,
            "messages": [{"role": "user", "content": "From this reasoning by Luis's entity, extract four concrete "
                "fields, quoting his ACTUAL projects/priorities - no placeholders, no meta-commentary.\n\nREASONING:\n" + reasoning[:2800]}],
            "response_format": {"type": "json_schema", "json_schema": {"name": "aeastate", "strict": True, "schema": STRUCT_SCHEMA}}}).encode()
        req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=body,
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 aea", "Authorization": f"Bearer {k}"}, method="POST")
        c = json.loads(urllib.request.urlopen(req, timeout=60).read())["choices"][0]["message"]["content"]
        meter.record("groq", "openai/gpt-oss-120b")
        return json.loads(c)
    except Exception as e:
        return {"matters_now": reasoning[:200], "changed": "", "action": "", "note_to_self": f"(structuring failed: {str(e)[:60]})"}

fetch_json = grid.fetch_json   # one home (was duplicated verbatim here and in brief.py)

def sense():
    """Public world-state relevant to Luis (raw private data is handled local-only elsewhere)."""
    out = {}
    try:
        repos = [r for r in fetch_json("https://api.github.com/users/Leyber91/repos?sort=pushed&per_page=5&type=owner") if not r.get("fork")]
        out["recent_repos"] = [f"{r['name']} (pushed {r['pushed_at'][:10]})" for r in repos[:5]]
    except Exception as e:
        out["recent_repos"] = [f"(fetch failed: {e})"]
    try:
        hn = fetch_json("https://hn.algolia.com/api/v1/search_by_date?tags=story&query=AI%20agent&hitsPerPage=6")
        out["ai_news"] = [h["title"] for h in hn.get("hits", []) if h.get("title")][:6]
    except Exception as e:
        out["ai_news"] = [f"(fetch failed: {e})"]
    return out

def load_state():
    try:
        return json.load(open(STATE_PATH, encoding="utf-8"))
    except Exception:
        return {"tick": 0, "memory": [], "surfaced": []}

def save_state(s):
    json.dump(s, open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def tick(seed, state):
    state["tick"] += 1
    world = sense()
    mem = "\n".join(f"- {m}" for m in state["memory"][-6:]) or "(first awakening - no prior memory)"
    prompt = (
        "You are Luis's autonomous entity (the AEA). You persist across time and serve ONLY him. Reason as HIM,"
        " for him.\n\n"
        f"WHO LUIS IS (your seed):\n{seed}\n\n"
        f"WHAT YOU ALREADY NOTICED (your memory, most recent):\n{mem}\n\n"
        f"WHAT IS NEW IN THE WORLD NOW:\n  his recent repos: {world['recent_repos']}\n  fresh AI news: {world['ai_news']}\n\n"
        "Think concretely about HIS actual projects and the income clock, then decide four things: the SINGLE most "
        "important thing for him right now; what changed vs your memory; one concrete action for today; one thing to "
        "remember next tick. Reason it through in prose - do NOT output JSON.")
    reasoning, who = core(prompt, 1400)     # phase 1: the MIND reasons freely
    out = structure(reasoning)              # phase 2: the FORMATTER tool makes it structured
    # CONTINUITY: the entity remembers across ticks (the forever-loop essence)
    state["memory"].append(f"tick{state['tick']}: {str(out.get('note_to_self',''))[:160]}")
    state["surfaced"].append({"tick": state["tick"], **{k: out.get(k, "") for k in ("matters_now", "changed", "action")}})
    # HADES watches every autonomous tick (Law 3). Output is anonymized+strategic -> grid watcher is safe here.
    verdict, vwho = hades.watch(STANDING_GOAL, json.dumps(out), "aea-core", pool, meter)
    return out, who, verdict, vwho, reasoning

def main():
    n_ticks = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    seed = open(SEED_PATH, encoding="utf-8").read()
    state = load_state()
    print(f"=== THE AEA WAKES ===  (seed: {len(seed)} chars | prior memory: {len(state['memory'])} notes | starting at tick {state['tick']})")
    rods = energy.ladder("frontier", "private")   # the LIVE ladder (the old CORE_CHAIN banner crashed on a deleted name - review 2026-07-10)
    names = [p + "/" + m.rsplit("/", 1)[-1] for p, m in rods[:4]]
    print("core ladder: " + " -> ".join(names) + "\n")
    for i in range(n_ticks):
        t0 = time.time()
        out, who, verdict, vwho, reasoning = tick(seed, state)
        save_state(state)   # persist EVERY tick - the entity survives restart (true continuity)
        print(f"--- TICK {state['tick']}  (core: {who}, {round(time.time()-t0,1)}s) ---")
        print(f"  (mind thinks: {reasoning[:110].strip()}...)")
        print(f"  matters now : {out.get('matters_now','')}")
        print(f"  changed     : {out.get('changed','')}")
        print(f"  action      : {out.get('action','')}")
        print(f"  remembers   : {out.get('note_to_self','')}")
        print(f"  HADES       : ({vwho}) {verdict.get('verdict')} - {verdict.get('why','')[:90]}")
        if i < n_ticks - 1:
            time.sleep(3)   # a real loop sleeps ~30min or is scheduled; 3s here just to tick
    print(f"\n=== THE AEA SLEEPS ===  (persistent memory now {len(state['memory'])} notes across {state['tick']} total ticks)")
    print("continuity proof - the entity's evolving memory (survives restart via aea_state.json):")
    for m in state["memory"][-n_ticks:]:
        print(f"  {m}")

if __name__ == "__main__":
    main()
