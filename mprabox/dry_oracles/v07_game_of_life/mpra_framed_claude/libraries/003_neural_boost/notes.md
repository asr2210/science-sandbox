# Experiment 003 — neural DHS boost

## Design
15K natural + 10K cCRE off + 10K pan-tissue DHS + **10K neural-tagged
DHS** + 5K mouse. Swapped 5K natural and 5K cCRE for 10K Neural-component
DHS summits.

## Result
- eval_01: 0.393 (Δ -0.001 vs exp 002, no change)
- K562: 0.605, HepG2: 0.428, SK-N-SH: 0.147 (all within noise of exp 002)

## Interpretation — T1 IS WRONG
T1 said: cell-type-specific regulatory content boosts cell-type-specific
prediction. Predicted: SK-N-SH lifts more than K562/HepG2. Observed:
SK-N-SH did not budge. Neural DHS swap was a wash.

This is a clean negative result. Three competing explanations:
1. DHS "Neural" component is brain (CNS) but SK-N-SH is neuroblastoma
   (PNS sympathetic). Wrong cell-type identity.
2. SK-N-SH gap is structural — MPRA noise floor in SK-N-SH, or model
   capacity limit, or eval-set construction.
3. 10K is too small a fraction to move SK-N-SH (need ≥25K?).

I lean toward (2): the eval pattern is identical across all 3 libraries
(eval_13 always best, eval_08 always worst, similar K562/HepG2/SK-N-SH
ranking). Eval-set difficulty seems intrinsic to the model not the
library.

## Implication
**Tissue-specific content selection is not a useful knob for v07.**
Focus next on: (a) different sequence-distribution properties (activity
range, motif density, naturalness), (b) overall library composition
rather than tissue-specific selection.
