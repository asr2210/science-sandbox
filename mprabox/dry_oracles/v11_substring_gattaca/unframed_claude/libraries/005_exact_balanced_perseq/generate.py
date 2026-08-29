#!/usr/bin/env python3
"""Strict per-sequence balanced composition: each sequence contains exactly
50 A, 50 C, 50 G, 50 T arranged in a random order. Tests if pinning
per-seq composition (zero Poisson variance) helps relative to random uniform.
"""
import numpy as np
import os

SEED = 31415
N = 50_000
L = 200
ALPH = np.array(list("ACGT"))

def main():
    rng = np.random.default_rng(SEED)
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)  # 50A,50C,50G,50T
    assert base.size == L
    seqs = np.broadcast_to(base, (N, L)).copy()
    # in-place independent shuffles per row
    for i in range(N):
        rng.shuffle(seqs[i])
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} balanced-composition seqs to {out_path}")

if __name__ == "__main__":
    main()
