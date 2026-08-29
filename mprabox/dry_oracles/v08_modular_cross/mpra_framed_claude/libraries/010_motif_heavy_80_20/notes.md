# Experiment 010 — 80/20 dense motifs + TSS promoters

## Result
- eval_08: mean=0.0062, SKNSH=0.0107 (huge SKNSH win on this eval!)
- eval_07: -0.0022 (was 0.0088 in 009 — collapsed)
- eval_03/12: -0.0037 (worse)
- Mean across 14 evals ≈ 0.001 (worse than 009's 0.003)

## Interpretation
- Different mix ratios "activate" different evals. 80/20 boosted
  eval_08 (with strong SKNSH signal) but lost eval_07.
- The signal-to-noise per individual experiment is small enough that
  ratio differences create big swings in which evals light up.
- There may be no single optimal ratio — the right answer is a
  library that hits multiple eval types simultaneously.

## What this tells me
The "ratio-tuning" approach has reached diminishing / chaotic returns.
Next: add a third sequence type (PLS cCREs — most active class of
real regulatory elements) to broaden coverage.

The fact that eval_08 SKNSH=0.0107 here vs 0.0047 in exp 006 suggests
that adding the right kind of sequence (likely strong promoter +
motif-loaded content) can drive SKNSH signal much higher.
