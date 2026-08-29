"""Experiment 027: 013 cCRE with DHS-quality filter.

Use 013 class composition (10K rare + 2.5K abundant), but only
sample cCREs that overlap a high-quality DHS:
  mean_signal >= q75 (across all DHSs) AND numsamples >= 5

Same DHS filter that gave 009 its lift over 008. Hypothesis:
ENCODE cCRE class assignment uses chromatin state but not signal
strength — many class-tagged cCREs may be weak. Filtering to
DHS-supported cCREs enriches for active regulatory units.

If a class loses too much pool size after filtering, fall back to
unfiltered for that class (with warning).
"""
import os
import gzip
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


def load_quality_dhs():
    """Load DHS Index, compute q75 of mean_signal, return high-quality intervals
    grouped by chrom and sorted by start."""
    print("loading DHS Index for q75 threshold...")
    signals = []
    rows = []
    with gzip.open(DHS, "rt") as f:
        header = f.readline()  # skip
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom = p[0]
            if chrom not in MAIN_CHROMS:
                continue
            start = int(p[1])
            end = int(p[2])
            mean_signal = float(p[4])
            numsamples = int(p[5])
            signals.append(mean_signal)
            rows.append((chrom, start, end, mean_signal, numsamples))
    q75 = np.quantile(signals, 0.75)
    print(f"  DHS q75 mean_signal = {q75:.4f}")
    by_chrom = defaultdict(list)
    kept = 0
    for chrom, start, end, ms, ns in rows:
        if ms >= q75 and ns >= 5:
            by_chrom[chrom].append((start, end))
            kept += 1
    print(f"  high-quality DHSs: {kept:,} / {len(rows):,}")
    for c in by_chrom:
        by_chrom[c].sort()
    return by_chrom


def load_cCREs():
    """Return per-class list of (chrom, start, end, mid)."""
    by_cls = defaultdict(list)
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom, start, end, cls = p[0], int(p[1]), int(p[2]), p[9]
            if chrom not in MAIN_CHROMS:
                continue
            mid = (start + end) // 2
            by_cls[cls].append((chrom, start, end, mid))
    return by_cls


def overlaps_quality_dhs(chrom, s, e, dhs_starts, dhs_ends):
    """True if [s, e] overlaps any quality DHS."""
    if len(dhs_starts) == 0:
        return False
    # any DHS with start <= e AND end >= s
    i = np.searchsorted(dhs_starts, e, side="right")
    if i == 0:
        return False
    # Check intervals 0..i-1 ; for overlap, need end >= s
    # Limit scan to last few (DHSs are tiny so a binary search on end is needed
    # for full safety, but DHSs are <1kb and cCREs are <1kb, so the maximum
    # gap is small; check a 50-back window)
    for k in range(max(0, i - 50), i):
        if dhs_ends[k] >= s:
            return True
    return False


def filter_class(pool, dhs_by_chrom_arrays):
    """Keep only cCREs that overlap a high-quality DHS."""
    out = []
    for chrom, start, end, mid in pool:
        ds, de = dhs_by_chrom_arrays.get(chrom, (np.array([]), np.array([])))
        if overlaps_quality_dhs(chrom, start, end, ds, de):
            out.append((chrom, mid))
    return out


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


def generate(seed, by_cls_filtered, by_cls_unfiltered, chrom_seqs):
    rng = np.random.default_rng(seed)
    out = []
    for cls, n_take in CLASS_COUNTS.items():
        pool = by_cls_filtered[cls]
        # If filtered pool too small, fall back
        if len(pool) < n_take * 1.05:
            print(f"  WARN {cls}: filtered pool {len(pool):,} < target {n_take:,}, "
                  f"falling back to unfiltered ({len(by_cls_unfiltered[cls]):,})")
            pool = [(c, m) for c, _, _, m in by_cls_unfiltered[cls]]
        n_draw = min(int(n_take * 1.05), len(pool))
        idx = rng.choice(len(pool), size=n_draw, replace=False)
        added = 0
        for j in idx:
            chrom, mid = pool[j]
            seq = extract_full(chrom_seqs, chrom, mid, rng)
            if seq is not None:
                out.append(seq)
                added += 1
                if added == n_take:
                    break
        assert added == n_take, f"{cls}: got {added}, want {n_take}"
    rng.shuffle(out)
    return out


def main():
    dhs_by_chrom = load_quality_dhs()
    dhs_arrays = {c: (np.array([s for s, _ in iv], dtype=np.int64),
                      np.array([e for _, e in iv], dtype=np.int64))
                  for c, iv in dhs_by_chrom.items()}
    print("loading cCREs...")
    by_cls_unfiltered = load_cCREs()
    print("filtering cCREs by DHS-quality overlap...")
    by_cls_filtered = {}
    for cls in CLASS_COUNTS:
        kept = filter_class(by_cls_unfiltered[cls], dhs_arrays)
        by_cls_filtered[cls] = kept
        print(f"  {cls}: {len(by_cls_unfiltered[cls]):,} -> {len(kept):,} "
              f"(target {CLASS_COUNTS[cls]:,})")
    print("loading hg38 main chromosomes into memory...")
    tb = twobitreader.TwoBitFile(TWOBIT)
    chrom_seqs = load_chrom_seqs(tb)
    for seed in (0, 1, 2):
        print(f"seed {seed}...")
        seqs = generate(seed, by_cls_filtered, by_cls_unfiltered, chrom_seqs)
        out_path = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out_path, "w") as f:
            f.write("\n".join(seqs) + "\n")
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:200])
        print(f"  wrote {out_path}")


if __name__ == "__main__":
    main()
