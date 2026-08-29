"""Experiment 006: cCREs stratified by class (equal counts).

Equal counts (~6,250) from each of the 8 ENCODE V4 cCRE classes:
PLS, pELS, dELS, CA-CTCF, CA-H3K4me3, CA-TF, CA, TF. Total = 50K.
200bp windows centered on midpoint, same extraction as 002.

Tests whether explicit class diversity beats natural-distribution
cCRE sampling (002, dELS-dominated 63%).
"""
import os
import sys
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

CLASSES = ["PLS", "pELS", "dELS", "CA-CTCF", "CA-H3K4me3", "CA-TF", "CA", "TF"]


def load_cCREs_by_class():
    by_cls = defaultdict(list)
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end = p[0], int(p[1]), int(p[2])
            cls = p[9]
            if chrom not in MAIN_CHROMS:
                continue
            mid = (start + end) // 2
            by_cls[cls].append((chrom, mid))
    return by_cls


def extract(tb, chrom, mid, rng):
    chrom_len = len(tb[chrom])
    start = mid - HALF
    end = mid + HALF
    if start < 0 or end > chrom_len:
        return None
    seq = tb[chrom][start:end].upper()
    if len(seq) != SEQ_LEN:
        return None
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in seq)


def generate(seed, by_cls, tb):
    rng = np.random.default_rng(seed)
    per_class = N_SEQS // len(CLASSES)  # 6,250
    remainder = N_SEQS - per_class * len(CLASSES)  # 0
    out = []
    for i, cls in enumerate(CLASSES):
        target = per_class + (1 if i < remainder else 0)
        oversample = int(target * 1.05)
        pool = by_cls[cls]
        idx = rng.choice(len(pool), size=min(oversample, len(pool)), replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract(tb, chrom, mid, rng)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == target:
                    break
        if added < target:
            raise RuntimeError(f"class {cls}: only {added}/{target}")
    if len(out) != N_SEQS:
        raise RuntimeError(f"got {len(out)} != {N_SEQS}")
    rng.shuffle(out)  # avoid block ordering by class
    return out


def main():
    print("loading cCREs by class...")
    by_cls = load_cCREs_by_class()
    for c in CLASSES:
        print(f"  {c}: {len(by_cls[c]):,}")
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
