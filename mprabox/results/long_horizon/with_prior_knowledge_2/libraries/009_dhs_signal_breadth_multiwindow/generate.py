"""Experiment 009 — dhs_signal_breadth_multiwindow.

Structural test: does the model want N elements with 1 window each, or
N/2 elements with 2 windows each? Total seq count fixed at 50K.

Design:
- 25,000 unique DHS elements drawn via the 003 recipe
  (12,500 weighted by mean_signal + 12,500 weighted by numsamples,
   disjoint).
- Per element, emit TWO 200bp windows:
  * summit-centered: [summit - 100, summit + 100]
  * shifted +100bp: [summit, summit + 200]
- Total = 50,000 sequences. 3 seeds.

Tests element-diversity vs within-element-augmentation. If multi-window
beats 003, sequence-level position variation around the same element
teaches transferable motif recognition. If it loses, element diversity
is the dominant signal at this budget.
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
N_ELEMENTS = N_TARGET // 2  # 25K
N_QUARTER = N_ELEMENTS // 2  # 12.5K per axis
SEQ_LEN = 200
HALF = SEQ_LEN // 2
SHIFT = 100
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


def draw_element_indices(rng, n_to_get, weights, drawn_global, chrom_idx,
                         summits, chrom_lens_by_idx):
    """Pick n_to_get unique element indices whose BOTH windows fit in chrom."""
    probs = weights / weights.sum()
    n_total = len(weights)
    picked: list[int] = []
    batch = max(n_to_get + 5_000, int(n_to_get * 1.5))
    while len(picked) < n_to_get:
        n_remaining = n_total - len(drawn_global)
        n_request = min(batch, n_remaining)
        if n_request <= 0:
            break
        idx = rng.choice(n_total, size=n_request, replace=False, p=probs)
        for i in idx:
            i = int(i)
            if i in drawn_global:
                continue
            drawn_global.add(i)
            s = int(summits[i])
            clen = chrom_lens_by_idx[int(chrom_idx[i])]
            # Need both windows in-range:
            #   w1: [s-HALF, s+HALF], w2: [s, s+SEQ_LEN]
            if s - HALF < 0 or s + SEQ_LEN > clen:
                continue
            picked.append(i)
            if len(picked) >= n_to_get:
                break
        batch = 5_000
    return picked[:n_to_get]


def emit_windows(picked, chrom_idx, summits, chrom_names, tb):
    """For each element, emit two 200bp windows. Skip any that yield N."""
    seqs: list[str] = []
    for i in picked:
        c = chrom_names[int(chrom_idx[i])]
        s = int(summits[i])
        w1 = tb[c][s - HALF:s + HALF].upper()
        w2 = tb[c][s:s + SEQ_LEN].upper()
        if len(w1) == SEQ_LEN and "N" not in w1:
            seqs.append(w1)
        if len(w2) == SEQ_LEN and "N" not in w2:
            seqs.append(w2)
    return seqs


def main():
    t0 = time.time()
    print("Loading DHS Index ...", flush=True)
    chrom_idx, summits, signals, numsamples = load_dhs_index()
    print(f"  {len(chrom_idx):,} rows.", flush=True)

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens_by_idx = {i: len(tb[c]) for i, c in enumerate(chrom_names)}

    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        drawn: set[int] = set()
        order = ["signal", "breadth"]
        rng.shuffle(order)
        picked: list[int] = []
        # We over-pick by 5% to give ourselves headroom for any element
        # that yields a window with N (shouldn't happen given the start/end
        # check but may with shifted windows in repeat-rich tracts).
        target_per_axis = int(N_QUARTER * 1.05)
        for which in order:
            w = signals if which == "signal" else numsamples
            half = draw_element_indices(
                rng, target_per_axis, w, drawn, chrom_idx, summits,
                chrom_lens_by_idx,
            )
            picked.extend(half)
        seqs = emit_windows(picked, chrom_idx, summits, chrom_names, tb)
        # Drop excess to land exactly on 50K.
        seqs = seqs[:N_TARGET]
        rng.shuffle(seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: order={order} {len(picked):,} elements -> "
              f"{len(seqs):,} seqs in {time.time() - ts:.1f}s", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
