#!/usr/bin/env python3
"""Markov chain with dinucleotide '12' depleted (DNA CpG-style).

Doubly stochastic matrix → marginal stays uniform 25% each.
Dinucleotide '12' has frequency ~2.5% vs uniform 6.25%.
Tests whether specific dinucleotide bias matching natural DNA helps c.
"""
import random
import os

random.seed(42)

N = 50000
L = 200

# Doubly stochastic transition matrix, rows are "from", cols "to"
P = [
    [0.25, 0.25, 0.25, 0.25],
    [0.30, 0.30, 0.10, 0.30],
    [0.25, 0.25, 0.30, 0.20],
    [0.20, 0.20, 0.35, 0.25],
]

def sample_next(prev: int) -> int:
    row = P[prev]
    r = random.random()
    cum = 0.0
    for i, p in enumerate(row):
        cum += p
        if r < cum:
            return i
    return 3

def make_seq(length: int) -> str:
    prev = random.randrange(4)
    out = [str(prev)]
    for _ in range(length - 1):
        prev = sample_next(prev)
        out.append(str(prev))
    return "".join(out)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(make_seq(L) + "\n")

print(f"Wrote {N} sequences with depleted '12' dinucleotide to {out_path}")
