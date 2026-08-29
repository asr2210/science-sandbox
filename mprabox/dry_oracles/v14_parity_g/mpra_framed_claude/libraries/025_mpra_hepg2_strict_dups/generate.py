"""Experiment 025: HepG2 strict same-strand dups, K22 preserved.

018 (K19/H6-dup/S25) → HepG2 r=0.0049 (best), but K19 < floor of 22.
022 (K22/H6-RC-dup/S22) → HepG2 r=0.0029 (RC bad).
024 (K22/H6-unique looser/S22) → HepG2 r=0.0027 (expansion hurts).

Isolate the variable: same-strand dup of strict-3k @ |lfc|≥3.76, with
K22 preserved (drop SKNSH to 22 to make room). Tests the cleanest
version of "HepG2 dup helps HepG2 r".

Layout (50k):
  SKNSH 22k (down from 25k)
  HepG2  3k strict + 3k same-strand dup = 6k slots (3k unique)
  K562  22k (preserved floor)
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

SKNSH_N = 22_000
HEPG2_UNIQUE = 3_000  # ×2 same-strand dup
K562_N  = 22_000
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


print("loading BEDs...")
sknsh = load_bed_sorted(SKNSH_BED)
hepg2 = load_bed_sorted(HEPG2_BED)
k562  = load_bed_sorted(K562_BED)
print(f"SKNSH={len(sknsh)}, HepG2={len(hepg2)}, K562={len(k562)}")


slots = []
taken = set()

# SKNSH
n = 0; last = None
for chrom, s, e, lfc in sknsh:
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    n += 1; last = lfc
    if n == SKNSH_N: break
print(f"SKNSH took {n} (last |lfc|={last:.3f})")

# HepG2 strict + dup
n = 0; last = None
for chrom, s, e, lfc in hepg2:
    if n == HEPG2_UNIQUE: break
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)  # ref
    slots.append(seq)  # same-strand dup
    n += 1; last = lfc
print(f"HepG2 unique={n} ×2 dup = {n*2} slots (last |lfc|={last:.3f})")

# K562
remaining = TOTAL - len(slots)
n = 0; last = None
for chrom, s, e, lfc in k562:
    if n == remaining: break
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    n += 1; last = lfc
print(f"K562 took {n} (last |lfc|={last:.3f})")

print(f"total: {len(slots)}")
assert len(slots) == TOTAL

rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote {OUT}")
