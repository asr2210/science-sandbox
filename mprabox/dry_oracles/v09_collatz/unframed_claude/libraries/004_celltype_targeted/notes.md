# Exp 004 — Cell-type-targeted cocktail (8/seq)

Cocktail: GATA1/KLF1/TAL1 (K562), HNF4/HNF1/CEBP/FOXA (HepG2),
NEUROD/MEF2/BRN2 (SK-N-SH), AP-1/CRE (universal). 8 inserts/seq.

## Result

| metric  | exp 001 | exp 002 | exp 004 |
|---------|--------:|--------:|--------:|
| eval_01 | 0.2307  | 0.2541  | 0.2468  |
| k562    | 0.1361  | 0.1262  | 0.1420  |
| hepg2   | -0.0742 | 0.0186  | -0.0198 |
| sknsh   | 0.6302  | 0.6174  | 0.6181  |

K562 improved over exp 002 by +0.016 (added GATA1/KLF1 explicit motifs).
HepG2 REGRESSED (-0.038 vs exp 002) — losing SP1/NFY hurt HepG2 more than
gaining HNF4/HNF1/CEBP/FOXA helped. SKNSH still ~0.62.

**Implications**: Motif identity matters per cell type but in
non-obvious ways. SP1/CCAAT seems to drive HepG2 in exp 002, not the
liver-specific HNFs we tried in exp 004. Need diagnostic experiments.
