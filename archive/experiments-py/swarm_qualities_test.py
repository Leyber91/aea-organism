"""HARDCORE swarm test: objective-answer questions (known truth, deterministic grading) across four
coordination conditions, to measure which swarm QUALITIES actually pay off and which models to trust.

  A. SINGLE         - one strong model, one shot (the baseline)
  B. CLONES x3      - same model x3, majority vote  (Law 2 says clones share blind spots -> no gain)
  C. HETERO x3      - three DIFFERENT models, majority vote  (Law 2: heterogeneity beats clones)
  D. HETERO+VERIFY  - three different propose, a fourth DIFFERENT model adjudicates  (full swarm)

Hypothesis (Constellation Law 2 + M-axis): D >= C > B ~= A."""
import grid, orchestrator, re, sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
try: sys.stdout.reconfigure(encoding='utf-8')
except Exception: pass

# diverse, all-4/4, cross-vendor models (heterogeneity by construction)
HETERO = [
    {"plant": "nvidia", "model": "meta/llama-3.3-70b-instruct"},
    {"plant": "groq",   "model": "openai/gpt-oss-120b"},
    {"plant": "nvidia", "model": "deepseek-ai/deepseek-v4-flash"},
    {"plant": "groq",   "model": "llama-3.3-70b-versatile"},
]
SINGLE = HETERO[0]

QUESTIONS = [  # (name, prompt, known answer)
    ("bat_ball",   "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How many CENTS does the ball cost? Answer with only the number.", "5"),
    ("strawberry", "How many times does the letter r appear in the word strawberry? Answer with only the number.", "3"),
    ("order_ops",  "What is 8 - 2 * 3? Answer with only the number.", "2"),
    ("discount",   "A shirt costs $40 after a 20% discount. What was the original price in dollars? Answer with only the number.", "50"),
    ("apples",     "I have 3 apples and I take away 2. How many apples do I now physically hold? Answer with only the number.", "2"),
    ("leap_feb",   "How many days were in February 2024? Answer with only the number.", "29"),
]

def ask(node, q, mx=24):
    r = grid.call_openai(node["plant"], node["model"], [{"role": "user", "content": q}], max_tokens=mx)
    return r["text"] if r["ok"] else ""

def num(ans):
    n = re.findall(r"-?\d+\.?\d*", (ans or "").replace(",", ""))
    return n[-1].rstrip(".0") or n[-1] if n else ""

def correct(ans, exp):
    return num(ans) == exp or exp in re.findall(r"-?\d+", (ans or "").replace(",", ""))

def parallel_ask(nodes, q):
    with ThreadPoolExecutor(max_workers=len(nodes)) as ex:
        return list(ex.map(lambda n: ask(n, q), nodes))

def single(q):  return ask(SINGLE, q)
def clones(q):  return Counter(num(a) for a in parallel_ask([SINGLE] * 3, q) if num(a)).most_common(1)[0][0] if any(parallel_ask([SINGLE], q)) else ""
def hetero(q):
    votes = [num(a) for a in parallel_ask(HETERO[:3], q) if num(a)]
    return Counter(votes).most_common(1)[0][0] if votes else ""
def hetero_verify(q):
    props = parallel_ask(HETERO[:3], q)
    j = ask(HETERO[3], f"Question: {q}\nCandidate answers from three models: {props}\nReturn ONLY the single correct number.")
    return j

CONDS = [("A single", single), ("B clones x3", clones), ("C hetero x3", hetero), ("D hetero+verify", hetero_verify)]
print(f"{'condition':16} " + " ".join(f"{q[0][:9]:>9}" for q in QUESTIONS) + "   ACC")
score = {}
for cname, fn in CONDS:
    row, hits = [], 0
    for qn, q, exp in QUESTIONS:
        ans = fn(q); ok = correct(str(ans), exp); hits += ok
        row.append(("OK " if ok else f"x{num(str(ans)) or '?'}")[:9])
    score[cname] = hits
    print(f"{cname:16} " + " ".join(f"{c:>9}" for c in row) + f"   {hits}/{len(QUESTIONS)}")

print("\n=== VERDICT ===")
for c, _ in CONDS:
    print(f"  {c:16} {score[c]}/{len(QUESTIONS)}  ({round(100*score[c]/len(QUESTIONS))}%)")
print(f"  Law 2 (heterogeneity beats clones): {'CONFIRMED' if score['C hetero x3'] > score['B clones x3'] else 'not shown'} "
      f"(hetero {score['C hetero x3']} vs clones {score['B clones x3']})")
print(f"  coordination beats single: {'CONFIRMED' if max(score['C hetero x3'], score['D hetero+verify']) > score['A single'] else 'not shown'}")
