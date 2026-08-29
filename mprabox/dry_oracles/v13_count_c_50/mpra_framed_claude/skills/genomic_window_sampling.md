# Genomic window sampling from hg38

Sample N random fixed-length windows from primary chromosomes, weighted
by chromosome length, with N-rejection and optional strand balance.

## Setup
- hg38.fa downloaded from `https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`
- Stored at `data/hg38.fa` (3.3 GB uncompressed) and `.fai` index built lazily by pyfaidx
- 455 contigs in the file. Primary set: `chr1`..`chr22`, `chrX`, `chrY`. Alt/random contigs add noise.

## Implementation
```python
from pyfaidx import Fasta
import numpy as np

fa = Fasta('data/hg38.fa')
CHROMS = [f'chr{i}' for i in range(1, 23)] + ['chrX', 'chrY']
lengths = {c: len(fa[c]) for c in CHROMS}
weights = np.array([lengths[c] for c in CHROMS], dtype=float)
weights /= weights.sum()

rng = np.random.default_rng(SEED)
seqs = []
while len(seqs) < N:
    chrom = CHROMS[rng.choice(len(CHROMS), p=weights)]
    start = rng.integers(0, lengths[chrom] - L)
    s = str(fa[chrom][start:start + L]).upper()
    if 'N' in s:
        continue
    if rng.random() < 0.5:
        s = revcomp(s)
    seqs.append(s)
```

## Performance
- ~5% rejection rate (N-bases / assembly gaps) — budget ~1.05x attempts.
- ~50,000 sequences in ~10 s on this machine.

## Validation
Always assert:
- exactly N lines
- each line exactly L characters
- characters in {A, C, G, T}

## When to use
- Baseline biology library
- Background distribution for shuffling / control
- "Negative" set for regulatory enrichment libraries
