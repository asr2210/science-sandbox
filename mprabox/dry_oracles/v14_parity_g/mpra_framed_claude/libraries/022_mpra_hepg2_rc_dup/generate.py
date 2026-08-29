"""Experiment 022: HepG2 strict + RC augmentation.

018 showed HepG2 same-strand duplication boosted HepG2 r 0.0044→0.0049
but K562 below floor (19k) collapsed it. Test if RC-augmented HepG2
dups can give same gain while preserving K562 floor of 22k.

Layout (50k):
  SKNSH 22k (down from 015's 25k — sacrifice a little SKNSH for HepG2)
  HepG2  3k strict + 3k RC = 6k slots (3k unique sites)
  K562  22k unique high-|lfc| (preserve floor)

Hypothesis: RC augmentation may add information beyond same-strand
dups by teaching the model RC-equivariance of regulatory motifs.
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
HEPG2_N = 3_000  # unique sites; will be duplicated as RC
K562_N  = 22_000
TOTAL = 50_000

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)

RC = str.maketrans("ACGT", "TGCA")
def rc(s): return s.translate(RC)[::-1]


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


# SKNSH first
n = 0
last = None
for chrom, s, e, lfc in sknsh:
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    n += 1
    last = lfc
    if n == SKNSH_N: break
print(f"SKNSH took {n} (last |lfc|={last:.3f})")

# HepG2 strict — add ref + RC for each
n_uniq = 0
last = None
for chrom, s, e, lfc in hepg2:
    if n_uniq == HEPG2_N: break
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    slots.append(rc(seq))
    n_uniq += 1
    last = lfc
print(f"HepG2 unique={n_uniq} (×2 with RC = {n_uniq*2} slots) last |lfc|={last:.3f}")

# K562
remaining = TOTAL - len(slots)
n = 0
last = None
for chrom, s, e, lfc in k562:
    if n == remaining: break
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    n += 1
    last = lfc
print(f"K562 took {n} (last |lfc|={last:.3f})")

print(f"total: {len(slots)}")
assert len(slots) == TOTAL

rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote {OUT}")
