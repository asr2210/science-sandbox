# 002_dhs_breadth_weighted

## What I tested
Identical pipeline to 001 but the sampling weight is `numsamples` (number
of biosamples in which the DHS element is accessible, range 1–733),
NOT `mean_signal`. Tests whether broadly-accessible elements teach the
model regulatory grammar that transfers across cell types.

## Result
- **eval_01 mean_r = 0.7152** (vs 001's 0.7242, Δ = -0.009)
- **Cross-14 mean = 0.7534** (vs 001's 0.7511, Δ = +0.002)
- Per-seed eval_01: 0.7173 / 0.7167 / 0.7115 — std ≈ 0.003
  (much tighter than 001's std ≈ 0.025)
- Time: 962s

## Per-eval shifts vs 001 (Δ = 002 − 001)
| eval | 002    | 001    | Δ      | note |
|------|--------|--------|--------|------|
| 01   | 0.7152 | 0.7242 | -0.009 | small loss |
| 04   | 0.7891 | 0.7819 | +0.007 |  |
| 07   | 0.7238 | 0.7611 | -0.037 | **big loss** |
| 08   | 0.6908 | 0.6781 | +0.013 | help |
| 09   | 0.8582 | 0.8496 | +0.009 | help |
| 13   | 0.7004 | 0.7564 | -0.056 | **big loss** |

## Takeaways
1. **Breadth is not a free win.** Pure numsamples-weighting trades cell-type
   discrimination for invariance. Loses 0.04–0.06 on eval_07 and eval_13,
   gains 0.01 on eval_04/08/09.
2. **Per-seed variance collapsed** (0.025 → 0.003). Broad-access weighting
   draws from a much smaller effective set: the numsamples distribution is
   heavily skewed (median=3, p99=365, max=733). With ns-weighting, ~17%
   of weight lands on the "Stromal A" component (only 1.6% of elements,
   median ns=116). The library is therefore much more redundant.
3. **eval_07 and eval_13 reward cell-type-specific elements.** From the
   baseline tables they were also the strongest beneficiaries of
   `dhs_sei` over `dhs_random` — chromatin-state specificity helps these.
4. **eval_08 still trails baseline** (0.69 vs ~0.77 for synth-containing
   strategies). Broad accessibility ≠ random-sequence coverage. Two
   different problems.

## What this updates in my theory
A library is informative when it spans **two orthogonal axes**:
   (a) cell-type-specific regulatory signal (high mean_signal, low
       numsamples — sharp motif discrimination, evals 07/13 reward this)
   (b) cell-type-invariant grammar (high numsamples — transferable
       regulatory programs, evals 04/08/09 reward this)
Pure (a) = experiment 001, pure (b) = experiment 002. Both leave 0.01–0.06
on the table for at least some eval set. Next: combine.
