# 012_malinois_random

## Setup
50k uniform-random subsample of the Malinois MPRA dataset (Gosai/Tewhey
2024): 763k 200bp oligos measured in K562/HepG2/SKNSH. Sequences tile
GTEX eQTLs (445k), UKBB GWAS variants (338k), and a CRE-derived subset
(14k).

## Result
- eval_01 = 0.6856 (cf. exp 002 cCREs = 0.6921, **−0.007**)
- eval_04 = 0.5832 vs 0.5977 (−0.015)
- eval_07 = 0.7521 vs 0.7562 (−0.004)
- eval_08 = 0.1194 vs 0.1248 (~tied)
- eval_10 = 0.6594 vs 0.6673 (−0.008)

## Interpretation
This is a surprising NEGATIVE result. Real MPRA training sequences
measured in the exact target cell types are *slightly worse* than
cCREs as a training library.

Two implications:
1. **No eval leakage**: the eval set is not a hidden split of the Malinois
   dataset. If it were, training on Malinois subsamples would give a big
   boost. The eval is generated independently (different sequences).
2. **Variants are noisy training material**: Malinois oligos are
   centered on GWAS/eQTL variants. Most variants have small (or no)
   effect on activity, so the bulk of Malinois oligos are
   regulatory-grammar-poor — they're just random genomic context. By
   contrast cCREs are pre-filtered for biochemical signatures of
   regulatory activity.

The cCRE library carries denser regulatory signal per sequence than the
Malinois variant tiles. cCREs win because each one is enriched for
function; Malinois sequences are enriched for *being near a variant*,
which is a much weaker prior.

## Takeaway
Need to select the *active* subset of Malinois rather than uniform
random. Will try variance-based selection in exp 013: prefer oligos
where K562/HepG2/SKNSH measurements show large magnitude or large
between-cell-type differences.
