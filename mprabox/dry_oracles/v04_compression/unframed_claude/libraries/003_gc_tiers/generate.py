"""Experiment 003: Library with GC content spread across 4 tiers.

Tests the diversity hypothesis (T1). 12,500 seqs at each of GC = 0.30,
0.45, 0.55, 0.70. Within each seq, bases are i.i.d. with those marginal
frequencies. Per-position entropy is similar to uniform random; what
changes is the cross-library variance in GC and downstream features.

Prediction (T1): score on eval_01 > 0.331 (the random uniform baseline).
"""
import os
import numpy as np

N_TOTAL = 50000
LEN = 200
SEED = 44

# (gc_fraction, n_seqs)
TIERS = [(0.30, 12500), (0.45, 12500), (0.55, 12500), (0.70, 12500)]

rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

all_rows = []
for gc, n in TIERS:
    # P(A)=P(T)=(1-gc)/2; P(C)=P(G)=gc/2 — order matches bases array
    p = np.array([(1 - gc) / 2, gc / 2, gc / 2, (1 - gc) / 2])  # A,C,G,T
    idx = rng.choice(4, size=(n, LEN), p=p)
    all_rows.append(bases[idx])

mat = np.concatenate(all_rows, axis=0)
# Shuffle so tiers aren't blocked together (some scorers might care about order)
perm = rng.permutation(N_TOTAL)
mat = mat[perm]

seqs = ["".join(row) for row in mat]
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    f.write("\n".join(seqs) + "\n")

print(f"Wrote {N_TOTAL} seqs across GC tiers {[t[0] for t in TIERS]}")
