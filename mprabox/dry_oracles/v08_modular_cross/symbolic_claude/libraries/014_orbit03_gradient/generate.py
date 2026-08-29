"""Experiment 014: Gradient sweep on Klein-orbit O03 dinucleotide frequency.

Klein 4-group orbits on dinucleotides (under (01)(23), (02)(13), (03)(12)):
  HOMO = {00,11,22,33}
  O01  = {01,10,23,32}
  O02  = {02,13,20,31}
  O03  = {03,12,21,30}

Exps 11-13 proved predictor is fully Klein- and position-invariant. So per-string
score depends only on orbit-count features. Sweep O03 dinucleotide frequency
across strings by per-string scaling factor f_i applied to T[0,3],T[3,0],T[1,2],
T[2,1] (the four directed dinucs in orbit O03), then renormalize rows.

If predictor responds to O03 frequency, |r| should be large.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 14

T0 = np.array([
    [0.30, 0.20, 0.28, 0.22],
    [0.32, 0.27, 0.05, 0.36],
    [0.27, 0.25, 0.25, 0.23],
    [0.18, 0.24, 0.29, 0.29],
])
init = np.array([0.295, 0.205, 0.205, 0.295])

# Per-string log-spaced factor: 0.05x to 5x
factors = np.exp(np.linspace(np.log(0.05), np.log(5.0), N))

# Build per-string transition matrices (N, 4, 4)
Ts = np.tile(T0, (N, 1, 1))  # (N, 4, 4)
# Scale O03-orbit cells: T[0,3], T[3,0], T[1,2], T[2,1]
o03_cells = [(0, 3), (3, 0), (1, 2), (2, 1)]
for r, c in o03_cells:
    Ts[:, r, c] *= factors
# Renormalize rows
Ts /= Ts.sum(axis=2, keepdims=True)
Tcum = np.cumsum(Ts, axis=2)  # (N, 4, 4)

rng = np.random.default_rng(SEED)
init_choices = rng.choice(4, size=N, p=init)
u = rng.random((N, L))

out = np.empty((N, L), dtype=np.uint8)
out[:, 0] = init_choices
row_idx = np.arange(N)
for j in range(1, L):
    prev = out[:, j - 1]
    cum_rows = Tcum[row_idx, prev]  # (N, 4)
    out[:, j] = (u[:, j:j + 1] < cum_rows).argmax(axis=1).astype(np.uint8)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

# Diagnostics: orbit O03 dinucleotide count per string
o03_set = {(0, 3), (3, 0), (1, 2), (2, 1)}
pairs = out[:, :-1] * 4 + out[:, 1:]
o03_codes = [r * 4 + c for r, c in o03_set]
mask = np.isin(pairs, o03_codes)
o03_per = mask.sum(axis=1)
print(f"O03 dinuc/string: min={o03_per.min()} mean={o03_per.mean():.1f} max={o03_per.max()}")
print(f"Wrote {N} sequences with O03-orbit gradient")
