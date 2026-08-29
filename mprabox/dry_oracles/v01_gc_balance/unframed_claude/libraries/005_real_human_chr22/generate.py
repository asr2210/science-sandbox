"""Experiment 005: Random 200bp slices from human chr22 (hg38).
Excludes Ns; uppercase. Tests whether real human DNA scores higher than random.
"""
import os
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
FASTA = os.path.join(os.path.dirname(__file__), "..", "..", "data", "chr22.fa")
N = 50_000
L = 200

# Load chr22 sequence (skip header lines)
with open(FASTA) as f:
    lines = [ln.strip() for ln in f if not ln.startswith(">")]
seq = "".join(lines).upper()
print(f"Loaded chr22: {len(seq)} bp")

rng = np.random.default_rng(46)
# Sample positions; reject sequences with too many Ns
seqs = []
attempts = 0
max_attempts = N * 5
while len(seqs) < N and attempts < max_attempts:
    attempts += 1
    p = rng.integers(0, len(seq) - L)
    s = seq[p:p+L]
    if s.count("N") == 0 and len(s) == L:
        seqs.append(s)

print(f"Got {len(seqs)} sequences after {attempts} attempts")
assert len(seqs) == N, f"Only got {len(seqs)}"

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {N} sequences to {OUT}")
