# Experiment 005 — Fixed composition (50/50/50/50)

## Setup
- 50K strings, each with exactly 50 of each letter {0,1,2,3}, randomly shuffled.
- Within-string order varies; per-string composition is constant.

## Results (vs exp 001 random)
- eval_01: mean 0.118 → -0.023 (DROP and FLIP).
- condition_a: 0.009 → ~0 (dropped ~near zero).
- condition_b: 0.156 → 0.017 (huge drop).
- condition_c: 0.190 → -0.085 (FLIPPED SIGN).

## Interpretation
- Composition variance was the PRIMARY driver of positive scores.
- Without composition variance, features barely correlate.
- condition_c is most composition-sensitive (sign-flips).
- condition_a is least composition-sensitive (didn't change much).

## Implications
- To push b, c up: need to provide MORE composition variance (in the right way).
- For condition_a: composition variance isn't the main lever. Try motifs / structure / something else.
- Exp 003 had composition variance but in a biased way (only '0' varied) and score dropped. So composition variance must be SYMMETRIC across letters.

## Next
Exp 006: Dirichlet-driven per-row composition. Each row has p ~ Dirichlet(α,α,α,α), then sample iid.
- α=1 gives uniform on simplex (more composition variance than exp 001's fixed-uniform).
