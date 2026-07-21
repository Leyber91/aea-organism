"""Measure REAL local capability on this machine (Ollama). Verify-don't-claim."""
import grid, time, urllib.request, json

def gen(model, prompt, mx=120):
    t = time.time()
    r = grid.call_openai('ollama', model, [{'role': 'user', 'content': prompt}], max_tokens=mx, timeout=240)
    dt = time.time() - t
    tps = round(r['tokens'] / dt, 1) if (dt and r.get('tokens')) else 0
    note = '' if r['ok'] else (' ERR ' + str(r.get('error'))[:50])
    print(f"  {model:24} ok={r['ok']} tokens={r['tokens']:>3} {round(dt,1):>5}s  {tps:>5} tok/s{note}")

print("LOCAL LLM (Ollama) - 1st qwen3:8b call loads to VRAM, 2nd is warm:")
for m in ['qwen3:8b', 'qwen3:8b', 'qwen3:1.7b', 'deepseek-r1:8b']:
    gen(m, 'Write two sentences about Mars.')

print("\nLOCAL EMBEDDINGS (the memory layer):")
body = json.dumps({'model': 'mxbai-embed-large', 'input': 'the entity remembers the day'}).encode()
req = urllib.request.Request('http://localhost:11434/v1/embeddings', data=body, headers={'Content-Type': 'application/json'})
t = time.time()
try:
    e = json.loads(urllib.request.urlopen(req, timeout=60).read())
    print(f"  mxbai-embed-large        dims={len(e['data'][0]['embedding'])}  {round(time.time()-t,2)}s")
except Exception as ex:
    print(f"  mxbai-embed-large FAILED: {ex}")
