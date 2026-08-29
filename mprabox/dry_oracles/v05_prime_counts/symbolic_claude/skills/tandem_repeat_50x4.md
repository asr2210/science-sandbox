# Skill: 50bp × 4 tandem repeat library

## When to use
Black-box DNA-like (alphabet {0,1,2,3}) scoring task where:
- Library size 50K × length 200
- Scoring is Pearson r between two per-sequence vectors
- Random uniform gives ~0.041 baseline on the primary metric
- You want a quick best-known structural improvement

## Recipe
```python
import random
random.seed(SEED)  # try several seeds; ~±0.0015 variance
N, L, UNIT = 50_000, 200, 50
ALPHA = "0123"
with open("sequences_0.txt", "w") as f:
    for _ in range(N):
        unit = "".join(random.choice(ALPHA) for _ in range(UNIT))
        f.write(unit * (L // UNIT) + "\n")
```

## Why it works
A 50bp unit repeated 4× across 200bp dramatically improves eval_08
(~0.12 → ~0.134) without losing other evals. The unit must:
- Divide the sequence length cleanly (50 divides 200 → ✓)
- Be long enough (≥50bp; 25, 20 fail)
- Be intact (10% random mutations destroy the gain)

## Don't bother trying
- AABB or other multi-segment tandem structures (worse than single)
- Embedding TF-like motifs in the unit (neutral)
- Mixing different period lengths (worse than pure 50×4)
- Palindromes / strand-symmetric sequences (strongly worse)
- Composition constraints tighter than natural binomial (worse)
