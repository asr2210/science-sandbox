# Skill: Random sampling of 200bp windows from hg38

## Setup
- Reference: `data/hg38.fa` (3.1 GB unzipped, downloaded from `https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`).
- pyfaidx (`from pyfaidx import Fasta`) loads it lazily once an `.fai` index is built (auto-built on first `Fasta()` call). Indexing takes ~30s the first time.
- Autosome list: `[f"chr{i}" for i in range(1, 23)]`. Total ~2.88 Gb.
- `chr1 length = 248,956,422`. `chr22 length = 50,818,468`.

## Sampling pattern
```python
from pyfaidx import Fasta
import numpy as np

fa = Fasta("data/hg38.fa")
autosomes = [f"chr{i}" for i in range(1, 23)]
chrom_lens = {c: len(fa[c]) for c in autosomes}
total = sum(chrom_lens.values())
weights = np.array([chrom_lens[c] / total for c in autosomes])

rng = np.random.default_rng(0)
n_seqs = 50_000
seq_len = 200

# Sample (chrom, start) pairs proportional to chromosome length.
seqs = []
while len(seqs) < n_seqs:
    chrom = rng.choice(autosomes, p=weights)
    L = chrom_lens[chrom]
    start = rng.integers(0, L - seq_len)
    s = str(fa[chrom][start:start + seq_len]).upper()
    if "N" not in s:
        seqs.append(s)
```

Caveats:
- Random genomic windows ARE mostly non-regulatory (≈98% of genome is non-coding, and most non-coding is not regulatory).
- N rejection rate is low for autosomes once you skip centromeres — typically <2%.
- Sequences are mixed-case in the fasta (lowercase = repeat-masked from `softmask` indication). Always `.upper()` to normalize.
- `pyfaidx` is 1-based-inclusive in the slice syntax `fa[c][a:b]` — actually it's 0-based python slicing. Test before relying on offsets.

## Performance
- 50,000 sequences take ~20 s to sample using single-pos pyfaidx lookups. If you need faster, do batch chromosome reads.

## Variants
- For regulatory-region-enriched sampling, restrict starts to fall within an ENCODE cCRE BED file.
- For accessibility-weighted sampling, use DNase peaks or ATAC peaks instead.
- For "centered-on-motif" sampling, find motif hits genome-wide and take 200bp windows centered on them.
