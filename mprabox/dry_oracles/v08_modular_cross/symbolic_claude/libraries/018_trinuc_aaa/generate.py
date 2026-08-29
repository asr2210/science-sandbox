"""Experiment 018: Trinuc AAA orbit (homo-triplet) insertion gradient.

Insert orbit{000} = {000,111,222,333} — "runs of length 3". Tests whether
eval_01 or other evals respond to homo-triplet density (a Klein-invariant
"long-run" structural feature distinct from dinuc HOMO count).
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 18
KMAX = 60

rng = np.random.default_rng(SEED)
out = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

orbit = np.array([
    [0, 0, 0],
    [1, 1, 1],
    [2, 2, 2],
    [3, 3, 3],
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

trin = out[:, :-2] * 16 + out[:, 1:-1] * 4 + out[:, 2:]
codes = [0, 21, 42, 63]  # 0*21=0 (000), 1*21=21 (111), 2*21=42 (222), 3*21=63 (333)
counts = np.isin(trin, codes).sum(axis=1)
print(f"AAA trinuc count per string: min={counts.min()} mean={counts.mean():.1f} max={counts.max()}")
print(f"Wrote {N} sequences with AAA trinuc insertion gradient")
