"""Exp 028: sigmoidal (instead of linear) gradient between endpoints.

Linear: base(t) = (1-t)*A + t*B. Halfway is always exactly midpoint.
Sigmoidal: base(t) = (1-s(t))*A + s(t)*B with s(t) = sigmoid((t-0.5)*k).
Creates more block-like structure: first half dominated by A, second by B,
with sharper transition in the middle. Each block has a more distinct
composition → potentially more between-seq * position signal.
"""
import os
import numpy as np

np.random.seed(20260627)

N = 50_000
L = 200
ALPHA = np.array(["0", "1", "2", "3"])
K = 4

W_MARKOV = 0.2
W_GRAD = 0.8
ROW_ALPHA = 0.2
K_SIG = 8.0  # sigmoid steepness

t_lin = np.linspace(0.0, 1.0, L)
s = 1.0 / (1.0 + np.exp(-(t_lin - 0.5) * K_SIG))
# Renormalize so s spans [0,1] exactly.
s = (s - s.min()) / (s.max() - s.min())
s_vec = s.reshape(-1, 1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    c_starts = np.random.dirichlet(np.full(K, 0.5), size=N)
    c_ends = np.random.dirichlet(np.full(K, 0.5), size=N)
    for i in range(N):
        base = (1.0 - s_vec) * c_starts[i] + s_vec * c_ends[i]
        T = np.random.dirichlet(np.full(K, ROW_ALPHA), size=K)
        seq = np.empty(L, dtype=np.int8)
        seq[0] = np.random.choice(K, p=base[0])
        for p in range(1, L):
            mix = W_MARKOV * T[seq[p - 1]] + W_GRAD * base[p]
            seq[p] = np.random.choice(K, p=mix)
        f.write("".join(ALPHA[seq]) + "\n")
print(f"wrote {N} sequences; sigmoid k={K_SIG}")
