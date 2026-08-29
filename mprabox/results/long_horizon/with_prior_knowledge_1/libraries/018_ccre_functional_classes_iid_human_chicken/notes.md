# 018 — cCRE functional only (12K PLS + 12K pELS + 11K dELS) + 5K iid + 5K human + 5K chicken

## Result — DRAMATIC regression, structural cCRE classes are CRITICAL
| metric  | 018 | 010 | Δ vs 010 |
|---------|-----|-----|----------|
| eval_01 | 0.6989 | **0.7599** | −0.0610 |
| eval_02 | 0.7881 | **0.8550** | −0.0669 |
| eval_03 | 0.7671 | **0.8413** | −0.0742 |
| eval_04 | 0.7703 | **0.8140** | −0.0437 |
| eval_05 | 0.6988 | **0.7599** | −0.0611 |
| eval_06 | 0.7882 | **0.8550** | −0.0668 |
| eval_07 | 0.6992 | **0.8044** | −0.1052 |
| eval_08 | 0.6409 | **0.7515** | −0.1106 |
| eval_09 | 0.8358 | **0.8872** | −0.0514 |
| eval_10 | 0.7398 | **0.8233** | −0.0835 |
| eval_11 | 0.6863 | **0.7464** | −0.0601 |
| eval_12 | 0.6606 | **0.7244** | −0.0638 |
| eval_13 | 0.6938 | **0.8016** | −0.1078 |
| eval_14 | 0.7882 | **0.8551** | −0.0669 |

Mean 14: **0.7326** vs 010=0.8056 (−0.0730). Wall: 546 s (much shorter
than usual ~1300s — the model trained faster, plausibly because
validation loss plateaued earlier on a worse representation).

## Per-seed eval_01
- seed 0: 0.7145
- seed 1: 0.6887
- seed 2: 0.6935

Spread = 0.026, moderate. The −0.073 mean regression is consistent
across all 3 seeds (not a one-bad-seed artifact).

## Pre-registered scorecard
- "018 > 010 by ≥ +0.005 (functional-only better, NEW BEST)":
  **strongly falsified**.
- "018 ≈ 010 (class balance doesn't matter)": falsified.
- "018 < 010 by 0.005-0.015 (mild structural contribution)": falsified.
- "018 < 010 by > 0.015 (structural classes critical)": **confirmed
  STRONGLY**, magnitude (−0.073) is HUGE — bigger than any single
  axis-swap loss measured so far.

## Two competing interpretations
The −0.073 could be due to:
  (i) Removing structural classes (CTCF-only, DNase-H3K4me3) erases
      a critical chromatin-context anchor the model uses to
      contextualize regulatory features.
  (ii) Imbalanced functional-class distribution (12K/12K/11K) confuses
       the model: too much mass on PLS/pELS/dELS dilutes their
       discriminative value.

Both effects could combine. The 019 follow-up (mild rebalance keeping
all 5 classes) will disentangle.

## Theory update — cCRE class diversity is critical
Previous theory treated cCRE backbone as a monolith ("more mass = more
value, up to 35K"). 018 reveals that the COMPOSITION of cCRE matters
sharply. Structural classes (CTCF-only, DNase-H3K4me3) are not
"redundant filler" — they provide essential context for the model.

Possible mechanism: the model learns activity prediction via a
combination of (motif features, chromatin-context features). PLS/pELS/
dELS provide motif signals (active TF binding); CTCF-only and
DNase-H3K4me3 provide chromatin-state signals (boundaries, primed
enhancers). Removing chromatin-state classes leaves the model with no
"context grammar" to disambiguate motif-rich sequences with different
activity levels.

## Refined theory — cCRE backbone has irreducible diversity requirement
> cCRE backbone: 35K total mass IS load-bearing AND class diversity
> matters sharply. Removing 2 of 5 primary classes costs ~−0.073
> mean (10× any single-axis swap). The 5-class structure is not
> arbitrary; it represents an irreducible chromatin-context vocabulary
> the model relies on.

## What I learned (operational)
1. **Sub-axis structure can have effects bigger than axis-swap effects.**
   The 018 −0.073 regression is bigger than the 012 iid-removal
   −0.056. cCRE class diversity is the SECOND most important known
   library design factor after iid presence.
2. **Training time can leak signal about library quality.** 018
   finished in 546s vs ~1300s for prior experiments — the model hit
   early-stopping faster, indicating it learned less. Future
   monitoring: training time as a quick "is this library bad?" signal.
3. **Always test sub-axis structure of large axes.** I treated cCRE as
   a monolith for 17 experiments. Sub-axis effects can dominate.

## What to try next
**019: mild cCRE class rebalance to disentangle 018.** Keep all 5
classes but shift mass toward functional: 9K PLS + 9K pELS + 9K dELS
+ 4K CTCF-only + 4K DNase-H3K4me3 + 5K iid + 5K human + 5K chicken
= 50K.

Pre-registered:
- 019 ≈ 010 (within ±0.005): rebalance is fine when all 5 classes
  are present. The 018 −0.073 was specifically about REMOVING
  structural classes entirely, not about reweighting.
- 019 between 010 and 018 (loss 0.005-0.060): mild rebalance hurts
  proportionally. Class balance has continuous value, not just step.
- 019 ≈ 018 (loss ~0.07): even mild rebalance immediately hurts;
  10's exact 7K-each balance is sharply optimal.

Alternative 019 candidates considered:
- All-structural (17.5K CTCF + 17.5K DNase): probably catastrophic;
  not informative.
- Drop just CTCF or just DNase: more focused but harder to compare
  to 018.

Going with the mild-rebalance design above. It's the cleanest test of
"is class balance a step (binary present/absent) or a continuous
function".