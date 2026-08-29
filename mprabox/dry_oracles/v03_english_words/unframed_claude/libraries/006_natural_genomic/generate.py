"""Exp 006: 50,000 random 200bp windows from human genome (hg38).
Pulls from data/genome_chunks.txt (12 x 1Mb regions across chromosomes).
Filters windows containing N. Sampled with random positions.
"""
import numpy as np
import os, sys

N_TARGET = 50_000
L = 200
SEED = 6
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data", "genome_chunks.txt")

with open(DATA) as f:
    chunks = [line.strip() for line in f if line.strip()]
print(f"Loaded {len(chunks)} chunks; total bp = {sum(len(c) for c in chunks)}")

rng = np.random.default_rng(SEED)
sampled = []
total_bp = sum(len(c) for c in chunks)
# Build cumulative offsets for sampling proportional to chunk length
cum = np.cumsum([len(c) for c in chunks])

attempts = 0
max_attempts = N_TARGET * 5
while len(sampled) < N_TARGET and attempts < max_attempts:
    attempts += 1
    pos = rng.integers(0, total_bp - L)
    # find which chunk
    ci = int(np.searchsorted(cum, pos, side="right"))
    chunk_start = 0 if ci == 0 else cum[ci - 1]
    local = pos - chunk_start
    chunk = chunks[ci]
    if local + L > len(chunk):
        continue
    sub = chunk[local:local + L]
    if "N" in sub:
        continue
    sampled.append(sub)

print(f"Sampled {len(sampled)} sequences in {attempts} attempts")
if len(sampled) < N_TARGET:
    print(f"WARNING: only got {len(sampled)} sequences", file=sys.stderr)
    sys.exit(1)

out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for s in sampled[:N_TARGET]:
        f.write(s + "\n")
print(f"Wrote {N_TARGET} natural sequences to {out_path}")
