# Scoring Function Observations

## Structure
- `prepare.py libraries/NNN/` scores `sequences_0.txt` (50,000 lines of length 200)
- 14 eval sets, eval_01 primary
- mean_r = (cond_a + cond_b + cond_c) / 3 (verified)
- Scoring time: ~14-50s. Random takes longest; biased/structured shorter
- Deterministic given a library

## Eval duplicates (random seed=42 baseline)
- (01, 14), (02, 05), (03, 12), (04, 09), (06, 11) appear identical
- 07, 08, 10, 13 are singletons
- eval_08 always lowest (~0.05 below others)

## Per-condition findings

### cond_a (~0.99 at best)
- Random uniform: a ≈ 0.99 (near-optimal)
- Markov runs (STAY=0.55): a → 0.72
- Markov anti-self (STAY=0.20): a → 0.95
- Single-base bias: a → 0.63
- Exact 50/50/50/50 per seq: a ≈ 0.99 (unaffected by per-seq balance)
- Palindromes: a ≈ 0.99 (palindromes preserve k-mer freq)
- Dinuc depletion: a → 0.95
- No self-transitions (zero same-base dinucs): a = NaN (UNDEFINED for missing k-mers)
- **Conclusion:** cond_a rewards near-uniform k-mer distribution at multiple orders.
  Truly random is near-optimal. Any structure costs. Constraint: NO k-mer can be
  totally absent (a goes NaN).

### cond_b (~0.56 at best)
- Random uniform: b ≈ 0.56 (near-optimal)
- Exact 50/50/50/50: b → -0.11 (REMOVING per-seq variance hurts)
- Per-seq strong bias: b → -0.36 (TOO MUCH variance hurts)
- Palindromes: b → 0.05 (symmetric structure hurts)
- Markov runs: b → 0.51
- Motif insertion: b ≈ 0.56-0.57 (mild change)
- **Conclusion:** Goldilocks zone. i.i.d. uniform sampling gives natural per-seq
  compositional variance ±6 counts that b loves. Less or more variance hurts.

### cond_c (~0 ± 0.01 always)
- Random uniform seed 42: -0.0065
- Random uniform seed 7: +0.0114
- All structured variants: c stayed in -0.01 to +0.01 range
- **Conclusion:** c is robustly near zero. Variation between seeds dominates.
  No structural intervention has moved c outside noise range so far. c is the
  bottleneck.

## Best library so far
- random uniform, seed=7 → eval_01 = 0.5241
- Variation 0.5174-0.5241 across 5 seeds; SD ~ 0.003
- Lucky seeds give marginally higher c

## Open questions
- Is c truly noise-bound from per-library design, or does it have a structural
  unlock we haven't found?
- Multi-seed best-of-N is the only known route to improvement
