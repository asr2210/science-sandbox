"""Experiment 011: pure replication of 002 with different seed.

Tests noise floor. If 011 ≈ 002, the 0.27 score is robust and additions hurt.
If 011 differs, noise is large and conclusions are loose.
"""
import numpy as np

rng = np.random.default_rng(100)  # different from 002's seed 2
N = 50_000
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
MOTIFS_PER_SEQ = 6

with open("libraries/011_replicate_002/sequences_0.txt", "w") as f:
    for _ in range(N):
        seq = list(BASES[rng.integers(0, 4, size=L)])
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
print("wrote 002 replicate with seed 100")
