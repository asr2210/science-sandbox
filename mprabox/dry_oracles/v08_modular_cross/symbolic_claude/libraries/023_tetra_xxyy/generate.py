"""Experiment 023: 4-mer orbit{0011} (XXYY pattern) insertion gradient.

Test whether predictor responds to a DIFFERENT 4-mer orbit. orbit{0011} =
{0011, 1100, 2233, 3322} — XXYY pattern (two pairs, not permutation).
Same gradient profile as exp 22 (k_max=50).

If similar +0.004 lift across evals → predictor likes ANY structured 4-mer.
If weaker → orbit{0123}'s permutation structure is specifically what works.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 23
KMAX = 50

rng = np.random.default_rng(SEED)
out = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

orbit = np.array([
    [0, 0, 1, 1],
    [1, 1, 0, 0],
    [2, 2, 3, 3],
    [3, 3, 2, 2],
], dtype=np.uint8)

ks = np.round(np.linspace(0, KMAX, N)).astype(int)
n_blocks = L // 4
block_starts = np.arange(n_blocks) * 4

rand_ord = rng.random((N, n_blocks))
order = np.argsort(rand_ord, axis=1)
orbit_choice = rng.integers(0, 4, size=(N, KMAX), dtype=np.uint8)

for i in range(N):
    k = ks[i]
    if k == 0:
        continue
    chosen = order[i, :k]
    starts = block_starts[chosen]
    reps = orbit[orbit_choice[i, :k]]
    for s, rep in zip(starts, reps):
        out[i, s:s + 4] = rep

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

orbit_codes = set()
for rep in orbit:
    orbit_codes.add(rep[0]*64 + rep[1]*16 + rep[2]*4 + rep[3])
quad = out[:, :-3]*64 + out[:, 1:-2]*16 + out[:, 2:-1]*4 + out[:, 3:]
n_orb = np.isin(quad, list(orbit_codes)).sum(axis=1)
print(f"orbit-0011 4-mer per string: min={n_orb.min()} mean={n_orb.mean():.1f} max={n_orb.max()}")
print(f"Wrote {N} sequences with orbit-0011 (XXYY) gradient")
