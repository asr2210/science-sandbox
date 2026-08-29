"""Experiment 007: random 200bp windows from ALL hg38 chromosomes.

Sample proportional to chromosome length so every region of the genome
contributes equivalent density. 50,000 windows total across chr1-22, X, Y.

Tests if maximum within-natural genomic diversity exceeds the 5-chrom
ceiling. This is the cleanest "pure natural diversity" library possible.
"""
from pathlib import Path
import numpy as np
from pyfaidx import Fasta

SEED = 0
N = 50_000
L = 200
DATA = Path(__file__).resolve().parents[2] / "data"
OUT = Path(__file__).parent / "sequences_0.txt"

CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
rng = np.random.default_rng(SEED)

# Load fasta lengths
fas = {c: Fasta(str(DATA / f"hg38.{c}.fa"), as_raw=True,
                sequence_always_upper=True) for c in CHROMS}
lengths = {c: len(fas[c][c]) for c in CHROMS}
total = sum(lengths.values())
print(f"Total genome length: {total/1e9:.2f} Gb across {len(CHROMS)} chroms")

# Allocate sequences proportional to length
allocations = {}
remaining = N
for i, c in enumerate(CHROMS):
    if i == len(CHROMS) - 1:
        allocations[c] = remaining
    else:
        n_c = int(round(N * lengths[c] / total))
        allocations[c] = n_c
        remaining -= n_c
print({c: a for c, a in allocations.items()})

valid = set("ACGT")
all_seqs = []
for c in CHROMS:
    target = allocations[c]
    chrom_len = lengths[c]
    collected = []
    while len(collected) < target:
        batch = rng.integers(0, chrom_len - L, size=max(4 * (target - len(collected)), 100))
        for start in batch:
            if len(collected) >= target:
                break
            s = fas[c][c][int(start):int(start) + L]
            if len(s) == L and set(s).issubset(valid):
                collected.append(s)
    all_seqs.extend(collected)

assert len(all_seqs) == N
rng.shuffle(all_seqs)
with OUT.open("w") as f:
    for s in all_seqs:
        f.write(s)
        f.write("\n")
print(f"Wrote {N} sequences from all 24 chromosomes.")
