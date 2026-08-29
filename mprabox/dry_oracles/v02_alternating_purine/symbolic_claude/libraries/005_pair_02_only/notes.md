# Exp 005 — sequences using only {0, 2}

## Design
50,000 sequences (length 200), each position independently uniform from
{0, 2}. Per-sequence diversity is huge (2^200 possible), so per-sequence
predictions ought to vary — yet…

## Result
**All NaN** — same ConstantInputWarning as Exp 002.

## Interpretation
The constancy isn't about per-sequence diversity. It's about
**library-wide alphabet coverage**. When bases 1 and 3 never appear at
any position across the entire library, the scorer's internal feature
matrix has zero-variance columns (likely positional one-hot for the
missing bases), and Pearson r over that feature dimension is undefined.

## Big lesson
Every viable library MUST have all 4 bases present at every (or nearly
every) position across the 50,000 sequences. Any subset-restricted
library is a wasted submission. Going forward I'll only test biased
(not restricted) distributions.

## Lost budget
This is the second NaN-wasted submission (002 + 005). 5/30 used,
25 remaining.
