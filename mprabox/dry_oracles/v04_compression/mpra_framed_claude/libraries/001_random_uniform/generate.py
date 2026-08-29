"""Experiment 001: pure random uniform DNA — baseline floor.

50,000 sequences of 200bp, each base uniformly random from {A, C, G, T}.
This tests: how much signal can a model extract from sequences with no
regulatory grammar? Any predictive ability above chance must come from
length/composition effects alone.
"""
import os
import numpy as np

N_SEQ = 50_000
L = 200
SEED = 0

ALPHABET = np.array(list("ACGT"))


def main():
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, 4, size=(N_SEQ, L), dtype=np.int8)
    seqs = ["".join(ALPHABET[row]) for row in idx]

    out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out, "w") as f:
        f.write("\n".join(seqs))
        f.write("\n")

    assert len(seqs) == N_SEQ
    assert all(len(s) == L for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:100])
    print(f"wrote {N_SEQ} sequences x {L}bp to {out}")


if __name__ == "__main__":
    main()
