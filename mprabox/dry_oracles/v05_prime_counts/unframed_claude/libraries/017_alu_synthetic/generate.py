#!/usr/bin/env python3
"""Synthetic AluY-derived sequences (200bp).

Take AluY consensus (~300bp), random 200bp segment, mutate at
~15% (typical Alu divergence). Tests if Alu specifically drives
eval_01 signal (Alu = ~10% of human genome, harbors TFBSs)."""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 17
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "sequences_0.txt")

# AluY consensus (Repbase), ~311bp
ALUY = (
    "GGCCGGGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGGCGGGCGGAT"
    "CACGAGGTCAGGAGATCGAGACCATCCCGGCTAAAACGGTGAAACCCCGTCTCTACTAAAA"
    "ATACAAAAAATTAGCCGGGCGTGGTGGCGGGCGCCTGTAGTCCCAGCTACTCGGGAGGCTG"
    "AGGCAGGAGAATGGCGTGAACCCGGGAGGCGGAGCTTGCAGTGAGCCGAGATCGCGCCACT"
    "GCACTCCAGCCTGGGCGACAGAGCGAGACTCCGTCTCAAAAAAAA"
)
print(f"AluY length: {len(ALUY)}")

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
alu = np.array(list(ALUY))
L_ALU = len(ALUY)
MUT_RATE = 0.15

seqs = []
for _ in range(N_SEQ):
    start = int(rng.integers(0, L_ALU - LEN + 1))
    s = alu[start:start + LEN].copy()
    # Mutate at MUT_RATE
    mask = rng.random(LEN) < MUT_RATE
    n_mut = int(mask.sum())
    if n_mut:
        s[mask] = bases[rng.integers(0, 4, size=n_mut)]
    seqs.append("".join(s.tolist()))

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} AluY-synthetic sequences (mut rate {MUT_RATE})")
