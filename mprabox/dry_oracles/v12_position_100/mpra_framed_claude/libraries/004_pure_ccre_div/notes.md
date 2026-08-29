# Experiment 004: Pure cCRE library with enhancer diversity

## Design
50,000 sequences, all cCRE-derived (no random background):
- 25,000 dELS (50% — most diverse class)
- 10,000 pELS, 5,000 PLS, 5,000 CA_TF, 5,000 CA-CTCF
Seed=4.

## Results vs 003 (deltas)
| eval | 003 | 004 | Δ |
|---|---|---|---|
| 01 | 0.0758 | 0.0755 | -0.0003 |
| 03 | 0.0949 | 0.0954 | +0.0005 |
| 04 | 0.0863 | 0.0862 | -0.0001 |
| 07 | 0.1444 | 0.1429 | -0.0015 |
| 08 | 0.0652 | 0.0617 | -0.0035 |
| 10 | 0.1277 | 0.1280 | +0.0003 |
| 13 | 0.1429 | 0.1409 | -0.0020 |
Time: 48s.

## What I learned
- Differences from 003 are tiny — within run-to-run noise.
- Dropping the 12.5% random background DIDN'T meaningfully help.
- Going dELS-heavy DIDN'T meaningfully help either.
- Adding CTCF as own bucket DIDN'T meaningfully help.
- eval_08 dropped slightly — possibly random background was a small
  positive control for this set.

## Conclusion
**Composition tweaks within cCRE-derived libraries are saturated at
~0.076 on eval_01.** Need a fundamentally different lever: either a
different sequence source (UTRs, TSS, ChIP-seq peaks), a different
sampling strategy (activity-weighted), or a different label-augmentation
scheme.

## Next
Test what part of cCRE content drives performance: real cCREs vs
dinucleotide-matched random sequences. If matched random does badly,
motifs/grammar are doing the work; if it's similar, base composition
is.
