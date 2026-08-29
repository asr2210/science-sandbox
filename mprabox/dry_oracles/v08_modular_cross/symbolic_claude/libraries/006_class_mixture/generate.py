"""Experiment 006: 5-class diverse mixture probe.

10,000 strings each from:
A. uniform random
B. Markov order-1 strongly autocorrelated (p_self=0.85)
C. tandem period-4 "0123" with 5% per-position noise (random replacement)
D. tandem period-2 "01" with 5% noise
E. biased composition (90% one char per string; char varies per string)

Each class is preserved as a block (positions 0-9999, 10000-19999, ...)
so we can interpret class-block predictions if we ever get them. The
across-string correlation is invariant to ordering.
"""
import os
import numpy as np

N_PER = 10_000
L = 200
SEED = 6

rng = np.random.default_rng(SEED)
all_chars = np.empty((5 * N_PER, L), dtype=np.uint8)

# Class A: uniform random
all_chars[0:N_PER] = rng.integers(0, 4, size=(N_PER, L), dtype=np.uint8)

# Class B: Markov p_self=0.85
p_self = 0.85
stays = rng.random((N_PER, L)) < p_self
non_self = rng.integers(0, 3, size=(N_PER, L), dtype=np.uint8)
starts = rng.integers(0, 4, size=N_PER)
for i in range(N_PER):
    cur = int(starts[i])
    all_chars[N_PER + i, 0] = cur
    si = stays[i]
    ni = non_self[i]
    for j in range(1, L):
        if si[j]:
            all_chars[N_PER + i, j] = cur
        else:
            other = int(ni[j])
            if other >= cur:
                other += 1
            cur = other
            all_chars[N_PER + i, j] = cur

# Class C: tandem period-4 "0123" with 5% noise
base4 = np.array([0, 1, 2, 3] * (L // 4), dtype=np.uint8)
noise_mask = rng.random((N_PER, L)) < 0.05
random_rep = rng.integers(0, 4, size=(N_PER, L), dtype=np.uint8)
all_chars[2 * N_PER : 3 * N_PER] = np.where(noise_mask, random_rep, base4[None, :])

# Class D: tandem period-2 "01" with 5% noise
base2 = np.array([0, 1] * (L // 2), dtype=np.uint8)
noise_mask = rng.random((N_PER, L)) < 0.05
random_rep = rng.integers(0, 4, size=(N_PER, L), dtype=np.uint8)
all_chars[3 * N_PER : 4 * N_PER] = np.where(noise_mask, random_rep, base2[None, :])

# Class E: biased composition (90% one char, randomly chosen per string)
dom = rng.integers(0, 4, size=N_PER)
dominant_mask = rng.random((N_PER, L)) < 0.90
other = rng.integers(0, 3, size=(N_PER, L), dtype=np.uint8)
for i in range(N_PER):
    d = int(dom[i])
    row = np.where(dominant_mask[i], d, np.where(other[i] >= d, other[i] + 1, other[i]))
    all_chars[4 * N_PER + i] = row.astype(np.uint8)

ALPHABET = np.array([ord(c) for c in "0123"], dtype=np.uint8)
chars = ALPHABET[all_chars]
lines = chars.view(f"S{L}").astype(str).ravel()

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"Wrote {5 * N_PER} sequences across 5 classes (A=random, B=Markov, C=period-4, D=period-2, E=biased)")
