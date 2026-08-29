"""Exp 020: gradient + Markov weight 0.3."""
import os
import numpy as np

np.random.seed(20260619)

N = 50_000
L = 200
ALPHA = np.array(["0", "1", "2", "3"])
K = 4

W_MARKOV = 0.3
W_GRAD = 1.0 - W_MARKOV

t_vec = np.linspace(0.0, 1.0, L).reshape(-1, 1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    c_starts = np.random.dirichlet(np.full(K, 0.5), size=N)
    c_ends = np.random.dirichlet(np.full(K, 0.5), size=N)
    for i in range(N):
        base = (1.0 - t_vec) * c_starts[i] + t_vec * c_ends[i]
        T = np.random.dirichlet(np.full(K, 0.5), size=K)
        seq = np.empty(L, dtype=np.int8)
        seq[0] = np.random.choice(K, p=base[0])
        for p in range(1, L):
            mix = W_MARKOV * T[seq[p - 1]] + W_GRAD * base[p]
            seq[p] = np.random.choice(K, p=mix)
        f.write("".join(ALPHA[seq]) + "\n")
print(f"wrote {N} sequences with Markov weight 0.3")
