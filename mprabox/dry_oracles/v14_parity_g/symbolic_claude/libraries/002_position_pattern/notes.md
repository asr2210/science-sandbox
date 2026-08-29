# 002 position-specific bias pattern

Each position p heavily biased toward char (p mod 4) with 70%, 10% others.
All 50K seqs share the same per-position pattern (but individually randomized).

Result: all conditions still ≈0. Even strong shared per-position bias gives
no signal. So the scorer is NOT rewarded by per-position character preferences
that are constant across the library.

Implication: the signal must vary BETWEEN sequences. Next: probe per-sequence
gradient where seq i encodes index i somehow.
