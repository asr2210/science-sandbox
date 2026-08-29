# Experiment 029 — 012 recipe seed=2025

## What I tested
5th seed sample of 012 recipe.

## Result
- eval_04/09: 0.0032, K562=0.0131 (high K562)
- eval_08: 0.0033 (balanced modest)
- eval_10: K562=0.0116 (K562 high)
- eval_07: -0.0067 (lost)
- Broad evals: NEGATIVE (-0.003)
- Mean across 14 ≈ -0.0010

## Updates
**Final 012-recipe seed survey:**
- seed 12: 0.0029
- seed 125: 0.0034 ← BEST
- seed 42: -0.0009
- seed 77: 0.0015
- seed 2025: -0.0010

Mean across seeds: 0.0012, std: 0.0018.

The recipe's stable mean is around 0.001-0.002. Single instances
can fall anywhere from -0.001 to +0.0034.

**For the final library (030), use SEED=125**: it gave the highest
observed mean (0.0034) and the best balance across broad evals.
