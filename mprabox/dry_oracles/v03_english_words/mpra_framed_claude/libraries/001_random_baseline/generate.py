"""Generate 50,000 uniform random 200bp sequences as a baseline."""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 0
OUT = Path(__file__).parent / "sequences_0.txt"

rng = np.random.default_rng(SEED)
alphabet = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N, L), dtype=np.int8)
seqs = alphabet[idx]

with OUT.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")

print(f"wrote {N} x {L}bp sequences to {OUT}")
