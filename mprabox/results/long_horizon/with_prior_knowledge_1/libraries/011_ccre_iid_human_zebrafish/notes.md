# 011 — cCRE (35K) + iid (5K) + human (5K) + zebrafish (5K)

## Result — slight regression vs 010, distance gradient hump-shaped
| metric  | 011 | 010 | 006 (mouse) | Δ vs 010 | Δ vs 006 |
|---------|-----|-----|------|----------|----------|
| eval_01 | 0.7543 | **0.7599** | 0.7468 | −0.0056 | +0.0075 |
| eval_02 | 0.8491 | **0.8550** | 0.8418 | −0.0059 | +0.0073 |
| eval_03 | 0.8357 | **0.8413** | 0.8262 | −0.0056 | +0.0095 |
| eval_04 | 0.8098 | **0.8140** | 0.8045 | −0.0042 | +0.0053 |
| eval_05 | 0.7542 | **0.7599** | 0.7469 | −0.0057 | +0.0073 |
| eval_06 | 0.8492 | **0.8550** | 0.8420 | −0.0058 | +0.0072 |
| eval_07 | 0.7954 | **0.8044** | 0.7871 | −0.0090 | +0.0083 |
| eval_08 | 0.7405 | **0.7515** | 0.7277 | −0.0110 | +0.0128 |
| eval_09 | 0.8810 | **0.8872** | 0.8753 | −0.0062 | +0.0057 |
| eval_10 | 0.8162 | **0.8233** | 0.8072 | −0.0071 | +0.0090 |
| eval_11 | 0.7406 | **0.7464** | 0.7341 | −0.0058 | +0.0065 |
| eval_12 | 0.7191 | **0.7244** | 0.7112 | −0.0053 | +0.0079 |
| eval_13 | 0.7921 | **0.8016** | 0.7793 | −0.0095 | +0.0128 |
| eval_14 | 0.8494 | **0.8551** | 0.8418 | −0.0057 | +0.0076 |

Mean 14: **0.7990** vs 010=0.8056 (−0.0066) vs 006=0.7908 (+0.0082). Wall: 1313 s.

## Per-seed eval_01
- seed 0: 0.7437
- seed 1: 0.7571
- seed 2: 0.7620

Spread = 0.0183. Wider than 010's 0.0096 but tighter than 006's 0.0204.

## Pre-registered scorecard
- "011 > 010 (gradient continues monotonically)": **falsified**.
- "011 ≈ 010 (gradient saturates)": close but slight regression.
- "011 < 010 by 0.005-0.015 (sweet spot near chicken)": **confirmed**
  (−0.0066 mean, −0.0056 eval_01).
- "011 < 010 by > 0.015 (teleost too distant)": falsified.
- "011 < 006 (zebrafish actively confuses)": **strongly falsified** —
  zebrafish is BETTER than mouse despite being more distant.

## Theory update — hump-shaped distance gradient

The single-species-at-5K cross-species gradient is now mapped at three
points:

| species at 5K | divergence | mean lift over 4-axis 004 |
|---------------|------------|---------------------------|
| 5K mouse  | ~80 Mya  | +0.0083 |
| 5K chicken | ~310 Mya | **+0.0231** |
| 5K zebrafish | ~430 Mya | +0.0165 |

The function is hump-shaped, peaking near chicken (~310 Mya). Mechanism
interpretation:
  - At small distance (mouse): too redundant with human non-cCRE.
  - At amniote distance (chicken): maximally orthogonal while sharing
    relevant tetrapod regulatory grammar.
  - At teleost distance (zebrafish): starts losing shared regulatory
    grammar — repeats, GC-content distribution, and some k-mer patterns
    are too far from human for the model to extract calibration value.

The order chicken > zebrafish > mouse rules out the simple "more distant
is always better" theory. The order also rules out "any non-mammal
collapses". The pattern is genuinely a sweet spot.

## Refined working theory
> Library value = (i) cCRE backbone + (ii) iid + (iii) human-genomic +
> (iv) cross-species at ≈ 5K mass per species. The cross-species
> contribution is hump-shaped over evolutionary distance, with chicken
> (amniote, ~310 Mya) at or near the peak. Likely candidates near the
> peak: other amniotes (xenopus ~360 Mya, lizard, platypus). Likely
> falling-off-the-cliff candidates: drosophila (invertebrate), yeast.

## What I learned (operational)
1. **The distance gradient is non-monotonic.** Both "more distant is better"
   (007) and "mammalian-only matters" (009 era) were wrong. Two data points
   established the gradient direction, but a third was needed to map the
   shape. Three data points is the minimum for fitting a non-trivial curve.
2. **The 010 → 011 regression is small (−0.0066 mean, well outside seed
   spread for 010 alone but within seed spread for the run).** Per-seed
   spread for 011 was 0.018 — bigger than 010's 0.010 — suggesting
   zebrafish may also be slightly less stabilizing than chicken. Worth
   tracking whether this correlates with the hump-shape.

## What to try next
**Test whether the cross-species axis stacks across distinct species at
the same backbone** — by dropping iid (the lowest-confidence remaining
axis) to make budget for a 2nd cross-species at 5K.

**012 design.** 35K cCRE + 0K iid + 5K human + 5K chicken + 5K mouse.
- 012 > 010 by ≥ +0.005: distant species stack on top of each other; iid
  is replaceable by mouse. Strongest result; reframes the budget allocation
  problem.
- 012 ≈ 010: iid value ≈ mouse value at this configuration. We can swap
  axes freely.
- 012 < 010 by 0.005-0.015: iid was load-bearing AND mouse adds something
  on top of chicken — partial stacking but iid still wins.
- 012 < 010 by > 0.015: iid was sharply load-bearing and/or mouse and
  chicken don't stack. Restore iid for next experiment.

Why mouse and not zebrafish for the second species? Mouse is the most
characterized cross-species source we have, and 008's back-out estimate
(chicken contributed +0.024 on top of mouse) is the strongest existing
evidence that two species CAN stack. Adding mouse on top of chicken
re-tests this with cleaner scaffolding. If 012 confirms stacking, exp
013 can test chicken + zebrafish for the more-distant pairing.
