# Skill: Loading hg38 FASTA into memory

## When to use
Whenever an experiment needs to extract sequence from genomic coordinates.

## Source
`data/hg38.fa` (3.1GB uncompressed). Downloaded once from
`https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz`.

## Loader (Python, no external deps)
```python
def load_fasta(path):
    chrs = {}
    cur = None
    parts = []
    with open(path) as f:
        for line in f:
            if line.startswith('>'):
                if cur:
                    chrs[cur] = ''.join(parts).upper()
                cur = line[1:].split()[0]  # e.g. 'chr1'
                parts = []
            else:
                parts.append(line.rstrip())
        if cur:
            chrs[cur] = ''.join(parts).upper()
    return chrs
```

Takes ~30s to load and uses ~3GB RAM. Coordinates are 0-based half-open
(BED convention). Sequence is uppercase, with N for unmapped regions.

## Performance tips
- Loading all of hg38 once and keeping in memory is fine for batch sequence
  generation (50K windows is small relative to chromosomes).
- For extracting many windows: iterate the BED, slice the chr string, skip
  windows containing 'N'.

## Caveats
- Reference includes Ns (assembly gaps, telomeres, centromeres). Always
  check `'N' in window` before accepting.
- Forward strand only. If you want strand-augmented training, you'd have
  to reverse-complement, but prepare.py is a black box so I leave it forward.
- Chromosome names in hg38.fa: `chr1`..`chr22`, `chrX`, `chrY`, `chrM`,
  plus many alt/random/unplaced contigs. Filter to main chromosomes for
  most use.
