#!/usr/bin/env python3
"""Markov: always change base (no self-transitions).

Marginal composition stays balanced. Dinucleotides "00","11","22","33" forbidden.
Other 12 dinucleotides over-represented uniformly.
Mirror of experiment 003 (STAY=0.55).
"""
import random
import os

random.seed(42)

N = 50000
L = 200

others_by_base = {b: [c for c in "0123" if c != b] for b in "0123"}

def make_seq(length: int) -> str:
    prev = random.choice("0123")
    out = [prev]
    for _ in range(length - 1):
        prev = random.choice(others_by_base[prev])
        out.append(prev)
    return "".join(out)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for _ in range(N):
        f.write(make_seq(L) + "\n")

print(f"Wrote {N} no-self-transition Markov sequences to {out_path}")
