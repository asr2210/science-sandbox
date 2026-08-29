# 009 — 25k Markov-2 + 25k uniform random

## Hypothesis
If two-mode hybrid lift is generic, this should also beat each parent. If
specific to strict+random, this will fall back.

## Setup
25,000 Markov-2 (human dinuc freqs) + 25,000 uniform random, interleaved.

## Result
- eval_01 mean=**0.7739** (K562 0.839, HepG2 0.871, SKNSH 0.612)
- Better than pure Markov (0.717) — SK-N-SH lifted from 0.42 to 0.61.
- Worse than pure random (0.849) — Markov drags overall.
- Much worse than strict+random hybrid (0.878).

## Interpretation
The hybrid-lift effect is real for any two distinct designs (SK-N-SH improved
partially), but the absolute score depends on the parent designs' qualities.
Strict was a good complement to random because strict beats random on
K562/HepG2 individually. Markov has weaker per-cell-line ceilings.

## Next
- 010-011: ratio sweep around 007's 25/25 strict/random.
- 012+: try adding a small third mode that's gentle on all heads.
