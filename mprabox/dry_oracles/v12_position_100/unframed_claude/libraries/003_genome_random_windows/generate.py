"""Exp 003: random 200bp windows from human chromosomes 17/19/22.

Tests whether real human genomic DNA (mostly non-regulatory but with
realistic local structure: repeats, gene bodies, occasional regulatory
elements) significantly beats random/dinuc.
"""
import os
import re
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
N, L = 50_000, 200
SEED = 7

def load_chr(name: str) -> str:
    with open(os.path.join(DATA, name)) as f:
        f.readline()  # skip header
        return "".join(line.strip() for line in f).upper()

chrs = [load_chr("chr17.fa"), load_chr("chr19.fa"), load_chr("chr22.fa")]
print("chr lens:", [len(c) for c in chrs])

rng = np.random.default_rng(SEED)

# Sample windows proportional to chromosome length.
weights = np.array([len(c) for c in chrs], dtype=np.float64)
weights /= weights.sum()
per_chr = rng.multinomial(N * 2, weights)  # oversample to allow rejection of Ns

acgt = set("ACGT")
seqs = []
for ci, n in enumerate(per_chr):
    c = chrs[ci]
    starts = rng.integers(0, len(c) - L + 1, size=n)
    for s in starts:
        w = c[s:s + L]
        if len(w) == L and set(w) <= acgt:
            seqs.append(w)
        if len(seqs) >= N:
            break
    if len(seqs) >= N:
        break

assert len(seqs) >= N, f"only got {len(seqs)}"
seqs = seqs[:N]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
