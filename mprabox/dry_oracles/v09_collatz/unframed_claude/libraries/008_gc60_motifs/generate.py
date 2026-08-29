"""Experiment 008: GC content probe — 60% GC backbone + 002 motifs.

Single-variable change vs 002: backbone bases are sampled with 30% G,
30% C, 20% A, 20% T (= 60% GC) instead of uniform 25% each (= 50% GC).
Tests whether higher GC backbone moves K562 (stuck at 0.13).
"""
import numpy as np

rng = np.random.default_rng(8)
N = 50_000
L = 200
BASES = np.array(list("ACGT"))
GC_FRAC = 0.60
# A, C, G, T
PROBS = np.array([(1 - GC_FRAC) / 2,
                  GC_FRAC / 2,
                  GC_FRAC / 2,
                  (1 - GC_FRAC) / 2])

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

MOTIFS_PER_SEQ = 6

with open("libraries/008_gc60_motifs/sequences_0.txt", "w") as f:
    for _ in range(N):
        idx = rng.choice(4, size=L, p=PROBS)
        seq = list(BASES[idx])
        chosen = rng.choice(len(MOTIFS), size=MOTIFS_PER_SEQ, replace=True)
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

print(f"wrote {N} seqs at 60% GC backbone + {MOTIFS_PER_SEQ} motifs each")
