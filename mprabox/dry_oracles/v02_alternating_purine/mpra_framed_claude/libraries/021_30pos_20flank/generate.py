"""
Experiment 021 — 30K positives + 20K paired flanks (3:2 ratio).

Composition (50K total):
- 18K uniform cCRE positives + 6K CTCF + 6K DNH3 = 30K positives
  (same 3:1:1 asymmetric ratio as 013, scaled up 1.2x)
- 20K far paired flanks: each of the first 20K positives gets a
  paired flank (1500-3000bp, overlap-checked). Last 10K positives
  are unpaired.

Hypothesis: 013's 25:25 ratio may not be optimal. More positive
diversity could give the model more sequence variety to learn from,
while still having enough flanks for context discrimination.

Predicted: small effect (±0.005). If more positives help, mean_r > 0.166.
"""
import os, time, numpy as np

L = 200
HALF = L // 2
FAR_MIN, FAR_MAX = 1500, 3000
SEED = 0

N_UNIFORM = 18_000
N_CTCF = 6_000
N_DNH3 = 6_000
N_FLANKS = 20_000  # only first 20K positives get a flank

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
    rng = np.random.default_rng(SEED)

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
    print(f"  total={len(all_mids):,}  CTCF={len(ctcf_mids):,}  DNH3={len(dnh3_mids):,}")

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

    def find_flank(c, mid):
        for _ in range(8):
            sign = 1 if rng.random() < 0.5 else -1
            offset = sign * rng.integers(FAR_MIN, FAR_MAX + 1)
            f_start = mid + int(offset) - HALF
            if f_start < 0 or f_start + L > len(genome[c]): continue
            if n_prefix[c][f_start + L] - n_prefix[c][f_start] != 0: continue
            if overlaps_ccre(c, f_start, f_start + L): continue
            fw = genome[c][f_start:f_start + L].tobytes().decode("ascii")
            if set(fw) <= bases: return fw
        return None

    def sample_pos(items, n_need, label):
        order = rng.permutation(len(items))
        out = []
        for j in order:
            c, mid = items[j]
            s = mid - HALF
            if s < 0 or s + L > len(genome[c]): continue
            if n_prefix[c][s + L] - n_prefix[c][s] != 0: continue
            w = genome[c][s:s + L].tobytes().decode("ascii")
            if set(w) <= bases:
                out.append((c, mid, w))
            if len(out) >= n_need: break
        print(f"  {label}: {len(out)}")
        return out

    positives = []
    positives += sample_pos(all_mids, N_UNIFORM, "uniform")
    positives += sample_pos(ctcf_mids, N_CTCF, "CTCF")
    positives += sample_pos(dnh3_mids, N_DNH3, "DNH3")
    assert len(positives) == 30_000

    # Pair the first N_FLANKS with a flank
    flanks = []
    paired_positives = []
    unpaired_positives = []
    for i, (c, mid, w) in enumerate(positives):
        if i < N_FLANKS:
            f = find_flank(c, mid)
            if f is None:
                # try a different positive later
                unpaired_positives.append(w)
                continue
            paired_positives.append(w)
            flanks.append(f)
        else:
            unpaired_positives.append(w)
    # If we have fewer than N_FLANKS pairs, try the unpaired list
    needed = N_FLANKS - len(flanks)
    if needed > 0:
        # Re-iterate from unpaired and try harder
        more_attempts = []
        for c, mid, w in positives[N_FLANKS:]:
            if needed <= 0: break
            f = find_flank(c, mid)
            if f is not None:
                paired_positives.append(w)
                flanks.append(f)
                needed -= 1
            else:
                unpaired_positives.append(w)
    print(f"  paired pairs: {len(flanks)}")
    print(f"  unpaired positives so far: {len(unpaired_positives)}")
    # ensure exactly 30K positives, 20K flanks
    all_pos = paired_positives + unpaired_positives
    # If by chance we have more than 30K (because we re-iterated), trim
    if len(all_pos) > 30_000:
        all_pos = all_pos[:30_000]
    # If fewer, we need to pad — shouldn't happen with our buckets
    assert len(all_pos) == 30_000, f"have {len(all_pos)} positives"
    assert len(flanks) == 20_000, f"have {len(flanks)} flanks"

    all_seqs = all_pos + flanks
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
