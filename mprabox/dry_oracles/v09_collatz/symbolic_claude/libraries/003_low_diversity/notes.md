# 003 — Low diversity (template + 5% mutations)

Single balanced template, 50k copies each with iid 5% substitutions.
Composition stays at 25%/25%/25%/25% (verified).

## Result
- eval_01: mean_r=0.1602 (vs 0.2399 baseline) — down 0.08
- a: 0.14 → -0.13 (FLIPPED negative)
- b: -0.05 → +0.14 (FLIPPED positive)
- c: 0.63 → 0.47 (down)
- eval_08 collapsed: 0.087 → 0.019 (most diversity-sensitive)

## Interpretation
The three conditions are NOT aligned:
- Condition a rewards within-library diversity
- Condition b rewards within-library similarity / template-like structure
- Condition c rewards diversity (strongly)
- Net (a+b+c): diversity wins, but b is partially compensating.

To beat uniform random we likely need:
- Preserve uniform composition (from 002)
- Preserve high between-sequence diversity (from this exp)
- Find what condition b wants OTHER than low diversity — likely
  structural features (motifs, periodicity, k-mer patterns) that
  can be embedded without collapsing diversity.

Next: try uniform-random library with a fixed structural motif
inserted at random positions per sequence — keeps diversity high
while adding structure b might like.
