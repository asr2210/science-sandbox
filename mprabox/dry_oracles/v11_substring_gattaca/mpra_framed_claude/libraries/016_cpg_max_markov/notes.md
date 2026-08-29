# 016 CpG max: T[C→G]=0.80 at GC=0.55

50k 200bp sequences. Markov chain with T[C→G]=0.80, stationary GC=0.55,
realized CpG dinucleotide rate=0.219 (vs 0.179 in 015, vs iid 0.076).

## Result
- mean_r = 0.857 (eval_01 = 0.876)
- **DOWN** from 015 (0.868, 0.884) by -0.011 mean, -0.008 eval_01
- Worse than exp 012 (uniform GC=0.55, no CpG, 0.857)

Cell breakdown (avg easy evals):
| cell  | 015  | 016  | Δ     |
|-------|------|------|-------|
| K562  | 0.83 | 0.81 | -0.02 |
| HepG2 | 0.90 | 0.92 | +0.02 |
| SKNSH | 0.92 | 0.90 | -0.02 |

## Takeaway
**CpG is NOT monotone.** Pushing past T[C→G]=0.65 hurts overall.
- HepG2 keeps benefiting (loves CpG)
- K562 and SKNSH start losing
- Net: -0.011 mean

Likely cause: at 22% CpG dinucleotide rate, the sequences are far above
real CpG island levels (~10-15%). The training labels for these
unnaturally CG-dense sequences become uninformative because the simulator
saturates or extrapolates. Model can't generalize to natural eval sets.

**CpG peak found: T[C→G]≈0.65, CpG rate ≈ 0.18**

## Next
Try a different lever. Options:
1. TpA depletion on top of exp 015 setup (test additivity)
2. Try a single-cell-targeted signal — boost K562 specifically (since K562
   keeps dragging eval_08, eval_10)
3. Different dinucleotide: try ApG enrichment, GpC enrichment

Plan exp 017: stick with exp 015 (CpG=0.65) as base, add TpA depletion to
test if a second dinucleotide signal stacks additively.
