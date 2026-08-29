#!/usr/bin/env python3
"""Diversity probe: 50,000 copies of one random sequence."""
import numpy as np
import os

SEED = 17
N = 50_000
L = 200
ALPH = np.array(list("ACGT"))

def main():
    rng = np.random.default_rng(SEED)
    one = ALPH[rng.integers(0, 4, size=L, dtype=np.int8)]
    seq = "".join(one.tolist())
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for _ in range(N):
            f.write(seq + "\n")
    print(f"Wrote {N} identical 200-bp copies to {out_path}")

if __name__ == "__main__":
    main()
