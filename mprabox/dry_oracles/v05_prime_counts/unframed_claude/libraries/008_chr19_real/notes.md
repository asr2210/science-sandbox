# Experiment 008 — chr19 random windows

## Hypothesis
chr19 is the most gene-dense human chromosome. If "gene-density"
or "regulatory density" of the source matters, chr19 should beat
chr22 (gene-poor).

## Method
50K random 200bp windows from hg38 chr19, N-windows rejected.

## Results
- eval_01: 0.0502 (chr22: 0.0492, random: 0.0420) → marginal +0.001 vs chr22
- avg: ~0.048
- All evals comparable to chr22 with tiny improvements

## Interpretation
Gene density gives only a TINY boost. Real human DNA in either
chromosome saturates at ~0.05 on eval_01. The "natural-DNA effect"
is small (+0.007 over random uniform) and not much extended by
gene density.

Need a structurally different intervention for a bigger jump.

## Next
EXP 9: sample 200bp windows from CpG islands (combined chr19+chr22)
— these are dense regulatory regions. If r jumps significantly,
CpG-island-like sequences are a key in-distribution class.
