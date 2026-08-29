# 016_ccre_plus_ctspecific

## Setup
40k cCREs (stratified) + 10k Malinois CT-specific (top by cross-CT std).
The cCRE base maintains the natural training distribution; the 10k
"spice" carries explicit cell-type-discriminator signal.

## Result
- eval_01 = 0.6914 vs cCRE-only 0.6921 (tied, −0.001)
- eval_04 = 0.6027 vs cCRE 0.5977 (+0.005, tiny lift; vs CT-specific
  alone +0.03)
- eval_07 = 0.7541 vs cCRE 0.7562 (−0.002)
- eval_10 = 0.6646 vs cCRE 0.6673 (−0.003)
- eval_08 = 0.1243 (tied)

## Interpretation
The 20% CT-specific spice dilutes its own signal: the eval_04 lift from
exp 015 (+0.03 when 100% CT-specific) shrinks to +0.005 here. The 80%
cCRE majority dominates the distribution.

So the cCRE-vs-CT-specific tradeoff is not "free": you have to spend
distribution mass to gain eval_04, and the cost shows up on eval_01.
A bit-for-bit lossy trade.

## Theory update → T8
For *eval_01 specifically*, the cCRE base is at a robust local maximum
that small additions can't improve. To break eval_01 I need a
fundamentally different signal source, not a remix of what I already
have.

## Takeaway
Pivot away from Malinois variants for the next experiments. Try
genuinely different annotation types: ChIP-seq peaks (direct TF
binding evidence) or per-cell-type DHS subsets refined by their
strongest co-evidence (e.g., DHS peaks with H3K27ac signal in
K562/HepG2/SKNSH).
