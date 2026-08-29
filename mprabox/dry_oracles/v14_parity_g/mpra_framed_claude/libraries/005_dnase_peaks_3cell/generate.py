"""Experiment 005: DNase-seq peaks from K562, HepG2, SK-N-SH.

Sample ~16,667 peaks from each cell type's DNase narrowPeak file
(ENCSR000EOT, ENCSR000EJV, ENCSR000ELQ), extract 200bp centered on
peak center. These are KNOWN open chromatin in each cell type —
the most direct possible "active sequence" library.

Rationale: previous libraries gave ~0. Test whether the simulator
responds to KNOWN active regions when we provide them. If yes, the
problem was activity strength. If still 0, the issue is elsewhere.

For generalization concern: these 3 cell types span 3 lineages
(blood/liver/neural). Their union of DNase peaks gives diverse
regulatory grammar that should partially transfer to other cell
types.
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200
PER_CELL = 16_667  # total 50001, will trim

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

import gzip
def load_peaks(path):
    out = []
    with gzip.open(path, "rt") as f:
        for line in f:
            cols = line.rstrip().split("\t")
            chrom = cols[0]
            if "_" in chrom or chrom == "chrM":
                continue
            start, end = int(cols[1]), int(cols[2])
            signal = float(cols[6])
            out.append((chrom, start, end, signal))
    return out

all_seqs = []
for cell, path in PEAKS.items():
    peaks = load_peaks(path)
    print(f"{cell}: {len(peaks)} peaks")
    idx = rng.choice(len(peaks), size=min(int(PER_CELL * 1.3), len(peaks)), replace=False)
    got = []
    for i in idx:
        chrom, s, e, sig = peaks[i]
        c = (s + e) // 2
        ss = c - L // 2
        ee = ss + L
        if ss < 0 or ee > len(fa[chrom]):
            continue
        seq = str(fa[chrom][ss:ee])
        if "N" in seq or len(seq) != L:
            continue
        got.append(seq)
        if len(got) == PER_CELL:
            break
    print(f"  got {len(got)}")
    all_seqs.extend(got)

all_seqs = all_seqs[:50_000]
# If short, top-up with extras from largest pool
while len(all_seqs) < 50_000:
    peaks = load_peaks(PEAKS["K562"])
    idx = rng.choice(len(peaks), size=len(peaks), replace=False)
    for i in idx:
        chrom, s, e, sig = peaks[i]
        c = (s + e) // 2
        ss = c - L // 2
        ee = ss + L
        if ss < 0 or ee > len(fa[chrom]):
            continue
        seq = str(fa[chrom][ss:ee])
        if "N" in seq or len(seq) != L:
            continue
        if seq not in all_seqs:
            all_seqs.append(seq)
            if len(all_seqs) == 50_000:
                break

assert len(all_seqs) == 50_000, len(all_seqs)
rng.shuffle(all_seqs)

with open(OUT, "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"wrote {len(all_seqs)} seqs to {OUT}")
