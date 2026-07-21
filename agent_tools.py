"""agent_tools.py - Phase 3: the agent reaches PAST its own weights.

Real tools (live web fetch + exact calculator) via OpenAI-compatible tool-calling on the FREE grid.
= AEA A-axis L3 (+tools) + seed-8 (transcendence toolset). The point: if we can't pay for AI tomorrow,
the free swarm can still ACT on the world - fetch live data, compute - not just talk from stale weights."""
import grid, json, urllib.request, sys, re
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

# ---- real tools (actually run) ----
def web_fetch(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'aea-agent/0.1'})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode('utf-8', 'ignore')[:8000]
    except Exception as e:
        return f"ERROR: {e}"

def calc(expression):
    if not re.fullmatch(r'[\d\s+\-*/().%]+', expression or ''):
        return "ERROR: arithmetic only"
    try:
        return str(eval(expression, {'__builtins__': {}}, {}))
    except Exception as e:
        return f"ERROR: {e}"

def json_get(url, key):
    """Fetch a JSON URL and return ONE field deterministically (the tool does the extraction)."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'aea-agent/0.1'})
        d = json.loads(urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore'))
        for k in str(key).split('.'):
            d = d[int(k)] if isinstance(d, list) else d[k]
        return str(d)
    except Exception as e:
        return f"ERROR: {e}"

IMPL = {'web_fetch': lambda a: web_fetch(a.get('url', '')),
        'calc':      lambda a: calc(a.get('expression', '')),
        'json_get':  lambda a: json_get(a.get('url', ''), a.get('key', ''))}

TOOLS = [
    {"type": "function", "function": {"name": "web_fetch",
        "description": "HTTP GET a URL and return the response body text (truncated). Use for LIVE internet data and APIs.",
        "parameters": {"type": "object", "properties": {"url": {"type": "string", "description": "full URL including https://"}}, "required": ["url"]}}},
    {"type": "function", "function": {"name": "calc",
        "description": "Evaluate an arithmetic expression exactly (e.g. '92837 * 4471').",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "json_get",
        "description": "Fetch a JSON URL and return ONE field's value (top-level key, or dotted/indexed path like 'owner.login'). Prefer this over web_fetch when you need a specific field from an API.",
        "parameters": {"type": "object", "properties": {"url": {"type": "string"}, "key": {"type": "string"}}, "required": ["url", "key"]}}},
]

def chat(plant, model, messages, max_tokens=500):
    cap = grid.PLANTS[plant]
    url = cap['base'].rstrip('/') + '/chat/completions'
    headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 aea-agent'}
    if cap['auth']:
        headers['Authorization'] = 'Bearer ' + (grid.key(cap['auth']) or '')
    body = json.dumps({'model': model, 'messages': messages, 'tools': TOOLS,
                       'tool_choice': 'auto', 'max_tokens': max_tokens, 'temperature': 0.1}).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())['choices'][0]['message']

def run_agent(task, plant='nvidia', model='meta/llama-3.3-70b-instruct', max_turns=5):
    messages = [{"role": "user", "content": f"TASK (your goal): {task}\nUse the tools when they help. State the final answer directly when done."}]
    print(f"AGENT: {plant}/{model}\nTASK: {task}")
    for turn in range(max_turns):
        try:
            msg = chat(plant, model, messages)
        except Exception as e:
            print(f"  ERROR: {e}"); return f"ERR {e}"
        tcs = msg.get('tool_calls')
        if tcs:
            messages.append(msg)
            for tc in tcs:
                name = tc['function']['name']
                try: args = json.loads(tc['function']['arguments'])
                except Exception: args = {}
                result = IMPL.get(name, lambda a: 'unknown tool')(args)
                print(f"  turn {turn+1}: TOOL {name}({json.dumps(args)[:70]}) -> {str(result)[:90].strip()}")
                messages.append({"role": "tool", "tool_call_id": tc.get('id', ''), "content": str(result)[:2000]})
        else:
            print(f"  ANSWER ({turn+1} turns): {(msg.get('content') or '').strip()[:400]}\n")
            return msg.get('content', '')
    return "(hit max turns)"

if __name__ == '__main__':
    print("=== PHASE 3: the free grid reaching the live internet via tool-calling ===\n")
    run_agent("How many stargazers does the GitHub repo ollama/ollama currently have? "
              "Use web_fetch on https://api.github.com/repos/ollama/ollama and read stargazers_count.")
    print("--- calc tool ---")
    run_agent("Use the calc tool to compute 92837 * 4471, then tell me the exact result.")
