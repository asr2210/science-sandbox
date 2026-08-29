# Experiment 012 — RC augmentation

## Design
25K random hg38 natural windows + their 25K reverse complements
(50K total but only 25K unique sequence contents).

## Result
- eval_01: 0.3883 (Δ +0.0007 vs nat baseline 0.3876)
- K562: 0.5967, HepG2: 0.4230, SK-N-SH: 0.1453

Within noise floor of seed variance (~0.002). **RC augmentation
is neutral.**

## Interpretation
Either:
1. The trained model is already RC-equivariant (architecture)
2. Halving unique sequence content offsets RC gain
3. Eval doesn't require RC symmetry

The eval pair pattern (eval_01==eval_14, etc) is NOT RC pairing
of evals — those are still independent metrics. The duplication
must be in the eval _input_ structure, not the model output.

## Side observation
eval_07 hit 0.3938 (vs 0.3823 nat baseline, Δ +0.0115). One eval
benefited from RC augmentation while others didn't budge. Possible
that one specific eval set is RC-sensitive. Not a strong enough
signal to act on.

## Next direction
RC augmentation off the table. Continue testing distributional
breadth hypotheses (T7):
- GC stratification (uniform across GC bins)
- Mix ratio sweep (90/10 vs 60/40 nat/reg)
- Cell-type marker DHS sampling
