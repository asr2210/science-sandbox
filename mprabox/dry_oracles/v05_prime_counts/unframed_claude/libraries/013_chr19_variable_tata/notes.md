# Experiment 013 — chr19 + variable TATA density (0-10 per seq)

## Hypothesis
Variable motif density creates across-library variance that both
correlation axes might track, raising r.

## Method
chr19 backbone, insert TATAAA randomly (0-10 copies, uniform).

## Results
- eval_01: 0.0341 (chr19: 0.0502)  → WORSE
- avg: ~0.032

## Interpretation
Adding TATA motifs to chr19 HURT (same pattern as cocktail). The
heavy TATA insertions shift composition toward AT and disturb
natural sequence patterns the oracle was rewarding.

## Theory update — T7
Motif insertion at ANY density hurts on this oracle. The oracle is
NOT TF-motif-driven in a simple sense. Either:
- The motifs need to be at exact positions / spacings (synthetic
  promoter design)
- Or motifs simply aren't the lever; some other property is

Pattern across all experiments:
- Best on eval_01: chr19 (real DNA) at 0.0502
- Anything that disturbs the natural composition or grammar hurts

The lever for >2x improvement seems to require a bimodal library
where two distinct sequence classes both produce consistent strong
signal from f and g. Test next.

## Next
EXP 14: bimodal library — 25K random uniform + 25K random with
strong enhancer scaffold inserts at FIXED positions. Tests whether
creating two distinct classes that both correlation axes recognize
boosts r dramatically.
