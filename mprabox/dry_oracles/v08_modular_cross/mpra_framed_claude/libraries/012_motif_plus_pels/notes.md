# Experiment 012 — 35k dense motifs + 15k pELS cCREs

## What I tested
35,000 dense motif scaffolds (same recipe as 007) + 15,000 pELS-class
cCREs (proximal enhancer-like signature, ~172k available, centered on
midpoint). 70/30 ratio.

## Hypothesis
pELS are real proximal enhancers — different from TSS promoters in
chromatin signature and likely in MPRA behavior. Mixing them with
motif scaffolds may light up evals that TSS promoters didn't.

## Result — new records on individual evals
- **eval_08: mean=0.0117, K562=0.0210, SKNSH=0.0099** (record on
  mean, K562, AND SKNSH balance)
- **eval_07: SKNSH=0.0162** (highest SK-N-SH ever)
- eval_10: mean=0.0057, SKNSH=0.0091
- eval_06/11: mean=0.0036, HepG2=0.0064
- eval_04/09: -0.0020 (lost ground here vs 009)
- Mean across 14 evals ≈ 0.0029 (similar to 009's 0.0026)

## What this tells me
- pELS cCREs are a strictly better "real-biology" supplement than
  RefSeq TSS promoters for the eval_08, eval_10 axis.
- pELS lifts SK-N-SH more than promoters do (SKNSH on eval_07 went
  from 0.0037 (009) → 0.0162 (012)).
- The mean barely moved because gains on eval_08 were offset by
  losses on eval_04/09.

## Updates to theory
**v3.4 → v3.5:** "Real enhancer-class regulatory sequences" (pELS)
help SKNSH and K562 more than "real promoter-class" (TSS). Probably
because:
- Enhancers carry more TF diversity in 200 bp than core promoters.
- Promoters skew toward HepG2/housekeeping in the model.
- SKNSH may need enhancer-class sequence to learn.

## Next
Try dELS (distal enhancer-like, biggest class — 510k) + motifs. Or
combine all cCRE classes for a bigger "real-biology" component.
