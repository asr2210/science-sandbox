# 022_even_wider

## Design
5K cCREs × 10 tiles with offsets in [-800, +800]. Many tiles miss
the regulatory element core entirely.

## Result
                eval_01  K562    HepG2   SKNSH   eval_13
020 wider 400:  0.3216   0.144   0.200   0.621   0.331
021 wider+RC:   0.3222   0.145   0.200   0.622   0.330
022 wider 800:  0.3221   0.143   0.202   0.621   0.333 ← new eval_13 high

Plateau holds at ~0.322. HepG2 inches up to 0.202.

## Interpretation
Context-breadth lever is saturated by ~±400. Going wider maintains
the lift but doesn't add. The HepG2 head is approaching a new
ceiling around 0.20-0.21 with the wider-tile family.

## Next
Experiment 023: combine wider tiling with EXPANDED REGION COUNT.
10K cCREs × 5 wider tiles = 50K. Tests whether wider tiles change
the saturation point (each wider tile carries more contextual
information, so the effective saturation may shift up or down).

Generalization: more diverse regulatory regions × context-aware
sampling = broader regulatory grammar exposure.
