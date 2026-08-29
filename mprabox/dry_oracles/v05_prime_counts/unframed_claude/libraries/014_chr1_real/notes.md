# Experiment 014 — chr1 random 200bp windows

## Hypothesis
Larger source chromosome may have more diverse / active sequence
content and beat chr19 (0.0502).

## Method
50K random 200bp windows from human chr1 (uppercase only).

## Results
- eval_01: 0.0489 (chr19: 0.0502) → slightly WORSE
- eval_08: 0.0317 (chr19: 0.0551) → WORSE
- avg: ~0.043

## Interpretation
chr1 ≈ chr19 on eval_01. Natural DNA caps near 0.05 regardless of
which chromosome. The size/gene-density of source chromosome is NOT
the lever.

## Theory update — T8
Plain natural DNA (any chromosome) hits a ceiling ~0.050 on eval_01.
Need a structural intervention OTHER than motif insertion to break
through. Insertion of motifs hurts (T7). Bigger chromosome doesn't
help (T8).

What's left:
- Filter chr19 to NON-REPEAT regions (use soft-mask info)
- Filter chr19 to ENCODE cCRE / open-chromatin regions
- Specific BIOLOGICAL annotation (active enhancers, promoters)
- True bimodal libraries (two distinct active classes)

## Next
EXP 15: chr19 with REPEATS REMOVED (only uppercase = non-repeat).
chr19.fa is soft-masked; filter to windows that are 100% uppercase.
Tests whether repeat sequences are diluting signal.
