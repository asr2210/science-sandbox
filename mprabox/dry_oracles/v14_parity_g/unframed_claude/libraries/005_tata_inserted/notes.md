# 005 — TATA at pos 50, CAAT at pos 100

50K random sequences with TATAAA at fixed position 50 and CCAAT at position 100.

## Result
Near zero, no improvement. Slight negative shift on K562 (eval_01..05 K562 around -0.008). 
Fixed-position single-motif insertion does not unlock score. Makes sense: every sequence has the same motif at the same position, so this is a constant feature within the library.
