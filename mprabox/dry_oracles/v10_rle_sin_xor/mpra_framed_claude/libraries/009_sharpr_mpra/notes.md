# 009 — Sharpr-MPRA real sequences padded to 200bp

## Design
50k 145bp Sharpr-MPRA fragments (DNase-peak tilings from K562/HepG2/HUVEC/H1-hESC) sampled from the 914k training set. Padded to 200bp with random uniform flanks (27 left, 28 right).

## Result
- eval_01 mean_r = **0.4987** (vs random uniform 0.518, cCREs 0.496)
- K562 r = 0.929 — same drop as cCREs
- HepG2 r = 0.560 — basically same
- SK-N-SH r = 0.007 — small positive (first hint of signal but within noise)
- GC = 0.572 (Sharpr is GC-shifted high; this matches the K562 penalty pattern)

## Reading
Real MPRA-tested sequences don't help. The Sharpr GC bias (0.57) is the K562 limiter; the random flanks didn't bring composition back to 0.5 enough. SK-N-SH crept up to a barely-positive number (0.007), possibly the first real motif signal — but it's within noise.

## Implication
Even canonical real MPRA training data fails to beat random uniform. The benchmark is so composition-locked to binomial-GC=0.5 that real-DNA bias trumps any motif content benefit. Random uniform remains the champion.
