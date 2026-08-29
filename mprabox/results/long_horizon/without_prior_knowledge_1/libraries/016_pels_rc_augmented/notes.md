# 016_pels_rc_augmented — notes

## Design
25K unique pELS (no replacement) + 25K reverse-complements
of those same elements, shuffled. 50K total sequences. Same
central-200bp extraction. Trades pool coverage (50% fewer
unique elements) for strand coverage (2× per element).

## Hypothesis
TF binding sites are largely strand-symmetric. A model trained
on single-strand data must learn this implicitly. Explicit RC
augmentation gives the model direct examples of both strands
per element.
- (A) "RC helps": mean > pELS-only (0.758) — model can't easily
  learn strand symmetry from one-sided data.
- (B) "RC neutral": mean ≈ pELS-only — model handles RC
  implicitly, augmentation is wasted.
- (C) "RC hurts": mean < pELS-only — pool coverage matters more
  than strand coverage.

## Result vs. pELS-only

| eval | pELS012 | RC016  | Δ      |
|------|---------|--------|--------|
| 01   | 0.7203  | 0.7048 | -0.016 |
| 02   | 0.8129  | 0.7958 | -0.017 |
| 03   | 0.7958  | 0.7800 | -0.016 |
| 04   | 0.7603  | 0.7495 | -0.011 |
| 05   | 0.7203  | 0.7047 | -0.016 |
| 06   | 0.8133  | 0.7964 | -0.017 |
| 07   | 0.7489  | 0.7254 | -0.024 |
| 08   | 0.6844  | 0.6626 | -0.022 |
| 09   | 0.8238  | 0.8123 | -0.012 |
| 10   | 0.7729  | 0.7560 | -0.017 |
| 11   | 0.7083  | 0.6930 | -0.015 |
| 12   | 0.6853  | 0.6701 | -0.015 |
| 13   | 0.7473  | 0.7230 | -0.024 |
| 14   | 0.8129  | 0.7960 | -0.017 |

Mean: pELS012 0.758, **RC016 0.741, Δ=-0.017**.

## Interpretation

**Hypothesis (C) confirmed: RC augmentation hurts.** Every
single eval drops. The penalty is uniform (-0.011 to -0.024,
mean -0.017), with no eval benefiting from RC examples.

This is a clean falsification of two ideas at once:
1. **Model already learns strand symmetry implicitly.** If RC
   was a feature the model couldn't easily acquire, explicit
   augmentation would lift performance. It does not.
2. **Pool diversity dominates.** The cost of halving unique
   elements (25K instead of 50K) outweighs any benefit from
   the RC examples.

The drops on eval_07 and eval_13 (-0.024 each) are the largest.
These were the dELS-favoring evals. The model's RC examples
appear to introduce slight redundancy that especially hurts
distal-enhancer-like generalization.

## Theory update

**New rule: explicit augmentation that reduces pool diversity
is strictly bad.** The architecture is already RC-equivariant
enough that adding RC examples is redundant; the cost is
losing real biological diversity.

This rules out a whole family of "augment by transforming
existing sequences" strategies. Useful augmentation must come
from genuinely new sequences (more elements, more positions),
not from transformations of existing ones.

**Implication:** to push past pELS-only's 0.758, we need
either:
1. More unique elements at the same window (already sampling
   25K from 249K — could go to full pool or to multiple
   windows per element)
2. Better sub-sampling within elements (random offset vs
   central) — tests whether "central 200bp" is overly
   restrictive
3. Pool filtering by quality/conservation/signal strength —
   tests whether the pELS pool has noise that filtering helps

Mixing classes (002, 005, 013, 015) and transformation
augmentation (016) are both ruled out. Stay single-class.
Only single-class operations remain.

## Next experiment

**Exp 017: pELS with random within-element offset.** Same 50K
unique pELS, no replacement, but instead of central-200bp
extract a 200bp window at a random offset within the cCRE.
Tests whether central position is too restrictive (model sees
only one slice of each element) vs whether positional
variation is just noise.
