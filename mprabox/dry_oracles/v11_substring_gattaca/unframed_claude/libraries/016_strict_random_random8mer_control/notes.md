# 016 — Control: 25k strict + 25k (random + 1 random 8-mer per seq, from 9-bank)

## Hypothesis
If motif identity drove 014's lift, swapping motifs for random 8-mers should
crash the score. If motif identity is irrelevant, random 8-mers will match
014.

## Setup
9 fixed random 8-mers in the bank. One inserted per random-half seq at a
random position.

## Result
- eval_01 mean=**0.8805** (K562 0.855, HepG2 0.915, SKNSH 0.871)
- Essentially tied with 014 (0.8811).

## Interpretation
**Motif identity does not matter.** The lift comes from inserting a
short, consistent (composition-balanced) sequence pattern into the random
half. This creates additional structured sub-clusters within the random
subset, which interacts with the strict subset to expand the joint
prediction-truth cloud.

The 9-bank acts like 9 "labels" attached to random sequences. With 9 labels,
the random half forms 9 micro-clusters, each shifted slightly in the
predictor's latent space.

## Implications
- Could try larger banks (e.g., 100 random 8-mers) to create more
  sub-clusters and potentially bigger lift.
- Could try longer inserts (e.g., 16-mers, 32-mers) to stronger differentiate
  clusters.
- Must keep inserts COMPOSITION-BALANCED to avoid HepG2 collapse.

## Next
- 017: 3-mode mix (strict + pure random + random+8mer) — does adding
  a non-inserted random subset preserve SK-N-SH while keeping motif lift?
- 018: try larger 8-mer bank (50 inserts) to see if more clusters lift more.
- 019: longer inserts (16-mer or 24-mer).
