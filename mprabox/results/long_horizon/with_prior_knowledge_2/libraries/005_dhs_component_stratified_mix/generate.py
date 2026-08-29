"""Experiment 005 — dhs_component_stratified_mix.

Force equal sampling from each of the 16 NMF components in the DHS Index
("Cancer / epithelial", "Cardiac", ..., "Tissue invariant"). 3,125
sequences per component × 16 components = 50,000.

Within each component, use the 003 winning recipe: half by
`mean_signal`-weighting, half by `numsamples`-weighting (without
overlap inside the component).

Tests whether forcing biological-program diversity adds information
beyond the abundance-proportional signal+breadth mixture of 003.
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
N_COMPONENTS = 16
N_PER_COMP = N_TARGET // N_COMPONENTS  # 3125
SEQ_LEN = 200
HALF = SEQ_LEN // 2
N_SEEDS = 3
VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}


def load_dhs_index():
    """Returns dict: component -> (chrom_idx, summit, signal, numsamples) arrays."""
    chrom_to_idx = {c: i for i, c in enumerate(sorted(VALID_CHROMS))}
    by_comp: dict[str, list[list]] = {}
    with gzip.open(DHS_PATH, "rt") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            c = p[0]
            if c not in chrom_to_idx:
                continue
            comp = p[9]
            entry = by_comp.setdefault(comp, [[], [], [], []])
            entry[0].append(chrom_to_idx[c])
            entry[1].append(int(p[6]))
            entry[2].append(float(p[4]))
            entry[3].append(int(p[5]))
    out = {}
    for comp, lst in by_comp.items():
        out[comp] = (
            np.asarray(lst[0], dtype=np.int8),
            np.asarray(lst[1], dtype=np.int32),
            np.asarray(lst[2], dtype=np.float32),
            np.asarray(lst[3], dtype=np.float32),
        )
    return out


def draw_with_weight(rng, n_to_get, weights, drawn_local, chrom_idx, summits,
                     chrom_names, chrom_lens, tb):
    probs = weights / weights.sum()
    n_total = len(weights)
    seqs: list[str] = []
    batch = max(n_to_get + 1_000, int(n_to_get * 1.2))
    while len(seqs) < n_to_get:
        n_remaining = n_total - len(drawn_local)
        if n_remaining <= 0:
            break
        n_request = min(batch, n_remaining)
        idx = rng.choice(n_total, size=n_request, replace=False, p=probs)
        idx = [int(i) for i in idx if int(i) not in drawn_local]
        for i in idx:
            drawn_local.add(i)
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
        batch = 1_000
    return seqs[:n_to_get]


def main():
    t0 = time.time()
    print("Loading DHS Index ...", flush=True)
    by_comp = load_dhs_index()
    print(f"  {len(by_comp)} components:", flush=True)
    for comp in sorted(by_comp):
        print(f"    {comp:<28}  n={len(by_comp[comp][0]):>9,}", flush=True)

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    n_per_half = N_PER_COMP // 2  # 1562
    n_per_half_remainder = N_PER_COMP - n_per_half  # 1563 (one extra to signal)

    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        all_seqs: list[str] = []
        for comp in sorted(by_comp):
            chrom_idx, summits, signals, numsamples = by_comp[comp]
            drawn: set[int] = set()
            sig = draw_with_weight(rng, n_per_half_remainder, signals, drawn,
                                    chrom_idx, summits, chrom_names, chrom_lens, tb)
            bre = draw_with_weight(rng, n_per_half, numsamples, drawn,
                                    chrom_idx, summits, chrom_names, chrom_lens, tb)
            all_seqs.extend(sig)
            all_seqs.extend(bre)
        # Top up if any component fell short (shouldn't happen but be safe).
        if len(all_seqs) < N_TARGET:
            print(f"  seed={seed} short by {N_TARGET - len(all_seqs)} — "
                  f"padding from largest component", flush=True)
            largest = max(by_comp.items(), key=lambda kv: len(kv[1][0]))[0]
            chrom_idx, summits, signals, numsamples = by_comp[largest]
            extras = draw_with_weight(rng, N_TARGET - len(all_seqs),
                                      signals, set(),  # fresh draw
                                      chrom_idx, summits, chrom_names, chrom_lens, tb)
            all_seqs.extend(extras)
        all_seqs = all_seqs[:N_TARGET]
        rng.shuffle(all_seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(all_seqs) + "\n")
        print(f"seed={seed}: wrote {len(all_seqs):,} in "
              f"{time.time() - ts:.1f}s", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
