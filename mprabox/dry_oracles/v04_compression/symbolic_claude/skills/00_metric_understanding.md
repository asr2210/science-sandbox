# Skill: Understanding the metric

The scoring function in this project is **Pearson correlation between a
learner's predictions on held-out eval sequences and oracle labels**. The
learner is fit by the harness using our 50K submitted sequences (X) plus
oracle-generated labels y = O(X).

Evidence:
- 002 (50K identical sequences) → NaN, with explicit warning
  "ConstantInputWarning: An input array is constant; the correlation
  coefficient is not defined."
- 007 (12.5K each of 4 homopolymers) → also NaN. Even with 4 distinct
  inputs the learner's predictions on the diverse eval set collapse to a
  constant.
- Score for random uniform ≈ 0.30 means the learner can extract _some_
  signal (likely composition) but is far from saturating.

## Implications for sequence design

1. **Diversity is essential.** 50K unique > 1K unique (003: 0.17 vs 001:
   0.30). Treat near-duplicates as wasted slots.
2. **Use the full alphabet.** Restricting to {1,2} or {0,3} drops the
   score sharply (004: 0.019, 005: 0.16). The learner needs to see all
   four characters in varied contexts.
3. **Avoid per-sequence composition skew.** A linear sweep of GC fraction
   (006) underperformed iid uniform.
4. **Random uniform is a strong baseline (≈0.30).** Any modification
   needs to preserve diversity + alphabet coverage.
5. **NaN-prone shapes**: all-identical, all-homopolymer, anything where
   the learner can map 50K → very few distinct internal patterns.

## What to test next

To push above 0.30 we likely need:
- Sequences that better match the oracle's training distribution
  (probably natural-DNA-like, given the project name).
- Embedded structural elements (motifs, repeats) so the learner picks up
  more than just composition.
- A mixture of "easy" and "hard" sequences spanning oracle's full output
  range, so the learner sees the full label distribution.
