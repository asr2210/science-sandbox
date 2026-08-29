# Skill: Diagnosing this scoring metric

## What we learned about the metric
The score is **Pearson r between two per-sequence vectors of length N**:
- `condition_a`, `condition_b`, `condition_c` — three r values per eval
- `mean_r` = average of a, b, c (sometimes one is NaN; appears excluded)
- The metric is **permutation-invariant on the library set** (sorting by GC → same scores as unsorted)

## NaN triggers (don't ship these)
- All sequences identical → NaN across all conditions
- 2 unique extreme sequences (e.g. all-0, all-1) → c=NaN
- Alphabet restricted to 2 letters → c=NaN
- Per-sequence base counts forced equal (no compositional variance) → all NaN

## Required: per-sequence compositional variance
Random uniform sampling provides natural binomial variance over base counts.
Narrowing this distribution (rejection sampling to a tight GC window) HURTS.
Widening it (per-seq GC ∈ [0.1, 0.9]) also HURTS (over-extreme distribution).
**Leave per-seq composition alone — natural binomial is correct.**

## Score floor / noise floor
- Random uniform seed=42: eval_01 = 0.0408
- Random uniform seed=43: eval_01 = 0.0419
- → seed-to-seed noise ≈ ±0.001

## Best known structure (see skills/tandem_repeat_50x4.md)
50bp × 4 tandem repeat → eval_01 ≈ 0.042-0.043, eval_08 ≈ 0.134
