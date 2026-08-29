# Exp 010: ENCODE cCRE-centered windows

**Hypothesis**: Real regulatory elements should score higher than random
genomic windows because they're enriched for active enhancer/promoter
motifs the model was trained to recognize.

**Method**: 1,063,878 ENCODE cCREs (BED). Found 42,852 cCREs in our 127 Mb
of genome data. Took 200bp window centered on each cCRE midpoint. Padded
to 50k via jittered windows.

**Results**:
- eval_01: 0.3898 (vs random 0.4203, natural 0.3975, cCRE WORSE)
- K562: 0.5428 (vs random 0.585)
- HepG2: 0.5590 (vs random 0.618)
- SKNSH: 0.0676 (vs random 0.059) → modest +0.009

**Interpretation**: cCREs score similar to or worse than random genomic
windows. Even REAL regulatory elements don't beat random. This is striking
evidence that the metric does NOT simply reward "high model-predicted
regulatory activity". 

**Theory v3**: The mean_r metric is correlation between predicted and
"reference" activity across 50k sequences. The reference distribution
likely matches random sequence statistics — so random libraries fit best.
Anything with structure (natural, cCREs, motifs) deviates from this
distribution and yields lower correlation, even if individual sequences
are biologically "more active".

**Implications**: Beating random requires a SUBTLE perturbation that
preserves the reference-matching properties. The +0.003 lift from
Exp 002 (3 broad motifs) is the only above-baseline result so far.
Next: test if that signal is real or just noise.
