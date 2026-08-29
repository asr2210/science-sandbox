# 012 GC content sweep (9 levels)

## Design
- 4 letter anchors × 1250 = 5000 (10%)
- 9 GC-content random strata × 5000:
  GC ∈ {0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85}
  Within GC: equal 1/2. Within AT: equal 0/3.

## Result
eval_01 = 0.6192 — NEW BEST.
+0.025 over exp 011 (0.5947).
eval_07 = 0.6934, eval_13 = 0.6634. All evals improved except eval_08
(stuck ~0.13).

## Conclusion
Fine GC sweep beats ad-hoc compositional strata. The score scales with
how much of the f-g curve we cover with compositional variety.

## Next
Add orthogonal compositional axes (purine vs pyrimidine, 01 vs 23
grouping) on top of GC sweep.
