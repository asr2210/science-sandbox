# 003 — GC Content Gradient

## Hypothesis
Pearson r will scale with the variance of predictions across the library.
GC content is one of the most robust correlates of regulatory activity, so a
wide spread in GC (0.15 to 0.85) should produce a wide spread in predicted
activity for both scoring methods → higher r.

## Method
For each of 50,000 sequences, draw target GC fraction ~ Uniform(0.15, 0.85),
then sample 200 bases i.i.d. with that GC.

## Result
- eval_01 mean_r = **0.3610** (vs 0.4200 random — significantly worse)
- K562: 0.5023 (−0.086 vs random!), HepG2: 0.5295 (−0.089), SKNSH: 0.0513

## Interpretation
GC gradient made things WORSE, not better — and by a large margin.
This kills the simple "variance is the lever" hypothesis.

Possible explanations:
1. Extreme GC (≤0.20 or ≥0.80) is far out-of-distribution for both scoring
   models; their predictions diverge in those regions even though the within-
   library variance is high. Random uniform (GC ≈ 0.50, narrow spread) stays
   well within the training distribution.
2. The metric may reward libraries whose k-mer / di-nucleotide distribution
   matches a "typical" reference distribution. Random uniform matches a flat
   k-mer distribution; GC-extreme libraries deviate strongly.
3. Maybe the scoring is composition-aware in a way I haven't pinned down.

Two interventions (002 motifs, 003 GC gradient) both reduced r. Random uniform
remains the strongest. This is a striking result on its own.

## Next
Test "realistic" composition (hg38-like dinucleotide Markov chain) vs random
uniform. If realism beats uniform, in-distribution wins. If realism is also
worse than uniform, then uniform is genuinely close to the metric-maximizing
point and I need a different angle entirely.
