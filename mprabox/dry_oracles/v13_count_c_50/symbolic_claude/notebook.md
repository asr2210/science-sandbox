# Lab Notebook — String Optimization

## 2026-06-02 21:05 — Setup and initial strategy

### Task
- Black-box scoring of 50,000 strings, length 200, alphabet {0,1,2,3}
- 30 submissions total
- 14 eval sets; eval_01 is primary
- Cannot read prepare.py

### Initial theory (working hypothesis)
Unknown. The alphabet size of 4 and library structure suggests this may be
related to biological sequence design (e.g. DNA over ACGT mapping to 0123),
which often rewards specific motifs, GC-content, or k-mer compositions.
But I should NOT assume that. Start agnostic.

### Strategy
Probe phase (Exps 1-6): establish baselines and discover what matters.
- 001: uniform random — pure baseline
- 002-005: single-character constant strings (all 0, all 1, all 2, all 3) to
  see if any character is intrinsically rewarded
- 006: try a deliberately diverse library
Then refine based on results.

Multiple eval sets may reward different things, so a single library cannot
optimize all. eval_01 is primary; track all 14 but optimize for eval_01.

## 2026-06-02 21:05 — Plan: Experiment 001 (uniform random baseline)

Generate 50,000 strings of length 200 by sampling each character iid from
{0,1,2,3} with equal probability. This is the no-information baseline.
Prediction: middling scores across all evals; gives us the reference point.

## 2026-06-02 21:30 — Exp 002-004 results & theory revision

### Exp 002 (4 constant strings × 12500 copies): ALL NaN
Critical leak: `ConstantInputWarning` reveals metric is Pearson r.
mean_r = mean(r_a, r_b, r_c), where each r is a correlation across 50000 sequence-level values.

### Theory revision
The score is NOT a per-sample reward. It's a correlation between TWO arrays of
per-sequence values (likely two predictor outputs, or predictor vs ground truth).
To maximize:
- High variance in per-sequence prediction (so correlation can be high)
- High agreement between the two predictors on the rank-ordering

### Exp 003: Dirichlet(0.5) per-sequence compositions
eval_01: 0.1451 → 0.3604 (+0.21). Composition variance helps a LOT.
But eval_08 dropped 0.5795 → 0.2070.

### Exp 004: Dirichlet(0.1) — more extreme
eval_01: 0.2816. WORSE than 0.5. Sweet spot exists.
Probably: extreme compositions are OOD for predictors → noisy → low correlation.

## 2026-06-02 21:35 — Plan: Exp 005 (Dirichlet(0.3))

Bracket the composition-variance optimum. alpha=0.5 was peak; alpha=0.1 too extreme.
Try alpha=0.3 (between). Then plan next experiment based on whether peak is at 0.3, 0.5, or higher.

## 2026-06-02 23:00 — Refined theory (after 22 experiments)

### What works (eval_01)
1. **Between-sequence composition variance** is the #1 driver. From 0.145
   (random uniform) → 0.392 (Dirichlet(2) per-seq).
2. **Smooth positional composition gradient** (linear, two endpoints from
   Dirichlet(0.5)) adds ~0.016: → 0.408.
3. **Light Markov mixing** (weight 0.2, Dirichlet(0.5) rows) on top of
   gradient adds another ~0.004: → 0.4115 (current best).

### What DOESN'T help
- Extreme per-seq compositions (Dirichlet < 0.3) → OOD penalty
- 4-corner hard clusters → smoothness matters
- Heavy Markov (weight ≥ 0.5) → dilutes composition signal
- Embedded motifs → no boost beyond composition
- Compositional random walk → LLN kills between-seq variance
- Multi-control-point gradient → no help

### Condition behaviour (eval_01)
- condition_a: HIGH with positional gradient (a sees position-dependent comp)
- condition_b: HIGH with Markov-like patterns
- condition_c: HIGH with both, smoother

### Champion recipe (so far)
gradient (Dirichlet(0.5) endpoints) + Markov weight 0.2 with Dirichlet(0.5) rows.
Implementation: exp 019.

### Plan for remaining ~8 experiments
- Refine champion slightly (a few variations)
- Try a creative idea or two
- Final champion submission

## 2026-06-02 23:45 — Final summary (after 30 experiments)

### Final champion: exp 030 → eval_01 = 0.4152

Recipe:
- N=50,000 sequences, L=200, alphabet {0,1,2,3}
- Per-seq: c_start, c_end ~ Dirichlet(α=0.5)
- Per-seq: Markov transition matrix T (rows ~ Dirichlet(α=0.25))
- base(t) = (1-t)*c_start + t*c_end, t = pos/(L-1)
- mix(t) = 0.2 * T[prev] + 0.8 * base(t)
- Sample position t from Categorical(mix(t))

### Trajectory of eval_01 best
- 001 uniform random: 0.1451
- 003 Dirichlet(0.5): 0.3604 (+0.215, between-seq composition variance)
- 007 Dirichlet(2.0): 0.3917 (alpha sweep optimum for plain Dirichlet)
- 013 smooth gradient α=2.0 endpoints: 0.3953
- 014 gradient α=1.0: 0.4066
- 015 gradient α=0.5: 0.4078
- 019 gradient + Markov w=0.2 (α=0.5 rows): 0.4115
- 023 Markov rows α=1.0: 0.4121
- 025 Markov rows α=0.3: 0.4128
- 026 Markov rows α=0.2: 0.4131
- 030 final (rows α=0.25, new seed): **0.4152**

### Final ranking of recipe components (cumulative gain on eval_01)
1. Between-seq composition variance via Dirichlet(0.5) per-seq:  +0.215
2. Smooth linear gradient (2 endpoints):                          +0.047
3. Light Markov mixing on top (w=0.2, sharp rows α≈0.25):        +0.007
Total: 0.145 → 0.4152

### What I learned about the task
- Metric is Pearson r (leaked from `ConstantInputWarning` in exp 002).
- mean_r = mean(r_a, r_b, r_c) for each eval_NN.
- 5 duplicate eval pairs: 01=14, 02=05, 03=12, 04=09, 06=11.
- eval_08 anti-correlates with our optimization direction (uniform random
  scores 0.5795, our champion scores 0.27). Some condition rewards
  uniformly-mixed sequences. We accept that loss since eval_01 is primary.
- eval_07 and eval_13 climb fastest with our recipe (cond_a-heavy).
- condition_b is the consistent laggard across our experiments — it likely
  rewards within-seq Markov structure more than between-seq composition.

### Things that didn't pan out
- Dirichlet alpha < 0.3 (too extreme, OOD)
- 4-corner / hard clusters (smoothness matters)
- Markov weight ≥ 0.3 (dilutes composition)
- Compositional random walk (LLN ate between-seq variance)
- Embedded motifs (no gain)
- 3-control-point gradient (worse than 2-point)
- Sigmoidal gradient (worse than linear)
- Endpoint α ≥ 0.7 (less between-seq variance)

### Final submission
libraries/030_champion_final/sequences_0.txt
eval_01 = 0.4152
