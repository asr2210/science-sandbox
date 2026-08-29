#!/usr/bin/env python3
"""Uniform random background with 3 inserted regulatory motifs per sequence.
Motif basket covers K562/HepG2/SK-N-SH-relevant TFs plus universal motifs.

Motifs are inserted at random positions (non-overlapping). 3 motifs of avg
length ~8 = 24 bp of "structured" out of 200 bp = ~12% biased composition,
85%+ random background.
"""
import numpy as np
import os

SEED = 91011
N = 50_000
L = 200
N_MOTIFS_PER = 3
ALPH = np.array(list("ACGT"))
ALPH_TO_IDX = {b: i for i, b in enumerate("ACGT")}

# Strong, canonical TF binding sites; consensus forms. IUPAC codes resolved
# to single canonical bases (no degenerate codes in inserts).
MOTIFS = [
    # K562 / erythroid
    "AGATAAG",        # GATA1
    "CCACGCCC",       # KLF1 GC-box
    "TGACTCAG",       # NFE2-like AP-1
    # HepG2 / liver
    "CAAAGTCCA",      # HNF4 half-site
    "GTTAATGATTAAC",  # HNF1
    "ATTGCGCAAT",     # C/EBP
    # SK-N-SH / neuronal
    "TTCAGCACCATGGACAG",  # REST/NRSE (full)
    "CACCTG",         # E-box (NEUROG/ASCL1)
    "CAGCTG",         # E-box variant
    # Universal promoter/enhancer
    "TATAAAA",        # TATA
    "CCAATCT",        # CCAAT
    "GGGCGGG",        # Sp1 / GC box
    "TGACGTCA",       # CREB
    "TGAGTCA",        # AP-1
    "GGGACTTTCC",     # NF-kB
    "CACGTG",         # MYC E-box
]
MOTIF_IDX = [np.array([ALPH_TO_IDX[c] for c in m], dtype=np.int8) for m in MOTIFS]

def main():
    rng = np.random.default_rng(SEED)
    # background: uniform random
    seqs = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    # for each sequence, choose 3 distinct motifs and place them non-overlapping
    for i in range(N):
        chosen = rng.choice(len(MOTIFS), size=N_MOTIFS_PER, replace=False)
        # try greedy non-overlapping placement
        used = []  # list of (start, end)
        for mi in chosen:
            m = MOTIF_IDX[mi]
            mlen = m.size
            for _ in range(20):
                start = rng.integers(0, L - mlen + 1)
                end = start + mlen
                if all(end <= s or start >= e for s, e in used):
                    seqs[i, start:end] = m
                    used.append((start, end))
                    break
            # if not placed in 20 tries, give up silently
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    flat = seqs.ravel()
    base_pct = np.bincount(flat, minlength=4) / flat.size
    print({"A": float(base_pct[0]), "C": float(base_pct[1]),
           "G": float(base_pct[2]), "T": float(base_pct[3])})
    print(f"Wrote {N} motif-augmented seqs to {out_path}")

if __name__ == "__main__":
    main()
