"""HARDCORE swarm experiment v2 — rigorous test of which coordination patterns actually pay off.

Fixes over v1: 24 clean unambiguous numeric-answer questions (no ambiguous items); 5 cross-family
models; sampling temperature 0.7 so CLONES genuinely vary (a fair diversity baseline); 429/empty
RETRY so rate limits never masquerade as wrong answers; 3 trials averaged; and per-question
disagreement logging so we can test the REAL hypotheses, not just headline accuracy:

  H1  coordination beats a single model?           (mean acc per condition)
  H2  MODEL diversity beats SAMPLING diversity?     (C hetero-vote  vs  B clones-vote)  <- the true Law 2
  H3  a reasoning VERIFIER beats blind majority?     (D  vs  C),  especially on SPLIT questions
  Diagnostic: heterogeneity can only help on questions where models DISAGREE — quantify that.

Conditions:
  A single        MODELS[0], temp 0.2, one shot
  B clones x3     MODELS[0] x3, temp 0.7, majority vote        (pure sampling diversity)
  C hetero x3     MODELS[1..3] (3 families), temp 0.7, vote     (model diversity)
  D hetero+verify MODELS[1..3] propose, MODELS[0] adjudicates   (verifier over candidates)
"""
import grid, re, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

MODELS = [
    ("nvidia", "meta/llama-3.3-70b-instruct"),     # 0 strong default -> single, clones, adjudicator
    ("groq",   "openai/gpt-oss-120b"),             # 1 proposer (openai-oss family)
    ("nvidia", "deepseek-ai/deepseek-v4-flash"),   # 2 proposer (deepseek family)
    ("groq",   "llama-3.3-70b-versatile"),         # 3 proposer (meta-llama family)
]
TRIALS = 3
CONC = 8  # cap concurrency so we don't trip 40rpm and contaminate the science with rate-limit noise

QUESTIONS = [
    ("mult",     "What is 47 * 89? Reply with only the number.", "4183"),
    ("order",    "What is 8 - 2 * 3? Reply with only the number.", "2"),
    ("div",      "What is 144 / 16? Reply with only the number.", "9"),
    ("pct",      "What is 15% of 80? Reply with only the number.", "12"),
    ("discount", "A shirt costs $40 after a 20% discount. What was the original price in dollars? Reply with only the number.", "50"),
    ("batball",  "A bat and a ball cost $1.10 total. The bat costs $1.00 more than the ball. How many cents does the ball cost? Reply with only the number.", "5"),
    ("paren",    "What is (3 + 5) * 2 - 4? Reply with only the number.", "12"),
    ("pow",      "What is 2 to the power of 10? Reply with only the number.", "1024"),
    ("fact",     "What is 7! divided by 5! ? Reply with only the number.", "42"),
    ("sqrt",     "What is the square root of 169? Reply with only the number.", "13"),
    ("speed",    "A train travels 60 miles in 1.5 hours. What is its speed in miles per hour? Reply with only the number.", "40"),
    ("widgets",  "If 5 machines make 5 widgets in 5 minutes, how many minutes do 100 machines need to make 100 widgets? Reply with only the number.", "5"),
    ("race",     "In a race, you just overtook the runner in 2nd place. What position are you in now? Reply with only the number.", "2"),
    ("months",   "How many months in a year have at least 28 days? Reply with only the number.", "12"),
    ("sheep",    "A farmer has 17 sheep. All but 9 die. How many sheep are left alive? Reply with only the number.", "9"),
    ("strawb",   "How many times does the letter r appear in the word strawberry? Reply with only the number.", "3"),
    ("missi",    "How many times does the letter s appear in the word Mississippi? Reply with only the number.", "4"),
    ("vowels",   "How many vowels are in the word education? Reply with only the number.", "5"),
    ("minutes",  "How many minutes are in 2.5 hours? Reply with only the number.", "150"),
    ("cm",       "How many centimeters are in 2 meters? Reply with only the number.", "200"),
    ("feb",      "How many days were in February 2024? Reply with only the number.", "29"),
    ("hexagon",  "How many sides does a hexagon have? Reply with only the number.", "6"),
    ("rightang", "How many degrees are in a right angle? Reply with only the number.", "90"),
    ("syllog",   "All bloops are razzies. All razzies are lazzies. Are all bloops lazzies? Reply 1 for yes, 0 for no.", "1"),
]

def num(ans):
    n = re.findall(r"-?\d+", (ans or "").replace(",", ""))
    return n[-1] if n else ""

def ask(model, q, temp, retries=3):
    plant, mdl = model
    for a in range(retries):
        r = grid.call_openai(plant, mdl, [{"role": "user", "content": q}], max_tokens=40, temperature=temp)
        if r["ok"] and num(r["text"]): return num(r["text"])
        time.sleep(1.5 * (a + 1))  # 429/empty -> back off and retry so rate limits != wrong answers
    return ""

def vote(answers):
    a = [x for x in answers if x]
    return Counter(a).most_common(1)[0][0] if a else ""

def pasync(jobs):  # jobs: list of (model, q, temp)
    with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        return list(ex.map(lambda j: ask(*j), jobs))

# each returns (final_answer, proposer_answers)
def cond_A(q): return ask(MODELS[0], q, 0.2), []
def cond_B(q):
    a = pasync([(MODELS[0], q, 0.7)] * 3); return vote(a), a
def cond_C(q):
    a = pasync([(MODELS[1], q, 0.7), (MODELS[2], q, 0.7), (MODELS[3], q, 0.7)]); return vote(a), a
def cond_D(q):
    a = pasync([(MODELS[1], q, 0.7), (MODELS[2], q, 0.7), (MODELS[3], q, 0.7)])
    j = ask(MODELS[0], f"A question and three candidate answers from other models are given. "
            f"Reason and return ONLY the single correct number.\nQuestion: {q}\nCandidates: {a}", 0.2)
    return j, a

CONDS = [("A single", cond_A), ("B clones", cond_B), ("C hetero", cond_C), ("D verify", cond_D)]

# data[cond][qname] = list over trials of dict(final, ok, props)
data = {c: {qn: [] for qn, _, _ in QUESTIONS} for c, _ in CONDS}
for t in range(TRIALS):
    for cname, fn in CONDS:
        with ThreadPoolExecutor(max_workers=CONC) as ex:
            outs = list(ex.map(lambda it: (it[0], it[2], fn(it[1])), QUESTIONS))
        for qn, exp, (final, props) in outs:
            data[cname][qn].append(dict(final=final, ok=(final == exp), props=props))
    print(f"  trial {t+1}/{TRIALS} done", flush=True)

def acc(cname):  # mean accuracy across trials
    hits = sum(r["ok"] for qn in data[cname] for r in data[cname][qn])
    tot = sum(len(data[cname][qn]) for qn in data[cname])
    return hits / tot

# classify each question by hetero-proposer disagreement (trial 0), to find SPLIT questions
split = []
for qn, exp, _ in [(q[0], q[2], q[1]) for q in QUESTIONS]:
    props = data["C hetero"][qn][0]["props"]
    if props and len(set(props)) > 1: split.append(qn)

def acc_on(cname, qns):
    rs = [r for qn in qns for r in data[cname][qn]]
    return (sum(r["ok"] for r in rs) / len(rs)) if rs else float("nan")

print("\n=== ACCURACY (mean of 3 trials, 24 questions) ===")
for c, _ in CONDS:
    print(f"  {c:12} {acc(c)*100:5.1f}%")
print(f"\n  H1 coordination > single:   best-council {max(acc('C hetero'),acc('D verify'))*100:.1f}%  vs single {acc('A single')*100:.1f}%")
print(f"  H2 model-div > sampling-div: hetero {acc('C hetero')*100:.1f}%  vs clones {acc('B clones')*100:.1f}%")
print(f"  H3 verify > vote:            verify {acc('D verify')*100:.1f}%  vs hetero-vote {acc('C hetero')*100:.1f}%")
print(f"\n  SPLIT questions (proposers disagreed): {len(split)}/{len(QUESTIONS)} -> {split}")
if split:
    print(f"    on SPLIT only:  single {acc_on('A single',split)*100:.1f}% | clones {acc_on('B clones',split)*100:.1f}% "
          f"| hetero {acc_on('C hetero',split)*100:.1f}% | verify {acc_on('D verify',split)*100:.1f}%")
agree = [q[0] for q in QUESTIONS if q[0] not in split]
if agree:
    print(f"    on AGREE only:  single {acc_on('A single',agree)*100:.1f}% | hetero {acc_on('C hetero',agree)*100:.1f}%")

# per-question table (mean ok across trials)
print("\n=== PER-QUESTION (fraction correct across trials) ===")
print(f"  {'q':10} {'exp':>5}  A    B    C    D    split")
for qn, _, exp in QUESTIONS:
    def frac(c): return sum(r["ok"] for r in data[c][qn]) / len(data[c][qn])
    print(f"  {qn:10} {exp:>5}  {frac('A single'):.2f} {frac('B clones'):.2f} {frac('C hetero'):.2f} {frac('D verify'):.2f}   {'Y' if qn in split else ''}")
