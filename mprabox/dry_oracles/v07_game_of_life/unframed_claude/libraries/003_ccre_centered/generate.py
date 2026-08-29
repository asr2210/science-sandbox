"""ENCODE cCRE-centered 200bp windows.

Pull 50k random rows from the ENCODE candidate cis-regulatory elements bed file,
extend the center of each region to a 200bp window, and emit those windows.
Tests whether real curated regulatory elements outperform random.
"""
import os
import sys
import numpy as np
from pyfaidx import Fasta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

N = 50000
L = 200
SEED = 42

bed = os.path.join(ROOT, 'data', 'encode_ccres_hg38.bed')

# Use the per-chromosome fasta files already present in the autoresearch cache
# These have .fai indexes alongside.
CHROM_DIR = '/data/users/arao/mpra_autoresearch/data'

# Read BED, then sample
print("Loading BED...")
records = []
with open(bed) as f:
    for line in f:
        parts = line.rstrip('\n').split('\t')
        chrom, start, end = parts[0], int(parts[1]), int(parts[2])
        records.append((chrom, start, end))
print(f"Loaded {len(records):,} cCREs")

rng = np.random.default_rng(SEED)
# Sample more than needed (some will fail due to N), then trim
idxs = rng.choice(len(records), size=N * 2, replace=False)

# Open all chromosomes lazily via pyfaidx
fastas = {}

def get_fasta(chrom):
    if chrom not in fastas:
        path = os.path.join(CHROM_DIR, f'{chrom}.fa')
        if not os.path.exists(path):
            return None
        fastas[chrom] = Fasta(path, sequence_always_upper=True)
    return fastas[chrom]

seqs = []
for idx in idxs:
    if len(seqs) >= N:
        break
    chrom, start, end = records[idx]
    fa = get_fasta(chrom)
    if fa is None:
        continue
    center = (start + end) // 2
    w_start = center - L // 2
    w_end = w_start + L
    if w_start < 0:
        continue
    rec = fa[chrom]
    if w_end > len(rec):
        continue
    s = str(rec[w_start:w_end]).upper()
    if len(s) != L:
        continue
    if any(c not in 'ACGT' for c in s):
        continue
    seqs.append(s)

print(f"Collected {len(seqs)} valid 200bp windows")
assert len(seqs) == N, f"Got {len(seqs)}; need {N}"

out = os.path.join(HERE, 'sequences_0.txt')
with open(out, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out}")
