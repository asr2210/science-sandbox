"""Experiment 015 — 30k motifs + 10k pELS + 10k dELS.

Theory v3.7: motifs need ~30k for broad baseline; cCRE classes need
~15k for full per-class signal but should retain partial signal at
~10k. This recipe sits right at both edges:
- 30k motifs (minimum for broad)
- 10k pELS (half-strength — target eval_08)
- 10k dELS (half-strength — target eval_10/13)

If both pELS and dELS deliver ~half their signal, we get a record
mean by covering more evals than any prior library. If dilution
collapses one or both, we've mapped the design floor.

Generalization angle: the model sees three distinct grammars
(synthetic high-density TF, real proximal enhancer, real distal
enhancer). A model trained on all three should generalize better to
unseen cell types where the dominant regulatory class may differ
from K562/HepG2/SK-N-SH.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
BED = "data/GRCh38-cCREs.bed"
N = 50_000
N_MOTIF = 30_000
N_PELS = 10_000
N_DELS = 10_000
L = 200
SEED = 15
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
    by_cls = load_ccres_by_class(["pELS", "dELS"])
    mot = dense_motifs(rng, N_MOTIF, L)
    pels = sample_ccres(rng, by_cls["pELS"], N_PELS, L, arrs)
    dels = sample_ccres(rng, by_cls["dELS"], N_DELS, L, arrs)
    print(f"motif={len(mot)}, pels={len(pels)}, dels={len(dels)} "
          f"in {time.time()-t0:.1f}s")
    seqs = mot + pels + dels
    rng.shuffle(seqs)
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"total {len(seqs)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
