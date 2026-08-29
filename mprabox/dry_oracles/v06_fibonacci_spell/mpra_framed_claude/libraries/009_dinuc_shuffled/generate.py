"""
Experiment 009: dinucleotide-shuffled chr22 200bp windows.

Diagnostic experiment to decompose what makes random-genomic libraries
work (003 → 0.134 vs random ACGT → 0.116). A dinucleotide shuffle
preserves the mono- and di-nucleotide composition of each window but
destroys higher-order structure (motifs, repeats, k-mer patterns).

Possible outcomes:
  (a) dinuc-shuffled ≈ random ACGT (0.116) → motif content drives all
      genomic advantage; composition alone is worth nothing.
  (b) dinuc-shuffled ≈ chr22 random (0.134) → composition (GC, CpG
      depletion, etc.) drives all genomic advantage; motifs are
      negligible at this scale.
  (c) something in between (e.g., 0.124) → both composition and
      motif content matter, roughly equally.

The answer tells me what to invest in for future libraries.

Design:
  - Random 50k chr22 windows (same as 003).
  - Each window: Altschul-Erickson dinucleotide shuffle (preserves
    dinucleotide counts exactly).
  - Random orientation.
  - Seed=42.
"""

import os
import random
from collections import defaultdict

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42

ALPHABET = set("ACGT")
COMPL = str.maketrans("ACGTNacgtn", "TGCANtgcan")
def revcomp(s): return s.translate(COMPL)[::-1]

def load_fasta(path):
    parts = []
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                parts.append(line.strip().upper())
    return "".join(parts)

def euler_dinuc_shuffle(seq, rng):
    """
    Altschul-Erickson-style dinucleotide shuffle.
    Builds an Eulerian random walk on the dinucleotide graph.
    Preserves: first char, last char, dinucleotide counts.

    Reference: Altschul & Erickson 1985.
    """
    n = len(seq)
    if n < 2:
        return seq
    first = seq[0]
    last = seq[-1]

    # Build edge list: for each position i, edge seq[i] -> seq[i+1]
    # We'll randomly permute edges while respecting:
    # - In-degree / out-degree per vertex is preserved
    # - Walk from `first` must reach `last`

    # Build adjacency: adj[v] = list of out-neighbors (multiset)
    out = defaultdict(list)
    for i in range(n - 1):
        out[seq[i]].append(seq[i + 1])

    for _ in range(50):  # try multiple times
        # 1. From each vertex, pick a "last edge" toward last (for connectivity).
        # The standard algorithm: ensure last-out edge of each vertex (except `last`)
        # leads to a path to `last`.
        # Approach: find a random spanning in-arborescence rooted at `last`.
        verts = set(out) | {seq[-1]}
        # Build reverse graph
        rev = defaultdict(list)
        for v, neigh in out.items():
            for w in neigh:
                rev[w].append(v)

        # Random in-arborescence rooted at last via random reverse BFS
        last_edge = {}
        visited = {last}
        order = [last]
        idx = 0
        while idx < len(order):
            u = order[idx]
            idx += 1
            preds = list(rev.get(u, []))
            rng.shuffle(preds)
            for p in preds:
                if p not in visited:
                    visited.add(p)
                    last_edge[p] = u
                    order.append(p)

        # Check connectivity from `first`
        if first not in visited and first != last:
            continue

        # Now shuffle edges except the "last edge" for each non-last vertex
        # The walk is reconstructed using the edges
        edges = {v: list(neigh) for v, neigh in out.items()}
        for v in edges:
            if v != last and v in last_edge:
                # Remove one instance of last_edge[v] from edges[v]
                edges[v].remove(last_edge[v])
                rng.shuffle(edges[v])
                edges[v].append(last_edge[v])  # put it last
            else:
                rng.shuffle(edges[v])

        # Walk
        result = [first]
        cur = first
        for _ in range(n - 1):
            if cur not in edges or not edges[cur]:
                break
            nxt = edges[cur].pop(0)
            result.append(nxt)
            cur = nxt
        if len(result) == n:
            return "".join(result)

    # Fallback: simple mononucleotide shuffle preserving composition
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)

def main():
    rng = random.Random(SEED)
    chr22 = load_fasta("data/chr22.fa")
    L = len(chr22)
    starts = []
    i = 0
    while i < L:
        if chr22[i] in ALPHABET:
            j = i
            while j < L and chr22[j] in ALPHABET:
                j += 1
            if j - i >= SEQ_LEN:
                starts.extend(range(i, j - SEQ_LEN + 1))
            i = j
        else:
            i += 1
    sampled = rng.sample(starts, N_SEQS)
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        for k, s in enumerate(sampled):
            w = chr22[s:s + SEQ_LEN]
            shuffled = euler_dinuc_shuffle(w, rng)
            if rng.random() < 0.5:
                shuffled = revcomp(shuffled)
            f.write(shuffled + "\n")
    print(f"Wrote {N_SEQS} dinucleotide-shuffled windows to {out}")

if __name__ == "__main__":
    main()
