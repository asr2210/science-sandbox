"""Experiment 004: Real human chr22 200bp windows.

Random non-N 200bp windows from human chr22 (hg38). Tests whether
naturalistic content scores higher than synthetic random.
"""
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 4

FA = Path(__file__).parents[2] / "data" / "chr22.fa"

# Read FASTA (single record), strip header and newlines, upper-case
seq = []
with open(FA) as f:
    for line in f:
        if line.startswith(">"):
            continue
        seq.append(line.strip().upper())
chr_seq = "".join(seq)
print(f"chr22 length: {len(chr_seq):,}")

# Sample N random 200bp windows, rejecting any containing N
rng = np.random.default_rng(SEED)
valid = set("ACGT")
out = []
attempts = 0
max_pos = len(chr_seq) - L
while len(out) < N:
    pos = int(rng.integers(0, max_pos))
    w = chr_seq[pos:pos + L]
    attempts += 1
    if set(w) <= valid:
        out.append(w)

print(f"Took {attempts} attempts to get {N} clean windows")

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")

print(f"Wrote {N} sequences of length {L}")
