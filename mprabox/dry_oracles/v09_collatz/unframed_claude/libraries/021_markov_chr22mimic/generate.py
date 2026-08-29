"""Experiment 021 — synthetic Markov-chain sequences mimicking chr22 dinucleotide stats.

Learn chr22 dinucleotide transition matrix P(next | prev). Generate
50k 200bp sequences via Markov chain. If the natural-DNA win is
purely COMPOSITION/DINUCLEOTIDE-driven, these should match chr22's
0.32. If natural DNA has higher-order structure (motifs, k-mer freqs,
repeats), Markov-mimic will score LOWER.

Definitive test of theory v6 (HepG2 model rewards natural composition).
"""
import numpy as np
from pathlib import Path

rng = np.random.default_rng(21)
N, L = 50_000, 200

fa = Path(__file__).resolve().parents[2] / "data" / "chr22.fa"
parts = []
with fa.open() as f:
    for line in f:
        if line.startswith(">"): continue
        parts.append(line.strip().upper())
seq = "".join(parts)
print(f"chr22: {len(seq):,}")

# Build dinucleotide transition matrix (skip Ns)
bases = "ACGT"
idx = {b: i for i, b in enumerate(bases)}
trans = np.zeros((4, 4), dtype=np.int64)
init = np.zeros(4, dtype=np.int64)

prev = None
n_used = 0
for c in seq:
    if c not in idx:
        prev = None
        continue
    i = idx[c]
    if prev is not None:
        trans[prev][i] += 1
    init[i] += 1
    prev = i
    n_used += 1

print(f"bases used: {n_used:,}")
print(f"base freqs: {init / init.sum()}")
# normalize
trans_p = trans / trans.sum(axis=1, keepdims=True)
init_p = init / init.sum()

# Print dinucleotide stats
print("Transition P(next|prev):")
for i, b in enumerate(bases):
    print(f"  {b} -> " + " ".join(f"{bases[j]}={trans_p[i][j]:.3f}" for j in range(4)))
print(f"CpG transition P(G|C) = {trans_p[idx['C']][idx['G']]:.3f}")
print(f"vs random expectation = {init_p[idx['G']]:.3f}")

# Generate
out = Path(__file__).parent / "sequences_0.txt"
# Pre-compute cumulative for fast sampling
cum = np.cumsum(trans_p, axis=1)
cum_init = np.cumsum(init_p)

with out.open("w") as f:
    for n in range(N):
        s = []
        # start from initial distribution
        r = rng.random()
        cur = int(np.searchsorted(cum_init, r))
        s.append(bases[cur])
        for _ in range(L - 1):
            r = rng.random()
            nxt = int(np.searchsorted(cum[cur], r))
            s.append(bases[nxt])
            cur = nxt
        f.write("".join(s)); f.write("\n")
print(f"Wrote {N} to {out}")
