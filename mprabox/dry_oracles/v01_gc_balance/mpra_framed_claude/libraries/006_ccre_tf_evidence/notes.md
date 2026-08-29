# 006_ccre_tf_evidence

## Setup
50k cCREs filtered to TF-evidence types only: PLS (12k), pELS (18k), TF (14k),
CA-TF (6k). Drops dELS distal enhancers, plain CA, CA-CTCF, CA-H3K4me3.

## Result vs exp 002 (full stratified)
| Eval        | 002    | 006    | Δ        |
|-------------|--------|--------|----------|
| eval_01     | 0.6921 | 0.6907 | −0.001   |
| eval_03     | 0.6992 | 0.6969 | −0.002   |
| eval_04/09  | 0.5977 | 0.6298 | **+0.032** |
| eval_07     | 0.7562 | 0.7416 | −0.015   |
| eval_08     | 0.1248 | 0.1247 |  0.000   |
| eval_10     | 0.6673 | 0.6505 | −0.017   |
| eval_13     | 0.7466 | 0.7308 | −0.016   |

## Interpretation
- Dropping dELS / CA-only types modestly *hurts* the strongest motif evals
  (07, 10, 13) but *helps* the baseline-type evals (04, 09).
- Net: roughly even on eval_01. The dropped types contain useful
  regulatory signal even though they have less direct TF evidence.
- eval_04 / 09 prefer libraries with **less motif concentration**. Their
  improvement when TF-evidence-only doesn't include the very-motif-heavy
  dELS pool is a small confirmation that they reward baseline calibration.

## Theory update
All cCRE types contribute signal. Filtering for TF-evidence types is not a
free win. To push eval_01 past ~0.69 I need new data, not better cCRE
filtering. Next: try DHS index for broader regulatory coverage.
