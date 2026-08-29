# Lab Notebook

## 2026-06-02 — Initial setup

### Problem summary
- Black-box scoring function over 50,000 strings of length 200 from alphabet {0,1,2,3}.
- 14 eval sets (eval_01..eval_14), primary is eval_01.
- 30 submissions total. result.json reveals score after each.
- Cannot read prepare.py.

### Initial theory
Unknown. The alphabet size of 4 over 200-length strings is suggestive of:
- DNA-like motif scoring (ACGT)
- Information-theoretic measures (entropy, complexity)
- Pattern/repetition rewards
- Specific motif matching (k-mer frequencies)

Possible mechanics for the score function:
1. Reward strings matching some hidden motif (per-sequence score)
2. Reward library-level diversity (collective property)
3. Reward k-mer frequency matching some hidden distribution
4. Reward specific character composition or GC-content analog
5. Reward distance from some hidden target sequences

The 14 eval sets suggest multiple independent metrics — so I need to explore broadly to identify what matters.

### Strategy for first probes
With 30 submissions, I'll spend early ones learning the function:
- Exp 001: All-zeros — establishes a degenerate baseline (zero diversity, zero entropy)
- Exp 002: Uniform random — natural baseline (max entropy)
- Exp 003: All sequences identical but mixed alphabet
- Exp 004: Each sequence one of 4 single-char rows (4 distinct rows repeated 12,500 times each)
- Exp 005: Periodic pattern (e.g., "0123" repeated)

These will reveal whether function rewards diversity, entropy, specific patterns, or something else.

## 2026-06-02 14:00 — Final summary (experiments 001-030 complete)

### Score progression (eval_01)
| Rank | Exp | Score | Method |
|------|-----|-------|--------|
| 1 | 010 | 0.0784 | bigram-Dir(α=0.3), seed=23 |
| 2 | 016 | 0.0782 | exact-count Dir(0.3) |
| 3 | 009 | 0.0779 | mix Dir(0.1,0.3,1.0,3.0) |
| 3 | 030 | 0.0779 | 4-seed bigram-Dir(0.3) mix |
| 5 | 018 | 0.0776 | asymmetric Dir bimodal |
| 6 | 025 | 0.0776 | 25K bigram-Dir+25K grid |
| 7 | 006 | 0.0774 | Dir(0.3) per-seq |
| 8 | 023 | 0.0771 | Dir(0.2) |
| 8 | 024 | 0.0771 | bigram-Dir mix alphas |
| 10 | 013 | 0.0770 | Dir(0.3) sorted by q0 |
| 10 | 014 | 0.0770 | Dir(0.5) |
| 10 | 020 | 0.0770 | bigram-Dir(0.5) |
| ... | ... | ... | ... |
| | 022 | 0.0769 | uniform simplex grid |
| | 002 | 0.0648 | uniform random (baseline) |
| | 008 | 0.0405 | homopolymers |
| | 005 | -0.005 | identical-composition shuffles |
| | 001,004 | NaN | constant input |

### Theory (refined through 30 experiments)
1. **Score is library-level, not per-sequence.** A single library produces 14
   correlation-like scores comparing some library-level statistic to hidden
   targets. The "ConstantInputWarning" surfaced in exp 001/004 reveals
   `scipy.stats.pearsonr` underlies the scoring — it needs across-library
   variance to produce a finite result.
2. **The signal is purely COMPOSITIONAL.** Permutation-invariance (exp 013
   sorted = unsorted), exp 005 (shuffles of fixed composition → 0), and the
   equivalence of monogram, bigram, and trigram Dirichlets prove ordering and
   k-mer structure add ~nothing once first-order composition is set.
3. **All 4 character axes must be active.** Exp 012 (only q0+q3=1 axis,
   q1=q2=0) gave 0.0380, about HALF the score of full 4-dim Dir(0.3).
4. **The compositional ceiling is ~0.078 on eval_01.** All approaches
   varying alpha, mixture, simplex coverage, and bigram structure cluster
   between 0.075-0.078. The +21% advantage over uniform random (0.0648)
   represents most of the recoverable signal in the compositional axis.
5. **Seed variance is non-trivial (~±0.001-0.002).** bigram-Dir(0.3) seeds
   gave: 23→0.0784, 99→0.0769, 151→0.0761. The 0.0784 is a +1.5σ outlier;
   the population mean is ~0.077.

### Eval pair structure
Identical scores to 4 dp on pairs (01,14), (02,05), (03,12), (04,09),
(06,11). Unique evals: 07, 08, 10, 13. So there are effectively ~9 distinct
eval signals.

### Cross-eval observations
Different methods optimize different evals:
- eval_01 (primary): bigram-Dir(0.3) wins
- eval_07: uniform-simplex-grid wins (0.1479)
- eval_08: uniform-simplex-grid (0.0753) > bigram-Dir
- eval_10: uniform-simplex-grid (0.1318) > bigram-Dir
This suggests multiple correlated-but-distinct signals; aggregating could
boost a sum-metric but not eval_01 alone.

### Best library
**Exp 010 / bigram-Dir(α=0.3), seed=23, mean_r=0.0784.**

### What I would try with more budget
- Sample 20+ bigram-Dir(0.3) seeds and pick the highest-scoring one
  (since seed variance dominates ~25% of the residual gap).
- Try variance-reducing constructions: control simplex coverage exactly
  while preserving bigram-Dir composition distribution.
- Score AVERAGING across multiple library samples for the same method to
  reduce noise floor and detect smaller effect sizes.
