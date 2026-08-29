"""Experiment 005: mixed-density library — test the variance hypothesis.

Build a library where each subset has different motif density:
  10,000 seqs with 0 motifs (pure random)
  10,000 seqs with 3 motifs
  10,000 seqs with 6 motifs
  10,000 seqs with 9 motifs
  10,000 seqs with 12 motifs

If mean_r is correlation between predicted activity and a target signal,
high cross-library variance in motif content should produce strong correlation.
Goal: beat 002's 0.2675.
"""
import numpy as np

rng = np.random.default_rng(5)
N_PER_BUCKET = 10_000
L = 200
BASES = np.array(list("ACGT"))

MOTIFS = [
    "TGAGTCA",
    "TGACGTCA",
    "GGGGCGGGG",
    "ACAGGAAGT",
    "CCAATCG",
    "CAAAGGTCA",
    "GTTAATCATTAAC",
    "AGATAAG",
    "CACCC",
    "CAGCTG",
]

DENSITIES = [0, 3, 6, 9, 12]

with open("libraries/005_mixed_density/sequences_0.txt", "w") as f:
    for density in DENSITIES:
        for _ in range(N_PER_BUCKET):
            seq = list(BASES[rng.integers(0, 4, size=L)])
            if density > 0:
                chosen = rng.choice(len(MOTIFS), size=density, replace=True)
                used = []
                for mi in chosen:
                    m = MOTIFS[mi]
                    ml = len(m)
                    for _try in range(20):
                        pos = int(rng.integers(0, L - ml + 1))
                        if all(pos + ml <= s or pos >= e for s, e in used):
                            used.append((pos, pos + ml))
                            for j, ch in enumerate(m):
                                seq[pos + j] = ch
                            break
            f.write("".join(seq) + "\n")

print(f"wrote {N_PER_BUCKET * len(DENSITIES)} sequences across densities {DENSITIES}")
