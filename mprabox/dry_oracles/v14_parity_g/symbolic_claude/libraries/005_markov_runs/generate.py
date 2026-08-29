"""Markov chain with STAY=0.7 (long runs of same character).
Tests local autocorrelation."""
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
STAY = 0.7

with open("libraries/005_markov_runs/sequences_0.txt", "w") as f:
    for _ in range(N):
        seq = [rng.integers(0, 4)]
        for _ in range(L - 1):
            if rng.random() < STAY:
                seq.append(seq[-1])
            else:
                others = [c for c in range(4) if c != seq[-1]]
                seq.append(rng.choice(others))
        f.write("".join(map(str, seq)) + "\n")
