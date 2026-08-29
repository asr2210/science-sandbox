"""Exp 005: random sequences over {0, 2} only.

Each of 50,000 sequences: 200 positions, each independent uniform from
{0, 2}. Tests if the scorer prefers the {0,2} pair over the full
alphabet.
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 5
rng = np.random.default_rng(SEED)

bits = rng.integers(0, 2, size=(N, L), dtype=np.uint8)
seqs = bits * 2  # 0 → 0, 1 → 2

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
print(f"wrote {N} sequences using {{0,2}} only")
