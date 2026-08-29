"""Experiment 020: cCRE 013 scheme on width-filtered cCREs (no genomic flank).

013 takes 200bp centered on cCRE midpoint, so for cCREs <200bp wide
the extracted window includes flanking genomic context. This
experiment removes that contamination by:
  1. Filtering to cCREs >=200bp wide (~80% of cCREs in each class).
  2. Extracting the central 200bp = pure cCRE sequence, no flank.

Same 013 counts: 10K each rare (PLS, CA-CTCF, CA-TF, CA-H3K4me3),
2.5K each abundant (pELS, dELS, CA, TF). All classes have
>=23K width-filtered cCREs (smallest is CA-TF at 23,185).

Tests whether 013's gains come from the cCRE element itself or
from cCRE + flanking genomic context.
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
MIN_WIDTH = 200

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


def load_widthfilt_cCREs_by_class():
    """Return {class: [(chrom, mid)]} for cCREs >= MIN_WIDTH wide.

    The midpoint is used so that extract() takes the central 200bp,
    which lies entirely inside the cCRE element.
    """
    by_cls = defaultdict(list)
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end, cls = p[0], int(p[1]), int(p[2]), p[9]
            if chrom not in MAIN_CHROMS:
                continue
            if (end - start) < MIN_WIDTH:
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
    print(f"loading width-filtered cCREs (>={MIN_WIDTH}bp) by class...")
    by_cls = load_widthfilt_cCREs_by_class()
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
