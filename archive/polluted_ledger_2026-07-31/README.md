# The production hands ledger, 2026-07-31, quarantined because 100% of it was synthetic.

4,925 rows. Every one written between 01:34 and 02:30 by `redteam.py` development and two
certificate runs. `decision_id` is null on 4,924 of 4,925. **Zero rows of real wake traffic** - the
three real R2 tool invocations from the 100-tick gate predate the ledger's existence.

WHY IT LOOKED REAL. Only 5 rows contain the canary. The canary payloads are REFUSED BEFORE THE
BOUNDARY and never reach a row; the 4,920 rows that did cross are clean moves - `read_state`,
`self_map`, `list_tools`, `calc 2+2` - which are indistinguishable from entity history by content.

WHY IT MATTERED. R3's bound gate is *the stored outcome matches the ledger*, and
`aea/lab/containment.py` already reads this file. Unlabelled, that gate would have certified
outcomes against 4,920 actions that never happened in a real tick - a FALSE OUTCOME RECORD, which is
R3's named hazard, manufactured by the instrument built to prevent it.

FIXED: `hands._ledger_path()` resolves at call time and honours `AEA_HANDS_LEDGER`; `redteam.py`
points it at its own temp directory; every row carries `src`, defaulting to `unattributed` rather
than `wake`, so an unlabelled caller is EXCLUDED from entity history instead of promoted into it.

Kept rather than deleted: it is the evidence for D48.
