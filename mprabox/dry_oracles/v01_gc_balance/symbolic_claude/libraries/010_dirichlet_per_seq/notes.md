# Exp 010 — Dirichlet per-sequence weights

## Design
50K sequences; per-sequence weights drawn from Dirichlet(α=10,10,10,10).
Each sequence then iid sampled from its own weights. Aggregate
composition uniform; per-seq stddev ~7-8% per char (~2.5× baseline iid).

## Result vs baseline
| eval    | baseline | exp010  | delta   |
|---------|----------|---------|---------|
| eval_01 | 0.4848   | 0.4846  | -0.0002 |
| eval_07 | 0.5200   | 0.5403  | +0.020  |
| eval_08 | 0.1613   | 0.1815  | +0.020  |
| eval_10 | 0.4700   | 0.5002  | +0.030  |
| eval_13 | 0.4992   | 0.5196  | +0.020  |
| eval_04 | 0.4440   | 0.4022  | -0.042  |

## Interpretation
- eval_01 is essentially unchanged. Per-seq composition variance is
  neither helpful nor harmful for the primary metric, in aggregate.
- However, eval_01 conditions shift internally:
    a: 0.5241 → 0.4929 (-0.031)
    b: 0.5009 → 0.5129 (+0.012)
    c: 0.4295 → 0.4480 (+0.019)
  Condition_a likes uniform; b and c like more per-seq variance.
- Several "low-baseline" evals (07, 08, 10, 13) lift +0.02-0.03.
- Eval_04 drops by -0.04 (per-seq variance hurts it).

## Implications
- Mean across all 14 evals: essentially unchanged (0.458 → 0.458).
- We may be near a ceiling for eval_01 around 0.48-0.49.
- To push higher, need a fundamentally different lever — k-mer
  structure, specific motifs, or other features.
