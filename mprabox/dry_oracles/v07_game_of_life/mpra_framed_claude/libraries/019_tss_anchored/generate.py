"""
Experiment 019 — TSS-anchored library (PLS only).

cCRE class PLS = Promoter-Like Signature = TSS-proximal elements.
Test whether eval is enriched for promoter sequences.

Design (50K):
  50K windows centered around PLS elements, with off-center jitter
  (30-170 bp from element center).
"""

import bisect
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
CCRE = os.path.join(DATA, "ccre.bed.gz")

HG38_CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
ALPHABET = set("ACGT")


def load_pls():
    rows = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[9] == "PLS" and parts[0] in HG38_CHROMS:
                rows.append((parts[0], (int(parts[1]) + int(parts[2])) // 2))
    return rows


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)

    print("Loading PLS elements...", file=sys.stderr)
    pls = load_pls()
    print(f"  {len(pls)} PLS elements", file=sys.stderr)

    # Sample 50K windows with replacement+jitter to fill (PLS is ~40K elements)
    anchors = [(c, a) for c, a in pls if c in fa]
    rng.shuffle(anchors)
    out = []
    idx = 0
    n_pass = 0
    while len(out) < 50_000:
        if idx >= len(anchors):
            rng.shuffle(anchors)
            idx = 0
            n_pass += 1
        c, anchor = anchors[idx]
        idx += 1
        offset = int(rng.integers(-85, 86))  # ±85bp jitter
        start = anchor + offset - L // 2
        clen = len(fa[c])
        if start < 0 or start + L > clen:
            continue
        seq = str(fa[c][start:start + L]).upper()
        if len(seq) != L or not set(seq).issubset(ALPHABET):
            continue
        out.append(seq)
    print(f"Generated {len(out)} after {n_pass+1} pass(es)", file=sys.stderr)
    assert len(out) == 50_000

    perm = rng.permutation(len(out))
    out = [out[i] for i in perm]
    with open(OUT, "w") as f:
        for s in out:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
