# Empirical findings so far (after exp 005)

## Quick reference table
| Library | eval_01 | Comment |
|---|---|---|
| 001 random uniform | 0.307 | composition floor |
| 002 natural genomic | 0.480 | clean naturalness baseline |
| 003 cCRE only (high-conf) | 0.345 | activity-range collapse |
| 004 natural+cCRE 50/50 | 0.494 | best so far |
| 005 synthetic motif + 40% GC bg | 0.155 | adversarial — worse than random |

## What works
- Natural genomic DNA (50K random windows from chr1-22,X,Y) is the strong
  baseline. Massive lift over random uniform.
- Mixing 25K natural + 25K cCRE gives small but consistent improvement
  over pure natural.

## What hurts
- Pure cCRE-only: collapses activity range; model can't tell active from
  inactive in eval.
- Pure synthetic motif insertion in random background: distribution shift
  is adversarial — worse than the original random baseline.

## Universal observations
- eval_08 always near 0.08-0.11 regardless of library. May be a stress
  test on something orthogonal to what natural DNA contains.
- K562_r always == HepG2_r exactly. Likely the eval label set treats them
  as one cell type (or the simulator does). Optimize mean_r; chase K562 ≡
  chase HepG2.
- SKNSH consistently slightly higher than K562/HepG2 across libraries.
- eval_07 is the easiest set; reaches ~0.60 with natural DNA.

## Working theory (T3)
A library is informative iff its sequence distribution **matches the
distribution of plausible regulatory genomes** the eval set is drawn from.
Within that constraint, motif content + activity-range diversity help.
Violating naturalness costs more than added motif density gains.

## Implications for further experiments
- Stay close to natural distribution.
- Test cheap augmentations on natural backbone (motif inserts in NATURAL bg,
  RC, slight shuffles).
- Test multi-source natural diversity (DHS index, FANTOM enhancers,
  multiple species).
- Avoid pure-synthetic, avoid all-cCRE.
