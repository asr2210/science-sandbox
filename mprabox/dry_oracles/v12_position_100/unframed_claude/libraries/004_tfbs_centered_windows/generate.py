"""Exp 004: 200bp windows centered on ENCODE TFBS cluster midpoints (chr17/19/22).

Each TFBS cluster represents a region where one or more transcription factors
bind across ENCODE ChIP-seq experiments. Centering 200bp windows on each
cluster midpoint gives a library of sequences that ARE actual TF-bound
regulatory regions — exactly what an MPRA model needs to learn from.

Sampling: uniform random over TFBS clusters that lie wholly within ACGT
sequence on chromosomes we have. We accept duplicate genomic positions if
the cluster row appears for different TFs/cells, treating each as one
training example (this gives weight to high-coverage regulatory regions).
"""
import os
import gzip
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(HERE, "sequences_0.txt")
N, L = 50_000, 200
SEED = 11

def load_chr(name: str) -> str:
    with open(os.path.join(DATA, name)) as f:
        f.readline()
        return "".join(line.strip() for line in f).upper()

chrs = {n: load_chr(f"chr{n}.fa") for n in ("17", "19", "22")}

intervals = []
with gzip.open(os.path.join(DATA, "encRegTfbsClusteredWithCells.hg38.bed.gz"), "rt") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if len(parts) < 3:
            continue
        c = parts[0]
        if c not in ("chr17", "chr19", "chr22"):
            continue
        s, e = int(parts[1]), int(parts[2])
        intervals.append((c[3:], (s + e) // 2))  # store ('17', center)
print(f"intervals on chr17/19/22: {len(intervals)}")

rng = np.random.default_rng(SEED)
idx = rng.permutation(len(intervals))

acgt = set("ACGT")
half = L // 2
seqs = []
for i in idx:
    chr_num, center = intervals[i]
    seq_str = chrs[chr_num]
    start = center - half
    end = start + L
    if start < 0 or end > len(seq_str):
        continue
    w = seq_str[start:end]
    if set(w) <= acgt:
        seqs.append(w)
    if len(seqs) >= N:
        break

assert len(seqs) >= N, f"only got {len(seqs)}"
seqs = seqs[:N]
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {OUT}: {N} x {L}")
