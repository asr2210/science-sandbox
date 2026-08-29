# Exp 005 — Synthetic library with 25+ TF motifs injected

## Design
50K x 200bp uniform random backgrounds. For each, insert 1–5 motifs at random
non-overlapping positions, each randomly RC or forward. 30 canonical TF
consensus motifs from JASPAR-like list (AP-1, SP1, GATA, E-box, CREB, NF-kB,
ETS, FOX, HOX, OCT, MEF2, p53, RUNX, TCF, T-box, HNF, NR-DR1, AHR, STAT, IRF,
YY1, CTCF, TATA, CAAT, etc.). GC = 0.494.

## Result
**eval_01 = 0.0401. Essentially identical to random uniform (0.042).**

Strikingly, **eval_08 = 0.1240 — identical to random uniform's 0.124.** All
other evals also match random uniform very closely.

## Interpretation
Motif injection with short consensus sequences barely perturbs the
distributional statistics of a 200bp sequence (10–15bp of motif in 200bp
background ≈ 5–7% of the content). The model "sees" essentially random
sequence with a little structure. Behavior matches random uniform exactly.

This says: **adding "biology" sparsely on top of uniform random doesn't
budge the eval. The injected motifs are too dilute relative to the
background to register as a learnable signal in a from-scratch CNN.**

This also tells me eval_08 is reproducibly returning ~0.124 whenever the
input distribution is approximately uniform random — a robust quirk
useful as a sanity check.

## Counter-evidence to theory
My theory predicted motif-rich libraries would help. Either:
- The motifs need to be much denser (10+ per sequence, or longer motifs).
- The motifs need to be in *natural context* (so spacing/flanks matter).
- The model is bottlenecked elsewhere.

## Next step
Test multi-source diversity (mix cCRE + random hg38 + synthetic). If even
mixing doesn't help, then library distribution within the natural-DNA
universe matters very little.

## Time
14s evaluator, 45s wall.
