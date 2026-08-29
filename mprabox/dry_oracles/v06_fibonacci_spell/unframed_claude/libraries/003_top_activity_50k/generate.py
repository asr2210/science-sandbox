"""Top 50,000 most-active 200bp sequences from Gosai dataset, ranked by
max(|K562|, |HepG2|, |SKNSH|) log2FC.

Hypothesis: scoring rewards strong-signal sequences; selecting tails will improve
correlation r, especially in K562 which had the biggest jump from random→real.
"""
import pandas as pd
import numpy as np

df = pd.read_csv('../../data/gosai_mpra.tsv', sep='\t', low_memory=False)
df = df[df['sequence'].str.len() == 200].reset_index(drop=True)
print(f"Available 200bp sequences: {len(df)}")

df['max_abs'] = df[['K562_log2FC','HepG2_log2FC','SKNSH_log2FC']].abs().max(axis=1)
top = df.nlargest(50_000, 'max_abs')
print(f"Top-50k max_abs range: [{top['max_abs'].min():.3f}, {top['max_abs'].max():.3f}]")
print(top[['K562_log2FC','HepG2_log2FC','SKNSH_log2FC']].describe())

with open('sequences_0.txt', 'w') as f:
    for s in top['sequence']:
        s = ''.join(c if c in 'ACGT' else 'A' for c in s.upper())
        assert len(s) == 200
        f.write(s + '\n')

print("Wrote 50,000 top-activity 200bp sequences")
