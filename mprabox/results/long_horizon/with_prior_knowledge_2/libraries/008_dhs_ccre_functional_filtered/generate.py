"""Experiment 008 — dhs_ccre_functional_filtered.

The 003 winning recipe (25K mean_signal-weighted + 25K numsamples-
weighted) restricted to DHS elements that overlap an ENCODE cCRE V3
class in {PLS, pELS, dELS} — i.e. elements that ENCODE classifies as
functional cis-regulatory (promoter / proximal enhancer / distal
enhancer). CTCF-only, DNase-H3K4me3, and "none" are excluded.

Tests whether ENCODE's multi-mark cCRE annotation captures regulatory
quality beyond what mean_signal + numsamples already capture. If yes,
cCRE class is an orthogonal "functional purity" filter we should keep.
If no, the 003 weights already implicitly select functional elements
and the cCRE label adds nothing.

Class distribution in the DHS pool (precomputed):
  none          2,238,078 (62%)  — excluded
  dELS            972,531 (27%)  — kept
  pELS            217,721 ( 6%)  — kept
  CTCF-only        72,756 ( 2%)  — excluded (architectural, not enhancer)
  PLS              56,316 (1.6%) — kept
  DNase-H3K4me3    34,496 ( 1%)  — excluded (orphan promoter mark)

Filtered pool: ~1.25M elements (35% of DHS). Plenty for 50K sample.
"""

import gzip
import os
import time

import numpy as np
import twobitreader

DATA_DIR = "/data/users/arao/mpra_autoresearch/data"
DHS_PATH = f"{DATA_DIR}/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
GENOME_PATH = f"{DATA_DIR}/genome/hg38.2bit"
CCRE_LABEL_PATH = f"{DATA_DIR}/cCRE/dhs_ccre_class.npy"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_TARGET = 50_000
N_HALF = N_TARGET // 2
SEQ_LEN = 200
HALF = SEQ_LEN // 2
N_SEEDS = 3
VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
KEEP_CLASSES = {"PLS", "pELS", "dELS"}


def load_dhs_filtered():
    """Load DHS rows, keeping only those whose cCRE class is in KEEP_CLASSES."""
    chrom_to_idx = {c: i for i, c in enumerate(sorted(VALID_CHROMS))}
    cls_arr = np.load(CCRE_LABEL_PATH, allow_pickle=True)
    chroms_arr, summits, signals, numsamples = [], [], [], []
    n_seen = 0
    with gzip.open(DHS_PATH, "rt") as f:
        next(f)
        for tsv_row, line in enumerate(f):
            n_seen += 1
            p = line.rstrip("\n").split("\t")
            c = p[0]
            if c not in chrom_to_idx:
                continue
            if cls_arr[tsv_row] not in KEEP_CLASSES:
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
    print("Loading DHS Index filtered to PLS/pELS/dELS ...", flush=True)
    chrom_idx, summits, signals, numsamples = load_dhs_filtered()
    print(f"  {len(chrom_idx):,} filtered rows", flush=True)
    print(f"  signal quartiles {np.percentile(signals, [25, 50, 75, 95])}",
          flush=True)
    print(f"  ns quartiles {np.percentile(numsamples, [25, 50, 75, 95])}",
          flush=True)

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        drawn: set[int] = set()
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
        rng.shuffle(seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: order={order} wrote {len(seqs):,} in "
              f"{time.time() - ts:.1f}s", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
