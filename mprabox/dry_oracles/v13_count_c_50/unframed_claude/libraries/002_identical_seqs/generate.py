"""002_identical_seqs: 50,000 copies of one random 200bp sequence.

Diagnostic: if r is Pearson correlation (requires variance among my sequences),
this should give NaN/0. If r is per-sequence mean activity, this gives a finite
value equal to whatever that one sequence scores.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))
seq = "".join(bases[rng.integers(0, 4, size=L)].tolist())

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for _ in range(N):
        f.write(seq)
        f.write("\n")
print(f"wrote {N} copies of one seq (len {L}) to {out}")
print(f"seq: {seq}")
