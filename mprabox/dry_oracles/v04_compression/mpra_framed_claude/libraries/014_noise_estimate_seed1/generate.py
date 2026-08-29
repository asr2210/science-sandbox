"""Experiment 014: Noise floor estimate — re-run exp 011 design with seed=1.

Same composition as exp 011 (current best, eval_01=0.5012):
20K natural + 15K cCRE off-center + 10K DHS + 5K mouse.

Only difference: SEED=1 instead of SEED=0.

Purpose: estimate the run-to-run noise of eval_01. If 014 differs from 011
by more than ~0.005, then differences of that scale across exps 011/012/013
are noise, not signal. This grounds future interpretations.
"""
import gzip
import os

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 20_000
N_CCRE = 15_000
N_DHS = 10_000
N_MOUSE = N_SEQ - N_NATURAL - N_CCRE - N_DHS
L = 200
SEED = 1

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
HG38 = os.path.join(REPO_ROOT, "data", "hg38.fa")
MM39 = os.path.join(REPO_ROOT, "data", "mm39.fa")
CCRE = os.path.join(REPO_ROOT, "data", "ccre.bed.gz")
DHS = os.path.join(REPO_ROOT, "data", "dhs_index.tsv.gz")

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


def main():
    hg = Fasta(HG38, sequence_always_upper=True)
    mm = Fasta(MM39, sequence_always_upper=True)
    rng = np.random.default_rng(SEED)
    natural = sample_natural(hg, HUMAN_CHROMS, N_NATURAL, rng)
    ccre = sample_offcenter_ccre(hg, N_CCRE, rng)
    dhs = sample_dhs(hg, N_DHS, rng)
    mouse = sample_natural(mm, MOUSE_CHROMS, N_MOUSE, rng)
    seqs = natural + ccre + dhs + mouse
    rng.shuffle(seqs)
    assert len(seqs) == N_SEQ
    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N_SEQ}: nat={len(natural)} ccre={len(ccre)} dhs={len(dhs)} mouse={len(mouse)}")


if __name__ == "__main__":
    main()
