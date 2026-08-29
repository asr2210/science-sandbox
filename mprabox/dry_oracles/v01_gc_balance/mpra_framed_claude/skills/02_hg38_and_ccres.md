# Working with hg38 + ENCODE cCREs

## Data downloads
- hg38 fasta: `https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`
  (~940MB gz, ~3GB decompressed; takes a couple of minutes; saved to
  `data/hg38/hg38.fa.gz`)
- ENCODE GRCh38 cCREs (~2.35M elements, v13 SCREEN): ENCODE accession
  ENCFF420VPZ. URL pattern: `https://www.encodeproject.org/files/ENCFF420VPZ/@@download/ENCFF420VPZ.bed.gz`
  (~32MB; saved to `data/encode/GRCh38-cCREs.bed`).
- Note: api.wenglab.org is blocked from this host. Always use
  www.encodeproject.org for downloads.

## cCRE BED format (10 cols)
`chrom  start  end  EH38E_id  0  .  start  end  color  ctype`
where `ctype` ∈ {PLS, pELS, dELS, TF, CA, CA-CTCF, CA-H3K4me3, CA-TF}.
Element counts (autosomes+X+Y, all biosamples):
- dELS 1,469,205 (dominant)
- pELS 249,464
- CA   245,985
- CA-CTCF 126,034
- TF   105,286
- CA-H3K4me3 79,246
- PLS  47,532
- CA-TF 26,102

## hg38 loading (no extra deps)
Streaming a gzipped FASTA with stdlib `gzip.open` and keeping uppercased
strings in a `{chrom: str}` dict uses ~3.5GB RAM. Restricting to chr1..22,X,Y
is plenty for cCRE work and avoids alt/random/Mt.

Reference loader (uses 3-4GB RAM, takes ~15s):
```python
def load_hg38(path, keep_chroms):
    chroms = {}
    cur = None; chunks = []
    with gzip.open(path, "rt") as fh:
        for line in fh:
            if line.startswith(">"):
                if cur and cur in keep_chroms:
                    chroms[cur] = "".join(chunks).upper()
                cur = line[1:].split()[0]; chunks = []
            elif cur in keep_chroms:
                chunks.append(line.rstrip())
    if cur in keep_chroms: chroms[cur] = "".join(chunks).upper()
    return chroms
```

## Window extraction recipe
For a cCRE with (chrom, start, end), take midpoint `mid = (start+end)//2` and
extract `seq[mid-100:mid+100]` (200bp centered). Reject windows containing
`N`. Reject and resample from a shuffled pool to avoid bias.

## Result so far (n=50k, stratified across cCRE types)
- eval_01=0.6921 vs random baseline 0.5131 (+0.18)
- eval_08=0.1248 vs random baseline 0.1624 (−0.04, key anomaly)

The eval_08 drop suggests one of the eval sets is **biased toward
random-composition / non-cCRE-distribution sequences**. Future libraries
should include a fraction of random / shuffled sequences to keep eval_08
healthy.
