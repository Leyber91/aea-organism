# INCIDENT RECORD — 2026-08-04 history rewrite and runtime-data loss

**Status: CLOSED for the leak, PERMANENT for the data loss.**
Written the day after, from measurements, not from memory. Every SHA and byte count below was read
off the machine. This file exists so that what happened is undeniable and does not have to be
reconstructed by anyone later.

---

## 1 · WHAT WAS DONE, AND WHY

A full privacy sweep of the working tree and all commits found **307 HIGH-severity hits across 30
files already pushed to two public remotes** — the employer folder name inside absolute paths, the
operator's employment and financial circumstances in plain words, and his full name. **CRITICAL
(API keys, tokens, private keys): ZERO, in tree and history, then and now.**

A gitignore does nothing to a commit already pushed. The history was therefore rewritten with
`git filter-repo`, in three passes, and both remotes were force-pushed.

**Files purged from every commit:**

    archive/orphaned-data/data.js        employer folder inside absolute evidence paths, dozens of times
    data.js                              same file at its earlier path
    state/lab/gate_ledger.jsonl          employment circumstances, in the entity's own words
    state/lab/battery/facts.json         same
    state/outcomes.jsonl                 same, plus the operator's full name
    cr_start.log, live.log               absolute paths in tracebacks
    .claude/settings.json                permission entries carrying the home directory

**Strings redacted across every surviving blob:** the employer names, the absolute-path prefixes,
the full personal name, the employment phrases, and the transcript-directory slug.

---

## 2 · THE ARCHIVE — the original history is NOT destroyed

A complete bundle of every ref as it stood **before the first rewrite** was taken, verified, and
moved out of the session temp directory to durable storage **outside the repository**.

    file    2026-08-04_aea-city_PRE-REWRITE_full-history.bundle
    where   <repo parent>/_aea-archive/          NOT tracked, NOT pushed, deliberately
    size    281,030,707 bytes
    sha256  fedf6e44bb5f2d2c53aba654fa2c8a3201f45391c29184d61c339a5bea05c4f4
    verify  git bundle verify <file>   -> "records a complete history ... is okay"

**The record lives in this repository. The payload does not, and must not** — it contains exactly
what the rewrite removed. Anyone needing to prove what the history contained restores that bundle
into a scratch clone; the sha256 above makes substitution detectable.

### The boundary, in SHAs

| ref | BEFORE (in the archive) | AFTER (live) |
|---|---|---|
| `wip/checkpoint-2026-07-22` | `a6520a77ffdbab` | `3045ca23c72fd0` |
| `master` | `ea437c89ad534d` | `9749653986d7c4` |
| `aeagame_main` | `929f43eb1abdf3` | `0410a470448133` |
| `gh-pages` | `831b611a46dc64` | `831b611a46dc64` *(unchanged)* |
| remote `organism/main` | `2730e7b0b745b7` | force-pushed from `master` |
| remote `*/wip/checkpoint…` | `fa3d2f25c69c89` | force-pushed |

**Every SHA changed. Any other clone must be re-cloned, never pulled.**

---

## 3 · THE DAMAGE — runtime data was destroyed, and it is not recoverable

**This is the part that must not be softened.** `git filter-repo` checks out the rewritten tree
when it finishes. Runtime state files that were **tracked** were therefore reverted to their
**last committed content**, discarding everything appended since that commit. `state/` had not been
committed during the session, so the revert reached back to whenever those files were last
committed — before the session began.

    state/hands_ledger.jsonl    172,324 bytes measured mid-session
                             ->  111,869 bytes in HEAD, which is what the checkout wrote
                                 ~60 KB of appended runtime history destroyed

**Same mechanism, same exposure:** `state/r1_decisions.jsonl`, `state/decisions.jsonl`,
`state/perception.jsonl`, and every other tracked `.jsonl` under `state/` — **289 tracked files at
the time.**

**NOT affected**, because they were gitignored and a checkout does not touch ignored files:
`aea_state.json` (memory, intact at 865 entries), `wake.log`, `thinking.jsonl`, `events.jsonl`.

### The first measurable consequence

**R4b regressed from PROVEN to PARTIAL.** `measure_r4b` counts `hands_ledger.jsonl` rows where
`tool=="look_outward" AND src=="wake"` and the dispatch actually ran. The ladder printed
`7/3 dispatches across 2 topics` consistently throughout 2026-08-04. It now reads **1 dispatch,
1 topic** — the surviving wake rows are both dated **2026-08-02**, the ones that happened to be in
the last commit. The 08-03 and 08-04 dispatches were in the 60 KB.

**The rung was genuinely earned and its evidence was destroyed by a maintenance action.** Do not
re-litigate the rung; re-earn the evidence, or accept the ledger as truncated and say so on its page.

### Why it was not caught

After the final rewrite the full test suite was re-run — **191 frozen behaviours, 15 wiring, 17 R5,
20 hypotheses, 29 artefacts, 10 contradictions, 16 wake, all green.** `python -m aea.tooling.ladder`
was **not** re-run. No suite counts `hands_ledger` rows. One command would have caught it the same
minute. **Green suites are not a regression check for data.**

---

## 4 · THE RULE THIS BUYS

> **A history rewrite is a working-tree operation. Before running one, either commit every tracked
> runtime file or copy `state/` aside — the checkout at the end reverts tracked files to their last
> commit and silently discards every append since. And re-run the MEASUREMENTS afterwards, not only
> the tests: a suite proves behaviour, a ledger holds evidence, and only the second one can be
> quietly emptied.**

---

## 5 · WHAT REMAINS OPEN

- The ~60 KB is **gone**. It was never in git, so no bundle contains it.
- `state/` remains largely tracked (289 files). **The same loss will recur on the next rewrite**
  unless those files are untracked or copied aside first.
- The `web/ladder/` dossier was generated **before** the rewrite; its numbers may be stale.
  Regenerate with `python -m aea.tooling.page.rungsite` before citing it.
- `HANDOFF_R6.md` line 24 states R4b PROVEN with 7 dispatches. **That was true when written and is
  no longer measurable.** This file is the reason it is not simply an error in the handoff.
