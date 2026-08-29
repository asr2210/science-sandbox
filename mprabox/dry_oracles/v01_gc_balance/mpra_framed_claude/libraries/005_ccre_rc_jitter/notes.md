# 005_ccre_rc_jitter

## Setup
50k stratified cCREs (same mix as 002, seed=5) with:
- positional jitter: window center = cCRE midpoint ± U(-50, 50)
- 50% chance per sequence of reverse complementing

## Result
- eval_01 = 0.6921 (exp 002 = 0.6921) — IDENTICAL to 4 d.p.
- eval_07 = 0.7582 (was 0.7562), eval_13 = 0.7487 (was 0.7466)
- eval_08 = 0.1221 (was 0.1248)
- Mean: ~0.62

## Conclusion
Null result. RC augmentation and ±50bp positional jitter give essentially
zero gain over the baseline cCRE library. The model presumably already
handles strand and positional invariance internally (most CNN-based MPRA
models do).

## Implication for theory
Within the cCRE pool, augmentations that re-frame the *same biology* don't
help. To push past 0.69 on eval_01, I need either:
1. Different data sources (other regulatory annotations)
2. Better cCRE selection (high-confidence elements)
3. Wider TF/cell-type coverage

The bottleneck is the *information content* of the training set, not how
each example is presented.
