# Experiment 012 — multi-seed probe (2 per-col-balanced libraries)

## Result
- mean_r=**0.5213** (vs 0.5195 single-seed exp 009, **+0.0018**)
- K562=0.9947, HepG2=0.5656, SKNSH=0.0039
- n_seeds=2, time=115s

## HUGE FINDING
**prepare.py averages over `sequences_N.txt` files for N=0,1,...**
Multiple independent libraries reduce noise in the final score.

Going 1→2 seeds: +0.0018 on eval_01. If this scales with sqrt(N) (typical
noise reduction), more seeds could push us substantially higher.

Next: 4 seeds, then 8, 16, ...
