# 001 — uniform random baseline

## Design
50,000 × 200 bp uniform-random DNA, each base i.i.d. from {A,C,G,T},
3 seeds (0/1/2). No constraints, no motifs, no genomic context.

## Results (mean over 3 seeds)
- eval_01 = **0.6954**
- mean across 14 evals ≈ **0.732** (range 0.6553–0.8115)
- per cell type: K562=0.731, HepG2=0.715, SK-N-SH=0.745 (averaged across evals)

## Across-seed variability
eval_01 by seed: 0.6969 / 0.6917 / 0.6976 → SD ≈ 0.003. Tight.
Across all evals, seed-to-seed deltas are <1%. Good reproducibility means
that comparisons between experiments will be sensitive to sub-percent
effects.

## Interpretation
Surprisingly high — random DNA is far from a "near-zero" floor. Two
non-exclusive explanations:
1. **Chance motifs hypothesis (de Boer 2024).** A 200bp uniform-random
   sequence contains ~196 6-mer windows; many will match real TF motifs
   by chance. Across 50K sequences that's ~10M motif-matched windows —
   enough to learn motif → activity if the assay/model picks it up.
2. **Composition baselines.** GC content / oligonucleotide frequencies
   alone may explain a chunk of the variance. Need to test.

## Per-eval pattern
Evals split into two clusters:
- High (~0.78–0.81): eval_02, 06, 08, 09, 14
- Mid (~0.66–0.76): eval_01, 03, 04, 05, 07, 10, 11
- Low (~0.65–0.66): eval_12, 13
This structure may reflect different eval-set difficulties or different
cell types / contexts — informative for picking what to optimize for.

## Cell-type pattern
SK-N-SH > K562 > HepG2 in nearly every eval. Random DNA model transfers
slightly better to SK-N-SH. Could be: (a) SK-N-SH eval data is "easier",
(b) SK-N-SH activity is more dominated by sequence-intrinsic features
that even a random-trained model captures.

## What this updates in the theory
T0 predicted random DNA produces a non-trivial model — confirmed.
What's surprising is HOW non-trivial: 0.7 correlation is a strong
baseline. Any subsequent design must clear this bar to be informative.

## Next experiment thoughts
The most informative next step is the head-to-head comparison:
real genomic regulatory elements (cCRE/DHS) vs. random.
- If real >> random: cis-regulatory grammar in real elements is
  irreplaceable, even though it brings homology bias.
- If real ≈ random: de Boer's "use synthetic, not genome" thesis is
  strongly supported.
- If real < random: would be a major result — the homology / repetitive
  / cell-type-program biases of natural sequences are net-harmful for
  generalization.
