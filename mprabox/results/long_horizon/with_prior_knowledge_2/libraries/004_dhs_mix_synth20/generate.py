"""Experiment 004 — dhs_mix_synth20.

Three-axis library: 40% mean_signal-weighted DHS + 40% numsamples-weighted
DHS + 20% i.i.d. uniform random {A,C,G,T} sequences. The DHS halves come
from the 003 winning recipe; the synthetic dose targets the eval_08 gap.
50,000 sequences total × 3 seeds.
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
N_DHS_SIGNAL = 20_000
N_DHS_BREADTH = 20_000
N_SYNTH = 10_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
N_SEEDS = 3
VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
ALPHABET = np.array(["A", "C", "G", "T"])


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


def random_sequences(rng, n, length=SEQ_LEN):
    arr = rng.integers(0, 4, size=(n, length), dtype=np.uint8)
    chars = ALPHABET[arr]
    return ["".join(row) for row in chars]


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
        sig = draw_with_weight(rng, N_DHS_SIGNAL, signals, drawn, chrom_idx,
                                summits, chrom_names, chrom_lens, tb)
        bre = draw_with_weight(rng, N_DHS_BREADTH, numsamples, drawn, chrom_idx,
                                summits, chrom_names, chrom_lens, tb)
        syn = random_sequences(rng, N_SYNTH)
        seqs = sig + bre + syn
        rng.shuffle(seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: {len(sig)}+{len(bre)}+{len(syn)}={len(seqs)} "
              f"in {time.time() - ts:.1f}s", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
