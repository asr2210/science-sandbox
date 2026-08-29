"""
Experiment 030 — finer GC stratification (10 bins) of natural human.

Final test: does higher-resolution GC balancing exceed the 5-bin ceiling?

All prior GC-strat experiments used 5 bins (0-35, 35-45, 45-55, 55-65, 65-100).
This uses 10 bins of equal width [25-35, 35-45, ..., 75-85] plus catch-all
tails. If 5-bin GC strat (014, 0.3939) wasn't fine enough, 10-bin should lift.
If matches, GC strat at 5-bin resolution was already saturated.

Design (50K):
  5000 natural windows per 10 GC bins, edges:
    [0, .25, .30, .35, .40, .45, .50, .55, .60, .65, 1.0]
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

BIN_EDGES = [0.0, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 1.0]
PER_BIN = 5000
N_BINS = len(BIN_EDGES) - 1


def gc(s):
    return (s.count("C") + s.count("G")) / len(s)


def bin_for(g):
    for i in range(N_BINS):
        if BIN_EDGES[i] <= g < BIN_EDGES[i + 1]:
            return i
    return N_BINS - 1


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)
    lens = {c: len(fa[c]) for c in HG38_CHROMS if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()

    bins = [[] for _ in range(N_BINS)]
    needed = PER_BIN * N_BINS
    n = 0
    while sum(len(b) for b in bins) < needed:
        n += 1
        c = cs[rng.choice(len(cs), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        b = bin_for(gc(s))
        if len(bins[b]) < PER_BIN:
            bins[b].append(s)
        if n % 200_000 == 0:
            print(f"  tried {n}, sizes: {[len(b) for b in bins]}",
                  file=sys.stderr)

    print(f"  final tried: {n}, sizes: {[len(b) for b in bins]}",
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
