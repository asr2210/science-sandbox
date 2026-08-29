# 007 — Random + one real regulatory core per sequence

## Hypothesis
A longer, real biological regulatory core (20–40bp) inserted into random
scaffold will be recognized by the predictor and boost the score.

## Setup
50k x 200bp. Each: uniform random, then one of 12 literature-validated
mammalian cores (SV40, CMV NFkB, AP-1 trimer, SP1 GC-box, NFY tandem,
CRE tandem, ETS trimer, E-box trimer, GATA trimer, nuclear receptor,
IRF/ISRE, PU.1) overlaid at random position, ~50% RC.

## Results
eval_01 = **0.2570** (random 0.3157). Drop of 0.06.

## Update to theory v7
EVEN inserting one well-known long regulatory core hurts. So far every
deliberate perturbation (composition, sparse motifs, dense motifs, real
cores, dinuc Markov, variable GC) has lowered the score.

The scorer seems trained on UNIFORM RANDOM 200bp libraries and rewards
matching that distribution exactly. Real biology adds out-of-distribution
character that the predictor penalizes via whatever metric "r" measures.

## Next
- Exp 008: pure random uniform, DIFFERENT seed → measure noise floor.
  If 0.32 ± 0.005 → uniform random is near-optimal already.
- Then explore if anything subtle helps (e.g., precisely 50% GC per seq,
  or de-Bruijn-style k-mer coverage).
