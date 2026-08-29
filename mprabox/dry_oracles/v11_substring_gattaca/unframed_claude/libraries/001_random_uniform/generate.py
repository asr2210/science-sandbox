#!/usr/bin/env python3
"""Random uniform 25% baseline: 50,000 x 200bp sequences."""
import numpy as np
import os

SEED = 42
N = 50_000
L = 200
ALPH = np.array(list("ACGT"))

def main():
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    seqs = ALPH[idx]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in seqs:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} sequences of length {L} to {out_path}")

if __name__ == "__main__":
    main()
