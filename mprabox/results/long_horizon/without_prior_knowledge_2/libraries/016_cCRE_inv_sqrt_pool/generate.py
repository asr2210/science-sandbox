"""Experiment 016: per-class counts proportional to 1/sqrt(pool_size).

Principled refinement of 013. Uses w_i = 1/sqrt(pool_i), normalized to
sum to 50,000.

Counts (rounded, then balanced to sum=50K):
PLS=9400, CA-CTCF=5700, CA-TF=12600, CA-H3K4me3=7300,
pELS=4100, dELS=1700, CA=4100, TF=6300  → sum=50200, scale to 50000.

Tests whether class info-density follows 1/sqrt(pool) law (T10/T8).
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
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

# Pool sizes from prior runs
POOLS = {
    "PLS": 47_532,
    "CA-CTCF": 126_034,
    "CA-TF": 26_102,
    "CA-H3K4me3": 79_246,
    "pELS": 249_464,
    "dELS": 1_469_205,
    "CA": 245_985,
    "TF": 105_286,
}


def compute_counts():
    raw = {c: 1.0 / np.sqrt(n) for c, n in POOLS.items()}
    s = sum(raw.values())
    counts = {c: int(round(N_SEQS * raw[c] / s)) for c in POOLS}
    diff = N_SEQS - sum(counts.values())
    # adjust the largest count to absorb rounding
    max_c = max(counts, key=counts.get)
    counts[max_c] += diff
    assert sum(counts.values()) == N_SEQS
    return counts


CLASS_COUNTS = compute_counts()


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


def extract(tb, chrom, mid, rng):
    L = len(tb[chrom])
    s, e = mid - HALF, mid + HALF
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
            seq = extract(tb, chrom, mid, rng)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == n_take:
                    break
        assert added == n_take, f"{cls}: got {added}, want {n_take}"
    rng.shuffle(out)
    return out


def main():
    print("computed 1/sqrt(pool) per-class counts:")
    for c, n in CLASS_COUNTS.items():
        print(f"  {c}: pool={POOLS[c]:,}, take={n:,}")
    by_cls = load_cCREs_by_class()
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
