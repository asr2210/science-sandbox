# 003 — cCRE class-balanced (40K) + random GENOMIC windows (10K)

## Result
| metric  | 003 | 002 (+iid) | 001 (cCRE only) | dhs_topic | Δ(003-002) |
|---------|-----|------------|------------------|-----------|------------|
| eval_01 | **0.7301** | 0.7278 | 0.7262 | 0.7232 | +0.0023 |
| eval_02 | **0.8218** | 0.8194 | 0.8190 | 0.8138 | +0.0024 |
| eval_03 | **0.8046** | 0.8003 | 0.8005 | 0.7933 | +0.0043 |
| eval_04 | 0.7910     | 0.7888 | 0.7935 | 0.7904 | +0.0022 |
| eval_05 | **0.7300** | 0.7276 | 0.7259 | 0.7230 | +0.0024 |
| eval_06 | **0.8220** | 0.8194 | 0.8191 | 0.8136 | +0.0026 |
| eval_07 | **0.7620** | 0.7466 | 0.7467 | 0.7398 | **+0.0154** |
| eval_08 | 0.6755     | **0.7149** | 0.6849 | 0.7011 | **−0.0394** |
| eval_09 | 0.8616     | 0.8570 | 0.8634 | 0.8601 | +0.0046 |
| eval_10 | 0.7777     | 0.7830 | 0.7818 | 0.7904 | −0.0053 |
| eval_11 | **0.7171** | 0.7147 | 0.7132 | 0.7098 | +0.0024 |
| eval_12 | **0.6925** | 0.6891 | 0.6890 | 0.6822 | +0.0034 |
| eval_13 | **0.7541** | 0.7330 | 0.7360 | 0.7271 | **+0.0211** |
| eval_14 | **0.8220** | 0.8198 | 0.8194 | 0.8144 | +0.0022 |

Mean across 14: **0.7690** (003) > 0.7672 (002) > 0.7656 (001) > 0.7644 (dhs_topic).
Wins on 12/14 vs 002. Wall: 1249 s.

## Per-seed eval_01
- seed 0: 0.7639 (highest single-seed result so far)
- seed 1: 0.6923 (low outlier — seed 1 has been tricky)
- seed 2: 0.7340

Spread = 0.072. Largest spread of any experiment yet. Worth investigating
whether seed-1's specific (chrom, mid) draws hit a degenerate region.

## Pre-registered prediction scorecard
- A (mechanism = sequence-space coverage; 003 ≈ 002): **partly correct** — true
  for most evals, but spectacularly false for eval_08.
- B (mechanism = iid random calibrates eval_08 specifically): **strongly
  correct** — eval_08 dropped −0.039 vs 002, almost back to 001.
- C (realistic genomic composition adds signal vs cCRE on eval_01): **mildly
  correct** — eval_01 + 0.0023, marginal but consistent with more
  modest-magnitude lifts on eval_02/03/05/06.

## What I learned
1. **iid random and random genomic are NOT interchangeable.** They help
   distinct eval sets, with very different mechanisms presumably.
2. **eval_08 specifically wants iid random in the training distribution.**
   This is consistent with the baseline-table observation that synth_oracle
   wins eval_08 outright (0.7696). My working hypothesis: eval_08 is held-out
   on iid-random / synthetic sequences with oracle labels — so a model
   trained on a library that contains iid random gets distribution-matched on
   the eval set, while a model trained on only-genomic sequences extrapolates.
   This is "calibration to the eval distribution" not pure "generalization".
3. **Random genomic windows broadly improve genomic-context evals.** eval_07
   (+0.015) and eval_13 (+0.021) are the biggest movers, plus small gains
   on eval_02/03/05/06/14. The genomic component teaches the model what
   non-cCRE genomic background looks like, which the model evidently uses
   when scoring genomic-context held-out sequences.
4. **eval_01 keeps creeping up.** 0.7232 → 0.7262 → 0.7278 → 0.7301 across
   dhs_topic / 001 / 002 / 003. The trajectory suggests that *both* random
   sources are contributing positively to the primary metric, just by
   different amounts.

## Theory update
Refined working theory:
> Library informativeness for cross-cell-type generalization is the SUM of two
> independent sources: (i) coverage of regulatory grammar categories that
> recur across cell types (cCRE class-balanced sampling drives this), and
> (ii) coverage of the broader sequence-space the model will be evaluated on
> (subdivided into "genomic background" — helps real-world held-out genomic
> sequences — and "iid random" — helps held-out random sequences). The two
> sub-sources of (ii) appear additive and target different eval distributions.

## Best next experiment
Combine all three sources: 40K cCRE class-balanced + 5K iid random + 5K random
genomic. If the eval_08 lift (002) and eval_07/13 lifts (003) are independent
and additive, this should win on most evals. If they trade off, we learn
that the two random components share an underlying mechanism that doesn't
scale.
