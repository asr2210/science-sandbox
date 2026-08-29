"""Experiment 022: Push 4-mer orbit{0123} gradient to extreme.

Each string i has k_i = round(i/(N-1) * 50) of its 50 length-4 blocks
filled with random reps of orbit{0123}={0123,1032,2301,3210}. Other blocks
are uniform random. Range 0 to ALL 50 blocks = ALL 200 chars structured.

If signal scales with gradient steepness, eval_01 mean_r should rise above
exp 21's +0.0045. If saturates, ~0.0045 is the cap from a single feature.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 22
KMAX = 50  # full coverage

rng = np.random.default_rng(SEED)
out = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

orbit = np.array([
    [0, 1, 2, 3],
    [1, 0, 3, 2],
    [2, 3, 0, 1],
    [3, 2, 1, 0],
], dtype=np.uint8)

ks = np.round(np.linspace(0, KMAX, N)).astype(int)
n_blocks = L // 4  # 50
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
print(f"orbit-0123 4-mer per string: min={n_orb.min()} mean={n_orb.mean():.1f} max={n_orb.max()}")
print(f"Wrote {N} sequences (k_max={KMAX} = full coverage)")
