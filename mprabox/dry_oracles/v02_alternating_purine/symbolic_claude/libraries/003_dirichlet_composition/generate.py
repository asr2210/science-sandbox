"""Exp 003: per-sequence composition diversity.

Each of 50,000 sequences gets its own composition p = (p0,p1,p2,p3)
drawn from a Dirichlet(alpha=0.5) — favors *biased* compositions
(some bases dominant, others rare) but with full diversity across the
library. Each sequence is then sampled i.i.d. with its own p.

Hypothesis: if the hidden scorer cares about composition features, a
library with wide composition diversity will score higher than pure
uniform random (which has narrow composition spread around 25/25/25/25).
If similar to baseline, composition isn't the main signal.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 3
ALPHA = 0.5  # smaller alpha → more skew per sequence

rng = np.random.default_rng(SEED)
comps = rng.dirichlet([ALPHA, ALPHA, ALPHA, ALPHA], size=N)  # (N, 4)

# Vectorised sampling: for each row pick L tokens with that row's p.
# Use cumulative trick.
u = rng.random((N, L))
cum = comps.cumsum(axis=1)  # (N, 4)
# tokens[i,j] = first k such that u[i,j] < cum[i,k]
tokens = (u[:, :, None] >= cum[:, None, :]).sum(axis=2).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in tokens:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
print(f"wrote {N} sequences; sample compositions:\n{comps[:3]}")
