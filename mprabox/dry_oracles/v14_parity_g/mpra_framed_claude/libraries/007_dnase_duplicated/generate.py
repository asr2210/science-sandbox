"""Experiment 007: top 5,000 DNase peaks duplicated 10x.

5,000 highest-signal DNase peaks (across K562/HepG2/SK-N-SH), each
duplicated 10 times = 50,000 lines.

Hypothesis: if the simulator measures each LINE independently and is
stochastic, duplicates give replicate measurements per unique sequence.
The model then trains on cleaner per-sequence signal (average of 10
noisy measurements >> single noisy measurement).

Test: if mean_r improves notably over 005 (same 50k unique peaks),
the simulator IS measuring per-line and duplication is valuable.
"""
import os
import gzip
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200
N_UNIQUE = 5_000
N_COPIES = 10

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
PEAKS = {
    "K562":   os.path.join(ROOT, "data", "ENCFF821KDJ.bed.gz"),
    "HepG2":  os.path.join(ROOT, "data", "ENCFF341XEM.bed.gz"),
    "SK-N-SH":os.path.join(ROOT, "data", "ENCFF752OZB.bed.gz"),
}
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)

# Pool all peaks with their signal, take top 5000 by signal
all_peaks = []
for cell, path in PEAKS.items():
    with gzip.open(path, "rt") as f:
        for line in f:
            cols = line.rstrip().split("\t")
            chrom = cols[0]
            if "_" in chrom or chrom == "chrM":
                continue
            s, e = int(cols[1]), int(cols[2])
            signal = float(cols[6])
            all_peaks.append((signal, chrom, s, e))

all_peaks.sort(reverse=True)  # high signal first
print(f"top 5 peak signals: {[round(p[0],1) for p in all_peaks[:5]]}")

unique_seqs = []
seen = set()
for sig, chrom, s, e in all_peaks:
    c = (s + e) // 2
    ss = c - L // 2
    ee = ss + L
    if ss < 0 or ee > len(fa[chrom]):
        continue
    seq = str(fa[chrom][ss:ee])
    if "N" in seq or len(seq) != L or seq in seen:
        continue
    seen.add(seq)
    unique_seqs.append(seq)
    if len(unique_seqs) == N_UNIQUE:
        break

print(f"got {len(unique_seqs)} unique top-signal sequences")

# Duplicate
all_seqs = unique_seqs * N_COPIES
assert len(all_seqs) == 50_000
rng.shuffle(all_seqs)

with open(OUT, "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"wrote {len(all_seqs)} lines ({len(set(all_seqs))} unique) to {OUT}")
