# 016_tight_perbase_sigma1

## Hypothesis
Each per-seq base count drawn from N(50, σ_target ≈ 1.3), independent across bases, mean-centered so sum = 200. Per-seq A count empirical std ≈ 1.33 (vs binomial 6.12).

If T6' (per-base variance plateau extends to tight): r ≈ 0.398.
If smooth decline 012 → 001: r ≈ 0.27.

## Result
- **eval_01 mean_r = 0.1862** (K562=0.3608, HepG2=0.1871, SKNSH=0.0106)
- Way below random uniform (0.398) but well above 012 (0.024).

## Interpretation
The per-base count variance lever is a steep curve from σ=0 to σ≈6, NOT a wide plateau. T6' is partially refuted: per-base variance has to be HIGH (binomial-level or above) to score on plateau.

Updated per-base count variance curve (eval_01):
- σ_perbase = 0:    0.024  (012)
- σ_perbase = 1.3:  0.186  (016 ← new)
- σ_perbase = 5-6 (binomial): 0.398  (001)
- σ_perbase ≈ 7 (slightly inflated): 0.399 (014)

Implication: the eval seems to use **per-seq feature predictions where per-base variance dominates**. Tighter per-base variance → less diverse per-seq predictions → lower correlation between two predictor models. The cliff is steep because dynamic range matters proportionally.

## Comparison to 015
- 015 only constrained GC TOTAL → per-base counts still binomial-spread → score = 0.398
- 016 constrained EACH base count tightly → score = 0.186

Confirms: the eval cares about **per-base count variance** (each ACGT independently), not just GC variance. 015 worked because A, C, G, T counts all still had std ~5 even though GC total was tight.

## Next
- The variance story is now well understood. The plateau is at per-base count std ~ 6 (binomial level).
- Pivot to orthogonal levers: per-position structure (017), dinucleotide bias, k-mer composition.
- 017 already launched: per-position bias rotating ACGT favored, library-uniform marginals.
