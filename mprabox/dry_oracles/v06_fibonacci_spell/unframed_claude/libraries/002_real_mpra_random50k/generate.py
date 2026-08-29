"""Sample 50,000 random 200bp sequences from the Gosai et al. 2023 lentiMPRA dataset.

Hypothesis: prepare.py's scoring is tied to this dataset (cell lines K562/HepG2/SKNSH,
200bp length match). Real regulatory sequences should score much higher than random.
"""
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
df = pd.read_csv('../../data/gosai_mpra.tsv', sep='\t', low_memory=False)
df = df[df['sequence'].str.len() == 200].reset_index(drop=True)
print(f"Available 200bp sequences: {len(df)}")

idx = rng.choice(len(df), size=50_000, replace=False)
seqs = df['sequence'].iloc[idx].str.upper().tolist()

# Sanity: only ACGT
bad = [s for s in seqs[:1000] if set(s) - set('ACGT')]
if bad:
    print(f"WARN: {len(bad)} of first 1000 contain non-ACGT, replacing N with A")

with open('sequences_0.txt', 'w') as f:
    for s in seqs:
        s = s.upper()
        # Replace any N with A as a safe fallback
        s = ''.join(c if c in 'ACGT' else 'A' for c in s)
        assert len(s) == 200
        f.write(s + '\n')

print("Wrote 50,000 200bp sequences from Gosai MPRA dataset")
