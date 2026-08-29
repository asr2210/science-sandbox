"""
Experiment 009 — maximum diversity multi-source mix.

Combines every reliable natural source I have, balanced.

Design (50K):
  10K human natural random
  10K mouse natural random
  10K human cCRE high-conf off-center
  10K human DHS summits
   5K FANTOM5 enhancers (CAGE-defined)
   5K Low-DNase cCRE (passive anchors, broaden composition coverage)
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
MM39 = os.path.join(DATA, "mm39.fa")
CCRE = os.path.join(DATA, "ccre.bed.gz")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")
FANTOM5 = os.path.join(DATA, "fantom5_enhancers.bed.gz")

HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MM39_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HIGH_CONF_CCRE = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}
LOW_DNASE_CCRE = {"Low-DNase"}
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


def load_fantom5():
    out = []
    with gzip.open(FANTOM5, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            try:
                start, end = int(parts[1]), int(parts[2])
                out.append((parts[0], (start + end) // 2))
            except ValueError:
                continue
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
    hg38 = Fasta(HG38, sequence_always_upper=True)
    mm39 = Fasta(MM39, sequence_always_upper=True)

    print("Human natural 10K...", file=sys.stderr)
    h_nat = sample_natural(hg38, HG38_CHROMS, 10_000, rng)
    print("Mouse natural 10K...", file=sys.stderr)
    m_nat = sample_natural(mm39, MM39_CHROMS, 10_000, rng)

    print("Loading high-conf cCRE...", file=sys.stderr)
    ccre_hi = load_ccre_class(HIGH_CONF_CCRE)
    print(f"  {len(ccre_hi)}", file=sys.stderr)
    print("Sampling 10K cCRE off-center...", file=sys.stderr)
    ccre_seqs = sample_anchored(hg38, ccre_hi, 10_000, rng)

    print("Loading DHS summits...", file=sys.stderr)
    dhs = load_dhs_summits()
    print(f"  {len(dhs)}", file=sys.stderr)
    print("Sampling 10K DHS...", file=sys.stderr)
    dhs_seqs = sample_anchored(hg38, dhs, 10_000, rng)

    print("Loading FANTOM5 enhancers...", file=sys.stderr)
    fantom = load_fantom5()
    print(f"  {len(fantom)}", file=sys.stderr)
    print("Sampling 5K FANTOM5...", file=sys.stderr)
    fantom_seqs = sample_anchored(hg38, fantom, 5_000, rng)

    print("Loading Low-DNase cCRE...", file=sys.stderr)
    ccre_lo = load_ccre_class(LOW_DNASE_CCRE)
    print(f"  {len(ccre_lo)}", file=sys.stderr)
    print("Sampling 5K Low-DNase cCRE...", file=sys.stderr)
    low_seqs = sample_anchored(hg38, ccre_lo, 5_000, rng)

    seqs = h_nat + m_nat + ccre_seqs + dhs_seqs + fantom_seqs + low_seqs
    print(f"Total: {len(seqs)}", file=sys.stderr)
    assert len(seqs) == 50_000

    perm = rng.permutation(len(seqs))
    seqs = [seqs[i] for i in perm]
    with open(OUT, "w") as f:
        for s in seqs:
            f.write(s + "\n")
    print(f"Wrote {OUT}", file=sys.stderr)


if __name__ == "__main__":
    main()
