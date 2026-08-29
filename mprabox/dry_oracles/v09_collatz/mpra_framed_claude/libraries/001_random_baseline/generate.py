"""001_random_baseline: 50,000 uniform random 200bp DNA sequences."""
import numpy as np
from pathlib import Path

N_SEQS = 50_000
LEN = 200
SEED = 0

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
idx = rng.integers(0, 4, size=(N_SEQS, LEN))
seqs = bases[idx]

out = Path(__file__).parent / "sequences_0.txt"
with open(out, "w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")

print(f"Wrote {N_SEQS} sequences of length {LEN} to {out}")
