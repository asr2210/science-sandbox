# Experiment 009 — maximum diversity multi-source mix

## Design
10K each of human natural / mouse natural / cCRE off-center / DHS
summits, + 5K FANTOM5, + 5K Low-DNase cCRE. Every reliable natural
source I have, balanced.

## Result
- eval_01: 0.394 (Δ -0.000 vs exp 002 4-way mix)
- K562: 0.606, HepG2: 0.429, SK-N-SH: 0.147

## Interpretation
EXACTLY 0.394, identical to the 4-way mix. T6 confirmed: the
ceiling is real and structural. Adding more diverse natural sources
adds nothing on top of "natural + regulatory enrichment."

## Implication
Library design space is exhausted within ε of 0.394. Need noise
estimate to know if 0.394 is actually better than 0.388 (natural)
or just noise.
