# Skill — Mixing heterogeneous sub-libraries

## Key findings (from exp 001-010)

1. **No single library type lifts all three cell types equally.**
   - Random uniform DNA → no signal anywhere
   - Random hg38 genomic → essentially no signal
   - cCREs (proportional sampling) → essentially no signal
   - TSS-centered promoters → HepG2 signal on certain evals (~0.014)
   - Sparse motif scaffold (~5 motifs/seq) → mild K562 signal
   - Dense motif scaffold (~20 motifs/seq, mixed pool) → broader K562
     + occasional SKNSH on some evals
   - 70/30 dense-motif / promoter mix → best mean to date (eval_07
     = 0.0088, all three cell types positive)
   - 50/50 mix → mixing dilutes both signals; mean drops
   - 80/20 mix → different evals light up; mean drops

2. **Library mixing is non-additive.** A 50/50 mix of two
   beneficial libraries does NOT produce a 50/50 lift; it can be
   worse than either alone. The dominant subset drives what the model
   learns.

3. **Weight toward the broader-acting subset.** Dense motif scaffolds
   help multiple cell types and many evals; promoters help only
   HepG2 evals. So a motif-dominant mix (70/30) outperforms balanced.

4. **The eval set is heterogeneous.** Different evals respond to
   different sequence "modes" — motif-loaded enhancers, promoter-like,
   etc. A library hitting more modes lifts the mean.

## Best library recipe (so far)

35,000 dense motif scaffolds + 15,000 TSS-centered RefSeq promoters,
shuffled together. mean_r ≈ 0.003, eval_07 ≈ 0.009 (all three cells).

## Mixing patterns to try next

- 3-way mix: dense motif scaffolds + TSS promoters + PLS cCREs
  (the most active real-regulatory class).
- Concentrated motif clusters (homotypic) for distinct motifs.
- Saturation of motif syntax (specific spacings/orientations) since
  natural enhancers care about syntax.

## What NOT to do

- Don't mix random uniform DNA or random genomic — they contribute
  noise.
- Don't down-weight motif scaffolds below ~50% — K562 signal collapses.
- Don't over-design cell-type-specific subsets in small fractions
  (they get drowned out).
