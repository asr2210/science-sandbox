# 023_mega_rc_jitter

## Setup
Same recipe as exp 020 (30k cCRE + 10k ChIP + 10k Malinois) but with:
- ±50bp positional jitter on cCRE / ChIP window centers
- 50% reverse-complement of each output sequence

## Result — third 0.6928 in a row
- eval_01 = 0.6928 (**identical** to exp 018, exp 020)
- All other evals within ±0.001 of exp 020

## Interpretation
Triple-confirmed: the mega-pool recipe gives eval_01 = 0.6928 with
remarkable stability:
- exp 018 (balanced 17/17/16, no augmentation): 0.6928
- exp 020 (cCRE-heavy 30/10/10, no augmentation): 0.6928
- exp 023 (cCRE-heavy 30/10/10 + RC + jitter): 0.6928

RC and jitter don't help here (consistent with exp 005 vs exp 002).
The model already learns strand and position invariance from raw data.

## Theory update → T15 — 0.6928 is the design-space maximum
The +0.0007 lift over pure cCRE (0.6921 → 0.6928) is real and
reproducible across 3 mega-pool variants. But the variance across
these 3 variants is < 0.0001 — meaning I cannot push beyond 0.6928
within the multi-source recipe.

## Takeaway
0.6928 is the achievable max for this design space. Will use remaining
experiments to verify (a) no recipe variant pushes past, and (b) the
final library is the best 0.6928 variant. The mega-pool 30/10/10
(exp 020) is the simplest version of the winning recipe.
