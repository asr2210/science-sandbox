"""
Experiment 009 — stratified cCRE at 50/50 ratio.

Composition (50K total):
- 25,000 random genomic windows
- 25,000 stratified cCRE: 5K each of PLS, pELS, dELS, CTCF-only,
  DNase-H3K4me3.

This isolates the stratification effect by holding the random/cCRE
ratio at the previously-found sweet spot (005's 50/50). If 009 ≥ both
005 and 008, "stratified 50/50" is the new working baseline.

Three-way comparison after 009:
- 005: 50/50 + uniform cCRE      → 0.156
- 008: 20/80 + stratified cCRE   → 0.154
- 009: 50/50 + stratified cCRE   → ?

If 009 > 005, stratification was the missing piece.
If 009 ≈ 005, stratification only helps in cCRE-heavy regime (where
the natural cCRE distribution is too dELS-dominant).
"""
import os, time, numpy as np
from collections import defaultdict

L = 200
HALF = L // 2
SEED = 0

CCRE_BUDGET = {
    "PLS":   5_000,
    "pELS":  5_000,
    "dELS":  5_000,
    "CTCF":  5_000,
    "DNH3":  5_000,
}
N_RANDOM = 25_000
N_SEQ = N_RANDOM + sum(CCRE_BUDGET.values())
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
    lens = np.array([len(genome[c]) for c in chroms], dtype=np.int64)
    print(f"genome+prefix in {time.time()-t0:.1f}s")
    bases = set("ACGT")
    rng = np.random.default_rng(SEED)

    buckets = defaultdict(list)
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in genome:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            bk = classify(parts[5])
            if bk is not None:
                buckets[bk].append((c, mid))
    print("bucket sizes:", {k: len(v) for k, v in buckets.items()})

    def sample_windows(items, need):
        order = rng.permutation(len(items))
        out = []
        for j in order:
            c, mid = items[j]
            start = mid - HALF
            if start < 0 or start + L > len(genome[c]):
                continue
            if n_prefix[c][start + L] - n_prefix[c][start] != 0:
                continue
            w = genome[c][start:start + L].tobytes().decode("ascii")
            if set(w) <= bases:
                out.append(w)
            if len(out) >= need:
                break
        return out

    all_seqs = []
    for bk, need in CCRE_BUDGET.items():
        seqs = sample_windows(buckets[bk], need)
        print(f"  {bk}: {len(seqs)}")
        all_seqs.extend(seqs)

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
    all_seqs.extend(rand_seqs)
    print(f"  random: {len(rand_seqs)}")
    assert len(all_seqs) == N_SEQ

    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]
    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s); f.write("\n")
    gc = sum(1 for s in all_seqs[:5000] for c in s if c in "GC") / (5000 * L)
    print(f"wrote {N_SEQ} → {out_path} (GC {gc:.3f}, total {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
