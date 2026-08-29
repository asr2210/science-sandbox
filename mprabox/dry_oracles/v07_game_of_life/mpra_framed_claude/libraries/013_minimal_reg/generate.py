"""
Experiment 013 — minimal regulatory dose.

Tests dose-response of regulatory enrichment.

Design (50K):
  45K random hg38 natural
   2.5K cCRE high-conf off-center
   2.5K DHS summits
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
CCRE = os.path.join(DATA, "ccre.bed.gz")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")

HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
HIGH_CONF_CCRE = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}
ALPHABET = set("ACGT")


def sample_natural(fa, chroms, n, rng):
    lens = {c: len(fa[c]) for c in chroms if c in fa}
    cs = list(lens.keys())
    weights = np.array([lens[c] for c in cs], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = cs[rng.choice(len(cs), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        out.append(s)
    return out


def load_ccre_class(classes):
    rows = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[9] in classes:
                rows.append((parts[0], (int(parts[1]) + int(parts[2])) // 2))
    return rows


def load_dhs_summits():
    out = []
    with gzip.open(DHS, "rt") as f:
        header = next(f).rstrip("\n").split("\t")
        ci = header.index("seqname")
        si = header.index("summit")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            out.append((parts[ci], int(parts[si])))
    return out


def sample_anchored(fa, anchors, n, rng, min_off=30, max_off=170):
    anchors = [(c, a) for c, a in anchors if c in fa]
    idxs = rng.permutation(len(anchors))
    out = []
    for i in idxs:
        c, anchor = anchors[i]
        offset = int(rng.integers(min_off, max_off))
        start = anchor - offset
        clen = len(fa[c])
        if start < 0 or start + L > clen:
            continue
        seq = str(fa[c][start:start + L]).upper()
        if len(seq) != L or not set(seq).issubset(ALPHABET):
            continue
        out.append(seq)
        if len(out) >= n:
            break
    return out


def main():
    rng = np.random.default_rng(SEED)
    fa = Fasta(HG38, sequence_always_upper=True)

    print("Natural 45K...", file=sys.stderr)
    nat = sample_natural(fa, HG38_CHROMS, 45_000, rng)

    print("Loading cCRE...", file=sys.stderr)
    ccre = load_ccre_class(HIGH_CONF_CCRE)
    print("Sampling 2.5K cCRE...", file=sys.stderr)
    ccre_seqs = sample_anchored(fa, ccre, 2_500, rng)

    print("Loading DHS...", file=sys.stderr)
    dhs = load_dhs_summits()
    print("Sampling 2.5K DHS...", file=sys.stderr)
    dhs_seqs = sample_anchored(fa, dhs, 2_500, rng)

    seqs = nat + ccre_seqs + dhs_seqs
    assert len(seqs) == 50_000

    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
