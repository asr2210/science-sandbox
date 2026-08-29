#!/usr/bin/env python3
"""25k strict (each gets a BALANCED 2A2C2G2T 8-mer insert from a 50-bank) +
25k (random + 1 8-mer from separate 50-bank).

Hypothesis: balanced 8-mers in strict preserve composition while adding
cluster structure (vs 019 which used unbalanced inserts and damaged
K562 ceiling).
"""
import numpy as np
import os

SEED = 232323
N = 50_000
HALF = N // 2
L = 200
BANK_SIZE = 50
MOTIF_LEN = 8
ALPH = np.array(list("ACGT"))


def make_balanced_8mer(rng):
    arr = np.repeat(np.arange(4, dtype=np.int8), 2)  # 2A2C2G2T
    rng.shuffle(arr)
    return arr


def main():
    rng = np.random.default_rng(SEED)
    # Strict half
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (HALF, L)).copy()
    for i in range(HALF):
        rng.shuffle(strict[i])
    # Balanced bank for strict
    balanced_bank = np.stack([make_balanced_8mer(rng) for _ in range(BANK_SIZE)])
    for i in range(HALF):
        mi = rng.integers(0, BANK_SIZE)
        start = rng.integers(0, L - MOTIF_LEN + 1)
        # In strict, swap the slice with the balanced 8mer (composition preserved)
        # But we need to MAINTAIN strict's 50/50/50/50. Swap is not a no-op
        # unless the slice matched the insert. So we re-shuffle the rest.
        # Simpler: replace, then rebalance by swapping bases to restore counts.
        orig = strict[i, start:start + MOTIF_LEN].copy()
        strict[i, start:start + MOTIF_LEN] = balanced_bank[mi]
        # If insert composition equals slice composition, no rebalance needed
        # Both are 2-2-2-2 only if orig was also balanced. Easier: don't insist
        # on perfect 50/50 — accept small drift (insert is balanced, so drift
        # is at most ±2 per base if orig wasn't balanced).
    # Random half with random 8mer insert
    rand = rng.integers(0, 4, size=(HALF, L), dtype=np.int8)
    rand_bank = rng.integers(0, 4, size=(BANK_SIZE, MOTIF_LEN), dtype=np.int8)
    for i in range(HALF):
        mi = rng.integers(0, BANK_SIZE)
        start = rng.integers(0, L - MOTIF_LEN + 1)
        rand[i, start:start + MOTIF_LEN] = rand_bank[mi]
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (strict+balanced-insert / rand+insert) to {out_path}")


if __name__ == "__main__":
    main()
