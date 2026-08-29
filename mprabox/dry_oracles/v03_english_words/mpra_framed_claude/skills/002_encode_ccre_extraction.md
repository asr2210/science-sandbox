# Skill: Extracting ENCODE cCRE sequences from hg38

## What this gives you
Real genomic 200bp sequences centered on candidate cis-regulatory elements
from the ENCODE Registry V4 — usable as a "biology-rich" MPRA training library
or as part of a mixed-composition library.

## Files needed (downloaded once to `data/`)
- `data/hg38.fa` (3.1 GB unzipped) — UCSC golden-path hg38 reference.
  - Source: `https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`
- `data/GRCh38-cCREs.V4.bed` (124 MB, ~2.35M elements) — ENCODE Registry V4.
  - Source: `https://downloads.wenglab.org/Registry-V4/GRCh38-cCREs.bed`

## Element type counts in V4
- dELS (distal enhancer-like): 1,469,205
- pELS (proximal enhancer-like): 249,464
- PLS (promoter-like): 47,532
- TF (TF binding only): 105,286
- CA-CTCF: 126,034
- CA-H3K4me3: 79,246
- CA (chromatin accessible): 245,985
- CA-TF: 26,102

## Recipe (200bp windows, autosomes + X/Y, no N-heavy windows)
```python
from pyfaidx import Fasta
import numpy as np

fa = Fasta('data/hg38.fa', as_raw=True, sequence_always_upper=True)

# Read BED, filter to standard chromosomes
records = []  # (chrom, start, end, etype)
with open('data/GRCh38-cCREs.V4.bed') as fh:
    for line in fh:
        chrom, start, end, _, _, etype = line.rstrip().split('\t')[:6]
        if chrom in CHROMS_OK:  # {"chr1"..."chr22","chrX","chrY"}
            records.append((chrom, int(start), int(end), etype))

# For each chosen cCRE, take 200bp centered on midpoint
mid = (start + end) // 2
seq = str(fa[chrom][mid-100 : mid+100]).upper()
# Skip if >5 Ns; otherwise replace N with random ACGT
```

## Gotchas
- hg38.fa has soft-masked lowercase for repeats. Use `sequence_always_upper=True`.
- ~455 "chromosomes" in hg38.fa (alt contigs). Filter to chr1-22, chrX, chrY.
- pyfaidx auto-builds a `.fai` index on first read (~30s); persists across runs.
- Extraction of 50K windows takes ~5s after index is built.

## What this teaches the model (per exp 003)
- LIFT to SK-N-SH r (0.045 → 0.079, roughly doubled).
- DROP to K562/HepG2 r (~0.04-0.07).
- Net eval_01 drop ~0.025 vs uniform random.
- Conclusion: real CREs are not a strict improvement on random — they are a *different* lever.
