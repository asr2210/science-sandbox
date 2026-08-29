"""Exp 010: 50,000 ENCODE cCRE-centered 200bp sequences.

Loads cCRE BED, finds cCREs that fall within downloaded genome chunks,
extracts a 200bp window centered on each cCRE midpoint, samples 50k.
"""
import numpy as np, os, sys
from collections import defaultdict

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "data")
BED = os.path.join(BASE, "GRCh38-cCREs.bed")
CHUNKS1 = os.path.join(BASE, "genome_chunks.txt")
CHUNKS2 = os.path.join(BASE, "genome_chunks_extra.tsv")
L = 200
SEED = 10

# Load all genome chunks into chrom -> list of (start, seq)
chunks_by_chrom = defaultdict(list)

# Original chunks
ORIGINAL = [
    ("chr1",  10_000_000), ("chr2",  30_000_000), ("chr3",  50_000_000),
    ("chr5",  80_000_000), ("chr7",  100_000_000), ("chr10", 60_000_000),
    ("chr12", 40_000_000), ("chr15", 70_000_000), ("chr17", 30_000_000),
    ("chr19", 20_000_000), ("chr21", 30_000_000), ("chr22", 20_000_000),
]
with open(CHUNKS1) as f:
    for (chrom, start), line in zip(ORIGINAL, f):
        seq = line.strip()
        chunks_by_chrom[chrom].append((start, seq))

with open(CHUNKS2) as f:
    for line in f:
        chrom, start, end, seq = line.rstrip("\n").split("\t")
        chunks_by_chrom[chrom].append((int(start), seq))

# Index chunks per chromosome by start
for c in chunks_by_chrom:
    chunks_by_chrom[c].sort()

print(f"Loaded chunks for {len(chunks_by_chrom)} chromosomes")
total_bp = sum(len(s) for vs in chunks_by_chrom.values() for _, s in vs)
print(f"Total bp: {total_bp:,}")

def lookup(chrom, pos):
    """Return (chunk_start, seq) covering pos on chrom, or None."""
    if chrom not in chunks_by_chrom:
        return None
    for cs, seq in chunks_by_chrom[chrom]:
        if cs <= pos < cs + len(seq):
            return cs, seq
    return None

# Walk through cCRE BED, extract 200bp window centered on cCRE midpoint
extracted = []
extracted_types = defaultdict(int)
with open(BED) as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        chrom = parts[0]
        if chrom not in chunks_by_chrom:
            continue
        start, end = int(parts[1]), int(parts[2])
        mid = (start + end) // 2
        win_start = mid - L // 2
        win_end = win_start + L
        hit = lookup(chrom, win_start)
        if hit is None:
            continue
        cs, seq = hit
        if win_end > cs + len(seq):
            continue
        local = win_start - cs
        sub = seq[local:local + L]
        if len(sub) != L or "N" in sub:
            continue
        extracted.append(sub)
        extracted_types[parts[5] if len(parts) > 5 else "?"] += 1

print(f"Extracted {len(extracted)} cCRE windows")
print("Type breakdown:")
for k in sorted(extracted_types, key=extracted_types.get, reverse=True):
    print(f"  {extracted_types[k]} {k}")

# If we have fewer than 50k, replicate with random alternative windows
# from each cCRE (jitter the center within ±50 bp)
N_TARGET = 50_000
rng = np.random.default_rng(SEED)

if len(extracted) >= N_TARGET:
    rng.shuffle(extracted)
    sampled = extracted[:N_TARGET]
else:
    # Re-scan BED with jittered centers to multiply
    sampled = list(extracted)
    needed = N_TARGET - len(sampled)
    print(f"Need {needed} more sequences; generating jittered windows")
    while len(sampled) < N_TARGET:
        with open(BED) as f:
            for line in f:
                if len(sampled) >= N_TARGET:
                    break
                parts = line.rstrip("\n").split("\t")
                chrom = parts[0]
                if chrom not in chunks_by_chrom:
                    continue
                start, end = int(parts[1]), int(parts[2])
                mid = (start + end) // 2
                # add a random jitter
                jitter = int(rng.integers(-60, 61))
                win_start = mid - L // 2 + jitter
                win_end = win_start + L
                hit = lookup(chrom, win_start)
                if hit is None:
                    continue
                cs, seq = hit
                if win_end > cs + len(seq) or win_start < cs:
                    continue
                local = win_start - cs
                sub = seq[local:local + L]
                if len(sub) != L or "N" in sub:
                    continue
                sampled.append(sub)

assert len(sampled) >= N_TARGET, len(sampled)
out_path = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
with open(out_path, "w") as f:
    for s in sampled[:N_TARGET]:
        f.write(s + "\n")
print(f"Wrote {N_TARGET} cCRE sequences to {out_path}")
