"""Experiment 010: DNA Markov + 0-density overlay gradient.

Generate DNA-like Markov chain (exp 9 transition matrix). Then for each
string i overwrite a fraction p_0(i) = (i/(N-1)) * 0.7 of positions with '0'.

If condition_a's preference for 0-density gradient (from exp 4) and
conditions b/c's preference for DNA structure (from exp 9) compose
additively, mean_r for eval_01 should exceed 0.005.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 10

T = np.array([
    [0.30, 0.20, 0.28, 0.22],
    [0.32, 0.27, 0.05, 0.36],
    [0.27, 0.25, 0.25, 0.23],
    [0.18, 0.24, 0.29, 0.29],
])
init = np.array([0.295, 0.205, 0.205, 0.295])
rng = np.random.default_rng(SEED)
Tcum = np.cumsum(T, axis=1)

init_choices = rng.choice(4, size=N, p=init)
u = rng.random((N, L))
out = np.empty((N, L), dtype=np.uint8)
out[:, 0] = init_choices
for j in range(1, L):
    cum_rows = Tcum[out[:, j - 1]]
    out[:, j] = (u[:, j:j + 1] < cum_rows).argmax(axis=1).astype(np.uint8)

# Overlay 0-density gradient
p_0 = np.linspace(0.0, 0.7, N)
mask = rng.random((N, L)) < p_0[:, None]
out = np.where(mask, 0, out).astype(np.uint8)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

zc = (out == 0).sum(axis=1)
print(f"Wrote {N}; 0-counts: min={zc.min()}, mean={zc.mean():.1f}, max={zc.max()}")
