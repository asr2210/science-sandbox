"""
Experiment 014 — GC-stratified natural windows.

Design (50K):
  10K natural windows per GC bin:
    GC ≤ 35%
    35-45%
    45-55%
    55-65%
    GC > 65%

Tests whether the lift from regulatory enrichment is mediated by
GC composition (cCRE/DHS regions are typically higher GC) or by
sequence content per se.

If GC-stratified natural beats nat baseline (0.388), GC matching
is part of the mechanism.
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

# Per-bin target: 10K each
BINS = [(0.0, 0.35), (0.35, 0.45), (0.45, 0.55), (0.55, 0.65), (0.65, 1.0)]
PER_BIN = 10_000


def gc(s):
    return (s.count("C") + s.count("G")) / len(s)


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)
    lens = {c: len(fa[c]) for c in HG38_CHROMS if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()

    bins = [[] for _ in BINS]
    needed = sum(PER_BIN for _ in BINS)
    n_tried = 0
    while sum(len(b) for b in bins) < needed:
        c = cs[rng.choice(len(cs), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        n_tried += 1
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        g = gc(s)
        for i, (lo, hi) in enumerate(BINS):
            if lo <= g < hi and len(bins[i]) < PER_BIN:
                bins[i].append(s)
                break
        if n_tried % 100_000 == 0:
            print(f"  tried {n_tried}, sizes: {[len(b) for b in bins]}",
                  file=sys.stderr)

    print(f"  final tried: {n_tried}, sizes: {[len(b) for b in bins]}",
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
