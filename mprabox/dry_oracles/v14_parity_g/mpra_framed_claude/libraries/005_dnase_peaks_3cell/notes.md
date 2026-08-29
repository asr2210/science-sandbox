# 005 — DNase peaks from K562/HepG2/SK-N-SH

50k = 16,667 × 3 from ENCODE DNase narrowPeak files for the three target cell types. 200bp centered on each peak center.

**Predicted:** Strong signal (mean_r 0.2-0.5) since these are guaranteed active in the eval cell types.

**Got:** mean_r ~0.0015. eval_08 = 0.0063 (highest yet, still tiny). All ~0.

**Critical insight:** Even directly providing known active regions from the EVAL cell types doesn't give the model anything to learn. This rules out "library needs active sequences" as the sole bottleneck.

**Conclusion:** the model needs explicit contrast (positives vs negatives) or much more concentrated motif signal to extract signal in its training budget.
