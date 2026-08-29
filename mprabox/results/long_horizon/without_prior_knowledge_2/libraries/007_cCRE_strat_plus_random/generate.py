"""Experiment 007: stratified cCREs (40K) + uniform random (10K) mix.

40,000 stratified-cCRE sequences (5,000 per class x 8 classes) + 10,000
uniform random 200bp sequences. Tests whether mixing in random recovers
the eval_08 coverage hole while keeping cCRE gains.

Class counts: 5,000 each from PLS, pELS, dELS, CA-CTCF, CA-H3K4me3,
CA-TF, CA, TF (= 40K cCREs).
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
N_RANDOM = 10_000
N_PER_CLASS = (N_SEQS - N_RANDOM) // 8  # 5,000
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


def random_seq(rng):
    return "".join(ALPHABET[rng.integers(0, 4, size=SEQ_LEN)])


def generate(seed, by_cls, tb):
    rng = np.random.default_rng(seed)
    out = []
    for cls in CLASSES:
        pool = by_cls[cls]
        idx = rng.choice(len(pool), size=int(N_PER_CLASS * 1.05), replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract(tb, chrom, mid, rng)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == N_PER_CLASS:
                    break
        assert added == N_PER_CLASS
    for _ in range(N_RANDOM):
        out.append(random_seq(rng))
    rng.shuffle(out)
    return out


def main():
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
