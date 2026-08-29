#!/usr/bin/env python3
"""Three-way mix: 16,667 strict + 16,667 random + 16,666 motif-augmented.
Tests if adding a third design mode further improves over 007's two-way.
"""
import numpy as np
import os

SEED = 24680
N = 50_000
THIRD = N // 3 + 1  # 16,667
L = 200
N_MOTIFS_PER = 3
ALPH = np.array(list("ACGT"))
ALPH_TO_IDX = {b: i for i, b in enumerate("ACGT")}

MOTIFS = [
    "AGATAAG", "CCACGCCC", "TGACTCAG",
    "CAAAGTCCA", "GTTAATGATTAAC", "ATTGCGCAAT",
    "TTCAGCACCATGGACAG", "CACCTG", "CAGCTG",
    "TATAAAA", "CCAATCT", "GGGCGGG",
    "TGACGTCA", "TGAGTCA", "GGGACTTTCC", "CACGTG",
]
MOTIF_IDX = [np.array([ALPH_TO_IDX[c] for c in m], dtype=np.int8) for m in MOTIFS]


def make_strict(n, rng):
    base = np.repeat(np.arange(4, dtype=np.int8), L // 4)
    out = np.broadcast_to(base, (n, L)).copy()
    for i in range(n):
        rng.shuffle(out[i])
    return out


def make_random(n, rng):
    return rng.integers(0, 4, size=(n, L), dtype=np.int8)


def make_motif(n, rng):
    out = rng.integers(0, 4, size=(n, L), dtype=np.int8)
    for i in range(n):
        chosen = rng.choice(len(MOTIFS), size=N_MOTIFS_PER, replace=False)
        used = []
        for mi in chosen:
            m = MOTIF_IDX[mi]
            mlen = m.size
            for _ in range(20):
                start = rng.integers(0, L - mlen + 1)
                end = start + mlen
                if all(end <= s or start >= e for s, e in used):
                    out[i, start:end] = m
                    used.append((start, end))
                    break
    return out


def main():
    rng = np.random.default_rng(SEED)
    s = make_strict(THIRD, rng)
    r = make_random(THIRD, rng)
    m = make_motif(N - 2 * THIRD, rng)
    seqs = np.concatenate([s, r, m], axis=0)
    order = rng.permutation(N)
    seqs = seqs[order]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in ALPH[seqs]:
            f.write("".join(row.tolist()))
            f.write("\n")
    print(f"Wrote {N} three-way-mix seqs (strict {s.shape[0]} / "
          f"random {r.shape[0]} / motif {m.shape[0]}) to {out_path}")


if __name__ == "__main__":
    main()
