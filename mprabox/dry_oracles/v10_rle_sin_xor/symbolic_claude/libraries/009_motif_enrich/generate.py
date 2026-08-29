#!/usr/bin/env python3
"""Random + balanced 8-mer motif "01230123" inserted twice per sequence at random positions.

Tests if motif enrichment moves any condition (especially c).
"01230123" has 2 each of bases 0,1,2,3.
"""
import random
import os

random.seed(42)

N = 50000
L = 200
ALPHA = "0123"
MOTIF = "01230123"
M = len(MOTIF)

def make_seq(length: int) -> str:
    seq = [random.choice(ALPHA) for _ in range(length)]
    # Insert MOTIF twice at random non-overlapping positions
    pos1 = random.randint(0, length - 2 * M - 1)
    pos2 = random.randint(pos1 + M, length - M)
    for i, c in enumerate(MOTIF):
        seq[pos1 + i] = c
        seq[pos2 + i] = c
    return "".join(seq)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(make_seq(L) + "\n")

print(f"Wrote {N} sequences with motif '{MOTIF}' x2 per seq to {out_path}")
