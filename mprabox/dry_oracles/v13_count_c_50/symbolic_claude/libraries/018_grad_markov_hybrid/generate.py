"""Exp 018: hybrid of compositional gradient + per-sequence Markov chain.

For each sequence:
- Endpoint compositions c_start, c_end ~ Dirichlet(0.5)
- Position-wise smooth gradient: base_comp(t) = (1-t)*c_start + t*c_end
- Random transition matrix T with rows ~ Dirichlet(0.5)
- At each position p, sample next char from a 50/50 blend of T[prev] and
  base_comp at position p

This combines positional variance (which boosted a, c) with within-seq
transition variance (which boosted b in exp 009).
"""
import os
import numpy as np

np.random.seed(20260617)

N = 50_000
L = 200
ALPHA = np.array(["0", "1", "2", "3"])
K = 4

t_vec = np.linspace(0.0, 1.0, L).reshape(-1, 1)  # (L, 1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    c_starts = np.random.dirichlet(np.full(K, 0.5), size=N)
    c_ends = np.random.dirichlet(np.full(K, 0.5), size=N)
    for i in range(N):
        base = (1.0 - t_vec) * c_starts[i] + t_vec * c_ends[i]  # (L, K)
        T = np.random.dirichlet(np.full(K, 0.5), size=K)        # (K, K)

        seq = np.empty(L, dtype=np.int8)
        # First position from base[0].
        seq[0] = np.random.choice(K, p=base[0])
        for p in range(1, L):
            mix = 0.5 * T[seq[p - 1]] + 0.5 * base[p]
            seq[p] = np.random.choice(K, p=mix)
        f.write("".join(ALPHA[seq]) + "\n")
print(f"wrote {N} hybrid gradient+Markov sequences")
