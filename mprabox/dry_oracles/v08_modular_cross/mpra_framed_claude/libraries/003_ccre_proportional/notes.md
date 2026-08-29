# Experiment 003 — ENCODE cCRE-centered windows

## What I tested
50,000 cCREs sampled uniformly from GRCh38 cCRE BED (~1.06M elements).
For each cCRE, extract 200 bp centered on its midpoint. Categories
included proportionally: dELS (~48%), dELS,CTCF (~26%), pELS variants
(~16%), CTCF-only/PLS/DNase-H3K4me3 (the rest).

## Hypothesis
Compared to random genomic windows, cCREs should give the model a much
higher fraction of "active" training examples — boosting mean_r
substantially above 0.002.

## Result
- eval_01 = -0.0004
- Mean ≈ -0.0001 across 14 evals.
- **No improvement over random.** Essentially worse than random
  genomic (mean 0.002).

## What this tells me
Mere "annotated as regulatory" is not enough. Three possibilities:
1. cCRE annotation is cross-cell-type aggregate — many cCREs are
   inactive in K562/HepG2/SK-N-SH specifically.
2. cCRE activity in an MPRA (no chromatin context) is much weaker
   than at the endogenous locus.
3. The model needs a stronger sequence-activity relationship than
   natural sequences provide. Synthetic motif inserts may be
   necessary.

Literature note (Agarwal et al. 2024 lentiMPRA on 680k cCREs): only
30–58% of cCREs were more active than synthetic negative controls.
So even an "enriched-for-regulatory" library has nearly half noise.

## Updates to theory
- Library design must produce **predictable, wide activity range**.
- Realism alone — even from highly curated annotations — does not
  produce a learnable signal under MPRA conditions.

## Next
Synthetic motif scaffolds (Exp 004): random backbone + variable number
of canonical TF motifs. Forces wide activity dynamic range.
