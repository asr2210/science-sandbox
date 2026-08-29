# Experiment 004 — Noise-floor control (random uniform, seed 99)

## What I tested
Same as exp 001 but seed=99. Pure control.

## Result
eval_01: 0.3222 (exp 001 was 0.3308). Diff = 0.0086.
Across all evals, seed-to-seed noise is roughly ±0.01-0.02.

## Interpretation
- Noise floor: ~0.01 on eval_01.
- The exp 002 drop (0.331→0.278 = 0.053) is ~5× the noise floor → REAL.
- The exp 003 drop (0.331→0.267 = 0.064) is ~7× the noise floor → REAL.
- The exp 007/exp 008 differences across seeds (~0.02) suggest some evals are noisier than others.

## Standings
eval_01: 001 (0.331) > 004 (0.322) > 002 (0.278) > 003 (0.267)
Random uniform is still the best library by a clear margin.

## Next
Exp 005: Generate seqs from a 1st-order Markov model with approximate human dinucleotide frequencies (CpG-depleted). Tests whether the scorers were trained on natural DNA and reward real-looking sequences.
