"""Exp 027: period-4 phase 0 p=0.7 with per-row noise direction.

Each row k has noise weights (p1, p2, p3) over {t+1, t+2, t+3 mod 4}
sampled from Dirichlet(1). Library-wide average is uniform.

At each position: with prob 0.7 emit template. With prob 0.3, emit
one of the 3 non-template bases per the per-row weights.

Hypothesis: per-row variation may lift condition_a/b without affecting
per-cell freqs (preserve c).
"""
import numpy as np
from pathlib import Path

N, L, SEED = 50_000, 200, 27
P_TEMPLATE = 0.7

rng = np.random.default_rng(SEED)
template = (np.arange(L) % 4).astype(np.uint8)            # (L,)
template_tile = np.broadcast_to(template, (N, L))         # (N, L)

# Per-row Dirichlet(1) over the 3 non-template directions {+1, +2, +3}
noise_weights = rng.dirichlet(np.ones(3), size=N)         # (N, 3)
noise_cum = noise_weights.cumsum(axis=1)                  # (N, 3)

# Sample noise position mask
keep_mask = rng.random((N, L)) < P_TEMPLATE               # (N, L)

# At noise positions, pick offset in {1,2,3} per row weights
u = rng.random((N, L))
# offset = first k (in 1..3) such that u < noise_cum[row, k-1]
offset = (u[:, :, None] >= noise_cum[:, None, :]).sum(axis=2) + 1  # (N, L) in {1,2,3}
alt = (template_tile + offset.astype(np.uint8)) % 4

seqs = np.where(keep_mask, template_tile, alt).astype(np.uint8)

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for row in seqs:
        f.write("".join(chr(48 + c) for c in row))
        f.write("\n")
mins = [min((seqs[:, j] == b).sum() for b in range(4)) for j in range(L)]
print(f"wrote {N}; min base count per position = {min(mins)}")
pos0_freqs = [(seqs[:, 0] == b).mean() for b in range(4)]
print(f"pos-0 freqs (expect ~0.7/0.1/0.1/0.1) = {[round(x,3) for x in pos0_freqs]}")
