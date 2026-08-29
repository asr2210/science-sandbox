"""Experiment 021: cCRE 013 with off-center extraction.

013 places the cCRE midpoint exactly at the window center (offset
100bp from each edge). Models trained this way may overfit to
position. 021 keeps 013's class counts but randomly off-centers the
window: the cCRE midpoint sits at a uniformly random position within
the window's central +-50bp, i.e. extraction window is shifted by
[-50, +50] bp from the cCRE midpoint.

Tests whether positional jitter forces position-invariant feature
learning (helps generalization) or removes a useful inductive prior
(hurts).
"""
import os
import numpy as np
import twobitreader
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BED = os.path.join(ROOT, "data", "cCRE", "ENCFF420VPZ.bed")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
MAX_OFFSET = 50  # cCRE midpoint can sit at window-center +- this many bp
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

CLASS_COUNTS = {
    "PLS": 10_000,
    "CA-CTCF": 10_000,
    "CA-TF": 10_000,
    "CA-H3K4me3": 10_000,
    "pELS": 2_500,
    "dELS": 2_500,
    "CA": 2_500,
    "TF": 2_500,
}
assert sum(CLASS_COUNTS.values()) == N_SEQS


def load_cCREs_by_class():
    by_cls = defaultdict(list)
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end, cls = p[0], int(p[1]), int(p[2]), p[9]
            if chrom not in MAIN_CHROMS:
                continue
            mid = (start + end) // 2
            by_cls[cls].append((chrom, mid))
    return by_cls


def extract_offcenter(tb, chrom, mid, rng):
    """Extract 200bp window around mid, with mid at window-center +- MAX_OFFSET."""
    L = len(tb[chrom])
    # Shift the window so cCRE mid is at random position [center-50, center+50].
    # window_center = mid - shift; window spans [mid - shift - HALF, mid - shift + HALF].
    shift = int(rng.integers(-MAX_OFFSET, MAX_OFFSET + 1))
    s = mid - shift - HALF
    e = mid - shift + HALF
    if s < 0 or e > L:
        return None
    seq = tb[chrom][s:e].upper()
    if len(seq) != SEQ_LEN:
        return None
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in seq)


def generate(seed, by_cls, tb):
    rng = np.random.default_rng(seed)
    out = []
    for cls, n_take in CLASS_COUNTS.items():
        pool = by_cls[cls]
        n_draw = min(int(n_take * 1.05), len(pool))
        idx = rng.choice(len(pool), size=n_draw, replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract_offcenter(tb, chrom, mid, rng)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == n_take:
                    break
        assert added == n_take, f"{cls}: got {added}, want {n_take}"
    rng.shuffle(out)
    return out


def main():
    print("loading cCREs by class...")
    by_cls = load_cCREs_by_class()
    for cls in CLASS_COUNTS:
        print(f"  {cls}: pool={len(by_cls[cls]):,}, take={CLASS_COUNTS[cls]:,}")
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_cls, tb)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
