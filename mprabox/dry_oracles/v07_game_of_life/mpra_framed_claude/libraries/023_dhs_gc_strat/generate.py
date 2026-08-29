"""
Experiment 023 — GC-stratified DHS only (no natural).

Tests whether pure regulatory + GC control reaches the ceiling, or
whether natural backbone is required for breadth.

Design (50K, all DHS):
  10K DHS summits per GC bin, anchored ±30-170bp from summit.
"""

import gzip
import os
import sys
import numpy as np
from pyfaidx import Fasta

L = 200
SEED = 0
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
HG38 = os.path.join(DATA, "hg38.fa")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")
HG38_CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
ALPHABET = set("ACGT")
BINS = [(0.0, 0.35), (0.35, 0.45), (0.45, 0.55), (0.55, 0.65), (0.65, 1.0)]
PER_BIN = 10_000


def gc(s):
    return (s.count("C") + s.count("G")) / len(s)


def bin_for(g):
    for i, (lo, hi) in enumerate(BINS):
        if lo <= g < hi:
            return i
    return len(BINS) - 1


def load_dhs():
    out = []
    with gzip.open(DHS, "rt") as f:
        header = next(f).rstrip("\n").split("\t")
        ci = header.index("seqname")
        si = header.index("summit")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[ci] in HG38_CHROMS:
                out.append((parts[ci], int(parts[si])))
    return out


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)

    print("Loading DHS...", file=sys.stderr)
    dhs = load_dhs()
    print(f"  {len(dhs)} DHS summits", file=sys.stderr)
    rng.shuffle(dhs)

    bins = [[] for _ in BINS]
    needed = PER_BIN * len(BINS)
    for c, anchor in dhs:
        if sum(len(b) for b in bins) >= needed:
            break
        offset = int(rng.integers(30, 170))
        start = anchor - offset
        clen = len(fa[c])
        if start < 0 or start + L > clen:
            continue
        seq = str(fa[c][start:start + L]).upper()
        if len(seq) != L or not set(seq).issubset(ALPHABET):
            continue
        b = bin_for(gc(seq))
        if len(bins[b]) < PER_BIN:
            bins[b].append(seq)

    print(f"  sizes: {[len(b) for b in bins]}", file=sys.stderr)
    # Top up any deficit with natural GC-strat
    if sum(len(b) for b in bins) < needed:
        from pyfaidx import Fasta as _F
        lens = {c: len(fa[c]) for c in HG38_CHROMS if c in fa}
        cs = list(lens.keys())
        weights = np.array([lens[c] for c in cs], dtype=np.float64)
        weights /= weights.sum()
        while sum(len(b) for b in bins) < needed:
            c = cs[rng.choice(len(cs), p=weights)]
            start = int(rng.integers(0, lens[c] - L))
            s = str(fa[c][start:start + L]).upper()
            if len(s) != L or not set(s).issubset(ALPHABET):
                continue
            b = bin_for(gc(s))
            if len(bins[b]) < PER_BIN:
                bins[b].append(s)

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
