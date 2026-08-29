# Experiment 005 — activity contrast (active cCRE + silent gene desert)

## Design
20K cCRE PLS/pELS/dELS centered (active) + 20K natural windows >5kb
from any cCRE/DHS (silent anchors) + 10K natural random.

## Result
- eval_01: 0.393 (Δ -0.001 vs exp 002)
- K562: 0.604, HepG2: 0.429, SK-N-SH: 0.147

## Interpretation
Activity range contrast does not help beyond the 4-way mix. Even
explicitly maximizing the active/silent contrast adds nothing.

## Implication
**T2 strengthened.** Within the "good library" regime (substantial
natural + some regulatory), library design choices produce ≤±0.002
variation in eval_01. The "good library" lift over pure natural is
only ~+0.006 in v07. The 0.394 ceiling is real.

To break the ceiling I need a fundamentally different approach, or to
confirm whether the ceiling reflects model/eval constraints I cannot
move with library design.
