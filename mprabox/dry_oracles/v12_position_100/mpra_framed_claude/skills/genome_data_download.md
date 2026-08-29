# Genome and regulatory data: where to get it

## hg38 genome
- URL: `https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`
- Size: 938MB compressed, 3.3GB uncompressed
- ~60 sec to download on this machine, ~1 min to gunzip
- Save to `data/hg38.fa.gz` and gunzip in place

## ENCODE Registry V4 cCREs (candidate cis-regulatory elements)
- URL: `https://downloads.wenglab.org/Registry-V4/GRCh38-cCREs.bed`
- Size: 129MB, 2.35M elements
- BED columns: chrom, start, end, accession_D, accession_E, class
- Classes & counts:
  - dELS (distal enhancer-like): 1.47M
  - pELS (proximal enhancer-like): 249K
  - CA (chromatin accessible only): 246K
  - CA-CTCF: 126K
  - TF: 105K
  - CA-H3K4me3: 79K
  - PLS (promoter-like): 47K
  - CA-TF: 26K
- Lengths: median 273bp, range 150-350bp → easy to extract 200bp windows
  centered on each.

## Loading with pyfaidx
```python
from pyfaidx import Fasta
fa = Fasta("data/hg38.fa", as_raw=True)
seq = str(fa["chr1"][100000:100200]).upper()
```
- `as_raw=True` returns plain strings (faster than Sequence objects).
- pyfaidx builds a `.fai` index on first load (~10s for hg38). Subsequent
  loads are instant.

## UCSC REST API (for small/targeted fetches)
- `https://api.genome.ucsc.edu/getData/sequence?genome=hg38;chrom=chr22;start=20000000;end=20000200`
- Returns JSON with `dna` field. Good for one-off fetches but not bulk
  (rate limits unclear). For 50K sequences, use local FASTA instead.

## Performance tips
- Pre-build `.fai` index by accessing chromosome once at start
- Cache `contig_lens = {c: len(fa[c]) for c in chroms}` to avoid repeated
  length queries
- Reject N-containing windows AFTER fetch (uppercase + set check)
- Random autosomal background: most windows are clean; ~1-in-25 contains
  N (in repeats), so loop with retries

## What this is good for
- Exp 003: cCRE sampling beat random by +22% on eval_01.
- Use cCRE BED to make any "regulatory-enriched" library
- Use random autosomal background as a non-regulatory "null" class
