"""Experiment 009: 25K natural + 25K natural windows containing a cCRE at random offset.

For each cCRE, instead of centering, pick a 200bp window such that the
cCRE midpoint falls somewhere in [25..175] of the window (uniform).
This adds positional diversity to the regulatory half — sometimes
cCRE on the left, sometimes right, sometimes center, sometimes with
mostly flanking natural genomic context.

Hypothesis: positional diversity helps the model learn that regulatory
elements can appear anywhere in a 200bp window. Centering may have been
a positional bias.

Generalization argument: in unseen cell types, regulatory elements
appear at unpredictable positions within any test window. Training with
positionally-diverse cCRE locations should match that better than
training with always-centered cCREs.
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


def sample_offcenter_ccre(fa, n, rng):
    elements = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            cls = parts[9]
            if chrom not in PRIMARY_SET or cls not in HIGH_CONF:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            elements.append((chrom, mid))
    idx = rng.permutation(len(elements))
    out = []
    for i in idx:
        chrom, mid = elements[i]
        # offset: where in [25, 175] the cCRE mid lands within the 200bp window
        offset = int(rng.integers(25, 176))
        start = mid - offset
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
    ccre = sample_offcenter_ccre(fa, N_CCRE, rng)
    print(f"offcenter cCRE: {len(ccre)}")
    seqs = natural + ccre
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ} sequences")


if __name__ == "__main__":
    main()
