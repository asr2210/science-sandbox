"""Experiment 009: DNA-style Markov chain probe.

50,000 strings drawn from a single order-1 Markov chain whose transitions
roughly match real DNA dinucleotide frequencies (with CpG depletion).
Mapping: A=0, C=1, G=2, T=3.

If the predictor was trained on biology-like data, structured-but-natural
sequences should score better than uniform random.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 9

# Approximate transition matrix derived from human-genome dinucleotide stats.
# Row = previous, Col = next. CG transition is depleted.
T = np.array([
    [0.30, 0.20, 0.28, 0.22],  # A→A,C,G,T
    [0.32, 0.27, 0.05, 0.36],  # C→A,C,G,T (CpG depletion: C→G low)
    [0.27, 0.25, 0.25, 0.23],  # G→
    [0.18, 0.24, 0.29, 0.29],  # T→
])
assert np.allclose(T.sum(axis=1), 1.0)
init = np.array([0.295, 0.205, 0.205, 0.295])  # AT-biased background

rng = np.random.default_rng(SEED)

# Vectorized: pick initial column index
init_choices = rng.choice(4, size=N, p=init)
# Pre-generate uniform randoms for transition decisions
u = rng.random((N, L))

# Cumulative transitions for fast inverse-CDF sampling
Tcum = np.cumsum(T, axis=1)
INIT_CUM = np.cumsum(init)

out = np.empty((N, L), dtype=np.uint8)
out[:, 0] = init_choices

for j in range(1, L):
    prev = out[:, j - 1]
    # row of Tcum for each prev value
    cum_rows = Tcum[prev]  # (N, 4)
    # find first index where u[:, j] < cum_rows[:, k]
    u_col = u[:, j:j + 1]
    out[:, j] = (u_col < cum_rows).argmax(axis=1).astype(np.uint8)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[out]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

# Verify CpG depletion in output
total_CG = 0
for row in out:
    total_CG += np.sum((row[:-1] == 1) & (row[1:] == 2))
print(f"Wrote {N} DNA-like Markov sequences. Avg CG dinuc per string: {total_CG/N:.2f}")
