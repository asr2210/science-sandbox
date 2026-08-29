"""Experiment 7: 50K natural genomic 200bp windows from hg38 chr1 + chr22.

Sample random 200bp windows containing only ACGT (no N).
Hypothesis: real genome carries multi-feature variance that MPRA-trained
models both recognize, raising r above the GC-only ceiling.
"""

import numpy as np
from pathlib import Path
import re

rng = np.random.default_rng(seed=7)
N, L = 50000, 200

DATA = Path(__file__).resolve().parents[2] / "data"

def load_fa(path):
    """Read single-chromosome FASTA (header + body) into uppercase string."""
    with open(path) as f:
        lines = f.read().splitlines()
    body = "".join(line for line in lines if not line.startswith(">")).upper()
    return body


chr1 = load_fa(DATA / "chr1.fa")
chr22 = load_fa(DATA / "chr22.fa")
print(f"chr1: {len(chr1):,} bp,  chr22: {len(chr22):,} bp")

chroms = [chr1, chr22]
chrom_names = ["chr1", "chr22"]
chrom_lens = np.array([len(c) for c in chroms])
weights = chrom_lens / chrom_lens.sum()

valid = re.compile(r"^[ACGT]+$")
out_seqs = []
attempts = 0
while len(out_seqs) < N:
    ci = int(rng.choice(len(chroms), p=weights))
    seq = chroms[ci]
    pos = int(rng.integers(0, chrom_lens[ci] - L))
    window = seq[pos:pos + L]
    attempts += 1
    if valid.match(window):
        out_seqs.append(window)
    if attempts % 200000 == 0:
        print(f"  {len(out_seqs)}/{N} accepted ({attempts} attempts)")

out_path = Path(__file__).parent / "sequences_0.txt"
out_path.write_text("\n".join(out_seqs) + "\n")
print(f"Wrote {len(out_seqs)} natural sequences. Acceptance rate: {len(out_seqs)/attempts:.2%}")

# Stats
A, C, G, T = ord('A'), ord('C'), ord('G'), ord('T')
arr = np.array([[ord(b) for b in s] for s in out_seqs[:5000]], dtype=np.int8)
gc = ((arr == C) | (arr == G)).mean(axis=1)
print(f"GC% (first 5k): mean={gc.mean():.3f}, std={gc.std():.3f}")
