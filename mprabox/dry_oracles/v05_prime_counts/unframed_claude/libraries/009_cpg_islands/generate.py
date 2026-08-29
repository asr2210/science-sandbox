#!/usr/bin/env python3
"""Sample 200bp windows from CpG islands (chr19 + chr22).
CpG islands are dense regulatory regions (promoters mostly).
If oracle's models like regulatory regions, this should beat
random genome windows."""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 9
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "sequences_0.txt")

# Load chr19 and chr22
genomes = {}
for chrom in ("chr19", "chr22"):
    fa = os.path.join(ROOT, "data", f"{chrom}.fa")
    chunks = []
    with open(fa) as fh:
        for line in fh:
            if line.startswith(">"):
                continue
            chunks.append(line.strip().upper())
    genomes[chrom] = "".join(chunks)

# Load CpG islands BED-like file (UCSC format)
# Columns: bin chrom chromStart chromEnd name length cpgNum gcNum perCpg perGc obsExp
cpgi = []
with open(os.path.join(ROOT, "data", "cpgIslandExt.txt")) as fh:
    for line in fh:
        parts = line.rstrip().split("\t")
        chrom = parts[1]
        if chrom not in genomes:
            continue
        start = int(parts[2])
        end = int(parts[3])
        if end - start >= LEN:
            cpgi.append((chrom, start, end))
print(f"loaded {len(cpgi)} CpG islands on chr19+chr22")

# Sample windows: pick CpGI weighted by (length - LEN + 1), then random start
rng = np.random.default_rng(SEED)
weights = np.array([end - start - LEN + 1 for chrom, start, end in cpgi], dtype=float)
weights /= weights.sum()

valid_chars = set("ACGT")
seqs = []
attempts = 0
max_attempts = N_SEQ * 50
while len(seqs) < N_SEQ and attempts < max_attempts:
    attempts += 1
    i = int(rng.choice(len(cpgi), p=weights))
    chrom, start, end = cpgi[i]
    pos = int(rng.integers(start, end - LEN + 1))
    s = genomes[chrom][pos:pos + LEN]
    if set(s) <= valid_chars:
        seqs.append(s)

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} CpG-island windows to {OUT}")
