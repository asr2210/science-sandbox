# 020 dirichlet_0p5_reseed

CRITICAL EXPERIMENT: re-run of Dirichlet(0.5) with seed 997 (was 11 in exp 005).

## Result
eval_01 = **-0.0024** vs exp 005 eval_01 = **+0.0030**.

## Implication: noise floor analysis
The same generative method yields swing of ~0.005 across seeds.
For N=50k sequences, Pearson SE ≈ 1/sqrt(50k) ≈ 0.0045 — matches.

**My "best" library was statistical noise.** None of my methods reliably move
eval_01 beyond ±0.005 noise band.

## Strategy pivot
- Stop fine-tuning Dirichlet alpha — within-method seed noise > between-method effects.
- For final submission, pick a method that's stable and reasonable.
- Acknowledge: scorer's hidden targets do not strongly correlate with any
  distributional property I've explored.
