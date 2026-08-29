"""Experiment 029: 022-style chimera with 160bp cognate + 20bp random flank each side.

Probe upper end of cognate-region gradient (T20). Test whether T24's
"chimeric design triggers eval_08 boost" effect kicks in even with
very small (20bp each) random flank.

Each 200bp sequence is built as:
  [20bp random hg38 main-chrom flank]
  [160bp cognate cCRE region centered on cCRE midpoint]
  [20bp random hg38 main-chrom flank]

013 class composition (10K rare + 2.5K abundant = 50K). Random flanks
from main-chrom positions >=10kb from any cCRE (same scaffold pool
as 022/023).

Branches:
- 029 mean >= 0.788 AND eval_08 > 0.73 → minimal-flank chimeric is
  the best of both; new top library
- 029 mean ~0.79 AND eval_08 ~0.71 → 20bp flank too small to trigger
  chimeric boost (gradient is smooth)
- 029 mean < 0.78 → cognate fraction effect sharper than expected
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
CCRE_REGION = 160  # cognate cCRE center segment
FLANK_LEN = (SEQ_LEN - CCRE_REGION) // 2  # 20bp each side
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


def random_flank(rng, chrom_lens, starts_by_chrom, ends_by_chrom, chrom_list):
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
