"""Real human genomic 200bp tiles sampled from hg38 chr22.

Tests whether biological sequence signal increases the score vs random uniform.
"""
import os
import numpy as np
from Bio import SeqIO

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

N = 50000
L = 200
SEED = 42

# Load chr22
fasta = os.path.join(ROOT, 'data', 'chr22.fa')
record = next(SeqIO.parse(fasta, 'fasta'))
seq = str(record.seq).upper()
print(f"chr22 length: {len(seq):,}")

rng = np.random.default_rng(SEED)
seqs = []
attempts = 0
max_attempts = N * 20
while len(seqs) < N and attempts < max_attempts:
    attempts += 1
    start = rng.integers(0, len(seq) - L + 1)
    window = seq[start:start + L]
    # Reject any window with non-ACGT (N or other)
    if all(c in 'ACGT' for c in window):
        seqs.append(window)

print(f"Collected {len(seqs)} valid 200bp tiles (attempts={attempts})")
assert len(seqs) == N

out_path = os.path.join(HERE, 'sequences_0.txt')
with open(out_path, 'w') as f:
    f.write('\n'.join(seqs) + '\n')
print(f"Wrote {N} sequences to {out_path}")
