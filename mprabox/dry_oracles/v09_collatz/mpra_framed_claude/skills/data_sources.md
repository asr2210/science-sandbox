# Data sources for MPRA library design

## hg38 reference genome
- File: `data/hg38.fa` (3.1 GB unzipped) + `data/hg38.fa.fai` (index)
- Downloaded from `https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`
- Use `pyfaidx.Fasta(path, as_raw=True, sequence_always_upper=True)` for fast indexed access
- **Gotcha:** if you index while file is still being written, the index will be incomplete and silent failures (missing chromosomes) result. Always wait for download/gunzip to finish, then delete any stale `.fai` and re-index.
- Main chromosomes: `chr1..chr22, chrX, chrY, chrM`. Other contigs have `_random` / alt names — usually exclude.

## ENCODE V3 cCREs (candidate cis-regulatory elements)
- File: `data/GRCh38-cCREs.bed` (61 MB)
- Source: `https://downloads.wenglab.org/V3/GRCh38-cCREs.bed`
- 1,063,878 elements total, defined across hundreds of cell types
- Columns: `chrom start end EH38D_id EH38E_id classes`
- Class distribution (from `cut -f6 | sort | uniq -c`):
  ```
  510920 dELS                     (distal enhancer-like, 48%)
  278280 dELS,CTCF-bound          (26%)
   96781 pELS,CTCF-bound          (9%)
   75246 pELS                     (proximal enhancer-like, 7%)
   35839 CTCF-only,CTCF-bound     (3.4%)
   31447 PLS,CTCF-bound           (3%)
   17627 DNase-H3K4me3            (1.7%)
    9444 PLS                      (promoter-like, 0.9%)
    8294 DNase-H3K4me3,CTCF-bound (0.8%)
  ```
- Element widths typically 150–500bp. For 200bp library, center 200bp window on midpoint of cCRE coordinates.

## ENCODE SCREEN per-cell-type cCRE annotations
- API for activity-by-cell-type: `https://api.wenglab.org/screen_v13/dataws/...`
- Z-scores per cell type available; can filter cCREs active in K562, HepG2, SK-N-SH, or any other cell type.
- Per-cell-type DHS narrowPeak files from ENCODE Portal also work for tissue-specific sampling.

## ENCODE Portal
- Search at `https://www.encodeproject.org`
- File listings via `https://www.encodeproject.org/search/?type=File&...`
- Useful for cell-type-specific DNase/ATAC/ChIP-seq peaks.
