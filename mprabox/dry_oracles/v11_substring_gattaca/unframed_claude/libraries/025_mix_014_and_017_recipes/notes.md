# 025 — Mix 014 (3-motif) + 017 (50-bank) recipes

## Hypothesis
014's SKNSH-lift (small bank, structured) + 017's K562-lift (large bank,
unstructured) stacked in a 3-mode mix may exceed either alone.

## Result
- eval_01 mean=**0.8757** (K562 0.8529, HepG2 0.9100, SKNSH 0.8642)
- vs 017 (50-bank only): -0.006
- vs 014 (3-motif only): -0.005

## Interpretation
Diluting each insert flavor to half its strength kills both effects.
SKNSH lift (0.880 → 0.864) and K562 lift (0.862 → 0.853) both lost.
The two recipes don't stack — they require full-population coverage.

## Lesson
Per-flavor cluster signal requires full-population coverage. Mixing
insert flavors hurts on both axes.

## Next
026: try a tighter structural strict (block-stratified).
