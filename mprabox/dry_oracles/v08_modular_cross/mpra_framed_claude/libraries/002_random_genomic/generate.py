"""Experiment 002 — random 200 bp windows from hg38 autosomes.

Sample 50,000 windows uniformly across hg38 chromosomes 1-22, weighted
by chromosome length so each base in the genome has equal probability
of being a window start. Reject windows containing N (assembly gaps).

This is the "default biological" baseline: real motif distributions,
real GC content, real dinucleotide structure. Almost every window will
be non-regulatory (the genome is ~98% non-regulatory), so activities
should mostly be low with a tail of higher-activity windows that
happen to overlap enhancer/promoter elements.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 2

CHROMS = [f"chr{i}" for i in range(1, 23)]


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r") for c in CHROMS}
    sizes = np.array([len(arrs[c]) - L for c in CHROMS], dtype=np.int64)
    weights = sizes / sizes.sum()
    seqs = []
    n_rej = 0
    while len(seqs) < N:
        c_idx = int(rng.choice(len(CHROMS), p=weights))
        s = int(rng.integers(0, sizes[c_idx]))
        chrom = CHROMS[c_idx]
        window = bytes(arrs[chrom][s : s + L]).decode("ascii")
        if "N" in window:
            n_rej += 1
            continue
        seqs.append(window)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N} seqs in {time.time()-t0:.1f}s ({n_rej} N-rejects)")


if __name__ == "__main__":
    main()
