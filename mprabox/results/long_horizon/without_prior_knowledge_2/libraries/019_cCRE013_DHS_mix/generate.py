"""Experiment 019: cCRE 013 + filtered DHS (50/50 atlas mix).

25K from 013-style cCRE: 5K each rare (PLS, CA-CTCF, CA-TF, CA-H3K4me3)
+ 1.25K each abundant (pELS, dELS, CA, TF).
25K uniform from filtered DHS pool (mean_signal >= q75 AND numsamples
>= 5; ~681K elements; same filter as 009).

Tests whether DHS adds independent signal on top of cCRE.
"""
import gzip
import os
import numpy as np
import twobitreader
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BED = os.path.join(ROOT, "data", "cCRE", "ENCFF420VPZ.bed")
DHS = os.path.join(ROOT, "data", "DHS", "DHS_Index_hg38.txt.gz")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_SEQS = 50_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}
SIG_QUANTILE = 0.75
MIN_SAMPLES = 5

CCRE_COUNTS = {
    "PLS": 5_000, "CA-CTCF": 5_000, "CA-TF": 5_000, "CA-H3K4me3": 5_000,
    "pELS": 1_250, "dELS": 1_250, "CA": 1_250, "TF": 1_250,
}
N_CCRE = sum(CCRE_COUNTS.values())
N_DHS = N_SEQS - N_CCRE
assert N_CCRE == 25_000 and N_DHS == 25_000


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


def load_dhs_filtered():
    rows, sigs = [], []
    with gzip.open(DHS, "rt") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom = p[0]
            if chrom not in MAIN_CHROMS:
                continue
            sig = float(p[4])
            ns = int(p[5])
            summit = int(p[6])
            rows.append((chrom, summit, sig, ns))
            sigs.append(sig)
    sig_thresh = float(np.quantile(np.array(sigs), SIG_QUANTILE))
    filtered = [(c, s) for (c, s, sig, ns) in rows if sig >= sig_thresh and ns >= MIN_SAMPLES]
    return filtered, sig_thresh


def extract(tb, chrom, mid, rng):
    L = len(tb[chrom])
    s, e = mid - HALF, mid + HALF
    if s < 0 or e > L:
        return None
    seq = tb[chrom][s:e].upper()
    if len(seq) != SEQ_LEN:
        return None
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in seq)


def generate(seed, by_cls, dhs_pool, tb):
    rng = np.random.default_rng(seed)
    out = []
    # cCRE half (013-style scaled by 0.5)
    for cls, n_take in CCRE_COUNTS.items():
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
    # DHS half
    idx = rng.choice(len(dhs_pool), size=int(N_DHS * 1.05), replace=False)
    added = 0
    for j in idx:
        chrom, summit = dhs_pool[j]
        seq = extract(tb, chrom, summit, rng)
        if seq is not None:
            out.append(seq)
            added += 1
            if added == N_DHS:
                break
    assert added == N_DHS, f"DHS: got {added}, want {N_DHS}"
    rng.shuffle(out)
    return out


def main():
    print("loading cCREs by class...")
    by_cls = load_cCREs_by_class()
    for cls in CCRE_COUNTS:
        print(f"  {cls}: pool={len(by_cls[cls]):,}, take={CCRE_COUNTS[cls]:,}")
    print("loading + filtering DHS index...")
    dhs_pool, sig_thresh = load_dhs_filtered()
    print(f"  sig_thresh (q{SIG_QUANTILE})={sig_thresh:.3f}; filtered DHS pool={len(dhs_pool):,}; take={N_DHS:,}")
    tb = twobitreader.TwoBitFile(TWOBIT)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_cls, dhs_pool, tb)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
