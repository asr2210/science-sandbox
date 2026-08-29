"""
Experiment 017 — high-GC heavy library.

Tests whether the eval's GC distribution is high-GC weighted. If so,
oversampling high-GC bins should beat uniform GC stratification.

Design (50K, all human natural):
  30K windows from GC > 55% (oversample high-GC)
  10K windows from GC 45-55%
  10K windows from GC < 45%
"""

import os
import sys
import numpy as np
from pyfaidx import Fasta

L = 200
SEED = 0
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
HG38 = os.path.join(DATA, "hg38.fa")
HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
ALPHABET = set("ACGT")

BINS = [(0.0, 0.45), (0.45, 0.55), (0.55, 1.0)]
TARGETS = [10000, 10000, 30000]


def gc(s):
    return (s.count("C") + s.count("G")) / len(s)


def bin_for(g):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= g < hi:
            return i
    return len(BINS) - 1


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)
    lens = {c: len(fa[c]) for c in HG38_CHROMS if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()

    bins = [[] for _ in BINS]
    n = 0
    while sum(len(b) for b in bins) < sum(TARGETS):
        n += 1
        c = cs[rng.choice(len(cs), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        b = bin_for(gc(s))
        if len(bins[b]) < TARGETS[b]:
            bins[b].append(s)
        if n % 500_000 == 0:
            print(f"  tried {n}, sizes {[len(b) for b in bins]}",
                  file=sys.stderr)

    print(f"  final tried {n}, sizes {[len(b) for b in bins]}",
          file=sys.stderr)
    seqs = [s for b in bins for s in b]
    assert len(seqs) == 50_000

    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
