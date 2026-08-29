#!/usr/bin/env python3
"""25k strict + 25k random-with-1-SKNSH-motif. Replace the random half of
007 with random-bg + a single SK-N-SH-relevant motif per sequence (REST,
CACCTG, CAGCTG). Targets SK-N-SH lift without 1/3-motif HepG2 collapse.
"""
import numpy as np
import os

SEED = 33333
N = 50_000
HALF = N // 2
L = 200
ALPH = np.array(list("ACGT"))
ALPH_TO_IDX = {b: i for i, b in enumerate("ACGT")}

SKNSH_MOTIFS = [
    "TTCAGCACCATGGACAG",  # REST/NRSE
    "CACCTG",             # E-box NEUROG
    "CAGCTG",             # E-box ASCL1
]
MOTIF_IDX = [np.array([ALPH_TO_IDX[c] for c in m], dtype=np.int8) for m in SKNSH_MOTIFS]


def main():
    rng = np.random.default_rng(SEED)
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (HALF, L)).copy()
    for i in range(HALF):
        rng.shuffle(strict[i])
    # random + 1 SKNSH motif per seq
    rand = rng.integers(0, 4, size=(HALF, L), dtype=np.int8)
    for i in range(HALF):
        mi = rng.integers(0, len(MOTIF_IDX))
        m = MOTIF_IDX[mi]
        start = rng.integers(0, L - m.size + 1)
        rand[i, start:start + m.size] = m
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} (25k strict + 25k random-with-1-SKNSH-motif) to {out_path}")


if __name__ == "__main__":
    main()
