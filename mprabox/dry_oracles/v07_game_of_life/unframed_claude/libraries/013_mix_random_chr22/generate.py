"""50% random uniform + 50% chr22 random 200bp tiles.

Tests how a partial biological contamination interacts with random uniform.
If the score is the average of (001 random uniform=0.398) and (002 chr22=0.393),
we'd expect ~0.395. If random uniform's win is *robust* to mixing, ~0.397.
If the bio component drags disproportionately, ~0.390.
"""
import os
import numpy as np
from Bio import SeqIO

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

N = 50000
L = 200
N_HALF = N // 2
SEED = 42

rng = np.random.default_rng(SEED)
bases = np.array(['A', 'C', 'G', 'T'])

# Random uniform half
arr = rng.integers(0, 4, size=(N_HALF, L))
random_seqs = [''.join(bases[row].tolist()) for row in arr]
print(f"Generated {len(random_seqs)} random uniform sequences")

# chr22 tiles half (replicate exp 002 strategy with disjoint sampling)
fasta = os.path.join(ROOT, 'data', 'chr22.fa')
record = next(SeqIO.parse(fasta, 'fasta'))
chr22 = str(record.seq).upper()
print(f"chr22 length: {len(chr22):,}")

chr_seqs = []
attempts = 0
while len(chr_seqs) < N_HALF and attempts < N_HALF * 20:
    attempts += 1
    start = rng.integers(0, len(chr22) - L + 1)
    window = chr22[start:start + L]
    if all(c in 'ACGT' for c in window):
        chr_seqs.append(window)
print(f"Collected {len(chr_seqs)} chr22 tiles")

assert len(random_seqs) == N_HALF
assert len(chr_seqs) == N_HALF

# Concatenate then shuffle
all_seqs = random_seqs + chr_seqs
order = rng.permutation(N)
shuffled = [all_seqs[i] for i in order]

out_path = os.path.join(HERE, 'sequences_0.txt')
with open(out_path, 'w') as f:
    f.write('\n'.join(shuffled) + '\n')
print(f"Wrote {N} sequences to {out_path}")
