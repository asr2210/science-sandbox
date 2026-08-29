#!/usr/bin/env python3
"""Each sequence has 5 different balanced 8-mer motifs inserted at random positions.

Tests if heavy motif content moves any condition.
Motifs are different permutations of 2-of-each-base 8-mers.
"""
import random
import os

random.seed(42)

N = 50000
L = 200
ALPHA = "0123"

# 5 distinct balanced 8-mers (each has 2 of each base)
MOTIFS = ["01230123", "32103210", "01322310", "23011032", "10322031"]
M = 8

def make_seq(length: int) -> str:
    seq = [random.choice(ALPHA) for _ in range(length)]
    # Insert each motif at a random non-overlapping position
    positions = sorted(random.sample(range(length - M + 1), len(MOTIFS)))
    # Reject if overlapping
    while any(positions[i + 1] - positions[i] < M for i in range(len(positions) - 1)):
        positions = sorted(random.sample(range(length - M + 1), len(MOTIFS)))
    for pos, motif in zip(positions, MOTIFS):
        for i, c in enumerate(motif):
            seq[pos + i] = c
    return "".join(seq)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(make_seq(L) + "\n")

print(f"Wrote {N} sequences with 5 motifs each ({len(MOTIFS) * M} structured chars) to {out_path}")
