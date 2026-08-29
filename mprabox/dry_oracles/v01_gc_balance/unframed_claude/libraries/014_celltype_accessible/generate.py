"""Experiment 014: Combined cell-type accessible regions.
~17k K562 ATAC + 17k HepG2 ATAC + 16k SK-N-SH DNase = 50k 200bp sequences.
Each is centered on the peak summit (or peak center if summit missing).
Tests whether cell-type-specific accessible chromatin (where the eval cell lines
have regulatory activity) beats generic real DNA.
"""
import os
import numpy as np
from pyfaidx import Fasta

OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FASTA = os.path.join(ROOT, "hg38.fa")
L = 200

fa = Fasta(FASTA, sequence_always_upper=True, as_raw=True)
chrom_lens = {k: len(fa[k]) for k in fa.keys()}

def load_peaks(path):
    peaks = []
    with open(path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3 or not parts[0].startswith("chr"):
                continue
            chrom, start, end = parts[0], int(parts[1]), int(parts[2])
            # narrowPeak: col 10 = relative summit (offset from start)
            if len(parts) >= 10 and parts[9].isdigit():
                summit = start + int(parts[9])
            else:
                summit = (start + end) // 2
            # Use signal (col 7 = signalValue) for ranking if available
            try:
                signal = float(parts[6])
            except Exception:
                signal = 0.0
            peaks.append((chrom, summit, signal))
    return peaks

print("Loading K562 ATAC...")
k562 = load_peaks(os.path.join(ROOT, "K562_ATAC.bed"))
print(f"  {len(k562)} peaks")
print("Loading HepG2 ATAC...")
hepg2 = load_peaks(os.path.join(ROOT, "HepG2_ATAC.bed"))
print(f"  {len(hepg2)} peaks")
print("Loading SK-N-SH DNase...")
sknsh = load_peaks(os.path.join(ROOT, "SKNSH_DNase.bed"))
print(f"  {len(sknsh)} peaks")

rng = np.random.default_rng(90)
seqs = []

def sample_peaks(peaks, n, rng):
    # Sort by signal (high first) and take top * some factor to ensure quality,
    # then sample n with replacement (or without if enough).
    sorted_peaks = sorted(peaks, key=lambda x: -x[2])
    # Use top half (or all if less)
    pool = sorted_peaks[:max(n * 3, len(sorted_peaks) // 2)]
    idx = rng.choice(len(pool), size=n, replace=len(pool) < n)
    out = []
    for i in idx:
        chrom, summit, _sig = pool[i]
        if chrom not in chrom_lens:
            continue
        p = max(0, min(summit - L // 2, chrom_lens[chrom] - L))
        s = str(fa[chrom][p:p+L])
        if len(s) == L and "N" not in s:
            out.append(s)
    return out

s_k562 = sample_peaks(k562, 17_000, rng)
print(f"  K562 yielded {len(s_k562)}")
s_hepg2 = sample_peaks(hepg2, 17_000, rng)
print(f"  HepG2 yielded {len(s_hepg2)}")
s_sknsh = sample_peaks(sknsh, 16_000, rng)
print(f"  SK-N-SH yielded {len(s_sknsh)}")

seqs = s_k562 + s_hepg2 + s_sknsh

# Top up if anything fell short
all_sorted = sorted(k562 + hepg2 + sknsh, key=lambda x: -x[2])
while len(seqs) < 50_000:
    chrom, summit, _ = all_sorted[rng.integers(0, min(len(all_sorted), 200_000))]
    if chrom not in chrom_lens:
        continue
    p = max(0, min(summit - L // 2, chrom_lens[chrom] - L))
    s = str(fa[chrom][p:p+L])
    if len(s) == L and "N" not in s:
        seqs.append(s)

seqs = seqs[:50_000]
rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"Wrote {len(seqs)} sequences")
