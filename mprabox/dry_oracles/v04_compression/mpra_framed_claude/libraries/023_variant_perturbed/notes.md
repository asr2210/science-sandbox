# 023_variant_perturbed — notes

## Design
12.5K natural + 12.5K natural-5SNPs + 10K cCRE + 5K cCRE-5SNPs +
5K DHS + 5K mouse = 50K. Each "variant" is base sequence with 5
random point mutations (2.5% substitution rate).

## Result
- eval_01 = 0.4985 (vs exp 011 = 0.5012, Δ = -0.003, within noise)
- All evals within ±0.005 of 011
- Time: 24s

## Interpretation
Paired-variant supervision is neutral. The model treats variants as
just more sequences in the library; it doesn't extract paired structure
because nothing in the training signal tells it which sequences are
paired.

## Implication
Synthetic paired-data construction doesn't unlock new signal in
single-pass supervised training. The plateau holds.

## Lesson
Augmentation (RC in 016, variant pairs here) doesn't help. The
information bottleneck is sequence-level content/diversity, not
example count or example structure.

## Next test
Maximal atlas diversity: 6-way mix with cCRE + DHS + ChIP + FANTOM5
all at moderate fractions. Tests if ALL the atlases together add
incremental signal vs the 2-atlas mix of exp 011.
