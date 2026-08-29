# Exp 008: Natural DNA-like Markov chain (CpG-depleted)

## What
50k sequences from Markov-1 chain with human-like transitions (CpG depleted,
TG/CA enriched). Mapping A=0,C=1,G=2,T=3.

## Result (eval_01)
- mean = 0.3836 (vs random 0.4192) — clearly worse
- K562 = 0.5317 (vs 0.5902)
- HepG2 = 0.5554 (vs 0.6228)
- SKNSH = 0.0636 (vs 0.0445) — slightly higher

## Interpretation
Natural-DNA Markov sequences are MORE CONSTRAINED than random uniform — they have
smaller composition variance across the 50k. This reduces the variance available
for Pearson correlation, lowering r.

This suggests: random uniform is favored not because it's "natural" but because
it has MAXIMAL ENTROPY ACROSS THE 50k SET — providing the widest variance for
any feature both models track to correlate.

## Implications
- The scoring rewards SET-LEVEL VARIANCE in features both models care about.
- Random uniform has near-maximal entropy → near-maximal variance in all features.
- To beat random, we'd need to create MORE variance in specific features (without
  going OOD).
- Slight SKNSH bump (0.06 vs 0.04) is intriguing — Markov constraint may add some
  SKNSH-specific signal but at the cost of K562/HepG2.

## Time
~2 minutes.
