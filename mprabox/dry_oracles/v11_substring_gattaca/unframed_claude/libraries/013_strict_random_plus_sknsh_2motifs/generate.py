#!/usr/bin/env python3
"""25k strict + 25k random with 2 SK-N-SH motifs each. Tests motif-dose
amplification."""
import numpy as np
import os

SEED = 44444
N = 50_000
HALF = N // 2
L = 200
N_MOTIFS = 2
ALPH = np.array(list("ACGT"))
ALPH_TO_IDX = {b: i for i, b in enumerate("ACGT")}

SKNSH_MOTIFS = ["TTCAGCACCATGGACAG", "CACCTG", "CAGCTG"]
MOTIF_IDX = [np.array([ALPH_TO_IDX[c] for c in m], dtype=np.int8) for m in SKNSH_MOTIFS]


def main():
    rng = np.random.default_rng(SEED)
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    strict = np.broadcast_to(base, (HALF, L)).copy()
    for i in range(HALF):
        rng.shuffle(strict[i])
    rand = rng.integers(0, 4, size=(HALF, L), dtype=np.int8)
    for i in range(HALF):
        chosen = rng.choice(len(MOTIF_IDX), size=N_MOTIFS, replace=True)
        used = []
        for mi in chosen:
            m = MOTIF_IDX[mi]
            for _ in range(20):
                start = rng.integers(0, L - m.size + 1)
                end = start + m.size
                if all(end <= s or start >= e for s, e in used):
                    rand[i, start:end] = m
                    used.append((start, end))
                    break
    seqs = np.concatenate([strict, rand], axis=0)
    seqs = seqs[rng.permutation(N)]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} seqs to {out_path}")


if __name__ == "__main__":
    main()
