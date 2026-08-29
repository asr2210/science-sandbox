"""Experiment 011: per-cell-type stratified top-|log2FC|.

010 sorted ALL pooled Tewhey BED entries by |log2FC| and kept top
50k. SKNSH won big (avg r 0.0078) because its BED is small (28k) so
nearly all its strong-activity sequences made the cut. K562 (228k
pool) and HepG2 (109k) high-activity tails were diluted.

This experiment fixes that: take top by |log2FC| WITHIN each cell:
- K562  top 16,667
- HepG2 top 16,667
- SKNSH top 16,666

Total 50k unique regions (deduped by coordinate, prefer cell with
larger |log2FC| if same region appears in multiple BEDs).

Hypothesis: K562 and HepG2 signal will recover; SKNSH may drop
slightly (only 16k of its top instead of ~26k). Overall mean_r
should rise because we're not double-counting SKNSH but instead
using the budget for K562/HepG2 high-activity sequences too.
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200
N = 50_000
PER_CELL = [16_667, 16_667, 16_666]  # K562, HepG2, SKNSH

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
BEDS = [
    ("K562",  os.path.join(ROOT, "data", "ENCFF822KPE.bed")),
    ("HepG2", os.path.join(ROOT, "data", "ENCFF887WCC.bed")),
    ("SKNSH", os.path.join(ROOT, "data", "ENCFF861MOC.bed")),
]
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
EXCLUDE_CHR = {"chr7", "chr13"}

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)

# Per-cell sorted lists of (chrom, s, e, abs_lfc)
per_cell_lists = {}
for cell, bed in BEDS:
    entries = []
    seen = set()
    with open(bed) as f:
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
    per_cell_lists[cell] = entries
    print(f"{cell}: {len(entries)} unique regions")

# Take top per_cell, deduplicating globally — if a region was already
# taken for an earlier cell, skip and grab the next from the current cell's list.
taken_keys = set()
selected = []  # list of (chrom, s, e, cell)
for (cell, _), quota in zip(BEDS, PER_CELL):
    n_taken_for_cell = 0
    for chrom, s, e, lfc in per_cell_lists[cell]:
        key = (chrom, s, e)
        if key in taken_keys:
            continue
        if chrom not in fa.keys():
            continue
        if s < 0 or e > len(fa[chrom]):
            continue
        seq = str(fa[chrom][s:e])
        if "N" in seq or len(seq) != L:
            continue
        taken_keys.add(key)
        selected.append((chrom, s, e, cell, seq, lfc))
        n_taken_for_cell += 1
        if n_taken_for_cell == quota:
            break
    print(f"{cell}: took {n_taken_for_cell} (lowest |lfc| kept {lfc:.3f})")

print(f"total selected: {len(selected)}")
assert len(selected) == N

seqs = [s[4] for s in selected]
rng.shuffle(seqs)

with open(OUT, "w") as f:
    f.write("\n".join(seqs) + "\n")
print(f"wrote {len(seqs)} to {OUT}")
