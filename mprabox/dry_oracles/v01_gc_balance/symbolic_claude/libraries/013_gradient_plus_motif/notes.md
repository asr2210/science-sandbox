# 013_gradient_plus_motif

## Setup
009-style composition gradient (det counts, random shuffle) PLUS up to 15
insertions of "0123" motif at non-overlapping random positions, count
proportional to row index.

## Results
- eval_01: 0.4698 (009 was 0.6010, drop 0.131)
- eval_07: 0.5282 (009 was 0.6685, drop 0.141)
- All evals dropped

## Interpretation
Inserting the "0123" motif at "random" positions (with overlap-avoidance and
proportional density) introduces structured patterns the model treats as
anti-active or anomalous. Even though per-position composition should be
preserved on average, the model picks up on the periodic placement
constraints.

## Rule learned
Don't insert specific known motifs at random/regular positions unless you
have strong reason to believe the motif is activating. Random-shuffle of
composition counts is much safer.

## What's left to try
- Push composition gradient endpoints to extreme (min=1)
- Find what specific motifs HELP (very hard without model knowledge)
- Different row-index-correlated features (k-mer counts, run lengths)
- Multi-seed averaging
