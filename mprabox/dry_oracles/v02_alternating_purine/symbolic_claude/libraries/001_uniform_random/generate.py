"""Exp 001: uniform random baseline.

50,000 strings of length 200, each char i.i.d. uniform over {0,1,2,3}.
Establishes a noise-floor for the scoring function before probing structure.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 1

rng = np.random.default_rng(SEED)
arr = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

out_path = Path(__file__).parent / "sequences_0.txt"
with out_path.open("w") as f:
    for row in arr:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
print(f"wrote {N} sequences to {out_path}")
