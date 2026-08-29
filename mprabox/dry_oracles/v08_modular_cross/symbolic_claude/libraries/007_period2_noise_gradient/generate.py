"""Experiment 007: Period-2 base with noise gradient.

Each string starts as period-2 ("01"*100 or "10"*100, phase random per string).
String i has noise_rate = 0.05 + 0.45*i/(N-1). Each position has prob
noise_rate of being replaced by a uniform random char in {0,1,2,3}.

Tests if predictor responds to anti-autocorrelation / period-2-ness.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 7

rng = np.random.default_rng(SEED)

base01 = np.array([0, 1] * (L // 2), dtype=np.uint8)
base10 = np.array([1, 0] * (L // 2), dtype=np.uint8)

phases = rng.integers(0, 2, size=N)  # 0 → "01...", 1 → "10..."
noise_rates = np.linspace(0.05, 0.50, N)

bases = np.where(phases[:, None] == 0, base01[None, :], base10[None, :])
noise_mask = rng.random((N, L)) < noise_rates[:, None]
random_rep = rng.integers(0, 4, size=(N, L), dtype=np.uint8)
chars = np.where(noise_mask, random_rep, bases).astype(np.uint8)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
out = ALPHABET[chars]
lines = out.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {N} period-2-base strings; noise from {noise_rates[0]:.2f} to {noise_rates[-1]:.2f}")
