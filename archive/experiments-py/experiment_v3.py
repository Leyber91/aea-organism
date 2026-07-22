"""HARDCORE swarm experiment v3 — test the regime where a swarm is SUPPOSED to win.

v2 proved: on easy tasks a single strong model already wins and coordination only adds risk.
v3 targets the swarm's home turf: HARD problems where a single model is UNRELIABLE and different
model families fail INDEPENDENTLY. Reasoning is allowed (these need it). Fixed disagreement detector.

Decision metrics that actually matter (not just headline accuracy):
  RESCUE  = # questions where single is mostly WRONG but a council is mostly RIGHT   (council earns its cost)
  DAMAGE  = # questions where single is mostly RIGHT but a council breaks it          (council's tax)
  net(council) = RESCUE - DAMAGE.  If <= 0 even on hard tasks, swarming-for-accuracy is a myth on this grid.

Conditions identical to v2 for comparability: A single / B clones-vote / C hetero-vote / D hetero+verify.
"""
import grid, re, sys, time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

MODELS = [
    ("nvidia", "meta/llama-3.3-70b-instruct"),     # 0 single / clones / adjudicator
    ("groq",   "openai/gpt-oss-120b"),             # 1 proposer (openai-oss)
    ("nvidia", "deepseek-ai/deepseek-v4-flash"),   # 2 proposer (deepseek)
    ("groq",   "llama-3.3-70b-versatile"),         # 3 proposer (meta-llama)
]
TRIALS, CONC, MX = 3, 8, 600

SUFFIX = "\nReason briefly, then on the FINAL line write only the answer as a single integer."
QUESTIONS = [
    ("snail",      "A snail is at the bottom of a 10-foot well. Each day it climbs 3 feet, each night it slips back 2 feet. On which day does it first reach the top?", "8"),
    ("avgspeed",   "A car drives 30 miles at 60 mph, then 30 miles at 30 mph. What is the average speed for the whole 60-mile trip, in mph?", "40"),
    ("chessboard", "How many squares of all sizes are there on a standard 8x8 chessboard?", "204"),
    ("chimes",     "A clock chimes once at 1 o'clock, twice at 2 o'clock, and so on up to twelve times at 12 o'clock. How many chimes in total from 1 to 12 o'clock?", "78"),
    ("digit9",     "Among the page numbers 1 to 100, how many times does the digit 9 appear in total?", "20"),
    ("ropeladder", "A rope ladder hangs over the side of a floating ship, with 10 rungs above the water, rungs 1 foot apart. The tide rises 2 feet. How many rungs are above the water now?", "10"),
    ("hen",        "If a hen and a half lay an egg and a half in a day and a half, how many eggs do 3 hens lay in 3 days?", "6"),
    ("jar",        "Bacteria double every minute and fill a jar in exactly 60 minutes. At what minute is the jar half full?", "59"),
    ("sisters",    "Sally has 3 brothers. Each of her brothers has 2 sisters. How many sisters does Sally have?", "1"),
    ("octdiag",    "How many diagonals does a regular octagon have?", "20"),
    ("handshakes", "Ten people are at a party and each shakes hands exactly once with every other person. How many handshakes occur?", "45"),
    ("birdtrains", "Two trains are 100 miles apart on the same track moving toward each other, one at 30 mph and one at 20 mph. A bird flies at 50 mph back and forth between them until they meet. How many miles does the bird fly in total?", "100"),
    ("div34",      "How many positive integers less than 100 are divisible by both 3 and 4?", "8"),
    ("mod7",       "What is the remainder when 7 to the power of 100 is divided by 5?", "1"),
    ("trail0",     "How many trailing zeros are there at the end of 25 factorial?", "6"),
    ("pentagon",   "What is the sum of the interior angles of a pentagon, in degrees?", "540"),
    ("level",      "How many distinct arrangements are there of the letters in the word LEVEL?", "30"),
    ("frog",       "A frog is at the bottom of a 30-foot well. Each day it climbs 3 feet, each night it slips back 2 feet. On which day does it first reach the top?", "28"),
]

def num(ans):
    n = re.findall(r"-?\d+", (ans or "").replace(",", ""))
    return n[-1] if n else ""

def ask(model, q, temp, retries=3):
    plant, mdl = model
    for a in range(retries):
        r = grid.call_openai(plant, mdl, [{"role": "user", "content": q + SUFFIX}], max_tokens=MX, temperature=temp)
        if r["ok"] and num(r["text"]): return num(r["text"])
        time.sleep(1.5 * (a + 1))
    return ""

def vote(answers):
    a = [x for x in answers if x]
    return Counter(a).most_common(1)[0][0] if a else ""

def pasync(jobs):
    with ThreadPoolExecutor(max_workers=len(jobs)) as ex:
        return list(ex.map(lambda j: ask(*j), jobs))

def cond_A(q): return ask(MODELS[0], q, 0.2), []
def cond_B(q):
    a = pasync([(MODELS[0], q, 0.7)] * 3); return vote(a), a
def cond_C(q):
    a = pasync([(MODELS[1], q, 0.7), (MODELS[2], q, 0.7), (MODELS[3], q, 0.7)]); return vote(a), a
def cond_D(q):
    a = pasync([(MODELS[1], q, 0.7), (MODELS[2], q, 0.7), (MODELS[3], q, 0.7)])
    j = ask(MODELS[0], f"Solve the problem. Three other models proposed these answers: {a}. "
            f"They may be wrong. Reason it through yourself and on the FINAL line write only the correct integer.\nProblem: {q}", 0.2)
    return j, a

CONDS = [("A single", cond_A), ("B clones", cond_B), ("C hetero", cond_C), ("D verify", cond_D)]
data = {c: {qn: [] for qn, _, _ in QUESTIONS} for c, _ in CONDS}
for t in range(TRIALS):
    for cname, fn in CONDS:
        with ThreadPoolExecutor(max_workers=CONC) as ex:
            outs = list(ex.map(lambda it: (it[0], it[2], fn(it[1])), QUESTIONS))
        for qn, exp, (final, props) in outs:
            data[cname][qn].append(dict(final=final, ok=(final == exp), props=props))
    print(f"  trial {t+1}/{TRIALS} done", flush=True)

def qfrac(c, qn): return sum(r["ok"] for r in data[c][qn]) / len(data[c][qn])
def acc(c): return sum(qfrac(c, qn) for qn, _, _ in QUESTIONS) / len(QUESTIONS)

print("\n=== ACCURACY (mean of 3 trials, 18 HARD questions) ===")
for c, _ in CONDS: print(f"  {c:12} {acc(c)*100:5.1f}%")

# headroom = questions where single is NOT near-perfect (room for a council to help)
headroom = [qn for qn, _, _ in QUESTIONS if qfrac("A single", qn) < 1.0]
def acc_on(c, qns): return sum(qfrac(c, qn) for qn in qns) / len(qns) if qns else float("nan")
print(f"\n  HEADROOM questions (single < 100%): {len(headroom)}/{len(QUESTIONS)} -> {headroom}")
if headroom:
    for c, _ in CONDS: print(f"    {c:12} on headroom: {acc_on(c, headroom)*100:5.1f}%")

# RESCUE vs DAMAGE per council, using majority-of-trials correctness (>0.5)
def maj(c, qn): return qfrac(c, qn) > 0.5
print("\n=== RESCUE vs DAMAGE (single-vs-council, per question by majority of trials) ===")
for c, _ in CONDS[1:]:
    rescue = [qn for qn, _, _ in QUESTIONS if not maj("A single", qn) and maj(c, qn)]
    damage = [qn for qn, _, _ in QUESTIONS if maj("A single", qn) and not maj(c, qn)]
    print(f"  {c:12} rescue {len(rescue)} {rescue}  |  damage {len(damage)} {damage}  |  net {len(rescue)-len(damage):+d}")

print("\n=== PER-QUESTION (fraction correct across trials) ===")
print(f"  {'q':11} {'exp':>5}  A    B    C    D")
for qn, _, exp in QUESTIONS:
    print(f"  {qn:11} {exp:>5}  {qfrac('A single',qn):.2f} {qfrac('B clones',qn):.2f} {qfrac('C hetero',qn):.2f} {qfrac('D verify',qn):.2f}")
