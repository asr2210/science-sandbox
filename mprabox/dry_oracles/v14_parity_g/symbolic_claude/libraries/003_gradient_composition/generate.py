"""Gradient composition: sequence i has fraction (i/N) of char '0',
remaining filled with random {1,2,3}. Tests whether per-sequence
composition variation (a monotonic property indexed by sequence order)
is rewarded."""
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
with open("libraries/003_gradient_composition/sequences_0.txt", "w") as f:
    for i in range(N):
        frac0 = i / (N - 1)  # 0..1
        n0 = int(round(frac0 * L))
        n_rest = L - n0
        zeros = ['0'] * n0
        rest = rng.choice(['1', '2', '3'], size=n_rest).tolist()
        seq = zeros + rest
        rng.shuffle(seq)
        f.write("".join(seq) + "\n")
