#!/usr/bin/env python3
"""3-mode: 25k strict + 12.5k pure random + 12.5k (random + 1 8-mer from
50-bank). Tests whether sub-structuring the random half (some with insert,
some without) adds productive diversity.
"""
import numpy as np
import os

SEED = 222222
N = 50_000
N_STRICT = 25_000
N_RAND = 12_500
N_INS = 12_500
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
    pure_rand = rng.integers(0, 4, size=(N_RAND, L), dtype=np.int8)
    ins_rand = rng.integers(0, 4, size=(N_INS, L), dtype=np.int8)
    bank = rng.integers(0, 4, size=(BANK_SIZE, MOTIF_LEN), dtype=np.int8)
    for i in range(N_INS):
        mi = rng.integers(0, BANK_SIZE)
        start = rng.integers(0, L - MOTIF_LEN + 1)
        ins_rand[i, start:start + MOTIF_LEN] = bank[mi]
    seqs = np.concatenate([strict, pure_rand, ins_rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (3-mode strict+rand+ins-rand) to {out_path}")


if __name__ == "__main__":
    main()
