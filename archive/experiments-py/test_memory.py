"""Phase 2 proof: memory turns hallucination into truth (A-axis L2, R-axis L3, seed 10).
Same node, same question - once blind, once grounded by recalled memory."""
import grid, memory, orchestrator, sys
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

print("Seeding local memory (Ollama mxbai embeddings)...")
n = memory.seed()
print(f"  {n} facts embedded\n")

Q = ("What is the AEA grid's total request capacity per minute, and roughly how many "
     "independent parallel nodes does it have? Be specific with numbers.")
pool = orchestrator.load_pool(); meter = grid.Meter()
node = orchestrator.pick(pool, 'bulk', 'public', meter)
print(f"node: {node['plant']}/{node['model']}")
print(f"QUESTION: {Q}\n")

r1 = grid.call_openai(node['plant'], node['model'], [{'role': 'user', 'content': Q}], max_tokens=180)
print("=== WITHOUT MEMORY (blind) ===")
print(r1['text'].strip()[:600])

facts = memory.recall(Q, 3)
ctx = "\n".join(f"- {f}" for f in facts)
r2 = grid.call_openai(node['plant'], node['model'],
                      [{'role': 'user', 'content': f"Answer using ONLY these facts:\n{ctx}\n\nQ: {Q}"}], max_tokens=180)
print("\n=== WITH MEMORY (recalled + injected) ===")
print("recalled:")
for f in facts:
    print(f"  * {f[:88]}")
print("\nanswer:")
print(r2['text'].strip()[:600])
