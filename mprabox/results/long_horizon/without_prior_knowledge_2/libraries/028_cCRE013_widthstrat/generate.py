"""Experiment 028: 013 cCRE with width-quartile stratification within each class.

Use 013 class composition (10K rare + 2.5K abundant). Within each
class, divide cCREs into 4 width quartiles by (end - start). Sample
n_take/4 from each quartile uniformly. Forces width-breadth within
each class.

Hypothesis: cCRE width may carry information orthogonal to class
(narrow vs broad regulatory regions). 013 samples uniformly from
class pool — if a class is dominated by narrow cCREs, the model
sees mostly narrow. Width-stratifying exposes the model to all
width regimes equally within each class.

Counter-evidence from 020 (width-FILTER >=200bp lost 0.058) was
attributed to selection bias — sampling ALL width quartiles is
fundamentally different from filtering away narrow ones.
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
N_QUARTILES = 4
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

CLASS_COUNTS = {
    "PLS":         10_000,
    "CA-CTCF":     10_000,
    "CA-TF":       10_000,
    "CA-H3K4me3":  10_000,
    "pELS":         2_500,
    "dELS":         2_500,
    "CA":           2_500,
    "TF":           2_500,
}
assert sum(CLASS_COUNTS.values()) == N_SEQS


def load_cCREs_with_width():
    """Return per-class list of (chrom, mid, width)."""
    by_cls = defaultdict(list)
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end, cls = p[0], int(p[1]), int(p[2]), p[9]
            if chrom not in MAIN_CHROMS:
                continue
            mid = (start + end) // 2
            width = end - start
            by_cls[cls].append((chrom, mid, width))
    return by_cls


def split_into_quartiles(pool):
    """Sort by width and split into N_QUARTILES equal slices."""
    pool_sorted = sorted(pool, key=lambda t: t[2])
    n = len(pool_sorted)
    quartiles = []
    for q in range(N_QUARTILES):
        s = (n * q) // N_QUARTILES
        e = (n * (q + 1)) // N_QUARTILES
        quartiles.append([(c, m) for c, m, _ in pool_sorted[s:e]])
    return quartiles


def load_chrom_seqs(tb):
    seqs = {}
    for c in sorted(MAIN_CHROMS):
        print(f"  loading {c}...", flush=True)
        seqs[c] = tb[c][:].upper()
    return seqs


def clean_seq(raw, rng):
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in raw)


def extract_full(chrom_seqs, chrom, mid, rng):
    s = mid - HALF
    e = mid + HALF
    L = len(chrom_seqs[chrom])
    if s < 0 or e > L:
        return None
    raw = chrom_seqs[chrom][s:e]
    if len(raw) != SEQ_LEN:
        return None
    return clean_seq(raw, rng)


def generate(seed, by_cls_quartiles, chrom_seqs):
    rng = np.random.default_rng(seed)
    out = []
    for cls, n_take in CLASS_COUNTS.items():
        quartiles = by_cls_quartiles[cls]
        # Allocate counts: floor + remainder distributed
        per_q = n_take // N_QUARTILES
        remainder = n_take - per_q * N_QUARTILES
        counts = [per_q + (1 if q < remainder else 0) for q in range(N_QUARTILES)]
        for q_idx, (q_pool, q_take) in enumerate(zip(quartiles, counts)):
            n_draw = min(int(q_take * 1.05), len(q_pool))
            idx = rng.choice(len(q_pool), size=n_draw, replace=False)
            added = 0
            for j in idx:
                chrom, mid = q_pool[j]
                seq = extract_full(chrom_seqs, chrom, mid, rng)
                if seq is not None:
                    out.append(seq)
                    added += 1
                    if added == q_take:
                        break
            assert added == q_take, f"{cls} q{q_idx}: got {added}, want {q_take}"
    rng.shuffle(out)
    return out


def main():
    print("loading cCREs...")
    by_cls = load_cCREs_with_width()
    by_cls_quartiles = {}
    for cls in CLASS_COUNTS:
        quartiles = split_into_quartiles(by_cls[cls])
        by_cls_quartiles[cls] = quartiles
        sizes = [len(q) for q in quartiles]
        widths = [(by_cls[cls][0][2] if not q else None,) for q in quartiles]
        # Print width range per quartile
        sorted_widths = sorted([w for _, _, w in by_cls[cls]])
        n = len(sorted_widths)
        ranges = []
        for q in range(N_QUARTILES):
            s = (n * q) // N_QUARTILES
            e = (n * (q + 1)) // N_QUARTILES - 1
            ranges.append(f"{sorted_widths[s]}-{sorted_widths[e]}")
        print(f"  {cls}: pool={n:,}, q-sizes={sizes}, ranges={ranges}")
    print("loading hg38 main chromosomes into memory...")
    tb = twobitreader.TwoBitFile(TWOBIT)
    chrom_seqs = load_chrom_seqs(tb)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_cls_quartiles, chrom_seqs)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
