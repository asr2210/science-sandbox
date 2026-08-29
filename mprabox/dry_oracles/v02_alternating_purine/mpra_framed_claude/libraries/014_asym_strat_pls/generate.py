"""
Experiment 014 — asymmetric stratification + PLS boost.

Composition (50K total):
- 10K cCRE-centered (uniform, natural distribution; ~8K dELS)
- 5K PLS (boosted from natural ~570)
- 5K CTCF-only (boosted)
- 5K DNase-H3K4me3 (boosted)
- 25K paired flanks (one per positive, ±1.5-3kb)

Hypothesis: 013's residual weakness on eval_13 (0.126) is due to
under-representation of PLS (promoter) content. Adding 5K PLS should
recover eval_13 (target: 0.158-like, from 011). Cost: drops dELS
from ~12K to ~8K, may slightly weaken eval_06/11.

Predicted:
- if PLS helps eval_13 → mean ≥ 0.166 (013)
- if dELS reduction dominates → mean ≤ 0.16
"""
import os, time, numpy as np

L = 200
HALF = L // 2
FLANK_MIN = 1500
FLANK_MAX = 3000
SEED = 0

N_UNIFORM = 10_000
N_PLS = 5_000
N_CTCF = 5_000
N_DNH3 = 5_000
N_PAIRS = N_UNIFORM + N_PLS + N_CTCF + N_DNH3  # 25000

def classify(type_str):
    parts = set(t.strip() for t in type_str.split(","))
    if "PLS" in parts: return "PLS"
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
    all_mids, pls_mids, ctcf_mids, dnh3_mids = [], [], [], []
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in genome: continue
            s, e = int(parts[1]), int(parts[2])
            ccre_intervals[c].append((s, e))
            mid = (s + e) // 2
            all_mids.append((c, mid))
            bk = classify(parts[5])
            if bk == "PLS": pls_mids.append((c, mid))
            elif bk == "CTCF": ctcf_mids.append((c, mid))
            elif bk == "DNH3": dnh3_mids.append((c, mid))
    for c in chroms:
        ccre_intervals[c].sort()
    print(f"  total={len(all_mids):,}  PLS={len(pls_mids):,}  CTCF={len(ctcf_mids):,}  DNH3={len(dnh3_mids):,}")

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

    p_u, f_u = sample_pairs(all_mids, N_UNIFORM, "uniform")
    p_p, f_p = sample_pairs(pls_mids, N_PLS, "PLS")
    p_c, f_c = sample_pairs(ctcf_mids, N_CTCF, "CTCF")
    p_d, f_d = sample_pairs(dnh3_mids, N_DNH3, "DNH3")

    positives = p_u + p_p + p_c + p_d
    flanks = f_u + f_p + f_c + f_d
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
