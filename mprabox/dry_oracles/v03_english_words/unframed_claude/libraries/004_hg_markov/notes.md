# 004 — hg38-like Markov Chain

## Hypothesis
"Realism" by 1st-order Markov chain matching hg38 dinucleotide frequencies
(notably CpG depletion) should beat random uniform if in-distribution composition
matters.

## Method
50k sequences from a 1st-order Markov chain with transition probabilities
fitted to published hg38 dinucleotide frequencies (CG ≈ 0.01, others ~0.05-0.10).

## Result
- eval_01 mean_r = **0.4072** (vs 0.4200 random)
- K562: 0.568 (−0.020), HepG2: 0.591 (−0.027), SKNSH: 0.062 (+0.009)

## Interpretation
Realistic dinucleotide composition slightly HURT K562/HepG2, slightly helped
SKNSH — but net negative for mean.

Combined with exp 002 (motifs hurt) and exp 003 (GC gradient hurt much more),
the picture is clear: K562/HepG2 r is maximized at *uniform i.i.d.* random
composition. Any structured bias reduces it.

But notice SKNSH crept up here. SKNSH seems to respond to "more biological"
sequences differently than K562/HepG2.

## Next
Try real MPRA sequences from the Malinois training data. Test whether
genuinely in-distribution sequences (not just composition-matched) can lift
SKNSH r dramatically.
