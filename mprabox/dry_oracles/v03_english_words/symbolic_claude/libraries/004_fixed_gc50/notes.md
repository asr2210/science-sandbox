# Exp 004: Fixed GC = 50% per sequence

## What
Each of 50k sequences has exactly 100 GC and 100 AT positions, shuffled. Within GC
positions, char ∈ {1,2} uniformly. Within AT, char ∈ {0,3} uniformly. Seed=4.

## Result (eval_01)
- mean = 0.4169 (vs random uniform 0.4192)
- K562 = 0.5852 (vs 0.5902)
- HepG2 = 0.6119 (vs 0.6228)
- SKNSH = 0.0536 (vs 0.0445)

## Interpretation
Score is essentially **unchanged** vs random uniform. Removing per-sequence GC
variance does NOT hurt the score.

Combined with exp 003 (GC stratified hurt severely), the picture is:
- Random uniform's baseline r=0.6 (K562/HepG2) does NOT come from GC variance.
- Adding GC variance hurts, removing it is neutral.
- The 0.6 baseline must come from another source.

## Implications
- GC is not the key axis. Don't engineer for GC content.
- Need to find the actual source of K562/HepG2 baseline r.
- Possible sources: higher-order k-mer variance, index-based target, motif presence.

## Time
~2 minutes.
