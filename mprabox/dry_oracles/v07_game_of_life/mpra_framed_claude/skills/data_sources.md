# Data sources for MPRA library design

## hg38 reference genome
- URL: https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
- Size: ~983MB gzipped, ~3.1GB unzipped
- Stored at `data/hg38.fa` (after gunzip)
- Indexed with `pyfaidx.Fasta` (creates `.fai`)
- Primary chromosomes: chr1-22, chrX, chrY. Skip alt/random/Unk contigs.
- Soft-masked. Uppercase before use. Skip any window containing N.

## ENCODE cCRE registry V4 (GRCh38)
- URL: https://www.encodeproject.org/files/ENCFF286VQG/@@download/ENCFF286VQG.bed.gz
- Size: 32MB gz, ~2.3M elements
- Stored at `data/ccre.bed.gz`
- Columns (BED-like): chrom, start, end, name, _, _, _, _, _, class, _
- Classes:
  - Low-DNase: 2.18M (low-confidence)
  - pELS: 42K (proximal enhancer-like)
  - dELS: 35K (distal enhancer-like)
  - CA-TF: 39K (chromatin accessible + TF binding)
  - CA-CTCF: 28K (CTCF)
  - PLS: 20K (promoter-like)
  - CA-H3K4me3: 5.8K
  - CA-only: 3K
- High-confidence set (PLS+pELS+dELS+CA-TF+CA-CTCF) ≈ 164K elements
- Most cCREs are short (<300bp); 200bp centered window usually covers
  the full element.

## JASPAR 2024 vertebrate motifs
- URL: https://jaspar.elixir.no/download/data/2024/CORE/JASPAR2024_CORE_vertebrates_non-redundant_pfms_jaspar.txt
- Stored at `data/jaspar2024_vertebrates.jaspar`
- 879 non-redundant vertebrate PWMs
- JASPAR format: `>MA0004.1\tArnt`, then 4 rows starting `A [...]` etc.
- Parse with regex `\d+\.?\d*` per row.
- Use pseudocount 0.5 when normalizing PFM→PWM.

## ENCODE blacklist
- URL: https://www.encodeproject.org/files/ENCFF356LFX/@@download/ENCFF356LFX.bed.gz
- Stored at `data/blacklist.bed.gz`
- 910 problematic regions to optionally exclude

## Things I haven't tried (to consider)
- Meuleman et al. 2020 DHS Index: 3.6M elements, 438 biosamples.
  URL: https://www.meuleman.org/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz
- VISTA enhancer browser (~3K validated enhancers)
- FANTOM5 enhancers (~40K CAGE-defined)
- ReMap TF ChIP atlas (huge, ~165 TFs combined)
- 1000 Genomes variants (for natural sequence perturbations)
