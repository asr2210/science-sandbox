"""Experiment 001: uniform random 200bp DNA baseline.

50,000 sequences, each base i.i.d. uniform from {A,C,G,T}, 3 seeds.
"""
import os
import sys
import numpy as np

N_SEQS = 50_000
SEQ_LEN = 200
ALPHABET = np.array(list("ACGT"))
HERE = os.path.dirname(os.path.abspath(__file__))


def generate(seed: int) -> list[str]:
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    chars = ALPHABET[idx]
    return ["".join(row) for row in chars]


def main():
    for seed in (0, 1, 2):
        seqs = generate(seed)
        out = os.path.join(HERE, f"sequences_{seed}.txt")
        with open(out, "w") as f:
            f.write("\n".join(seqs) + "\n")
        # sanity check
        assert len(seqs) == N_SEQS
        assert all(len(s) == SEQ_LEN for s in seqs)
        assert all(set(s) <= set("ACGT") for s in seqs[:100])
        print(f"wrote {out} ({N_SEQS} x {SEQ_LEN}bp)")


if __name__ == "__main__":
    main()
