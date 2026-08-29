"""Experiment 008: Template-following library.

Generate a fixed random base template (length 200, all 4 chars used).
Each of 50k sequences = 90% match the template, 10% noise (uniform other 3 chars).

Population at each position p: 90% prob of base[p], ~3.3% each of other 3 chars.
All 4 chars represented at every position → no NaN.

Tests if all 50k sequences "agreeing" on a fixed random template scores higher than
50k independent random sequences.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 23
MATCH = 0.9

rng = np.random.default_rng(SEED)
template = rng.integers(0, 4, size=L, dtype=np.uint8)
assert len(np.unique(template)) == 4
print(f"Template (first 50): {''.join(map(str, template.tolist()))[:50]}")
print(f"Template char counts: {np.bincount(template, minlength=4)}")

# For each (seq, pos): with prob MATCH, use template[pos]; else random other char.
# Vectorized:
templ_bcast = np.broadcast_to(template, (N, L))
keep_mask = rng.random((N, L)) < MATCH
noise_offset = rng.integers(1, 4, size=(N, L), dtype=np.uint8)
noise_chars = (templ_bcast + noise_offset) % 4
mat = np.where(keep_mask, templ_bcast, noise_chars).astype(np.uint8)

# Verify NaN safety: every position has all 4 chars across population
for p in range(L):
    counts = np.bincount(mat[:, p], minlength=4)
    assert (counts > 0).all(), f"Position {p} missing chars: {counts}"

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for row in mat:
        f.write("".join(map(str, row.tolist())))
        f.write("\n")
print(f"Wrote {N} template-biased sequences to {out_path}")
