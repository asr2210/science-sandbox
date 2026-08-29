# Experiment 011 — 3-way mix (motifs + promoters + PLS cCREs)

## What I tested
30k dense motif scaffolds + 10k TSS promoters + 10k PLS cCREs (most
active class). Tests whether adding a third sequence type lifts the
floor.

## Result
- eval_08: mean=0.0056, K562=0.0055, HepG2=0.0052, SKNSH=0.0061 —
  balanced positives across all 3 cell types. Best balanced eval seen.
- eval_07: mean=0.0050, SKNSH=0.0124 (still high)
- eval_04/09: mean=0.0041, all 3 positive
- eval_13: mean=-0.0068, HepG2=-0.0183 (worst)
- Mean across 14 evals ≈ 0.0017

## What this tells me
3-way mix DID improve eval_08's balance (all 3 cell types positive).
But the mean took a hit because some other evals went negative (13).

The pattern: adding diversity helps some evals while hurting others.
The library design problem is becoming a multi-objective optimization
over evals.

## Updates to theory
**v3.3 → v3.4:** The eval set acts like a multi-objective benchmark.
Different sub-libraries serve different evals. A library that helps
on EVERY eval simultaneously might not exist within the 50k cap.

The "mean_r" metric may be best maximized by a library that hits the
most evals decently rather than any one strongly.

## Next
Try a different *real* component: pELS cCREs (proximal enhancer-like,
the biggest active class). Mixed with motif scaffolds.
