# Exp 023 — chr22 REPEAT-RICH windows (≥70% lowercase)

Inverse of exp 022. Keep windows that are mostly soft-masked repeats
(Alu/LINE/SINE). 35% acceptance from random sampling. GC mean=0.441
(repeat-rich is slightly AT-richer).

## Result

| metric  | chr22 random | chr22 non-repeat | chr22 repeat-rich |
|---------|-------------:|-----------------:|------------------:|
| eval_01 | 0.3202       | 0.3146           | 0.3009            |
| k562    | 0.1443       | 0.1307           | **0.1459** (+0.002) |
| hepg2   | 0.1990       | 0.1918           | 0.1930            |
| sknsh   | 0.6173       | 0.6212           | **0.5639** (-0.053) |

Confirms K562 SLIGHTLY likes repeats (+0.002 over random; +0.015 over
non-repeat). HepG2 unchanged. SKNSH HATES repeats (-0.053).

**Net story** (across exp 021-023):
- K562: rewards repetitive elements, capped near 0.15
- HepG2: needs higher-order natural structure, hates synthetic Markov
- SKNSH: prefers cleaner, less repetitive composition near 50% GC

**Implication**: chr22 random tiles ≈ Pareto optimum. It's the only
recipe that satisfies all three constraints simultaneously. Any move
away (filter, augment, synthesize) sacrifices one cell type's score.

**Remaining strategies for 024-030**:
1. Find a clever mix that nudges 0.001-0.005 over 0.3202
2. Test if multi-chromosome SAMPLING with chr1 diversity adds anything
3. Test chr22 + tiny HepG2-specific motif boost (HNF4)
