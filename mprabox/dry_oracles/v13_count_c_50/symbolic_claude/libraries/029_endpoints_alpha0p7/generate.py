"""Exp 029: gradient endpoints alpha=0.7 + Markov weight 0.2 + rows alpha=0.2.

Fills gap between tested endpoint alphas 0.5 and 1.0 (current champion uses 0.5).
"""
import os
import numpy as np

np.random.seed(20260628)

N = 50_000
L = 200
ALPHA = np.array(["0", "1", "2", "3"])
K = 4

W_MARKOV = 0.2
W_GRAD = 0.8
ROW_ALPHA = 0.2
ENDPOINT_ALPHA = 0.7

t_vec = np.linspace(0.0, 1.0, L).reshape(-1, 1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    c_starts = np.random.dirichlet(np.full(K, ENDPOINT_ALPHA), size=N)
    c_ends = np.random.dirichlet(np.full(K, ENDPOINT_ALPHA), size=N)
    for i in range(N):
        base = (1.0 - t_vec) * c_starts[i] + t_vec * c_ends[i]
        T = np.random.dirichlet(np.full(K, ROW_ALPHA), size=K)
        seq = np.empty(L, dtype=np.int8)
        seq[0] = np.random.choice(K, p=base[0])
        for p in range(1, L):
            mix = W_MARKOV * T[seq[p - 1]] + W_GRAD * base[p]
            seq[p] = np.random.choice(K, p=mix)
        f.write("".join(ALPHA[seq]) + "\n")
print(f"wrote {N} sequences; endpoints alpha={ENDPOINT_ALPHA}")
