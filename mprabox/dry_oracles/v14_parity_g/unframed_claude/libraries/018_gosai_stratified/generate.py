#!/usr/bin/env python3
"""Gosai sequences uniformly stratified across activity bins.
Each cell line is binned into 10 quantiles; sample evenly across product bins.
This maximizes coverage of the joint activity space.
"""
import numpy as np
import os

N = 50_000
L = 200
SEED = 42

SRC = "data/evaluator_data/41586_2024_8070_MOESM4_ESM.txt"

K = []
H = []
S = []
seqs = []
with open(SRC) as f:
    h = f.readline().rstrip("\n").split("\t")
    iseq = h.index("sequence")
    iK = h.index("K562_log2FC")
    iH = h.index("HepG2_log2FC")
    iS = h.index("SKNSH_log2FC")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) <= iseq: continue
        s = parts[iseq].upper()
        if len(s) != L or not set(s) <= set("ACGT"): continue
        try:
            k = float(parts[iK]); h_ = float(parts[iH]); sn = float(parts[iS])
        except ValueError:
            continue
        K.append(k); H.append(h_); S.append(sn); seqs.append(s)

K = np.asarray(K); H = np.asarray(H); S = np.asarray(S)
n_total = len(K)
print(f"Total: {n_total}")

# 8 bins per cell line based on quantiles
nb = 8
def bin_of(x):
    q = np.quantile(x, np.linspace(0, 1, nb + 1)[1:-1])
    return np.searchsorted(q, x)

bK = bin_of(K); bH = bin_of(H); bS = bin_of(S)
group = bK * nb * nb + bH * nb + bS  # 512 groups

# Build group → list of indices
from collections import defaultdict
groups = defaultdict(list)
for i, g in enumerate(group):
    groups[int(g)].append(i)

rng = np.random.default_rng(SEED)
# Pick proportionally to sqrt of group size (smooth uniform vs proportional)
sizes = {g: len(idxs) for g, idxs in groups.items()}
weights = {g: np.sqrt(sz) for g, sz in sizes.items()}
total_w = sum(weights.values())

picks = []
for g, w in weights.items():
    n_g = max(1, int(round(N * w / total_w)))
    take = min(n_g, len(groups[g]))
    chosen_idx = rng.choice(groups[g], size=take, replace=False)
    picks.extend(int(i) for i in chosen_idx)

# Trim or pad
if len(picks) > N:
    picks = list(rng.choice(picks, size=N, replace=False))
elif len(picks) < N:
    extra = rng.choice(n_total, size=N - len(picks), replace=False)
    picks.extend(int(i) for i in extra)

chosen = [seqs[i] for i in picks]
rng.shuffle(chosen)

out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(chosen) + "\n")
print(f"Wrote {len(chosen)} stratified Gosai sequences to {out}")
print(f"Filled {len(groups)} groups (8^3=512 max)")
