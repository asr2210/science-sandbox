# Skill: useful genomic data sources

Reference of URLs and quick-load notes for data I've pulled into `data/`.

## Already downloaded
- `data/hg38.fa.gz` (939 MB) — UCSC full GRCh38 fasta
  - source: https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
- `data/hg38.fa` (3.1 GB, gitignored) — gunzipped
- `data/hg38_cache.pkl` (~3 GB, gitignored) — fast-load cache, see
  `skills/load_hg38.md`.
- `data/chr22.fa.gz` (12 MB) and `data/chr22.fa` (51 MB, gitignored).
- `data/GRCh38-cCREs.bed` (~50 MB) — ENCODE SCREEN registry V3 cCREs,
  1,063,878 entries. Columns: chrom, start, end, accession,
  cre_accession, type. Types: dELS, dELS+CTCF, pELS, pELS+CTCF,
  CTCF-only, PLS, PLS+CTCF, DNase-H3K4me3, DNase-H3K4me3+CTCF.
  - source: https://downloads.wenglab.org/Registry-V3/GRCh38-cCREs.bed
  - chr22 only has 21,578 of these — not enough for a 50K library
    without resampling.

## Useful but not yet downloaded
- ENCODE rDHSs (~3.5M DNase-hypersensitive sites): bigger / finer than
  cCREs. https://downloads.wenglab.org/Registry-V4/GRCh38-rDHSs.bed
- JASPAR 2024 CORE PFM database (PFM matrices for ~800 TFs).
  https://jaspar.genereg.net/download/data/2024/CORE/JASPAR2024_CORE_non-redundant_pfms_meme.txt
- ENCODE TF ChIP-seq peaks per cell type: per-TF BED files at
  https://www.encodeproject.org/. Useful for cell-type-specific motif
  enrichment.
- HOCOMOCO v12 (similar to JASPAR, often better coverage of human TFs).
- HepG2/K562/SK-N-SH-specific MPRA training datasets at GEO (e.g.,
  Sharpr-MPRA, lentiMPRA Agarwal et al.). Use sparingly — these may
  overlap with the eval sets.

## Quick recipe — sample N windows centered on a bed file's elements

```python
import pickle, numpy as np
with open("data/hg38_cache.pkl", "rb") as f:
    cache = pickle.load(f)
mids = []  # populate from BED midpoints, filtered by chroms in cache
# ... sample N indices, center 200bp window, skip N-containing windows ...
```
