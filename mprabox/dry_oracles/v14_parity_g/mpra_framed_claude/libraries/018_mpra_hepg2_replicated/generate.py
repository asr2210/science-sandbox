"""Experiment 018: HepG2 strict 3k duplicated 2x.

Tests whether duplicating ultra-strict HepG2 sequences gives the model
extra "MPRA replicate" effect that boosts HepG2 signal further.

Layout:
- SKNSH 25k all unique (proven optimum)
- HepG2 3k strict ULTRA × 2 dups = 6 slots
- K562 19k strict (|lfc|≥~1.9) — 3 fewer than 015's 22 to make room

Total = 25 + 6 + 19 = 50 slots; 47 unique sequences.

If HepG2 r climbs from 0.0044 to e.g. 0.0065 → replicating helps.
If K562 r drops below 0.0024 → K562 needs ≥22k unique.
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
K562_BED  = os.path.join(ROOT, "data", "ENCFF822KPE.bed")
HEPG2_BED = os.path.join(ROOT, "data", "ENCFF887WCC.bed")
SKNSH_BED = os.path.join(ROOT, "data", "ENCFF861MOC.bed")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
EXCLUDE_CHR = {"chr7", "chr13"}

K562_N = 19_000
HEPG2_N_UNIQUE = 3_000
HEPG2_DUPS = 2
SKNSH_N = 25_000
TOTAL = 50_000

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)


def load_bed_sorted(path):
    entries = []
    seen = set()
    with open(path) as f:
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
    return entries


def get_seq(chrom, s, e):
    if chrom not in fa.keys():
        return None
    if s < 0 or e > len(fa[chrom]):
        return None
    seq = str(fa[chrom][s:e])
    if "N" in seq or len(seq) != L:
        return None
    return seq


sknsh = load_bed_sorted(SKNSH_BED)
hepg2 = load_bed_sorted(HEPG2_BED)
k562  = load_bed_sorted(K562_BED)
print(f"SKNSH={len(sknsh)}, HepG2={len(hepg2)}, K562={len(k562)}")

slots = []
taken = set()

# SKNSH 25k unique
n = 0
for chrom, s, e, lfc in sknsh:
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    n += 1
    if n == SKNSH_N: break
print(f"SKNSH took {n} unique (lowest |lfc|={lfc:.3f})")

# HepG2 3k ultra-strict × 2 dups = 6 slots
n = 0
hepg2_seqs = []
for chrom, s, e, lfc in hepg2:
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    hepg2_seqs.append(seq)
    n += 1
    if n == HEPG2_N_UNIQUE: break
for _ in range(HEPG2_DUPS):
    slots.extend(hepg2_seqs)
print(f"HepG2 took {n} unique x {HEPG2_DUPS} dups = {n*HEPG2_DUPS} slots (lowest |lfc|={lfc:.3f})")

# K562 fills the rest
remaining = TOTAL - len(slots)
n = 0
for chrom, s, e, lfc in k562:
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    n += 1
    if n == remaining: break
print(f"K562 took {n} unique (lowest |lfc|={lfc:.3f})")

print(f"total slots: {len(slots)}")
assert len(slots) == TOTAL

rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote to {OUT}")
