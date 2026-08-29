# Exp 003: GC stratified (full range)

## What
50k sequences with per-sequence GC fraction p ~ U[0,1]. Each position independently
G/C (chars 1,2) with prob p, A/T (chars 0,3) with prob 1-p. Within each, uniform.
Seed=3.

## Result (eval_01)
- mean = 0.3311 (down from 0.4192 baseline)
- K562 = 0.4590 (down from 0.5902)
- HepG2 = 0.4760 (down from 0.6228)
- SKNSH = 0.0583 (similar to baseline 0.0445)

## Interpretation
Extreme GC stratification HURTS K562/HepG2 r. Random uniform already produces some
natural variance, and any signal from random's GC variance is more aligned with target
than EXTREME stratification.

Possible reasons:
1. **OOD effect**: sequences with GC=0% or GC=100% are outside the model's training
   distribution → prediction & target diverge → lower r.
2. **Removed alphabet diversity**: high-GC sequences contain only chars {1,2} so all
   k-mers involving 0 or 3 are absent. Models trained on 4-letter sequences may produce
   degenerate predictions in this regime.
3. **Multi-modal targets**: target signal may not be monotonic in GC.

## Implications
- DON'T extreme-stratify any single composition axis.
- Random uniform's r=0.42 is a strong baseline; "naive" tweaks have decreased it.
- Need to either:
  (a) keep close to random + add small targeted signal, OR
  (b) find an axis whose variance both models track in the SAME direction.

## Time
~2.5 minutes.
