# Exp 006: Random 8-mer motif library injection

## What
50k random uniform backgrounds. For each seq, sample K ~ U{0,20}. Insert K random
8-mers (from a fixed library of 64 random 8-mers, seed 123) at random non-overlapping
positions.

## Result (eval_01)
- mean = 0.4038 (vs random uniform 0.4192)
- K562 = 0.5573 (vs 0.5902)
- HepG2 = 0.5870 (vs 0.6228)
- SKNSH = 0.0671 (vs 0.0445)

## Interpretation
Slight overall drop. K562/HepG2 modestly hurt; SKNSH improved a touch.

The fact that adding RANDOM 8-mers (most of which aren't real biological motifs)
hurts K562/HepG2 suggests we may be moving away from the agreement region — the model
"recognizes" some random 8-mers as features but the target model doesn't agree.

SKNSH slight uptick is interesting — it's so low (0.04) that any perturbation can
push it up.

## Implications
- Random motif insertion is not a winning strategy.
- Worth trying biologically-meaningful motifs (canonical TFBSs).
- SKNSH may have headroom worth exploring separately.

## Time
~2 minutes.
