"""Experiment 013: 25k hg38 random + 25k mm10 chr1 random.

Tests cross-species hypothesis: does adding mouse DNA (which shares much
regulatory grammar with human but is also diverged) help model training?

If mouse adds informative diversity → score > 0.139.
If mouse is off-distribution for human MPRA test → score < 0.139.
"""
import pickle
import numpy as np
from pathlib import Path

N_HALF = 25_000
L = 200
SEED = 13

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    hg = pickle.load(f)

# Load mouse chr1
mm_seq = []
with open(DATA / "mm10_chr1.fa") as f:
    for line in f:
        if line.startswith(">"):
            continue
        mm_seq.append(line.strip().upper())
mm_chr1 = "".join(mm_seq)
print(f"mm10 chr1 length: {len(mm_chr1):,}")

names = list(hg.keys())
lens = np.array([len(hg[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

rng = np.random.default_rng(SEED)
valid = set("ACGT")

# Half 1: hg38
def hg38_random(n):
    out = []
    while len(out) < n:
        ci = int(rng.choice(len(names), p=p))
        c = names[ci]
        pos = int(rng.integers(0, lens[ci] - L))
        w = hg[c][pos:pos + L]
        if set(w) <= valid:
            out.append(w)
    return out

# Half 2: mm10 chr1
def mm10_random(n):
    out = []
    while len(out) < n:
        pos = int(rng.integers(0, len(mm_chr1) - L))
        w = mm_chr1[pos:pos + L]
        if set(w) <= valid:
            out.append(w)
    return out

a = hg38_random(N_HALF)
b = mm10_random(N_HALF)
all_seqs = a + b
rng.shuffle(all_seqs)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in all_seqs:
        f.write(s + "\n")
print(f"Wrote {len(all_seqs)} sequences (25k hg38 + 25k mm10_chr1)")
