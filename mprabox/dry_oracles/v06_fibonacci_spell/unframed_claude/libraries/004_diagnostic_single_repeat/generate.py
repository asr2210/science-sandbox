"""Diagnostic: one random Gosai sequence repeated 50,000 times.

This tests how prepare.py handles zero variance in the library:
- If r is computed per-sequence with target labels, output will be ~0 / NaN.
- If r is computed over library-level statistics (k-mer dist, etc.), may not collapse.
- Tells us if the metric is per-sequence vs aggregate.
"""
import pandas as pd
import numpy as np

df = pd.read_csv('../../data/gosai_mpra.tsv', sep='\t', low_memory=False)
df = df[df['sequence'].str.len() == 200].reset_index(drop=True)

# Pick one moderately-active sequence
rng = np.random.default_rng(7)
idx = int(rng.integers(0, len(df)))
seq = df['sequence'].iloc[idx].upper()
seq = ''.join(c if c in 'ACGT' else 'A' for c in seq)
print(f"Sequence chosen idx={idx}, activity K562={df['K562_log2FC'].iloc[idx]:.2f} "
      f"HepG2={df['HepG2_log2FC'].iloc[idx]:.2f} SKNSH={df['SKNSH_log2FC'].iloc[idx]:.2f}")

assert len(seq) == 200
with open('sequences_0.txt', 'w') as f:
    for _ in range(50_000):
        f.write(seq + '\n')

print("Wrote 50,000 copies of one sequence")
