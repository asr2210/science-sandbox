# Experiment 022 — chr19 ENCODE TFBS-centered windows

## Method
Download ENCODE TFBS clusters (466K peaks on chr19), take 200bp
centered on each peak.

## Results
- eval_01: 0.0431 (chr19 baseline: 0.0502) → WORSE
- eval_08: 0.0594 → slight gain

## Interpretation
Real regulatory regions (TFBS-rich) do NOT score higher than
random chr19 windows. eval_01 prefers a broader background, not
TFBS-enriched. Consistent with CpG-island and FANTOM5 enhancer
results (both worse).

eval_01 doesn't reward "active regulatory" but rather the
average natural chromatin background.

## Next
EXP 23: shuffled chr19 (whole-sequence shuffle per window).
Preserves base composition but destroys positional grammar.
Tests if the chr19 advantage is composition-only (then shuffled =
chr19) or also positional (then shuffled << chr19).
