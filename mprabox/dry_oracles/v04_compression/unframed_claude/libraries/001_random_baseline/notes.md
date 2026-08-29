# 001 — Random baseline

## Hypothesis
Uniform random DNA gives the "no signal" reference score. If "r" is correlation between predicted activity and observed, random should be near 0; if it's a normalized predicted-activity, it should be moderate.

## Setup
50,000 sequences, 200bp, uniform i.i.d. {A,C,G,T}. Seed 20260602.

## Results
eval_01 mean_r = 0.3157  (K562=0.3134, HepG2=0.3134, SKNSH=0.3204)
All 14 evals: range 0.10 (eval_08) — 0.45 (eval_07). Mean ≈ 0.32.

## Key observations
1. **K562_r == HepG2_r exactly** in every single eval. The scoring function must
   evaluate K562 and HepG2 with the same predictor, or the cell-line annotations
   shown are misleading. SKNSH differs only slightly. Implication: optimizing
   "across cell types" is not really 3 independent targets — effectively 2.
2. **Duplicate evals**: 01==14, 02==05, 04==09, 03==12, 06==11. So 14 evals
   collapse to 9 unique ones. Probably 9 distinct models scored with some repeats.
3. **Random baseline is HIGH (~0.32)**. Strongly suggests "r" is not a correlation
   (would be ~0 for random) but a predicted-activity / rank-score that has a
   nonzero floor. Improvements must beat 0.32.
4. eval_08 baseline is 0.10 — the hardest / strictest eval. Big headroom there.
5. eval_07 baseline is 0.45 — already easy on random; less to push.

## Update to theory
- This is likely a regression/prediction setup where each eval returns a per-eval
  mean predicted-activity score. So we are designing libraries whose sequences
  the model PREDICTS to be highly active.
- K562 and HepG2 share a model. SKNSH is a separate (but similar) model.
- 9 distinct evaluators — likely 9 different MPRA models.

## Next
Test composition: does GC content matter? Then test motif insertion.
