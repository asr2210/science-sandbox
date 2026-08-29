#!/usr/bin/env python3
"""25k position-stratified (block-) strict + 25k (random + 1 8-mer 50-bank).

Position-stratified strict: each 4-bp block is a permutation of ACGT.
This gives every position-window the exact same per-base composition
(25% each in any 4-bp window). Stronger structural pattern than 017's
globally-balanced shuffle.

Hypothesis: tighter strict structure pushes K562/HepG2 above current
ceiling without losing SKNSH (random half unchanged).
"""
import numpy as np
import os

SEED = 262626
N = 50_000
HALF = N // 2
L = 200
BLOCK = 4
BANK_SIZE = 50
MOTIF_LEN = 8
ALPH = np.array(list("ACGT"))


def main():
    rng = np.random.default_rng(SEED)
    # Block-strict: build per-block permutations
    n_blocks = L // BLOCK
    block_perms = np.tile(np.arange(BLOCK, dtype=np.int8), (HALF, n_blocks, 1))
    # Shuffle each block independently
    for i in range(HALF):
        for b in range(n_blocks):
            rng.shuffle(block_perms[i, b])
    strict = block_perms.reshape(HALF, L)

    rand = rng.integers(0, 4, size=(HALF, L), dtype=np.int8)
    bank = rng.integers(0, 4, size=(BANK_SIZE, MOTIF_LEN), dtype=np.int8)
    for i in range(HALF):
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
    print(f"Wrote {N} seqs (4-block-strict + insert-rand) to {out_path}")


if __name__ == "__main__":
    main()
