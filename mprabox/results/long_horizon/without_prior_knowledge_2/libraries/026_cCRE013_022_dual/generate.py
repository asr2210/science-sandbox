"""Experiment 026: dual library = 25K (013-style) + 25K (022-style chimeric).

T22 from 024 said label-divergent mixing (cCRE + pure random) hurts.
But 022's eval_08 boost (+0.049) is real and comes from the chimeric
design (cCRE peak in random flank). Test if mixing two cCRE-anchored
designs preserves the eval_08 lift without 024's dilution penalty.

Library composition:
- 25K full 200bp cCRE windows centered on midpoint (013 design,
  scaled to 25K: 5K each rare + 1.25K each abundant)
- 25K chimeric: 100bp cCRE region + 50bp random hg38 flank each side
  (022 design, scaled to 25K, same per-class counts)

Both halves draw cCREs independently from full pool (sampling without
replacement within each half — overlap between halves possible).
Final library shuffled.

Branches:
- 026 mean > 013 (>0.7905), eval_08 > 0.73 → bridges; new alt-best
- 026 ≈ 022 → chimeric character dominates; eval_08 lift but small
- 026 < 013 by 0.005+ → even cCRE-anchored mixing hurts; rule out
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
N_PER_HALF = 25_000
SEQ_LEN = 200
HALF = SEQ_LEN // 2
CCRE_REGION = 100  # 022 design
FLANK_LEN = (SEQ_LEN - CCRE_REGION) // 2  # 50bp each side
ALPHABET = np.array(list("ACGT"))
MAIN_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY"}

# 013 recipe scaled to 25K (factor 0.5)
CLASS_COUNTS = {
    "PLS":         5_000,
    "CA-CTCF":     5_000,
    "CA-TF":       5_000,
    "CA-H3K4me3":  5_000,
    "pELS":        1_250,
    "dELS":        1_250,
    "CA":          1_250,
    "TF":          1_250,
}
assert sum(CLASS_COUNTS.values()) == N_PER_HALF


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


def random_flank(rng, chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list):
    while True:
        chrom = chrom_list[rng.integers(0, len(chrom_list))]
        L = chrom_lens[chrom]
        s = int(rng.integers(0, L - FLANK_LEN))
        e = s + FLANK_LEN
        if overlaps_cCRE(chrom, s, e, starts_by_chrom[chrom], ends_by_chrom[chrom]):
            continue
        return chrom, s, e


def extract_full(chrom_seqs, chrom, mid, rng):
    """013-style: 200bp centered on cCRE midpoint."""
    s = mid - HALF
    e = mid + HALF
    L = len(chrom_seqs[chrom])
    if s < 0 or e > L:
        return None
    raw = chrom_seqs[chrom][s:e]
    if len(raw) != SEQ_LEN:
        return None
    return clean_seq(raw, rng)


def extract_chimeric(chrom_seqs, chrom, mid, rng,
                     chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list):
    """022-style: 50bp random + 100bp cognate cCRE + 50bp random."""
    cs = mid - CCRE_REGION // 2
    ce = mid + CCRE_REGION // 2
    L = chrom_lens[chrom]
    if cs < 0 or ce > L:
        return None
    cog_raw = chrom_seqs[chrom][cs:ce]
    if len(cog_raw) != CCRE_REGION:
        return None
    lc, ls, le = random_flank(rng, chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list)
    rc, rs, re_ = random_flank(rng, chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list)
    lf_raw = chrom_seqs[lc][ls:le]
    rf_raw = chrom_seqs[rc][rs:re_]
    if len(lf_raw) != FLANK_LEN or len(rf_raw) != FLANK_LEN:
        return None
    return clean_seq(lf_raw + cog_raw + rf_raw, rng)


def fill_class(extractor, cls, n_take, pool, rng):
    n_draw = min(int(n_take * 1.05), len(pool))
    idx = rng.choice(len(pool), size=n_draw, replace=False)
    out = []
    for j in idx:
        chrom, mid = pool[j]
        seq = extractor(chrom, mid)
        if seq is not None:
            out.append(seq)
            if len(out) == n_take:
                return out
    raise RuntimeError(f"{cls}: only got {len(out)}/{n_take}")


def generate(seed, by_cls, chrom_seqs, chrom_lens,
             starts_by_chrom, ends_by_chrom, chrom_list):
    rng = np.random.default_rng(seed)
    out = []
    # Half 1: full 200bp cCRE windows (013 style)
    for cls, n_take in CLASS_COUNTS.items():
        out.extend(fill_class(
            lambda c, m: extract_full(chrom_seqs, c, m, rng),
            cls, n_take, by_cls[cls], rng,
        ))
    assert len(out) == N_PER_HALF
    # Half 2: chimeric 100bp cCRE + 50bp random flanks each side (022 style)
    for cls, n_take in CLASS_COUNTS.items():
        out.extend(fill_class(
            lambda c, m: extract_chimeric(chrom_seqs, c, m, rng,
                                          chrom_lens, starts_by_chrom,
                                          ends_by_chrom, chrom_list),
            cls, n_take, by_cls[cls], rng,
        ))
    assert len(out) == N_TOTAL
    rng.shuffle(out)
    return out


def main():
    print("loading cCREs...")
    by_cls, intervals = load_cCREs()
    for cls in CLASS_COUNTS:
        print(f"  {cls}: pool={len(by_cls[cls]):,}, take_each_half={CLASS_COUNTS[cls]:,}")
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
