# Experiment 005 — 1st-order Markov human-like (CpG-depleted)

## What I tested
50K seqs from a 1st-order Markov model with approximate human dinucleotide frequencies. Key feature: P(G|C) = 0.05 (heavy CpG depression), other dinucs roughly uniform.

## Result
eval_01: 0.331 → **0.169**. Score dropped by HALF.
Every single eval dropped substantially. eval_07 went 0.420 → 0.191.

## Interpretation
Hugely informative negative result. The scorer is NOT rewarding "natural-looking DNA". Random uniform i.i.d. is far better than natural-DNA-like sequences. This contradicts the most common assumption for MPRA-style models (trained on real sequences → should like real sequences).

Three possible explanations:
1. **Independence matters.** Random uniform has zero within-sequence correlation. The Markov chain introduces positional correlations that may break some assumption of the scoring metric (e.g., correlations across positions reduce some kind of independent-feature signal).
2. **k-mer balance matters.** Random uniform has nearly-balanced k-mer counts. The CpG depression creates a non-uniform k-mer distribution, which may correlate with sequence prediction in ways the metric penalizes.
3. **Scorer trained on uniform random oligos.** Maybe the underlying MPRA datasets are themselves synthetic libraries of random 200bp oligos (which is how many MPRA experiments are actually run). In that case, uniform random IS the in-distribution case.

## Theory update → T3
The scorer is OOD-sensitive but in the OPPOSITE direction from what I expected: uniform random is in-distribution, natural DNA is OOD.

T3: The reference / target distribution for the scorer is something close to uniform i.i.d. random 200bp DNA. Anything that introduces structure (motifs at fixed positions, GC bias, dinucleotide bias) moves us OOD and reduces correlations.

**Corollary:** If T3 is right, the route to higher scores is NOT through biologically-meaningful sequences but through finding what specific variant of "near-uniform-random" is best. Possibly perfectly balanced k-mer libraries, or libraries with very controlled statistical properties.

## Next
Exp 006: Test the "motifs preserve variance when randomly placed" idea. Sprinkle one of several common TF motifs at random positions in each random seq. If T3 is right, this still hurts (motifs disrupt uniform-random statistics). If motifs are actually rewarded when variance is preserved, score goes up.
