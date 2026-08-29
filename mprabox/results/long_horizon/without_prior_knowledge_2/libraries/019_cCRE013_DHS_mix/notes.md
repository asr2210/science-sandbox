# 019 — cCRE 013 + filtered DHS (50/50 atlas mix)

## Design (planned)
25K from 013-style cCRE: 5K each rare class (PLS, CA-CTCF, CA-TF,
CA-H3K4me3) + 1.25K each abundant (pELS, dELS, CA, TF) = 25K.
+ 25K uniform from filtered DHS pool (mean_signal >= q75 AND
numsamples >= 5; ≈681K elements; same filter as 009).
= 50K total.

200bp centered on cCRE midpoint (cCRE half) or DHS summit (DHS half).

## Hypothesis tested
Whether DHS adds INDEPENDENT signal on top of cCRE. Different from
018 which tested if the same upweighting principle generalizes —
this tests if the two atlases are complementary.

## Pre-experiment branches
- 019 > 013 → DHS atlas adds independent signal even though
  atlas-level rebalancing (018) failed; the two atlases together
  cover sequence space the cCRE atlas alone misses
- 019 ≈ 013 → DHS is ~redundant with cCRE
- 019 < 013 → DHS dilutes cCRE quality (echoes 007's strat+random
  failure); pure 013 wins
