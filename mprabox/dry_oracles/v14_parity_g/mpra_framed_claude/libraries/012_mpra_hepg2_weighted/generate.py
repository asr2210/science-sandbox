"""Experiment 012: HepG2-weighted budget (15/25/10).

011 with even budget (16.7k each) showed:
- K562   avg r = 0.0024 (good — improved 5x)
- HepG2  avg r = 0.0009 (essentially flat — bottleneck)
- SKNSH  avg r = 0.0075 (strong)

HepG2 is the laggard. Two competing hypotheses:
(a) HepG2 MPRA data is noisy → needs MORE sequences for the model
    to average over the noise.
(b) HepG2 needs a stricter |lfc| bar (its 011 threshold was 0.97,
    K562 was 2.26).

This experiment tests (a): give HepG2 the biggest budget, at the
cost of K562 and SKNSH.
- K562   top 15,000
- HepG2  top 25,000 (effective threshold should drop slightly)
- SKNSH  top 10,000 (we know SKNSH saturates well below 16k)
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200
PER_CELL = [("K562", 15_000), ("HepG2", 25_000), ("SKNSH", 10_000)]

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
BED_PATH = {
    "K562":  os.path.join(ROOT, "data", "ENCFF822KPE.bed"),
    "HepG2": os.path.join(ROOT, "data", "ENCFF887WCC.bed"),
    "SKNSH": os.path.join(ROOT, "data", "ENCFF861MOC.bed"),
}
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
EXCLUDE_CHR = {"chr7", "chr13"}

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)

per_cell_sorted = {}
for cell, _ in PER_CELL:
    entries = []
    seen = set()
    with open(BED_PATH[cell]) as f:
        for line in f:
            cols = line.rstrip().split("\t")
            chrom = cols[0]
            if chrom in EXCLUDE_CHR or "_" in chrom or chrom == "chrM":
                continue
            s, e = int(cols[1]), int(cols[2])
            if e - s != L:
                c = (s + e) // 2
                s = c - L // 2
                e = s + L
            try:
                lfc = float(cols[6])
            except (ValueError, IndexError):
                continue
            key = (chrom, s, e)
            if key in seen:
                continue
            seen.add(key)
            entries.append((chrom, s, e, abs(lfc)))
    entries.sort(key=lambda r: -r[3])
    per_cell_sorted[cell] = entries
    print(f"{cell}: {len(entries)} unique regions")

taken = set()
seqs = []
for cell, quota in PER_CELL:
    n = 0
    last_lfc = None
    for chrom, s, e, lfc in per_cell_sorted[cell]:
        key = (chrom, s, e)
        if key in taken:
            continue
        if chrom not in fa.keys():
            continue
        if s < 0 or e > len(fa[chrom]):
            continue
        seq = str(fa[chrom][s:e])
        if "N" in seq or len(seq) != L:
            continue
        taken.add(key)
        seqs.append(seq)
        n += 1
        last_lfc = lfc
        if n == quota:
            break
    print(f"{cell}: took {n} (lowest |lfc| {last_lfc:.3f})")

print(f"total: {len(seqs)}")
assert len(seqs) == 50_000

rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote to {OUT}")
