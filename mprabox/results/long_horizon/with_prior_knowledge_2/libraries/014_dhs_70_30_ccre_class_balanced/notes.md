# 014_dhs_70_30_ccre_class_balanced

## What I tested
First experiment with the ratio LOCKED at 70/30 (the 011 winner)
and a NEW orthogonal lever introduced: enforce equal counts of
{PLS, pELS, dELS} ENCODE cCRE classes inside the signal-weighted
half. Tests whether regulatory-class balance is an information-
orthogonal axis to mean_signal+numsamples.

## Result — orthogonal but unfavorable
| metric   | 014    | 011    | Δ vs 011 | direction |
|----------|--------|--------|----------|-----------|
| eval_01  | 0.7280 | 0.7383 | -0.010   | down      |
| eval_04  | 0.8048 | 0.7988 | +0.006   | UP        |
| eval_07  | 0.7334 | 0.7751 | **-0.042** | DOWN      |
| eval_08  | 0.7115 | 0.7041 | +0.007   | UP        |
| eval_09  | 0.8766 | 0.8702 | +0.006   | UP        |
| eval_13  | 0.7155 | 0.7644 | **-0.049** | DOWN      |
| cross-14 | 0.7676 | 0.7811 | -0.014   | down      |

Per-seed eval_01: 0.7269 / 0.7285 / 0.7287 (std ≈ 0.001 — even
tighter than 011's 0.002). The signal is REAL, not noise.

## Why this matters
The clean per-seed reproducibility (std 0.001) confirms that
cCRE-class balancing is a true orthogonal lever — not a correlated
re-encoding of mean_signal+numsamples information. It produces
deterministic, predictable changes in the trained model.

But the changes split: gains on {eval_04, eval_08, eval_09} and big
losses on {eval_07, eval_13}. The losers are likely cell-type-
specific evals; the winners look like input-coverage / out-of-
distribution / chromatin-state-broad evals.

## Mechanistic interpretation
Forcing 11,667 elements per cCRE class:
- PLS pool is only 56K elements → drawing 21% of it pulls in much
  lower-signal promoters than the natural draw would include.
- dELS pool is 972K → 11.7K is 1.2% of it, only the highest-signal
  enhancers get included. Natural 70/30 would draw ~25K dELS at the
  top of the signal distribution; class balance cuts that in half.
- pELS pool is 217K → 5.4%, mid-signal range.

Net: we lose the strong top-of-distribution dELS elements that
carry cell-type-specific enhancer grammar (eval_07/13 collapse).
We gain promoter-grammar coverage which helps the diversity-
sensitive evals (eval_04/08/09 rise).

## Theory update — v12 → v13
> cCRE-class composition is a true orthogonal axis to
> mean_signal+numsamples (per-seed std drops to 0.001 when both
> are controlled). It produces predictable, reproducible behavioral
> changes in the model. But on cross-14 the trade is unfavorable:
> the model pays more in lost cell-type-specific enhancer signal
> than it gains in promoter-grammar diversity.
>
> Implication: orthogonal levers are not automatically good. Each
> lever has a trade vector across the 14 evals. The librarian's job
> is to find a lever whose trade is net-positive on cross-14 — or
> to combine levers whose trades partially cancel out the wrong-
> direction parts and reinforce the right-direction parts.
>
> Stability lesson: locking the ratio (70/30) preserved the tight
> 011 basin even with a major composition change. So follow-up
> experiments can vary OTHER levers without losing the variance
> control we worked hard to find.

## Next
- 015: GC-content stratified sampling at 70/30. Hypothesis: eval_08
  prefers libraries with GC-diverse sequences (random sequences
  tend to be GC-balanced). If GC-balanced lifts eval_08 without
  hurting eval_07/13, it's a directly useful axis. If it doesn't
  lift eval_08, the 014 eval_08 gain came from something class-
  specific (CpG islands, promoter motifs) rather than GC.
