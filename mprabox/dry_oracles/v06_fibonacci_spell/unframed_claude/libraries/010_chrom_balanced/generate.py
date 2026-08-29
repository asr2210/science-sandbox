"""Experiment 010: Chromosome-balanced random sampling.

Each of 24 canonical chromosomes contributes ~2083 sequences (50k / 24).
Tests whether under-sampling small/gene-dense chromosomes hurts score.
"""
import pickle
import numpy as np
from pathlib import Path

N = 50_000
L = 200
SEED = 10

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
per_chrom = N // len(names)
remainder = N - per_chrom * len(names)

rng = np.random.default_rng(SEED)
valid = set("ACGT")
out = []
for i, name in enumerate(names):
    n = per_chrom + (1 if i < remainder else 0)
    seq = chroms[name]
    got = 0
    attempts = 0
    while got < n:
        pos = int(rng.integers(0, len(seq) - L))
        w = seq[pos:pos + L]
        attempts += 1
        if set(w) <= valid:
            out.append(w)
            got += 1
        if attempts > n * 10:
            print(f"WARNING: chrom {name} struggled, attempts={attempts}, got={got}")
            break

print(f"Generated {len(out)} sequences across {len(names)} chromosomes")
rng.shuffle(out)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in out:
        f.write(s + "\n")

print(f"Wrote {len(out)} sequences of length {L}")
