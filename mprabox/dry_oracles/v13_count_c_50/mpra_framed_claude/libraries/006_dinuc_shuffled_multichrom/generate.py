"""Experiment 006: dinucleotide-shuffled multi-chromosome genomic.

Take the experiment 004 sequences (multi-chrom random natural) and
dinucleotide-shuffle each one. This preserves the per-sequence
dinucleotide composition while destroying all motif structure.

Diagnostic purpose: if scores drop to near random baseline (~0.13 on
eval_01), then motif grammar is doing the work. If scores stay near
multi-chrom (~0.55), then dinucleotide composition alone explains the
predictive performance. The result calibrates how much of the gain
attributed to "natural sequences" comes from motifs vs k-mer biases.
"""
from pathlib import Path
import numpy as np

SEED = 0
SRC = Path(__file__).resolve().parents[1] / "004_multi_chrom_genomic" / "sequences_0.txt"
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)


def dinuc_shuffle(seq: str, rng) -> str:
    """Altschul-Erikson dinucleotide shuffle.

    Implements the Eulerian-path algorithm: build a graph where each
    nucleotide is a node and each consecutive pair is an edge. A random
    Eulerian path on this graph gives a sequence with identical dinucleotide
    counts to the input.
    """
    n = len(seq)
    if n < 2:
        return seq
    # Edges grouped by source nucleotide
    edges = {b: [] for b in "ACGT"}
    for i in range(n - 1):
        edges[seq[i]].append(seq[i + 1])

    last = seq[-1]
    # Need a spanning arborescence rooted at `last`: pick a last-outgoing
    # edge per non-`last` letter that is the LAST one used at that letter.
    # We do this by reversed sampling: pick one edge per non-last letter
    # to keep "for the end" of that letter's traversal, ensuring graph
    # connectivity to `last`. Retry until valid spanning tree.
    letters = list("ACGT")
    for _attempt in range(50):
        # for each non-last letter, choose one of its edges as the "last"
        # edge: that edge must lead to a letter whose chosen-last edges
        # eventually reach `last`.
        last_edges = {}
        ok = True
        for b in letters:
            if b == last:
                continue
            if not edges[b]:
                # b doesn't appear before last char: skip
                continue
            i = rng.integers(0, len(edges[b]))
            last_edges[b] = edges[b][i]
        # Check spanning: following last_edges from each non-last letter
        # must reach `last`.
        for start in last_edges:
            cur = start
            seen = {cur}
            while cur != last:
                if cur not in last_edges:
                    ok = False
                    break
                cur = last_edges[cur]
                if cur in seen:
                    ok = False
                    break
                seen.add(cur)
            if not ok:
                break
        if ok:
            break
    if not ok:
        # Fallback: just shuffle the sequence (preserves 1-mer composition)
        arr = list(seq)
        rng.shuffle(arr)
        return "".join(arr)

    # Build a working copy of edges, moving last_edges to the end of their lists
    work = {b: list(es) for b, es in edges.items()}
    for b, e in last_edges.items():
        work[b].remove(e)
        work[b].append(e)
    # Shuffle each list except last position
    for b in letters:
        if not work[b]:
            continue
        if b in last_edges:
            head = work[b][:-1]
            rng.shuffle(head)
            work[b] = head + [work[b][-1]]
        else:
            rng.shuffle(work[b])

    # Eulerian traversal from seq[0]
    out = [seq[0]]
    cur = seq[0]
    idx = {b: 0 for b in letters}
    for _ in range(n - 1):
        nxt = work[cur][idx[cur]]
        idx[cur] += 1
        out.append(nxt)
        cur = nxt
    return "".join(out)


def main():
    with SRC.open() as f:
        src_seqs = [l.rstrip("\n") for l in f]
    print(f"Loaded {len(src_seqs)} source sequences")
    shuffled = []
    for s in src_seqs:
        shuffled.append(dinuc_shuffle(s, rng))
    with OUT.open("w") as f:
        for s in shuffled:
            f.write(s)
            f.write("\n")
    print(f"Wrote {len(shuffled)} dinucleotide-shuffled sequences.")

    # Sanity check: dinucleotide counts should match for each sequence
    from collections import Counter
    def dincount(s):
        return Counter(s[i:i+2] for i in range(len(s)-1))
    matches = 0
    for a, b in zip(src_seqs[:200], shuffled[:200]):
        if dincount(a) == dincount(b):
            matches += 1
    print(f"Dinucleotide preservation: {matches}/200 (target: 200/200)")


if __name__ == "__main__":
    main()
