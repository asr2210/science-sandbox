"""
Experiment 003 — neural-biased boost to test cell-type-specific
content hypothesis.

Design (50K):
  15K natural human genomic
  10K cCRE off-center (pan-tissue, high-conf)
  10K DHS pan-tissue summit windows
  10K DHS summits filtered to "Neural" component
   5K mouse natural

Hypothesis: SK-N-SH (neuroblastoma) is under-represented in pan-
tissue regulatory collections. Adding neural-tagged DHS content
should preferentially lift SK-N-SH (≥0.01) without harming K562/HepG2.
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
MM39 = os.path.join(DATA, "mm39.fa")
CCRE = os.path.join(DATA, "ccre.bed.gz")
DHS = os.path.join(DATA, "dhs_index.tsv.gz")

HG38_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MM39_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HIGH_CONF_CCRE = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}
ALPHABET = set("ACGT")


def sample_natural(fa, chroms, n, rng):
    lens = {c: len(fa[c]) for c in chroms if c in fa}
    chroms = [c for c in chroms if c in lens]
    weights = np.array([lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = chroms[rng.choice(len(chroms), p=weights)]
        start = int(rng.integers(0, lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if len(s) != L or not set(s).issubset(ALPHABET):
            continue
        out.append(s)
    return out


def load_ccre_high_conf():
    rows = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[9] in HIGH_CONF_CCRE:
                rows.append((parts[0], int(parts[1]), int(parts[2])))
    return rows


def load_dhs_summits(component=None):
    summits = []
    with gzip.open(DHS, "rt") as f:
        header = next(f).rstrip("\n").split("\t")
        comp_idx = header.index("component")
        summit_idx = header.index("summit")
        chr_idx = header.index("seqname")
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if component is not None and parts[comp_idx] != component:
                continue
            summits.append((parts[chr_idx], int(parts[summit_idx])))
    return summits


def window_from_anchor(fa, c, anchor, offset, L_):
    start = anchor - offset
    if c not in fa:
        return None
    chrom_len = len(fa[c])
    if start < 0 or start + L_ > chrom_len:
        return None
    seq = str(fa[c][start:start + L_]).upper()
    if len(seq) != L_ or not set(seq).issubset(ALPHABET):
        return None
    return seq


def sample_anchored(fa, anchors, n, rng, min_off=30, max_off=170):
    out = []
    idxs = rng.permutation(len(anchors))
    for i in idxs:
        c, anchor = anchors[i]
        offset = int(rng.integers(min_off, max_off))
        seq = window_from_anchor(fa, c, anchor, offset, L)
        if seq is None:
            continue
        out.append(seq)
        if len(out) >= n:
            break
    return out


def sample_ccre_offcenter(fa, rows, n, rng):
    anchors = [(c, (s + e) // 2) for c, s, e in rows]
    return sample_anchored(fa, anchors, n, rng, min_off=20, max_off=180)


def main():
    rng = np.random.default_rng(SEED)
    hg38 = Fasta(HG38, sequence_always_upper=True)
    mm39 = Fasta(MM39, sequence_always_upper=True)

    print("Sampling natural human (15K)...", file=sys.stderr)
    nat_h = sample_natural(hg38, HG38_CHROMS, 15_000, rng)

    print("Loading high-conf cCRE...", file=sys.stderr)
    ccre = load_ccre_high_conf()
    print(f"  {len(ccre)} cCREs", file=sys.stderr)
    print("Sampling cCRE off-center (10K)...", file=sys.stderr)
    ccre_seqs = sample_ccre_offcenter(hg38, ccre, 10_000, rng)

    print("Loading pan-tissue DHS summits...", file=sys.stderr)
    dhs = load_dhs_summits(component=None)
    print(f"  {len(dhs)} DHS summits", file=sys.stderr)
    print("Sampling DHS pan-tissue (10K)...", file=sys.stderr)
    dhs_seqs = sample_anchored(hg38, dhs, 10_000, rng, min_off=40, max_off=160)

    print("Loading neural-component DHS summits...", file=sys.stderr)
    neural = load_dhs_summits(component="Neural")
    print(f"  {len(neural)} neural-tagged DHS summits", file=sys.stderr)
    print("Sampling neural DHS (10K)...", file=sys.stderr)
    neural_seqs = sample_anchored(hg38, neural, 10_000, rng, min_off=40, max_off=160)

    print("Sampling mouse natural (5K)...", file=sys.stderr)
    nat_m = sample_natural(mm39, MM39_CHROMS, 5_000, rng)

    seqs = nat_h + ccre_seqs + dhs_seqs + neural_seqs + nat_m
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
