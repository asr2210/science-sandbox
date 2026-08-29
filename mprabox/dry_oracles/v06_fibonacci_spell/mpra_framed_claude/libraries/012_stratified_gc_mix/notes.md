# 012 — Stratified GC mix (5 quantile bins × 10k)

## What I tested
50k chr22 200bp windows stratified into 5 equal-quantile GC bins
(GC ranges: [0,0.38], [0.38,0.44], [0.44,0.50], [0.50,0.555], [0.555+])
with 10k unique windows per bin. Random orientation. Seed=42.

## Result — FIRST PLATEAU BREAK
- eval_01 = **0.1367**  (003: 0.1341, +0.003 — NEW BEST)
- mean of evals = 0.1308 (003: 0.1281, +0.003)
- K562: 0.038 (003: 0.037)
- HepG2: 0.174 (003: 0.169, +0.005)
- SK-N-SH: 0.198 (003: 0.196)
- eval_03: 0.138 (new max)
- eval_12: 0.138 (new max)

## What this means
Explicit compositional breadth helps. Stratified sampling
oversamples the rare GC tails that chr22 random under-represents,
giving the model more examples at compositional extremes. The
model benefits modestly but consistently.

This is the FIRST design that beats chr22 random in 9 experiments.

## Theory update
"Match the natural distribution" is wrong. The correct rule is
"cover the FULL compositional space, including underrepresented
tails." Natural sampling underweights extremes; stratified sampling
explicitly upweights them.

## What to try next
013: more granular stratification (10 bins × 5k). Tests if more
bins extracts more benefit, or if 5 bins captured most of it.
