# Experiment 011 — 80/20 multi-chrom + cCRE

## Results across all three ratios tested
| eval | 80/20 (this) | 70/30 (009) | 50/50 (010) |
|------|--------------|-------------|-------------|
| 01 ★ | 0.5710 | **0.5748** | 0.5699 |
| 02 | 0.5719 | 0.5756 | 0.5706 |
| 03 | 0.5702 | 0.5709 | 0.5611 |
| 04 | 0.5517 | 0.5695 | **0.5891** |
| 06 | 0.5700 | 0.5732 | 0.5671 |
| 07 | 0.6174 | 0.6069 | 0.5787 |
| 08 | 0.1081 | 0.1560 | **0.2280** |
| 10 | 0.5106 | 0.5101 | 0.4985 |
| 13 | **0.6010** | 0.5897 | 0.5601 |
| mean8 | 0.563 | **0.581** | 0.569 |

## Verdict
30% cCRE is the peak ratio. The landscape is shallow but 70/30 wins on
both the primary eval_01 (by 0.004) and the 8-eval mean (by 0.012-0.018).

## Pattern observed
- 80/20 has slightly better eval_07/13 (more genomic diversity) and lower
  eval_08 (less GC).
- 50/50 has better eval_04/08 (more cCRE composition) but worse eval_07/13.
- 70/30 is the balanced peak.

## What this tells me
The cCRE-to-genomic mix optimizes a tradeoff between two eval subsets:
"reward broad genomic diversity" (07/13) vs "reward GC/composition"
(04/08). Past ~30% cCRE, the diversity loss is faster than the GC gain.

The ratio is locally optimal. To push higher, need a different axis.
