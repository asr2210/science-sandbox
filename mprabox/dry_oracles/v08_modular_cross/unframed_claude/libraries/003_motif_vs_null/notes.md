# 003 — motif-rich + AT-null

## Method
50k sequences: 25k "active" (GC=55% background + 6 random TF motif
insertions from a panel of 10 strong universal motifs) and 25k "null"
(AT-rich GC=20%, no motifs), then shuffled. Tests whether a bimodal
active/null mix gives a stronger correlation signal than uniform
random.

## Results (eval_01)
mean_r=0.0014, K562=+0.0137, HepG2=-0.0060, SKNSH=-0.0034

## Key finding
**K562_r jumped ~10x** vs random baseline (+0.0014 → +0.0137).
HepG2 and SKNSH moved slightly NEGATIVE. Mean_r barely moved because
positive K562 and negative HepG2/SKNSH offset.

Interpretation: the motif panel I picked (AP-1, E-box, SP1, NF-Y,
CREB, GATA, TEAD, AGGTCA, ETS) is K562-friendly. K562 model agrees
"motif-rich" = active, "AT-rich" = inactive. But HepG2 and SKNSH
models appear to read AT-rich as MORE active than GC-rich-with-these-
motifs (consistent with HepG2 having AT-rich enhancers around HNF1A
and FOXA1 sites, which are AT-rich consensus).

## Updated theory
- The scorer is reading per-cell-line regulatory predictions. The
  "two predictors" might be a per-cell-line eval model vs. ground-
  truth measurements (which is itself a function of sequence).
- Cell-type-specific motifs matter — universal motifs are not enough.
- Wide dynamic range (active vs null mix) is HELPFUL but only if both
  predictors agree on which side is which.

## Next experiment
Build a 4-bank library:
- K562-bank: GATA1/KLF/NFE2/TAL1/AP-1 motifs, GC-rich background
- HepG2-bank: HNF1A/HNF4A/CEBPA/FOXA motifs, AT-rich background
- SK-N-SH-bank: NEUROD/ASCL1/CREB/EBOX motifs, neutral background
- Null-bank: low-complexity, no motifs

Predict: all three cell-line r's should move positive simultaneously.
