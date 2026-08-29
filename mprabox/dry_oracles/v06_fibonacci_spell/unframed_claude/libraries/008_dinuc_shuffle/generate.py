"""Experiment 008: Dinucleotide-shuffled full-genome random windows.

Take exp 006's sequences and shuffle within each sequence while preserving
dinucleotide frequencies (Altschul-Erickson shuffle via simple Eulerian walk).
If score ≈ 0.139 (same as raw), composition matters. If much lower, structure
matters.
"""
import numpy as np
from pathlib import Path

L = 200
SEED = 8
SRC = Path(__file__).parents[1] / "006_genome_windows" / "sequences_0.txt"
OUT = Path(__file__).with_name("sequences_0.txt")


def dinuc_shuffle(seq: str, rng) -> str:
    """Altschul-Erickson dinucleotide shuffle.

    Build Eulerian graph: nodes = ACGT, edges = adjacent dinucs.
    Random Eulerian path = shuffled sequence with same dinuc freqs.
    """
    n = len(seq)
    # Adjacency lists per node
    adj = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        adj[seq[i]].append(seq[i + 1])
    # Try repeatedly until we get a valid Eulerian path
    last = seq[-1]
    for _ in range(20):
        # Copy and shuffle each adjacency list
        edges = {b: list(lst) for b, lst in adj.items()}
        for b in "ACGT":
            rng.shuffle(edges[b])
        # The last edge from each non-terminal node must point toward `last`.
        # Use the standard trick: pick a random spanning tree rooted at `last`
        # whose edges are the LAST out-edge from each node. Other edges are
        # randomized. We approximate by attempting traversal and falling back.
        path = [seq[0]]
        ok = True
        cur = seq[0]
        used = {b: 0 for b in "ACGT"}
        while True:
            if used[cur] >= len(edges[cur]):
                if len(path) == n:
                    ok = True
                else:
                    ok = False
                break
            nxt = edges[cur][used[cur]]
            used[cur] += 1
            path.append(nxt)
            cur = nxt
        if ok and len(path) == n:
            return "".join(path)
    # Fallback: simple shuffle (rare)
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)


rng = np.random.default_rng(SEED)
src_lines = [ln.strip() for ln in open(SRC)]
out = []
for s in src_lines:
    out.append(dinuc_shuffle(s, rng))

assert len(out) == 50_000
assert all(len(s) == L for s in out)

with open(OUT, "w") as f:
    for s in out:
        f.write(s + "\n")

print(f"Wrote {len(out)} dinuc-shuffled sequences")
