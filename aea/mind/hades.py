"""hades.py - HADES: the WATCHER over the SEDAH swarm.

CONSTELLATION LAW 3 (the SEDAH Law): every autonomous layer gets a watcher that does NO other work;
it converts "it runs by itself" into "it runs by itself AND I can still answer for it."

ADAPTED from Luis's old canon (a distilgpt2 society on a laptop) to what we run NOW: HADES does no
task work - it watches a worker's output against the ORIGINAL goal and, on drift or wrong-work,
RE-GROUNDS (Focused ReAct) or REROUTES to a DIFFERENT model (Law 2: heterogeneity beats clones),
logging every decision = the accountability trail. The watcher is cheap, fast, and a DIFFERENT model
than the workers. Its own watcher is Luis, on top (Law 6: the human is a link)."""
import sys, json, re, urllib.request
from aea.kernel import grid
from aea.mind import orchestrator
from aea.mind import swarm
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

VERDICT_SCHEMA = {"type": "object", "additionalProperties": False,
    "properties": {"on_goal": {"type": "boolean"}, "correct": {"type": "boolean"},
                   "verdict": {"type": "string"},
                   "why": {"type": "string"}},
    "required": ["on_goal", "correct", "verdict", "why"]}

def watch(goal, attempt, worker, pool, meter):
    """The watcher JUDGES (does no work). Uses Groq strict-mode JSON (research: 100% schema adherence
    on gpt-oss-120b) so the verdict ALWAYS parses - a watcher that can't reliably report is useless."""
    k = grid.key('GROQ_API_KEY')
    if k:
        try:
            body = json.dumps({"model": "openai/gpt-oss-120b", "temperature": 0, "max_tokens": 1500,  # reasoning model: needs room to think THEN emit the strict JSON (250 -> 400 json_validate_failed)
                "messages": [{"role": "user", "content": f"You are HADES, a watcher; you do no work, you ONLY judge a worker's output against the ORIGINAL GOAL. Be strict. verdict must be one of: accept | redo | reground | halt.\nGOAL: {goal}\nWORKER OUTPUT: {attempt[:700]}"}],
                "response_format": {"type": "json_schema", "json_schema": {"name": "verdict", "strict": True, "schema": VERDICT_SCHEMA}}}).encode()
            req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=body,
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0 aea", "Authorization": f"Bearer {k}"}, method="POST")
            c = json.loads(urllib.request.urlopen(req, timeout=40).read())["choices"][0]["message"]["content"]
            meter.record("groq", "openai/gpt-oss-120b")
            return json.loads(c), "groq/gpt-oss-120b (strict-json)"
        except Exception as e:
            print(f"     (strict watcher failed: {str(e)[:50]}; falling back)")
    n = swarm.pick_varied(pool, 'reflex', meter) or orchestrator.pick(pool, 'bulk', 'public', meter)
    r = orchestrator.call_node(n, f"Judge vs GOAL. GOAL: {goal}\nWORKER: {attempt[:600]}\nOutput ONLY JSON {{\"on_goal\":bool,\"correct\":bool,\"verdict\":\"accept|redo|reground|halt\",\"why\":\"...\"}}", meter, 150)
    try:
        return json.loads(re.search(r'\{.*\}', r['text'], re.S).group(0)), f"{n['plant']}/{n['model']}"
    except Exception:
        # a watcher that cannot produce a verdict must FLAG, never silently accept (that is rubber-stamping)
        return {"on_goal": False, "correct": False, "verdict": "unverified", "why": "watcher could not parse a verdict"}, f"{n['plant']}/{n['model']}"

def watch_local(goal, attempt, meter, worker_model="granite4.1:3b"):
    """Private-safe watcher (Law 3 + the privacy boundary): judges on a LOCAL Ollama model DIFFERENT from the
    worker (Law 2 heterogeneity), so the verdict over PRIVATE content never leaves the machine. Loose JSON parse."""
    model = "llama3.1:8b" if "granite" in (worker_model or "") else "granite4.1:3b"
    r = grid.call_openai("ollama", model, [{"role": "user", "content":
        "You are HADES, a watcher. You do no work; you ONLY judge the brief below against the GOAL. The brief has three "
        "markdown sections: '## What you're moving on', '## One opportunity', '## Today'. Rule: on_goal=true and correct=true "
        "if EACH of the three sections contains at least one line of real content (be lenient about brevity; a present "
        "section is a pass). Only set verdict='redo' if a section is empty, missing, or shows an error. "
        "Output ONLY one JSON object: {\"on_goal\":true_or_false,\"correct\":true_or_false,"
        "\"verdict\":\"accept|redo|reground|halt\",\"why\":\"short reason\"}.\n"
        f"GOAL: {goal}\nBRIEF:\n{attempt[:1600]}"}], max_tokens=700, temperature=0, timeout=120)
    if r.get("ok"):
        meter.record("ollama", model)
    try:
        return json.loads(re.search(r"\{.*\}", r["text"], re.S).group(0)), f"ollama/{model} (local watcher)"
    except Exception:
        return {"on_goal": False, "correct": False, "verdict": "unverified", "why": "local watcher could not parse a verdict"}, f"ollama/{model}"


def oversee(goal, zone='public', max_interventions=3):
    pool = orchestrator.load_pool(); meter = grid.Meter()
    print(f"GOAL: {goal}\n")
    log, used, grounded, final = [], set(), goal, ""
    for i in range(max_interventions + 1):
        worker = orchestrator.pick(pool, 'bulk', zone, meter, exclude=used)
        if not worker: break
        used.add((worker['plant'], worker['model']))
        r = orchestrator.call_node(worker, f"GOAL: {grounded}\nAnswer directly, nothing else.", meter, 300)
        final = (r['text'] if r['ok'] else 'ERR').strip()
        v, who = watch(goal, final, f"{worker['plant']}/{worker['model']}", pool, meter)
        accept = v.get('verdict') == 'accept' or (v.get('on_goal') and v.get('correct'))
        print(f"  attempt {i+1}: WORKER {worker['plant']}/{worker['model']}")
        print(f"     output : {final[:90]}")
        print(f"     HADES  : ({who}) on_goal={v.get('on_goal')} correct={v.get('correct')} -> {v.get('verdict')}  [{v.get('why')}]")
        log.append({"attempt": i + 1, "worker": f"{worker['plant']}/{worker['model']}", "watcher": who,
                    **{k: v.get(k) for k in ('on_goal', 'correct', 'verdict', 'why')}})
        if accept:
            print(f"\n  HADES ACCEPTED after {i+1} attempt(s).  (accountable: a watcher signed off)"); break
        if v.get('verdict') == 'halt':
            print(f"\n  HADES HALTED: {v.get('why')}"); break
        if v.get('verdict') == 'reground':
            grounded = f"{goal}\nSTAY STRICTLY ON THIS - a prior attempt drifted: {v.get('why')}"
        # else: redo with a DIFFERENT worker (heterogeneity)
    print(f"\n=== HADES OVERSIGHT LOG (the accountability trail) ===")
    print(json.dumps(log, indent=2))
    return final, log

if __name__ == '__main__':
    # a constraint task a worker can easily drift on (add prose / wrong items) -> HADES catches it
    oversee("List exactly three countries that border Germany, as a bare comma-separated list with NO other words.")
