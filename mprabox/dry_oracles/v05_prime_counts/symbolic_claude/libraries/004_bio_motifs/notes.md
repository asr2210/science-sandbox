# 004 — Biological-style motifs inserted (one mapping guess)

## Setup
Assumed mapping 0,1,2,3 → A,C,G,T. Inserted 4 canonical TF binding consensuses
(TATA, GC-box, E-box, AP-1) into each of 50K uniform-random length-200
sequences at random non-overlapping positions. 25 bp motif content per seq
(~12.5% coverage).

## Results
- eval_01 = 0.0402 (vs baseline 0.0420; Δ ≈ −0.002)
- eval_08 = 0.1000 (vs baseline 0.1242; Δ ≈ −0.024)
- All evals essentially indistinguishable from baseline

## Inference
- Bio-style motif content under this mapping at 12.5% coverage doesn't move
  the score
- Either: mapping is wrong, or motif content at this coverage is not what the
  score rewards, or the score isn't motif-sensitive in this way
- Combined with exp 003 (simple repeats also flat), insertion-based motifs
  don't seem to help much in general
