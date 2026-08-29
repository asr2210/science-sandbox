"""
Experiment 012 — hybrid cCRE + paired flanks + random.

Composition (50K total):
- 20,000 cCRE-centered positives (natural distribution)
- 20,000 paired flanks (one per positive, ±1.5-3kb shift, cCRE-overlap-checked)
- 10,000 pure random genomic windows

Hypothesis: 010 (paired flanks) was the new best (0.158) but lost
ground on eval_07 (-0.007) and eval_13 (-0.036), both "random-loving"
evals. Adding 10K random genomic should recover those evals without
sacrificing 010's K562/general-eval gains.

Predicted:
- best case: mean_r 0.160-0.165 (hits both signals).
- worst case: ≤0.155 (random dilutes paired-flank signal too much).
"""
import os, time, numpy as np

N_PAIRS = 20_000
N_RANDOM = 10_000
L = 200
HALF = L // 2
FLANK_MIN = 1500
FLANK_MAX = 3000
SEED = 0

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
    lens = np.array([len(genome[c]) for c in chroms], dtype=np.int64)
    print(f"genome+prefix in {time.time()-t0:.1f}s")
    bases = set("ACGT")
    rng = np.random.default_rng(SEED)

    ccre_intervals = {c: [] for c in chroms}
    all_mids = []
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in genome: continue
            s, e = int(parts[1]), int(parts[2])
            ccre_intervals[c].append((s, e))
            all_mids.append((c, (s + e) // 2))
    for c in chroms:
        ccre_intervals[c].sort()
    print(f"  {len(all_mids):,} cCREs loaded, {time.time()-t0:.1f}s")

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

    order = rng.permutation(len(all_mids))
    positives, flanks = [], []
    idx = 0
    while len(positives) < N_PAIRS and idx < len(order):
        c, mid = all_mids[order[idx]]
        idx += 1
        p_start = mid - HALF
        if p_start < 0 or p_start + L > len(genome[c]):
            continue
        if n_prefix[c][p_start + L] - n_prefix[c][p_start] != 0:
            continue
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
    print(f"  positives+flanks: {len(positives)} (consumed {idx} cCREs)")
    assert len(positives) == N_PAIRS

    # random genomic
    p = lens / lens.sum()
    rand_seqs = []
    while len(rand_seqs) < N_RANDOM:
        need = N_RANDOM - len(rand_seqs)
        bs = need * 2
        chrom_idx = rng.choice(len(chroms), size=bs, p=p)
        chrom_lens_arr = lens[chrom_idx]
        starts = (rng.random(bs) * (chrom_lens_arr - L)).astype(np.int64)
        for i in range(bs):
            if len(rand_seqs) >= N_RANDOM: break
            c = chroms[chrom_idx[i]]
            s = int(starts[i])
            if n_prefix[c][s + L] - n_prefix[c][s] != 0: continue
            w = genome[c][s:s + L].tobytes().decode("ascii")
            if set(w) <= bases: rand_seqs.append(w)
    print(f"  random: {len(rand_seqs)}")

    all_seqs = positives + flanks + rand_seqs
    assert len(all_seqs) == 50_000
    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s); f.write("\n")
    gc = sum(1 for s in all_seqs[:5000] for c in s if c in "GC") / (5000 * L)
    print(f"wrote 50000 → {out_path} (GC {gc:.3f}, total {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
