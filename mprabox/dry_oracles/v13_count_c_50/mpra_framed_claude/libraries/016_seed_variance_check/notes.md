# Experiment 016 — seed-variance probe (013 recipe, SEED=1)

## Result
| eval | 013 (seed=0) | 016 (seed=1) | Δ |
|------|--------------|---------------|---|
| 01 ★ | 0.5765 | 0.5762 | -0.0003 |
| 04 | 0.5774 | 0.5778 | +0.0004 |
| 07 | 0.6037 | 0.6045 | +0.0008 |
| 08 | 0.1730 | 0.1726 | -0.0004 |
| 10 | 0.5087 | 0.5086 | -0.0001 |
| 13 | 0.5865 | 0.5871 | +0.0006 |
| mean8 | 0.5705 | 0.5704 | -0.0001 |

## Noise floor
Seed-to-seed variance ≈ 0.0005-0.001 per eval, ~0.0001 on mean8.
TINY. The library composition is the dominant driver, not the RNG.

## Implications for prior rankings
| comparison | Δ | real? |
|------------|---|-------|
| 013 vs 009 | +0.002 on eval_01 | borderline real (2-4×noise) |
| 013 vs 015 | +0.0006 on eval_01 | within noise |
| 014 vs 013 | -0.022 on eval_01 | strongly real (20+×noise) |
| 012 vs 009 | -0.002 on eval_01 | borderline real |

Most fine-tuning Δs are small but real; large source changes are clearly real.

## What this means for next experiments
Tuning within the cCRE recipe (type balance, chrom set) gives ~0.002 gains
per try — possible but slow. Bigger moves (different sources, different
augmentation strategies) give larger but more variable Δs.

Next direction: a probe that answers the core mechanism question — is
cCREs' value motif-driven or composition-driven?
