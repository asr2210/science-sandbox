"""Experiment 020: HepG2 ref+alt augmentation.

K562 ref+alt pairing broke K562 in 017, but unexpectedly raised HepG2 r.
Test the converse: HepG2 ref+alt for top 3k HepG2 strict. Does
HepG2 ref+alt pairing help HepG2 (or break it like K562)?

Layout (50k):
- SKNSH 22k (down from 25k to make room)
- HepG2 3k ref + 3k alt = 6 slots (ultra-strict |lfc|≥3.76 ref)
- K562 22k ref strict (keep proven K562 budget)

Tests:
- Does HepG2 ref+alt augmentation help HepG2?
- Does SKNSH at 22k (vs 25k) materially hurt SKNSH r?
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
HEPG2_N_UNIQUE = 3_000
HEPG2_ALT_N = 3_000  # alt allele variants for the same 3k
K562_N = 22_000
TOTAL = 50_000

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)


def load_bed_sorted_with_name(path):
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
            entries.append((chrom, s, e, abs(lfc), cols[3]))
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


def parse_ref_alt(name):
    parts = name.split(":")
    if len(parts) < 4:
        return None
    ref, alt = parts[2], parts[3]
    if len(ref) != 1 or len(alt) != 1:
        return None
    return ref.upper(), alt.upper()


print("loading BEDs...")
sknsh = load_bed_sorted_with_name(SKNSH_BED)
hepg2 = load_bed_sorted_with_name(HEPG2_BED)
k562  = load_bed_sorted_with_name(K562_BED)
print(f"SKNSH={len(sknsh)}, HepG2={len(hepg2)}, K562={len(k562)}")

slots = []
taken = set()

# SKNSH 22k
n = 0
for chrom, s, e, lfc, name in sknsh:
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    n += 1
    if n == SKNSH_N: break
print(f"SKNSH took {n}")

# HepG2 ultra-strict 3k REF + ALT
n_ref = 0
n_alt = 0
for chrom, s, e, lfc, name in hepg2:
    if n_ref == HEPG2_N_UNIQUE: break
    if (chrom, s, e) in taken: continue
    ref_seq = get_seq(chrom, s, e)
    if ref_seq is None: continue
    parsed = parse_ref_alt(name)
    if parsed is None:
        # skip if can't determine alt
        continue
    ref_base, alt_base = parsed
    center = L // 2
    if ref_seq[center] != ref_base:
        continue
    taken.add((chrom, s, e))
    slots.append(ref_seq)
    n_ref += 1
    # add alt
    alt_seq = ref_seq[:center] + alt_base + ref_seq[center + 1:]
    slots.append(alt_seq)
    n_alt += 1
print(f"HepG2 ref={n_ref} alt={n_alt} (lowest |lfc|={lfc:.3f})")

# K562 22k
remaining = TOTAL - len(slots)
n = 0
for chrom, s, e, lfc, name in k562:
    if n == remaining: break
    if (chrom, s, e) in taken: continue
    seq = get_seq(chrom, s, e)
    if seq is None: continue
    taken.add((chrom, s, e))
    slots.append(seq)
    n += 1
print(f"K562 took {n} (lowest |lfc|={lfc:.3f})")

print(f"total: {len(slots)}")
assert len(slots) == TOTAL

rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote to {OUT}")
