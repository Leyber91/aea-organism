# DEV DIARY — how any conversation takes over

This repo is built to be handed off. A new conversation (a fresh agent, or Luis in a new session)
should be able to take over development from the repository itself, cheaply, without re-reading
everything. This folder is the running record that makes that possible.

## START OF SESSION — read in this order (cheap → deep)

1. **`/README.md`** — what the project is + the repo map.
2. **`/graph.json`** — the deterministic knowledge-graph (modules, imports, endpoints, design,
   state, web). **Query the node you need and its edges; do NOT re-scan the tree.** This is the
   token-saver: pre-structured map instead of brute-force file reads. Refresh it with
   `python aea/build_graph.py` after any structural change.
3. **`diary/SESSION_LOG.md`** — the latest entry: current state, what's `LOCKED`, and the exact
   next task. Start from `NEXT`; do not re-litigate `LOCKED`.
4. **`/GAME_PLAN.md`** + `design/` — the design, read on demand (via graph.json's design nodes).

## END OF SESSION — append one entry to `SESSION_LOG.md`

So the next session starts warm. One entry must carry: **what shipped**, **how it was verified**
(the command + result — never "it compiles in my head"), **what broke**, **the next task**, and
**the exact command to re-verify**. If the file/module structure changed, regenerate the graph.

## What's in this folder

- **`SESSION_LOG.md`** — the running dev journal (append-only; latest entry at top).
- **`REORG_PLAN.md`** — record of the 2026-07-22 root reorg (126 loose files → clean tree).

## The token rule (why the graph exists)

Graph-based structural maps cut an agent's token use dramatically by replacing broad file reads and
brute-force searches with precise structural queries: pull only the directly-connected neighbourhood
of a node, avoid context rot from irrelevant data, and cache the map (`graph.json`) so future
queries never re-analyse the source. Use it: orient from `graph.json`, open only the files its edges
point you to.

## References

`/references/` holds the external reference material a takeover agent needs (design/AEA sources,
portfolio references). The diary points there; that folder's own README says what's in it.
