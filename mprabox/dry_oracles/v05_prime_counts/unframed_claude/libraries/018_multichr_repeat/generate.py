#!/usr/bin/env python3
"""Repeat-only windows pooled from chr1 + chr19 + chr22.

Tests if cross-chromosome repeat-class diversity boosts r above
chr19-only repeats (0.0518)."""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 18
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "sequences_0.txt")

lower_acgt = set("acgt")
rng = np.random.default_rng(SEED)

def get_repeat_windows(fa_path, n_target, seed_offset):
    chunks = []
    with open(fa_path) as fh:
        for line in fh:
            if line.startswith(">"):
                continue
            chunks.append(line.strip())
    genome = "".join(chunks)
    local_rng = np.random.default_rng(SEED + seed_offset)
    seqs = []
    attempts = 0
    while len(seqs) < n_target and attempts < n_target * 1000:
        attempts += 1
        start = int(local_rng.integers(0, len(genome) - LEN))
        s = genome[start:start + LEN]
        if set(s) <= lower_acgt:
            seqs.append(s.upper())
    return seqs

# ~17K from each → 51K, then shuffle and take 50K
N_PER = 17_000
seqs = []
for chr_name, off in [("chr1", 0), ("chr19", 1), ("chr22", 2)]:
    fa = os.path.join(ROOT, "data", f"{chr_name}.fa")
    s = get_repeat_windows(fa, N_PER, off)
    seqs.extend(s)
    print(f"  {chr_name}: {len(s)} repeat windows")

rng.shuffle(seqs)
seqs = seqs[:N_SEQ]
with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} multi-chr repeat-only sequences")
