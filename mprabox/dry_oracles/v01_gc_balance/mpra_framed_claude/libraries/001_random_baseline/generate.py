"""001_random_baseline: 50,000 uniformly random 200bp DNA sequences.

Establishes the noise floor. Each base i.i.d. uniform from {A,C,G,T}.
"""
import os
import numpy as np

RNG_SEED = 1
N = 50000
L = 200
ALPHABET = np.array(list("ACGT"))


def main():
    rng = np.random.default_rng(RNG_SEED)
    idx = rng.integers(0, 4, size=(N, L), dtype=np.int8)
    seqs = ALPHABET[idx]
    out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
    with open(out_path, "w") as f:
        for row in seqs:
            f.write("".join(row.tolist()))
            f.write("\n")


if __name__ == "__main__":
    main()
