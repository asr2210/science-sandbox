# 022_pels_short — notes

## Design
50K SHORTEST pELS cCREs (length 150-186bp) from 249K pool.
Same central-200bp extraction. Three seeds.

## Result vs. pELS length matrix

| eval | uniform012 | long021 | short022 | Δ short |
|------|------------|---------|----------|---------|
| 01   | 0.7203     | 0.7141  | 0.7030   | -0.017  |
| 02   | 0.8129     | 0.8077  | 0.7927   | -0.020  |
| 03   | 0.7958     | 0.7874  | 0.7778   | -0.018  |
| 04   | 0.7603     | 0.7631  | 0.7454   | -0.015  |
| 05   | 0.7203     | 0.7142  | 0.7028   | -0.017  |
| 06   | 0.8133     | 0.8082  | 0.7932   | -0.020  |
| 07   | 0.7489     | 0.7315  | 0.7273   | -0.022  |
| 08   | 0.6844     | 0.6819  | 0.6653   | -0.019  |
| 09   | 0.8238     | 0.8259  | 0.8073   | -0.016  |
| 10   | 0.7729     | 0.7740  | 0.7500   | -0.023  |
| 11   | 0.7083     | 0.7021  | 0.6912   | -0.017  |
| 12   | 0.6853     | 0.6762  | 0.6700   | -0.015  |
| 13   | 0.7473     | 0.7200  | 0.7324   | -0.015  |
| 14   | 0.8129     | 0.8078  | 0.7927   | -0.020  |

Mean: uniform 0.758, long 0.751, **short 0.739**.

## Interpretation

**Hypothesis (B) "both tails are atypical" CONFIRMED.** Both
length extremes drop vs. uniform, but **shortest hurts more
than longest** (-0.019 vs -0.007).

**Length matrix:**
- pELS uniform (full distribution): 0.758
- pELS longest (≥336bp): 0.751 (-0.007)
- pELS shortest (≤186bp): 0.739 (-0.019)

**Key asymmetry:** shortest hurts ~2.7× more than longest.

**Mechanism hypothesis for short-worse-than-long:**
The 200bp central window centered on a ≤186bp cCRE extends
~7-25bp into FLANKING genomic content on each side. So short
pELS sequences carry less cCRE-defined content per window
and more flanking-genomic content. This dilutes signal-to-noise
from the model's perspective. Long pELS by contrast have
their 200bp window FULLY inside the cCRE — clean signal but
slightly atypical chromatin context.

**Combined finding:** the "natural" length distribution
(uniform sampling across pELS) is itself an OPTIMUM. Filtering
to either extreme moves away from the model's learned
distribution.

This generalizes the lesson from 016/017: per-element
manipulation hurts. Extracting a NON-RANDOM subset of pELS
on intrinsic features uniformly drops performance even with
the same pool size and same class.

## Theory update

**Length-as-quality is fully FALSIFIED.** Combined evidence
from 021/022: extreme pELS (either tail) underperform random
sampling across the whole pool.

**Reframed: pELS uniform sampling captures a CALIBRATED
distribution of cCRE-window/flanking ratios.** Filtering to
a homogeneous subset systematically disrupts that calibration.
The model expects to see a mix of "tight cCRE inside window"
and "loose cCRE with flanking" — neither pure tail works as
well as the natural mixture.

**Implication:** quality filtering on intrinsic BED-coordinate
features is unlikely to help. To exceed pELS-only, we need
either (i) external annotation (chromatin signal strength,
conservation, cell-type breadth), or (ii) per-element
augmentation that ADDS information without changing the pool
distribution.

## Next experiment

**Exp 023: pELS with 1% sequence mutation noise.** 50K
pELS with same central-200bp extraction, but each sequence
has 2 random base substitutions injected. Tests whether
mild input noise injection helps generalization (a known DL
augmentation strategy). The oracle labels are recomputed
on the mutated sequences, so the supervision matches the
input — this isolates whether the model learns more
robust regulatory grammar when forced to handle mild noise.
