"""Experiment 015: replace cCRE with ReMap ChIP-seq peaks.

20K natural + 15K ReMap ChIP peaks + 10K DHS + 5K mouse.

ReMap2022 non-redundant peaks (68.6M entries across all TFs and cell
types) tag where TFs are *actually bound in vivo*, not just where
chromatin is open. cCRE/DHS mark accessibility; ChIP marks bound TF
identity + context.

Hypothesis: in-vivo TF binding adds motif identity + context information
beyond open-chromatin alone. If exp 015 > 0.508 (exp 011 + 2σ), ChIP
peaks contribute new signal. If equal, open-chromatin atlases already
capture most bound-TF information.

A/B test against exp 011: same structure, ChIP substitutes for cCRE.

Sampling strategy:
- Reservoir sample to keep memory bounded — read all 68M peaks once.
- For each kept peak, use the MACS summit (col 7) as the center, then
  apply random offset [25,176) like off-center cCRE.
- Skip N-containing windows.
"""
import gzip
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 20_000
N_CHIP = 15_000
N_DHS = 10_000
N_MOUSE = N_SEQ - N_NATURAL - N_CHIP - N_DHS
L = 200
SEED = 0
CHIP_RESERVOIR = 200_000  # >> 15K so we can be choosy about valid windows

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HG38 = os.path.join(REPO_ROOT, "data", "hg38.fa")
MM39 = os.path.join(REPO_ROOT, "data", "mm39.fa")
REMAP = os.path.join(REPO_ROOT, "data", "remap_nr.bed.gz")
DHS = os.path.join(REPO_ROOT, "data", "dhs_index.tsv.gz")

HUMAN_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MOUSE_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HUMAN_SET = set(HUMAN_CHROMS)


def sample_natural(fa, chroms, n, rng):
    chrom_lens = {c: len(fa[c]) for c in chroms}
    arr = np.array(chroms)
    weights = np.array([chrom_lens[c] for c in chroms], dtype=np.float64)
    weights /= weights.sum()
    out = []
    while len(out) < n:
        c = rng.choice(arr, p=weights)
        start = int(rng.integers(0, chrom_lens[c] - L))
        s = str(fa[c][start:start + L]).upper()
        if "N" in s or len(s) != L:
            continue
        out.append(s)
    return out


def reservoir_sample_chip(rng, k):
    """Single-pass reservoir sample of k ChIP peaks (chrom, summit)."""
    reservoir = []
    n = 0
    rs = np.random.default_rng(int(rng.integers(0, 2**31)))
    with gzip.open(REMAP, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in HUMAN_SET:
                continue
            try:
                summit = int(parts[6])
            except (ValueError, IndexError):
                continue
            if n < k:
                reservoir.append((chrom, summit))
            else:
                j = int(rs.integers(0, n + 1))
                if j < k:
                    reservoir[j] = (chrom, summit)
            n += 1
    print(f"ReMap peaks scanned: {n}, reservoir: {len(reservoir)}")
    return reservoir


def sample_chip(fa, n, rng):
    candidates = reservoir_sample_chip(rng, CHIP_RESERVOIR)
    idx = rng.permutation(len(candidates))
    out = []
    for i in idx:
        chrom, summit = candidates[i]
        offset = int(rng.integers(25, 176))
        start = summit - offset
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


def sample_dhs(fa, n, rng):
    summits = []
    with gzip.open(DHS, "rt") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in HUMAN_SET:
                continue
            summits.append((parts[0], int(parts[6])))
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
    hg = Fasta(HG38, sequence_always_upper=True)
    mm = Fasta(MM39, sequence_always_upper=True)
    rng = np.random.default_rng(SEED)
    natural = sample_natural(hg, HUMAN_CHROMS, N_NATURAL, rng)
    chip = sample_chip(hg, N_CHIP, rng)
    dhs = sample_dhs(hg, N_DHS, rng)
    mouse = sample_natural(mm, MOUSE_CHROMS, N_MOUSE, rng)
    seqs = natural + chip + dhs + mouse
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ}: nat={len(natural)} chip={len(chip)} dhs={len(dhs)} mouse={len(mouse)}")


if __name__ == "__main__":
    main()
