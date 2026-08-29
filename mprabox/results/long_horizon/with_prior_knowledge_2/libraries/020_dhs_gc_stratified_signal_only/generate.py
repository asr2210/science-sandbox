"""Experiment 020 — dhs_gc_stratified_signal_only.

Ablation of 015: same GC stratification (5 equal-population bins)
but with 100% mean_signal weighting (no numsamples/breadth axis at
all). 10K signal-weighted draws per bin = 50K total.

Tests whether the breadth axis (numsamples) is still needed when
GC stratification is in play, or whether GC stratification's
"include lower-signal but GC-poor elements" mechanism implicitly
captures the breadth-axis benefit.

If 020 ≥ 015: drop breadth axis, simpler recipe.
If 020 < 015: numsamples axis carries information distinct from GC
stratification.
"""

import gzip
import os
import time

import numpy as np
import twobitreader

DATA_DIR = "/data/users/arao/mpra_autoresearch/data"
DHS_PATH = f"{DATA_DIR}/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
GENOME_PATH = f"{DATA_DIR}/genome/hg38.2bit"
GC_PATH = f"{DATA_DIR}/dhs/dhs_gc.npy"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_TARGET = 50_000
N_BINS = 5
N_PER_BIN = N_TARGET // N_BINS  # 10,000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
N_SEEDS = 3
VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_dhs_index():
    chrom_to_idx = {c: i for i, c in enumerate(sorted(VALID_CHROMS))}
    chroms_arr, summits, signals, numsamples = [], [], [], []
    with gzip.open(DHS_PATH, "rt") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            c = p[0]
            if c not in chrom_to_idx:
                continue
            chroms_arr.append(chrom_to_idx[c])
            summits.append(int(p[6]))
            signals.append(float(p[4]))
            numsamples.append(int(p[5]))
    return (
        np.asarray(chroms_arr, dtype=np.int8),
        np.asarray(summits, dtype=np.int32),
        np.asarray(signals, dtype=np.float32),
        np.asarray(numsamples, dtype=np.float32),
    )


def draw_with_weight(rng, n_to_get, candidate_idx, weights, drawn_global,
                     chrom_idx, summits, chrom_names, chrom_lens, tb):
    """Draw n_to_get sequences from candidate_idx, weighted by weights[candidate_idx]."""
    sub_w = weights[candidate_idx]
    probs = sub_w / sub_w.sum()
    n_pool = len(candidate_idx)
    seqs: list[str] = []
    batch = max(n_to_get + 5_000, int(n_to_get * 1.2))
    while len(seqs) < n_to_get:
        n_request = min(batch, n_pool)
        local_idx = rng.choice(n_pool, size=n_request, replace=False, p=probs)
        global_idx = [int(candidate_idx[i]) for i in local_idx
                      if int(candidate_idx[i]) not in drawn_global]
        for i in global_idx:
            drawn_global.add(i)
            c = chrom_names[chrom_idx[i]]
            s = int(summits[i])
            start, end = s - HALF, s + HALF
            if start < 0 or end > chrom_lens[c]:
                continue
            seq = tb[c][start:end].upper()
            if len(seq) != SEQ_LEN or "N" in seq:
                continue
            seqs.append(seq)
            if len(seqs) >= n_to_get:
                break
        batch = 5_000
    return seqs[:n_to_get]


def main():
    t0 = time.time()
    print("Loading DHS Index ...", flush=True)
    chrom_idx, summits, signals, numsamples = load_dhs_index()
    print(f"  {len(chrom_idx):,} rows.", flush=True)

    print("Loading GC content ...", flush=True)
    gc = np.load(GC_PATH)
    valid_mask = ~np.isnan(gc)
    print(f"  {valid_mask.sum():,} valid.", flush=True)

    # Equal-population GC quintiles over valid DHS.
    gc_valid = gc[valid_mask]
    bin_edges = np.percentile(gc_valid, np.linspace(0, 100, N_BINS + 1))
    bin_edges[0] -= 1e-6
    bin_edges[-1] += 1e-6
    print(f"  GC bin edges: {[f'{e:.3f}' for e in bin_edges]}", flush=True)

    bin_idx_per_dhs = np.full(len(gc), -1, dtype=np.int8)
    for b in range(N_BINS):
        in_bin = valid_mask & (gc > bin_edges[b]) & (gc <= bin_edges[b + 1])
        bin_idx_per_dhs[in_bin] = b

    bin_candidates = [np.where(bin_idx_per_dhs == b)[0] for b in range(N_BINS)]
    for b in range(N_BINS):
        print(f"  bin {b}: {len(bin_candidates[b]):,} DHS", flush=True)

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        drawn: set[int] = set()
        seqs: list[str] = []

        bin_order = list(range(N_BINS))
        rng.shuffle(bin_order)
        for b in bin_order:
            part = draw_with_weight(
                rng, N_PER_BIN, bin_candidates[b], signals, drawn,
                chrom_idx, summits, chrom_names, chrom_lens, tb,
            )
            seqs.extend(part)

        rng.shuffle(seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: wrote {len(seqs):,} in "
              f"{time.time() - ts:.1f}s", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
