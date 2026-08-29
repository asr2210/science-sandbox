"""Experiment 015: K20/H3/S27 — optimum per-cell budget allocation.

013: K=20, H=10, S=20 → mean_r=0.0039 (K=0.0020, H=0.0021, S=0.0076)
014: K=25, H=5,  S=20 → mean_r=0.0039 (K=0.0010, H=0.0028, S=0.0078)

Hypothesis: K562 sweet spot ≈ 20k @ |lfc|≥2.0; HepG2 keeps improving
with stricter cut. Free budget → SKNSH. Total 50k = 20 + 3 + 27.
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200
# SKNSH BED ~25k unique. Process SKNSH first (smallest), then HepG2,
# then K562 last (largest pool, used to fill to exactly 50k).
PER_CELL = [("SKNSH", 27_000), ("HepG2", 3_000), ("K562", 50_000)]
TOTAL = 50_000

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
    remaining = TOTAL - len(seqs)
    eff_quota = min(quota, remaining)
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
        if n == eff_quota:
            break
    print(f"{cell}: took {n} (lowest |lfc| {last_lfc:.3f})")

print(f"total: {len(seqs)}")
assert len(seqs) == TOTAL

rng.shuffle(seqs)
with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote to {OUT}")
