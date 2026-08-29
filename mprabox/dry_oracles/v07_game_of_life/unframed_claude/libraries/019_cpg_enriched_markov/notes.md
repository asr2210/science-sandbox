# 019_cpg_enriched_markov

## Hypothesis
Doubly-stochastic Markov chain biasing C→G (0.40) and G→C (0.40) transitions while keeping stationary mononucleotide distribution exactly uniform 0.25 each. Per-seq mononuc stats nearly identical to random uniform; only dinucleotide composition shifts (CG dinuc count ≈ 20 vs uniform expected 12.4).

Tests if dinuc lever can help or hurts. Prior dinuc experiments (007, 010) hurt — and 019 biases a specific chemically active dinucleotide.

## Result
- **eval_01 mean_r = 0.2934** (K562=0.4531, HepG2=0.3211, SKNSH=0.1060)
- **Big drop**: -0.105 vs random uniform. CpG enrichment hurts a lot.

## Interpretation
Dinucleotide composition is a STRONG lever — even with matched mononucleotide marginals, biasing the dinuc distribution moves the score significantly. This means T7 needs refinement:

**T7'**: The eval's per-sequence predictions use BOTH mononucleotide and dinucleotide composition features. Random uniform's natural dinuc distribution (each dinuc ~ 12.4) is near-optimal. Shifting any dinuc away (either direction, biased or suppressed) hurts.

This means: random uniform i.i.d. is optimal across BOTH mononuc and dinuc axes. There's no easy "fix" that pushes above 0.398.

## Bigger picture
After 19 experiments, only random uniform (and near-variants on the plateau) score ~0.398. Every structural deviation tested has hurt:
- Bio content (002, 003): -0.005
- Motifs (008): -0.013
- Markov repeat (010): -0.009
- High complexity / no runs (007): -0.023
- Mixing (013): -0.009
- CpG enrichment (019): -0.105
- Tight per-base variance (016): -0.21
- Exact 50/50/50/50 (012): -0.37
- Bimodal GC (004): -0.058

Random uniform is the global optimum on the lever axes I've tested.

## Next
- 020 (running): replicate 014 (slight upward bump) with different seed.
- 021+: confirm submission strategy.
