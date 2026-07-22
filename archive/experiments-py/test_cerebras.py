"""Verify the Cerebras free-tier rate limit: the research report says 5 RPM / 30K TPM / 8K ctx
(a big downgrade from the 30 RPM we had). Fire a clean concurrent burst and see where it 429s."""
import grid, time
from concurrent.futures import ThreadPoolExecutor

MODEL = 'gpt-oss-120b'
def one(_):
    r = grid.call_openai('cerebras', MODEL, [{'role': 'user', 'content': 'hi'}], max_tokens=1, timeout=30)
    return r['status']

t0 = time.time()
with ThreadPoolExecutor(max_workers=12) as ex:
    res = list(ex.map(one, range(12)))
ok = sum(1 for s in res if s == 200); r429 = sum(1 for s in res if s == 429)
print(f"cerebras {MODEL} burst of 12:  ok={ok}  429={r429}  other={12-ok-r429}  in {round(time.time()-t0,1)}s")
print(f"  statuses: {res}")
print(f"  => real burst ceiling ~{ok} concurrent. Report claims 5 RPM.")
