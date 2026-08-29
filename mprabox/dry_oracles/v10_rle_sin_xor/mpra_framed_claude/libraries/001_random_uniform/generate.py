"""Experiment 001: random uniform DNA baseline.

Generates 50,000 sequences of length 200 with each base drawn iid uniform
from {A,C,G,T}. Establishes the floor performance for sequences with no
intentional regulatory structure.
"""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 0

ALPHABET = np.array(list("ACGT"))


def main() -> None:
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    chars = ALPHABET[idx]
    seqs = ["".join(row) for row in chars]

    out_path = Path(__file__).parent / "sequences_0.txt"
    out_path.write_text("\n".join(seqs) + "\n")

    assert len(seqs) == N_SEQS
    assert all(len(s) == SEQ_LEN for s in seqs)
    assert all(set(s) <= set("ACGT") for s in seqs[:100])
    print(f"wrote {len(seqs)} sequences of length {SEQ_LEN} to {out_path}")


if __name__ == "__main__":
    main()
