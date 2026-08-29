"""Experiment 001 — dhs_signal_weighted.

Sample 50,000 DHS Index elements (Meuleman 2020, hg38) with probability
proportional to `mean_signal` (the closest proxy for NMF-topic-weighted
sampling given the columns available in the public Index file). Extract
200bp centered on the DHS `summit` column from hg38, drop any window
containing N or running off-chromosome, and oversample as needed to
reach exactly 50,000 valid 200bp ACGT sequences. Repeat for 3 seeds.
"""

import gzip
import os
import sys
import time

import numpy as np
import twobitreader

DATA_DIR = "/data/users/arao/mpra_autoresearch/data"
DHS_PATH = f"{DATA_DIR}/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
GENOME_PATH = f"{DATA_DIR}/genome/hg38.2bit"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_TARGET = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
N_SEEDS = 3

VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_dhs_index() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (chrom_idx, summit, mean_signal) for autosomal+sex DHS rows.

    chrom_idx is an int8 lookup into VALID_CHROMS_LIST so we can keep
    arrays compact; summit is int32; mean_signal is float32.
    """
    chrom_to_idx = {c: i for i, c in enumerate(sorted(VALID_CHROMS))}
    chroms_arr, summits, signals = [], [], []
    with gzip.open(DHS_PATH, "rt") as f:
        next(f)  # skip header
        for line in f:
            p = line.rstrip("\n").split("\t")
            c = p[0]
            if c not in chrom_to_idx:
                continue
            chroms_arr.append(chrom_to_idx[c])
            summits.append(int(p[6]))
            signals.append(float(p[4]))
    return (
        np.asarray(chroms_arr, dtype=np.int8),
        np.asarray(summits, dtype=np.int32),
        np.asarray(signals, dtype=np.float32),
    )


def sample_sequences(
    seed: int,
    chrom_idx: np.ndarray,
    summits: np.ndarray,
    signals: np.ndarray,
    chrom_names: list[str],
    chrom_lens: dict[str, int],
    tb: twobitreader.TwoBitFile,
) -> list[str]:
    """Draw weighted-without-replacement until we have N_TARGET valid seqs."""
    rng = np.random.default_rng(seed)
    probs = signals / signals.sum()
    n_total = len(signals)

    # Oversample: 60k initial draw covers the small fraction with N's or
    # off-chromosome windows. We pad iteratively if still short.
    drawn = set()
    seqs: list[str] = []
    batch = max(N_TARGET + 10_000, int(N_TARGET * 1.2))

    while len(seqs) < N_TARGET:
        n_remaining = n_total - len(drawn)
        n_request = min(batch, n_remaining)
        idx = rng.choice(n_total, size=n_request, replace=False, p=probs)
        # Drop any we have already inspected.
        idx = np.array([i for i in idx if i not in drawn])
        for i in idx:
            drawn.add(int(i))
            c = chrom_names[chrom_idx[i]]
            s = int(summits[i])
            start = s - HALF
            end = s + HALF
            if start < 0 or end > chrom_lens[c]:
                continue
            seq = tb[c][start:end].upper()
            if len(seq) != SEQ_LEN or "N" in seq:
                continue
            seqs.append(seq)
            if len(seqs) >= N_TARGET:
                break
        batch = 10_000  # smaller follow-up batches if needed

    return seqs[:N_TARGET]


def main() -> None:
    t0 = time.time()
    print("Loading DHS Index ...", flush=True)
    chrom_idx, summits, signals = load_dhs_index()
    print(
        f"  {len(chrom_idx):,} valid rows in {time.time() - t0:.1f}s",
        flush=True,
    )

    print("Opening hg38.2bit ...", flush=True)
    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    for seed in range(N_SEEDS):
        ts = time.time()
        seqs = sample_sequences(
            seed, chrom_idx, summits, signals, chrom_names, chrom_lens, tb
        )
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(
            f"seed={seed}: wrote {len(seqs):,} seqs to {out} "
            f"in {time.time() - ts:.1f}s",
            flush=True,
        )

    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
