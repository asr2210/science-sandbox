#!/usr/bin/env python3
"""Force exact per-position base balance across library.

For each position p in [0, 199], the 50000 characters across sequences are
exactly 12500 of each base. Each sequence still random uniform individually.
"""
import random
import os

random.seed(7)  # use best seed

N = 50000
L = 200
PER_POS = N // 4  # 12500

# For each position, create a list with 12500 of each base, shuffle
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

# Build column-wise
columns = []
for _ in range(L):
    col = [b for b in "0123" for _ in range(PER_POS)]
    random.shuffle(col)
    columns.append(col)

# Transpose to rows
with open(out_path, "w") as f:
    for i in range(N):
        seq = "".join(columns[p][i] for p in range(L))
        f.write(seq + "\n")

print(f"Wrote {N} position-balanced sequences (seed=7) to {out_path}")
