# Scoring function — what we know

Black-box scoring of a library of 50,000 strings of length 200 over {0,1,2,3}.

## Confirmed facts
- **mean_r is a Pearson correlation.** Submitting identical sequences
  produces `ConstantInputWarning` from `scipy.stats.pearsonr` and NaN
  scores everywhere (exp 002).
- There are 14 reported evals (eval_01..eval_14) with three sub-scores
  each: condition_a, condition_b, condition_c, plus the mean mean_r.
- Several eval slots are exact duplicates of one another. From the
  uniform random baseline (exp 001):
    eval_01 == eval_14
    eval_02 == eval_05
    eval_03 == eval_12
    eval_04 == eval_09
    eval_06 == eval_11
  → 9 distinct underlying evals replicated to 14 slots.
- eval_01 is the primary metric.
- Uniform random baseline (exp 001) scores ~0.48 on most evals, ~0.52
  on eval_07, and only 0.16 on eval_08.
- Condition c is systematically the weakest of {a, b, c}.
  Condition a is systematically the strongest.

## Inferred (not confirmed)
- The eval pipeline likely runs a model on each sequence to predict an
  activity vector (over conditions, positions, or replicates), then
  compares against a target vector via Pearson r per sequence, then
  averages over the library to produce `mean_r`.
- Identical sequences likely produce a constant predicted vector for
  the axis r is computed across.
- The directory name MPRAgent suggests MPRA (Massively Parallel Reporter
  Assay) — biological regulatory DNA prediction. {0,1,2,3} likely maps
  to {A,C,G,T} though we have not confirmed which order.

## Hard rules
1. Never submit a library of identical strings — score is NaN.
2. Maintain diversity within the library. Distinct sequences are safer.
3. Every sequence should contain all four characters (avoid sequences
   that are themselves monochromatic).

## Files
- `prepare.py` is the harness entry point — DO NOT read/inspect.
- The eval code lives in `eval/harness.py` (we have seen the path in
  warning output: `eval/harness.py:111`). We will NOT read it.

## Cost
- ~50s wallclock per submission; ~24s of actual scoring + ~26s overhead.
- 30 total submissions allowed.

## What we've learned about composition

The scoring is strongly composition-sensitive AND ASYMMETRIC along the
GC↔AT axis (under assumed mapping {0,1,2,3} = {A,C,G,T}).

- Uniform composition (25/25/25/25): eval_01 = 0.485 (best)
- Mild AT bias (30/20/20/30): eval_01 = 0.467 (-0.018, very gentle drop)
- Mild GC bias (20/30/30/20): eval_01 = -0.241 (catastrophic)
- Single-char bias (55/15/15/15 avg over 4): eval_01 = 0.400

For PRIMARY eval_01, uniform composition is near-optimal. AT-bias has
a very gentle penalty; GC-bias is brutally bad.

For evals 07, 13: AT-bias gives big lifts (+0.19) but eval_01 is the
primary metric.

## What we've learned about dinucleotide structure

Decoupled from composition:
- Auto-correlated (P(same)=0.5, uniform marginals): -0.20 on eval_01
- Anti-correlated (P(same)=0.0, uniform marginals): -0.24 on eval_01

Uniform random dinucleotide structure is at a sharp peak. Both
directions hurt. Adding "human DNA" dinucleotide structure on top of
matched composition adds only ~+0.01 (i.e., is essentially noise).

## What we've learned about evals
- 14 eval slots, 9 distinct: pairs {01,14}, {02,05}, {03,12}, {04,09},
  {06,11} are identical.
- Eval_01 is primary.
- Three response groups by composition:
  * Group A (likes AT): 03, 07, 10, 13
  * Group B (mildly prefers uniform): 01, 02, 06
  * Group C (strongly prefers uniform): 04, 08
- Condition order: a > b > c in score, consistently.

## Confirmed alphabet mapping
**{0,1,2,3} = {A,C,G,T}** (alphabetical).

Verified by: prepare.py rewrites sequences_0.txt, converting our digits
to DNA letters. After exp 001 ran, file contents are pure ACGT, with
digit 0 → A, 1 → C, 2 → G, 3 → T.

## Inferred scoring mechanism

Most consistent with observations:
- For each (eval, condition) pair, scoring computes Pearson r ACROSS
  the 50K sequences between two per-sequence vectors:
    predicted_activity[i] (model output for sequence i)
    target[i]             (depends on per-sequence composition/feature)
- mean_r per eval = average over the 3 conditions.

Evidence:
- Monochromatic (exp 002): NaN. Predicted may be constant within
  sub-library; correlation across sub-libraries breaks.
- Forced 50/50/50/50 per-seq (exp 009): NaN even though all sequences
  are distinct. Target depends on per-sequence composition → constant
  → NaN.
- Composition shifts (exp 003, 006, 007, 008) give clean numeric
  responses — predicted varies in a way that aligns or misaligns with
  the target.

## Open knobs to test
- Per-sequence composition variance (vs baseline iid's natural variance)
- Higher-order k-mer structure with neutral composition
- Specific motifs / palindromes / regulatory elements
- Heterogeneous libraries combining strategies
- Position-specific structure within sequences
