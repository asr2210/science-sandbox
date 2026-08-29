"""Experiment 010: random uniform DNA, seed=42 (variance estimate vs exp 001)."""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 42
ALPHABET = np.array(list("ACGT"))


def main() -> None:
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    seqs = ["".join(row) for row in ALPHABET[idx]]
    out = Path(__file__).parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
