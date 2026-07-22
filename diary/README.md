# DEV DIARY — how any conversation takes over

This repo is built to be handed off. A new conversation (a fresh agent, or Luis in a new session)
should be able to take over development from the repository itself, cheaply, without re-reading
everything. This folder is the running record that makes that possible.

## START OF SESSION — read in this order (cheap → deep)

0. **`/CLAUDE.md`** — the introduction. HOW to work here and WHERE everything is. Stable: it does
   not carry state, so it rarely changes. In Claude Code it auto-loads, so you have often already
   read it before you get here — it is what sends you to the graph and this log.
1. **`/graph.json`** — the deterministic knowledge-graph (modules, imports, endpoints, design,
   state, web). **Query the node you need and its edges; do NOT re-scan the tree.** This is the
   token-saver: pre-structured map instead of brute-force file reads. Refresh it with
   `python aea/build_graph.py` after any structural change.
2. **`diary/SESSION_LOG.md`** — the latest entry: current state, what's `LOCKED`, and the exact
   next task. Start from `NEXT`; do not re-litigate `LOCKED`.
3. **`diary/DISCOVERIES.md`** — *why* the plan is what it is (inherit the reasoning, not just the
   result). The raw sparks that feed these live in **`diary/REFLECTIONS.md`** — read it for the frontier.
4. **`/GAME_PLAN.md`** + `design/` — the design, read on demand (via graph.json's design nodes).

**The division of labour, in one line:** `CLAUDE.md` = the method + the map (stable) · this diary =
the state (updated every session). If you ever want to record progress in `CLAUDE.md`, use the log instead.

## END OF SESSION — append one entry to `SESSION_LOG.md`

So the next session starts warm. One entry must carry: **what shipped**, **how it was verified**
(the command + result — never "it compiles in my head"), **what broke**, **the next task**, and
**the exact command to re-verify**. If the file/module structure changed, regenerate the graph.

## What's in this folder

- **`SESSION_LOG.md`** — the running dev journal (append-only; latest entry at top). THE STATE.
- **`REFLECTIONS.md`** — Luis's raw realizations, captured mess-first (upstream of DISCOVERIES). THE SPARKS.
- **`DISCOVERIES.md`** — the load-bearing findings (why the plan is what it is), as graph nodes.
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
