#!/usr/bin/env python3
"""Markov chain with self-transition bias.

Marginal composition stays balanced (uniform stationary distribution),
but sequences have runs (long same-base stretches).

Transition: stay at same base with prob STAY, else uniform over other 3.
With STAY=0.55, expected run length is 1/(1-0.55)≈2.2.
"""
import random
import os

random.seed(42)

N = 50000
L = 200
STAY = 0.55

def make_seq(length: int) -> str:
    prev = random.choice("0123")
    out = [prev]
    others_by_base = {b: [c for c in "0123" if c != b] for b in "0123"}
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

print(f"Wrote {N} Markov-run sequences (STAY={STAY}) to {out_path}")
