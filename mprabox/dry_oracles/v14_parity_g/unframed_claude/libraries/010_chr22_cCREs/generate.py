#!/usr/bin/env python3
"""Use real ENCODE cCRE regions on chr22 as sequences.

cCREs are typically 150-350bp. For each, extract a 200bp window centered on
the cCRE. With 21K cCREs on chr22, we need to expand to 50K — do this by
extracting MULTIPLE 200bp windows around each cCRE with random offsets.
"""
import numpy as np
import os
from Bio import SeqIO

N = 50_000
L = 200
SEED = 42

REF = "data/chr22.fa"
CCRE = "data/GRCh38-cCREs.bed"

rec = next(SeqIO.parse(REF, "fasta"))
s = str(rec.seq).upper()

# Read chr22 cCREs
ccres = []
with open(CCRE) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0] != "chr22":
            continue
        st, en = int(parts[1]), int(parts[2])
        ccres.append((st, en))
print(f"chr22 cCREs: {len(ccres)}")

rng = np.random.default_rng(SEED)
out_seqs = []
attempts_per_ccre = N // len(ccres) + 2

for st, en in ccres:
    if len(out_seqs) >= N:
        break
    center = (st + en) // 2
    for _ in range(attempts_per_ccre):
        # Random window position around the cCRE
        # If cCRE longer than 200, pick within
        # If shorter, center with random jitter
        if en - st >= L:
            win_st = rng.integers(st, en - L + 1)
        else:
            jitter = rng.integers(-20, 21)
            win_st = center - L // 2 + jitter
        win_st = max(0, min(len(s) - L, int(win_st)))
        seq = s[win_st : win_st + L]
        if "N" in seq:
            continue
        out_seqs.append(seq)
        if len(out_seqs) >= N:
            break

# If short, fill with random uniform 200bp
print(f"From cCREs: {len(out_seqs)}")
if len(out_seqs) < N:
    bases = np.array(list("ACGT"))
    extra = N - len(out_seqs)
    arr = rng.integers(0, 4, size=(extra, L))
    fill = bases[arr]
    out_seqs.extend(["".join(row) for row in fill])
    print(f"Added {extra} random fillers")

rng.shuffle(out_seqs)
assert len(out_seqs) == N
out = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out, "w") as f:
    f.write("\n".join(out_seqs) + "\n")
print(f"Wrote {len(out_seqs)} cCRE-derived sequences to {out}")
