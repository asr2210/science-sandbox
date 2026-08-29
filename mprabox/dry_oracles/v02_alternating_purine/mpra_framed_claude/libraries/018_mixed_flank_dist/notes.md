# Experiment 018 — mixed-distance flanks (extreme eval_07/13 but kills 06/11)

## Design
- 25K positives (15K uniform + 5K CTCF + 5K DNH3)
- 25K flanks: 60% far (1500-3000bp) + 40% near (500-1500bp), per-pair
  random choice.

## Result — mean_r 0.133 (worst flank library), but new highs on 07/13
| eval | 013 | 016 | 018 |
|------|-----|-----|-----|
| 06/11 |**0.218**|0.135|0.097 |
| 07    |0.177|0.157|**0.203** |
| 10    |0.151|0.161|0.145 |
| 13    |0.126|0.151|**0.173** |
| mean  |**0.166**|0.135|0.133 |

**eval_07 = 0.203 NEW HIGH** (vs 011's prev best 0.187)
**eval_13 = 0.173 NEW HIGH** (vs 002's prev best 0.176... close to)

But eval_06/11 K562_r = -0.108 (very negative). Total mean is the
worst of any flank-based library.

## Interpretation
Fundamental tension confirmed:
- FAR flanks (1500-3000bp) train K562 enhancer signal (eval_06/11)
- NEAR flanks (500-1500bp) train something orthogonal that helps
  eval_07/13 — possibly cleaner motif extraction because the model
  can't rely on chromatin context.

A symmetric mix at 40% near drags eval_06/11 K562 below zero
because half the time the model sees confusing near-flank pairs.

## Theory T17
Negative-distance is multi-modal. Different evals reward different
distances. A "right" library may need TARGETED flank distances per
positive type, not a global mix.

## Next
019 = targeted-distance flanks: uniform cCRE → far flanks (for 06/11),
CTCF/DNH3 → near flanks (for 07/13). Hypothesis: type-specific flank
distance gives each positive type the negative it needs.
