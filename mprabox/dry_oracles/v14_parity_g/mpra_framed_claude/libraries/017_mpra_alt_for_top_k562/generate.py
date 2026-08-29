"""Experiment 017: K562 ref + alt for top |lfc| K562 sequences.

Builds on 015 (K22/H3-strict/S25, mean_r=0.0045). Test whether adding
ALT-allele paired sequences for the strongest K562 elements provides
additional learnable signal (paired contrast for high-activity).

009 tested ref+alt on RANDOM-activity variants and it didn't help
(diversity halved). 017 tests it for strict high-activity K562 only.

Allocation (50,000 lines total):
- K562 17k ref (top by |lfc|) + 5k alt for top 5k K562 = 22 K562 slots
- HepG2 3k ultra-strict (|lfc|≥~3.76)
- SKNSH 25k (all available)

Total unique sequences = 50,000 (since alts differ from refs by 1 bp).
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

K562_REF_N = 17_000
K562_ALT_N = 5_000  # top K562_ALT_N by |lfc| get alt-allele
HEPG2_N    = 3_000
SKNSH_N    = 25_000

rng = np.random.default_rng(SEED)
fa = Fasta(FA, sequence_always_upper=True)


def load_bed_sorted(path):
    """Return list of (chrom, s, e, abs_lfc, name) sorted by abs_lfc desc.
    Dedup by coordinate, exclude chr7/chr13 etc."""
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


def parse_name_ref_alt(name):
    """e.g. '1:14677:G:A:R:wC' -> ('G', 'A'). None on parse error."""
    parts = name.split(":")
    if len(parts) < 4:
        return None
    ref, alt = parts[2], parts[3]
    if len(ref) != 1 or len(alt) != 1:
        return None
    return ref.upper(), alt.upper()


# Pre-load all BEDs
print("loading BEDs...")
sknsh = load_bed_sorted(SKNSH_BED)
hepg2 = load_bed_sorted(HEPG2_BED)
k562  = load_bed_sorted(K562_BED)
print(f"SKNSH={len(sknsh)}, HepG2={len(hepg2)}, K562={len(k562)}")

# Process SKNSH first, then HepG2, then K562 (most flexibility)
all_seqs = []
taken_coords = set()

# SKNSH
n = 0
for chrom, s, e, lfc, name in sknsh:
    if (chrom, s, e) in taken_coords:
        continue
    seq = get_seq(chrom, s, e)
    if seq is None:
        continue
    taken_coords.add((chrom, s, e))
    all_seqs.append(seq)
    n += 1
    if n == SKNSH_N:
        break
print(f"SKNSH took {n} (lowest |lfc| ~ {lfc:.3f})")

# HepG2 ultra-strict
n = 0
for chrom, s, e, lfc, name in hepg2:
    if (chrom, s, e) in taken_coords:
        continue
    seq = get_seq(chrom, s, e)
    if seq is None:
        continue
    taken_coords.add((chrom, s, e))
    all_seqs.append(seq)
    n += 1
    if n == HEPG2_N:
        break
print(f"HepG2 took {n} (lowest |lfc| ~ {lfc:.3f})")

# K562: ref + alt for top, then ref only for next
k562_ref_taken = 0
k562_alt_taken = 0
i = 0
while k562_ref_taken < K562_REF_N and i < len(k562):
    chrom, s, e, lfc, name = k562[i]
    i += 1
    if (chrom, s, e) in taken_coords:
        continue
    ref_seq = get_seq(chrom, s, e)
    if ref_seq is None:
        continue
    parsed = parse_name_ref_alt(name)
    if parsed is None:
        # Fall through — still keep ref but no alt
        taken_coords.add((chrom, s, e))
        all_seqs.append(ref_seq)
        k562_ref_taken += 1
        continue
    ref_base, alt_base = parsed
    center = L // 2
    if ref_seq[center] != ref_base:
        # genome doesn't match expected ref — skip
        continue
    taken_coords.add((chrom, s, e))
    all_seqs.append(ref_seq)
    k562_ref_taken += 1
    if k562_alt_taken < K562_ALT_N:
        alt_seq = ref_seq[:center] + alt_base + ref_seq[center + 1:]
        all_seqs.append(alt_seq)
        k562_alt_taken += 1

print(f"K562 ref took {k562_ref_taken}, alt {k562_alt_taken}")
print(f"total: {len(all_seqs)}")
assert len(all_seqs) == 50_000

rng.shuffle(all_seqs)
with open(OUT, "w") as f:
    f.write("\n".join(all_seqs) + "\n")
print(f"wrote to {OUT}")
