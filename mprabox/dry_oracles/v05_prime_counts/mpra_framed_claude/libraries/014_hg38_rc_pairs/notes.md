# Exp 014 — Strand augmentation (forward + RC pairs)

## Design
25K random hg38 windows; each contributes 2 sequences (forward + RC).
Total 50K, 25K independent contexts. GC=0.409.

## Result
**eval_01 = 0.0479.** Tied with 013 (0.0493) and 010 (0.048). RC pairing
neither helps nor hurts measurably.

| eval | 010 | 013 | 014 |
|------|-----|-----|-----|
| 01 | 0.0480 | 0.0493 | 0.0479 |
| 07 | 0.0331 | 0.0348 | 0.0371 |
| 13 | 0.0376 | 0.0363 | 0.0343 |
| HepG2 mean | 0.0526 | 0.0535 | 0.0506 |

## Interpretation
Two readings, both consistent:
1. prepare.py's model already RC-augments internally (so explicit RC adds
   no information).
2. RC pairing gains exactly cancel diversity loss (25K vs 50K contexts).

Either way: no lift available from this axis.

## Theory update
Symmetry augmentations are not the bottleneck. The 0.05 ceiling on natural
hg38 libraries holds.

## Next step
Try the opposite enrichment direction: 30K random + 20K cCRE (stronger
regulatory enrichment than 013's 20%). Tests whether HepG2 lift from
cCRE-enrichment can be pushed further before composition skew bites.

## Time
42s wall, 11s evaluator.
