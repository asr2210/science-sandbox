"""Experiment 007 — dense motif scaffold (15-25 motifs per sequence).

Tests whether sequence-to-activity signal scales with motif density.
Same 200 bp scaffold, but each sequence gets 15-25 motifs (vs 0-10 in
exp 004, 4-12 in exp 006), drawn from a CURATED, STRONG, broadly
acting pool. Goal is to push activity range and signal-to-noise.

If r grows with density, this validates the motif-saturation strategy
and a future hybrid library should use these dense scaffolds.

Why this generalizes: the pool intentionally covers TF families used
by many cell types simultaneously — not just K562/HepG2/SK-N-SH. A
model that learns motifs at high density learns them more robustly
(because they appear in many contexts), which transfers to any cell
type that uses any of these TFs.
"""
import os
import time
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N = 50_000
L = 200
SEED = 7

# Curated strong motif pool, mixing universal activators with cell-
# type-biased motifs from K562 / HepG2 / SK-N-SH lineages.
MOTIFS = {
    # universal activators (apply in nearly all cell types)
    "AP1":    "TGACTCA",
    "ETS":    "ACCGGAAGT",
    "NRF1":   "CGCATGCGCA",
    "USF":    "CACGTG",
    "SP1":    "GGGGTGGGG",
    "CREB":   "TGACGTCA",
    "CTCF":   "CCCTCTAGTGGCCAGCAGAGGG",
    "NFY":    "CCAATCAG",
    "MEF2":   "CTATAAATAG",
    "YY1":    "CCATCTT",
    "TATA":   "TATAAAA",
    "INR":    "TCAGTT",          # initiator-like
    # hematopoietic (K562)
    "GATA1":  "AGATAAG",
    "TAL1":   "CAGCTG",
    "RUNX":   "TGTGGTT",
    "MYB":    "TAACGGT",
    "KLF1":   "CACACCC",
    "NFE2":   "TGCTGAGTCAT",
    "STAT5":  "TTCCCGGAA",
    "GFI1B":  "AAATCAC",
    # liver (HepG2)
    "HNF1":   "GTTAATAATTAAC",
    "HNF4":   "AGGTCAAAGGTCA",
    "FOXA":   "TGTTTGTTT",
    "CEBP":   "ATTGCGCAAT",
    "PPARA":  "AGGTCAAAGGTCA",
    "HNF6":   "ATTGATTAA",
    # neural (SK-N-SH)
    "NEUROD": "GCCAGCTGTT",
    "ASCL1":  "AACAGCTGGT",
    "BRN2":   "ATGCATAATGC",     # POU
    "FOXG1":  "TGTTTAC",
    "PAX6":   "TTCACGC",
    "LHX":    "TAATTAA",
    "TBR1":   "TCTAGGTGT",
    "PHOX2":  "TAATTG",
    "NRSF":   "TCCTGGACAGCGCC",  # REST repressor in non-neural
}

KEYS = list(MOTIFS.keys())
COMP = {ord("A"): "T", ord("C"): "G", ord("G"): "C", ord("T"): "A"}


def revcomp(s):
    return s.translate(COMP)[::-1]


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    alpha = np.array(list("ACGT"))
    bb_idx = rng.integers(0, 4, size=(N, L))
    backbone = ["".join(alpha[r].tolist()) for r in bb_idx]
    n_inserts = rng.integers(15, 26, size=N)
    seqs = []
    for i in range(N):
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
        seqs.append("".join(b))
    with open(OUT, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")
    print(f"wrote {N} seqs in {time.time()-t0:.1f}s; "
          f"mean inserts={n_inserts.mean():.1f}")


if __name__ == "__main__":
    main()
