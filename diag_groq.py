import grid, json, urllib.request, urllib.error
k = grid.key('GROQ_API_KEY')
body = json.dumps({"model": "openai/gpt-oss-120b", "max_tokens": 200,
    "messages": [{"role": "user", "content": "Verdict for goal=list 3, output=a,b,c"}],
    "response_format": {"type": "json_schema", "json_schema": {"name": "v", "strict": True,
        "schema": {"type": "object", "additionalProperties": False,
                   "properties": {"ok": {"type": "boolean"}}, "required": ["ok"]}}}}).encode()
req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=body,
    headers={"Content-Type": "application/json", "User-Agent": "x", "Authorization": "Bearer " + k}, method="POST")
try:
    print("OK:", urllib.request.urlopen(req, timeout=30).read().decode()[:300])
except urllib.error.HTTPError as e:
    print("HTTP", e.code, ":", e.read().decode()[:500])
