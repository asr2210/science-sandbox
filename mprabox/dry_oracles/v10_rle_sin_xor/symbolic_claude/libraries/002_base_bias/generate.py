#!/usr/bin/env python3
"""Probe single-base compositional sensitivity.

4 groups of 12500 sequences. Each enriched (~80%) for one of 4 bases.
"""
import random
import os

random.seed(42)

N = 50000
L = 200
GROUP_SIZE = N // 4  # 12500 per group
ENRICHED_P = 0.80   # 80% enriched base, ~6.67% other bases

def make_seq(enriched_base: str, length: int) -> str:
    others = [c for c in "0123" if c != enriched_base]
    out = []
    for _ in range(length):
        if random.random() < ENRICHED_P:
            out.append(enriched_base)
        else:
            out.append(random.choice(others))
    return "".join(out)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for base in "0123":
        for _ in range(GROUP_SIZE):
            f.write(make_seq(base, L) + "\n")

print(f"Wrote {N} sequences (4 groups of {GROUP_SIZE}) to {out_path}")
