"""Experiment 025: orbit{0123} + 0-density combined gradient.

Per-string i has BOTH gradients at level p_i = i/(N-1):
- Insert k_i = round(p_i * 50) orbit{0123} blocks
- Remaining (non-block) positions: 0 with prob p_i * 0.5, else uniform

Both axes boost cond_a (exp4 a=+0.0091, exp21 a=+0.0102). If they compound,
eval_01 mean_r could exceed +0.005. If they cancel (like exp10/19), revert
to pure orbit{0123} for final.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 25
KMAX = 50

rng = np.random.default_rng(SEED)

# Build base: per-position, draw with extra weight on 0
p_per_string = np.linspace(0.0, 1.0, N)
p_zero = 0.25 + p_per_string * 0.25  # 0.25 to 0.5 prob of 0

# Per-position uniform-with-0-bias: with prob p_zero use 0, else uniform from {1,2,3}
u_base = rng.random((N, L))
base_choice = rng.integers(1, 4, size=(N, L), dtype=np.uint8)  # 1,2,3
base_is_zero = u_base < p_zero[:, None]
out = np.where(base_is_zero, 0, base_choice).astype(np.uint8)

orbit = np.array([
    [0, 1, 2, 3],
    [1, 0, 3, 2],
    [2, 3, 0, 1],
    [3, 2, 1, 0],
], dtype=np.uint8)

ks = np.round(p_per_string * KMAX).astype(int)
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

zc = (out == 0).sum(axis=1)
orbit_codes = set()
for rep in orbit:
    orbit_codes.add(rep[0]*64 + rep[1]*16 + rep[2]*4 + rep[3])
quad = out[:, :-3]*64 + out[:, 1:-2]*16 + out[:, 2:-1]*4 + out[:, 3:]
n_orb = np.isin(quad, list(orbit_codes)).sum(axis=1)
print(f"0-counts: min={zc.min()} mean={zc.mean():.1f} max={zc.max()}")
print(f"orbit-0123 4-mer: min={n_orb.min()} mean={n_orb.mean():.1f} max={n_orb.max()}")
print(f"Wrote {N} sequences with combined orbit+0-density gradient")
