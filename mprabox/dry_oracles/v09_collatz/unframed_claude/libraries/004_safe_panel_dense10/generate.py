"""Experiment 004: 002's safe panel at density 10.

Disentangle whether 003's regression came from (H1) higher density or
(H2) new harmful motifs. Hold panel fixed at the 002 working set; only
increase density.
"""
import numpy as np

rng = np.random.default_rng(4)
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

MOTIFS_PER_SEQ = 10

with open("libraries/004_safe_panel_dense10/sequences_0.txt", "w") as f:
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

print(f"wrote {N} sequences with {MOTIFS_PER_SEQ} motifs each from safe 10-panel")
