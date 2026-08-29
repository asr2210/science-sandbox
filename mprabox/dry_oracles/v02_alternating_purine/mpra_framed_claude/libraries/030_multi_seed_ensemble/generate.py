"""
Experiment 030 — multi-seed 013 ensemble.

013 with SEED=0 → mean_r=0.166. With SEED=1 → 0.150. Identical
design, 0.016 spread. This experiment splits the 013 composition
across TWO seeds to broaden cCRE coverage and reduce seed-specific
sampling bias.

Composition (50K total):
- 7.5K uniform + 2.5K CTCF + 2.5K DNH3 from SEED=0 (12.5K positives)
- 7.5K uniform + 2.5K CTCF + 2.5K DNH3 from SEED=1 (12.5K positives)
- Each positive has a paired 1500-3000bp flank → 25K flanks total

Hypothesis: covering 25K different cCREs across two independent
draws gives broader sampling than 25K from one seed (which has
seed-specific clustering). Expected mean ≈ 0.158 (average of two
seeds), potentially higher if diversity helps.

Predicted: 0.155-0.170. Either matches the average, or beats
both seeds individually via diversity.
"""
import os, time, numpy as np

L = 200
HALF = L // 2
FAR_MIN, FAR_MAX = 1500, 3000

def classify_rare(type_str):
    parts = set(t.strip() for t in type_str.split(","))
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

    ccre_intervals = {c: [] for c in chroms}
    all_mids, ctcf_mids, dnh3_mids = [], [], []
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in genome: continue
            s, e = int(parts[1]), int(parts[2])
            ccre_intervals[c].append((s, e))
            mid = (s + e) // 2
            all_mids.append((c, mid))
            bk = classify_rare(parts[5])
            if bk == "CTCF": ctcf_mids.append((c, mid))
            elif bk == "DNH3": dnh3_mids.append((c, mid))
    for c in chroms:
        ccre_intervals[c].sort()

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

    def sample_pairs(items, n_need, label, rng):
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
                offset = sign * rng.integers(FAR_MIN, FAR_MAX + 1)
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
        print(f"  {label} (seed): {len(positives)}")
        return positives, flanks

    positives = []
    flanks = []
    for seed in (0, 1):
        rng = np.random.default_rng(seed)
        p_u, f_u = sample_pairs(all_mids, 7_500, f"uniform_s{seed}", rng)
        p_c, f_c = sample_pairs(ctcf_mids, 2_500, f"CTCF_s{seed}", rng)
        p_d, f_d = sample_pairs(dnh3_mids, 2_500, f"DNH3_s{seed}", rng)
        positives += p_u + p_c + p_d
        flanks += f_u + f_c + f_d

    assert len(positives) == len(flanks) == 25_000

    all_seqs = positives + flanks
    perm_rng = np.random.default_rng(42)
    perm = perm_rng.permutation(len(all_seqs))
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
