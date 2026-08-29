# 020 — symmetric structural-heavy rebalance (5K PLS + 5K pELS + 5K dELS + 10K CTCF + 10K DNase) + 5K iid + 5K human + 5K chicken

## Result — bowl is asymmetric, structural-heavy hurts ~2× more than functional-heavy
| metric  | 020 | 010 | 019 | Δ vs 010 | Δ vs 019 |
|---------|-----|-----|-----|----------|----------|
| eval_01 | 0.7331 | **0.7599** | 0.7467 | −0.0268 | −0.0136 |
| eval_02 | 0.8273 | **0.8550** | 0.8414 | −0.0277 | −0.0141 |
| eval_03 | 0.8119 | **0.8413** | 0.8250 | −0.0294 | −0.0131 |
| eval_04 | 0.7881 | **0.8140** | 0.8065 | −0.0259 | −0.0184 |
| eval_05 | 0.7330 | **0.7599** | 0.7469 | −0.0269 | −0.0139 |
| eval_06 | 0.8275 | **0.8550** | 0.8415 | −0.0275 | −0.0140 |
| eval_07 | 0.7737 | **0.8044** | 0.7784 | −0.0307 | −0.0047 |
| eval_08 | 0.7028 | **0.7515** | 0.7227 | −0.0487 | −0.0199 |
| eval_09 | 0.8559 | **0.8872** | 0.8782 | −0.0313 | −0.0223 |
| eval_10 | 0.7917 | **0.8233** | 0.8029 | −0.0316 | −0.0112 |
| eval_11 | 0.7202 | **0.7464** | 0.7337 | −0.0262 | −0.0135 |
| eval_12 | 0.6977 | **0.7244** | 0.7093 | −0.0267 | −0.0116 |
| eval_13 | 0.7693 | **0.8016** | 0.7738 | −0.0323 | −0.0045 |
| eval_14 | 0.8273 | **0.8551** | 0.8415 | −0.0278 | −0.0142 |

Mean 14: **0.7757** vs 010=0.8056 (Δ=−0.0299) and 019=0.7892 (Δ=−0.0135).
Wall: 935 s (intermediate — between 018's 546s catastrophic and
019/010's normal 1300s; consistent with moderate library degradation).

## Per-seed eval_01
- seed 0: 0.7410
- seed 1: 0.7291
- seed 2: 0.7292
Spread = 0.012, tight. Result is reproducible.

## Pre-registered scorecard
- "020 ≈ 019 (within ±0.005, both ≈ 0.789): bowl is symmetric":
  **falsified** (Δ=−0.0135 vs 019, well outside ±0.005).
- "020 ≈ 010 (structural under-weighted)": **falsified** (Δ=−0.030).
- "020 < 019 (loss > 0.020 vs 010): functional more load-bearing":
  **confirmed** (loss = 0.030 vs 010 vs 019's 0.016).
- "020 > 019 (loss < 0.010 vs 010): structural under-weighted":
  **falsified**.

## Quantitative bowl model (functional shift = total functional mass − 21K)
Three points along the functional/structural axis:
- 020: shift = −6K, cost = 0.030
- 010: shift = 0K, cost = 0
- 019: shift = +6K, cost = 0.016

Fit a parabola cost(x) = a(x − c)²:
- (6 − c)² · a = 0.016
- (−6 − c)² · a = 0.030
- Ratio: (6 − c)² / (6 + c)² = 0.533 → (6 − c)/(6 + c) = 0.730
- Solve: c ≈ 0.94K, a ≈ 6.3e-4 per K²

So the **true class-balance optimum is at ~+1K functional shift from 7K-each** (essentially 010 itself: 7.25K each functional, 6.6K each structural would be the predicted optimum). The cost function is shallow near 010 — predicted improvement at the optimum vs 010 is only ~0.0006, well below seed noise (~0.012).

**Implication: 010's 7K-each balance is essentially optimal.** Further class-balance perturbation experiments are not productive — the cost function is nearly flat in a ~±1K window around 7K-each.

## Theory update — class balance bowl is asymmetric and shallow at the bottom
**Refined theory (v4).**
> cCRE backbone class balance follows an asymmetric bowl around
> 7K-each. The bottom is broad (∼flat within ±1K of optimum). Pulling
> mass AWAY from functional classes (PLS/pELS/dELS) hurts ~2× more
> per K than pulling mass away from structural classes (CTCF-only,
> DNase-H3K4me3). The optimum is at ~7-8K-each functional + ~6-6.5K-
> each structural. 010's 7K-each is within 0.001 of optimum.

**Per-element value (rough estimate, marginal contribution at 7K-each):**
- Functional class element: ~0.001 mean per K
- Structural class element: ~0.0005 mean per K
- (Both contribute, but functional ~2× more per element.)

## What I learned (operational)
1. **Asymmetric bowls are common.** When testing class balance, always
   test BOTH directions of perturbation. The asymmetry was not
   predicted by 018+019 alone — it required 020 to confirm.
2. **Quantitative parabola fit gives a useful pseudo-optimum estimate.**
   Three points (010 + 019 + 020) plus quadratic assumption produces
   a closed-form prediction of the true optimum. The estimate (~7-8K
   functional + ~6-6.5K structural) is within 1K of 010's 7K-each.
3. **The flat-bottom region implies further class-balance experiments
   are exhausted.** Predicted improvement from sub-1K shifts (~0.0006)
   is below seed noise (0.012 on eval_01). Move to other axes.
4. **Wall time 935s correlates with moderate impairment.** Continuing
   the pattern: 546s = catastrophic, 935s = moderate, 1300s = healthy.
   Useful pre-eval signal.

## What to try next
**021: iid composition test.** Replace 5K pure-uniform iid with 5K
hg38-mononucleotide-matched iid (still iid by position, but matched
mononuc frequencies — ~29% A, 21% C, 21% G, 29% T from hg38). Library:
35K cCRE 7K-each + 5K hg38-iid + 5K human-gen + 5K chicken = 50K.

This is a pure iid sub-axis structure probe. Iid is the second-most-
critical component (after cCRE) at value ~+0.05; we've never asked
WHAT about iid is critical — uniform-by-position randomness, off-genome
calibration, low information content, or composition mismatch.

Pre-registered:
- 021 ≈ 010 within ±0.005: composition doesn't matter for iid value.
  Iid value is "uniform-by-position randomness" or "low information
  anchor" — composition-agnostic.
- 021 > 010 by +0.005-0.015: hg38-matched iid is BETTER. Iid value
  partly comes from genome-composition matching (closer-to-realistic
  noise distribution helps the model calibrate sequence likelihood).
- 021 < 010 by 0.005-0.020: hg38-matched iid is WORSE. Iid value
  comes specifically from "uniform" character — distinctively
  off-genome composition is what helps the model calibrate the
  sequence-vs-no-sequence boundary.
- 021 << 010 by > 0.030: hg38-matched iid is much worse. Iid acts as
  the "very obvious off-genome anchor" — making it look like genome
  removes its anchoring power.

Alternatives considered:
- **Iid mass curvature (7.5K iid)**: probes iid magnitude, but
  requires reducing cCRE below 35K (which we know hurts). Confounded
  axes — lower information.
- **CTCF-bound qualifier sub-structure within cCRE**: there's a hidden
  axis (PLS-CTCF-bound vs PLS, pELS-CTCF-bound vs pELS, etc.). Worth
  testing eventually but lower priority — we just established cCRE
  class balance is solved.
- **Replace human-gen with novel category**: human-gen value is only
  ~+0.005 (modest). Could replace, but no obvious high-value untested
  category (chicken cCRE annotations not available; cross-species
  cap rules out adding more species; hard negatives ruled out).

iid composition is the cleanest unexplored axis. Going with 021.
