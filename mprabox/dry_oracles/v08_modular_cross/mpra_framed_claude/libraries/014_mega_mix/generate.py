"""Experiment 014 — Mega-mix: motifs + pELS + dELS + PLS.

Tests the v3.6 theory: each cCRE class is an independent eval-axis,
so combining them all should hit max eval coverage.

Composition (20k + 10k + 10k + 10k = 50k):
- 20k dense motif scaffolds (broad-acting baseline)
- 10k pELS cCREs (lit up eval_08 in 012)
- 10k dELS cCREs (lit up eval_10 + eval_13 in 013)
- 10k PLS cCREs (lit up eval_08 balanced in 011)

Risk: dilution kills per-source signals. If each subset needs ~15k
to lift its eval, this won't work. If ~10k is enough, this could be
the highest mean library yet.

Generalization angle: this is the most heterogeneous "real-biology"
library tested. It samples promoter, proximal-enhancer, and distal-
enhancer grammars from many tissues, plus synthetic motif scaffolds
that emphasize TF binding. A model trained on this should generalize
better to unseen cell types because it sees the FULL diversity of
regulatory grammar rather than one narrow class.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
BED = "data/GRCh38-cCREs.bed"
N = 50_000
N_MOTIF = 20_000
N_PELS = 10_000
N_DELS = 10_000
N_PLS = 10_000
L = 200
SEED = 14
CHROMS = set([f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"])

MOTIFS = {
    "AP1":"TGACTCA","ETS":"ACCGGAAGT","NRF1":"CGCATGCGCA","USF":"CACGTG",
    "SP1":"GGGGTGGGG","CREB":"TGACGTCA",
    "CTCF":"CCCTCTAGTGGCCAGCAGAGGG","NFY":"CCAATCAG","MEF2":"CTATAAATAG",
    "YY1":"CCATCTT","TATA":"TATAAAA","INR":"TCAGTT",
    "GATA1":"AGATAAG","TAL1":"CAGCTG","RUNX":"TGTGGTT","MYB":"TAACGGT",
    "KLF1":"CACACCC","NFE2":"TGCTGAGTCAT","STAT5":"TTCCCGGAA","GFI1B":"AAATCAC",
    "HNF1":"GTTAATAATTAAC","HNF4":"AGGTCAAAGGTCA","FOXA":"TGTTTGTTT",
    "CEBP":"ATTGCGCAAT","PPARA":"AGGTCAAAGGTCA","HNF6":"ATTGATTAA",
    "NEUROD":"GCCAGCTGTT","ASCL1":"AACAGCTGGT","BRN2":"ATGCATAATGC",
    "FOXG1":"TGTTTAC","PAX6":"TTCACGC","LHX":"TAATTAA","TBR1":"TCTAGGTGT",
    "PHOX2":"TAATTG","NRSF":"TCCTGGACAGCGCC",
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


def load_ccres_by_class(classes):
    by_cls = {c: [] for c in classes}
    with open(BED) as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            chrom = p[0]
            if chrom not in CHROMS:
                continue
            cat = p[5]
            for c in classes:
                if cat == c or cat == f"{c},CTCF-bound":
                    by_cls[c].append((chrom, int(p[1]), int(p[2])))
                    break
    return by_cls


def sample_ccres(rng, regions, n, L, arrs):
    idx = rng.permutation(len(regions))
    out = []; i = 0
    while len(out) < n:
        if i >= len(idx):
            idx = rng.permutation(len(regions)); i = 0
        chrom, s, e = regions[idx[i]]; i += 1
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
    by_cls = load_ccres_by_class(["pELS", "dELS", "PLS"])
    mot = dense_motifs(rng, N_MOTIF, L)
    pels = sample_ccres(rng, by_cls["pELS"], N_PELS, L, arrs)
    dels = sample_ccres(rng, by_cls["dELS"], N_DELS, L, arrs)
    pls = sample_ccres(rng, by_cls["PLS"], N_PLS, L, arrs)
    print(f"motif={len(mot)}, pels={len(pels)}, dels={len(dels)}, "
          f"pls={len(pls)} in {time.time()-t0:.1f}s")
    seqs = mot + pels + dels + pls
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
