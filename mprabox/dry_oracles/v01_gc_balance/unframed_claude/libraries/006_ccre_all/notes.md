# 006_ccre_all

50k 200bp windows centered on ENCODE cCREs (all categories: PLS, pELS, dELS, CTCF-only, DNase-H3K4me3).

## Result
eval_01: 0.6840 (vs 0.6780 chr22) — only marginally better.
eval_07: 0.7412 (vs 0.7462 chr22) — slightly worse.
eval_04: 0.6093 (vs 0.5809 chr22) — +0.03 improvement.
eval_08: 0.1279 (vs 0.1230 chr22) — still stuck low.

## Interpretation
cCREs barely beat random chr22 slices. The scorer isn't strongly differentiating
"regulatory" from "generic real DNA." This is interesting — implies the predictor
& target functions agree about most real DNA, not just cREs.

Hypothesis: there is a saturation effect. Once the library "looks like real DNA"
the score plateaus around 0.68 for eval_01, 0.74 for eval_07.

To push higher we probably need to:
1. Pick sequences with strong, confident predictions (where predictor and target
   both give large signal)
2. Use cell-type-specific accessible regions
3. Possibly use real MPRA-tested sequences directly

## Next
- 007: multi-chromosome whole-genome random sampling — sanity check
- 008: K562 DNase HS peaks
- 009: aggregate top hits
