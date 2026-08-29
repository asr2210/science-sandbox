# 021 — 30k strict + 20k (random+8mer 50-bank): ratio shift

## Hypothesis
Insert helps random-half; maybe optimal ratio shifted toward strict.

## Result
- eval_01 mean=**0.8756** (K562 0.8623, HepG2 0.9063, SKNSH 0.8583)
- vs 017 (25/25 split): mean -0.0064. SKNSH -0.014.

## Interpretation
Strict-heavy ratio hurts SKNSH. 50/50 multimodal balance is robust across
insert/no-insert conditions.

## Next
022: 3-mode test (strict + pure rand + insert-rand).
