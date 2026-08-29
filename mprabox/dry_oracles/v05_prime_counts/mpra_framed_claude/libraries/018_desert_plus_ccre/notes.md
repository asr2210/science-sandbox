# Exp 018 — 40K gene-desert + 10K cCRE (additive test)

## Design
Combine the two helpful directions:
- 40K gene-desert (016 mechanism: HepG2 lift)
- 10K cCRE-centered (013 mechanism: marginal eval_01 lift)
GC=0.415; CpG=0.0108.

## Result
**eval_01 = 0.0477; HepG2 = 0.0554.** Essentially identical to 016 alone.

| metric | 016 (desert) | 013 (rand+cCRE) | 018 (desert+cCRE) |
|--------|--------------|-----------------|---------------------|
| eval_01 | 0.0479 | 0.0493 | 0.0477 |
| HepG2 | 0.0556 | 0.0535 | 0.0554 |
| eval_13 | 0.0384 | 0.0363 | 0.0376 |

## Interpretation
The two lifts do NOT stack. Gene-desert + cCRE ≈ gene-desert alone. The
cCRE addition adds no new signal once gene-desert background is in place.
This implies the 013 eval_01 lift (+0.001 over 010) was mostly noise OR
it operated through the same "natural DNA mix" axis that gene-desert
already maxes out.

## Theory update
- Confirmed: gene-desert is the best single direction for HepG2 lift,
  bounded at ~0.056.
- Combinatorial stacking of natural-DNA designs doesn't break the
  ceiling. The 0.05 eval_01 / 0.056 HepG2 floor is structural.

## Next step
Try a fundamentally different signal: explicit cell-type-balanced design.
Combine gene-desert with a small motif "injection" of TFs known to be
HepG2-active (HNF4, CEBP, FOXA), to see if motif-knowledge can push
HepG2 further past gene-desert ceiling.

## Time
51s wall, 21s evaluator.
