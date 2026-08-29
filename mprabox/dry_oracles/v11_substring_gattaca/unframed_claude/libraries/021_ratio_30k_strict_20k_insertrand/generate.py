#!/usr/bin/env python3
"""30k strict + 20k (random + 1 8-mer from 50-bank). Ratio shift toward
strict — tests whether the insert lift allows a more strict-heavy mix.
"""
import numpy as np
import os

SEED = 212121
N = 50_000
N_STRICT = 30_000
N_RAND = N - N_STRICT
L = 200
BANK_SIZE = 50
MOTIF_LEN = 8
ALPH = np.array(list("ACGT"))


def main():
    rng = np.random.default_rng(SEED)
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (N_STRICT, L)).copy()
    for i in range(N_STRICT):
        rng.shuffle(strict[i])
    rand = rng.integers(0, 4, size=(N_RAND, L), dtype=np.int8)
    bank = rng.integers(0, 4, size=(BANK_SIZE, MOTIF_LEN), dtype=np.int8)
    for i in range(N_RAND):
        mi = rng.integers(0, BANK_SIZE)
        start = rng.integers(0, L - MOTIF_LEN + 1)
        rand[i, start:start + MOTIF_LEN] = bank[mi]
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (30k strict + 20k insert-rand) to {out_path}")


if __name__ == "__main__":
    main()
