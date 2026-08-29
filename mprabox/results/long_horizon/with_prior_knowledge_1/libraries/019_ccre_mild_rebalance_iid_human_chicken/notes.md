# 019 — cCRE mild rebalance (9K PLS + 9K pELS + 9K dELS + 4K CTCF + 4K DNase) + 5K iid + 5K human + 5K chicken

## Result — between 010 and 018, decomposition is clean
| metric  | 019 | 010 | 018 | Δ vs 010 | Δ vs 018 |
|---------|-----|-----|-----|----------|----------|
| eval_01 | 0.7467 | **0.7599** | 0.6989 | −0.0132 | +0.0478 |
| eval_02 | 0.8414 | **0.8550** | 0.7881 | −0.0136 | +0.0533 |
| eval_03 | 0.8250 | **0.8413** | 0.7671 | −0.0163 | +0.0579 |
| eval_04 | 0.8065 | **0.8140** | 0.7703 | −0.0075 | +0.0362 |
| eval_05 | 0.7469 | **0.7599** | 0.6988 | −0.0130 | +0.0481 |
| eval_06 | 0.8415 | **0.8550** | 0.7882 | −0.0135 | +0.0533 |
| eval_07 | 0.7784 | **0.8044** | 0.6992 | −0.0260 | +0.0792 |
| eval_08 | 0.7227 | **0.7515** | 0.6409 | −0.0288 | +0.0818 |
| eval_09 | 0.8782 | **0.8872** | 0.8358 | −0.0090 | +0.0424 |
| eval_10 | 0.8029 | **0.8233** | 0.7398 | −0.0204 | +0.0631 |
| eval_11 | 0.7337 | **0.7464** | 0.6863 | −0.0127 | +0.0474 |
| eval_12 | 0.7093 | **0.7244** | 0.6606 | −0.0151 | +0.0487 |
| eval_13 | 0.7738 | **0.8016** | 0.6938 | −0.0278 | +0.0800 |
| eval_14 | 0.8415 | **0.8551** | 0.7882 | −0.0136 | +0.0533 |

Mean 14: **0.7892** vs 010=0.8056 (Δ=−0.0164) and 018=0.7326 (Δ=+0.0566).
Wall: 1301 s (back to normal — model converged fully, unlike 018's truncated 546s).

## Per-seed eval_01
- seed 0: 0.7451
- seed 1: 0.7416
- seed 2: 0.7535
Spread = 0.012, tight (typical seed variance for healthy library).

## Pre-registered scorecard
- "019 ≈ 010 within ±0.005 (rebalance is fine when all 5 present)":
  **falsified** (loss = 0.0164 > 0.005).
- "019 between 010 and 018 (loss 0.005-0.060)": **confirmed**
  (loss = 0.0164, comfortably in range).
- "019 ≈ 018 (≈ 0.07 loss; mild rebalance immediately fatal)":
  **falsified** (recovered +0.0566 of the 0.073 catastrophic loss).

## Clean decomposition of 018's −0.073
| component | Δ |
|-----------|------|
| Remove structural classes entirely (4K CTCF + 4K DNase → 0+0) | −0.0566 |
| Mild rebalance from 7K-each toward functional (4K shift each way) | −0.0164 |
| **Sum** | **−0.0730** |
| **018 measured loss** | **−0.0730** |

The sum matches 018's measured regression EXACTLY (to 4 decimals, by
coincidence of independent noise — still strongly suggestive that the
two effects are approximately additive on this metric scale).

## Theory update — class balance is BOTH a step AND a continuous function
- The dominant effect (~78% of 018's loss) is the **step**:
  removing 2 of 5 cCRE classes erases an irreducible chromatin-context
  vocabulary. This is what 018 already established.
- A smaller effect (~22%) is **continuous**: shifting mass within the
  5-class space by ~30% (4K out of ~14K shifted) costs ~0.016. So
  10's 7K-each balance is not just a special "all present" plateau —
  it's near a smooth local optimum, and proportional rebalance has
  proportional cost.
- The two effects are approximately **additive** here, not multiplicative.

## What I learned (operational)
1. **Decomposition by paired experiment works.** 019 isolated the
   "rebalance" cost from the "remove" cost in 018. This is a useful
   pattern — when a multi-axis change has a big effect, design the
   single-axis intermediate to attribute the loss.
2. **The class-balance optimum may be smooth.** The fact that 019 is
   between 010 and 018 (rather than near one extreme) suggests the
   optimum is differentiable, not a sharp ridge. A symmetric
   structural-heavy rebalance (020) will test this.
3. **Training time is not binary signal of quality.** 018 (catastrophic)
   trained in 546s; 019 (modest hurt) trained in 1301s, fully normal.
   Training time only flags when the model gives up early. Mild
   regressions train normally.

## What to try next
**020: symmetric structural-heavy rebalance.** Mirror 019 around 7K-each:
5K PLS + 5K pELS + 5K dELS + 10K CTCF + 10K DNase + 5K iid + 5K human
+ 5K chicken = 50K. Magnitude of deviation from 7K-each is identical
(sum-abs = 12K, sum = 0), but the direction is structural rather than
functional.

Pre-registered:
- 020 ≈ 019 (within ±0.005, both ≈ 0.789): the balance optimum is
  symmetric; only magnitude of deviation from 7K-each matters, not
  direction. Class balance is a smooth bowl around 7K-each.
- 020 ≈ 010 (within ±0.005, ≈ 0.806): structural classes were
  under-weighted in 010; rebalancing toward structural is fine or
  better. Functional classes are NOT the load-bearing ones —
  removing them in matching magnitude doesn't hurt.
- 020 < 019 (loss > 0.020 vs 010): functional classes are
  intrinsically more load-bearing than structural; the 7K-each
  optimum is biased — even small reductions in PLS/pELS/dELS hurt
  more than equal reductions in CTCF/DNase.
- 020 > 019 (loss < 0.010 vs 010): structural classes were the
  under-weighted ones; 7K-each is wrong, the true optimum tilts
  structural-heavy.

This is a high-information experiment because all 4 outcomes have
distinct theoretical implications.

Alternatives considered:
- **iid composition test** (replace pure-uniform iid with hg38
  4-mer-matched random): probes iid axis structure, but lower
  priority — iid value is well-established as critical, exact form
  matters less for further library design.
- **5K mono-shuffled cCRE** (instead of dinuc-shuffled): probes
  whether the 016 negative was about dinuc structure or about hard
  negatives generally. Less informative — already established hard
  negatives hurt, distinction between mono vs dinuc is academic.
- **Iid mass perturbation** (7.5K iid + 32.5K cCRE): jointly perturbs
  two known-important axes and would be hard to interpret cleanly.

Going with 020 — clean symmetric perturbation around the established
optimum is highest information density.
