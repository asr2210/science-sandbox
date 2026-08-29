#!/usr/bin/env python3
"""Ratio sweep: 17k strict + 33k random (random-heavy)."""
import numpy as np
import os

SEED = 11111
N = 50_000
N_STRICT = 16_667
N_RANDOM = N - N_STRICT
L = 200
ALPH = np.array(list("ACGT"))


def main():
    rng = np.random.default_rng(SEED)
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (N_STRICT, L)).copy()
    for i in range(N_STRICT):
        rng.shuffle(strict[i])
    rand = rng.integers(0, 4, size=(N_RANDOM, L), dtype=np.int8)
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (strict {N_STRICT} / random {N_RANDOM}) to {out_path}")


if __name__ == "__main__":
    main()
