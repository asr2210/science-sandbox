"""Experiment 021: K562 from TSV with padj filter.

K562 BED |lfc| ranking may include statistically noisy entries. The
K562 TSV (ENCFF141ZOX.tsv) has padj — take top 22k K562 sequences
where padj<0.05 AND allele=ref AND window=center, ranked by |lfc|.

Keep 015 allocation pattern otherwise:
  SKNSH 25k (BED, all available) — processed first
  HepG2  3k ultra-strict (BED) — second
  K562  22k TSV padj<0.05 — fill remainder

Tests whether statistical significance adds value beyond magnitude
for K562 selection.
"""
import os
import numpy as np
from pyfaidx import Fasta

SEED = 42
L = 200

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FA = os.path.join(ROOT, "data", "hg38.fa")
K562_TSV  = os.path.join(ROOT, "data", "ENCFF141ZOX.tsv")
HEPG2_BED = os.path.join(ROOT, "data", "ENCFF887WCC.bed")
SKNSH_BED = os.path.join(ROOT, "data", "ENCFF861MOC.bed")
OUT = os.path.join(os.path.dirname(__file__), "sequences_0.txt")
EXCLUDE_CHR = {"chr7", "chr13"}

SKNSH_N = 25_000
HEPG2_N = 3_000
K562_N  = 22_000
TOTAL = 50_000
PADJ_MAX = 0.05

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


def load_k562_tsv_sorted(path):
    """ref allele, center window, padj<0.05, dedup by (chrom,window-start).
    Returns sorted by |log2FoldChange| desc."""
    entries = []
    seen = set()
    with open(path) as f:
        header = f.readline().rstrip().split("\t")
        idx = {h: i for i, h in enumerate(header)}
        for line in f:
            cols = line.rstrip().split("\t")
            if cols[idx["allele"]] != "ref":
                continue
            if cols[idx["window"]] != "center":
                continue
            try:
                padj = float(cols[idx["padj"]])
                lfc = float(cols[idx["log2FoldChange"]])
            except (ValueError, IndexError):
                continue
            if not (padj < PADJ_MAX):
                continue
            chrom_raw = cols[idx["chr"]]
            chrom = chrom_raw if chrom_raw.startswith("chr") else "chr" + chrom_raw
            if chrom in EXCLUDE_CHR or "_" in chrom or chrom == "chrM":
                continue
            pos = int(cols[idx["pos"]])
            # 200bp centered on pos
            s = pos - L // 2
            e = s + L
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


print("loading SKNSH BED...")
sknsh = load_bed_sorted(SKNSH_BED)
print(f"SKNSH unique: {len(sknsh)}")

print("loading HepG2 BED...")
hepg2 = load_bed_sorted(HEPG2_BED)
print(f"HepG2 unique: {len(hepg2)}")

print("loading K562 TSV (allele=ref, window=center, padj<0.05)...")
k562 = load_k562_tsv_sorted(K562_TSV)
print(f"K562 TSV padj<0.05 ref center: {len(k562)}")


slots = []
taken = set()


def take(sorted_pool, quota, label):
    global taken, slots
    k = 0
    last_lfc = None
    remaining_global = TOTAL - len(slots)
    eff_quota = min(quota, remaining_global)
    for chrom, s, e, lfc in sorted_pool:
        if (chrom, s, e) in taken:
            continue
        seq = get_seq(chrom, s, e)
        if seq is None:
            continue
        taken.add((chrom, s, e))
        slots.append(seq)
        k += 1
        last_lfc = lfc
        if k == eff_quota:
            break
    print(f"{label}: took {k} (last |lfc|={last_lfc:.3f})")
    return k


take(sknsh, SKNSH_N, "SKNSH")
take(hepg2, HEPG2_N, "HepG2")
take(k562,  K562_N,  "K562")

# If anything short, fill rest from K562 by lfc (regardless of padj)
if len(slots) < TOTAL:
    fill = TOTAL - len(slots)
    print(f"short by {fill}; filling from K562 TSV pool")
    # already exhausted padj<0.05 dedup; pad with HepG2 then SKNSH leftovers
    take(hepg2, fill, "HepG2 leftover")
    if len(slots) < TOTAL:
        fill = TOTAL - len(slots)
        take(sknsh, fill, "SKNSH leftover")

print(f"total: {len(slots)}")
assert len(slots) == TOTAL, f"only got {len(slots)}"

rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote to {OUT}")
