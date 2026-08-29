# 013_motif_stuffed

chr22 real backbone + insert 3-5 strong TF motifs per sequence at random positions.
Motifs include GATA1, TAL1, MYC, NFY, SP1, AP-1, ETS, CEBP, HNF, KLF, TATA, etc.

## Result
eval_01: 0.6618 (vs 0.6780 plain chr22) — slightly WORSE.
eval_07: 0.7396 (vs 0.7462) — slightly worse.

## Interpretation
Random insertion of canonical TF motifs DOES NOT help; slightly hurts.
The predictor isn't simply pattern-matching for motif occurrences. Random
placement disrupts the natural sequence context that the predictor uses.

This suggests the predictor uses higher-order features (gapped k-mers, longer
context, motif co-occurrence patterns, evolutionary signatures) rather than
just motif presence.

## Implication
Need either (a) actual MPRA-tested sequences from the predictor's training
distribution, or (b) sequences with NATURAL motif placement (e.g., real
enhancer/promoter cores).

## Next
Look for K562 specific accessible regions / ENCODE cCRE per-cell-type data.
