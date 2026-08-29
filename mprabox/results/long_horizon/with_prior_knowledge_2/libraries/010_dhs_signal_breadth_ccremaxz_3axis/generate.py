"""Experiment 010 — dhs_signal_breadth_ccremaxz_3axis.

Adds a third additive axis to the 003 winning recipe: ENCODE cCRE
maxZ score (max z-score across DNase + H3K27ac + H3K4me3 + CTCF
within the cCRE that overlaps the DHS). Cell-type-aggregated by
construction, so the third axis is cell-type-agnostic.

Plan:
- Axis 1: 16,667 sequences, weighted by mean_signal (sharp specificity)
- Axis 2: 16,666 sequences, weighted by numsamples (broad invariance)
- Axis 3: 16,667 sequences, weighted by cCRE_maxZ (multi-mark
  regulatory strength). Only cCRE-overlapping DHS (1.35M of 3.59M)
  participate; non-cCRE DHS have weight 0.
- All three draws disjoint. 3 seeds.

Tests whether multi-mark regulatory strength is a third orthogonal
quality axis on top of single-mark DNase signal + breadth.
"""

import gzip
import os
import time

import numpy as np
import twobitreader

DATA_DIR = "/data/users/arao/mpra_autoresearch/data"
DHS_PATH = f"{DATA_DIR}/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
GENOME_PATH = f"{DATA_DIR}/genome/hg38.2bit"
CCRE_MAXZ_PATH = f"{DATA_DIR}/cCRE/dhs_ccre_maxz.npy"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_TARGET = 50_000
N_PER_AXIS = (N_TARGET + 2) // 3  # 16,667
SEQ_LEN = 200
HALF = SEQ_LEN // 2
N_SEEDS = 3
VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_dhs_index_with_maxz():
    chrom_to_idx = {c: i for i, c in enumerate(sorted(VALID_CHROMS))}
    full_maxz = np.load(CCRE_MAXZ_PATH)
    chroms_arr, summits, signals, numsamples, maxz = [], [], [], [], []
    with gzip.open(DHS_PATH, "rt") as f:
        next(f)
        for tsv_row, line in enumerate(f):
            p = line.rstrip("\n").split("\t")
            c = p[0]
            if c not in chrom_to_idx:
                continue
            chroms_arr.append(chrom_to_idx[c])
            summits.append(int(p[6]))
            signals.append(float(p[4]))
            numsamples.append(int(p[5]))
            maxz.append(float(full_maxz[tsv_row]))
    return (
        np.asarray(chroms_arr, dtype=np.int8),
        np.asarray(summits, dtype=np.int32),
        np.asarray(signals, dtype=np.float32),
        np.asarray(numsamples, dtype=np.float32),
        np.asarray(maxz, dtype=np.float32),
    )


def draw_with_weight(rng, n_to_get, weights, drawn_global, chrom_idx, summits,
                     chrom_names, chrom_lens, tb):
    # Restrict to elements with strictly positive weight.
    pos_idx = np.where(weights > 0)[0]
    pos_w = weights[pos_idx]
    probs = pos_w / pos_w.sum()
    n_total = len(pos_idx)
    seqs: list[str] = []
    batch = max(n_to_get + 5_000, int(n_to_get * 1.2))
    while len(seqs) < n_to_get:
        n_remaining = n_total - sum(1 for i in pos_idx if int(i) in drawn_global)
        n_request = min(batch, n_remaining)
        if n_request <= 0:
            break
        local_idx = rng.choice(n_total, size=n_request, replace=False, p=probs)
        idx = [int(pos_idx[k]) for k in local_idx if int(pos_idx[k]) not in drawn_global]
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
    print("Loading DHS Index + cCRE maxZ ...", flush=True)
    chrom_idx, summits, signals, numsamples, maxz = load_dhs_index_with_maxz()
    print(f"  {len(chrom_idx):,} rows. "
          f"cCRE-overlapping (maxZ>0): {(maxz > 0).sum():,}", flush=True)

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    n_seqs_target = [N_PER_AXIS, N_PER_AXIS, N_TARGET - 2 * N_PER_AXIS]
    print(f"  per-axis seq targets: {n_seqs_target}", flush=True)

    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        drawn: set[int] = set()
        order_axes = list(zip(["signal", "breadth", "maxz"],
                              [signals, numsamples, maxz],
                              n_seqs_target))
        rng.shuffle(order_axes)
        seqs: list[str] = []
        for which, w, n in order_axes:
            chunk = draw_with_weight(
                rng, n, w, drawn, chrom_idx, summits, chrom_names, chrom_lens, tb,
            )
            print(f"  seed={seed}: axis={which} drew {len(chunk):,}",
                  flush=True)
            seqs.extend(chunk)
        rng.shuffle(seqs)
        seqs = seqs[:N_TARGET]
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: wrote {len(seqs):,} in {time.time() - ts:.1f}s",
              flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
