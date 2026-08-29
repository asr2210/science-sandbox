"""Experiment 019: broadly-active cross-cell elements.

13,359 BED elements are strong (|lfc|>=1.5) in BOTH K562 and HepG2
(after excluding chr7/13). These are "broadly active" — likely to be
generalizable regulatory regions.

Layout (50k):
- SKNSH 25k (all available)
- HepG2 3k ultra-strict (|lfc|>=~3.76 in HepG2)
- K562 22k: 11k from K562-HepG2 broadly-active pool (sorted by max|lfc|)
            + 11k K562-only strong (top |lfc| in K562 not in broadly-active)

Hypothesis: broadly-active sequences should boost generalization to
unseen cell types (per instructions emphasis). Also should boost
HepG2 signal further (since these are HepG2-strong too).
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

BROADLY_ACTIVE_N = 11_000
K562_ONLY_N = 11_000
HEPG2_N = 3_000
SKNSH_N = 25_000
TOTAL = 50_000

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)


def load_bed_dict(path):
    """Return dict (chrom,s,e) -> abs_lfc."""
    d = {}
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
            if key not in d or abs(lfc) > d[key]:
                d[key] = abs(lfc)
    return d


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
k562_d  = load_bed_dict(K562_BED)
hepg2_d = load_bed_dict(HEPG2_BED)
sknsh_d = load_bed_dict(SKNSH_BED)
print(f"K562={len(k562_d)}, HepG2={len(hepg2_d)}, SKNSH={len(sknsh_d)}")

# Broadly active = K562 |lfc|>=1.5 AND HepG2 |lfc|>=1.5
broadly_active = []
for key in k562_d:
    if k562_d[key] >= 1.5 and key in hepg2_d and hepg2_d[key] >= 1.5:
        # sort key = sum of magnitudes (so most strongly broadly-active first)
        broadly_active.append((key, k562_d[key] + hepg2_d[key]))
broadly_active.sort(key=lambda x: -x[1])
print(f"broadly active (both K562 & HepG2 |lfc|>=1.5): {len(broadly_active)}")

# K562-only top: K562 |lfc| sorted but exclude broadly-active set
broadly_set = {k for k, _ in broadly_active}
k562_only_sorted = sorted(
    [(k, v) for k, v in k562_d.items() if k not in broadly_set],
    key=lambda x: -x[1]
)

# SKNSH and HepG2 strict (sorted by their own |lfc|)
sknsh_sorted = sorted(sknsh_d.items(), key=lambda x: -x[1])
hepg2_sorted = sorted(hepg2_d.items(), key=lambda x: -x[1])


slots = []
taken = set()


def take(sorted_pool, n, label):
    global taken, slots
    k = 0
    last_lfc = None
    for entry in sorted_pool:
        # entry: ((chrom,s,e), lfc) for dict; or ((chrom,s,e), score) for broadly
        if isinstance(entry, tuple) and len(entry) == 2:
            key, score = entry
        else:
            key, score = entry, None
        if key in taken:
            continue
        chrom, s, e = key
        seq = get_seq(chrom, s, e)
        if seq is None:
            continue
        taken.add(key)
        slots.append(seq)
        k += 1
        last_lfc = score
        if k == n:
            break
    print(f"{label}: took {k} (last score={last_lfc:.3f})")
    return k


# Order: SKNSH first (smallest pool), then HepG2 strict, then broadly-active, then K562-only fill
take(sknsh_sorted,    SKNSH_N,         "SKNSH")
take(hepg2_sorted,    HEPG2_N,         "HepG2 strict")
take(broadly_active,  BROADLY_ACTIVE_N,"broadly active K&H")
# fill remainder with K562-only top
remaining = TOTAL - len(slots)
take(k562_only_sorted, remaining,      "K562-only fill")

print(f"total: {len(slots)}")
assert len(slots) == TOTAL

rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote to {OUT}")
