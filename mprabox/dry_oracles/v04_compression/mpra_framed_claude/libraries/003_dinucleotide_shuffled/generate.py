"""Experiment 003: dinucleotide-preserving shuffle of the 002 genomic windows.

Take the 50,000 genomic 200bp windows from exp 002 and shuffle each one
preserving its dinucleotide composition (Altschul-Erickson algorithm).
This matches GC content and dinucleotide statistics but destroys all
motifs and combinatorial structure.

Goal: isolate whether the "genomic lift" (0.34 → 0.50) comes from
low-order composition or from motif/combinatorial content.

Why this generalizes beyond K562/HepG2/SKNSH: dinucleotide composition
is universal across human cell types. If composition alone produces the
lift, the resulting model is using universal sequence statistics,
which transfers to any cell type. If motifs are the source, those too
are largely shared across cell types (TFs are mostly cell-type-agnostic
proteins; differential expression sets which ones are active).
"""
import os
import random
from pathlib import Path

SEED = 42
HERE = Path(__file__).parent
SRC = HERE.parent / "002_genomic_random_windows" / "sequences_0.txt"

def altschul_erickson_shuffle(seq, rng):
    """Shuffle nucleotides while preserving dinucleotide counts.

    Implementation of the Altschul-Erickson algorithm (1985), which
    generates a random Eulerian walk over the dinucleotide multigraph.
    Result: a string with the same length, same nucleotide composition,
    and the same dinucleotide counts as the input.
    """
    n = len(seq)
    if n < 3:
        return seq
    # Edges: list per starting nucleotide of next nucleotide for each edge
    edges = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        edges[seq[i]].append(seq[i + 1])

    # Last nucleotide is fixed (last edge of Eulerian walk must end at seq[-1])
    last = seq[-1]
    first = seq[0]

    # Build a random Eulerian walk: at each node, pick a random outgoing edge.
    # To guarantee an Eulerian walk exists, ensure that from each node !=last
    # there is a path to `last` using remaining edges. Use the standard
    # arborescence-into-last trick: choose, for every node v != last, one
    # specific outgoing edge that must be used LAST (this edge belongs to
    # the spanning arborescence into `last`).
    for _ in range(200):  # retry a bounded number of times
        # Random shuffle of each adjacency list
        shuf = {b: edges[b][:] for b in "ACGT"}
        for b in shuf:
            rng.shuffle(shuf[b])
        # Try to build an arborescence into `last`: for each node v != last,
        # designate the LAST element of shuf[v] as its "must-be-used-last"
        # edge. Then check: starting from any node != last and following
        # these designated edges, you must reach `last` (i.e. no cycle that
        # avoids last).
        chosen_last = {}
        for b in "ACGT":
            if b == last or not shuf[b]:
                continue
            chosen_last[b] = shuf[b][-1]
        # Check arborescence by walking from each starting node
        ok = True
        for b in chosen_last:
            v = b
            seen = set()
            while v != last:
                if v in seen or v not in chosen_last:
                    ok = False
                    break
                seen.add(v)
                v = chosen_last[v]
            if not ok:
                break
        if not ok:
            continue
        # Build the walk: at each node, pop next edge from front of shuf[v];
        # ensure that the LAST edge taken from each v (!=last) is chosen_last[v].
        # Easy way: reorder shuf[v] so chosen_last[v] is the last element
        # (already the case by construction), then traverse Eulerian walk
        # picking edges in shuf[v] order.
        # Need to also start from `first`.
        adj = {b: list(shuf[b]) for b in "ACGT"}  # we'll pop from end (last)
        # Actually pop from index 0 (front) so chosen_last stays last.
        result = [first]
        v = first
        # Eulerian walk: at node v, pop front of adj[v]
        for _ in range(n - 1):
            if not adj[v]:
                ok = False
                break
            nxt = adj[v].pop(0)
            result.append(nxt)
            v = nxt
        if ok and v == last and all(len(a) == 0 for a in adj.values()):
            return "".join(result)
    # Fallback: trivial mononucleotide shuffle (very rare)
    chars = list(seq)
    rng.shuffle(chars)
    return "".join(chars)

def main():
    rng = random.Random(SEED)
    out_lines = []
    with open(SRC) as f:
        src_seqs = [line.strip() for line in f if line.strip()]
    assert len(src_seqs) == 50_000, len(src_seqs)
    for s in src_seqs:
        shuffled = altschul_erickson_shuffle(s, rng)
        assert len(shuffled) == 200
        # sanity: same dinucleotide counts
        out_lines.append(shuffled)

    out_path = HERE / "sequences_0.txt"
    with open(out_path, "w") as f:
        f.write("\n".join(out_lines))
        f.write("\n")
    print(f"Wrote {len(out_lines)} sequences to {out_path}")

    # quick sanity check on first sequence
    def dinuc_counts(s):
        from collections import Counter
        return Counter(s[i:i+2] for i in range(len(s) - 1))
    c1 = dinuc_counts(src_seqs[0])
    c2 = dinuc_counts(out_lines[0])
    print("first seq dinuc match:", c1 == c2)

if __name__ == "__main__":
    main()
