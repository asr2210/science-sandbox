"""Experiment 013 — Mixed DHS peaks from K562 + HepG2 + SK-N-SH.

Use ENCODE DNase-seq narrowPeak files for K562 (ENCFF274YGF),
HepG2 (ENCFF973TJW), SK-N-SH (ENCFF752OZB). Sample peaks from
chr1, chr18, chr19, chr22 (the chromosome sequences we have).
Take 200bp windows centered on each peak.

Library composition: ~equal parts from each cell type, so each
cell-type model gets to score its own active sequences highly.
"""
import gzip
import numpy as np
from pathlib import Path

rng = np.random.default_rng(13)
N, L = 50_000, 200

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

# Load chromosomes
chrom_seq = {}
for name in ("chr1", "chr18", "chr19", "chr22"):
    parts = []
    with (DATA / f"{name}.fa").open() as f:
        for line in f:
            if line.startswith(">"):
                continue
            parts.append(line.strip().upper())
    chrom_seq[name] = "".join(parts)
    print(f"{name}: {len(chrom_seq[name]):,}")

# Load peaks per cell type, restrict to our chroms
def load_peaks(name):
    peaks = []
    with gzip.open(DATA / f"{name}_dnase.bed.gz", "rt") as f:
        for line in f:
            if line.startswith("#") or line.startswith("chrom"):
                continue
            parts = line.rstrip("\n").split("\t")
            try:
                ch, s, e = parts[0], int(parts[1]), int(parts[2])
            except (ValueError, IndexError):
                continue
            if ch not in chrom_seq:
                continue
            peaks.append((ch, s, e))
    return peaks

k562 = load_peaks("k562")
hepg2 = load_peaks("hepg2")
sknsh = load_peaks("sknsh")
print(f"peaks (chr1/18/19/22): K562={len(k562)}, HepG2={len(hepg2)}, SKNSH={len(sknsh)}")

# Compose: target 50k. Sample equal parts (with replacement if needed)
per_set = N // 3 + 1  # ~16,667

def sample_windows(peaks, k):
    seqs = []
    while len(seqs) < k:
        idx = int(rng.integers(0, len(peaks)))
        ch, s, e = peaks[idx]
        mid = (s + e) // 2
        ps = mid - L // 2
        pe = ps + L
        if ps < 0 or pe > len(chrom_seq[ch]):
            continue
        seq = chrom_seq[ch][ps:pe]
        if "N" in seq:
            continue
        seqs.append(seq)
    return seqs

all_seqs = sample_windows(k562, per_set) + sample_windows(hepg2, per_set) + sample_windows(sknsh, per_set)
rng.shuffle(all_seqs)
all_seqs = all_seqs[:N]
print(f"final: {len(all_seqs)}")

out = Path(__file__).parent / "sequences_0.txt"
with out.open("w") as f:
    for s in all_seqs:
        f.write(s); f.write("\n")
print(f"Wrote to {out}")
