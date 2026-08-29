# Exp 022 — GC-stratified hg38 (4 bins, 12.5K each)

## Design
Sample 12.5K random hg38 windows in each of 4 GC bins (30-40, 40-50,
50-60, 60-70%). Library GC=0.491 (shifted high vs natural 0.41).

## Result
**eval_01 = 0.0488; HepG2 = 0.0562.** Plateau. But notable shifts in
individual eval cells:
- HepG2 on eval_01 = 0.0632 (highest single value seen!)
- eval_04/09: 0.0551 (highest)
- eval_13: 0.0293 (regression from 010's 0.038)
- eval_07: 0.0265 (regression)

## Interpretation
GC stratification rebalances signal: rewards high-GC-responsive evals
(HepG2 strongly) but hurts sequence-specific evals (eval_07, 13). Net
eval_01 unchanged.

## Theory update
- Composition shifts via stratification do redistribute signal across
  cell types and eval directions, but the AVERAGE eval_01 sits at the
  natural ceiling of 0.05.
- Implies the eval set itself has a natural composition; libraries far
  from that composition trade off some evals for others, never lifting
  the mean.

## Next step
Sweep cCRE fraction lower. 013 (20% cCRE) is best stable; try 5% cCRE
(47.5K rand + 2.5K cCRE) to see if even lighter enrichment captures the
benefit.

## Time
42s wall, 11s evaluator.
