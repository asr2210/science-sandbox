"""
Experiment 018 — CpG dinucleotide-stratified natural.

CpG dinucleotides are special: heavily methylated genome-wide,
depleted compared to GC composition would predict, but elevated
at CpG islands (active regulatory loci). Stratifying by CpG count
controls for methylation context independently of GC.

Design (50K, all human natural):
  10K per CpG-count bin: 0-1, 2-5, 6-12, 13-25, 26+
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

# CpG-count bins (calibrated from genome distribution)
BINS = [(0, 2), (2, 6), (6, 13), (13, 26), (26, 1000)]
PER_BIN = 10_000


def cpg_count(s):
    return s.count("CG")


def bin_for(c):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= c < hi:
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
    needed = sum(PER_BIN for _ in BINS)
    while sum(len(b) for b in bins) < needed:
        n += 1
        c = cs[rng.choice(len(cs), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        b = bin_for(cpg_count(s))
        if len(bins[b]) < PER_BIN:
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
