"""005 — Natural-looking sequences via dinucleotide Markov chain.

Uses approximate human-genome dinucleotide transition probabilities.
CpG is strongly suppressed in mammalian non-island regions.

Hypothesis: if the scorer was trained on natural sequences, sequences with
realistic dinucleotide bias should score higher than uniform random.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(5)
N, L = 50_000, 200
BASES = list("ACGT")

# Approximate human-genome dinucleotide frequencies (Lander 2001 etc.)
# Each row sums to 1: row=previous base, col=next base
# Order: A C G T
TRANS = np.array([
    # next A    C     G     T   (after A)
    [0.30, 0.20, 0.29, 0.21],  # A -> _
    [0.32, 0.27, 0.07, 0.34],  # C -> _ (CG strongly suppressed)
    [0.27, 0.23, 0.25, 0.25],  # G -> _
    [0.18, 0.24, 0.29, 0.29],  # T -> _
])
# Approximate starting freq
START = np.array([0.295, 0.205, 0.205, 0.295])
B2I = {b: i for i, b in enumerate(BASES)}

cumT = np.cumsum(TRANS, axis=1)
cumS = np.cumsum(START)

def sample_seq():
    u = rng.random(L)
    out = np.empty(L, dtype=np.int8)
    out[0] = np.searchsorted(cumS, u[0])
    for i in range(1, L):
        prev = out[i-1]
        out[i] = np.searchsorted(cumT[prev], u[i])
    return "".join(BASES[k] for k in out)

# Vectorize the loop better: sample column-by-column? still O(NL) but in Python.
# 50k*200 = 10M ops; should run in ~30s in python. Use numpy more.
def batch_sample(n):
    states = np.empty((n, L), dtype=np.int8)
    u0 = rng.random(n)
    states[:, 0] = np.searchsorted(cumS, u0)
    for i in range(1, L):
        u = rng.random(n)
        prev = states[:, i-1]
        # For each row, use cumT[prev[row]] then searchsorted
        # vectorize: cum = cumT[prev]  shape (n,4); compare with u[:,None]
        cum = cumT[prev]
        states[:, i] = (u[:, None] > cum).sum(axis=1)
    return states

states = batch_sample(N)
seqs = np.array(BASES)[states]
out = Path(__file__).parent / "sequences_0.txt"
with open(out, "w") as f:
    f.write("\n".join("".join(row) for row in seqs) + "\n")

print(f"wrote {N} sequences to {out}")
