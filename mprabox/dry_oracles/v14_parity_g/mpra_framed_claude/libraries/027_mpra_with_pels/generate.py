"""Experiment 027: MPRA core + cross-cell pELS diversity.

015 (K22/H3/S25=50) → mean 0.0045. 026 showed SKNSH at 22k is BETTER
than 25k. So 3k slots are free. Test if filling with cross-cell
ENCODE pELS (proximal enhancer-like signatures) helps generalization,
especially eval_08 (consistently negative).

Layout (50k):
  K562 22k strict (|lfc|≥1.69)
  HepG2  3k strict (|lfc|≥3.76)
  SKNSH 22k strict (|lfc|≥~0.1 — top 22k of 25411)
  cCRE pELS 3k random (cross-cell enhancer grammar)
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
CCRE_BED  = os.path.join(ROOT, "data", "ENCFF420VPZ.bed")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
EXCLUDE_CHR = {"chr7", "chr13"}

SKNSH_N = 22_000
HEPG2_N = 3_000
K562_N  = 22_000
PELS_N  = 3_000
TOTAL   = 50_000

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


def load_ccre_pels(path):
    """ENCODE cCRE combined BED. Filter to pELS class."""
    entries = []
    seen = set()
    with open(path) as f:
        for line in f:
            cols = line.rstrip().split("\t")
            chrom = cols[0]
            if chrom in EXCLUDE_CHR or "_" in chrom or chrom == "chrM":
                continue
            if len(cols) < 10 or cols[9] != "pELS":
                continue
            s, e = int(cols[1]), int(cols[2])
            if e - s != L:
                c = (s + e) // 2
                s = c - L // 2
                e = s + L
            key = (chrom, s, e)
            if key in seen:
                continue
            seen.add(key)
            entries.append((chrom, s, e))
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
pels  = load_ccre_pels(CCRE_BED)
print(f"SKNSH={len(sknsh)}, HepG2={len(hepg2)}, K562={len(k562)}, pELS={len(pels)}")


slots = []
taken = set()


def take(pool, n, label):
    global taken, slots
    k = 0; last = None
    for entry in pool:
        if k == n: break
        if len(entry) == 4:
            chrom, s, e, lfc = entry
        else:
            chrom, s, e = entry; lfc = None
        if (chrom, s, e) in taken: continue
        seq = get_seq(chrom, s, e)
        if seq is None: continue
        taken.add((chrom, s, e))
        slots.append(seq)
        k += 1; last = lfc
    msg = f"{label}: took {k}"
    if last is not None:
        msg += f" (last |lfc|={last:.3f})"
    print(msg)


take(sknsh, SKNSH_N, "SKNSH")
take(hepg2, HEPG2_N, "HepG2")
take(k562,  K562_N,  "K562")
# shuffle pELS for random sample
pels_idx = rng.permutation(len(pels))
pels_shuf = [pels[i] for i in pels_idx]
take(pels_shuf, PELS_N, "pELS")

assert len(slots) == TOTAL, f"got {len(slots)}"
rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote {OUT}")
