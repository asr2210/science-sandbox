# 009_dels_enhancers

50k 200bp windows from dELS (distal enhancer-like) cCREs only (~789k regions).

## Result
eval_01: 0.6711 — same plateau (~0.68) as chr22-random and cCRE-all.
eval_07: 0.7500 — best yet for eval_07.
eval_04: 0.5472 (slightly worse than cCRE-all's 0.609)

## Interpretation
dELS alone doesn't push past the ~0.68 plateau on eval_01.
cCRE-all mix (PLS + pELS + dELS + CTCF) is essentially tied with random chr22
and dELS.

Conclusion: the score plateau is set by "real-DNA-likeness." Cell-type-agnostic
regulatory enrichment doesn't help on top.

## Next ideas to break plateau
1. Engineer sequences with VARIANCE — half high-activity (motif-rich), half low
   to amplify the correlation
2. MPRA-tested sequences from public data
3. Sequences from cell-type specific accessible regions (DHS for K562)
4. Conserved regulatory elements
