"""Doubly-stochastic Markov chain biasing CpG dinucleotides.

Mononucleotide marginals exactly 0.25 each (stationary distribution).
Per-base count variance similar to random uniform (slightly inflated from Markov).
DIFFERENCE: dinucleotide composition shifted — CG (and GC) enriched.

Construction: transition matrix T[i,j] = P(next=j | prev=i), with row sums = 1
and column sums = 1 (doubly stochastic), so stationary dist is uniform [0.25].
Biased toward C→G and G→C transitions.

Tests whether the eval is sensitive to dinucleotide composition shift even when
mononucleotide stats match random uniform. 007 and 010 tested OTHER dinuc shifts
(suppress runs / enhance runs) and BOTH hurt — but neither biased a specific
chemically-active dinucleotide like CG (CpG islands).
"""
import os
import numpy as np

N = 50000
L = 200
SEED = 42

# Doubly stochastic transition matrix with CpG enrichment.
# Bases: A=0, C=1, G=2, T=3
# Build T with rows summing to 1 and cols summing to 1.
# Increase C->G and G->C transitions; decrease A<->T weight where needed.
T = np.array([
    # A     C     G     T
    [0.20, 0.30, 0.30, 0.20],  # A ->
    [0.20, 0.20, 0.40, 0.20],  # C ->  (C->G boosted)
    [0.30, 0.40, 0.20, 0.10],  # G ->  (G->C boosted)
    [0.30, 0.10, 0.10, 0.50],  # T ->
])
assert np.allclose(T.sum(axis=1), 1.0), "rows must sum to 1"
assert np.allclose(T.sum(axis=0), 1.0), f"cols must sum to 1, got {T.sum(axis=0)}"

# Stationary check (should be uniform [0.25] given doubly stochastic).
import numpy.linalg as la
w, v = la.eig(T.T)
idx = np.argmin(np.abs(w - 1))
stat = np.real(v[:, idx])
stat = stat / stat.sum()
print(f"Stationary distribution: {stat.round(4)}  (expected [0.25, 0.25, 0.25, 0.25])")

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

seqs = []
for _ in range(N):
    seq = np.zeros(L, dtype=int)
    seq[0] = rng.integers(0, 4)  # start uniform
    for i in range(1, L):
        seq[i] = rng.choice(4, p=T[seq[i-1]])
    seqs.append(''.join(bases[seq].tolist()))

import statistics
gcs = [sum(c in 'GC' for c in s) / L for s in seqs[:2000]]
acounts = [s.count('A') for s in seqs[:2000]]
cg_dinucs = [sum(1 for i in range(L-1) if s[i:i+2] == 'CG') for s in seqs[:2000]]
gc_dinucs = [sum(1 for i in range(L-1) if s[i:i+2] == 'GC') for s in seqs[:2000]]
print(f"Per-seq GC: mean={statistics.mean(gcs):.3f} std={statistics.stdev(gcs):.4f}")
print(f"Per-seq A count: mean={statistics.mean(acounts):.2f} std={statistics.stdev(acounts):.3f}")
print(f"Per-seq CG dinuc: mean={statistics.mean(cg_dinucs):.2f} (uniform expected: {199*0.25*0.25:.2f})")
print(f"Per-seq GC dinuc: mean={statistics.mean(gc_dinucs):.2f} (uniform expected: {199*0.25*0.25:.2f})")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
