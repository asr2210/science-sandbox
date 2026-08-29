"""Experiment 010: each sequence has exactly 50/50/50/50 base composition.

Per-sequence equiprobable composition. Maintains per-column balance (each
column still has uniform expectations by symmetry). Tests whether killing
per-sequence GC sampling noise pushes scores higher.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
N, L = 50_000, 200
ALPHABET = np.array(list("ACGT"))

rng = np.random.default_rng(10)

base_row = np.repeat(np.arange(4, dtype=np.int8), L // 4)  # 50A 50C 50G 50T
matrix = np.empty((N, L), dtype=np.int8)
for i in range(N):
    matrix[i] = rng.permutation(base_row)

seqs = ["".join(ALPHABET[row]) for row in matrix]
# sanity
sample = seqs[0]
print(f"first seq composition: A={sample.count('A')} C={sample.count('C')} G={sample.count('G')} T={sample.count('T')}")
gc_lib = sum((s.count("C") + s.count("G")) for s in seqs[:2000]) / (2000 * L)
print(f"library GC (first 2000): {gc_lib:.4f}")

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {len(seqs)} sequences to {OUT}")
