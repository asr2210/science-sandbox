"""Experiment 017: Trinuc XYX (palindromic) orbit insertion gradient.

Same scheme as exp 016 but using Klein orbit of "010" = {010,101,232,323}.
This is the palindromic-triplet orbit — XYX pattern with X≠Y.

If eval_01 responds to this orbit (unlike O012), it helps target the primary.
Comparing magnitudes across orbits tells us which trinuc class the
predictor weights.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 17
KMAX = 60

rng = np.random.default_rng(SEED)
out = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

orbit = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [2, 3, 2],
    [3, 2, 3],
], dtype=np.uint8)

ks = np.round(np.linspace(0, KMAX, N)).astype(int)

n_blocks = L // 3
block_starts = np.arange(n_blocks) * 3

rand_ord = rng.random((N, n_blocks))
order = np.argsort(rand_ord, axis=1)
orbit_choice = rng.integers(0, 4, size=(N, KMAX), dtype=np.uint8)

for i in range(N):
    k = ks[i]
    if k == 0:
        continue
    chosen_blocks = order[i, :k]
    starts = block_starts[chosen_blocks]
    reps = orbit[orbit_choice[i, :k]]
    for s, rep in zip(starts, reps):
        out[i, s:s + 3] = rep

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

orbit_set = {(0, 1, 0), (1, 0, 1), (2, 3, 2), (3, 2, 3)}
codes = [r * 16 + g * 4 + b for r, g, b in orbit_set]
trin = out[:, :-2] * 16 + out[:, 1:-1] * 4 + out[:, 2:]
counts = np.isin(trin, codes).sum(axis=1)
print(f"orbit-010 trinuc count per string: min={counts.min()} mean={counts.mean():.1f} max={counts.max()}")
print(f"Wrote {N} sequences with XYX trinuc insertion gradient")
