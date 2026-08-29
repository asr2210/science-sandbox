"""Experiment 6: Joint GC + CpG variance via first-order Markov chain.

For each sequence, sample:
  gc ~ Uniform[0.05, 0.95]
  cpg_oe ~ Uniform[0.05, 3.0]   (CpG observed/expected ratio)

Build a first-order Markov chain whose stationary base frequencies match gc and
whose dinucleotide P(C,G) = cpg_oe * P(C) * P(G), via IPF over the 4x4 matrix.
Indices: A=0, C=1, G=2, T=3.
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(seed=6)
N, L = 50000, 200


def ipf_dinuc(pi, cg_target, n_iter=80, tol=1e-7):
    pi = np.asarray(pi, dtype=np.float64)
    P = np.outer(pi, pi).copy()
    cg_target = float(min(cg_target, 0.99 * pi[1], 0.99 * pi[2]))
    cg_target = max(cg_target, 1e-9)
    P[1, 2] = cg_target
    for _ in range(n_iter):
        # Row scaling
        for i in range(4):
            if i == 1:
                residual = pi[1] - P[1, 2]
                cur = P[1, [0, 1, 3]].sum()
                if cur > 0 and residual > 0:
                    P[1, [0, 1, 3]] *= residual / cur
            else:
                rs = P[i].sum()
                if rs > 0:
                    P[i] *= pi[i] / rs
        # Column scaling
        for j in range(4):
            if j == 2:
                residual = pi[2] - P[1, 2]
                cur = P[[0, 2, 3], 2].sum()
                if cur > 0 and residual > 0:
                    P[[0, 2, 3], 2] *= residual / cur
            else:
                cs = P[:, j].sum()
                if cs > 0:
                    P[:, j] *= pi[j] / cs
        if (np.abs(P.sum(axis=1) - pi).max() < tol and
            np.abs(P.sum(axis=0) - pi).max() < tol):
            break
    T = P / pi[:, None]
    T = T / T.sum(axis=1, keepdims=True)
    return T


def sample_chain_vec(T, pi, L, rng):
    """Sample one sequence of length L from a 4-state Markov chain."""
    # Use cumulative distributions for fast sampling
    cumT = np.cumsum(T, axis=1)            # 4x4
    cumPi = np.cumsum(pi)                  # 4
    bases = np.empty(L, dtype=np.int8)
    u = rng.random(L)
    bases[0] = np.searchsorted(cumPi, u[0])
    for k in range(1, L):
        bases[k] = np.searchsorted(cumT[bases[k - 1]], u[k])
    return bases


gc_targets = rng.uniform(0.05, 0.95, size=N)
cpg_oe_targets = rng.uniform(0.05, 3.0, size=N)

alphabet = np.array(list("ACGT"))
out = np.empty((N, L), dtype=np.int8)
for i in range(N):
    gc = gc_targets[i]
    pi = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])
    cg_target = cpg_oe_targets[i] * pi[1] * pi[2]
    T = ipf_dinuc(pi, cg_target)
    out[i] = sample_chain_vec(T, pi, L, rng)
    if (i + 1) % 10000 == 0:
        print(f"  generated {i+1}/{N}")

seqs = ["".join(alphabet[row]) for row in out]
out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(seqs) + "\n")

gc_actual = ((out == 1) | (out == 2)).mean(axis=1)
cg_count = ((out[:, :-1] == 1) & (out[:, 1:] == 2)).sum(axis=1)
expected_cg = (L - 1) * (gc_targets / 2) ** 2
oe_actual = cg_count / np.maximum(expected_cg, 1e-6)
print(f"GC realized: mean={gc_actual.mean():.3f}, std={gc_actual.std():.3f}")
print(f"CpG O/E realized: mean={oe_actual.mean():.3f}, std={oe_actual.std():.3f}, "
      f"range=[{oe_actual.min():.2f}, {oe_actual.max():.2f}]")
