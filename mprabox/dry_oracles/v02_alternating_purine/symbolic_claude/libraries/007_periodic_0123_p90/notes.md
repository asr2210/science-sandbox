# Exp 007 — periodic 0123, p_template = 0.9

## Design
Same pattern as Exp 006 (position i prefers base i mod 4) but with
stronger template adherence: p=0.9 vs 0.7.

## Result
eval_01 mean_r = 0.1307 (vs Exp 006's 0.1550). **Worse than p=0.7.**
condition_c dropped 0.41 → 0.36.

## Interpretation
There is a sweet spot in template strength. Too much structure
collapses library diversity → predictions cluster → lower correlation
magnitude. p=0.7 beat both p=1 (degenerate) and p=0.9.

## Next direction
Test whether it's specifically **period-4** ordering that helps, or
any per-position positional bias. Exp 008 will use a fixed *random*
preferred base per position (not periodic), at p=0.7. If similar to
006, positional bias alone is the lever. If different, periodicity
matters.
