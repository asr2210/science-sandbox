"""Experiment 022: cCRE 013 with random-genomic flank.

Test whether flank's contribution (T17, ~+0.058) is cognate-content
(co-binding TFs, nucleosome positioning, cell-type-specific local
context) or just receptive-field scaffolding.

Build each 200bp sequence as:
  [50bp random hg38 main-chrom flank]
  [100bp cognate cCRE region centered on cCRE midpoint]
  [50bp random hg38 main-chrom flank]

Class composition matches 013: 10K each rare (PLS, CA-CTCF, CA-TF,
CA-H3K4me3) + 2.5K each abundant (pELS, dELS, CA, TF) = 50K.

Random flanks are drawn from main-chrom positions far enough from
the cCRE that overlap with cognate cCRE flank is statistically
negligible (>= 10kb away from any cCRE in the BED).
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
CCRE_REGION = 100  # cognate cCRE center segment
FLANK_LEN = (SEQ_LEN - CCRE_REGION) // 2  # 50bp each side
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


def load_cCREs():
    """Return ({class: [(chrom, mid)]}, {chrom: sorted [(start, end)]})."""
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
    """Load all main-chrom sequences into memory (uppercase, ~3 GB)."""
    seqs = {}
    for c in sorted(MAIN_CHROMS):
        print(f"  loading {c}...", flush=True)
        seqs[c] = tb[c][:].upper()
    return seqs


def overlaps_cCRE(chrom, s, e, starts_arr, ends_arr, pad=10_000):
    """Returns True if [s, e] is within `pad` bp of any cCRE on chrom."""
    if len(starts_arr) == 0:
        return False
    # Find first interval whose start > e + pad; everything before may overlap
    i = np.searchsorted(starts_arr, e + pad, side="right")
    # Check intervals up to i: any whose end >= s - pad overlaps
    if i == 0:
        return False
    # Look at the closest intervals (those with start <= e+pad)
    # An interval (a, b) overlaps iff b + pad >= s and a - pad <= e
    # Among intervals with a <= e+pad, we need any with b >= s-pad
    # Take the slice [0:i] and check max end >= s-pad — but only the "near" ones matter.
    # Use a precomputed running max of ends? Simpler: scan back from i-1 a few.
    # Conservative: check the 5 intervals nearest to s-e
    for k in range(max(0, i - 5), i):
        if ends_arr[k] + pad >= s:
            return True
    return False


def random_flank(rng, chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list):
    """Sample a FLANK_LEN-bp window from random main-chrom location, far from any cCRE."""
    while True:
        chrom = chrom_list[rng.integers(0, len(chrom_list))]
        L = chrom_lens[chrom]
        s = int(rng.integers(0, L - FLANK_LEN))
        e = s + FLANK_LEN
        if overlaps_cCRE(chrom, s, e, starts_by_chrom[chrom], ends_by_chrom[chrom]):
            continue
        return chrom, s, e


def clean_seq(raw, rng):
    return "".join(c if c in "ACGT" else ALPHABET[rng.integers(0, 4)] for c in raw)


def extract_chimeric(chrom_seqs, chrom, mid, rng,
                     chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list):
    """[50bp random] + [100bp cognate cCRE around mid] + [50bp random]."""
    cs = mid - CCRE_REGION // 2
    ce = mid + CCRE_REGION // 2
    L = chrom_lens[chrom]
    if cs < 0 or ce > L:
        return None
    cog_raw = chrom_seqs[chrom][cs:ce]
    if len(cog_raw) != CCRE_REGION:
        return None
    # Two independent random flanks
    lc, ls, le = random_flank(rng, chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list)
    rc, rs, re_ = random_flank(rng, chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list)
    lf_raw = chrom_seqs[lc][ls:le]
    rf_raw = chrom_seqs[rc][rs:re_]
    if len(lf_raw) != FLANK_LEN or len(rf_raw) != FLANK_LEN:
        return None
    return clean_seq(lf_raw + cog_raw + rf_raw, rng)


def generate(seed, by_cls, chrom_seqs, chrom_lens,
             starts_by_chrom, ends_by_chrom, chrom_list):
    rng = np.random.default_rng(seed)
    out = []
    for cls, n_take in CLASS_COUNTS.items():
        pool = by_cls[cls]
        n_draw = min(int(n_take * 1.05), len(pool))
        idx = rng.choice(len(pool), size=n_draw, replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract_chimeric(chrom_seqs, chrom, mid, rng,
                                   chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == n_take:
                    break
        assert added == n_take, f"{cls}: got {added}, want {n_take}"
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
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
