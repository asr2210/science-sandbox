"""Exp 014: 50k natural genomic 200bp windows filtered to GC in [0.45, 0.55].
Preserves natural higher-order structure (motifs, repeats) while removing
the wide per-seq GC variance that hurt K562/HepG2 in pure natural.

Hypothesis: K562/HepG2 closer to random; SKNSH closer to natural -> mean
above random.
"""
import numpy as np, os, sys
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "data")
CHUNKS1 = os.path.join(BASE, "genome_chunks.txt")
CHUNKS2 = os.path.join(BASE, "genome_chunks_extra.tsv")
L = 200
N_TARGET = 50_000
SEED = 14
LOW, HIGH = 0.45, 0.55

# Combine all chunks into one big list
all_chunks = []
with open(CHUNKS1) as f:
    for line in f:
        s = line.strip()
        if s:
            all_chunks.append(s)
with open(CHUNKS2) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) == 4:
            all_chunks.append(parts[3])

total_bp = sum(len(c) for c in all_chunks)
cum = np.cumsum([len(c) for c in all_chunks])
print(f"Loaded {len(all_chunks)} chunks; total bp = {total_bp:,}")

rng = np.random.default_rng(SEED)
sampled = []
attempts = 0
max_attempts = N_TARGET * 100

while len(sampled) < N_TARGET and attempts < max_attempts:
    attempts += 1
    pos = int(rng.integers(0, total_bp - L))
    ci = int(np.searchsorted(cum, pos, side="right"))
    chunk_start = 0 if ci == 0 else int(cum[ci - 1])
    local = pos - chunk_start
    chunk = all_chunks[ci]
    if local + L > len(chunk):
        continue
    sub = chunk[local:local + L]
    if "N" in sub:
        continue
    gc = (sub.count("G") + sub.count("C")) / L
    if not (LOW <= gc <= HIGH):
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
print(f"Wrote {N_TARGET} natural sequences (GC in [{LOW}, {HIGH}])")
