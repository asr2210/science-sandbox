"""Exp 007: insert canonical TFBS motifs (mapping A=0, C=1, G=2, T=3).

Hypothesis: if the scorer is a CNN-based DNA model trained on real biological data,
canonical TFBS motifs (TATA box, Sp1, NF-Y, CRE, E-box, etc.) will be recognized as
activating, creating strong prediction variance correlated with target variance.

Each sequence: random uniform background, K ~ U{0,15} known motifs inserted at random
non-overlapping positions.
"""
import os
import numpy as np

N = 50_000
L = 200
MAX_K = 15
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

# Map: A=0, C=1, G=2, T=3 (guess; biologists also use ACGT order alphabetically)
def s2arr(s):
    m = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    return np.array([m[c] for c in s], dtype=np.int8)

# 10 canonical TFBS motifs (forward + reverse-complement variants)
motif_strs = [
    "TATAAA",   # TATA box
    "TTTATA",   # rev-comp TATA
    "CCAAT",    # NF-Y (CCAAT box)
    "ATTGG",    # rev-comp CCAAT
    "GGGCGG",   # Sp1
    "CCGCCC",   # rev-comp Sp1
    "TGACGT",   # CRE
    "ACGTCA",   # rev-comp CRE
    "CACGTG",   # E-box (palindrome)
    "AGGTCA",   # NR half-site
    "TGACCT",   # rev-comp NR
    "GCCACGTGGC", # extended E-box context
    "TGACTCA",  # AP-1 / Nrf2
    "TGAGTCA",  # rev-comp AP-1
]
motif_lib = [s2arr(s) for s in motif_strs]
print(f"Motif lib: {len(motif_lib)} motifs, lengths {[len(m) for m in motif_lib]}")

rng = np.random.default_rng(7)
seqs = rng.integers(0, 4, size=(N, L), dtype=np.int8)
Ks = rng.integers(0, MAX_K + 1, size=N)
n_lib = len(motif_lib)

for i in range(N):
    K = int(Ks[i])
    if K == 0:
        continue
    occupied = np.zeros(L, dtype=bool)
    placed = 0
    tries = 0
    while placed < K and tries < 5 * K:
        midx = int(rng.integers(0, n_lib))
        m = motif_lib[midx]
        s = int(rng.integers(0, L - len(m) + 1))
        if not occupied[s:s + len(m)].any():
            seqs[i, s:s + len(m)] = m
            occupied[s:s + len(m)] = True
            placed += 1
        tries += 1

seqs += ord('0')
with open(OUT, "wb") as f:
    for i in range(N):
        f.write(bytes(seqs[i].tolist()))
        f.write(b"\n")
print(f"Wrote {N} sequences with TFBS motif injection to {OUT}")
print(f"Avg K (target) per seq: {Ks.mean():.2f}")
