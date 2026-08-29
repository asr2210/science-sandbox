# Exp 007: 25k random + 25k natural

**Hypothesis**: Mixing would let each cell type see its preferred composition,
lifting mean_r above both component baselines.

**Results**:
- eval_01 mean=0.3967 (vs 0.4203 random, 0.3975 natural)
- K562=0.5437 (random 0.585, natural 0.541) → near natural
- HepG2=0.5577 (random 0.618, natural 0.552) → near natural
- SKNSH=0.0888 (random 0.059, natural 0.099) → near natural

**Interpretation**: Mix landed close to natural side rather than averaging
or exceeding both. The correlation metric does NOT compose linearly across
sub-libraries. Adding natural sequences pulled K562/HepG2 scores down
without lifting SKNSH proportionally.

Random alone is still the best for mean_r so far. Beating random requires
finding a perturbation that helps all 3 cell types simultaneously, or
helps the dominant K562/HepG2 axis more than SKNSH suffers.
