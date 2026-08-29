# 006 — Markov order-1 dinucleotide bias

Stationary distribution uniform but with biased transitions:
0→1, 1→0, 2→3, 3→2 each at 0.55 (others 0.15).

Marginal composition uniform 25% each (verified). Dinucleotides "01","10","23","32" enriched (~13.75% vs iid 6.25%).

## Result
- eval_01: mean_r = 0.2963 (vs 0.4200 baseline) — substantially WORSE
- a = 0.3991, b = 0.4497, c = 0.0401 (all worse)

## Interpretation
**Dinucleotide structure HURTS even with uniform composition.**
This is the strongest evidence so far that the scoring rewards iid randomness specifically (not just any uniform distribution).

Combined evidence:
- Composition skew → bad
- Exact composition uniformity → bad  
- Composition variance via Dirichlet → bad for a,b; good for c
- Dinucleotide structure → bad

iid random sequences with binomial-level per-seq composition variance seem to be the sweet spot for a, b.

## Next probe
Verify reproducibility by trying a different seed. If 0.42 is consistent across seeds, we know iid random is a stable target. Then bold attempts: hybrid libraries, motif insertion, etc.
