# 002 — single char

50,000 sequences split into 4 chunks of 12500, each chunk is a constant single character.

Result: ALL NaN. Triggered `ConstantInputWarning: An input array is constant; the correlation coefficient is not defined`.

**Big lesson:** The scoring uses Pearson r (or similar). For r to be defined, both arrays must be non-constant. Either:
- Per-sequence target arrays are constant when sequences are constant (likely: target depends on sequence content)
- Per-position features are constant within each chunk (composition-only sequences have no within-sequence variation)

In any case: NEVER submit a library where 50K sequences produce a constant-derived array.

Cost: 1 of 30 submissions wasted (now used 2).
