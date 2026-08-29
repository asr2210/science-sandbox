"""Experiment 003: composition split.

Split 50,000 into 4 chunks of 12,500. Within each chunk, each sequence
is iid drawn with one character enriched at 70% (others at 10% each).
- Chunk 0: 70% '0' / 10% each others
- Chunk 1: 70% '1' / 10% each others
- Chunk 2: 70% '2' / 10% each others
- Chunk 3: 70% '3' / 10% each others

Overall composition equals uniform (25% each), but each sequence is
heavily skewed in composition. Tests whether scoring rewards/punishes
within-sequence composition skew vs uniform random baseline (001 = 0.42).
"""
import numpy as np

N = 50_000
L = 200
chunk = N // 4
rng = np.random.default_rng(123)

with open("sequences_0.txt", "w") as f:
    for enriched in range(4):
        p = np.array([0.1, 0.1, 0.1, 0.1])
        p[enriched] = 0.7
        for _ in range(chunk):
            seq = rng.choice(4, size=L, p=p)
            f.write("".join(chr(48 + c) for c in seq))
            f.write("\n")

print(f"Wrote {N} sequences of length {L}")
