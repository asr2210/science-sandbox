"""Experiment 003 — dhs_signal_breadth_mixture.

50% sampled from DHS Index weighted by `mean_signal` (the
sharp-discrimination half from experiment 001) + 50% sampled by
`numsamples` (the cell-type-invariance half from experiment 002).

Goal: test whether the two axes are complementary. If 003 beats both
001 (eval_01) and 002 (cross-14 mean), they combine; if it falls
strictly between them, they are substitutes.
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
N_HALF = N_TARGET // 2  # 25_000 per weighting scheme
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
    """Draw n_to_get unique valid 200bp ACGT seqs by `weights`.

    Skips any element index already in `drawn_global` so the two halves
    never overlap.
    """
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
        # Half from mean_signal, half from numsamples. Order randomised
        # (signal-first or breadth-first) per seed to remove any
        # systematic interaction with set membership.
        order = ["signal", "breadth"]
        rng.shuffle(order)
        seqs: list[str] = []
        for which in order:
            w = signals if which == "signal" else numsamples
            half = draw_with_weight(
                rng, N_HALF, w, drawn, chrom_idx, summits,
                chrom_names, chrom_lens, tb,
            )
            seqs.extend(half)
        # Final shuffle so the file isn't visually segmented.
        rng.shuffle(seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: order={order} wrote {len(seqs):,} in "
              f"{time.time() - ts:.1f}s", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
