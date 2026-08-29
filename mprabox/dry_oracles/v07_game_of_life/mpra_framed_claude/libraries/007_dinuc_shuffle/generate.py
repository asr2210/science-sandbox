"""
Experiment 007 — dinucleotide-shuffled natural human.

Take 50K natural human windows (same as exp 001 strategy), then
Altschul-Erickson dinucleotide-shuffle each. Preserves exact
dinucleotide frequencies; destroys motifs, k-mers (k>=3), and
higher-order patterns.

Critical probe of what "naturalness" means.
"""

import os
import sys
import numpy as np
from collections import defaultdict
from pyfaidx import Fasta

L = 200
SEED = 0
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
HG38 = os.path.join(DATA, "hg38.fa")
HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
ALPHABET = set("ACGT")


def dinuc_shuffle(seq, rng):
    """Altschul-Erickson dinucleotide shuffle (Wilson's algorithm
    arborescence + edge-shuffled Eulerian walk)."""
    n = len(seq)
    if n < 4:
        return seq

    edges = defaultdict(lambda: defaultdict(int))
    for i in range(n - 1):
        edges[seq[i]][seq[i + 1]] += 1

    start = seq[0]
    end = seq[-1]
    verts = set(edges.keys()) | {end}

    for attempt in range(50):
        in_tree = {end: None}
        for v in verts:
            if v in in_tree:
                continue
            if not edges[v]:
                in_tree[v] = None
                continue
            path = [v]
            cur = v
            steps = 0
            while cur not in in_tree:
                cands = []
                for tgt, cnt in edges[cur].items():
                    cands.extend([tgt] * cnt)
                if not cands:
                    break
                nxt = cands[int(rng.integers(0, len(cands)))]
                if nxt in path:
                    idx = path.index(nxt)
                    path = path[:idx + 1]
                    cur = nxt
                else:
                    path.append(nxt)
                    cur = nxt
                steps += 1
                if steps > 1000:
                    break
            for i in range(len(path) - 1):
                in_tree[path[i]] = path[i + 1]

        ok = True
        for v in verts:
            if v == end or not edges[v]:
                continue
            seen = {v}
            cur = in_tree.get(v)
            while cur is not None and cur != end:
                if cur in seen:
                    ok = False
                    break
                seen.add(cur)
                cur = in_tree.get(cur)
            if not ok or cur != end:
                ok = False
                break
        if not ok:
            continue

        edge_lists = {}
        for v in verts:
            full_list = []
            for tgt, cnt in edges[v].items():
                full_list.extend([tgt] * cnt)
            rng.shuffle(full_list)
            if v != end and in_tree.get(v) is not None:
                tree_tgt = in_tree[v]
                idx = full_list.index(tree_tgt)
                full_list.pop(idx)
                full_list.append(tree_tgt)
            edge_lists[v] = full_list

        out = [start]
        cur = start
        success = True
        for _ in range(n - 1):
            elist = edge_lists.get(cur, [])
            if not elist:
                success = False
                break
            nxt = elist.pop(0)
            out.append(nxt)
            cur = nxt

        if success and len(out) == n:
            return "".join(out)

    return seq


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)
    chroms = [c for c in HG38_CHROMS if c in fa]
    lens = {c: len(fa[c]) for c in chroms}
    weights = np.array([lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()

    seqs = []
    attempts = 0
    while len(seqs) < 50_000:
        attempts += 1
        c = chroms[rng.choice(len(chroms), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        s_sh = dinuc_shuffle(s, rng)
        if len(s_sh) != L or not set(s_sh).issubset(ALPHABET):
            continue
        seqs.append(s_sh)
        if len(seqs) % 10000 == 0:
            print(f"  {len(seqs)}/50000", file=sys.stderr)

    print(f"Sampled+shuffled {len(seqs)} in {attempts} attempts",
          file=sys.stderr)

    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
