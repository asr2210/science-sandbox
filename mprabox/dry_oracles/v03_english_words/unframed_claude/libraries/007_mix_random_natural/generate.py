"""Exp 007: 25k random + 25k natural genomic.
Test if a mixed library lifts mean_r above either component alone.
"""
import numpy as np, os, sys

N_TOTAL = 50_000
N_HALF = N_TOTAL // 2
L = 200
SEED = 7
rng = np.random.default_rng(SEED)
bases = np.array(list("ACGT"))

# Random half
arr = rng.integers(0, 4, size=(N_HALF, L))
random_seqs = ["".join(row.tolist()) for row in bases[arr]]

# Natural half
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data",
                    "genome_chunks.txt")
with open(DATA) as f:
    chunks = [line.strip() for line in f if line.strip()]
cum = np.cumsum([len(c) for c in chunks])
total_bp = int(cum[-1])

natural = []
attempts = 0
while len(natural) < N_HALF and attempts < N_HALF * 10:
    attempts += 1
    pos = int(rng.integers(0, total_bp - L))
    ci = int(np.searchsorted(cum, pos, side="right"))
    chunk_start = 0 if ci == 0 else int(cum[ci - 1])
    local = pos - chunk_start
    chunk = chunks[ci]
    if local + L > len(chunk):
        continue
    sub = chunk[local:local + L]
    if "N" in sub:
        continue
    natural.append(sub)

assert len(natural) == N_HALF, len(natural)

# Interleave so order is not biased (probably doesn't matter)
all_seqs = []
for r, n in zip(random_seqs, natural):
    all_seqs.append(r)
    all_seqs.append(n)
rng.shuffle(all_seqs)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for s in all_seqs:
        f.write(s + "\n")
print(f"Wrote {len(all_seqs)} sequences (25k random + 25k natural)")
