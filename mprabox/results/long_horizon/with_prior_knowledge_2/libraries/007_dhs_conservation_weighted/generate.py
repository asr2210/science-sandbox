"""Experiment 007 — dhs_conservation_weighted.

Sample 50,000 DHS Index elements weighted by mean phyloP100way score
over the 200bp summit-centered window. phyloP precomputed in
`data/conservation/dhs_phyloP_mean.npy` (aligned to TSV row order).

Pure conservation-axis test, parallel to 001 (signal-only) and 002
(breadth-only). Validates whether conservation is a usable quality axis
before mixing it in 008+.
"""

import gzip
import os
import time

import numpy as np
import twobitreader

DATA_DIR = "/data/users/arao/mpra_autoresearch/data"
DHS_PATH = f"{DATA_DIR}/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
GENOME_PATH = f"{DATA_DIR}/genome/hg38.2bit"
PHYLOP_PATH = f"{DATA_DIR}/conservation/dhs_phyloP_mean.npy"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_TARGET = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
N_SEEDS = 3
VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_dhs_index_with_phylop():
    """Returns (chrom_idx, summit, phyloP_score) arrays for valid rows.

    phyloP_score is clamped to a min of 0.01 so sampling can include
    accelerated regions at low weight (we don't want to *exclude* them
    with zero probability — they may still encode useful signal).
    """
    chrom_to_idx = {c: i for i, c in enumerate(sorted(VALID_CHROMS))}
    full_phylop = np.load(PHYLOP_PATH)
    chroms_arr, summits, scores, valid_idx = [], [], [], []
    with gzip.open(DHS_PATH, "rt") as f:
        next(f)
        for tsv_row, line in enumerate(f):
            p = line.rstrip("\n").split("\t")
            c = p[0]
            if c not in chrom_to_idx:
                continue
            score = full_phylop[tsv_row]
            if not np.isfinite(score):
                continue
            chroms_arr.append(chrom_to_idx[c])
            summits.append(int(p[6]))
            scores.append(max(0.01, float(score)))
            valid_idx.append(tsv_row)
    return (
        np.asarray(chroms_arr, dtype=np.int8),
        np.asarray(summits, dtype=np.int32),
        np.asarray(scores, dtype=np.float32),
    )


def sample_sequences(seed, chrom_idx, summits, weights, chrom_names, chrom_lens, tb):
    rng = np.random.default_rng(seed)
    probs = weights / weights.sum()
    n_total = len(weights)
    drawn: set[int] = set()
    seqs: list[str] = []
    batch = max(N_TARGET + 10_000, int(N_TARGET * 1.2))
    while len(seqs) < N_TARGET:
        n_remaining = n_total - len(drawn)
        n_request = min(batch, n_remaining)
        idx = rng.choice(n_total, size=n_request, replace=False, p=probs)
        idx = [int(i) for i in idx if int(i) not in drawn]
        for i in idx:
            drawn.add(i)
            c = chrom_names[chrom_idx[i]]
            s = int(summits[i])
            start, end = s - HALF, s + HALF
            if start < 0 or end > chrom_lens[c]:
                continue
            seq = tb[c][start:end].upper()
            if len(seq) != SEQ_LEN or "N" in seq:
                continue
            seqs.append(seq)
            if len(seqs) >= N_TARGET:
                break
        batch = 10_000
    return seqs[:N_TARGET]


def main():
    t0 = time.time()
    print("Loading DHS Index + phyloP ...", flush=True)
    chrom_idx, summits, weights = load_dhs_index_with_phylop()
    print(f"  {len(chrom_idx):,} valid rows; phyloP weight quartiles "
          f"{np.percentile(weights, [25, 50, 75, 95, 99])}", flush=True)

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    for seed in range(N_SEEDS):
        ts = time.time()
        seqs = sample_sequences(
            seed, chrom_idx, summits, weights, chrom_names, chrom_lens, tb
        )
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: wrote {len(seqs):,} in {time.time() - ts:.1f}s",
              flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
