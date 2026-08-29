# Exp 017 — period-4 (0,1,2,3) with asymmetric noise

## Design
Per position i: template-base (i mod 4) at 0.7, next-cycle base at 0.2,
other two at 0.05 each. Asymmetric noise.

## Result
eval_01 mean_r = 0.1196 — worse than symmetric Exp 006 (0.1550).
condition_c ≈ 0.32.

## Interpretation
Symmetric noise (0.1 each for non-template bases) is better than
asymmetric. The hidden template's "secondary preference" hypothesis is
wrong — there's no benefit to biasing toward the next-cycle base.

## Next
Fine-tune p between 0.7 and 0.9. Test p=0.75.
