# 016 markov_43_57

Markov chain p_stay=0.4 with rejection on [43,57] composition.

Result: eval_01 mean_r = **0.8420** (worse than 009's 0.8820).
- a: 0.828 (down from 0.856)
- b: 0.912 (≈ same)
- c: 0.787 (down from 0.881)

Within-string autocorrelation HURTS, especially c. i.i.d. random shuffle is optimal.

**Design rule confirmed:** within each sequence, characters should be placed
independently/randomly (random shuffle), not with local structure.

So winning recipe: [43,57] uniform-over-tuples composition + random shuffle within seq.
Next: try different SHAPES of composition distribution (uniform marginals).
