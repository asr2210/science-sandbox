# 004_ccre_plus_shuffled

## Design
50,000 = 25,000 real 200bp cCRE windows + 25,000 dinucleotide-shuffled
versions of those same windows (matched composition, randomised motif
syntax). Sharpr-style paired-control design.

## Hypothesis
Pairing real with composition-matched shuffled controls should let
the model learn motif-specific signal (vs composition-driven). Should
lift HepG2 r and eval_08 if motif/composition separation is the
limiting factor.

## Result vs 002
                eval_01  K562    HepG2   SKNSH   eval_08
002 cCRE pure:  0.3154   0.145   0.177   0.625   0.076
004 cCRE+shuf:  0.3116   0.144   0.168   0.623   0.082

Small drop in HepG2 (-0.009) and tiny lift in eval_08 (+0.006).
Net: -0.004 on eval_01.

## Interpretation
Shuffled controls do NOT help. The model is not bottlenecked by
inability to separate motif-driven from composition-driven activity.
Halving the real sequence count actually slightly hurts (HepG2).

Combined with 003 finding (K562 source doesn't matter, K562 stuck at
0.14), the picture is now: **all reasonable single-tile-per-region
libraries plateau around mean_r ≈ 0.31–0.32**. K562 (~0.14), HepG2
(~0.18), SKNSH (~0.63) ceilings are robust to source choice.

## Theory T3 → T4
- Motif/composition separation is NOT the bottleneck.
- The plateau is likely limited by either (a) measurement noise in
  prepare.py's MPRA (replicate concordance ceiling), or (b)
  insufficient information per training pair given 1 tile per region.
- Literature (PARM) shows dense per-region coverage can break this
  plateau. PARM with ~240× coverage of 30K promoters gives R=0.92 on
  K562, 0.89 on HepG2. They used 10M total fragments but the principle
  is dense per-region resampling, not just total size.
- For 50K library, dense per-region is achievable: e.g. 10K regions ×
  5 tiles each, or 5K regions × 10 tiles. Tradeoff: density vs
  diversity.

## Next
Experiment 005: dense per-region tiling. 10,000 cCREs × 5 random-
offset 200bp tiles each. Tests density hypothesis directly. Predict:
HepG2 lifts above 0.18; K562 maybe slight lift but probably still
ceiling-limited.
