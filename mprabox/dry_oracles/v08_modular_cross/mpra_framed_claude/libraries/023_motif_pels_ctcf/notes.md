# Experiment 023 — 35k motifs + 15k pELS,CTCF-bound only

## What I tested
Same as 012 with pELS slot restricted to the CTCF-bound subset
(96k pool vs full pELS 172k). Hypothesis: CTCF-bound elements are
more conserved/active across cell types.

## Result — slightly worse than 012
- eval_03/12: 0.0037 (slight record on these)
- eval_07: 0.0055 (decent)
- eval_08: mean=0.0064, K562=0.0099, HepG2=0.0086 (balanced but
  lower than 012's 0.0117)
- eval_10: -0.0060 (lost)
- eval_13: SKNSH=0.0147 (high)
- Mean across 14 ≈ 0.0016 (vs 012's 0.0029)

## What this tells me
**Filtering pELS to CTCF-bound DILUTED diversity.** The CTCF-bound
subset is biased toward sequences containing CTCF binding sites
(CCCTC...), reducing TF variety. The model gets a narrower set of
TF features.

Same pattern as 017 (broader motif pool hurt) — variety in the
real-biology pool matters for the model to learn diverse features.

## Updates to theory
**v3.14 → v3.15:** Filtering "real biology" by chromatin feature
HURTS by reducing TF/sequence variety, even when the filter selects
"higher-quality" elements. The raw pELS pool is better than refined
subsets because it spans more TF families.

## Next
Try the inverse experiment: focus the MOTIF pool to 10 universal TFs
(housekeeping/general - SP1, NRF1, ETS, USF, AP1, CREB, NFY, YY1,
TATA, INR). Tests if a focused, generalizable TF set can preserve
mean while improving cell-type-agnostic features.
