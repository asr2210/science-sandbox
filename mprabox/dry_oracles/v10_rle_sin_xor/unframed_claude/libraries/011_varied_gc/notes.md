# Experiment 011 — per-seq GC drawn uniform [0.2, 0.8]

## Result
- mean_r=**0.4684**, K562=0.8482, HepG2=0.5509, SKNSH=0.0063

## Interpretation
HepG2 stayed at 0.55, **NOT higher despite 5x more per-seq GC variance**
than baseline. K562 dropped to 0.85.

So HepG2 r doesn't grow monotonically with per-seq GC variance; it peaks
near natural Bin(200, 0.5) variance. K562 likes per-seq GC tight around 50%.
The sweet spot is essentially the random uniform baseline.

SKNSH crept positive (0.006) — possibly noise but interesting. Real chr21
also gave SKNSH=0.007. Both have natural per-seq GC variance similar to
baseline, but with non-uniform mean composition. Worth probing whether
realistic compositions help SKNSH minutely.
