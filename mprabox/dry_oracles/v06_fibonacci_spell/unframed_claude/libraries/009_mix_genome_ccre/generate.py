"""Experiment 009: Mix of 25k full-genome random + 25k cCRE-centered.

Tests variance hypothesis: adding more "active" cCRE sequences to broad
"baseline" genome sequences could widen the predicted-activity distribution
and increase r. Sources are independent random samples (different seeds).
"""
import pickle
import numpy as np
from pathlib import Path

N_HALF = 25_000
L = 200
SEED = 9

DATA = Path(__file__).parents[2] / "data"
with open(DATA / "hg38_chroms.pkl", "rb") as f:
    chroms = pickle.load(f)

names = list(chroms.keys())
lens = np.array([len(chroms[n]) for n in names], dtype=np.int64)
p = lens / lens.sum()

valid = set("ACGT")
rng = np.random.default_rng(SEED)

# Half 1: full-genome random
def genome_random(n):
    out = []
    while len(out) < n:
        ci = int(rng.choice(len(names), p=p))
        c = names[ci]
        pos = int(rng.integers(0, lens[ci] - L))
        w = chroms[c][pos:pos + L]
        if set(w) <= valid:
            out.append(w)
    return out

# Half 2: cCRE-centered
bed = []
with open(DATA / "cCREs.bed") as f:
    for line in f:
        parts = line.rstrip().split("\t")
        c, s, e = parts[0], int(parts[1]), int(parts[2])
        if c in chroms:
            bed.append((c, s, e))

def ccre_random(n):
    out = []
    while len(out) < n:
        i = int(rng.integers(0, len(bed)))
        c, s, e = bed[i]
        center = (s + e) // 2
        start = center - L // 2
        end = start + L
        if start < 0 or end > len(chroms[c]):
            continue
        w = chroms[c][start:end]
        if set(w) <= valid:
            out.append(w)
    return out

half1 = genome_random(N_HALF)
half2 = ccre_random(N_HALF)
all_seqs = half1 + half2
rng.shuffle(all_seqs)

with open(__file__.replace("generate.py", "sequences_0.txt"), "w") as f:
    for s in all_seqs:
        f.write(s + "\n")

print(f"Wrote {len(all_seqs)} sequences (25k genome + 25k cCRE)")
