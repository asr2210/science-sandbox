#!/usr/bin/env python3
"""All sequences are reverse-complement palindromes.

Assuming alphabet maps to DNA bases with complement pairing 0<->3, 1<->2.
First 100 chars random, last 100 = reverse complement of first 100.
Each sequence's full length = 200, palindromic.

Tests if palindromic structure unlocks condition_c.
"""
import random
import os

random.seed(42)

N = 50000
L = 200
HALF = L // 2
ALPHA = "0123"
COMP = {"0": "3", "3": "0", "1": "2", "2": "1"}

def rev_comp(s: str) -> str:
    return "".join(COMP[c] for c in reversed(s))

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        half = "".join(random.choice(ALPHA) for _ in range(HALF))
        seq = half + rev_comp(half)
        f.write(seq + "\n")

print(f"Wrote {N} palindromic sequences (rev-comp 0<->3, 1<->2) to {out_path}")
