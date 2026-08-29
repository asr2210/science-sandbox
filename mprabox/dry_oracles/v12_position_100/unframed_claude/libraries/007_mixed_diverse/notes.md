# 007 mixed_diverse

**Design:** 10k each from random_uniform, dinuc_markov, genome random windows, K562 DHS centered, motif-dense synthetic. Shuffled. Tests diversity hypothesis.

**Result:** eval_01 = 0.0700. Worse than several pure libraries. Diversity per se does not help.

**Updated:** every 50k library (random, dinuc, genome, TFBS, K562 DHS, motif-dense, mixed) lands in 0.064-0.077 for eval_01. The score is saturating. Two new explanations to test:
- Maybe prepare.py noise is on the order of 0.01 and these libraries are statistically indistinguishable.
- Maybe a fundamentally different library structure is required.

Next: noise check (re-run 001 — but that wastes an experiment slot). Better: skip noise test and pivot to a totally different library type (e.g., very-low-complexity dimer / tandem-repeat libraries) to see if the score is moved at all.
