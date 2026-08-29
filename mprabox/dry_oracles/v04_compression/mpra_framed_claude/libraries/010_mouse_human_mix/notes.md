# 010_mouse_human_mix — notes

## Design
25K human (hg38) natural + 25K mouse (mm39) natural. Each is random
200bp window from primary autosomes + X/Y.

## Result
- eval_01: 0.4739 (vs 0.4798 pure human natural; 0.4956 best from off-center cCRE mix)
- **Mouse hurts vs pure human** (-0.006)
- **Mouse slightly helps eval_08** (0.0962 vs ~0.09): tiny but consistent
  with mouse being more "diverse" than human

## Interpretation
Cross-species DNA is *not* interchangeable with human DNA. There's a
measurable species-specific signal (~1-3% relative). This means
regulatory grammar is not perfectly universal — it has measurable
species-tuning.

For our goal (model that generalizes across HUMAN cell types), pure
human DNA is the better source. Cross-species would only help if the
goal were cross-species transfer.

## Surprising notes
- eval_08 nudge upward is the first thing I've found that helps it.
  Suggests eval_08 may contain sequences with species-or-distribution-shift
  features that mouse-trained partly recognizes.

## Plateau analysis
Best mean_r on eval_01 across 10 experiments:
- 009 off-center cCRE mix: 0.4956 (current best)
- 004 centered cCRE mix: 0.4937
- 008 3-way mix: 0.4934
- 007 natural+DHS: 0.4898
- 002 pure natural: 0.4798
- 010 human+mouse: 0.4739

Plateau is ~0.49-0.50. Hardest to break.

## Next
Try TSS-centered (promoter-specific) regulatory enrichment, or
reverse-complement augmentation, or larger 4-way mix.
