# Exp 017 — Gene-desert with 1kb cCRE buffer

## Design
Same as 016 but 1kb (vs 100bp) exclusion buffer around every cCRE.
61.7% of genome remains accessible. GC=0.390; CpG=0.0082.

## Result
**eval_01 = 0.0468; HepG2 = 0.0526.** Slightly worse than 016 across the board.

| metric | 016 (100bp) | 017 (1kb) |
|--------|-------------|-----------|
| eval_01 | 0.0479 | 0.0468 |
| HepG2 | 0.0556 | 0.0526 |
| eval_13 | 0.0384 | 0.0333 |

## Interpretation
Deeper exclusion costs more than it gains. The 016 HepG2 lift came from
removing direct cCRE windows, not from sweeping a wider neighborhood. The
neighborhood IS regulatory-context-relevant DNA; removing it shrinks
effective sample space without removing the bias source.

## Theory update
- 100bp buffer is sufficient for the cCRE-removal signal.
- Beyond that, diversity loss dominates.
- HepG2 lift from gene-desert is real but bounded (≤0.003 mean).

## Next step
Try combining gene-desert (helps HepG2) with a light cCRE enrichment
(helped eval_01 +0.001) in 013. Test 40K gene-desert + 10K cCRE — does
each contribute additively?

## Time
44s wall, 13s evaluator.
