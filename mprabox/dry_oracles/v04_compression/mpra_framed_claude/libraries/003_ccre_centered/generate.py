"""Experiment 003: cCRE-centered regulatory sequences.

Sample 50,000 cCREs from the high-confidence classes (PLS, pELS, dELS,
CA-TF, CA-CTCF) of ENCODE registry V4 (ENCFF286VQG). For each, extract
a 200bp window centered on the cCRE midpoint. Uppercase.

Hypothesis: cCREs are the regulatory vocabulary of the human genome.
Density of functional motifs is ~10-100x higher than in random genomic
DNA. If motif density is what matters for the model, this beats exp 002.

Generalization argument: cCREs were called across hundreds of cell types
(not just K562/HepG2/SK-N-SH), so the library is biased toward "regulatory
content shared across cell types" rather than any particular cell type's
specific enhancers. This is exactly the kind of training data that should
generalize to unseen cell types: it teaches the model the universal
motif/syntax vocabulary, not a cell-type-specific dialect.
"""
import gzip
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
L = 200
SEED = 0

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GENOME = os.path.join(REPO_ROOT, "data", "hg38.fa")
CCRE = os.path.join(REPO_ROOT, "data", "ccre.bed.gz")

PRIMARY_CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])
HIGH_CONF = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}


def main():
    fa = Fasta(GENOME, sequence_always_upper=True)

    # Load high-confidence cCREs
    elements = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            cls = parts[9]
            if chrom not in PRIMARY_CHROMS:
                continue
            if cls not in HIGH_CONF:
                continue
            mid = (start + end) // 2
            elements.append((chrom, mid))
    print(f"loaded {len(elements)} high-confidence cCREs")

    rng = np.random.default_rng(SEED)
    idx = rng.permutation(len(elements))

    seqs = []
    n_attempt = 0
    for i in idx:
        chrom, mid = elements[i]
        start = mid - L // 2
        end = start + L
        chrom_len = len(fa[chrom])
        if start < 0 or end > chrom_len:
            continue
        s = str(fa[chrom][start:end]).upper()
        n_attempt += 1
        if "N" in s or len(s) != L:
            continue
        seqs.append(s)
        if len(seqs) >= N_SEQ:
            break
        if len(seqs) % 10_000 == 0:
            print(f"  {len(seqs)} kept / {n_attempt} attempts")

    print(f"final: {len(seqs)} kept / {n_attempt} attempts")
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ} sequences to {out}")


if __name__ == "__main__":
    main()
