# 006 — DNase peaks + dinucleotide-shuffled controls

25k DNase peaks (K562/HepG2/SK-N-SH mix) + 25k dinucleotide-preserving shuffles. Provides explicit pos/neg contrast with matched composition.

**Predicted:** Modest signal (mean_r 0.1-0.3) from learning real vs shuffled.
**Got:** mean_r -0.002. Still essentially zero.

**Interpretation:** Either the simulator gives similar (noisy) activity for both real and shuffled, OR the model can't extract the contrast in its training budget.

**New direction:** test whether DUPLICATION of sequences (replicates per unique sequence) helps. If MPRA measurements are stochastic per-line, replicates clean labels.
