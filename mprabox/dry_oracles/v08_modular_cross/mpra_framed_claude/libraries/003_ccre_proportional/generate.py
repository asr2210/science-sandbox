"""Experiment 003 — ENCODE cCRE-centered 200 bp windows.

Sample 50,000 cCREs uniformly at random from the GRCh38-cCREs.bed file
(~1.06M elements: dELS / pELS / PLS / CTCF-only / DNase-H3K4me3). For
each cCRE, extract a 200 bp window centered on the cCRE midpoint.
Reject windows that fall off chromosome ends or contain N.

Why this is interesting for cross-cell-type generalization:
ENCODE cCREs aggregate DNase/H3K27ac/H3K4me3/CTCF evidence across 1500+
biosamples. They are *not* K562 / HepG2 / SK-N-SH specific — they
represent regulatory elements active in *some* cell type. A model
trained on such sequences sees a broad sample of regulatory grammar
rather than the tissue-specific subset our three labeled cell types use.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
BED = "data/GRCh38-cCREs.bed"
N = 50_000
L = 200
SEED = 3
CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])


def load_ccres():
    rows = []
    with open(BED) as f:
        for line in f:
            chrom, s, e, _, _, _ = line.rstrip("\n").split("\t")
            if chrom not in CHROMS:
                continue
            rows.append((chrom, int(s), int(e)))
    return rows


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    ccres = load_ccres()
    print(f"loaded {len(ccres)} cCREs in {time.time()-t0:.1f}s")
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r")
            for c in CHROMS}
    idx = rng.permutation(len(ccres))
    seqs = []
    n_rej = 0
    i = 0
    while len(seqs) < N:
        if i >= len(idx):
            idx = rng.permutation(len(ccres))
            i = 0
        chrom, s, e = ccres[idx[i]]
        i += 1
        mid = (s + e) // 2
        start = mid - L // 2
        end = start + L
        if start < 0 or end > len(arrs[chrom]):
            n_rej += 1
            continue
        window = bytes(arrs[chrom][start:end]).decode("ascii")
        if "N" in window:
            n_rej += 1
            continue
        seqs.append(window)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N} seqs in {time.time()-t0:.1f}s ({n_rej} rejects)")


if __name__ == "__main__":
    main()
