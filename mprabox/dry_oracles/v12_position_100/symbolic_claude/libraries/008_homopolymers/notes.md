# Exp 008: 4-corner homopolymers

## Setup
12.5K sequences each of "0"*200, "1"*200, "2"*200, "3"*200 (shuffled).
Only 4 distinct sequences across library.

## Results
WORSE than random (and much worse than Dir(0.3)):
- eval_01: 0.0774 (d0.3) → 0.0405 (homo)
- eval_07: 0.1479 → 0.0617
- eval_10: 0.1286 → 0.0223 (steep drop)

## Theory update
Confirms "saturation" hypothesis. Going to pure-corner gives 4 distinct predictions, but each only carries categorical info → limited correlation.

The sweet spot: BROAD composition coverage with diverse but not pure compositions. Dir(0.3) was best so far.

## Next
- Exp 009: Mixture: 12.5K each of Dir(0.1), Dir(0.3), Dir(1.0), Dir(3.0). Hybrid coverage.
- Or: deterministic simplex coverage.
