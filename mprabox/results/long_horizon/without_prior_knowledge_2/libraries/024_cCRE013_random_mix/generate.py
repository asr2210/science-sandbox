"""Experiment 024: 013 cCRE 80% + 20% uniform random hg38 mix.

T21 from 023: random-flank libraries gain a lot on eval_08 (+0.05 to
+0.06 vs 013) — eval_08 likely tests broader-coverage sequence.
Test whether mixing 20% pure-random hg38 windows into a 013-style
cCRE library gives that eval_08 boost without sacrificing the
cCRE-strong evals.

Library composition (50K total):
- 40K cCRE (013 recipe scaled 80%): 8K each rare + 2K each abundant
- 10K uniform random hg38 main-chrom 200bp windows >=10kb from any cCRE

Random windows drawn from same scaffold pool as 022/023 flanks.
Final library shuffled together.

Branches:
- 024 mean > 013 (0.7900) → mixing wins; tune ratio in 025
- 024 mean ≈ 013, eval_08 strongly up → tradeoff confirmed
- 024 mean < 013, eval_08 only marginally up → abandon mix
"""
import os
import numpy as np
import twobitreader
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BED = os.path.join(ROOT, "data", "cCRE", "ENCFF420VPZ.bed")
TWOBIT = os.path.join(ROOT, "data", "genome", "hg38.2bit")

N_TOTAL = 50_000
N_CCRE = 40_000
N_RAND = 10_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

# 013 recipe scaled to 40K (factor 0.8)
CLASS_COUNTS = {
    "PLS":         8_000,
    "CA-CTCF":     8_000,
    "CA-TF":       8_000,
    "CA-H3K4me3":  8_000,
    "pELS":        2_000,
    "dELS":        2_000,
    "CA":          2_000,
    "TF":          2_000,
}
assert sum(CLASS_COUNTS.values()) == N_CCRE


def load_cCREs():
    by_cls = defaultdict(list)
    intervals = defaultdict(list)
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end, cls = p[0], int(p[1]), int(p[2]), p[9]
            if chrom not in MAIN_CHROMS:
                continue
            mid = (start + end) // 2
            by_cls[cls].append((chrom, mid))
            intervals[chrom].append((start, end))
    for c in intervals:
        intervals[c].sort()
    return by_cls, intervals


def load_chrom_seqs(tb):
    seqs = {}
    for c in sorted(MAIN_CHROMS):
        print(f"  loading {c}...", flush=True)
        seqs[c] = tb[c][:].upper()
    return seqs


def overlaps_cCRE(chrom, s, e, starts_arr, ends_arr, pad=10_000):
    if len(starts_arr) == 0:
        return False
    i = np.searchsorted(starts_arr, e + pad, side="right")
    if i == 0:
        return False
    for k in range(max(0, i - 5), i):
        if ends_arr[k] + pad >= s:
            return True
    return False


def clean_seq(raw, rng):
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in raw)


def extract_cCRE(chrom_seqs, chrom, mid, rng):
    s = mid - HALF
    e = mid + HALF
    L = len(chrom_seqs[chrom])
    if s < 0 or e > L:
        return None
    raw = chrom_seqs[chrom][s:e]
    if len(raw) != SEQ_LEN:
        return None
    return clean_seq(raw, rng)


def random_window(rng, chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list,
                  chrom_seqs):
    """200bp random main-chrom window, >=10kb from any cCRE."""
    while True:
        chrom = chrom_list[rng.integers(0, len(chrom_list))]
        L = chrom_lens[chrom]
        s = int(rng.integers(0, L - SEQ_LEN))
        e = s + SEQ_LEN
        if overlaps_cCRE(chrom, s, e, starts_by_chrom[chrom], ends_by_chrom[chrom]):
            continue
        raw = chrom_seqs[chrom][s:e]
        if len(raw) != SEQ_LEN:
            continue
        return clean_seq(raw, rng)


def generate(seed, by_cls, chrom_seqs, chrom_lens,
             starts_by_chrom, ends_by_chrom, chrom_list):
    rng = np.random.default_rng(seed)
    out = []
    # 40K cCRE
    for cls, n_take in CLASS_COUNTS.items():
        pool = by_cls[cls]
        n_draw = min(int(n_take * 1.05), len(pool))
        idx = rng.choice(len(pool), size=n_draw, replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract_cCRE(chrom_seqs, chrom, mid, rng)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == n_take:
                    break
        assert added == n_take, f"{cls}: got {added}, want {n_take}"
    assert len(out) == N_CCRE
    # 10K random
    for _ in range(N_RAND):
        out.append(random_window(rng, chrom_lens, starts_by_chrom,
                                 ends_by_chrom, chrom_list, chrom_seqs))
    rng.shuffle(out)
    return out


def main():
    print("loading cCREs...")
    by_cls, intervals = load_cCREs()
    for cls in CLASS_COUNTS:
        print(f"  {cls}: pool={len(by_cls[cls]):,}, take={CLASS_COUNTS[cls]:,}")
    starts_by_chrom = {c: np.array([a for a, _ in iv], dtype=np.int64)
                       for c, iv in intervals.items()}
    ends_by_chrom = {c: np.array([b for _, b in iv], dtype=np.int64)
                     for c, iv in intervals.items()}
    print("loading hg38 main chromosomes into memory...")
    tb = twobitreader.TwoBitFile(TWOBIT)
    chrom_seqs = load_chrom_seqs(tb)
    chrom_lens = {c: len(s) for c, s in chrom_seqs.items()}
    chrom_list = sorted(MAIN_CHROMS)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_cls, chrom_seqs, chrom_lens,
                        starts_by_chrom, ends_by_chrom, chrom_list)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_TOTAL
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
