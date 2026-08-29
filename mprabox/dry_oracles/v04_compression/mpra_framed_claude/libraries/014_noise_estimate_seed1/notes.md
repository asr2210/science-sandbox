# 014_noise_estimate_seed1 — notes

## Design
Same as exp 011 (20K nat + 15K cCRE off + 10K DHS + 5K mouse) but SEED=1.

## Result
- eval_01 = 0.4971 (vs exp 011 = 0.5012, Δ = -0.0041)
- All evals within ~0.005 of exp 011:
  - eval_03: 0.5373 vs 0.5377 (Δ -0.0004)
  - eval_07: 0.5920 vs 0.5946 (Δ -0.0026)
  - eval_13: 0.5911 vs 0.5946 (Δ -0.0035)
  - eval_08: 0.0980 vs 0.0953 (Δ +0.0027)
- Time: 26s (matches exp 011 timing)

## Noise floor
**Re-running the same library design with a different seed produces
±0.004 on eval_01.** So differences ≤0.005 between experiments are noise.

This re-interprets recent results:
- exp 011 (0.5012), 012 (0.4979), 013 (0.4990), 014 (0.4971) are
  STATISTICALLY INDISTINGUISHABLE.
- The 4-source mix design is near-optimal in this neighborhood.
- Diminishing-returns interpretation for 012/013 was overconfident; they
  may just have been seed luck the other direction.

## Implication for next experiments
- Stop testing micro-rebalances within the 4-source family.
- Only believe results that move eval_01 by ≥0.008.
- Pursue genuinely new sequence sources/modalities that could push beyond
  the noise band.

## Best library so far
exp 011 design is the best, but exp 014 says its 0.5012 is "0.498 ± 0.004".
The TRUE plateau is around 0.499.

## Next test
TF ChIP peaks. In vivo TF-bound regions (TF + chromatin + co-factor signal
together) — a different signal modality than open chromatin alone.
