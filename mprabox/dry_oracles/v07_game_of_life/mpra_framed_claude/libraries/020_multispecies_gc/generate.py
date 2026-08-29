"""
Experiment 020 — GC-stratified human + GC-stratified mouse.

mouse-only (006) matched human-only (001) at 0.388 mean_r — species
didn't matter. GC-strat (014) lifted to 0.394. Open question: does
multi-genome + composition control beat single-genome composition
control?

Design (50K):
  25K hg38 natural, GC-strat (5K per bin)
  25K mm39 natural, GC-strat (5K per bin)
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
MM39 = os.path.join(DATA, "mm39.fa")

HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MM39_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
ALPHABET = set("ACGT")
BINS = [(0.0, 0.35), (0.35, 0.45), (0.45, 0.55), (0.55, 0.65), (0.65, 1.0)]


def gc(s):
    return (s.count("C") + s.count("G")) / len(s)


def bin_for(g):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= g < hi:
            return i
    return len(BINS) - 1


def sample_gc(fa, chroms, per_bin, rng):
    lens = {c: len(fa[c]) for c in chroms if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()
    bins = [[] for _ in BINS]
    n = 0
    while sum(len(b) for b in bins) < sum(per_bin):
        n += 1
        c = cs[rng.choice(len(cs), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        b = bin_for(gc(s))
        if len(bins[b]) < per_bin[b]:
            bins[b].append(s)
    return [s for b in bins for s in b], n


def main():
    rng = np.random.default_rng(SEED)
    hg38 = Fasta(HG38, sequence_always_upper=True)
    mm39 = Fasta(MM39, sequence_always_upper=True)

    print("Human GC-strat 25K (5K/bin)...", file=sys.stderr)
    h, hn = sample_gc(hg38, HG38_CHROMS, [5000] * 5, rng)
    print(f"  human tries: {hn}", file=sys.stderr)
    print("Mouse GC-strat 25K (5K/bin)...", file=sys.stderr)
    m, mn = sample_gc(mm39, MM39_CHROMS, [5000] * 5, rng)
    print(f"  mouse tries: {mn}", file=sys.stderr)

    seqs = h + m
    assert len(seqs) == 50_000

    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
