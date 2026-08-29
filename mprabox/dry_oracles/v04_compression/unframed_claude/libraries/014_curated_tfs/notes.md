# 014 — Curated 33 TFs (univ + cell-type), 3/seq

## Setup
22 universal + 7 HepG2-specific + 6 K562-specific + 6 SK-N-SH-specific
(33 successfully loaded from JASPAR).

## Results
eval_01 = 0.3433 (exp 010 was 0.3644). **Drop on eval_01 by 0.02.**
BUT: eval_07 = 0.4698 (new best), eval_13 = 0.4393 (new best), eval_08 +0.01.

## Insight
eval_01 specifically likes my smaller 17-universal-TF set. Adding cell-type
specific dilutes the effect. Other evals (07, 08, 13) benefit from broader TF
coverage.

## Next
Try EVEN SMALLER universal set (8 TFs) to see if eval_01 keeps climbing.
