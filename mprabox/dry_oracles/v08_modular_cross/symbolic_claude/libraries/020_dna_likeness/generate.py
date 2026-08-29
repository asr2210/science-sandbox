"""Experiment 020: Per-string DNA-likeness mixture gradient.

Each string i has at each position: with prob p_i a sample from DNA-like
Markov chain (exp 9 transitions), with prob 1-p_i a uniform random char.
p_i = i/(N-1). String i=0 is uniform random; string i=N-1 is pure DNA Markov.

This sweeps DNA-likeness smoothly. If predictor for eval_01 (or any) is
bio-pretrained, per-string Pearson should detect monotone response.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 20

T = np.array([
    [0.30, 0.20, 0.28, 0.22],
    [0.32, 0.27, 0.05, 0.36],
    [0.27, 0.25, 0.25, 0.23],
    [0.18, 0.24, 0.29, 0.29],
])
init = np.array([0.295, 0.205, 0.205, 0.295])
rng = np.random.default_rng(SEED)
Tcum = np.cumsum(T, axis=1)

p_dna = np.linspace(0.0, 1.0, N)  # per-string DNA fraction

# Generate per-string by drawing DNA-Markov and uniform sequences, then mixing
init_choices = rng.choice(4, size=N, p=init)
u_trans = rng.random((N, L))

# DNA Markov pass
dna = np.empty((N, L), dtype=np.uint8)
dna[:, 0] = init_choices
for j in range(1, L):
    cum_rows = Tcum[dna[:, j - 1]]
    dna[:, j] = (u_trans[:, j:j + 1] < cum_rows).argmax(axis=1).astype(np.uint8)

# Uniform random pass
uni = rng.integers(0, 4, size=(N, L), dtype=np.uint8)

# Per-position mixing: with prob p_i use dna, else uniform
mix_u = rng.random((N, L))
mask = mix_u < p_dna[:, None]
out = np.where(mask, dna, uni).astype(np.uint8)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

# Diagnostic: CG dinuc count per string
cg = ((out[:, :-1] == 1) & (out[:, 1:] == 2)).sum(axis=1)
print(f"CG dinuc per string: min={cg.min()} mean={cg.mean():.2f} max={cg.max()}")
print(f"Wrote {N} sequences with DNA-likeness gradient (p_DNA 0→1)")
