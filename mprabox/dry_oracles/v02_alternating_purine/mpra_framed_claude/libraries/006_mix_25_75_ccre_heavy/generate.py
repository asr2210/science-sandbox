"""
Experiment 006 — 25/75 mix (cCRE-heavy): 12,500 random + 37,500 cCRE.

A ratio test against 005 (50/50). Asks: does shifting toward more
regulatory content improve mean_r further, or did 005 already overshoot?

Compared to 005:
- 005: 25,000 random + 25,000 cCRE (mean_r 0.156)
- 006: 12,500 random + 37,500 cCRE  → less SK-N-SH freebie, more
  motif grammar
- Predict: K562_r should go up further (more cCRE-derived motif
  examples), SK-N-SH_r may drop slightly toward pure-cCRE level (0.42).
  If mean_r goes UP, more regulatory is better. If it goes DOWN, 005
  was near optimum.

Generalization rationale: by varying the mix and observing the shape
of mean_r, we triangulate the optimum without committing to a
hypothetical "right" ratio.

Faster implementation than 005: vectorized cCRE midpoint loading,
vectorized random window proposal, batched N-check via per-chr
prefix sums computed once per chr.
"""
import os
import time
import numpy as np

N_SEQ = 50_000
N_RANDOM = 12_500
N_CCRE = N_SEQ - N_RANDOM
L = 200
HALF = L // 2
SEED = 0

def main():
    here = os.path.dirname(__file__)
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    cache_dir = os.path.join(repo_root, "data", "hg38_npy")
    bed_path = os.path.join(repo_root, "data", "GRCh38-cCREs.bed")
    t0 = time.time()

    # load genome (mmap), build per-chr ascii arr + n-prefix
    genome = {}
    n_prefix = {}
    for f in sorted(os.listdir(cache_dir)):
        if f.endswith(".npy"):
            c = f[:-4]
            arr = np.load(os.path.join(cache_dir, f), mmap_mode="r")
            # materialize once to compute prefix; keep mmap arr for window read
            mat = np.asarray(arr)
            genome[c] = mat
            is_n = (mat == ord("N")).astype(np.int32)
            n_prefix[c] = np.concatenate(([0], np.cumsum(is_n)))
    chroms = sorted(genome.keys())
    lens = np.array([len(genome[c]) for c in chroms], dtype=np.int64)
    print(f"genome+prefix in {time.time()-t0:.1f}s")
    bases = set("ACGT")

    rng = np.random.default_rng(SEED)

    # ---------- random genomic windows (vectorized) ----------
    t1 = time.time()
    rand_seqs = []
    # weight chromosomes by length
    p = lens / lens.sum()
    while len(rand_seqs) < N_RANDOM:
        need = N_RANDOM - len(rand_seqs)
        bs = need * 2
        chrom_idx = rng.choice(len(chroms), size=bs, p=p)
        # per-chrom max_start
        chrom_lens_arr = lens[chrom_idx]
        starts = (rng.random(bs) * (chrom_lens_arr - L)).astype(np.int64)
        # N-check
        for i in range(bs):
            if len(rand_seqs) >= N_RANDOM:
                break
            c = chroms[chrom_idx[i]]
            s = int(starts[i])
            if n_prefix[c][s + L] - n_prefix[c][s] != 0:
                continue
            window = genome[c][s:s + L].tobytes().decode("ascii")
            if set(window) <= bases:
                rand_seqs.append(window)
    print(f"random: {len(rand_seqs)} in {time.time()-t1:.1f}s")

    # ---------- cCRE windows (vectorized) ----------
    t2 = time.time()
    # build (chrom_idx, mid) arrays
    chrom_to_idx = {c: i for i, c in enumerate(chroms)}
    cidx, mids = [], []
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in chrom_to_idx:
                continue
            mids.append((int(parts[1]) + int(parts[2])) // 2)
            cidx.append(chrom_to_idx[c])
    cidx = np.array(cidx, dtype=np.int32)
    mids = np.array(mids, dtype=np.int64)
    print(f"  {len(mids):,} cCREs loaded in {time.time()-t2:.1f}s")

    order = rng.permutation(len(mids))
    ccre_seqs = []
    for j in order:
        c = chroms[cidx[j]]
        start = int(mids[j]) - HALF
        if start < 0 or start + L > lens[cidx[j]]:
            continue
        if n_prefix[c][start + L] - n_prefix[c][start] != 0:
            continue
        window = genome[c][start:start + L].tobytes().decode("ascii")
        if set(window) <= bases:
            ccre_seqs.append(window)
        if len(ccre_seqs) >= N_CCRE:
            break
    print(f"cCRE: {len(ccre_seqs)} in {time.time()-t2:.1f}s")

    all_seqs = rand_seqs + ccre_seqs
    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]
    assert len(all_seqs) == N_SEQ

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s); f.write("\n")
    with open(out_path) as f:
        lines = f.read().splitlines()
    assert len(lines) == N_SEQ
    assert all(len(s) == L for s in lines)
    assert all(set(s) <= bases for s in lines[:1000])
    gc = sum(1 for line in lines[:5000] for c in line if c in "GC") / (5000 * L)
    print(f"wrote {len(lines)} → {out_path} (GC {gc:.3f}, total {time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
