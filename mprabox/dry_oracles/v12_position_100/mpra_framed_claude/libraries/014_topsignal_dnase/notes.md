# Experiment 014: Top-signal DNase peaks (quality > quantity)

## Design
Same as 009 composition (20K cCRE + 25K DNase + 5K random) but DNase
restricted to TOP signalValue peaks per cell. Top-8K of K562 = top 3.4%,
top-8K HepG2 = top 9%, top-9K SKNSH = top 5.8%.

## Result
eval_01 = **0.0721**, on the low edge of the noise band.

| eval | 009 mean (band ~0.075±0.002) | 014 |
|---|---|---|
| 01 | 0.0772 / 0.0734 (rep) | 0.0721 |
| K562 | 0.0799 / 0.0761 | 0.0744 |
| HepG2 | 0.0812 / 0.0774 | 0.0758 |
| SKNSH | 0.0705 / 0.0667 | 0.0662 |

## What I learned
**Top-signal DNase peaks did NOT help.** Possible reasons:
- Top peaks are dominated by housekeeping/ubiquitous regions (promoters,
  CTCF sites) — they're high-signal because they're open in EVERY cell.
  This makes them less cell-type-distinctive.
- Lower-signal peaks include subtle cell-type-specific enhancers that
  may be informative for MPRA differential activity prediction.
- Quality of "accessibility signal" isn't the bottleneck — diversity is.

## Theory update
Quality filtering by signal magnitude is the WRONG axis. The model wants:
- High SEQUENCE diversity (many distinct motif contexts)
- Not high accessibility/coverage signal

## Next: exp 015 — SKNSH heavy
Across all experiments, SKNSH is consistently the weakest per-cell
(0.066-0.070 vs K562 0.076-0.080). Mean improvement requires lifting
SKNSH. Try: massively oversample SKNSH-specific data.
- 10K cCRE + 8K K562 DNase + 8K HepG2 DNase + 14K SKNSH DNase + 5K SKNSH H3K27ac + 5K random
- SKNSH gets 19K (38%) of library, vs K562 8K (16%), HepG2 8K (16%)
