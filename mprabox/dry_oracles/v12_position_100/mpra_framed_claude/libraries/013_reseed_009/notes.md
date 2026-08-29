# Experiment 013: Reseed 009 — measure noise floor

## Design
EXACT same composition as 009 (20K cCRE + 25K DNase + 5K random) but SEED=13
instead of SEED=9. Tests pipeline run-to-run variability.

## Result — large noise discovered
| eval | 009 (SEED=9) | 013 (SEED=13) | Δ (noise!) |
|---|---|---|---|
| 01 | 0.0772 | 0.0734 | **-0.0038** |
| 02 | 0.0755 | 0.0719 | -0.0036 |
| 03 | 0.0955 | 0.0889 | -0.0066 |
| 04 | 0.0913 | 0.0879 | -0.0034 |
| 06 | 0.0765 | 0.0722 | -0.0043 |
| 07 | 0.1437 | 0.1398 | -0.0039 |
| 08 | 0.0639 | 0.0674 | +0.0035 |
| 10 | 0.1286 | 0.1300 | +0.0014 |
| 13 | 0.1409 | 0.1398 | -0.0011 |

All three cells drop by ~0.0038 (K562, HepG2, SKNSH each ~0.004 lower).
**This means the seed alone changes eval_01 by ±0.004.**

## Implication — most prior "improvements" are within noise

Recompiling all hybrid/cCRE-based experiments on eval_01:
| exp | eval_01 |
|---|---|
| 003 cCREs (SEED=3) | 0.0758 |
| 004 pure cCRE (SEED=4) | 0.0755 |
| 005 cCRE+shuffled (SEED=5) | 0.0727 |
| 006 cCRE+TSS (SEED=6) | 0.0708 |
| 007 multiwindow (SEED=7) | 0.0747 |
| 008 DNase (SEED=8) | 0.0764 |
| 009 hybrid (SEED=9) | **0.0772** |
| 010 3-source (SEED=10) | 0.0753 |
| 011 more DNase (SEED=11) | 0.0759 |
| 012 multi-cell (SEED=12) | 0.0758 |
| 013 reseed 009 (SEED=13) | 0.0734 |

Range: 0.0708-0.0772 = 0.0064. With noise floor ~0.004, this entire
range is within ~1.5σ of a common mean. Mean ≈ 0.0753, std ≈ 0.0017.
009's 0.0772 was a +1σ outlier; 013's 0.0734 is a -1σ outlier.

**Conclusion: from exp 003 onward, no design has been clearly better
than any other.** The "hybrid is best" theory was a noise artifact.

## What was real
- Jump from 002 (0.0646) to 003 (0.0758) = +0.0112, well above noise.
  Genomic regulatory sequences are real signal vs random.
- Everything since is in the same noise band.

## Theory revision
The model has a strong but bounded inductive bias: any library of
GENOMIC REGULATORY SEQUENCES (cCREs, DNase peaks, mixed) gives roughly
the same performance ~0.076 on eval_01. To break this band, we need:
1. Much larger data volume (but N=50K fixed)
2. Higher-quality labels (e.g., top-percentile peaks, not all peaks)
3. Multi-seed evaluation to detect smaller real effects
4. Qualitatively new sequence types that aren't redundant with cCRE/DNase

## Next
Two complementary directions:
- Exp 014: **quality** — restrict to top-signal peaks only (e.g., top 10%
  by signal score), test if high-confidence labels beat random sampling
- Long-term: run designs with multiple seeds and average
