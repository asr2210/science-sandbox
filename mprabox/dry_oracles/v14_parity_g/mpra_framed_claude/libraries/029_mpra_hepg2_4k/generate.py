"""Experiment 029: HepG2 expanded to 4k (smallest possible expansion).

015 has H3 strict @ |lfc|≥3.76 → HepG2 r=0.0044.
024 had H6 @ |lfc|≥2.83 → HepG2 r=0.0027 (dilution hurts).

Test the *smallest* expansion: H4 @ |lfc|≥3.45 (just +1k unique HepG2
in the next-tier range 3.45-3.76). Sacrifices 1k SKNSH (lowest |lfc|).

Layout (50k):
  K562 22k strict (preserved floor)
  HepG2  4k (|lfc|≥3.45)
  SKNSH 24k

Tests fine-grained HepG2 sweet-spot. If H4 outperforms H3, future
work could explore H3.5 or H4.5. If H4 hurts (like H6), then H3 is
the strict cliff.
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

SKNSH_N = 24_000
HEPG2_N = 4_000
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
    k = 0; last = None
    for chrom, s, e, lfc in pool:
        if (chrom, s, e) in taken: continue
        seq = get_seq(chrom, s, e)
        if seq is None: continue
        taken.add((chrom, s, e))
        slots.append(seq)
        k += 1; last = lfc
        if k == n: break
    print(f"{label}: took {k} (last |lfc|={last:.3f})")


take(sknsh, SKNSH_N, "SKNSH")
take(hepg2, HEPG2_N, "HepG2")
remaining = TOTAL - len(slots)
take(k562,  remaining, "K562")

assert len(slots) == TOTAL
rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote {OUT}")
