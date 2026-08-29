# 006_motif_injected_random

50k uniform random 200bp ACGT with 2-5 well-known TFBS consensus motifs
injected at random non-overlapping positions, random strand. Motif
catalog: 25 broadly-conserved mammalian TFBSs (TATA, CAAT, Sp1, CREB,
AP-1, NFkB, E-box, GATA, HNF4, p53, etc.).

## Result
mean across 14 evals: 0.319 — **WORSE than pure random (001: 0.342)**
eval_01: 0.307 (vs 001: 0.343, -0.036)

EVERY eval set scored lower than pure random.

## Interpretation
Injecting consensus TFBS motifs into random backbone *hurts*. This was
unexpected. Possible mechanisms:
1. Consensus sites are too strong/uniform. Real TFBSs in genomes vary
   along a PWM continuum, with most matches being weak. A library of
   ultra-strong consensus sites teaches the model to over-predict
   activity from any close motif match → poor calibration.
2. Out-of-distribution: random ACGT background with crisp consensus
   motifs is unlike any natural sequence. The model overfits to this
   pattern and fails to generalize to natural test sequences.
3. The MPRA on this library may produce a different activity
   distribution (more bimodal — sequences with strong motifs vs
   essentially-random sequences). The model trained on this can't
   predict the smoother gradient of natural sequences.

## Implication
Adding designed/artificial motifs to a library is harmful. The model
needs to see natural motif distributions in natural sequence contexts.
This is consistent with the cCRE result: curation/enrichment toward
specific sequence types hurts the model.

The pattern across 001-006:
- The closer the library matches "broad natural human DNA", the
  higher the score.
- Both *removing* natural content (uniform random) and *adding*
  artificial content (consensus motifs, regulatory enrichment) hurt.
- Random genomic windows (002) appear to sit near a natural-data
  ceiling at ~0.50 for our 50k budget.

## Open questions
- Is the 0.50 ceiling fundamental, or can it be pushed by more
  diverse natural data (more chromosomes, multi-species)?
- What is eval_08 actually measuring? It's stuck at ~0.07-0.11 across
  every library type so far and got HURT by motif injection too.
