"""Experiment 023: K562 with min-distance spacing.

Top 22k K562 by |lfc| has 6,457 pairs within 1kb (30% clustering).
chr19 alone has 2,287 entries (10%). Try greedy selection by |lfc|
with ≥500bp min spacing between selected K562 entries — frees slots
for distinct loci with slightly lower |lfc|, potentially adding
diversity at small cost.

Layout (50k):
  SKNSH 25k (BED)        — 015 reference
  HepG2  3k strict (BED) — 015 reference
  K562  22k spaced (≥500bp gap) by |lfc|

Hypothesis: chromosome-spaced K562 selection trades a tiny amount of
peak |lfc| for substantially more diverse genomic context, helping
generalization.
"""
import os
import bisect
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200
MIN_GAP = 500  # bp gap between selected K562 entries

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
K562_BED  = os.path.join(ROOT, "data", "ENCFF822KPE.bed")
HEPG2_BED = os.path.join(ROOT, "data", "ENCFF887WCC.bed")
SKNSH_BED = os.path.join(ROOT, "data", "ENCFF861MOC.bed")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
EXCLUDE_CHR = {"chr7", "chr13"}

SKNSH_N = 25_000
HEPG2_N = 3_000
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
# Per-chrom sorted-start-coordinates list of selected entries for any source
# (for K562 spacing, only track K562 selections globally)
selected_starts_by_chr = {}


def is_too_close(chrom, s, e, min_gap):
    starts = selected_starts_by_chr.get(chrom)
    if not starts:
        return False
    # find insertion point
    i = bisect.bisect_left(starts, s)
    # check neighbor left
    if i > 0:
        prev_s = starts[i-1]
        if s - (prev_s + L) < min_gap:
            return True
    # check neighbor right
    if i < len(starts):
        next_s = starts[i]
        if next_s - e < min_gap:
            return True
    return False


def register_selection(chrom, s):
    starts = selected_starts_by_chr.setdefault(chrom, [])
    bisect.insort(starts, s)


# SKNSH first (no spacing constraint)
n = 0
last = None
for chrom, s, e, lfc in sknsh:
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    register_selection(chrom, s)
    n += 1
    last = lfc
    if n == SKNSH_N: break
print(f"SKNSH took {n} (last |lfc|={last:.3f})")

# HepG2 strict (no spacing constraint)
n = 0
last = None
for chrom, s, e, lfc in hepg2:
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    register_selection(chrom, s)
    n += 1
    last = lfc
    if n == HEPG2_N: break
print(f"HepG2 took {n} (last |lfc|={last:.3f})")

# K562 with spacing
n = 0
last = None
n_skipped_close = 0
for chrom, s, e, lfc in k562:
    if n == K562_N: break
    if (chrom, s, e) in taken: continue
    if is_too_close(chrom, s, e, MIN_GAP):
        n_skipped_close += 1
        continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    register_selection(chrom, s)
    n += 1
    last = lfc
print(f"K562 took {n} (last |lfc|={last:.3f}); skipped {n_skipped_close} for proximity")

# Final pad if short (shouldn't happen)
if len(slots) < TOTAL:
    fill = TOTAL - len(slots)
    print(f"WARNING short by {fill}; padding K562 without spacing")
    for chrom, s, e, lfc in k562:
        if (chrom, s, e) in taken: continue
        seq = get_seq(chrom, s, e)
        if seq is None: continue
        taken.add((chrom, s, e))
        slots.append(seq)
        if len(slots) == TOTAL: break

print(f"total: {len(slots)}")
assert len(slots) == TOTAL

rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote {OUT}")
