# 021_five_way_chip — notes

## Design
5-way mix: 17K nat + 13K cCRE off + 8K DHS + 7K ChIP (random) + 5K mouse.
Tests if ADDING ChIP (random sampling) as 5th source to exp 011 helps.

## Result
- eval_01 = 0.4992 (vs exp 011 = 0.5012, Δ = -0.002, within noise)
- eval_10 = 0.5466 (slight uptick over 011's 0.5451)
- eval_04 = 0.5168 (slight uptick over 011's 0.5180? no, -0.0012)
- Time: 17s (fastest yet)

## Interpretation
Adding ChIP as 5th source is statistically identical to 4-way. Confirms
exp 013's earlier finding (FANTOM5 as 5th source also neutral). The
plateau is FIXED for any combination of ≥4 atlas-derived sources.

## Pattern across exp 013, 015, 021
- exp 013 (5-way with FANTOM5): 0.4990
- exp 015 (ChIP substituted): 0.5002
- exp 021 (5-way with ChIP): 0.4992
- exp 011 (4-way): 0.5012
- exp 014 (4-way seed=1): 0.4971
- Mean of these 5: 0.4993, sd 0.0017

The "best design family" is centered at 0.4993 with sd ~0.002 across
random seeds and minor source-mix variations. The 0.5012 of exp 011
is a +1σ realization, not a fundamentally better design.

## Implication
Any further atlas-additive or atlas-substitutive experiment will land
in this band. Time to test something STRUCTURALLY different.

## Next test
3-way no-mouse: 25K nat + 15K cCRE + 10K DHS (no mouse component).
Tests if the mouse 5K is net-positive or net-negative. The 5K mouse
represents a strong distribution shift; if removing it helps, the
4-way mix benefits despite mouse, not because of it.
