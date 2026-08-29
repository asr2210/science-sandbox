#!/usr/bin/env python3
"""Markov with mild anti-self bias (STAY=0.20).

Slightly under-represents same-base dinucleotides. Marginals balanced.
"""
import random
import os

random.seed(42)

N = 50000
L = 200
STAY = 0.20

others_by_base = {b: [c for c in "0123" if c != b] for b in "0123"}

def make_seq(length: int) -> str:
    prev = random.choice("0123")
    out = [prev]
    for _ in range(length - 1):
        if random.random() < STAY:
            out.append(prev)
        else:
            prev = random.choice(others_by_base[prev])
            out.append(prev)
    return "".join(out)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(make_seq(L) + "\n")

print(f"Wrote {N} Markov (STAY={STAY}) sequences to {out_path}")
