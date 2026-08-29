"""
Experiment 011 — stratified cCRE positives + paired flanking negatives.

Composition (50K total):
- 25,000 stratified cCRE-centered positives: 5K each of PLS, pELS,
  dELS, CTCF-only, DNase-H3K4me3.
- 25,000 paired flanks: one per cCRE positive, 200bp window shifted
  ±1500-3000bp from the same cCRE midpoint, rejected if it overlaps
  any annotated cCRE.

Hypothesis: combine the two winning ideas:
- 008 (stratified positives) helped enhancer evals (06/11).
- 010 (paired flanking negatives) helped general evals and K562.
If the two stack additively, 011 > 010 (>0.158).

If 011 ~= 010, the two ideas address overlapping signal: the model
already gets enough type diversity from 010's natural cCRE distribution.

If 011 < 010, stratification reduces dELS density too much (only 5K
dELS vs 010's ~20K dELS, since natural cCRE distribution is dELS-heavy).
"""
import os, time, numpy as np
from collections import defaultdict

L = 200
HALF = L // 2
FLANK_MIN = 1500
FLANK_MAX = 3000
SEED = 0

CCRE_BUDGET = {
    "PLS":   5_000,
    "pELS":  5_000,
    "dELS":  5_000,
    "CTCF":  5_000,
    "DNH3":  5_000,
}
N_SEQ = 2 * sum(CCRE_BUDGET.values())
assert N_SEQ == 50_000

def classify(type_str):
    parts = set(t.strip() for t in type_str.split(","))
    if "PLS" in parts: return "PLS"
    if "pELS" in parts: return "pELS"
    if "dELS" in parts: return "dELS"
    if "DNase-H3K4me3" in parts: return "DNH3"
    if "CTCF-only" in parts: return "CTCF"
    return None

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    cache_dir = os.path.join(repo_root, "data", "hg38_npy")
    bed_path = os.path.join(repo_root, "data", "GRCh38-cCREs.bed")
    t0 = time.time()

    genome, n_prefix = {}, {}
    for f in sorted(os.listdir(cache_dir)):
        if f.endswith(".npy"):
            c = f[:-4]
            mat = np.asarray(np.load(os.path.join(cache_dir, f), mmap_mode="r"))
            genome[c] = mat
            is_n = (mat == ord("N")).astype(np.int32)
            n_prefix[c] = np.concatenate(([0], np.cumsum(is_n)))
    chroms = sorted(genome.keys())
    print(f"genome+prefix in {time.time()-t0:.1f}s")
    bases = set("ACGT")
    rng = np.random.default_rng(SEED)

    # Bucket cCREs by type AND build per-chr interval list for overlap check.
    buckets = defaultdict(list)
    ccre_intervals = {c: [] for c in chroms}
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in genome:
                continue
            s, e = int(parts[1]), int(parts[2])
            ccre_intervals[c].append((s, e))
            bk = classify(parts[5])
            if bk is not None:
                mid = (s + e) // 2
                buckets[bk].append((c, mid))
    for c in chroms:
        ccre_intervals[c].sort()
    print("bucket sizes:", {k: len(v) for k, v in buckets.items()})
    print(f"  cCREs loaded, {time.time()-t0:.1f}s")

    def overlaps_ccre(chrom, start, end):
        intervals = ccre_intervals[chrom]
        lo, hi = 0, len(intervals)
        while lo < hi:
            m = (lo + hi) // 2
            if intervals[m][0] < end:
                lo = m + 1
            else:
                hi = m
        for k in range(max(0, lo - 2), min(len(intervals), lo + 1)):
            s2, e2 = intervals[k]
            if s2 < end and start < e2:
                return True
        return False

    positives, flanks = [], []
    bucket_counts = {}
    for bk, need in CCRE_BUDGET.items():
        items = buckets[bk]
        order = rng.permutation(len(items))
        kept = 0
        idx = 0
        while kept < need and idx < len(order):
            c, mid = items[order[idx]]
            idx += 1
            p_start = mid - HALF
            if p_start < 0 or p_start + L > len(genome[c]):
                continue
            if n_prefix[c][p_start + L] - n_prefix[c][p_start] != 0:
                continue
            # try to find paired flank
            flank_found = None
            for _ in range(8):
                sign = 1 if rng.random() < 0.5 else -1
                offset = sign * rng.integers(FLANK_MIN, FLANK_MAX + 1)
                f_start = mid + int(offset) - HALF
                if f_start < 0 or f_start + L > len(genome[c]):
                    continue
                if n_prefix[c][f_start + L] - n_prefix[c][f_start] != 0:
                    continue
                if overlaps_ccre(c, f_start, f_start + L):
                    continue
                fw = genome[c][f_start:f_start + L].tobytes().decode("ascii")
                if not set(fw) <= bases:
                    continue
                flank_found = fw
                break
            if flank_found is None:
                continue
            pw = genome[c][p_start:p_start + L].tobytes().decode("ascii")
            if not set(pw) <= bases:
                continue
            positives.append(pw)
            flanks.append(flank_found)
            kept += 1
        bucket_counts[bk] = kept
        print(f"  {bk}: {kept} positives+flanks (consumed {idx} candidates)")

    assert len(positives) == len(flanks) == sum(CCRE_BUDGET.values())
    all_seqs = positives + flanks
    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]
    assert len(all_seqs) == N_SEQ

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s); f.write("\n")
    gc = sum(1 for s in all_seqs[:5000] for c in s if c in "GC") / (5000 * L)
    print(f"wrote {N_SEQ} → {out_path} (GC {gc:.3f}, total {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
