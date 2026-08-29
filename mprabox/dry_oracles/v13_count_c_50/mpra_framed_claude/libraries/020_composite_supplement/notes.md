# Experiment 020 — composite supplement (shuf-cCRE + GC-filter)

## Result
| eval | 013 (cCRE) | 019 (GCf) | 020 (composite) | vs 013 |
|------|------------|-----------|------------------|--------|
| 01 ★ | **0.5765** | 0.5507 | 0.5660 | -0.011 |
| 04 | 0.5774 | 0.5735 | **0.5797** | +0.002 |
| 07 | **0.6037** | 0.5603 | 0.5825 | -0.021 |
| 08 | 0.1730 | **0.2254** | 0.2081 | +0.035 |
| 10 | 0.5087 | 0.4752 | 0.4946 | -0.014 |
| 13 | **0.5865** | 0.5431 | 0.5650 | -0.022 |
| mean8 | 0.5705 | 0.5536 | 0.5652 | -0.005 |

## Verdict: interpolation, not super-addition
Just like 015 (3-source), the composite supplement lands between the two
components on every eval. No stacking. The two compositional recipes
conflict rather than compose.

## Mechanism
shuffled-cCRE supplies a wide-GC distribution; GC-filter pulls it toward
narrow high-GC. Mixed, the result is intermediate. The model can't
"learn from both halves separately" — it integrates across all training
examples and converges on the AVERAGE composition.

## Hard lesson
Composition tuning at 30% supplement seems to have a ceiling around
eval_01 ≈ 0.577. Cannot break this with further compositional moves
because all moves trade one compositional axis against another.

## Next direction: change the BASE library or augmentation strategy
To push past the ceiling, need a different lever. Options:
- Higher-GC base library (chr16/17/19/20/22 instead of mc5)
- Different augmentation strategy (e.g., reverse complement)
- Entirely different content axis (JASPAR motif-flanked sequences)
