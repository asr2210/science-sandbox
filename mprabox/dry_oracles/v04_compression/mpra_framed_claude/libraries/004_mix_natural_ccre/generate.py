"""Experiment 004: 50/50 mix of random genomic + cCRE-centered.

Tests whether cCRE adds value when combined with broad genomic coverage.
Exp 002 (50K natural) scored 0.480 on eval_01. Exp 003 (50K cCRE) scored
0.345. If mix > 0.480, cCRE helps when given a baseline of natural-DNA
diversity. If mix ≈ 0.480, cCRE neither helps nor hurts. If < 0.480,
cCRE actively harms.

Hypothesis: mix beats pure natural because the cCRE half provides
high-information regulatory examples while the natural half provides
the activity-range coverage and negative examples.

Generalization argument: mix should out-generalize either pure source.
Natural provides the "what does nothing" baseline; cCRE provides the
"what regulates" content. The model trained on the mix can both identify
regulatory motifs *and* tell when sequences lack them — both essential
for predicting activity in unseen cell types.
"""
import gzip
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 25_000
N_CCRE = N_SEQ - N_NATURAL
L = 200
SEED = 0

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GENOME = os.path.join(REPO_ROOT, "data", "hg38.fa")
CCRE = os.path.join(REPO_ROOT, "data", "ccre.bed.gz")

PRIMARY_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
PRIMARY_SET = set(PRIMARY_CHROMS)
HIGH_CONF = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}


def sample_natural(fa, n, rng):
    chrom_lens = {c: len(fa[c]) for c in PRIMARY_CHROMS}
    chroms = np.array(PRIMARY_CHROMS)
    weights = np.array([chrom_lens[c] for c in PRIMARY_CHROMS], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = rng.choice(chroms, p=weights)
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
    return out


def sample_ccre(fa, n, rng):
    elements = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            cls = parts[9]
            if chrom not in PRIMARY_SET or cls not in HIGH_CONF:
                continue
            mid = (start + end) // 2
            elements.append((chrom, mid))
    idx = rng.permutation(len(elements))
    out = []
    for i in idx:
        chrom, mid = elements[i]
        start = mid - L // 2
        end = start + L
        if start < 0 or end > len(fa[chrom]):
            continue
        s = str(fa[chrom][start:end]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
        if len(out) >= n:
            break
    return out


def main():
    fa = Fasta(GENOME, sequence_always_upper=True)
    rng = np.random.default_rng(SEED)

    natural = sample_natural(fa, N_NATURAL, rng)
    print(f"natural: {len(natural)}")
    ccre = sample_ccre(fa, N_CCRE, rng)
    print(f"cCRE: {len(ccre)}")

    seqs = natural + ccre
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ} mixed sequences to {out}")


if __name__ == "__main__":
    main()
