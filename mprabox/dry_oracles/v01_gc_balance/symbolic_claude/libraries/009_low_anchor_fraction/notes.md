# 009 low anchor fraction (20%) + 4 diverse random strata

## Design
- 4 letter anchors × 2500 = 10000 (20% anchor weight)
- 4 random strata × 10000 each = 40000:
  uniform, GC-rich, AT-rich, no-homopolymer

## Result
eval_01 = 0.5689 — NEW BEST.
+0.006 over exp 005 (0.5627).
+0.039 over exp 003 (pure uniform random).

## Interpretation
The combination of (a) diverse random strata and (b) modest anchor weight
beats either alone. Anchors at 20% are sufficient — heavier anchor weight
hurts (exp 005 had 62% anchor, lower score).

The "no-homopolymer" stratum is new; possibly contributes positively by
filling a region of (f, g) space.
