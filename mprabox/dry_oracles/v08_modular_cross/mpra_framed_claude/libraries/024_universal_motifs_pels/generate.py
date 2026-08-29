"""Experiment 024 — 35k motifs (10 universal TFs) + 15k pELS.

Restricts motif pool to 10 "universal" TFs that are active in MOST
cell types: SP1, NRF1, ETS, USF, AP1, CREB, NFY, YY1, TATA, INR.
Removes cell-type-specific TFs (GATA, HNF, NEUROD, BRN2, etc.).

Hypothesis: a model trained ONLY on universal TFs learns features
that transfer maximally to unseen cell types (no cell-type-specific
TF features that wouldn't fire elsewhere). Loses cell-type-specific
eval signals but gains broad generalization.

This is a focused TEST of generalization vs. K562/HepG2/SKNSH
performance. If mean drops a lot, cell-type-specific motifs are
doing necessary work. If mean stays similar, universal motifs are
the core signal.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
BED = "data/GRCh38-cCREs.bed"
N = 50_000
N_MOTIF = 35_000
N_PELS = N - N_MOTIF
L = 200
SEED = 24
CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])

# UNIVERSAL TFs only — active in essentially all mammalian cell types.
MOTIFS = {
    "AP1":"TGACTCA",     # AP1 (FOS/JUN) - stress, broad
    "ETS":"ACCGGAAGT",   # ETS family - ubiquitous
    "NRF1":"CGCATGCGCA", # NRF1 - mitochondrial, broad
    "USF":"CACGTG",      # USF/E-box - broad bHLH
    "SP1":"GGGGTGGGG",   # SP1 - housekeeping GC box
    "CREB":"TGACGTCA",   # CREB - cAMP response, broad
    "NFY":"CCAATCAG",    # NFY - CCAAT box, very broad
    "YY1":"CCATCTT",     # YY1 - polycomb-associated, broad
    "TATA":"TATAAAA",    # TATA box - core promoter
    "INR":"TCAGTT",      # Initiator - core promoter
}
KEYS = list(MOTIFS.keys())
COMP = {ord("A"): "T", ord("C"): "G", ord("G"): "C", ord("T"): "A"}


def revcomp(s):
    return s.translate(COMP)[::-1]


def dense_motifs(rng, n, L):
    alpha = np.array(list("ACGT"))
    bb_idx = rng.integers(0, 4, size=(n, L))
    backbone = ["".join(alpha[r].tolist()) for r in bb_idx]
    n_inserts = rng.integers(15, 26, size=n)
    out = []
    for i in range(n):
        b = list(backbone[i])
        for _ in range(int(n_inserts[i])):
            mk = KEYS[rng.integers(0, len(KEYS))]
            m = MOTIFS[mk]
            if rng.random() < 0.5:
                m = revcomp(m)
            if len(m) >= L:
                continue
            pos = int(rng.integers(0, L - len(m) + 1))
            b[pos:pos + len(m)] = list(m)
        out.append("".join(b))
    return out


def load_pels():
    out = []
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom = p[0]
            if chrom not in CHROMS:
                continue
            cat = p[5]
            if cat == "pELS" or cat == "pELS,CTCF-bound":
                out.append((chrom, int(p[1]), int(p[2])))
    return out


def sample_pels(rng, n, L, arrs):
    pels = load_pels()
    idx = rng.permutation(len(pels))
    out = []; i = 0
    while len(out) < n:
        if i >= len(idx):
            idx = rng.permutation(len(pels)); i = 0
        chrom, s, e = pels[idx[i]]; i += 1
        mid = (s + e) // 2
        start = mid - L // 2; end = start + L
        if start < 0 or end > len(arrs[chrom]):
            continue
        w = bytes(arrs[chrom][start:end])
        if b"N" in w:
            continue
        out.append(w.decode("ascii"))
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    arrs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r")
            for c in CHROMS}
    mot = dense_motifs(rng, N_MOTIF, L)
    pels = sample_pels(rng, N_PELS, L, arrs)
    print(f"motif={len(mot)} (universal-only 10 TFs), "
          f"pels={len(pels)} in {time.time()-t0:.1f}s")
    seqs = mot + pels
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
