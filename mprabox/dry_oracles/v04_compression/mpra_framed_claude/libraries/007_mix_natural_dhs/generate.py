"""Experiment 007: 25K natural + 25K DHS-summit-centered (multi-cell-type).

Tests if the Meuleman 2020 DHS Index (3.6M open-chromatin sites across
438 biosamples) is a better regulatory source than cCRE for cross-cell-type
generalization, vs exp 004 (natural+cCRE = 0.494).

For each DHS, take 200bp centered on the summit. Stratify DHS sampling
across all 16 tissue components proportional to component size, so the
sample is representative of the genome-wide accessibility landscape.

Generalization argument: DHS index covers cell types we don't measure
(K562/HepG2/SK-N-SH are 3 of 438 biosamples). A library containing
regulatory regions from many cell types should expose the model to the
universal motif/syntax grammar shared across them. This is a more direct
test of "regulatory content from many cell types" than cCRE.
"""
import gzip
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 25_000
N_DHS = N_SEQ - N_NATURAL
L = 200
SEED = 0

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GENOME = os.path.join(REPO_ROOT, "data", "hg38.fa")
DHS = os.path.join(REPO_ROOT, "data", "dhs_index.tsv.gz")

PRIMARY_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
PRIMARY_SET = set(PRIMARY_CHROMS)


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


def sample_dhs(fa, n, rng):
    # Stratify by tissue component proportional to component frequency.
    # Simpler: load summits, sample n at random — already proportional.
    summits = []  # (chrom, summit)
    with gzip.open(DHS, "rt") as f:
        next(f)  # header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in PRIMARY_SET:
                continue
            summit = int(parts[6])
            summits.append((chrom, summit))
    print(f"loaded {len(summits)} DHS summits")
    idx = rng.permutation(len(summits))
    out = []
    for i in idx:
        chrom, mid = summits[i]
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
    dhs = sample_dhs(fa, N_DHS, rng)
    print(f"dhs: {len(dhs)}")

    seqs = natural + dhs
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ} sequences")


if __name__ == "__main__":
    main()
