# Experiment 008: Cell-type DNase-seq peaks

## Design
50K sequences from ENCODE DNase narrowPeak files:
- 16.7K K562 peaks (ENCFF821KDJ)
- 16.7K HepG2 peaks (ENCFF341XEM)
- 16.7K SK-N-SH peaks (ENCFF752OZB)
Each peak centered to 200bp window. Seed=8.

## Results vs 003 (50K balanced cCREs)
| eval | 003 | 008 | Δ |
|---|---|---|---|
| 01 | 0.0758 | **0.0764** | +0.001 |
| 02 | 0.0742 | 0.0751 | +0.001 |
| 03 | 0.0949 | 0.0950 | ~0 |
| 04 | 0.0863 | **0.0903** | +0.004 |
| 06 | 0.0753 | 0.0756 | ~0 |
| 07 | 0.1444 | 0.1374 | -0.007 |
| 08 | 0.0652 | 0.0621 | -0.003 |
| 10 | 0.1277 | 0.1248 | -0.003 |
| 13 | 0.1429 | 0.1380 | -0.005 |
Time: 39s

## Per-cell-type breakdown on eval_01
| Library | K562 | HepG2 | SKNSH |
|---|---|---|---|
| 001 random | 0.063 | 0.064 | 0.059 |
| 003 cCREs | 0.080 | 0.080 | 0.067 |
| 008 DNase | **0.079** | **0.080** | **0.070** |

**SK-N-SH improved meaningfully**: 0.0669 → 0.0697 (+0.003). This is
the biggest SKNSH boost since 001. Confirms that cell-type-targeted
training data improves per-cell-type prediction.

## What I learned
- DNase peaks slightly **beat** cCREs on eval_01 (primary metric)
- But lose on eval_07/10/13 (-0.005 to -0.007) — these eval sets
  apparently reward broader regulatory diversity that cCREs provide
- DNase peaks ARE the new best for eval_01, eval_02, eval_04

## Theory update
The model benefits from BOTH:
- Cell-type-specific training data (helps eval_01, SKNSH, per-cell r)
- Broad regulatory diversity (helps eval_07/10/13, mean across sets)

A hybrid library combining cCREs (diversity) + cell-type DNase peaks
(targeted labels) may capture both.

## Next
Exp 009: Hybrid library combining cCREs and cell-type DNase peaks.
Test if combining the best of both pushes past the 0.076 plateau.
