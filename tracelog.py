"""tracelog.py - the trace substrate the whole swarm stands on.

Every node carries its GOAL-STACK (root -> ... -> me) so any depth can look UP at the bigger picture
(vertical lineage = anti-drift by construction). Two stores, by design (they are NOT the same thing):
  - registry (in-memory): the ACTIVE nodes + their current target -> what a discriminator reads each tick
  - log (append-only JSONL): every spawn/step/result with rationale  -> the history you mine to IMPROVE
A node may have MULTIPLE parents (merge = the tree becomes a DAG); both lineages are tracked so a fused
node can report up both paths. Cycles are refused (stay a DAG). This is the floor under the discriminator,
the crystallizer, and HADES-as-tree-overseer.
"""
import json, os, time, threading

HERE = os.path.dirname(os.path.abspath(__file__))


class Node:
    __slots__ = ("id", "parents", "goal", "goal_stack", "depth", "zone", "status", "model", "result", "children")

    def __init__(self, nid, parents, goal, goal_stack, depth, zone):
        self.id = nid; self.parents = parents; self.goal = goal; self.goal_stack = goal_stack
        self.depth = depth; self.zone = zone; self.status = "active"; self.model = None
        self.result = None; self.children = []


class Trace:
    def __init__(self, root_goal, path=None):
        self.path = path or os.path.join(HERE, "brief_trace.jsonl")
        self.lock = threading.Lock(); self._n = 0
        self.nodes = {}; self.registry = {}      # id->Node ; id->{goal,depth,zone} for ACTIVE nodes only
        open(self.path, "w", encoding="utf-8").close()   # fresh log per run
        self.root = self.spawn(root_goal, parent=None, zone="public", depth=0, why="root goal")

    def _id(self):
        self._n += 1; return f"n{self._n}"

    def _log(self, event):
        event["t"] = round(time.time(), 3)
        with self.lock:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def spawn(self, goal, parent=None, zone=None, depth=None, why=""):
        """Create a node. parent: a Node, a LIST of Nodes (merge -> DAG), or None (root)."""
        with self.lock:      # the whole mutation, not just the id (review 2026-07-10: nodes/children/
            nid = self._id() # registry were mutated unlocked - a torn tree under concurrent spawns)
            parents = [] if parent is None else (parent if isinstance(parent, list) else [parent])
            # cycle guard: parents pre-exist; children only ever point forward -> DAG stays acyclic
            gstack = (parents[0].goal_stack if parents else []) + [goal]
            d = depth if depth is not None else (parents[0].depth + 1 if parents else 0)
            z = zone if zone is not None else (parents[0].zone if parents else "public")
            node = Node(nid, [p.id for p in parents], goal, gstack, d, z)
            self.nodes[nid] = node
            for p in parents:
                self.nodes[p.id].children.append(nid)
            self.registry[nid] = {"goal": goal, "depth": d, "zone": z}
        self._log({"event": "merge" if len(parents) > 1 else "spawn", "id": nid,
                   "parents": [p.id for p in parents], "goal": goal, "goal_stack": gstack,
                   "depth": d, "zone": z, "why": why})
        return node

    def mark(self, node, action, detail=""):
        """A node marks its way - a step on its path, with rationale (the trail for the discriminator)."""
        self._log({"event": "step", "id": node.id, "action": action, "detail": str(detail)[:300]})

    def done(self, node, result, model=None):
        with self.lock:
            node.status = "done"; node.result = result; node.model = model
            self.registry.pop(node.id, None)
        self._log({"event": "done", "id": node.id, "model": model, "result": str(result)[:500]})

    def lookup(self, node):
        """VERTICAL: any node, at any depth, can see the bigger picture - its goal-stack root -> me."""
        return " > ".join(node.goal_stack)

    def snapshot(self):
        """HORIZONTAL substrate: what is active RIGHT NOW - exactly what a discriminator would read."""
        with self.lock:
            return dict(self.registry)

    def tree_str(self, nid=None, ind=0):
        nid = nid or self.root.id; n = self.nodes[nid]
        tag = f"[{n.zone}]" + (f" via {n.model}" if n.model else "")
        s = "  " * ind + f"{n.id} {tag}  {n.goal[:74]}\n"
        for c in n.children:
            s += self.tree_str(c, ind + 1)
        return s
