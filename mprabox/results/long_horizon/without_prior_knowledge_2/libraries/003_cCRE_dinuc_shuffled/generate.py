"""Experiment 003: dinucleotide-shuffled cCREs.

Take the same 50K cCRE sample as 002 (per seed), then dinucleotide-shuffle
each sequence with Hierholzer's algorithm. This preserves the dinucleotide
multiset (all dinucleotide frequencies exact) while destroying motifs.

Tests whether the cCRE gain over random comes from:
  (a) real TF motif content (destroyed here) — predict 003 ≈ random
  (b) compositional/k-mer biases (preserved here) — predict 003 ≈ cCREs
  (c) both — predict 003 between them
"""
import os
import sys
import numpy as np
import twobitreader
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BED = os.path.join(ROOT, "data", "cCRE", "ENCFF420VPZ.bed")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_cCREs():
    rows = []
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end = p[0], int(p[1]), int(p[2])
            if chrom not in MAIN_CHROMS:
                continue
            mid = (start + end) // 2
            rows.append((chrom, mid))
    return rows


def extract(tb, chrom, mid, rng):
    chrom_len = len(tb[chrom])
    start = mid - HALF
    end = mid + HALF
    if start < 0 or end > chrom_len:
        return None
    seq = tb[chrom][start:end].upper()
    if len(seq) != SEQ_LEN:
        return None
    out = []
    for c in seq:
        if c in "ACGT":
            out.append(c)
        else:
            out.append(ALPHABET[rng.integers(0, 4)])
    return "".join(out)


def dinuc_shuffle(seq, rng):
    """Hierholzer's algorithm Eulerian walk -> exact dinucleotide preservation."""
    n = len(seq)
    adj = defaultdict(list)
    for i in range(n - 1):
        adj[seq[i]].append(seq[i + 1])
    for u in adj:
        rng.shuffle(adj[u])
    stack = [seq[0]]
    path = []
    while stack:
        u = stack[-1]
        if adj[u]:
            stack.append(adj[u].pop())
        else:
            path.append(stack.pop())
    path.reverse()
    return "".join(path)


def generate(seed, cCREs, tb):
    rng = np.random.default_rng(seed)
    target = int(N_SEQS * 1.05)
    idx = rng.choice(len(cCREs), size=target, replace=False)
    out = []
    for i in idx:
        chrom, mid = cCREs[i]
        seq = extract(tb, chrom, mid, rng)
        if seq is None:
            continue
        # Use a per-sequence rng seeded by (seed, i) for determinism
        sub_rng = np.random.default_rng(int(seed * 10**9 + i))
        out.append(dinuc_shuffle(seq, sub_rng))
        if len(out) == N_SEQS:
            break
    if len(out) < N_SEQS:
        raise RuntimeError(f"only got {len(out)} / {N_SEQS}")
    return out


def main():
    print("loading cCREs...")
    cCREs = load_cCREs()
    print(f"  {len(cCREs):,} cCREs")
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, cCREs, tb)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
