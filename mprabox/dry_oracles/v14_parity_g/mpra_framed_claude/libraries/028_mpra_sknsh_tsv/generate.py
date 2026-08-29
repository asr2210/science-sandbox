"""Experiment 028: SKNSH from TSV padj<0.05 (replace BED).

BED SKNSH (015) has 25k entries down to |lfc|≥0.006 — very noisy at
the bottom. Experiments 024, 026 showed SKNSH at 22k (top BED) is
BETTER than 25k — bottom 3k BED entries are noise.

Try TSV-based SKNSH: ref allele, window=center, padj<0.05 → 39,696
entries. Top 25k @ |lfc|≥0.97 — much higher signal density.

Layout (50k):
  K562 22k BED strict (|lfc|≥1.69)
  HepG2  3k BED strict (|lfc|≥3.76)
  SKNSH 25k TSV padj<0.05 top by |lfc|

Hypothesis: removing noisy SKNSH BED entries by switching to TSV-padj
ranking will boost SKNSH r past 0.0066.
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
SKNSH_TSV = os.path.join(ROOT, "data", "ENCFF521IVN.tsv")
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


def load_tsv_padj_sorted(path):
    entries = []
    seen = set()
    with open(path) as f:
        header = f.readline().rstrip().split("\t")
        idx = {h: i for i, h in enumerate(header)}
        for line in f:
            cols = line.rstrip().split("\t")
            if cols[idx["allele"]] != "ref" or cols[idx["window"]] != "center":
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


print("loading BEDs and SKNSH TSV...")
sknsh = load_tsv_padj_sorted(SKNSH_TSV)
hepg2 = load_bed_sorted(HEPG2_BED)
k562  = load_bed_sorted(K562_BED)
print(f"SKNSH TSV padj<0.05: {len(sknsh)}, HepG2={len(hepg2)}, K562={len(k562)}")


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


# Order: HepG2 first (strictest), then K562, then SKNSH last (TSV may
# overlap with BEDs since variant pool is shared across Tewhey cells)
take(hepg2, HEPG2_N, "HepG2")
take(k562,  K562_N,  "K562")
remaining = TOTAL - len(slots)
take(sknsh, remaining, "SKNSH")

assert len(slots) == TOTAL
rng.shuffle(slots)
with open(OUT, "w") as f:
    f.write("\n".join(slots) + "\n")
print(f"wrote {OUT}")
