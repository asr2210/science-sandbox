# 003 — Markov-2 genome-like

## Hypothesis
Genome-like dinucleotide composition matches test sequence distribution better
than uniform → higher Pearson r.

## Setup
1st-order Markov chain with human-genome dinucleotide frequencies
(CpG-depleted, ~41% GC). Per-base composition: A 29.5%, C 20.6%, G 20.7%,
T 29.2%.

## Result
- eval_01: mean=**0.7169** (K562 0.8367, HepG2 0.8929, **SKNSH 0.4212**)
- Mean of 14 evals ≈ 0.70

## Interpretation
Worse overall — driven entirely by SK-N-SH collapse (0.84 → 0.42, sometimes
down to 0.20 on eval_07). K562 slightly up (+0.006), HepG2 up (+0.014).
SK-N-SH is **composition-sensitive** and prefers uniform 25% bases.

Possible reasons:
1. SK-N-SH-relevant regulatory features sit in high-entropy k-mer regions
   where uniform random gives broader coverage.
2. The pre-trained scoring model has been trained against synthetic random
   benchmarks for SK-N-SH; biased composition drives it off-distribution.
3. The metric is not a simple kNN/distillation; some library statistic
   (e.g., k-mer entropy) is what's being correlated with cell-line activity,
   and SK-N-SH's correlation depends on full k-mer coverage.

## Next
- 004: per-sequence variable GC (each seq drawn at a random GC ∈ [20%, 80%])
  to test if *higher-order diversity* (composition variance across seqs) helps
  without losing the average uniform composition.
