#!/usr/bin/env python3
"""25k strict + 12.5k (random + 1 K562-motif from 3-bank) + 12.5k (random
+ 1 8-mer from 50-bank).

Tests if SKNSH-lift from 014's small structured bank and K562-lift from
017's larger random bank can stack.
"""
import numpy as np
import os

SEED = 252525
N = 50_000
N_STRICT = 25_000
N_MOTIF = 12_500
N_RAND_BANK = 12_500
L = 200
BANK_SIZE = 50
MOTIF_LEN = 8
ALPH = np.array(list("ACGT"))
ALPH_TO_IDX = {b: i for i, b in enumerate("ACGT")}

K562_MOTIFS = [
    "AGATAAG",
    "CCACGCCC",
    "TGACTCAG",
]
MOTIF_IDX = [np.array([ALPH_TO_IDX[c] for c in m], dtype=np.int8) for m in K562_MOTIFS]


def main():
    rng = np.random.default_rng(SEED)
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (N_STRICT, L)).copy()
    for i in range(N_STRICT):
        rng.shuffle(strict[i])

    rand_motif = rng.integers(0, 4, size=(N_MOTIF, L), dtype=np.int8)
    for i in range(N_MOTIF):
        mi = rng.integers(0, len(MOTIF_IDX))
        m = MOTIF_IDX[mi]
        start = rng.integers(0, L - m.size + 1)
        rand_motif[i, start:start + m.size] = m

    rand_bank = rng.integers(0, 4, size=(N_RAND_BANK, L), dtype=np.int8)
    bank = rng.integers(0, 4, size=(BANK_SIZE, MOTIF_LEN), dtype=np.int8)
    for i in range(N_RAND_BANK):
        mi = rng.integers(0, BANK_SIZE)
        start = rng.integers(0, L - MOTIF_LEN + 1)
        rand_bank[i, start:start + MOTIF_LEN] = bank[mi]

    seqs = np.concatenate([strict, rand_motif, rand_bank], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs (014+017 mix) to {out_path}")


if __name__ == "__main__":
    main()
