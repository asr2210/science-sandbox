# Experiment 017 — Broader motif pool (87 TFs) + 15k pELS

## What I tested
Doubled motif vocabulary from 35 to 87 TFs (added more pioneer
factors, more housekeeping, more inflammatory, more developmental).
Recipe otherwise identical to 012.

## Hypothesis
A broader vocabulary covers more TF families, generalizing to unseen
cell types whose master regulators differ from K562/HepG2/SK-N-SH.

## Result — mean dropped
- eval_04/09: 0.0047 (best on these — record!)
- eval_07: K562=0.0090 (decent)
- eval_10: SKNSH=0.0106 (new high)
- eval_13: K562=0.0075 (positive)
- **eval_08: -0.0015 (LOST badly — was 012's 0.0117)**
- Mean across 14 ≈ 0.0003 (well below 012's 0.0029)

## What this tells me
**Adding more motifs DILUTED the signal.** The original 35-TF pool
was apparently well-tuned for eval_08 — adding 52 more TFs cut
per-motif representation roughly in half. The model learned weaker
features for each motif and lost the eval_08 specialization.

This contradicts the "more diversity = better generalization" naive
intuition. With only 50k training examples, per-motif representation
matters more than vocabulary breadth.

Bright spots: eval_04/09 (0.0047 — new record on these) and eval_10
SKNSH (0.0106 — new high). The added motifs helped some evals while
hurting others. Same multi-objective tradeoff pattern.

## Updates to theory
**v3.9 → v3.10:** Motif vocabulary has a sweet spot. ~35 TFs (the
007/012 pool) seems near-optimal for 50k library / small model.
Below: under-coverage. Above: under-representation. The pool needs
to be just-broad-enough to cover major TF families without diluting
per-motif signal.

This is a *capacity* constraint — at higher N or with bigger models,
more motifs would likely help.

## Next
Test motif DENSITY (per-sequence count). Currently 15-25 inserts/seq.
Try denser (35-50) vs sparser (5-10) variants to map the density
axis with the proven 012 cCRE half.
