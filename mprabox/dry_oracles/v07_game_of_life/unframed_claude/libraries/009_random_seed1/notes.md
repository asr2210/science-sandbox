# 009_random_seed1

## Hypothesis
Random uniform i.i.d. with seed=1 should give nearly the same r as the seed=42 baseline. With 50,000 sequences, the law of large numbers should average out the specific bases chosen. Tight spread (<0.001) confirms my earlier 0.005 differences across libraries are real, not seed noise.

## Method
Same generator as 001 but with seed=1.

## Result
- **eval_01 mean_r = 0.3973** (vs 0.3981 for seed=42)
- Difference: **0.0008** — well within "noise" and confirms reproducibility.

## Interpretation
The library-resampling noise floor for random uniform is ~0.001 in eval_01. So:
- Random uniform's "true" score is ~0.397-0.398.
- The ~0.005 gap to chr22/cCRE (002, 003) is a real library effect, not noise.
- The bigger gaps (0.013-0.058 for motifs, runs, GC variants) are *very* real.

Random uniform appears to sit on a remarkably narrow plateau. Anything more elaborate than random uniform i.i.d. either matches or loses.

## Next
- 010: Test the *other* side of "naturalness" — first-order Markov chain with mildly higher P(repeat)=0.30. If it scores above random uniform, longer-run statistics are favored. If lower or equal, random uniform i.i.d. really is at the top.
