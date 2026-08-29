# Skill: Sequence data sources

## hg38 reference chromosomes
UCSC per-chromosome FASTAs:
`https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/chr{N}.fa.gz`
- chr8: 145Mb, chr19: 58Mb (GC-rich), chr21: 47Mb, chr22: 51Mb, chrX: 156Mb
- chr8+19+21+22+X downloaded under `data/` (gitignored — see .gitignore)

## ENCODE cCREs V3 (SCREEN)
Direct URL (~64MB):
`https://downloads.wenglab.org/V3/GRCh38-cCREs.bed`
- 1,063,878 cCREs genome-wide
- 6-column BED: chrom, start, end, dnase_id, ccre_id, classification
- Classifications: PLS (promoter), pELS (proximal enhancer),
  dELS (distal enhancer), DNase-H3K4me3, CTCF-only, all with CTCF-bound variants
- ~145k in chr8/19/21/22/X subset

## Loading with pyfaidx
```python
from pyfaidx import Fasta
fa = Fasta("data/hg38.chrN.fa", as_raw=True, sequence_always_upper=True)
s = fa["chrN"][start:end]  # returns str
```
`as_raw=True` returns plain strings, `sequence_always_upper=True` handles
soft-masked lowercase.

## Sampling pattern
Always reject windows with non-ACGT bases (mostly N at assembly gaps):
```python
valid = set("ACGT")
if len(s) == L and set(s).issubset(valid):
    keep(s)
```

## Disk footprint observed
Per chromosome ~50–150MB unzipped, ~15–45MB gzipped. Five chromosomes
(chr8, chr19, chr21, chr22, chrX) = ~445MB unzipped.
