# Experiment 006: Random windows from full hg38

## Plan
50k 200bp windows sampled across all 24 chromosomes (autosomes + X/Y), weighted
by chromosome length, rejecting any with N.

## Result
- eval_01 mean_r = **0.1387** (K562=0.049, HepG2=0.172, SKNSH=0.195)
- **Beats chr22 random (0.1346) and cCREs (0.1285).**
- K562 r jumped 4x over random baseline (0.012 → 0.049)

## Big finding
Genome-wide diversity beats both restricted (chr22) and concentrated (cCREs)
sampling. This is consistent with T5: the scorer rewards libraries that span
natural sequence-space broadly.

## Theory update
T5 confirmed. The scorer most likely either:
- Compares two model predictions on our library → high r when models agree,
  which happens most on typical genomic DNA
- Or rewards libraries that resemble natural genome k-mer distribution

## Next
Push further by testing: tiled (maximally non-redundant) genome windows.
Should beat random sampling if duplication is a small issue.
