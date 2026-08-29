"""Experiment 021 — 50k pure dense motifs at 35-50 inserts/seq.

Pure motif scaffold, no cCRE, no real sequence. Tests whether 018's
eval_07 record (0.0109) came from motifs alone or from pELS adding
on top. Also: pure motif library is the most "cell-type-agnostic"
training distribution — contains TF binding info without any
cell-type-specific genomic context.

Generalization angle: a model trained purely on synthetic motif
sequences sees only TF binding patterns. Such a model would
generalize to any cell type where the represented TFs are active —
no genomic context dependencies. This is the maximally transferable
training distribution in principle.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 21

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


def dense_motifs(rng, n, L, n_low, n_high):
    alpha = np.array(list("ACGT"))
    bb_idx = rng.integers(0, 4, size=(n, L))
    backbone = ["".join(alpha[r].tolist()) for r in bb_idx]
    n_inserts = rng.integers(n_low, n_high + 1, size=n)
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


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    mot = dense_motifs(rng, N, L, 35, 50)
    print(f"motif={len(mot)} in {time.time()-t0:.1f}s")
    with open(OUT, "w") as f:
        f.write("\n".join(mot))
        f.write("\n")
    print(f"total {len(mot)} in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
