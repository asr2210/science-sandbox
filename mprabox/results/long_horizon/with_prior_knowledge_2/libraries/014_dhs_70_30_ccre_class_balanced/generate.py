"""Experiment 014 — dhs_70_30_ccre_class_balanced.

Lock the 70/30 ratio from 011 and introduce a NEW lever: enforce
equal representation of {PLS, pELS, dELS} ENCODE cCRE functional
classes inside the signal-weighted half. Tests whether regulatory-
class balance is an orthogonal dimension to mean_signal+numsamples.

Design:
- 35K signal-weighted DHS, but split 11,667 from each of PLS, pELS,
  dELS (signal-weighted within each class subset).
- 15K numsamples-weighted DHS from the cCRE-overlapping universe
  (no class stratification — keep the lever isolated to the
  signal half).
"""

import gzip
import os
import time

import numpy as np
import twobitreader

DATA_DIR = "/data/users/arao/mpra_autoresearch/data"
DHS_PATH = f"{DATA_DIR}/dhs/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz"
GENOME_PATH = f"{DATA_DIR}/genome/hg38.2bit"
CCRE_CLASS_PATH = f"{DATA_DIR}/cCRE/dhs_ccre_class.npy"

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
N_TARGET = 50_000
N_SIGNAL = 35_000
N_BREADTH = N_TARGET - N_SIGNAL  # 15,000
N_PER_CLASS = N_SIGNAL // 3  # 11,666 — last class gets +2 to hit 35K
CLASSES = ("PLS", "pELS", "dELS")
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

    print("Loading cCRE class assignments ...", flush=True)
    ccre_class = np.load(CCRE_CLASS_PATH, allow_pickle=True)
    assert len(ccre_class) == len(chrom_idx), \
        f"cCRE class array length {len(ccre_class)} != DHS rows {len(chrom_idx)}"

    class_idx = {cls: np.where(ccre_class == cls)[0] for cls in CLASSES}
    ccre_any_idx = np.where(ccre_class != "none")[0]
    for cls in CLASSES:
        print(f"  {cls}: {len(class_idx[cls]):,} candidates", flush=True)
    print(f"  any cCRE: {len(ccre_any_idx):,} candidates", flush=True)

    tb = twobitreader.TwoBitFile(GENOME_PATH)
    chrom_names = sorted(VALID_CHROMS)
    chrom_lens = {c: len(tb[c]) for c in chrom_names}

    for seed in range(N_SEEDS):
        ts = time.time()
        rng = np.random.default_rng(seed)
        drawn: set[int] = set()
        seqs: list[str] = []

        # Signal half: equal counts per cCRE class, signal-weighted within class.
        # Last class gets the remainder so totals hit N_SIGNAL exactly.
        per_class = [N_PER_CLASS, N_PER_CLASS, N_SIGNAL - 2 * N_PER_CLASS]
        cls_order = list(zip(CLASSES, per_class))
        rng.shuffle(cls_order)
        for cls, n in cls_order:
            part = draw_with_weight(
                rng, n, class_idx[cls], signals, drawn,
                chrom_idx, summits, chrom_names, chrom_lens, tb,
            )
            seqs.extend(part)

        # Breadth half: numsamples-weighted across cCRE-overlapping DHS.
        breadth = draw_with_weight(
            rng, N_BREADTH, ccre_any_idx, numsamples, drawn,
            chrom_idx, summits, chrom_names, chrom_lens, tb,
        )
        seqs.extend(breadth)

        rng.shuffle(seqs)
        out = os.path.join(OUT_DIR, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        print(f"seed={seed}: cls_order={[c for c,_ in cls_order]} "
              f"wrote {len(seqs):,} in {time.time() - ts:.1f}s", flush=True)
    print(f"Done in {time.time() - t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
