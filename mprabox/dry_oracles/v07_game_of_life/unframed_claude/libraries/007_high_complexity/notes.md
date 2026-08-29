# 007_high_complexity

## Hypothesis
Random uniform sequences contain ~8 runs of length ≥4 per 200bp by chance. If long runs hurt r, rejecting them should improve the score. Or: forcing anti-run structure might shift dinuc statistics enough to hurt.

## Method
- Generate 50,000 random uniform sequences via Markov sampling: when the last 3 bases are identical, forbid that base.
- Verified: no run > 3 in output.
- Per-seq GC still ~50% (binomial).
- Seed 42.

## Result
- **eval_01 mean_r = 0.3749** (K562=0.5877, HepG2=0.4104, SKNSH=0.1266)
- Significant drop of 0.023 vs random uniform (0.3981).
- All eval sets and cell lines down.

## Interpretation
The natural runs/binomial dinuc distribution of random uniform is *helpful*. Removing long runs (forcing flatter dinuc distribution) hurts the score noticeably.

This is consistent with theory T4: The metric prefers random uniform i.i.d. distribution. Even artificial flattening hurts. So:
- Real DNA (002, 003): different stats from random uniform → slight loss
- Bimodal/spread GC (004, 005): big stats deviation → big loss
- High complexity (007): different dinuc → small-medium loss

## Next
- 008: Test motif insertion (different lever)
- 009: Random uniform with different seed (noise-floor measurement)
- 010+: Targeted manipulations if motif results inform direction
