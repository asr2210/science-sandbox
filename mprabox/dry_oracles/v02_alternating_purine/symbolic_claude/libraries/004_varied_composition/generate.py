"""004_varied_composition: 50,000 distinct random strings, each with its own
single-character bias (composition).

For each i in 1..N:
  - Sample p0 uniformly in [0, 1]  -> fraction of "0" in string i
  - Other characters get (1 - p0) / 3 each
  - Sample positions independently from the resulting categorical
This creates a library that maximally varies single-character bulk composition.

If the scoring correlation responds strongly to bulk composition (e.g. predictor
outputs scale with GC-content equivalent), r should jump above the 001 baseline of
0.116.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
chars = np.array(list("0123"))

rng = np.random.default_rng(seed=4)
p0 = rng.uniform(0.0, 1.0, size=N)  # per-string fraction of "0"
# Construct per-string distribution: [p0, (1-p0)/3, (1-p0)/3, (1-p0)/3]
others = (1.0 - p0) / 3.0
probs = np.stack([p0, others, others, others], axis=1)  # (N, 4)
# Per-string sample: do it row-by-row using gumbel trick (vectorized)
# x_ij = argmax_k (log p_jk + Gumbel) => sample
log_p = np.log(np.clip(probs, 1e-12, None))  # (N, 4)
gumbel = -np.log(-np.log(rng.uniform(size=(N, L, 4))))  # (N, L, 4)
idx = (log_p[:, None, :] + gumbel).argmax(axis=-1)  # (N, L)
seqs = chars[idx]

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(row.tolist()))
        f.write("\n")
print(f"Wrote {N} sequences of length {L} to {out}")
# Sanity print
print(f"First p0={p0[0]:.3f}, first string starts: {''.join(seqs[0][:30].tolist())}")
print(f"Last  p0={p0[-1]:.3f}, last  string starts: {''.join(seqs[-1][:30].tolist())}")
