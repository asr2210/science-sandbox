# 007 — Saturation mutagenesis (2500 seeds × 20 variants)

## What I tested
2500 seeds (random chr22 200bp + 3 random motifs) × 20 variants per seed
(1 original + 19 single-base random substitutions) = 50,000 sequences.

## Result
- eval_01 = **0.0977** (vs 006: 0.135, drop of 0.04)
- mean of evals = 0.0941
- K562: 0.018  (lower than even random baseline)
- HepG2: 0.124
- SK-N-SH: 0.152
- eval_08 dropped to **0.021** (its worst)

## What this means
STRONG negative result. Saturation mutagenesis with only 2500 unique
contexts is far worse than random genomic. The 19 variants per seed
add redundancy without diversity — the model sees only 2500 actually-
different sequences when it could be seeing 50,000.

## Theory update
- **Context diversity dominates gradient-information value** for a
  50k-sequence library with a small CNN.
- Number of unique contexts matters more than within-context variation.
- Active learning's "informativeness per example" advantage breaks
  down when "informativeness" = small Hamming-distance variants of
  the same context.

## What to try next
008: pivot to a mixed library. 25k chr22 random + 25k chr22+motifs.
Tests: does mixing two-best strategies (broad genomic + motif boost)
beat either alone?
