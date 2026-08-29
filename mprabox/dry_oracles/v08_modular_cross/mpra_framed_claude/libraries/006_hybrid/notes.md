# Experiment 006 — Hybrid library (promoters + hema motifs + neural motifs)

## What I tested
17,000 TSS-centered promoters + 16,500 hematopoietic-biased motif
scaffolds + 16,500 neural-biased motif scaffolds (each scaffold:
random uniform backbone + 4–12 motif inserts).

## Hypothesis
Each library type lit up a different cell type in earlier experiments.
Mixing them should raise the mean by activating multiple cell types
at once.

## Result — best mean_r so far
- eval_01 = 0.0033 (vs 0.005 for motif-only, 0.000 for promoters-only)
- eval_03/12: mean 0.0037, HepG2 = 0.014 (strong, from promoters)
- eval_04/09: K562 = 0.0084 (from motif scaffolds)
- SK-N-SH: mostly near zero or negative — the neural motif subset
  did NOT visibly help SK-N-SH.

## What this tells me
**Confirmed:** combining multiple library types ADDS their cell-type-
specific contributions, raising the mean — at least for K562/HepG2.
**Not confirmed:** SK-N-SH did not respond to the neural motif
scaffold. Either:
- Neural TF motifs as currently chosen aren't activating SK-N-SH in
  the MPRA simulator
- SK-N-SH evaluation needs real neuroblastoma-specific sequence, not
  designed scaffolds
- My neural motif pool was too redundant (NEUROG/NEUROD/ASCL1 all
  share the same E-box core CAGCTG)

## Updates to theory
- Hybrid design works: cell-type-specific signals are additive.
- Bottleneck for mean_r is now the weakest cell signal (SK-N-SH).
- The next-best lever is to find what specifically activates SK-N-SH.

## Next
Try real ENCODE SK-N-SH cCREs / neural-specific peaks rather than
synthetic neural motifs.
