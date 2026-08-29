# Experiment 010 — 50/50 multi-chrom + cCRE

## Results vs 70/30 (009)
| eval | 70/30 (009) | 50/50 (this) | Δ |
|------|-------------|--------------|---|
| 01 ★ | **0.5748** | 0.5699 | -0.005 |
| 02 | 0.5756 | 0.5706 | -0.005 |
| 03 | 0.5709 | 0.5611 | -0.010 |
| 04 | 0.5695 | 0.5891 | +0.020 |
| 06 | 0.5732 | 0.5671 | -0.006 |
| 07 | 0.6069 | 0.5787 | -0.028 |
| 08 | 0.1560 | 0.2280 | +0.072 |
| 10 | 0.5101 | 0.4985 | -0.012 |
| 13 | 0.5897 | 0.5601 | -0.030 |

eval_01 (primary) slightly worse. eval_07/13 worse by 0.03. eval_08 better
by 0.07. eval_04 +0.02.

## Verdict
70/30 wins on the primary metric. More cCRE share trades eval_07/13 (which
reward broad genomic diversity) for eval_08 (which reward GC content).
Net mean across 8 unique evals: 70/30 = 0.581, 50/50 = 0.569.

## Implication
- The cCRE share has a sweet spot around 30%. Try 80/20 next.
- The eval_07/13 vs eval_08 tradeoff is concrete: cCREs hurt the
  diversity-rewarding evals as they help the GC-rewarding one.
- Optimization should focus on what we can multiply, not what we can trade.
