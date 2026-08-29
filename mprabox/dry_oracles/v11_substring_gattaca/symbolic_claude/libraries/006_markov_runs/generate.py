"""Markov chain with self-transition probability 0.5 → 'runs' within strings.
Maintains balanced composition on average but introduces local structure
(adjacent positions are correlated).

Tests if within-string structure (autocorrelation) helps or hurts r."""
import os
import numpy as np

rng = np.random.default_rng(42)
N, L = 50000, 200
p_stay = 0.5
p_switch = (1 - p_stay) / 3  # 0.1667

# Transition matrix: row i = next char distribution given current = i
T = np.full((4, 4), p_switch)
np.fill_diagonal(T, p_stay)

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
chars = list("0123")

with open(OUT, "w") as f:
    for _ in range(N):
        seq = []
        prev = rng.integers(0, 4)
        seq.append(chars[prev])
        for _ in range(L - 1):
            prev = rng.choice(4, p=T[prev])
            seq.append(chars[prev])
        f.write("".join(seq) + "\n")
print(f"wrote {N} Markov-chain sequences (p_stay={p_stay})")
