# 027_ccre_fantom_malinois

## Setup
3-source variant of the mega-pool: 17k cCRE + 17k FANTOM5 CAGE + 16k
Malinois. Drops ChIP-seq, replaces with FANTOM5.

## Result
- eval_01 = 0.6907 vs (cCRE+ChIP+Malinois) 0.6928 (−0.002)
- **eval_04 = 0.6220 (new best)**
- eval_07 = 0.7416 (down from 0.7553)
- eval_10 = 0.6527 (down from 0.6665)
- eval_13 = 0.7297 (down from 0.7472)

## Interpretation
Replacing ChIP-seq with FANTOM5 costs ~0.002 on eval_01 — ChIP-seq
contributes a small but specific signal to eval_01. FANTOM5 lifts
eval_04 strongly (best across experiments at 0.6220) because
transcription-output evidence directly tests the same regulatory
quantity eval_04 cares about.

## Theory update → T18 — ChIP-seq is the marginal eval_01 lifter
The 3-source mega-pool eval_01 lift above pure cCRE (+0.0007) comes
from the *ChIP-seq + Malinois* combination, not from any 3 sources.
- cCRE + ChIP + Malinois: 0.6928
- cCRE + FANTOM5 + Malinois: 0.6907 (no ChIP, drop)
- cCRE + ChIP + Malinois + FANTOM5: 0.6928 (FANTOM5 doesn't add eval_01,
  but lifts eval_04)

## Takeaway
For pure eval_01: stick with cCRE + ChIP + Malinois (3-source).
For balanced multi-eval: add FANTOM5 → 4-source mega-pool.

Final library candidate: 4-source mega-pool (cCRE + ChIP + Malinois +
FANTOM5) at 12.5k each — exp 025's recipe.
