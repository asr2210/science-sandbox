"""
Experiment 022 — 25K positives + 12.5K paired flanks + 12.5K random.

Composition (50K total):
- 25K positives: 15K uniform + 5K CTCF + 5K DNH3 (013 ratio)
- 12.5K far paired flanks (first 12.5K positives paired)
- 12.5K random genomic windows

Hypothesis: 013's eval_13 weakness (0.126) and eval_07 weakness
(relative to 018's 0.203) may be partly addressable with a
modest random component. Half of the negatives stay as paired
flanks (preserves K562 enhancer signal), the other half becomes
random (helps eval_13).

Predicted:
- best case: mean_r 0.165-0.170 (random helps eval_13 modestly)
- worst case: ≤0.16 (dilutes flank signal too much, similar to 012)

Note: 012 had a similar idea (20+20+10 random) and got 0.153.
022's 25+12.5+12.5 keeps full positive set + bigger random component.
"""
import os, time, numpy as np

L = 200
HALF = L // 2
FAR_MIN, FAR_MAX = 1500, 3000
SEED = 0

N_UNIFORM = 15_000
N_CTCF = 5_000
N_DNH3 = 5_000
N_FLANKS = 12_500
N_RANDOM = 12_500

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
    lens = np.array([len(genome[c]) for c in chroms], dtype=np.int64)
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

    positives = []
    positives += sample_pos(all_mids, N_UNIFORM, "uniform")
    positives += sample_pos(ctcf_mids, N_CTCF, "CTCF")
    positives += sample_pos(dnh3_mids, N_DNH3, "DNH3")
    assert len(positives) == 25_000

    flanks = []
    # Pair the first N_FLANKS positives with a flank; retry with subsequent
    # ones if a flank can't be found.
    used_for_flanking = [False] * len(positives)
    i = 0
    while len(flanks) < N_FLANKS and i < len(positives):
        c, mid, w = positives[i]
        f = find_flank(c, mid)
        if f is not None:
            flanks.append(f)
            used_for_flanking[i] = True
        i += 1
    print(f"  paired flanks: {len(flanks)}")
    assert len(flanks) == N_FLANKS

    # Random genomic windows
    p_chr = lens / lens.sum()
    rand_seqs = []
    while len(rand_seqs) < N_RANDOM:
        need = N_RANDOM - len(rand_seqs)
        bs = need * 2
        chrom_idx = rng.choice(len(chroms), size=bs, p=p_chr)
        starts = (rng.random(bs) * (lens[chrom_idx] - L)).astype(np.int64)
        for k in range(bs):
            if len(rand_seqs) >= N_RANDOM: break
            c = chroms[chrom_idx[k]]
            s = int(starts[k])
            if n_prefix[c][s + L] - n_prefix[c][s] != 0: continue
            w = genome[c][s:s + L].tobytes().decode("ascii")
            if set(w) <= bases: rand_seqs.append(w)
    print(f"  random: {len(rand_seqs)}")

    pos_seqs = [w for (_, _, w) in positives]
    all_seqs = pos_seqs + flanks + rand_seqs
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
