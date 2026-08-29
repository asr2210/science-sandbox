# Exp 026 — 30K random + 20K cCRE-type-balanced (4K each x 5 types)

## Design
Equal counts of PLS, pELS, dELS, CTCF-only, DNase-H3K4me3.
GC=0.449; CpG=0.0174.

## Result
**eval_01 = 0.0474; HepG2 = 0.0518.** Similar to 013/015 (cCRE-enriched
mixes).

## Interpretation
Equal weighting across cCRE types doesn't lift over the dELS-dominated
random sampling. The cCRE-type axis doesn't carry signal in this regime.

## Theory update
- The natural-DNA ceiling holds across yet another design dimension.
- Type-balance is a no-op for eval_01.

## Next step
Try a within-sequence chimeric design — half-cCRE + half-random per 200bp.
Tests whether MPRA-cassette-like sequences (active element in random
flank) match the eval distribution better than centered cCREs alone.

## Time
44s wall, 13s evaluator.
