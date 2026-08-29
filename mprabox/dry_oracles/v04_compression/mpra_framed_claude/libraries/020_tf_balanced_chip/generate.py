"""Experiment 020: TF-balanced ReMap ChIP peaks.

Same as exp 015 (ChIP substituting cCRE) but enforce TF balance: cap
peaks per TF to spread vocabulary across all TFs in ReMap, rather than
random sampling which is dominated by heavily-studied TFs (TP53, MYC,
CTCF, GATA, etc.).

20K natural + 15K TF-balanced ChIP + 10K DHS + 5K mouse.

Strategy: scan ReMap once, bucket peak locations by TF (col 4 = "TF:cell").
For each TF, keep up to PEAKS_PER_TF random peaks (reservoir sample per
TF). After scan, sample 15K windows total proportional to per-TF count
but capped.

Hypothesis: TF motif vocabulary in random ChIP is dominated by top ~50
TFs; balanced sampling exposes the model to rare-TF motifs.
"""
import gzip
import os
from collections import defaultdict

import numpy as np
from pyfaidx import Fasta

N_SEQ = 50_000
N_NATURAL = 20_000
N_CHIP = 15_000
N_DHS = 10_000
N_MOUSE = N_SEQ - N_NATURAL - N_CHIP - N_DHS
L = 200
SEED = 0
PEAKS_PER_TF = 30  # cap per TF

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


def collect_tf_balanced_chip(rng, peaks_per_tf):
    """Scan ReMap once; for each TF, reservoir-sample up to peaks_per_tf
    (chrom, summit) tuples."""
    rs = np.random.default_rng(int(rng.integers(0, 2**31)))
    per_tf = defaultdict(list)
    per_tf_count = defaultdict(int)
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
            # parts[4] looks like "TF:CellType" (possibly comma-separated cells)
            tf = parts[3].split(":")[0]
            seen = per_tf_count[tf]
            if len(per_tf[tf]) < peaks_per_tf:
                per_tf[tf].append((chrom, summit))
            else:
                j = int(rs.integers(0, seen + 1))
                if j < peaks_per_tf:
                    per_tf[tf][j] = (chrom, summit)
            per_tf_count[tf] += 1
    print(f"TFs found: {len(per_tf)}, peaks/TF capped at {peaks_per_tf}, "
          f"total candidates: {sum(len(v) for v in per_tf.values())}")
    return per_tf


def sample_chip_balanced(fa, n, rng):
    per_tf = collect_tf_balanced_chip(rng, PEAKS_PER_TF)
    # Flatten and shuffle
    all_peaks = []
    for tf, peaks in per_tf.items():
        for p in peaks:
            all_peaks.append(p)
    print(f"Flattened candidates: {len(all_peaks)}")
    idx = rng.permutation(len(all_peaks))
    out = []
    for i in idx:
        chrom, summit = all_peaks[i]
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
    chip = sample_chip_balanced(hg, N_CHIP, rng)
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
