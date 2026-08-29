# Experiment 010 — noise estimate: re-seed of 4-way mix

## Design
Exact copy of exp 002 (20K nat + 15K cCRE + 10K DHS + 5K mouse)
with SEED=1 instead of SEED=0. Tests sampling noise.

## Result
- eval_01: 0.3961 (vs exp 002 at 0.3937)
- K562: 0.6056, HepG2: 0.4326, SK-N-SH: 0.1500
- Same eval_14: 0.3961 (vs 0.3937), eval_13: 0.4106 (vs 0.4090)

## Sampling noise estimate
Δ across the 14 evals between exp 002 (seed=0) and exp 010 (seed=1):
- eval_01: +0.0024, eval_02: +0.0023, eval_03: +0.0022,
  eval_04: +0.0018, eval_05: +0.0023, eval_06: +0.0022,
  eval_07: +0.0003, eval_08: +0.0002, eval_09: +0.0018,
  eval_10: -0.0002, eval_11: +0.0022, eval_12: +0.0022,
  eval_13: +0.0016, eval_14: +0.0024

|Δ| ≈ 0.002, with a sign bias (seed=1 happens to score higher
on most evals). Noise floor for a single seed swap of same design
is **σ ≈ 0.002** with possible **systematic bias of ±0.002** per
seed.

## Signal vs noise
- nat baseline (exp 001): eval_01=0.3876
- 4-way mix seed=0 (exp 002): eval_01=0.3937 (Δ +0.0061 over nat)
- 4-way mix seed=1 (exp 010): eval_01=0.3961 (Δ +0.0085 over nat)
- Lift is **2-4x noise floor** → real signal.

## Updated ceiling
Apparent ceiling is **~0.395 ± 0.002**, not 0.394. With seed
variance the best designs may peak at 0.396-0.398. Still ~0.005
below the apparent eval_01 max (eval_13 hits 0.41).

## Library design dynamic range, revised
v07 floor: 0.369 (random uniform)
v07 ceiling: ~0.396 (best mix, ± noise)
v07 dynamic range: ~0.027

## Implications for exp 011+
- Single-seed eval_01 differences <0.003 are not interpretable
- Need to test materially different designs (motif density, GWAS,
  PWM-curated) and look for differences ≥0.005
- The remaining 0.004 gap from 0.396 to ~0.40 is the territory I
  should target
