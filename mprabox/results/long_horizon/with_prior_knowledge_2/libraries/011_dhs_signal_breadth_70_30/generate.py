"""Experiment 011 — dhs_signal_breadth_70_30.

Same as 003 but tilted to 70% mean_signal-weighted (35K) + 30%
numsamples-weighted (15K). Tests whether 003's 50/50 ratio is optimal
or whether a signal-heavy tilt yields a small improvement.

001 (signal-only) was 0.7242 on eval_01 vs 002 (breadth-only) at
0.7152 — signal is the stronger single axis. So a moderate tilt
toward signal might capture more actionable motif information per
element.
"""

import gzip
import os
import time

import numpy as np
import twobitreader

DATA_DIR = "/data/users/arao/mpra_autoresearch/data"
DHS_PATH = f"{DATA_DIR}/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
GENOME_PATH = f"{DATA_DIR}/genome/hg38.2bit"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_TARGET = 50_000
N_SIGNAL = 35_000
N_BREADTH = N_TARGET - N_SIGNAL  # 15,000
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


def draw_with_weight(rng, n_to_get, weights, drawn_global, chrom_idx, summits,
                     chrom_names, chrom_lens, tb):
    probs = weights / weights.sum()
    n_total = len(weights)
    seqs: list[str] = []
    batch = max(n_to_get + 5_000, int(n_to_get * 1.2))
    while len(seqs) < n_to_get:
        n_remaining = n_total - len(drawn_global)
        n_request = min(batch, n_remaining)
        idx = rng.choice(n_total, size=n_request, replace=False, p=probs)
        idx = [int(i) for i in idx if int(i) not in drawn_global]
        for i in idx:
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

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        drawn: set[int] = set()
        order = [("signal", N_SIGNAL), ("breadth", N_BREADTH)]
        rng.shuffle(order)
        seqs: list[str] = []
        for which, n in order:
            w = signals if which == "signal" else numsamples
            half = draw_with_weight(
                rng, n, w, drawn, chrom_idx, summits,
                chrom_names, chrom_lens, tb,
            )
            seqs.extend(half)
        rng.shuffle(seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: order={order} wrote {len(seqs):,} in "
              f"{time.time() - ts:.1f}s", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
