"""Experiment 002: natural human genomic DNA from random windows.

Sample 50,000 200bp windows uniformly at random from primary hg38
chromosomes (chr1-22, X, Y). Skip any window containing N. Uppercase
to remove soft-masking.

Hypothesis: natural DNA carries the regulatory grammar (TFBS, CpG depletion,
k-mer co-occurrence) of all human cell types — features the model needs
to learn to generalize beyond K562/HepG2/SK-N-SH.

Generalization argument: random genomic windows are an unbiased sample of
the human regulatory landscape — not enriched for any particular cell
type's accessible chromatin. A model trained on it sees the "average"
regulatory grammar shared across cell types, which should transfer
better than e.g. a K562-enriched library.
"""
import os
import sys

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
L = 200
SEED = 0

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GENOME = os.path.join(REPO_ROOT, "data", "hg38.fa")

PRIMARY_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]


def main():
    fa = Fasta(GENOME, sequence_always_upper=True)
    chrom_lens = {c: len(fa[c]) for c in PRIMARY_CHROMS}
    total = sum(chrom_lens.values())
    print(f"primary genome length: {total/1e9:.2f} Gbp")

    rng = np.random.default_rng(SEED)
    chroms = np.array(PRIMARY_CHROMS)
    weights = np.array([chrom_lens[c] for c in PRIMARY_CHROMS], dtype=np.float64)
    weights /= weights.sum()

    seqs = []
    n_attempt = 0
    while len(seqs) < N_SEQ:
        c = rng.choice(chroms, p=weights)
        start = rng.integers(0, chrom_lens[c] - L)
        s = str(fa[c][start:start + L]).upper()
        n_attempt += 1
        if "N" in s:
            continue
        if len(s) != L:
            continue
        seqs.append(s)
        if len(seqs) % 10_000 == 0:
            print(f"  {len(seqs)} kept / {n_attempt} attempts")

    print(f"final: {len(seqs)} kept / {n_attempt} attempts")
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    assert all(len(s) == L for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:1000])
    print(f"wrote {N_SEQ} sequences to {out}")


if __name__ == "__main__":
    main()
