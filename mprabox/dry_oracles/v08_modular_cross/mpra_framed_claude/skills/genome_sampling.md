# Skill — Sampling random 200 bp windows from hg38

## When to use
Any time you need real genomic background sequence: as a positive
baseline, as a backbone for motif insertion, as a control distribution,
or as the main library itself.

## Setup (do once)
```
curl -sS -o data/hg38.fa.gz \
  https://hgdownload.soe.ucsc.edu/goldenPath/hg38/bigZips/hg38.fa.gz
gunzip data/hg38.fa.gz
python3 data/cache_hg38.py   # produces data/hg38_npy/chrN.npy uint8
rm data/hg38.fa              # save 2.3 GB
```

The npy cache is ~2.9 GB total (24 autosomes + X + Y).

## How to load
```python
import numpy as np, os
CHROMS = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
seqs = {c: np.load(f"data/hg38_npy/{c}.npy", mmap_mode="r") for c in CHROMS}
```
mmap_mode="r" keeps RAM low — no need to load 3 GB into memory.

## How to sample 200 bp windows uniformly across the genome
Weight chromosomes by length so sampling is uniform per base.
Reject windows containing N (assembly gaps) and optionally repeat-mask
masked-out regions.

```python
def sample_windows(n, L=200, seed=0, autosomes_only=True):
    rng = np.random.default_rng(seed)
    chroms = [f"chr{i}" for i in range(1, 23)]
    if not autosomes_only:
        chroms += ["chrX", "chrY"]
    sizes = np.array([len(seqs[c]) - L for c in chroms], dtype=np.int64)
    weights = sizes / sizes.sum()
    out = []
    while len(out) < n:
        c_idx = rng.choice(len(chroms), p=weights)
        chrom = chroms[c_idx]
        s = rng.integers(0, sizes[c_idx])
        window = bytes(seqs[chrom][s:s+L]).decode("ascii")
        if "N" in window:
            continue
        out.append(window)
    return out
```

## Notes
- ~5–7% of hg38 is N (gaps, centromeres, telomeres). Rejection
  sampling handles this cleanly with negligible overhead.
- Random uniform genomic sampling is dominated by non-regulatory
  sequence (~98% of genome is not enhancer/promoter). That's
  realistic — most random windows should have low MPRA activity.
- For *enhancer*-enriched sampling, intersect with ENCODE cCRE BED
  files instead (see future skill).
- Strand: hg38 is on the forward (+) strand only. MPRA libraries
  generally test the sequence as-given; reverse complement
  augmentation is a separate design decision.
- Repeat content: hg38 fasta has soft-masked repeats in lowercase if
  using softMasked file; the bigZips/hg38.fa.gz I use here is
  all-uppercase. Cache uppercases regardless.

## What NOT to do
- Don't sample from one chromosome only — biased by chromosome-
  specific gene density / GC.
- Don't include unplaced/random contigs (chrUn_*, *_random) — they
  are mostly repetitive junk.
