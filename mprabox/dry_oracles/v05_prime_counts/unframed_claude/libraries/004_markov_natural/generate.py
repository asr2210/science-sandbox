#!/usr/bin/env python3
"""Order-2 Markov chain trained on approximate human dinucleotide
frequencies. Reproduces AT-bias and CpG depletion of the human
genome, which should be more in-distribution for human-trained
sequence models than uniform random."""

import numpy as np
import os

N_SEQ = 50_000
LEN = 200
SEED = 4
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

# Approximate human dinucleotide frequencies (percent of all dinucs)
# Sources: standard human genome stats, see
# Ewens & Grant "Statistical Methods in Bioinformatics" etc.
# Rows = first base, cols = second base; ordering A,C,G,T.
DINUC = np.array([
    [9.5, 5.2, 7.1, 7.5],   # A.
    [7.3, 5.2, 1.0, 7.1],   # C.
    [5.8, 4.1, 5.2, 5.2],   # G.
    [5.7, 5.8, 7.3, 9.5],   # T.
], dtype=float)

# Convert to transition matrix P(next | prev)
TRANS = DINUC / DINUC.sum(axis=1, keepdims=True)
# Marginal of first base
MARG = DINUC.sum(axis=1) / DINUC.sum()

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
ix = {b: i for i, b in enumerate("ACGT")}

def make_seq():
    out = np.empty(LEN, dtype=np.int64)
    out[0] = rng.choice(4, p=MARG)
    for i in range(1, LEN):
        out[i] = rng.choice(4, p=TRANS[out[i-1]])
    return "".join(bases[out].tolist())

with open(OUT, "w") as f:
    for _ in range(N_SEQ):
        f.write(make_seq() + "\n")

print(f"Wrote {N_SEQ} Markov-natural sequences of length {LEN} to {OUT}")
