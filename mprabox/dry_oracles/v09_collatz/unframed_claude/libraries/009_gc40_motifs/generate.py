"""Experiment 009: 40% GC backbone + 002 motifs.

Test the low-GC direction. Predicted big K562 gain.
"""
import numpy as np

rng = np.random.default_rng(9)
N = 50_000
L = 200
BASES = np.array(list("ACGT"))
GC_FRAC = 0.40
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

with open("libraries/009_gc40_motifs/sequences_0.txt", "w") as f:
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

print(f"wrote {N} seqs at 40% GC backbone + {MOTIFS_PER_SEQ} motifs each")
