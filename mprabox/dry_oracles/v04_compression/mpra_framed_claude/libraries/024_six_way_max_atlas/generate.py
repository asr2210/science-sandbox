"""Experiment 024: 6-way maximal-atlas diversity mix.

20K natural + 8K cCRE + 7K DHS + 7K ChIP + 3K FANTOM + 5K mouse = 50K.

Spreads 25K regulatory content across 4 distinct atlas modalities
(cCRE chromatin marks, DHS DNase accessibility, ChIP TF binding,
FANTOM CAGE transcription). Each atlas at 6-16%.

Tests if maximal modality diversity helps when individual atlas sizes
are smaller. Previous tests (013, 015, 021) varied 2-3 atlases; this
tests all 4 atlases simultaneously.

Prediction: within noise of plateau (0.494-0.504). If exceeds 0.508,
then modality multiplexing matters.
"""
import gzip
import os
from collections import defaultdict

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 20_000
N_CCRE = 8_000
N_DHS = 7_000
N_CHIP = 7_000
N_FANTOM = 3_000
N_MOUSE = N_SEQ - N_NATURAL - N_CCRE - N_DHS - N_CHIP - N_FANTOM
L = 200
SEED = 0
CHIP_RESERVOIR = 100_000

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HG38 = os.path.join(REPO_ROOT, "data", "hg38.fa")
MM39 = os.path.join(REPO_ROOT, "data", "mm39.fa")
CCRE = os.path.join(REPO_ROOT, "data", "ccre.bed.gz")
DHS = os.path.join(REPO_ROOT, "data", "dhs_index.tsv.gz")
REMAP = os.path.join(REPO_ROOT, "data", "remap_nr.bed.gz")
FANTOM = os.path.join(REPO_ROOT, "data", "fantom5_enhancers.bed.gz")

HUMAN_CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
MOUSE_CHROMS = [f"chr{i}" for i in range(1, 20)] + ["chrX", "chrY"]
HUMAN_SET = set(HUMAN_CHROMS)
HIGH_CONF = {"PLS", "pELS", "dELS", "CA-TF", "CA-CTCF"}


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


def sample_offcenter_ccre(fa, n, rng):
    elements = []
    with gzip.open(CCRE, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if parts[0] not in HUMAN_SET or parts[9] not in HIGH_CONF:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            elements.append((parts[0], mid))
    idx = rng.permutation(len(elements))
    out = []
    for i in idx:
        chrom, mid = elements[i]
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


def reservoir_sample_chip(rng, k):
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


def sample_fantom(fa, n, rng):
    elements = []
    with gzip.open(FANTOM, "rt") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            chrom = parts[0]
            if chrom not in HUMAN_SET:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            elements.append((chrom, mid))
    idx = rng.permutation(len(elements))
    out = []
    for i in idx:
        chrom, mid = elements[i]
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
    hg = Fasta(HG38, sequence_always_upper=True)
    mm = Fasta(MM39, sequence_always_upper=True)
    rng = np.random.default_rng(SEED)
    natural = sample_natural(hg, HUMAN_CHROMS, N_NATURAL, rng)
    ccre = sample_offcenter_ccre(hg, N_CCRE, rng)
    dhs = sample_dhs(hg, N_DHS, rng)
    chip = sample_chip(hg, N_CHIP, rng)
    fantom = sample_fantom(hg, N_FANTOM, rng)
    mouse = sample_natural(mm, MOUSE_CHROMS, N_MOUSE, rng)
    seqs = natural + ccre + dhs + chip + fantom + mouse
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ}: nat={len(natural)} ccre={len(ccre)} dhs={len(dhs)} "
          f"chip={len(chip)} fantom={len(fantom)} mouse={len(mouse)}")


if __name__ == "__main__":
    main()
