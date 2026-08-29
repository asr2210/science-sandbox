"""Experiment 004: 0-density gradient.

50,000 strings; string i has P(char='0') = i/(N-1) at each position; the
remaining mass is split equally among {1,2,3}.

This induces a monotonic 0-count gradient across strings. If any eval's
predictor responds linearly to 0-content, |r| should be substantially > 0.
"""
import os
import numpy as np

N = 50_000
L = 200
SEED = 4
ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)

rng = np.random.default_rng(SEED)
p0 = np.linspace(0.0, 1.0, N)  # per-string probability of '0'

# Vectorized sampling: for each string, decide whether each position is '0'
is_zero = rng.random((N, L)) < p0[:, None]  # (N, L) bool
# If not '0', uniform over {1,2,3}
other_idx = rng.integers(1, 4, size=(N, L))  # 1, 2, or 3
char_idx = np.where(is_zero, 0, other_idx).astype(np.uint8)  # 0..3
chars = ALPHABET[char_idx]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

zero_counts = (char_idx == 0).sum(axis=1)
print(f"Wrote {N} sequences; 0-count range [{zero_counts.min()},{zero_counts.max()}], mean {zero_counts.mean():.1f}")
