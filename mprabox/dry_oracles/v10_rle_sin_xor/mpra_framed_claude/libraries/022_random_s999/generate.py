"""Experiment 022: random uniform seed=999 (3rd variance check).

Need to bound the baseline noise. 001 (s=0)=0.5177, 010 (s=42)=0.5183.
A third seed gives us mean±std on the baseline.
"""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
SEQ_LEN = 200
SEED = 999
HERE = Path(__file__).resolve()


def main() -> None:
    rng = np.random.default_rng(SEED)
    alphabet = np.array(list("ACGT"))
    idx = rng.integers(0, 4, size=(N_SEQS, SEQ_LEN), dtype=np.uint8)
    seqs = ["".join(row) for row in alphabet[idx]]
    out = HERE.parent / "sequences_0.txt"
    out.write_text("\n".join(seqs) + "\n")
    print(f"wrote {len(seqs)} sequences to {out}")


if __name__ == "__main__":
    main()
