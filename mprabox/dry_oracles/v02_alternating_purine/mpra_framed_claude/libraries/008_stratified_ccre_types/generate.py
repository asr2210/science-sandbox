"""
Experiment 008 — stratified cCRE types + random.

Currently random cCRE sampling is dominated by dELS (~80% of genome-wide
cCREs are dELS or dELS+CTCF). Promoters (PLS) get only ~4% representation.
Different cCRE types contain different TF motif distributions:
- PLS  : promoters; TBP, NRF1, ETS-like motifs
- pELS : proximal enhancers; promoter+enhancer hybrid grammar
- dELS : distal enhancers; diverse cell-type-specific TFs
- CTCF : insulator/boundary; CTCF motif strongly
- DNase-H3K4me3 : open chromatin without classical CRE annotation

If the model needs to see ALL of these types to generalize across the
14 evals, balancing should help. If most signal comes from one type
(probably dELS for enhancers), balancing should hurt.

Composition (50K total):
- 10,000 random genomic windows
- 10,000 PLS (PLS or PLS+CTCF)
- 10,000 pELS (pELS or pELS+CTCF)
- 10,000 dELS (dELS or dELS+CTCF)
- 5,000 CTCF-only
- 5,000 DNase-H3K4me3 (with or without CTCF)
"""
import os, time, numpy as np
from collections import defaultdict

L = 200
HALF = L // 2
SEED = 0

CCRE_BUDGET = {
    "PLS":   10_000,
    "pELS":  10_000,
    "dELS":  10_000,
    "CTCF":  5_000,
    "DNH3":  5_000,
}
N_RANDOM = 10_000
N_SEQ = N_RANDOM + sum(CCRE_BUDGET.values())
assert N_SEQ == 50_000

def classify(type_str):
    """Map cCRE type string to a bucket key (or None to skip)."""
    parts = set(t.strip() for t in type_str.split(","))
    # PLS first (strongest signal for "promoter")
    if "PLS" in parts:
        return "PLS"
    if "pELS" in parts:
        return "pELS"
    if "dELS" in parts:
        return "dELS"
    if "DNase-H3K4me3" in parts:
        return "DNH3"
    if "CTCF-only" in parts:
        return "CTCF"
    return None

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    cache_dir = os.path.join(repo_root, "data", "hg38_npy")
    bed_path = os.path.join(repo_root, "data", "GRCh38-cCREs.bed")
    t0 = time.time()

    genome = {}; n_prefix = {}
    for f in sorted(os.listdir(cache_dir)):
        if not f.endswith(".npy"):
            continue
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

    # ---------- bucket cCREs ----------
    t1 = time.time()
    buckets = defaultdict(list)  # bucket -> list of (chrom, midpoint)
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
    print("bucket sizes:", {k: len(v) for k, v in buckets.items()},
          f"({time.time()-t1:.1f}s)")
    for k, need in CCRE_BUDGET.items():
        assert len(buckets[k]) >= need, f"{k}: {len(buckets[k])} < {need}"

    # ---------- sample each bucket ----------
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
    for bucket, need in CCRE_BUDGET.items():
        seqs = sample_windows(buckets[bucket], need)
        print(f"  {bucket}: {len(seqs)}")
        all_seqs.extend(seqs)

    # ---------- random genomic ----------
    p = lens / lens.sum()
    rand_seqs = []
    while len(rand_seqs) < N_RANDOM:
        need = N_RANDOM - len(rand_seqs)
        bs = need * 2
        chrom_idx = rng.choice(len(chroms), size=bs, p=p)
        chrom_lens_arr = lens[chrom_idx]
        starts = (rng.random(bs) * (chrom_lens_arr - L)).astype(np.int64)
        for i in range(bs):
            if len(rand_seqs) >= N_RANDOM:
                break
            c = chroms[chrom_idx[i]]
            s = int(starts[i])
            if n_prefix[c][s + L] - n_prefix[c][s] != 0:
                continue
            w = genome[c][s:s + L].tobytes().decode("ascii")
            if set(w) <= bases:
                rand_seqs.append(w)
    all_seqs.extend(rand_seqs)
    print(f"  random: {len(rand_seqs)}")
    assert len(all_seqs) == N_SEQ

    # shuffle
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
