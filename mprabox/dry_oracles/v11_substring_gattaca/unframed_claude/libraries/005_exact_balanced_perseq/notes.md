# 005 — Strict 50A/50C/50G/50T per sequence

## Hypothesis
Pinning each sequence to exactly 50 of each base eliminates Poisson
composition variance. If the scoring expects uniform composition, this should
match or beat random.

## Setup
Each sequence: shuffle of 50 A + 50 C + 50 G + 50 T.

## Result
- eval_01 mean=**0.8260** (K562 **0.8668**, HepG2 **0.9131**, SKNSH 0.6982)
- K562 +0.036, HepG2 +0.034 vs random (gains!)
- SK-N-SH -0.140 (big loss)
- Mean: down from random because SK-N-SH loss dominates

## Interpretation
K562 and HepG2 *prefer* zero per-sequence composition variance. SK-N-SH
*needs* Poisson composition variance to score well. These two preferences
are in tension. The simplest mechanism: K562/HepG2 scoring head is robust
to inputs at exact 25% comp, while SK-N-SH head uses a feature
(maybe related to per-seq composition deviation, GC entropy, or low-complexity
detection) that becomes constant or degenerate at strict uniformity.

This means a single-mode library cannot peak all three simultaneously.
Possible play: hybrid (half strict, half random) or perturbed-strict (
each sequence between 48-52 of each base).

## Next
- 006: motif insertion on uniform random background. Tests an orthogonal
  axis (regulatory content) before pursuing composition hybrids.
