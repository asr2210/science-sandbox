# 005_hybrid_genomic_ccre

25k random GRCh38 windows + 25k cCREs (same 6 chromosomes). Seed 42.

## Result
mean across 14 evals: 0.524 (same as 002: 0.524)
eval_01: 0.502 (vs 002: 0.497, +0.005)

## Per-eval delta vs 002 (random genomic windows)
- eval_01: +0.006
- eval_03: +0.003
- eval_04: +0.009  (consistent with eval_04 liking regulatory)
- eval_06: +0.003
- eval_07: -0.007
- eval_08: +0.002
- eval_10: -0.000
- eval_13: -0.007

## Interpretation
Hybrid is essentially tied with pure genomic, with tiny per-eval shifts
in expected directions (eval_04 benefits from cCREs; eval_07/13
prefer broader genomic). Mixing didn't break through the ~0.50
plateau.

So adding regulatory elements doesn't *add* signal beyond what random
genomic windows already provide — it just shifts which evals win
slightly. The information budget is dominated by overall coverage of
the sequence space, not by enrichment for any one element type.

## Open question
What WILL beat genomic random windows? Possible levers:
- Explicit motif injection (more motif density)
- Synthetic sequences with controlled grammar
- Wider chromosome coverage (probably marginal)
- Activity-balanced selection (need predictor)
