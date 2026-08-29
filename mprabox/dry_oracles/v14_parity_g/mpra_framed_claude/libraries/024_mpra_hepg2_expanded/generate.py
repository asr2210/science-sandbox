"""Experiment 024: HepG2 expanded to 6k UNIQUE.

015 has HepG2 at top 3k (|lfc|≥3.76). 018 dups (H6 = 3k×2) helped
HepG2 r 0.0044→0.0049 (slight). Test if HepG2 wants more UNIQUE
sites at slightly looser |lfc| threshold instead of dups.

Layout (50k):
  SKNSH 22k (down from 25k)
  HepG2 6k unique (|lfc|≥2.83 — top 6k)
  K562 22k (preserved floor)

Hypothesis: more unique HepG2 sites at lower stringency may give
HepG2 r > 0.0049 (best so far), and SKNSH at 22k loses <0.001.
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
HEPG2_N = 6_000
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


def take(pool, n, label):
    global taken, slots
    k = 0
    last = None
    for chrom, s, e, lfc in pool:
        if (chrom, s, e) in taken: continue
        seq = get_seq(chrom, s, e)
        if seq is None: continue
        taken.add((chrom, s, e))
        slots.append(seq)
        k += 1
        last = lfc
        if k == n: break
    print(f"{label}: took {k} (last |lfc|={last:.3f})")


take(sknsh, SKNSH_N, "SKNSH")
take(hepg2, HEPG2_N, "HepG2")
remaining = TOTAL - len(slots)
take(k562,  remaining, "K562")

print(f"total: {len(slots)}")
assert len(slots) == TOTAL

rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote {OUT}")
