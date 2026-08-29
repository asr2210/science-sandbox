"""Experiment 026: Cyclic Markov gradient — smoother orbit{0123} content.

Per-string i with cyclic strength p_i = i/(N-1):
- Pick starting char c0 ∈ {0,1,2,3} uniform
- Pick direction d ∈ {+1, -1} uniform
- At each step: with prob p_i, advance (c+d) mod 4; else uniform random

When p=1, produces deterministic cyclic "01230123..." (or other rotation/
direction). When p=0, uniform random. Klein-invariant via direction/start
randomization.

Hypothesis: avoiding block-boundary noise lifts eval_01 above +0.0045.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 26

rng = np.random.default_rng(SEED)
p_vals = np.linspace(0.0, 1.0, N)

start = rng.integers(0, 4, size=N, dtype=np.uint8)
direction = rng.choice(np.array([1, 3], dtype=np.uint8), size=N)  # +1 or -1 mod 4

out = np.empty((N, L), dtype=np.uint8)
out[:, 0] = start

u_step = rng.random((N, L))
rand_choice = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

for j in range(1, L):
    advance = (out[:, j - 1] + direction) % 4
    use_advance = u_step[:, j] < p_vals
    out[:, j] = np.where(use_advance, advance, rand_choice[:, j]).astype(np.uint8)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

# Count orbit{0123} 4-mer windows
orbit_codes = []
for rep in [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]:
    orbit_codes.append(rep[0]*64 + rep[1]*16 + rep[2]*4 + rep[3])
quad = out[:, :-3]*64 + out[:, 1:-2]*16 + out[:, 2:-1]*4 + out[:, 3:]
n_orb = np.isin(quad, orbit_codes).sum(axis=1)
print(f"orbit{{0123}} 4-mer windows per string: min={n_orb.min()} mean={n_orb.mean():.1f} max={n_orb.max()}")
print(f"Wrote {N} sequences with cyclic Markov gradient")
