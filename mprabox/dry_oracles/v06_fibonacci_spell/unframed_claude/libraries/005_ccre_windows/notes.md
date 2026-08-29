# Experiment 005: ENCODE cCRE-centered 200bp windows

## Plan
Sample 50k random cCREs from ENCODE V3 (~1M elements across genome), take 200bp
window centered on each. Predict: enriched for regulatory features → higher score.

## Result
- eval_01 mean_r = **0.1285** (K562=0.031, HepG2=0.161, SKNSH=0.194)
- **LOWER than chr22 random (0.1346)** but higher than synthetic random (0.1176)
- All cell types slightly down vs chr22 random

## Big finding
Concentrating on regulatory elements does NOT help — it hurts slightly compared
to random genomic windows. This is unexpected if score = "regulatory content".

## Theory update
T4 partially refined: the scorer doesn't just want regulatory content. Possible
explanations:
- (a) Score depends on sequence-space DIVERSITY; cCREs cluster together
- (b) Score compares two model outputs; models agree best on "typical" DNA
- (c) cCREs are over-represented for CpG islands and other low-complexity
  regions that hurt variance

## Next
- Exp 006: sample random 200bp windows from FULL hg38 (more diverse than chr22)
- Exp 007: try active enhancers specifically (subset of cCREs that are likely
  active in K562/HepG2/SKNSH)
- Compare: maximize between diversity vs specificity
