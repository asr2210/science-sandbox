"""
Experiment 015 — soft-balanced stratification with dELS lead.

Composition (50K total):
- 9K dELS + 4K pELS + 4K PLS + 4K CTCF + 4K DNH3 = 25K positives
- 25K paired flanks (one per positive, ±1.5-3kb)

Hypothesis: 011's lift on eval_07/10/13 came from balanced 5-way
distribution. 008's lift on eval_06/11 came from dELS quantity (10K
dELS). Stack both: keep dELS as the largest (9K, near 008's 10K)
but ensure all five types are over-represented vs natural frequency.

Predicted: mean_r 0.165-0.170, ideally beats 013.
"""
import os, time, numpy as np

L = 200
HALF = L // 2
FLANK_MIN = 1500
FLANK_MAX = 3000
SEED = 0

BUDGET = {
    "dELS": 9_000,
    "pELS": 4_000,
    "PLS":  4_000,
    "CTCF": 4_000,
    "DNH3": 4_000,
}
N_PAIRS = sum(BUDGET.values())
assert N_PAIRS == 25_000

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

    ccre_intervals = {c: [] for c in chroms}
    buckets = {k: [] for k in BUDGET.keys()}
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in genome: continue
            s, e = int(parts[1]), int(parts[2])
            ccre_intervals[c].append((s, e))
            bk = classify(parts[5])
            if bk in buckets:
                buckets[bk].append((c, (s + e) // 2))
    for c in chroms:
        ccre_intervals[c].sort()
    print("bucket sizes:", {k: len(v) for k, v in buckets.items()})

    def overlaps_ccre(chrom, start, end):
        intervals = ccre_intervals[chrom]
        lo, hi = 0, len(intervals)
        while lo < hi:
            m = (lo + hi) // 2
            if intervals[m][0] < end: lo = m + 1
            else: hi = m
        for k in range(max(0, lo - 2), min(len(intervals), lo + 1)):
            s2, e2 = intervals[k]
            if s2 < end and start < e2: return True
        return False

    def sample_pairs(items, n_need, label):
        order = rng.permutation(len(items))
        positives, flanks = [], []
        idx = 0
        while len(positives) < n_need and idx < len(order):
            c, mid = items[order[idx]]
            idx += 1
            p_start = mid - HALF
            if p_start < 0 or p_start + L > len(genome[c]): continue
            if n_prefix[c][p_start + L] - n_prefix[c][p_start] != 0: continue
            flank_found = None
            for _ in range(8):
                sign = 1 if rng.random() < 0.5 else -1
                offset = sign * rng.integers(FLANK_MIN, FLANK_MAX + 1)
                f_start = mid + int(offset) - HALF
                if f_start < 0 or f_start + L > len(genome[c]): continue
                if n_prefix[c][f_start + L] - n_prefix[c][f_start] != 0: continue
                if overlaps_ccre(c, f_start, f_start + L): continue
                fw = genome[c][f_start:f_start + L].tobytes().decode("ascii")
                if not set(fw) <= bases: continue
                flank_found = fw
                break
            if flank_found is None: continue
            pw = genome[c][p_start:p_start + L].tobytes().decode("ascii")
            if not set(pw) <= bases: continue
            positives.append(pw)
            flanks.append(flank_found)
        print(f"  {label}: {len(positives)}")
        return positives, flanks

    positives, flanks = [], []
    for bk, need in BUDGET.items():
        p, fl = sample_pairs(buckets[bk], need, bk)
        positives.extend(p); flanks.extend(fl)
    assert len(positives) == len(flanks) == N_PAIRS

    all_seqs = positives + flanks
    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]
    assert len(all_seqs) == 50_000

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s); f.write("\n")
    gc = sum(1 for s in all_seqs[:5000] for c in s if c in "GC") / (5000 * L)
    print(f"wrote 50000 → {out_path} (GC {gc:.3f}, total {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
