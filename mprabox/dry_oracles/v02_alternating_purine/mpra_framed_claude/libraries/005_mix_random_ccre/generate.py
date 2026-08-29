"""
Experiment 005 — 50/50 mix of random genomic and cCRE-centered windows.

Composition:
- 25,000 random 200bp windows sampled uniformly from chr1..22, X, Y
  (in proportion to chromosome length).
- 25,000 windows centered on randomly chosen genome-wide cCREs.

Hypothesis (T4 → T5): a mix should preserve the SK-N-SH "freebie"
signal that random genomic provides (was 0.46) while keeping the
K562/HepG2 motif-grammar signal that cCREs unlocked (K562_r > 0 on
some evals in 004). Predicted: mean_r > both 002 (0.150) and 004
(0.143).

Generalization rationale: a model trained on a mixed library sees the
full dynamic range of activity (low: random non-regulatory; high:
regulatory cCREs) and learns to distinguish them, plus the natural
sequence background that all cell types share. This should be more
robust to unseen cell types than a pure regulatory library (which
biases toward "everything is active") or a pure random library
(which has no regulatory signal to learn).
"""
import os
import time
import numpy as np

N_SEQ = 50_000
N_RANDOM = 25_000
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
    genome = {}
    for f in os.listdir(cache_dir):
        if f.endswith(".npy"):
            c = f[:-4]
            genome[c] = np.load(os.path.join(cache_dir, f), mmap_mode="r")
    chroms = sorted(genome.keys())
    chrom_lens = np.array([len(genome[c]) for c in chroms], dtype=np.int64)
    print(f"genome mmap loaded: {len(chroms)} chroms, total {chrom_lens.sum():,} bp ({time.time()-t0:.1f}s)")

    rng = np.random.default_rng(SEED)

    # --- Part A: random genomic windows ---
    t1 = time.time()
    bases = set("ACGT")
    random_seqs = []
    while len(random_seqs) < N_RANDOM:
        need = N_RANDOM - len(random_seqs)
        # pick chromosomes weighted by length
        chrom_probs = chrom_lens / chrom_lens.sum()
        chosen = rng.choice(len(chroms), size=need * 2, p=chrom_probs)
        starts = rng.integers(0, chrom_lens.max(), size=need * 2)
        for c_idx, s in zip(chosen, starts):
            if len(random_seqs) >= N_RANDOM:
                break
            chrom = chroms[c_idx]
            arr = genome[chrom]
            if s + L > len(arr):
                continue
            sub = arr[int(s):int(s) + L]
            if np.any(sub == ord("N")):
                continue
            window = sub.tobytes().decode("ascii")
            if set(window) <= bases:
                random_seqs.append(window)
    print(f"random part: {len(random_seqs)} ({time.time()-t1:.1f}s)")

    # --- Part B: cCRE-centered windows ---
    t2 = time.time()
    ccres = []
    keep = set(chroms)
    with open(bed_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            c = parts[0]
            if c not in keep:
                continue
            mid = (int(parts[1]) + int(parts[2])) // 2
            ccres.append((c, mid))
    print(f"  loaded {len(ccres):,} cCREs ({time.time()-t2:.1f}s)")

    order = rng.permutation(len(ccres))
    ccre_seqs = []
    for i in order:
        chrom, mid = ccres[i]
        start = mid - HALF
        arr = genome[chrom]
        if start < 0 or start + L > len(arr):
            continue
        sub = arr[start:start + L]
        if np.any(sub == ord("N")):
            continue
        window = sub.tobytes().decode("ascii")
        if set(window) <= bases:
            ccre_seqs.append(window)
        if len(ccre_seqs) >= N_CCRE:
            break
    print(f"cCRE part: {len(ccre_seqs)} ({time.time()-t2:.1f}s)")

    # combine and shuffle the interleaving
    all_seqs = random_seqs + ccre_seqs
    perm = rng.permutation(len(all_seqs))
    all_seqs = [all_seqs[i] for i in perm]
    assert len(all_seqs) == N_SEQ

    out_path = os.path.join(here, "sequences_0.txt")
    with open(out_path, "w") as f:
        for s in all_seqs:
            f.write(s)
            f.write("\n")
    with open(out_path) as f:
        lines = f.read().splitlines()
    assert len(lines) == N_SEQ
    assert all(len(s) == L for s in lines)
    assert all(set(s) <= bases for s in lines[:1000])
    gc = sum(1 for line in lines[:5000] for c in line if c in "GC") / (5000 * L)
    print(f"wrote {len(lines)} sequences of length {L} to {out_path}")
    print(f"approximate GC fraction (first 5000): {gc:.3f}")
    print(f"total time: {time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
