# Skill: measure seed-noise floor early

## Why
A black-box scorer + stochastic library generator can have *much* larger seed
variance than intuition suggests. In this run, identical PWM-sampled config
gave eval_01 = {0.3106, 0.3398, 0.3644} across 3 seeds — a ~0.05 swing on a
50k-sequence library. Most small algorithmic deltas land within this band
and are indistinguishable from noise.

## What to do
After finding a baseline (a config that scores noticeably above pure
random), spend 2 experiments **immediately** reseeding it with different
RNG seeds. Measure noise floor empirically before trusting any improvement
to a sub-noise-floor delta.

## How to apply
- If your improvement is within ±2× the seed-noise std, treat it as noise
  and don't update theory.
- If you have a single "best" run, suspect it may be at the lucky tail.
  Reseed once before claiming a real lever.
- Budget seed-search experiments: if noise is 0.05 wide, a 6-seed grid will
  occasionally produce a +0.05 lucky draw worth keeping.

## Concrete numbers (exp 010 config)
17 JASPAR TFs × 3 motifs/seq × random scaffold × PWM-sampled, 50k seqs:
- seed 20260610: 0.3644
- seed 99:       0.3398
- seed 424242:   0.3106
- mean ± std: 0.338 ± 0.022
