# 002_chr22_tiles

## Hypothesis
Real human genomic DNA from chr22 (random 200bp tiles) will score higher than uniform random sequences if the scoring function rewards biological content (motifs, GC structure, dinucleotide patterns).

## Method
- Download hg38 chr22 from UCSC
- Sample N=50,000 random 200bp tiles
- Reject tiles containing any 'N' base
- Seed 42

## Result
- **eval_01 mean_r = 0.3928** (K562=0.6038, HepG2=0.4285, SKNSH=0.1461)
- Slightly *worse* than random uniform (0.3981).
- Same eval-duplication pattern (01==14, etc.); same eval_08 outlier.

## Interpretation
Biological DNA does NOT outperform random uniform. This is a strong negative result. It suggests:
1. The score isn't a simple "biological content" detector.
2. Random uniform's higher entropy / 50% GC may even be slightly favored.
3. chr22 has biases (AT-rich, repeats, low-complexity stretches) that random uniform doesn't have.

The score difference (0.005) is small but consistent across most evals.

## Next
- Test cCRE-centered windows (real curated regulatory elements). If those also don't beat random, biology is firmly not the axis.
- Probe what *does* matter: GC content, sequence entropy, dynamic range.
