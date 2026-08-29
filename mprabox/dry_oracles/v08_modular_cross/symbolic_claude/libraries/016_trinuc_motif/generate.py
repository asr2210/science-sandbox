"""Experiment 016: Trinuc motif insertion gradient.

Each string i has k_i = round(i/(N-1) * 60) non-overlapping length-3 windows
replaced with a Klein-orbit-{012} representative. The base is uniform random.

If predictor responds to trinuc-orbit features, mean_r should emerge.
Choose representative per insertion uniformly from {012, 103, 230, 321}
(Klein orbit of "012") so we're injecting orbit-mass cleanly.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 16
KMAX = 60  # max inserts per string

rng = np.random.default_rng(SEED)
out = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

# Orbit reps as length-3 arrays
orbit = np.array([
    [0, 1, 2],
    [1, 0, 3],
    [2, 3, 0],
    [3, 2, 1],
], dtype=np.uint8)

# Per-string insertion count
ks = np.round(np.linspace(0, KMAX, N)).astype(int)

# Pre-pick positions: choose KMAX random non-overlapping windows then trim to k_i
# A simpler scheme: divide string into ceil(L/3) blocks of length 3, pick k_i
# random blocks to overwrite. L=200, blocks = 66 (last is 2-long, skip it).
n_blocks = L // 3  # 66
block_starts = np.arange(n_blocks) * 3  # 0,3,6,...,195

# Per-string: pick k_i random block indices, overwrite with random orbit reps
# Vectorize via random argsort
rand_ord = rng.random((N, n_blocks))
order = np.argsort(rand_ord, axis=1)  # (N, 66)

orbit_choice = rng.integers(0, 4, size=(N, KMAX), dtype=np.uint8)

for i in range(N):
    k = ks[i]
    if k == 0:
        continue
    chosen_blocks = order[i, :k]
    starts = block_starts[chosen_blocks]
    reps = orbit[orbit_choice[i, :k]]  # (k, 3)
    for s, rep in zip(starts, reps):
        out[i, s:s + 3] = rep

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

# Diagnostic: count orbit{012} trinucleotides per string
orbit_set = {(0, 1, 2), (1, 0, 3), (2, 3, 0), (3, 2, 1)}
codes = set(r * 16 + g * 4 + b for r, g, b in orbit_set)
trin = out[:, :-2] * 16 + out[:, 1:-1] * 4 + out[:, 2:]
counts = np.isin(trin, list(codes)).sum(axis=1)
print(f"orbit-012 trinuc count per string: min={counts.min()} mean={counts.mean():.1f} max={counts.max()}")
print(f"Wrote {N} sequences with trinuc-motif insertion gradient")
