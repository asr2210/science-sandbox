# Experiment 025 — closer flanks (1000-2000bp)

## Design
- 013 ratio: 15K uniform + 5K CTCF + 5K DNH3 + 25K paired flanks
- ONLY change: flank distance band 1000-2000bp (vs 1500-3000 in 013)

## Result — mean_r 0.157 (worse than 013's 0.166)
- eval_06/11 = 0.216 (close to 013's 0.218!)
- eval_10 = 0.136 (down from 013's 0.151)
- eval_13 = 0.125 (similar)
- eval_07 = 0.141 (down from 013's 0.177)
- eval_08 = 0.049 (slight lift from 013's 0.036)

## Interpretation
Sweep result: flank distance 1500-3000 IS the peak.
- 1000-2000: preserves eval_06/11 but loses eval_07/10
- 1500-3000 (013): balanced peak
- 3000-6000 (024): loses eval_06/11

Closer flanks make eval_06/11 easy (still high CTCF/local-context
contrast), but eval_07 needs varied negatives at distance to learn
broader motif signatures. The 1500-3000 band is the unique trade-off.

## Next
026 = NEW direction. Tried positives (014, 015, 023), tried flanks
distances (016, 018, 024, 025), tried negatives (017, 022). Test
dinucleotide-shuffled per-positive negatives: each positive paired
with its OWN dinuc-shuffled sequence as the negative. Removes
ALL spatial structure while preserving local composition.
