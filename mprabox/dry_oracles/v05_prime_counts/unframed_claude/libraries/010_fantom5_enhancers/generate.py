#!/usr/bin/env python3
"""200bp windows centered on/within FANTOM5 enhancers on chr19+chr22.
FANTOM5 is a curated catalog of active enhancers across human cell types.
If oracle's models like real regulatory regions, this should beat
genome-random."""
import os
import numpy as np

N_SEQ = 50_000
LEN = 200
SEED = 10
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "sequences_0.txt")

genomes = {}
for chrom in ("chr19", "chr22"):
    chunks = []
    with open(os.path.join(ROOT, "data", f"{chrom}.fa")) as fh:
        for line in fh:
            if line.startswith(">"):
                continue
            chunks.append(line.strip().upper())
    genomes[chrom] = "".join(chunks)

# Load enhancer regions, expand small ones by flanking
enhancers = []
with open(os.path.join(ROOT, "data", "F5_enhancers.bed")) as fh:
    for line in fh:
        parts = line.rstrip().split("\t")
        chrom = parts[0]
        if chrom not in genomes:
            continue
        start = int(parts[1])
        end = int(parts[2])
        # Always center & expand to at least LEN by padding both sides
        if end - start < LEN:
            center = (start + end) // 2
            start = max(0, center - LEN // 2 - 50)
            end = min(len(genomes[chrom]), center + LEN // 2 + 50)
        if end - start >= LEN:
            enhancers.append((chrom, start, end))

print(f"loaded {len(enhancers)} usable enhancer regions on chr19+chr22")

# Sample weighted by length-LEN+1
weights = np.array([end - start - LEN + 1 for chrom, start, end in enhancers], dtype=float)
weights /= weights.sum()

rng = np.random.default_rng(SEED)
valid_chars = set("ACGT")
seqs = []
attempts = 0
while len(seqs) < N_SEQ and attempts < N_SEQ * 50:
    attempts += 1
    i = int(rng.choice(len(enhancers), p=weights))
    chrom, start, end = enhancers[i]
    pos = int(rng.integers(start, end - LEN + 1))
    s = genomes[chrom][pos:pos + LEN]
    if set(s) <= valid_chars:
        seqs.append(s)

with open(OUT, "w") as f:
    for s in seqs:
        f.write(s + "\n")
print(f"Wrote {len(seqs)} FANTOM5-enhancer windows to {OUT}")
